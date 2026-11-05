# -*- coding: utf-8 -*-
import json
DZ = json.load(open('res_designs.json'))
T = DZ['table']
AB = json.load(open('res_ablation.json'))
BS = json.load(open('res_bo_stats.json'))
MS = json.load(open('res_mc_stats.json'))
FE = json.load(open('res_fe2d.json'))


def f(v, n=2):
    return ('%.' + str(n) + 'f') % v


names = list(T.keys())
lab = ['D0 Kraft/NE', 'D1 Aramid-pulp proxy', 'D2 NFC presspaper', 'D3 BNNS/CNF paper', 'D4 $\\varepsilon$-minimised',
       'D5 Exact matching', 'D6 Robust uniform', 'D7 Robust graded', 'D8 Low-$\\varepsilon$ + D7 (hyp.)']
rows = []
for n, l in zip(names, lab):
    t = T[n]
    rows.append([l, f(t['eps']), f(t['tau60'], 1) + '/' + f(t['tau110'], 1), f(t['Ea']), f(t['util_mean'], 3),
                 f(t['util_max']), f(t['peak_oil_mean']) + '/' + f(t['peak_oil_max']),
                 f(t['peak_paper_mean'], 1) + '/' + f(t['peak_paper_max'], 1), '%d' % round(t['q_int_mean']),
                 f(t['iso_oil']), f(t['grad_oil'])])
TABLE_DES = dict(
    caption='Robust Comparison of Candidate Papers over the 40 Scenarios (Nominal Constants)',
    header=['Paper', '$\\varepsilon_p$', '$\\rho_\\tau$ 60/110 °C', '$E_a$ (eV)', '$J$', '$\\max u_s$',
            '$E_o^{\\max}$ mean/max', '$E_p^{\\max}$ mean/max', '$Q_i$', 'iso. oil', 'grad. oil'],
    rows=rows, widths=[1.35, 0.42, 0.72, 0.45, 0.48, 0.5, 0.82, 0.82, 0.42, 0.45, 0.47], wide=True,
    note='Fields in kV/mm, $Q_i$ in \u03bcC/m\u00b2. Graded papers are characterised by the middle barrier. '
         '“iso. oil”: mean $E_o^{\\max}$ over isothermal, unaged, $t_r$ = 10 s scenarios; '
         '“grad. oil”: mean over gradient scenarios.')

arows = []
J0 = AB['A0 Full']['util_mean']
for k, v in AB.items():
    arows.append([k.split(' ', 1)[1] if k != 'A0 Full' else 'Full design (D7)', f(v['util_mean'], 3),
                  ('+%.1f' % (100 * (v['util_mean'] / J0 - 1))) if k != 'A0 Full' else '–',
                  f(v['peak_oil_mean']), f(v['peak_paper_mean'], 1), '%d' % round(v['q_int_mean'])])
TABLE_ABL = dict(caption='Ablation Study (Each Variant Re-Optimised, Judged on All 40 Scenarios)',
                 header=['Variant', '$J$', '$\\Delta J$ (%)', '$E_o^{\\max}$', '$E_p^{\\max}$', '$Q_i$'],
                 rows=arows, widths=[1.45, 0.42, 0.45, 0.42, 0.42, 0.38], wide=False)

brows = []
def sci(v):
    m, e = ('%.1e' % v).split('e')
    return '%s\u00d710$^{%d}$' % (m, int(e))
for m, nm in [('gpei', 'GP-EI'), ('cma', 'CMA-ES'), ('random', 'Random'), ('sobol', 'Sobol')]:
    b = BS[m]
    brows.append([nm, '%.4f' % b['med'], '%.4f\u2013%.4f' % (b['q1'], b['q3']), '%d/15' % round(15 * b['hit_frac']),
                  ('%.0f' % b['hit_med']) if b['hit_med'] and b['hit_frac'] > 0.3 else '\u2013',
                  ('%.4f' % b['p_holm']) if 'p_holm' in b else '\u2013', ('%.2f' % b['rbc']) if 'rbc' in b else '\u2013'])
TABLE_BO = dict(caption='Final Simple Regret after 80 Evaluations over 15 Paired Seeds',
                header=['Method', 'Median', 'IQR', 'Within 0.5%', 'Evals', '$p_{\\mathrm{Holm}}$', '$r_{rb}$'],
                rows=brows, widths=[0.52, 0.5, 0.95, 0.5, 0.36, 0.5, 0.36], wide=True,
                note='Regret in kV/mm. \u201cEvals\u201d: median evaluations to reach 0.5% of $J^\\star$ among successful runs; tests compare each method with GP-EI.')

mrows = []
for k, nm in [('aramid_proxy', 'D1 Aramid proxy'), ('strict', 'D5 Exact match'), ('uniform', 'D6 Robust unif.'),
              ('graded', 'D7 Robust graded')]:
    s = MS[k]
    mrows.append([nm, '%.2f (%.2f, %.2f)' % (s['mean'], s['lo'], s['hi']), '%.1f/%.1f' % (s['p5'], s['p95']),
                  '%.2f' % s['pos'], '%.1f' % s['oil'], '%.1f' % s['pap'], '%.1f' % s['q']])
TABLE_MC = dict(caption='Monte-Carlo Robustness of the Gain over Kraft Paper (300 Paired Draws)',
                header=['Paper', '$\\overline{g}$ % (95% CI)', 'P5/P95', '$P(g>0)$', 'oil %', 'paper %', '$Q_i$ %'],
                rows=mrows, widths=[0.8, 0.95, 0.6, 0.45, 0.35, 0.42, 0.38], wide=True,
                note='Last three columns: mean relative reduction of scenario-mean $E_o^{\\max}$, $E_p^{\\max}$ and $Q_i$; negative values are increases.')

frows = []
for sc, scl in [('110-70', '110→70 °C'), ('85-85', '85 °C')]:
    for d, dn in [('Kraft/NE', 'D0'), ('Exact window matching', 'D5'), ('Robust graded', 'D7')]:
        r = FE['%s|%s' % (sc, d)]
        frows.append([scl, dn, f(r['1.0']['oil']), f(r['0.5']['oil']), f(r['oil_rich']), f(r['1.0']['pap'], 1),
                      f(r['0.5']['pap'], 1), f(r['pap_rich'], 1)])
TABLE_FE = dict(caption='2-D Axisymmetric Verification ($t_r$ = 10 s, Unaged) with Mesh Refinement',
                header=['Profile', 'Paper', '$E_o^{\\max}$ $h$=1', '$h$=0.5', 'extrap.', '$E_p^{\\max}$ $h$=1', '$h$=0.5', 'extrap.'],
                rows=frows, widths=[0.62, 0.35, 0.48, 0.42, 0.45, 0.48, 0.42, 0.45], wide=True,
                note='Fields in kV/mm; extrapolation by (24).')

LY = json.load(open('res_layers.json'))
TABLE_LAY = dict(caption='Layer-Resolved Properties of the Robust Graded Paper D7',
                 header=['Layer', '$c_l$', '$\\varepsilon_p$', '$\\sigma_p$ 50 \u00b0C (fS/m)', '$E_a$ (eV)',
                         '$\\rho_\\tau$ 60/85/110 \u00b0C', 'ionic share'],
                 rows=[[['wrap', 'barrier 1', 'barrier 2', 'barrier 3', 'barrier 4'][r['layer']], '%.2f' % r['c'],
                        '%.2f' % r['eps'], '%.0f' % (r['s50'] * 1e15), '%.3f' % r['Ea'],
                        '%.1f/%.1f/%.1f' % tuple(r['tr']), '%.2f' % r['ion_frac']] for r in LY],
                 widths=[0.6, 0.38, 0.38, 0.62, 0.45, 0.85, 0.48], wide=False,
                 note='$c_l$ in mmol/g; ionic share is the fraction of $\\sigma_p$ carried by the carboxylate channel at 85 \u00b0C.')
KP = json.load(open('res_kappa.json'))
TABLE_KAP = dict(caption='Effect of the Design-Stress Ratio on the Graded Optimum',
                 header=['$\\kappa$', '$w_A$/$w_C$', '$c_w$/$c_k$', '$\\rho_\\tau$ 60/110 \u00b0C', '$g$ (%)',
                         '$E_o^{\\max}$', '$E_p^{\\max}$'],
                 rows=[['%g' % float(k), '%.2f/%.2f' % (KP[k]['v'][0], KP[k]['v'][1]),
                        '%.2f/%.2f' % (KP[k]['v'][2], KP[k]['v'][3]), '%.1f/%.1f' % (KP[k]['tau60'], KP[k]['tau110']),
                        '%.1f' % KP[k]['gain'], '%.2f' % KP[k]['oil'], '%.1f' % KP[k]['pap']]
                       for k in sorted(KP, key=float)],
                 widths=[0.3, 0.6, 0.6, 0.65, 0.38, 0.42, 0.42], wide=False,
                 note='Kraft reference: $E_o^{\\max}$ = %.2f kV/mm and $E_p^{\\max}$ = %.1f kV/mm (scenario means); $w_B$ = 0.10 at every optimum.' % (KP['3.0']['oil0'], KP['3.0']['pap0']))

g = lambda k, m: T[k][m]
K0, K5, K7, K6, K1, K8 = names[0], names[5], names[7], names[6], names[1], names[8]
pct = lambda a, b: 100 * (a / b - 1)

RESULTS = [
    ('h1', 'V. RESULTS'),
    ('h2', 'A. Mechanism: Exact Matching under Isothermal and Gradient Conditions (RQ1)'),
    ('p', '{F:fig3_mechanism}a maps the isothermal oil overshoot $\\Gamma_o$ at 85 °C against the relaxation-time ratio and the '
          'reversal time, using a kraft-permittivity paper whose conductivity is scaled to give the prescribed '
          '$\\rho_\\tau$. At $\\rho_\\tau$ = 1 the overshoot equals one for every reversal time, as (11) and (16) '
          'require. At $\\rho_\\tau$ = 10 it rises to 1.61 for a 1 s reversal, 1.20 for 10 s and falls below one '
          '(0.47) for 120 s, because a slow ramp lets the interface charge relax while the voltage is still small. '
          '{F:fig3_mechanism}b shows the corresponding interface charge, which is zero at $\\rho_\\tau$ = 1 and grows to about '
          '4200 \u03bcC/m\u00b2 at $\\rho_\\tau$ = 10, together with the paper field, which climbs above four times its '
          'capacitive value as the paper becomes the resistive member of the stack. Under isothermal conditions '
          'exact matching therefore does what the theory promises.'),
    ('p', '{F:fig3_mechanism}c adds a radial temperature drop $\\Delta T$ centred on 85 °C. Without a gradient the best '
          'ratio is 1.26 (grid resolution) and the oil peak equals the capacitive field. With $\\Delta T$ = 20 K the '
          'best ratio moves to 3.2 and the oil peak to 1.36 times capacitive, against 1.60 at $\\rho_\\tau$ = 1; '
          'with $\\Delta T$ = 40 K the best ratio is 2.5 with 2.06, against 2.29 at exact matching. Repeating the '
          'map with the paper activation energy set equal to that of the oil lowered the best value at 40 K to 1.82, '
          'whereas a steeper 1.4 eV paper raised it to 2.19. A gradient therefore moves the optimum away from '
          'exact matching toward a moderately resistive paper whose conductivity tracks the oil’s temperature '
          'dependence, as the bulk-charge term (12) predicts.'),
    ('fig', 'fig3_mechanism.png', 'Mechanism maps for a kraft-permittivity paper with prescribed relaxation-time '
            'ratio $\\rho_\\tau$ at 85 °C. (a) Isothermal oil overshoot $\\Gamma_o$ versus reversal time. (b) '
            'Isothermal interface charge and normalised paper peak for $t_r$ = 10 s. (c) Peak oil field over the '
            'whole sequence, normalised by the capacitive field, versus radial temperature drop. White dashed lines '
            'mark exact matching.', True),
    ('p', '{F:fig4_traces} follows the hardest scenario (110→70 °C, $t_r$ = 10 s, unaged) through the first reversal. '
          'Kraft paper holds 28.5 kV/mm in the cold barriers before reversal, and its oil peak reaches 11.1 kV/mm '
          'about 7 s after the ramp ends, when the stored interface charge adds to the reversed capacitive field. '
          'The exactly matched D5 nearly removes that transient overshoot, but the stack then settles to a DC oil '
          'field of 13.1 kV/mm in the cold gap, above every transient of the other two papers. The robust graded D7 '
          'lies between: its overshoot peaks at 9.9 kV/mm, its DC oil field settles at 7.5 kV/mm and its barrier '
          'field at 21.9 kV/mm. Across the full scenario set ({T:TABLE_DES}) D5 cut the mean interface charge by '
          '%.0f%% and the isothermal fast-reversal oil peak by %.1f%% relative to kraft, but raised the gradient-'
          'scenario oil peak by %.1f%% and the robust utilisation by %.1f%%. The answer to RQ1 is negative: exact '
          'matching is not robust once thermal gradients are present.' % (
              -pct(g(K5, 'q_int_mean'), g(K0, 'q_int_mean')), -pct(g(K5, 'iso_oil'), g(K0, 'iso_oil')),
              pct(g(K5, 'grad_oil'), g(K0, 'grad_oil')), pct(g(K5, 'util_mean'), g(K0, 'util_mean')))),
    ('fig', 'fig4_traces.png', 'Field histories after the first reversal in the hardest scenario (110→70 °C, '
            '$t_r$ = 10 s, unaged). Open circles show the steady DC values just before the reversal starts. (a) '
            'Largest oil-gap field. (b) Largest solid-layer field.', True),
    ('h2', 'B. Robust Composition (RQ2)'),
    ('p', '{T:TABLE_DES} and {F:fig5_designs} compare the nine papers. The robust graded optimum D7 has $w_A$ = 0.35, '
          '$w_C$ = 0.12, $w_B$ = 0.10 and a carboxylate content rising from 1.02 mmol/g in the wrap to 1.68 mmol/g '
          'next to the core. Its sheet permittivity is 4.47, its porosity 0.21 and its 50 °C conductivity '
          '89–137 fS/m from wrap to core, 1.6–2.5 times that of kraft, with an apparent activation energy of '
          '0.87–0.89 eV. The resulting ratio $\\rho_\\tau$ runs from 9.5 at 60 °C to 2.7 at 110 °C in the middle '
          'barrier: well short of matching. Relative to kraft, D7 lowered the robust utilisation from %s to %s kV/mm '
          '(%.1f%%), the worst-case utilisation by %.1f%%, the mean barrier peak by %.1f%%, the largest barrier peak '
          'by %.1f%% and the mean interface charge by %.1f%%. The mean oil peak fell by %.1f%%, while the largest '
          'oil peak over all scenarios rose from %s to %s kV/mm (%.1f%%). The uniform optimum D6 reached a '
          'utilisation %.1f%% below kraft with a lower barrier peak than D7 but a higher oil peak, so grading '
          'mainly buys oil-side relief.' % (
              f(g(K0, 'util_mean'), 3), f(g(K7, 'util_mean'), 3), -pct(g(K7, 'util_mean'), g(K0, 'util_mean')),
              -pct(g(K7, 'util_max'), g(K0, 'util_max')), -pct(g(K7, 'peak_paper_mean'), g(K0, 'peak_paper_mean')),
              -pct(g(K7, 'peak_paper_max'), g(K0, 'peak_paper_max')), -pct(g(K7, 'q_int_mean'), g(K0, 'q_int_mean')),
              -pct(g(K7, 'peak_oil_mean'), g(K0, 'peak_oil_mean')), f(g(K0, 'peak_oil_max')), f(g(K7, 'peak_oil_max')),
              pct(g(K7, 'peak_oil_max'), g(K0, 'peak_oil_max')), -pct(g(K6, 'util_mean'), g(K0, 'util_mean')))),
    ('table', 'TABLE_DES'),
    ('p', 'The literature proxies behave as their design intent suggests. The aramid-pulp proxy D1, with its '
          'permittivity reduced to 3.34, gave the lowest mean oil peak of the manufacturable candidates and a '
          'utilisation %.1f%% below kraft, but left the barrier stress unchanged. The NFC presspaper D2 was neutral. '
          'The BNNS/CNF paper D3 and the permittivity-minimised D4 were worse than kraft (utilisation +%.1f%% and '
          '+%.1f%%), because their lower conductivity widens the relaxation mismatch and loads the barriers. The '
          'hypothetical D8 shows that the two levers add: placing the D7 conductivity profile on the D1 matrix '
          'lowered the utilisation by %.1f%% and the mean oil peak by %.1f%%. The ohmic dissipation density stayed '
          'below 4.2 kW/m\u00b3 for every candidate, and D7 raised the through-plane thermal conductivity only from '
          '0.190 to 0.201 W/(m·K), so flat-lying BNNS acts here mainly as a conduction regulator.' % (
              -pct(g(K1, 'util_mean'), g(K0, 'util_mean')), pct(T[names[3]]['util_mean'], g(K0, 'util_mean')),
              pct(T[names[4]]['util_mean'], g(K0, 'util_mean')), -pct(g(K8, 'util_mean'), g(K0, 'util_mean')),
              -pct(g(K8, 'peak_oil_mean'), g(K0, 'peak_oil_mean')))),
    ('fig', 'fig5_designs.png', 'Scenario-mean metrics of the nine candidate papers relative to kraft (dashed '
            'line). Squares: proposed robust designs; open diamond: hypothetical combination D8.', True),
    ('p', '{T:TABLE_LAY} resolves D7 layer by layer. The carboxylate channel carries 68\u201378%% of the conductivity at '
          '85 \u00b0C, and the grading lowers $\\rho_\\tau$ from the wrap to the core-side barrier at every temperature, '
          'so the coldest barriers, which face the coldest oil, are the least resistive. {F:fig_space}a places the nominal '
          'designs in the stress plane spanned by %d uniform compositions. The compositions form a narrow band: '
          'moving along it trades barrier stress for oil stress, and exact matching (D5) sits at the low-barrier, '
          'high-oil end. Kraft lies above the band, so it is dominated: a uniform composition exists that lowers '
          'both stresses at once, and D6 and D7 sit near the knee. {F:fig_space}b shows the carboxylate response at '
          'fixed $w_C$ and $w_B$. Without ANF the utilisation is lowest near 0.6 mmol/g and rises again as the paper '
          'becomes too conductive; with more ANF the minimum moves to higher carboxylate content and becomes '
          'deeper, because the higher dissociation energy of a low-permittivity sheet tempers the ionic channel.' % len(json.load(open('res_space.json')))),
    ('table', 'TABLE_LAY'),
    ('fig', 'fig_space.png', '(a) Scenario-mean oil and barrier peaks of uniform compositions on a regular grid, '
            'shaded by the robust utilisation, with the nominal designs marked. (b) Robust utilisation versus '
            'carboxylate content for four ANF fractions at $w_C$ = 0.15 and $w_B$ = 0.10.', True),
    ('h2', 'C. Sample Efficiency of the Design Loop (RQ3)'),
    ('p', '{F:fig6_bo} and {T:TABLE_BO} compare the optimisers on the 5-D graded problem, where $J^\\star$ = 7.2003 kV/mm. '
          'GP-EI ended with a median regret of %.1e kV/mm and came within 0.5%% of $J^\\star$ in all 15 runs '
          '(median %d evaluations). CMA-ES reached that band in 10 runs and finished with a regret 17 times larger; '
          'random and Sobol search reached it once each. GP-EI was better than every competitor in the paired '
          'comparison (Holm-corrected $p$ = %.1e, rank-biserial correlation 0.98–1.00). During the first 30 '
          'evaluations all methods were comparable; the advantage of the surrogate appears once it has enough points '
          'to locate the narrow valley along the carboxylate direction.' % (
              BS['gpei']['med'], round(BS['gpei']['hit_med']), BS['cma']['p_holm'])),
    ('fig', 'fig6_bo.png', 'Simple regret of the four optimisers (median over 15 seeds, shaded inter-quartile '
            'range). The first ten GP-EI evaluations are the Sobol initial design.', False),
    ('table', 'TABLE_BO'),
    ('h2', 'D. Ablation'),
    ('p', '{T:TABLE_ABL} and {F:fig7_ablation_sobol}a remove one ingredient at a time and re-optimise the rest. Removing the carboxylate '
          'channel had the largest effect (+8.4% in $J$): without it the optimiser falls back to almost plain kraft. '
          'Designing with the dissociation coupling switched off and then judging the design with it switched on '
          'cost 3.0%, because the uncoupled model overestimates the ionic conduction of low-permittivity sheets and '
          'selects too little B-CNF. An isothermal objective cost 2.4%: it chose a more conductive paper '
          '(barrier peak 11.0 kV/mm, interface charge 1916 \u03bcC/m\u00b2) whose oil peak was the highest of all '
          'variants. Removing BNNS, ANF or the radial grading cost 1.7%, 1.4% and 1.1%. Dropping the ageing '
          'states (+0.3%) or the fast reversal (+0.0%) from the objective hardly changed the optimum, which shows '
          'that the thermal profiles decide the composition far more than the reversal time or ageing do.'),
    ('table', 'TABLE_ABL'),
    ('h2', 'E. Sensitivity and Robustness'),
    ('p', '{F:fig7_ablation_sobol}b gives the Sobol indices of the gain $g$ of D7 over kraft. The ester conductivity at 50 °C '
          'dominated (total index 0.56, first-order 0.26), followed by the ionic gain (0.41) and the cellulose '
          'permittivity (0.35); the ANF permittivity and the BNNS aspect ratio contributed about 0.1 each and all '
          'other inputs, including both oil and paper activation energies and the ageing multiplier, less than 0.06. '
          'The first-order indices add up to about 0.62, so interactions carry the remaining variance: a more '
          'conductive ester calls for a more conductive paper, and the ionic gain decides whether the fixed '
          'composition supplies it. Across the Sobol sample the gain averaged 4.5% and was positive in 86% of the '
          'model evaluations.'),
    ('fig', 'fig7_ablation_sobol.png', '(a) Increase of the robust utilisation when one ingredient or objective '
            'element is removed and the rest re-optimised. (b) Total and first-order Sobol indices of the gain of D7 '
            'over kraft; bars show 95% confidence intervals of the total index.', True),
    ('p', '{T:TABLE_MC} and {F:fig8_mc} report the paired Monte-Carlo study. With compositions frozen at their nominal '
          'optima, D7 kept a mean gain of %.2f%% (95%% CI %.2f–%.2f%%), positive in %.0f%% of draws '
          '(Wilcoxon $p<10^{-30}$). D6 behaved similarly with a smaller mean. Exact matching D5 had a negative '
          'mean gain of %.2f%% with a 5th percentile of %.1f%%, and was better than kraft in only half of the draws. '
          'The aramid proxy D1 gained %.2f%% in every draw, with a narrow spread, because its benefit comes from '
          'permittivity alone; its gain did not differ significantly from that of D7 ($p$ = 0.58). {F:fig8_mc}b shows why '
          'the two achieve similar totals by different means: D7 lowers the paper term of the utilisation in most '
          'draws while its oil stress moves along the diagonal.' % (
              MS['graded']['mean'], MS['graded']['lo'], MS['graded']['hi'], 100 * MS['graded']['pos'],
              MS['strict']['mean'], MS['strict']['p5'], MS['aramid_proxy']['mean'])),
    ('table', 'TABLE_MC'),
    ('fig', 'fig8_mc.png', 'Robustness over 300 paired parameter draws. (a) Empirical distribution of the gain over '
            'kraft. (b) Scenario-mean oil peaks and scaled paper peaks of D7 against kraft; points below the '
            'diagonal favour D7.', True),
    ('p', 'The design-stress ratio $\\kappa$ encodes how much stronger the impregnated barriers are than the oil, '
          'and it moves the optimum continuously ({T:TABLE_KAP}). With $\\kappa$ = 2 the barriers matter as much as '
          'the oil, the optimum approaches matching ($\\rho_\\tau$ = 4.0 at 60 \u00b0C and 1.4 at 110 \u00b0C) and '
          'the gain over kraft reaches %.1f%%, mostly through a 36%% lower barrier peak. With $\\kappa$ = 4 and 6 '
          'the optimiser accepts higher barrier stress, steepens the grading (core-side carboxylate at the bound, '
          'wrap-side content falling toward zero) and keeps a %.1f\u2013%.1f%% gain through the oil term alone. The '
          'gain stayed positive over the whole range, so the qualitative conclusion does not hinge on the nominal '
          '$\\kappa$, but the furnish does.' % (KP['2.0']['gain'], KP['6.0']['gain'], KP['4.0']['gain'])),
    ('table', 'TABLE_KAP'),
    ('h2', 'F. Verification and 2-D Field Check'),
    ('p', 'The modal ladder agreed with stiff BDF integration of the same equations to a relative error below '
          '$10^{-9}$ for both a two-layer case and the full stack. For planar isothermal layers the 2-D solver gave '
          'a paper peak of 9.919 kV/mm against 9.917 kV/mm from the ladder; its oil peak converged at first order '
          '(5.53 and 5.76 kV/mm at $h$ = 1 and 0.5 mm), and the extrapolated 5.99 kV/mm lies within 0.4%% of the '
          'ladder value of 6.01 kV/mm. {T:TABLE_FE} and {F:fig9_fe2d} give the axisymmetric results. In the hardest scenario '
          'the extrapolated worst oil field was %s kV/mm for kraft, %s kV/mm for D5 and %s kV/mm for D7, a %.1f%% '
          'reduction for D7 and a %.1f%% increase for D5, in the same order as the 1-D model. The high-stress region '
          'sits in the cold barriers and oil gaps near the core, while the winding corner and the washer are not '
          'critical in this geometry. At a uniform 85 °C the three oil peaks lay within 6%% of one another and '
          'D7 had the highest wrap-corner field (23.7 kV/mm against 20.3 kV/mm for kraft), because its wrap carries '
          'the least carboxylate of the five layers.' % (
              f(FE['110-70|Kraft/NE']['oil_rich']), f(FE['110-70|Exact window matching']['oil_rich']),
              f(FE['110-70|Robust graded']['oil_rich']),
              -pct(FE['110-70|Robust graded']['oil_rich'], FE['110-70|Kraft/NE']['oil_rich']),
              pct(FE['110-70|Exact window matching']['oil_rich'], FE['110-70|Kraft/NE']['oil_rich']))),
    ('table', 'TABLE_FE'),
    ('fig', 'fig9_fe2d.png', 'Field magnitude in the 2-D model for the hardest scenario: steady DC just before the '
            'first reversal (top) and 5 s after the reversal ramp ends (bottom). Gray outlines: solid layers; black '
            'outline: winding copper.', True),
]
