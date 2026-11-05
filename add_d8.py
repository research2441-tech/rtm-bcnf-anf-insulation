"""Adds D8: hypothetical low-permittivity matrix (aramid-pulp proxy) carrying the D7 conductivity profile."""
import json, numpy as np, mw1d, design as D, props as pp
dz = json.load(open('res_designs.json'))
kr = mw1d.designed_material(pp.KRAFT)
mat = [mw1d.Material(0.704 * kr.eps, m.sig) for m in D.materials(dz['opt_graded']['v'])]
s, rows = D.evaluate(mat)
m0 = mat[2]
s['tau60'] = float((m0.eps / m0.sig(333.15)) / (pp.NOMINAL['eps_ne'] / pp.oil_conductivity(333.15)))
s['tau110'] = float((m0.eps / m0.sig(383.15)) / (pp.NOMINAL['eps_ne'] / pp.oil_conductivity(383.15)))
s['Ea'] = float(pp.KB * np.log(m0.sig(383.15) / m0.sig(333.15)) / (1 / 333.15 - 1 / 383.15))
iso = [r for r in rows if r['scen'][0] == r['scen'][1] and r['scen'][3] == 1 and r['scen'][4] == 1 and r['scen'][2] == 10.0]
grad = [r for r in rows if r['scen'][0] != r['scen'][1]]
s['iso_oil'] = float(np.mean([r['peak_oil'] for r in iso])); s['iso_q'] = float(np.mean([r['q_int'] for r in iso]))
s['grad_oil'] = float(np.mean([r['peak_oil'] for r in grad])); s['grad_dcoil'] = float(np.mean([r['dc_oil'] for r in grad]))
dz['table']['D8 Low-eps matrix + D7 tuning (hypothetical)'] = s
json.dump(dz, open('res_designs.json', 'w'), indent=1, default=float)
for k, v in dz['table'].items():
    print('%-46s J=%.3f max=%.2f oil=%.2f/%.2f pap=%.2f/%.2f q=%.0f iso=%.2f grad=%.2f leak=%.0f g=%.2f' % (k, v['util_mean'], v['util_max'], v['peak_oil_mean'], v['peak_oil_max'], v['peak_paper_mean'], v['peak_paper_max'], v['q_int_mean'], v['iso_oil'], v['grad_oil'], v['leak_max'], v['gamma_mean']))
print({k: dz[k]['v'] for k in ['opt_graded', 'opt_uniform', 'strict_match', 'eps_min']})
print({k: dz[k]['k_through'] for k in ['opt_graded', 'opt_uniform']})
