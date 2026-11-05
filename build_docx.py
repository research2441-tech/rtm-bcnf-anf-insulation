# -*- coding: utf-8 -*-
"""Builds the manuscript on the supplied IEEE Transactions master template."""
import copy, os, re, sys
from lxml import etree
import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import omml
import sec_front as F, sec_rw as RWm, sec_method as ME, sec_exp as EX, sec_results as RE, sec_disc as DI

TEMPLATE = os.environ.get('IEEE_TEMPLATE', 'ieee_template.docx')
OUT = sys.argv[1] if len(sys.argv) > 1 else 'manuscript.docx'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

# ------------------------------------------------------------------ references
REFS = {}
for line in open('refs_raw.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if not line.strip():
        continue
    k, au, ti, jo, vol, iss, pg, yr, doi = line.split('|')
    REFS[k] = dict(au=au, ti=ti, jo=jo, vol=vol, iss=iss, pg=pg, yr=yr, doi=doi)
ORDER = []


def cite_numbers(keys):
    nums = []
    for k in keys:
        assert k in REFS, 'unknown ref ' + k
        if k not in ORDER:
            ORDER.append(k)
        nums.append(ORDER.index(k) + 1)
    assert len(nums) <= 3, 'more than 3 refs in one bracket: %s' % keys
    nums = sorted(set(nums))
    if len(nums) == 3 and nums[2] - nums[0] == 2:
        return '[%d]–[%d]' % (nums[0], nums[2])
    return '[' + ', '.join(str(n) for n in nums) + ']'


CITE_RE = re.compile(r'\[@([^\]]+)\]')


def resolve_cites(text):
    text = re.sub(r'\{F:([A-Za-z0-9_]+)\}', lambda m: 'Fig. %d' % FIGNUM[m.group(1)], text)
    text = re.sub(r'\{T:([A-Za-z0-9_]+)\}', lambda m: 'Table %s' % ROMAN[TABNUM[m.group(1)] - 1], text)
    return CITE_RE.sub(lambda m: cite_numbers([s.strip().lstrip('@') for s in m.group(1).split(';')]), text)


# ------------------------------------------------------------------ numbering of floats
COUNTERS = dict(eq=0, fig=0, tab=0)
FIGNUM, TABNUM = {}, {}
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
STATS = dict(display=0, inline=0)

doc = docx.Document(TEMPLATE)
body = doc.element.body
paras = doc.paragraphs
# keep title/abstract section; collect sectPr templates
sect_title = paras[7]._p.find(qn('w:pPr')).find(qn('w:sectPr'))
sect_two = copy.deepcopy(paras[88]._p.find(qn('w:pPr')).find(qn('w:sectPr')))
for s in [sect_title, sect_two]:
    for fr in s.findall(qn('w:footerReference')) + s.findall(qn('w:headerReference')):
        s.remove(fr)
sect_one = copy.deepcopy(sect_two)
sect_one.find(qn('w:cols')).attrib.pop(qn('w:num'))
# remove the drafting box (first table) and everything after paragraph 7
first_table = doc.tables[0]._tbl
first_table.getparent().remove(first_table)
p7 = paras[7]._p
started = False
for el in list(body):
    if el is p7:
        started = True
        continue
    if started and el.tag != qn('w:sectPr'):
        body.remove(el)
final_sect = body.find(qn('w:sectPr'))
for fr in final_sect.findall(qn('w:footerReference')) + final_sect.findall(qn('w:headerReference')):
    final_sect.remove(fr)
final_sect.find(qn('w:cols')).set(qn('w:num'), '2')
typ = final_sect.find(qn('w:type'))
if typ is None:
    typ = etree.SubElement(final_sect, qn('w:type'))
    final_sect.remove(typ)
    final_sect.insert(0, typ)
typ.set(qn('w:val'), 'continuous')
# remove footer/header parts entirely so nothing appears there
for rel in list(doc.part.rels.values()):
    if rel.reltype.endswith('/footer') or rel.reltype.endswith('/header'):
        doc.part.drop_rel(rel.rId)

# ------------------------------------------------------------------ helpers
MATH_RE = re.compile(r'(\$[^$]+\$|<b>|</b>)')


def add_runs(p, text, size=None, bold=False, italic=False):
    """Append text with inline $math$ and <b> tags to paragraph p."""
    text = resolve_cites(text)
    parts = MATH_RE.split(text)
    b = bold
    for part in parts:
        if not part:
            continue
        if part == '<b>':
            b = True; continue
        if part == '</b>':
            b = bold; continue
        if part.startswith('$') and part.endswith('$') and len(part) > 1:
            om = omml.convert([part[1:-1]])[0]
            if size:
                for r in om.iter('{%s}r' % omml.M):
                    rpr = r.find(qn('w:rPr'))
                    if rpr is not None:
                        sz = etree.SubElement(rpr, qn('w:sz')); sz.set(qn('w:val'), str(int(size * 2)))
            p._p.append(om)
            STATS['inline'] += 1
        else:
            r = p.add_run(part)
            r.bold = b or None
            r.italic = italic or None
            if size:
                r.font.size = Pt(size)


def para(style='Normal', align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph(style=style)
    if align is not None:
        p.alignment = align
    return p


def section_break(sect):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    ppr = p._p.get_or_add_pPr()
    ppr.append(copy.deepcopy(sect))
    return p


STATE = dict(wide=False)


def ensure_wide(wide):
    if wide and not STATE['wide']:
        section_break(sect_two)      # closes the preceding two-column section
        STATE['wide'] = True
    elif not wide and STATE['wide']:
        section_break(sect_one)      # closes the single-column (wide) section
        STATE['wide'] = False


def heading(text, level):
    ensure_wide(False)
    style = 'IEEE Section' if level == 1 else 'IEEE Subsection'
    p = para(style, None)
    add_runs(p, text)
    if level == 1:
        p.paragraph_format.keep_with_next = True
    else:
        p.paragraph_format.keep_with_next = True


def body_par(text):
    ensure_wide(False)
    p = para()
    add_runs(p, text)


def equation(latex):
    ensure_wide(False)
    COUNTERS['eq'] += 1
    om = omml.convert([latex])[0]
    p = para()
    p._p.append(omml.display(om, COUNTERS['eq']))
    STATS['display'] += 1


def figure(path, caption, wide):
    ensure_wide(wide)
    COUNTERS['fig'] += 1
    p = para(None, WD_ALIGN_PARAGRAPH.CENTER)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=Inches(7.0 if wide else 3.4))
    c = para('Figure Caption', WD_ALIGN_PARAGRAPH.JUSTIFY)
    add_runs(c, 'Fig. %d. ' % COUNTERS['fig'] + caption, size=8)


def set_cell_border(cell, **kw):
    tcPr = cell._tc.get_or_add_tcPr()
    b = tcPr.find(qn('w:tcBorders'))
    if b is None:
        b = etree.SubElement(tcPr, qn('w:tcBorders'))
    for edge, val in kw.items():
        e = b.find(qn('w:' + edge))
        if e is None:
            e = etree.SubElement(b, qn('w:' + edge))
        e.set(qn('w:val'), val); e.set(qn('w:sz'), '4'); e.set(qn('w:space'), '0'); e.set(qn('w:color'), '000000')


def fix_widths(t, widths_in):
    tbl = t._tbl
    tblPr = tbl.tblPr
    for tag in ('w:tblW', 'w:tblLayout'):
        e = tblPr.find(qn(tag))
        if e is not None:
            tblPr.remove(e)
    tw = etree.SubElement(tblPr, qn('w:tblW'))
    tw.set(qn('w:w'), str(int(sum(widths_in) * 1440))); tw.set(qn('w:type'), 'dxa')
    lay = etree.SubElement(tblPr, qn('w:tblLayout')); lay.set(qn('w:type'), 'fixed')
    grid = tbl.tblGrid
    for gc in list(grid):
        grid.remove(gc)
    for w in widths_in:
        gc = etree.SubElement(grid, qn('w:gridCol')); gc.set(qn('w:w'), str(int(w * 1440)))
    for row in t.rows:
        for c, w in zip(row.cells, widths_in):
            c.width = Inches(w)


def table(spec):
    ensure_wide(spec.get('wide', False))
    COUNTERS['tab'] += 1
    c = para('Table Caption', WD_ALIGN_PARAGRAPH.CENTER)
    c.paragraph_format.keep_with_next = True
    r = c.add_run('TABLE %s' % ROMAN[COUNTERS['tab'] - 1])
    r.add_break()
    cap = re.sub(r'(\$[^$]+\$)|([^$]+)', lambda m: m.group(1) if m.group(1) else m.group(2).upper(), spec['caption'])
    add_runs(c, cap)
    rows = [spec['header']] + spec['rows']
    t = doc.add_table(rows=len(rows), cols=len(spec['header']))
    t.style = doc.styles['Table Grid']
    t.alignment = 1
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            cell.width = Inches(spec['widths'][j])
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            add_runs(p, val, size=7.5, bold=(i == 0))
    for row in t.rows:
        trpr = row._tr.get_or_add_trPr()
        cs = etree.SubElement(trpr, qn('w:cantSplit'))
    widths = spec['widths']
    total = 7.0 if spec.get('wide') else 3.4
    sc = total / sum(widths)
    fix_widths(t, [w * sc for w in widths])
    if spec.get('note'):
        n = para(None, WD_ALIGN_PARAGRAPH.JUSTIFY)
        n.paragraph_format.space_before = Pt(2)
        add_runs(n, spec['note'], size=7)
    else:
        sp = para(None)
        sp.paragraph_format.space_after = Pt(2)


def algorithm(title, lines):
    ensure_wide(False)
    t = doc.add_table(rows=2, cols=1)
    t.alignment = 1
    c0 = t.cell(0, 0); c1 = t.cell(1, 0)
    fix_widths(t, [3.4])
    set_cell_border(c0, top='single', bottom='single', left='nil', right='nil')
    set_cell_border(c1, top='single', bottom='single', left='nil', right='nil')
    p = c0.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
    add_runs(p, '<b>' + title.split(':')[0] + ':</b>' + title.split(':', 1)[1], size=8)
    first = True
    for ln in lines:
        p = c1.paragraphs[0] if first else c1.add_paragraph()
        first = False
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        add_runs(p, ln, size=8)
    sp = para(None); sp.paragraph_format.space_after = Pt(2)


# ------------------------------------------------------------------ title block
P = doc.paragraphs
P[1].text = ''
P[1].add_run(F.TITLE)
P[2].text = ''
P[2].add_run(F.AUTHORS)
P[3].text = ''
P[3].add_run(F.AFFIL)
for i, (lab, txt) in [(5, ('Abstract—', F.ABSTRACT)), (6, ('Index Terms—', F.INDEX_TERMS))]:
    p = P[i]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    rr = p.add_run(lab); rr.bold = True; rr.italic = True
    add_runs(p, txt)


# ------------------------------------------------------------------ body
def emit(blocks, tables=None):
    for b in blocks:
        kind = b[0]
        if kind == 'h1':
            heading(b[1], 1)
        elif kind == 'h2':
            heading(b[1], 2)
        elif kind == 'p':
            body_par(b[1])
        elif kind == 'eq':
            equation(b[1])
        elif kind == 'fig':
            figure(b[1], b[2], b[3])
        elif kind == 'table':
            table(tables[b[1]])
        elif kind == 'alg':
            algorithm(b[1], b[2])


mb = ME.METHOD
k = [i for i, b in enumerate(mb) if b[0] == 'h2' and b[1].startswith('B.')][0]
ALL = F.INTRO + RWm.RW + [('table', 'TABLE_LIT')] + mb[:k] + [('table', 'TABLE_PARAM')] + mb[k:] + EX.EXP + \
    RE.RESULTS + DI.DISC + DI.BACK
TABLES = dict(TABLE_CONTRIB=F.TABLE_CONTRIB, TABLE_LIT=RWm.TABLE_LIT, TABLE_PARAM=ME.TABLE_PARAM, TABLE_DES=RE.TABLE_DES,
              TABLE_ABL=RE.TABLE_ABL, TABLE_BO=RE.TABLE_BO, TABLE_MC=RE.TABLE_MC, TABLE_FE=RE.TABLE_FE,
              TABLE_LAY=RE.TABLE_LAY, TABLE_KAP=RE.TABLE_KAP)
for b_ in ALL:
    if b_[0] == 'fig':
        FIGNUM[b_[1].rsplit('.', 1)[0]] = len(FIGNUM) + 1
    elif b_[0] == 'table':
        TABNUM[b_[1]] = len(TABNUM) + 1
P = doc.paragraphs
for i_, (lab, txt) in [(5, ('Abstract\u2014', F.ABSTRACT)), (6, ('Index Terms\u2014', F.INDEX_TERMS))]:
    pass
emit(ALL, TABLES)

# ------------------------------------------------------------------ references
heading('REFERENCES', 1)
missing = [k for k in REFS if k not in ORDER]
assert not missing, 'uncited references: %s' % missing


def fmt_ref(n, r):
    s = '[%d] %s, “%s,” ' % (n, r['au'], r['ti'])
    if r['jo'].startswith('Proc.') or r['jo'].startswith('IEC'):
        s += '<i>%s</i>' % r['jo']
    else:
        s += '<i>%s</i>' % r['jo']
    if r['vol']:
        s += ', vol. %s' % r['vol']
    if r['iss']:
        s += ', no. %s' % r['iss']
    if r['pg']:
        if r['pg'][0].isalpha() or ('-' not in r['pg'] and r['pg'].replace('e', '').isdigit()):
            s += ', Art. no. %s' % r['pg']
        elif r['pg'].startswith('Geneva'):
            s += ', %s' % r['pg']
        else:
            s += ', pp. %s' % r['pg'].replace('-', '–')
    s += ', %s' % r['yr']
    if r['doi']:
        s += ', doi: %s' % r['doi']
    return s + '.'


for n, k in enumerate(ORDER, 1):
    p = para(None, WD_ALIGN_PARAGRAPH.JUSTIFY)
    pf = p.paragraph_format
    pf.left_indent = Inches(0.28); pf.first_line_indent = Inches(-0.28); pf.space_after = Pt(1)
    txt = fmt_ref(n, REFS[k])
    for part in re.split(r'(<i>.*?</i>)', txt):
        if not part:
            continue
        if part.startswith('<i>'):
            rr = p.add_run(part[3:-4]); rr.italic = True
        else:
            rr = p.add_run(part)
        rr.font.size = Pt(8)
ensure_wide(False)
doc.save(OUT)
print('saved', OUT, 'equations', COUNTERS['eq'], 'figs', COUNTERS['fig'], 'tables', COUNTERS['tab'],
      'refs', len(ORDER), 'inline math', STATS['inline'])
