"""Design-space map (uniform designs on a grid) and kappa sweep of the graded optimum."""
import json, itertools, sys
import numpy as np
from scipy.optimize import differential_evolution
import design as D
if sys.argv[1] == 'grid':
    g = [np.linspace(0, 0.35, 6), np.linspace(0.05, 0.30, 6), np.linspace(0, 1.7, 9), np.linspace(0, 0.10, 3)]
    out = []
    for v in itertools.product(*g):
        v = np.array(v)
        if not D.feasible(np.r_[v[:3], v[2], v[3]]):
            continue
        s, _ = D.evaluate(np.r_[v[:3], v[2], v[3]])
        out.append([*v, s['util_mean'], s['peak_oil_mean'], s['peak_paper_mean'], s['q_int_mean']])
    json.dump(out, open('res_space.json', 'w'))
else:
    res = {}
    for kap in [2.0, 4.0, 6.0]:
        r = differential_evolution(lambda v: D.objective(v, kappa=kap), [tuple(b) for b in D.BOUNDS], seed=5,
                                   maxiter=25, popsize=10, tol=1e-6, polish=True)
        s, _ = D.evaluate(r.x, kappa=kap)
        k0, _ = D.evaluate(np.array([0, 0.05, 0, 0, 0]), kappa=kap)
        res[kap] = dict(v=r.x.tolist(), J=float(r.fun), J0=float(k0['util_mean']), oil=s['peak_oil_mean'],
                        pap=s['peak_paper_mean'], oil0=k0['peak_oil_mean'], pap0=k0['peak_paper_mean'])
        print(kap, res[kap], flush=True)
    json.dump(res, open('res_kappa.json', 'w'), indent=1)
