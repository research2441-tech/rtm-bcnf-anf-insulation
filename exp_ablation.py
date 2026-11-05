"""E5: component and objective ablations; each variant is re-optimised and then judged on the full scenario set."""
import json, time
import numpy as np
from scipy.optimize import differential_evolution
import props as pp, design as D

B = [tuple(b) for b in D.BOUNDS]
ISO = [(60, 60), (85, 85), (110, 110)]


def opt(fun, bounds, seed=3):
    r = differential_evolution(fun, bounds, seed=seed, maxiter=30, popsize=10, tol=1e-6, polish=True)
    return r.x


def variant(name, make_v, bounds, design_kw=None, design_P=None):
    kw = design_kw or {}
    P = design_P or pp.NOMINAL
    t0 = time.time()
    x = opt(lambda z: D.objective(make_v(z), P=P, **kw), bounds)
    v = make_v(x)
    s, rows = D.evaluate(v)                       # judged with the nominal model on all 40 scenarios
    print('%-30s J=%.3f oil=%.2f pap=%.2f q=%.0f  v=%s  %.0fs' % (name, s['util_mean'], s['peak_oil_mean'],
          s['peak_paper_mean'], s['q_int_mean'], np.round(v, 3), time.time() - t0), flush=True)
    return dict(v=list(map(float, v)), **{k: s[k] for k in ['util_mean', 'util_max', 'peak_oil_mean', 'peak_oil_max',
                                                           'peak_paper_mean', 'q_int_mean']})


if __name__ == '__main__':
    out = {}
    full = lambda z: np.asarray(z)
    out['A0 Full'] = variant('A0 Full', full, B)
    out['A1 no ANF'] = variant('A1 no ANF', lambda z: np.r_[0.0, z], B[1:])
    out['A2 no carboxylate'] = variant('A2 no carboxylate', lambda z: np.r_[z[0], z[1], 0, 0, z[2]], [B[0], B[1], B[4]])
    out['A3 no BNNS'] = variant('A3 no BNNS', lambda z: np.r_[z, 0.0], B[:4])
    out['A4 no grading'] = variant('A4 no grading', lambda z: np.r_[z[:3], z[2], z[3]], [B[0], B[1], B[2], B[4]])
    out['A5 isothermal objective'] = variant('A5 isothermal objective', full, B, dict(t_scen=ISO))
    out['A6 no ageing scenarios'] = variant('A6 no ageing scenarios', full, B, dict(age_scen=[(1.0, 1.0)]))
    out['A7 slow reversal only'] = variant('A7 slow reversal only', full, B, dict(tr_scen=[120.0]))
    Pn = dict(pp.NOMINAL); Pn['couple'] = False
    out['A8 no dissociation coupling'] = variant('A8 no dissociation coupling', full, B, design_P=Pn)
    json.dump(out, open('res_ablation.json', 'w'), indent=1)
