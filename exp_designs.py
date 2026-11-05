"""E3: reference optima and comparison of candidate papers over the 40-scenario set."""
import json, time
import numpy as np
from scipy.optimize import differential_evolution
import props as pp, mw1d, design as D

T_WIN = np.linspace(333.15, 383.15, 11)


def de_opt(fun, bounds, seed=0, maxiter=40, popsize=12):
    r = differential_evolution(fun, bounds, seed=seed, maxiter=maxiter, popsize=popsize, tol=1e-6,
                               polish=True, updating='deferred', workers=1)
    return r.x, r.fun, r.nfev


def strict_match_loss(v4):
    x = D.to_x(v4)
    if not D.feasible(np.r_[v4[:2], v4[2], v4[2], v4[3]]):
        return 1e3
    lr = np.log(pp.tau_ratio(x, T_WIN))
    return float(np.mean(lr ** 2))


def eps_loss(v4):
    x = D.to_x(np.r_[v4[0], v4[1], 0.0, v4[2]])
    if (v4[0] + v4[1] + v4[2]) > 0.6:
        return 1e3
    return float(pp.permittivity(x))


def main():
    out = {}
    t0 = time.time()
    b5 = [tuple(b) for b in D.BOUNDS]
    b4 = [b5[0], b5[1], b5[2], b5[4]]
    # proposed graded (5-D) and uniform (4-D) robust optima
    vg, fg, ng = de_opt(lambda v: D.objective(v), b5, seed=1)
    vu, fu, nu = de_opt(lambda v: D.objective(np.r_[v[:3], v[2], v[3]]), b4, seed=1)
    out['opt_graded'] = dict(v=vg.tolist(), J=fg, nfev=int(ng))
    out['opt_uniform'] = dict(v=np.r_[vu[:3], vu[2], vu[3]].tolist(), J=fu, nfev=int(nu))
    vs, fs, _ = de_opt(strict_match_loss, b4, seed=1)
    out['strict_match'] = dict(v=np.r_[vs[:3], vs[2], vs[3]].tolist(), loss=fs)
    ve, fe, _ = de_opt(eps_loss, [b5[0], b5[1], b5[4]], seed=1)
    out['eps_min'] = dict(v=[ve[0], ve[1], 0.0, 0.0, ve[2]], eps=fe)
    print('optimisation done %.0fs' % (time.time() - t0))

    kr = mw1d.designed_material(pp.KRAFT)
    designs = {
        'D0 Kraft/NE': kr,
        'D1 Aramid-pulp hybrid proxy': mw1d.Material(0.704 * kr.eps, kr.sig),
        'D2 NFC presspaper proxy': mw1d.designed_material(dict(w_a=0, w_c=0.10, c=0, w_b=0)),
        'D3 BNNS/CNF paper proxy': mw1d.designed_material(dict(w_a=0, w_c=0.10, c=0, w_b=0.05)),
        'D4 Permittivity-minimised': D.materials(out['eps_min']['v']),
        'D5 Exact window matching': D.materials(out['strict_match']['v']),
        'D6 Robust uniform (proposed)': D.materials(out['opt_uniform']['v']),
        'D7 Robust graded (proposed)': D.materials(out['opt_graded']['v']),
    }
    table = {}
    for name, mat in designs.items():
        s, rows = D.evaluate(mat)
        m0 = mat[2] if isinstance(mat, list) else mat
        s['tau60'] = float((m0.eps / m0.sig(333.15)) / (pp.NOMINAL['eps_ne'] / pp.oil_conductivity(333.15)))
        s['tau110'] = float((m0.eps / m0.sig(383.15)) / (pp.NOMINAL['eps_ne'] / pp.oil_conductivity(383.15)))
        s['Ea'] = float(pp.KB * np.log(m0.sig(383.15) / m0.sig(333.15)) / (1 / 333.15 - 1 / 383.15))
        # isothermal, new, fast-reversal subset (the mechanism the matching idea targets)
        iso = [r for r in rows if r['scen'][0] == r['scen'][1] and r['scen'][3] == 1 and r['scen'][4] == 1
               and r['scen'][2] == 10.0]
        grad = [r for r in rows if r['scen'][0] != r['scen'][1]]
        s['iso_oil'] = float(np.mean([r['peak_oil'] for r in iso]))
        s['iso_q'] = float(np.mean([r['q_int'] for r in iso]))
        s['grad_oil'] = float(np.mean([r['peak_oil'] for r in grad]))
        s['grad_dcoil'] = float(np.mean([r['dc_oil'] for r in grad]))
        table[name] = s
        print('%-32s J=%.3f oil=%.2f/%.2f pap=%.2f q=%.0f iso_oil=%.2f grad_oil=%.2f eps=%.2f Ea=%.2f tau60=%.2f tau110=%.2f'
              % (name, s['util_mean'], s['peak_oil_mean'], s['peak_oil_max'], s['peak_paper_mean'], s['q_int_mean'],
                 s['iso_oil'], s['grad_oil'], s['eps'], s['Ea'], s['tau60'], s['tau110']))
    out['table'] = table
    for k in ['opt_graded', 'opt_uniform', 'strict_match', 'eps_min']:
        v = out[k]['v']
        out[k]['comp_mid'] = D.to_x(v)
        out[k]['k_through'] = float(pp.thermal_conductivity(D.to_x(v)))
    json.dump(out, open('res_designs.json', 'w'), indent=1, default=float)
    print('total %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
