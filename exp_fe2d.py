"""E8: 2-D axisymmetric verification of the design ranking (worst thermal scenario, fast reversal)."""
import json, time
import numpy as np
import props as pp, mw1d, design as D, fe2d

dz = json.load(open('res_designs.json'))
DES = {'Kraft/NE': mw1d.designed_material(pp.KRAFT),
       'Exact window matching': D.materials(dz['strict_match']['v']),
       'Robust graded': D.materials(dz['opt_graded']['v'])}
SCEN = [(110, 70), (85, 85)]


def to_list(mat):
    return mat if isinstance(mat, list) else [mat] * 5


if __name__ == '__main__':
    out = {}
    t_dc = mw1d.T_STEP['pre']
    for (th, tc) in SCEN:
        for name, mat in DES.items():
            rec = {}
            for h in (1.0, 0.5):
                g = fe2d.Geometry(h=h)
                t0 = time.time()
                snaps = [('dc', t_dc - 1.0), ('rev', t_dc + 10.0 + 5.0)] if h == 1.0 else []
                o = fe2d.run_pr(g, to_list(mat), th, tc, t_r=10.0, snapshots=snaps)
                rec[h] = dict(oil=float(o['peak_oil']), pap=float(o['peak_paper']), sec=time.time() - t0)
                if h == 1.0:
                    rec['trace'] = dict(t=o['t'].tolist(), oil=o['oil_max'].tolist(), pap=o['pap_max'].tolist())
                    rec['maps'] = {k: dict(t=v[0], E=v[1][::2, ::2].round(3).tolist()) for k, v in o['snaps'].items()}
                    rec['geom'] = dict(mat=g.mat[::2, ::2].tolist(), r=g.rc[::2].tolist(), z=g.zc[::2].tolist())
                    rec['T'] = o['T'][::2, ::2].round(2).tolist()
                print((th, tc), name, h, rec[h], flush=True)
            rec['oil_rich'] = 2 * rec[0.5]['oil'] - rec[1.0]['oil']
            rec['pap_rich'] = 2 * rec[0.5]['pap'] - rec[1.0]['pap']
            out['%d-%d|%s' % (th, tc, name)] = {str(k): v for k, v in rec.items()}
    json.dump(out, open('res_fe2d.json', 'w'))
