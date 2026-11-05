"""LaTeX-subset -> native Word OMML via pandoc (batch conversion, cached)."""
import subprocess, tempfile, os, zipfile, copy, hashlib, json
from lxml import etree

M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'m': M, 'w': W}
_cache = {}


def convert(snippets):
    """Return list of <m:oMath> elements (one per LaTeX snippet)."""
    todo = [s for s in snippets if s not in _cache]
    if todo:
        with tempfile.TemporaryDirectory() as td:
            md = os.path.join(td, 'm.md')
            with open(md, 'w') as f:
                for s in todo:
                    f.write('$' + s + '$\n\n')
            out = os.path.join(td, 'm.docx')
            subprocess.run(['pandoc', md, '-f', 'markdown+tex_math_dollars', '-o', out], check=True)
            xml = zipfile.ZipFile(out).read('word/document.xml')
            root = etree.fromstring(xml)
            paras = root.findall('.//w:body/w:p', NS)
            assert len(paras) == len(todo), (len(paras), len(todo))
            for s, p in zip(todo, paras):
                om = p.findall('.//m:oMath', NS)
                if len(om) != 1:
                    raise ValueError('bad math: ' + s)
                _style(om[0])
                _cache[s] = om[0]
    return [copy.deepcopy(_cache[s]) for s in snippets]


def _style(om):
    """Give every math run Cambria Math; drop empty separator characters."""
    for sc in list(om.iter('{%s}sepChr' % M)):
        if sc.get('{%s}val' % M, '') == '':
            sc.getparent().remove(sc)
    # default round delimiters are written the way the template writes them (no explicit characters)
    for dpr in om.iter('{%s}dPr' % M):
        b = dpr.find('{%s}begChr' % M); e = dpr.find('{%s}endChr' % M)
        if b is not None and e is not None and b.get('{%s}val' % M) == '(' and e.get('{%s}val' % M) == ')':
            dpr.remove(b); dpr.remove(e)
            g = dpr.find('{%s}grow' % M)
            if g is not None:
                dpr.remove(g)
    for r in om.iter('{%s}r' % M):
        rpr = r.find('{%s}rPr' % W)
        if rpr is None:
            rpr = etree.SubElement(r, '{%s}rPr' % W)
            r.remove(rpr)
            # w:rPr must follow m:rPr if present
            mrpr = r.find('{%s}rPr' % M)
            idx = 1 if mrpr is not None else 0
            r.insert(idx, rpr)
        f = etree.SubElement(rpr, '{%s}rFonts' % W)
        f.set('{%s}ascii' % W, 'Cambria Math'); f.set('{%s}hAnsi' % W, 'Cambria Math')


def display(om, number):
    """Template layout: oMathPara > oMath > 4-column matrix [ , eq, , (n)]."""
    para = etree.Element('{%s}oMathPara' % M)
    o = etree.SubElement(para, '{%s}oMath' % M)
    mm = etree.SubElement(o, '{%s}m' % M)
    mpr = etree.SubElement(mm, '{%s}mPr' % M)
    ph = etree.SubElement(mpr, '{%s}plcHide' % M); ph.set('{%s}val' % M, '1')
    mcs = etree.SubElement(mpr, '{%s}mcs' % M)
    mc = etree.SubElement(mcs, '{%s}mc' % M)
    mcpr = etree.SubElement(mc, '{%s}mcPr' % M)
    c = etree.SubElement(mcpr, '{%s}count' % M); c.set('{%s}val' % M, '4')
    j = etree.SubElement(mcpr, '{%s}mcJc' % M); j.set('{%s}val' % M, 'center')
    mr = etree.SubElement(mm, '{%s}mr' % M)
    etree.SubElement(mr, '{%s}e' % M)
    e2 = etree.SubElement(mr, '{%s}e' % M)
    for ch in list(om):
        e2.append(ch)
    etree.SubElement(mr, '{%s}e' % M)
    e4 = etree.SubElement(mr, '{%s}e' % M)
    r = etree.SubElement(e4, '{%s}r' % M)
    rpr = etree.SubElement(r, '{%s}rPr' % M)
    etree.SubElement(rpr, '{%s}nor' % M)
    t = etree.SubElement(r, '{%s}t' % M); t.text = '(%d)' % number
    return para


if __name__ == '__main__':
    o = convert([r'\rho_\tau(T)=\frac{\varepsilon_p\,\sigma_o(T)}{\varepsilon_o\,\sigma_p(T)}', r'E_{o}^{\max}'])
    print(etree.tostring(o[0])[:400])
