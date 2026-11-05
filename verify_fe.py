"""Verification of the 2-D solver against the exact 1-D ladder solution (planar layers, isothermal)."""
import numpy as np, time, json, props as pp, mw1d, fe2d
res={}
mats=mw1d.designed_material(pp.KRAFT)
for h in (1.0, 0.5):
    g=fe2d.Geometry(h=h, planar=True, r_shift=1e5)
    t0=time.time()
    o=fe2d.run_pr(g, mats, 85, 85, t_r=10.0)
    res[h]=dict(oil=float(o['peak_oil']), pap=float(o['peak_paper']), sec=time.time()-t0, n=g.nr*g.nz)
    print(h,res[h])
# 1-D reference: stack is axisymmetric in 2-D; compare with planar 1-D (curvature effect small: r~306-357)
r=mw1d.pr_sequence(mats, T_hot=358.15, T_cold=358.15, t_r=10.0)
print('1D', r['peak_oil'], r['peak_paper'])
res['1d']=dict(oil=float(r['peak_oil']), pap=float(r['peak_paper']))
json.dump(res, open('verify_fe.json','w'), indent=1)
