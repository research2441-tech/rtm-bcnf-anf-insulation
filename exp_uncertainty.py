"""E6 Sobol sensitivity and E7 Monte-Carlo robustness of the design ranking."""
import json, sys, time
import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol
import props as pp, mw1d, design as D

dz = json.load(open('res_designs.json'))
V_GR = np.array(dz['opt_graded']['v'])
V_UN = np.array(dz['opt_uniform']['v'])
V_SM = np.array(dz['strict_match']['v'])

PROBLEM = dict(
    names=['eps_cell', 'eps_anf', 'p0', 'beta_fill', 'Ea_b', 'log_sig_o', 'Ea_o_ne', 'log_ion_gain',
           'E_mu', 'a_pair', 'alpha_bn', 'age_factor'],
    bounds=[[5.0, 7.0], [3.0, 4.2], [0.30, 0.50], [0.20, 0.60], [0.90, 1.20], [np.log10(0.3e-12), np.log10(3e-12)],
            [0.30, 0.90], [np.log10(3.0), np.log10(30.0)], [0.35, 0.55], [0.35, 0.55], [20.0, 100.0], [2.0, 8.0]])
PROBLEM['num_vars'] = len(PROBLEM['names'])


def make_P(row):
    P = dict(pp.NOMINAL)
    for n, val in zip(PROBLEM['names'], row):
        if n == 'log_sig_o':
            P['sig_o50_ne'] = 10 ** val
        elif n == 'log_ion_gain':
            P['ion_gain'] = 10 ** val
        elif n == 'age_factor':
            continue
        else:
            P[n] = val
    a = row[PROBLEM['names'].index('age_factor')]
    age = [(1.0, 1.0), (a, 1.0), (1.0, a), (a, a)]
    return P, age


def J_of(mat_fn, P, age):
    rows = D.scenario_metrics(mat_fn(P), P, age_scen=age)
    return float(np.mean([r['util'] for r in rows])), float(np.mean([r['peak_oil'] for r in rows])), \
        float(np.mean([r['peak_paper'] for r in rows])), float(np.mean([r['q_int'] for r in rows]))


MATS = {
    'kraft': lambda P: mw1d.designed_material(pp.KRAFT, P),
    'aramid_proxy': lambda P: (lambda m: mw1d.Material(0.704 * m.eps, m.sig))(mw1d.designed_material(pp.KRAFT, P)),
    'strict': lambda P: D.materials(V_SM, P),
    'uniform': lambda P: D.materials(V_UN, P),
    'graded': lambda P: D.materials(V_GR, P),
}


def run_sobol(N):
    X = saltelli.sample(PROBLEM, N, calc_second_order=False)
    Y = np.zeros((len(X), 2))
    t0 = time.time()
    for i, row in enumerate(X):
        P, age = make_P(row)
        jk = J_of(MATS['kraft'], P, age)[0]
        jg = J_of(MATS['graded'], P, age)[0]
        Y[i] = [1 - jg / jk, jg]
        if i % 500 == 0:
            print('sobol', i, len(X), '%.0fs' % (time.time() - t0), flush=True)
    out = {}
    for k, lab in enumerate(['rel_gain', 'J_graded']):
        S = sobol.analyze(PROBLEM, Y[:, k], calc_second_order=False, print_to_console=False)
        out[lab] = dict(S1=S['S1'].tolist(), S1_conf=S['S1_conf'].tolist(), ST=S['ST'].tolist(),
                        ST_conf=S['ST_conf'].tolist())
    out['names'] = PROBLEM['names']
    out['Y_summary'] = dict(gain_mean=float(Y[:, 0].mean()), gain_p05=float(np.percentile(Y[:, 0], 5)),
                            gain_p95=float(np.percentile(Y[:, 0], 95)), frac_pos=float((Y[:, 0] > 0).mean()))
    return out


def run_mc(N, seed=11):
    rng = np.random.default_rng(seed)
    lo = np.array([b[0] for b in PROBLEM['bounds']]); hi = np.array([b[1] for b in PROBLEM['bounds']])
    X = lo + rng.random((N, len(lo))) * (hi - lo)
    res = {k: [] for k in MATS}
    t0 = time.time()
    for i, row in enumerate(X):
        P, age = make_P(row)
        for k, fn in MATS.items():
            res[k].append(J_of(fn, P, age))
        if i % 100 == 0:
            print('mc', i, '%.0fs' % (time.time() - t0), flush=True)
    return {k: np.array(v).tolist() for k, v in res.items()}


if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'sobol':
        json.dump(run_sobol(int(sys.argv[2])), open('res_sobol.json', 'w'))
    else:
        json.dump(run_mc(int(sys.argv[2])), open('res_mc.json', 'w'))
