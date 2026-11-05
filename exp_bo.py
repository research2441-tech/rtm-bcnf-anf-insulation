"""E4: sample efficiency of constrained GP-EI Bayesian optimisation versus baselines (5-D graded design)."""
import json, time, sys, warnings
import numpy as np
from scipy.stats import qmc, norm
from scipy.optimize import minimize
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel, WhiteKernel
import cma
import design as D

warnings.filterwarnings('ignore')
LB, UB = D.BOUNDS[:, 0], D.BOUNDS[:, 1]
DIM = len(LB)
BUDGET = 80
N_INIT = 10


def scale(u):
    return LB + np.asarray(u) * (UB - LB)


def f_unit(u):
    v = scale(u)
    if not D.feasible(v):
        return None
    return D.objective(v)


def feasible_unit(U):
    V = scale(U)
    return (V[:, 0] + V[:, 1] + V[:, 4]) <= 0.60


def sample_feasible(n, rng, sobol=None):
    out = []
    while len(out) < n:
        U = sobol.random(64) if sobol is not None else rng.random((64, DIM))
        out.extend(U[feasible_unit(U)])
    return np.array(out[:n])


def run_random(seed):
    rng = np.random.default_rng(seed)
    U = sample_feasible(BUDGET, rng)
    return [f_unit(u) for u in U]


def run_sobol(seed):
    s = qmc.Sobol(DIM, scramble=True, seed=seed)
    U = sample_feasible(BUDGET, None, s)
    return [f_unit(u) for u in U]


def run_cma(seed):
    ys = []
    es = cma.CMAEvolutionStrategy([0.5] * DIM, 0.3, {'bounds': [0, 1], 'seed': seed + 1, 'verbose': -9,
                                                      'popsize': 8})
    while len(ys) < BUDGET:
        X = es.ask()
        F = []
        for x in X:
            y = f_unit(x)
            if y is None:
                F.append(20.0)            # infeasible: penalised, still counts toward the budget
                ys.append(np.nan)
            else:
                F.append(y)
                ys.append(y)
            if len(ys) >= BUDGET:
                break
        if len(F) == len(X):
            es.tell(X, F)
    return ys[:BUDGET]


def expected_improvement(gp, X, ybest, xi=0.01):
    mu, sd = gp.predict(X, return_std=True)
    sd = np.maximum(sd, 1e-9)
    z = (ybest - mu - xi) / sd
    return (ybest - mu - xi) * norm.cdf(z) + sd * norm.pdf(z)


def run_gpei(seed):
    rng = np.random.default_rng(seed)
    s = qmc.Sobol(DIM, scramble=True, seed=seed)
    X = list(sample_feasible(N_INIT, None, s))
    y = [f_unit(u) for u in X]
    kern = ConstantKernel(1.0, (1e-3, 1e3)) * Matern(length_scale=np.full(DIM, 0.3),
                                                     length_scale_bounds=(1e-2, 1e1), nu=2.5) \
        + WhiteKernel(1e-6, (1e-9, 1e-2))
    while len(y) < BUDGET:
        gp = GaussianProcessRegressor(kern, normalize_y=True, n_restarts_optimizer=2, random_state=seed)
        gp.fit(np.array(X), np.array(y))
        ybest = min(y)
        C = sample_feasible(3000, rng)
        ei = expected_improvement(gp, C, ybest)
        starts = C[np.argsort(-ei)[:4]]
        best_u, best_ei = starts[0], ei.max()
        for x0 in starts:
            r = minimize(lambda u: -expected_improvement(gp, u[None, :], ybest)[0], x0,
                         bounds=[(0, 1)] * DIM, method='L-BFGS-B')
            if feasible_unit(r.x[None, :])[0] and -r.fun > best_ei:
                best_u, best_ei = r.x, -r.fun
        X.append(best_u)
        y.append(f_unit(best_u))
    return y


METHODS = dict(gpei=run_gpei, random=run_random, sobol=run_sobol, cma=run_cma)

if __name__ == '__main__':
    seeds = range(int(sys.argv[1]) if len(sys.argv) > 1 else 15)
    res = {m: [] for m in METHODS}
    t0 = time.time()
    for sd in seeds:
        for m, fn in METHODS.items():
            ys = fn(sd)
            res[m].append([float(v) if v is not None and not np.isnan(v) else None for v in ys])
        print('seed', sd, {m: round(min(v for v in res[m][-1] if v is not None), 4) for m in METHODS},
              '%.0fs' % (time.time() - t0), flush=True)
    json.dump(res, open('res_bo.json', 'w'))
