"""E0 verification and E1/E2 mechanism maps."""
import json, time
import numpy as np
from scipy.integrate import solve_ivp
import props as pp, mw1d

kr = mw1d.designed_material(pp.KRAFT)
eo = pp.NOMINAL['eps_ne']


def mat_tau(tau85, Ea=None):
    """Kraft-permittivity paper whose relaxation-time ratio at 85 C equals tau85 (activation Ea)."""
    T85 = 358.15
    so = float(pp.oil_conductivity(T85))
    sp85 = kr.eps * so / (eo * tau85)
    Ea = pp.NOMINAL['Ea_b'] if Ea is None else Ea
    return mw1d.Material(kr.eps, lambda T: sp85 * np.exp(-Ea / pp.KB * (1 / np.asarray(T) - 1 / T85)))


def verify():
    """Exact modal ladder versus stiff BDF integration of the same ODE (two-layer and full stack)."""
    out = {}
    for name, stack in [('two-layer', [('paper', 3.0), ('oil', 6.0)]), ('stack', mw1d.STACK)]:
        m = mat_tau(10.0)
        d, eps, sig, is_oil = mw1d.build_layers(m, T_hot=358.15, T_cold=333.15, stack=stack)
        lad = mw1d.Ladder(d, eps, sig)
        U = 100e3
        E0 = mw1d.capacitive_field(d, eps, -U)
        u0 = (E0 * d)[:-1]
        tr = 10.0
        ts = np.linspace(0, tr, 101)[1:]
        ue, Ve = lad.evolve(u0, -U, 2 * U / tr, ts)
        Ee = lad.fields(ue, Ve)
        C = eps / d; G = sig / d
        def rhs(t, E):
            # direct field form: eps dE/dt = J - sig E, J from sum d E = V
            w = d / eps
            J = ((2 * U / tr) + np.sum(d * sig * E / eps)) / np.sum(w)
            return (J - sig * E) / eps
        sol = solve_ivp(rhs, (0, tr), E0, method='BDF', t_eval=ts, rtol=1e-10, atol=1e-6)
        err = np.abs(sol.y.T - Ee).max() / np.abs(Ee).max()
        out[name] = float(err)
        print('verify', name, 'max rel err %.2e' % err)
    return out


def map_isothermal():
    taus = np.geomspace(0.1, 100, 31)
    trs = np.geomspace(1, 300, 25)
    G = np.zeros((len(taus), len(trs))); Q = np.zeros_like(G); P = np.zeros_like(G)
    for i, t in enumerate(taus):
        m = mat_tau(t)
        for j, tr in enumerate(trs):
            r = mw1d.pr_sequence(m, T_hot=358.15, T_cold=358.15, t_r=tr)
            G[i, j] = r['rev_oil'] / r['cap_oil']
            Q[i, j] = r['q_int']
            P[i, j] = r['peak_paper'] / r['cap_paper']
    return dict(taus=taus.tolist(), trs=trs.tolist(), gamma=G.tolist(), q=Q.tolist(), pap=P.tolist())


def map_gradient():
    taus = np.geomspace(0.1, 100, 31)
    dTs = np.linspace(0, 50, 26)
    out = {}
    for lab, Ea in [('Ea_kraft', None), ('Ea_oil', pp.NOMINAL['Ea_o_ne']), ('Ea_high', 1.4)]:
        F = np.zeros((len(taus), len(dTs))); Pp = np.zeros_like(F)
        for i, t in enumerate(taus):
            m = mat_tau(t, Ea)
            for j, dT in enumerate(dTs):
                r = mw1d.pr_sequence(m, T_hot=358.15 + dT / 2, T_cold=358.15 - dT / 2, t_r=10.0)
                F[i, j] = r['peak_oil'] / r['cap_oil']
                Pp[i, j] = r['peak_paper'] / r['cap_paper']
        out[lab] = dict(F=F.tolist(), P=Pp.tolist())
    out['taus'] = taus.tolist(); out['dTs'] = dTs.tolist()
    return out


if __name__ == '__main__':
    t0 = time.time()
    res = dict(verify=verify(), iso=map_isothermal(), grad=map_gradient())
    # traces for three papers in the hardest scenario (110->70 C, tr = 10 s)
    import design as D
    dz = json.load(open('res_designs.json'))
    tr = {}
    for name, v in [('kraft', None), ('strict', dz['strict_match']['v']), ('graded', dz['opt_graded']['v'])]:
        mat = kr if v is None else D.materials(v)
        r = mw1d.pr_sequence(mat, T_hot=383.15, T_cold=343.15, t_r=10.0, return_traces=True)
        d, eps, sig, is_oil = r['layers']
        T, E = [], []
        for ts, Et, tag in r['traces']:
            T.append(ts); E.append(Et)
        T = np.concatenate(T); E = np.concatenate(E) / 1e6
        io = np.where(is_oil)[0]
        ip = np.where(~is_oil)[0]
        tr[name] = dict(t=T.tolist(), oil_max=np.abs(E[:, io]).max(1).tolist(),
                        pap_max=np.abs(E[:, ip]).max(1).tolist(),
                        oil_cold=E[:, io[-1]].tolist(), oil_hot=E[:, io[0]].tolist())
    res['traces'] = tr
    json.dump(res, open('res_maps.json', 'w'))
    print('done %.0fs' % (time.time() - t0))
