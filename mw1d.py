"""One-dimensional transient Maxwell-Wagner model of a multilayer oil/paper barrier stack.

Each sub-layer is a parallel RC element (per unit area); the series ladder is driven by V(t).
Reducing to n-1 layer voltages gives a symmetric-definite pencil whose modal solution is exact for
piecewise-linear V(t), so the polarity-reversal (PR) sequence is resolved without time-step error.
"""
import numpy as np
import props as pp

# representative valve-side main gap (winding side first), thickness in mm
STACK = [('paper', 3.0), ('oil', 6.0), ('paper', 3.0), ('oil', 8.0), ('paper', 3.0), ('oil', 8.0),
         ('paper', 3.0), ('oil', 8.0), ('paper', 3.0), ('oil', 6.0)]
U_PR = 250e3        # polarity-reversal test level used throughout (V)
T_STEP = dict(pre=90 * 60.0, mid=90 * 60.0, post=45 * 60.0)   # IEC 60076-57-129 sequence


class Material:
    """Holds eps and sigma(T) for the solid layer; oil properties come from props."""

    def __init__(self, eps, sig_fun):
        self.eps = eps
        self.sig = sig_fun


def designed_material(x, P=pp.NOMINAL):
    return Material(pp.permittivity(x, 'ne', P), lambda T: pp.paper_conductivity(x, T, 'ne', P))


def build_layers(mat, P=pp.NOMINAL, T_hot=358.15, T_cold=333.15, D_o=1.0, D_p=1.0,
                 stack=STACK, nsub_oil=4, nsub_paper=2):
    d, eps, sig, is_oil = [], [], [], []
    total = sum(t for _, t in stack)
    z = 0.0
    eo = pp.oil_permittivity('ne', P)
    k_solid = 0
    for kind, t in stack:
        n = nsub_oil if kind == 'oil' else nsub_paper
        for k in range(n):
            zc = z + (k + 0.5) * t / n
            T = T_hot + (T_cold - T_hot) * zc / total
            d.append(t / n * 1e-3)
            if kind == 'oil':
                eps.append(eo)
                sig.append(D_o * float(pp.oil_conductivity(T, 'ne', P)))
                is_oil.append(True)
            else:
                m = mat[k_solid] if isinstance(mat, (list, tuple)) else mat
                eps.append(m.eps)
                sig.append(D_p * float(m.sig(T)))
                is_oil.append(False)
        if kind != 'oil':
            k_solid += 1
        z += t
    return (np.array(d), np.array(eps) * pp.E0, np.array(sig), np.array(is_oil))


def capacitive_field(d, eps, V):
    return V / eps / np.sum(d / eps)


class Ladder:
    """Series RC ladder (per unit area): C_i du_i/dt + G_i u_i = J, sum u_i = V(t).
    Reduced to n-1 layer voltages, giving a symmetric-definite pencil (K, M) solved by eigh."""

    def __init__(self, d, eps, sig):
        from scipy.linalg import eigh
        self.d = d
        C = eps / d
        G = sig / d
        n = len(d)
        one = np.ones(n - 1)
        M = np.diag(C[:-1]) + C[-1] * np.outer(one, one)
        K = np.diag(G[:-1]) + G[-1] * np.outer(one, one)
        lam, Phi = eigh(K, M)              # Phi^T M Phi = I
        self.lam, self.Phi = lam, Phi
        self.Cn, self.Gn = C[-1], G[-1]
        self.PhiT1 = Phi.T @ one
        self.Minv_proj = Phi.T @ M         # q = Phi^T M u

    def fields(self, u, V):
        un = V - u.sum(axis=-1)
        U = np.concatenate([u, un[..., None]], axis=-1)
        return U / self.d

    def evolve(self, u0, V0, slope, t):
        """Layer voltages for times t (array) with V(t)=V0+slope*t."""
        t = np.atleast_1d(t)[:, None]
        lam = self.lam[None, :]
        q0 = self.Minv_proj @ u0
        g0 = (self.Cn * slope + self.Gn * V0) * self.PhiT1
        g1 = (self.Gn * slope) * self.PhiT1
        e = np.exp(-lam * t)
        q = e * q0 + g0 / lam * (1 - e) + g1 * (t / lam - (1 - e) / lam ** 2)
        u = q @ self.Phi.T
        V = V0 + slope * t[:, 0]
        return u, V


def pr_sequence(mat, P=pp.NOMINAL, T_hot=358.15, T_cold=333.15, D_o=1.0, D_p=1.0,
                t_r=120.0, U=U_PR, stack=STACK, n_samp=140, return_traces=False):
    d, eps, sig, is_oil = build_layers(mat, P, T_hot, T_cold, D_o, D_p, stack)
    lad = Ladder(d, eps, sig)
    E = capacitive_field(d, eps, -U)                 # instantaneous step to -U
    u = (E * d)[:-1]
    V = -U
    Ec_oil = np.abs(E[is_oil]).max()
    Ec_pap = np.abs(E[~is_oil]).max()
    traces = []
    state = dict(t=0.0, po=Ec_oil, pp=Ec_pap)

    def run(u, V, T, slope, tag):
        ts = np.unique(np.concatenate([np.geomspace(1e-2, T, n_samp), [T]]))
        ut, Vt = lad.evolve(u, V, slope, ts)
        Et = lad.fields(ut, Vt)
        po = np.abs(Et[:, is_oil]).max()
        pa = np.abs(Et[:, ~is_oil]).max()
        state['po'] = max(state['po'], po)
        state['pp'] = max(state['pp'], pa)
        if return_traces:
            traces.append((state['t'] + ts, Et, tag))
        state['t'] += T
        return ut[-1], Vt[-1], po, Et[-1]

    u, V, _, E_dc = run(u, V, T_STEP['pre'], 0.0, 'dc-')
    u, V, p1, _ = run(u, V, t_r, 2 * U / t_r, 'rev1')
    u, V, p2, _ = run(u, V, T_STEP['mid'], 0.0, 'dc+')
    u, V, p3, _ = run(u, V, t_r, -2 * U / t_r, 'rev2')
    u, V, p4, _ = run(u, V, T_STEP['post'], 0.0, 'dc-2')
    rho = interface_charge(d, eps, E_dc)
    iface = is_oil[1:] != is_oil[:-1]
    out = dict(peak_oil=state['po'] / 1e6, peak_paper=state['pp'] / 1e6, cap_oil=Ec_oil / 1e6,
               cap_paper=Ec_pap / 1e6,
               dc_oil=np.abs(E_dc[is_oil]).max() / 1e6, dc_paper=np.abs(E_dc[~is_oil]).max() / 1e6,
               rev_oil=max(p1, p3) / 1e6, gamma=max(p1, p2, p3, p4) / Ec_oil,
               rho_max=np.abs(rho[iface]).max() * 1e6,                       # uC/m2
               q_int=float(np.abs(rho[iface]).sum() * 1e6),
               q_bulk=float(np.abs(rho[~iface]).sum() * 1e6),
               leak=float(np.max(sig * E_dc ** 2)))
    if return_traces:
        out['traces'] = traces
        out['layers'] = (d, eps, sig, is_oil)
    return out


def interface_charge(d, eps, E):
    """Free charge density (C/m2) on each sub-layer boundary: eps_{i+1}E_{i+1} - eps_i E_i."""
    D = eps * E
    return np.diff(D)


if __name__ == '__main__':
    import time
    for name, x in [('kraft', pp.KRAFT), ('mix', dict(w_a=0.3, c=1.2, w_c=0.2, w_b=0.03)),
                    ('hi', dict(w_a=0.1, c=1.7, w_c=0.3, w_b=0.0))]:
        t0 = time.time()
        r = pr_sequence(designed_material(x))
        print(name, {k: round(v, 3) if isinstance(v, float) else v for k, v in r.items()},
              '%.1f ms' % ((time.time() - t0) * 1e3))
