"""Robust design objective over temperature, reversal-time and ageing scenarios."""
import numpy as np
import props as pp
import mw1d

C2K = 273.15
T_SCEN = [(60, 60), (85, 85), (110, 110), (85, 60), (110, 70)]       # (winding side, core side) degC
TR_SCEN = [10.0, 120.0]                                               # reversal time, s
AGE_SCEN = [(1.0, 1.0), (4.0, 1.0), (1.0, 4.0), (4.0, 4.0)]           # (oil, paper) conductivity factors
KAPPA = 3.0                                                           # paper-to-oil design-stress ratio [A]

BOUNDS = np.array([[0.0, 0.35],    # w_a  ANF mass fraction
                   [0.05, 0.30],   # w_c  B-CNF mass fraction
                   [0.0, 1.70],    # c_w  carboxylate content of the winding-side layer, mmol/g
                   [0.0, 1.70],    # c_k  carboxylate content of the core-side layer, mmol/g
                   [0.0, 0.10]])   # w_b  BNNS mass fraction
NAMES = ['w_a', 'w_c', 'c_w', 'c_k', 'w_b']
N_SOLID = sum(1 for k, _ in mw1d.STACK if k != 'oil')


def to_x(v, layer=None):
    """Composition of solid layer `layer` (0 = winding side); c varies linearly between c_w and c_k."""
    v = np.asarray(v, float)
    if len(v) == 4:                       # uniform design (w_a, w_c, c, w_b)
        v = np.array([v[0], v[1], v[2], v[2], v[3]])
    f = 0.0 if layer is None else layer / (N_SOLID - 1)
    c = (1 - f) * v[2] + f * v[3] if layer is not None else 0.5 * (v[2] + v[3])
    return dict(w_a=float(v[0]), w_c=float(v[1]), c=float(c), w_b=float(v[4]))


def materials(v, P=pp.NOMINAL):
    v = np.asarray(v, float)
    if len(v) == 4 or np.isclose(v[2], v[3]):
        return mw1d.designed_material(to_x(v), P)
    return [mw1d.designed_material(to_x(v, k), P) for k in range(N_SOLID)]


def feasible(v):
    v = np.asarray(v, float)
    wb = v[-1]
    return (v[0] + v[1] + wb) <= 0.60


def scenario_metrics(mat, P=pp.NOMINAL, t_scen=T_SCEN, tr_scen=TR_SCEN, age_scen=AGE_SCEN, kappa=KAPPA):
    rows = []
    for (th, tc) in t_scen:
        for tr in tr_scen:
            for (do, dp) in age_scen:
                r = mw1d.pr_sequence(mat, P, th + C2K, tc + C2K, do, dp, tr)
                r['util'] = max(r['peak_oil'], r['peak_paper'] / kappa)
                r['scen'] = (th, tc, tr, do, dp)
                rows.append(r)
    return rows


def summarise(rows):
    keys = ['util', 'peak_oil', 'peak_paper', 'rev_oil', 'dc_oil', 'dc_paper', 'rho_max', 'q_int', 'q_bulk', 'leak', 'gamma']
    out = {k + '_mean': float(np.mean([r[k] for r in rows])) for k in keys}
    out.update({k + '_max': float(np.max([r[k] for r in rows])) for k in keys})
    return out


def objective(v, P=pp.NOMINAL, kappa=KAPPA, **kw):
    if not feasible(v):
        return 1e3
    rows = scenario_metrics(materials(v, P), P, kappa=kappa, **kw)
    return float(np.mean([r['util'] for r in rows]))


def evaluate(v_or_mat, P=pp.NOMINAL, kappa=KAPPA, **kw):
    if isinstance(v_or_mat, (mw1d.Material, list)):
        mat = v_or_mat
    else:
        mat = materials(v_or_mat, P)
    rows = scenario_metrics(mat, P, kappa=kappa, **kw)
    s = summarise(rows)
    m0 = mat[len(mat) // 2] if isinstance(mat, list) else mat
    s['eps'] = float(m0.eps)
    s['sig60'] = float(m0.sig(333.15))
    s['sig110'] = float(m0.sig(383.15))
    return s, rows
