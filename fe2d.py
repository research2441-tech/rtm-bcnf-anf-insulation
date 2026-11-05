"""Axisymmetric (r, z) finite-volume solver for the transient electro-quasistatic problem
    div(sigma grad phi) + d/dt div(eps grad phi) = 0
on a representative valve-side winding/barrier geometry with a steady temperature field.
Backward-Euler time stepping; one sparse LU factorisation per distinct time step.
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import props as pp
import mw1d

MM = 1e-3


class Geometry:
    """Material map on a uniform grid (cell size h mm). Codes: 0 oil, 1..5 solid layers (1 = wrap), -1 electrode."""

    def __init__(self, h=1.0, planar=False, r_shift=0.0):
        self.h = h
        self.r0, self.r1 = 306.0 + r_shift, 480.0 + r_shift
        self.z0, self.z1 = 0.0, 380.0
        nr = int(round((self.r1 - self.r0) / h))
        nz = int(round((self.z1 - self.z0) / h))
        self.nr, self.nz = nr, nz
        rc = self.r0 + (np.arange(nr) + 0.5) * h
        zc = self.z0 + (np.arange(nz) + 0.5) * h
        self.rc, self.zc = rc, zc
        R, Z = np.meshgrid(rc - r_shift, zc, indexing='ij')
        mat = np.zeros((nr, nz), int)
        # barrier cylinders (layers 2..5, winding side first)
        cyl = [(345, 348), (334, 337), (323, 326), (312, 315)]
        if planar:
            for k, (a, b) in enumerate(cyl):
                mat[(R > a) & (R < b)] = k + 2
            mat[(R > 354) & (R < 357)] = 1
            mat[R > 357] = -1
            self.mat = mat
            self.top_ground = False
            return
        zt = 250.0                                  # winding top
        rad = 5.0                                   # corner radius of winding copper
        for k, (a, b) in enumerate(cyl):
            mat[(R > a) & (R < b) & (Z < 330)] = k + 2
        # end washer (layer 3 material) above the winding
        mat[(Z > 275) & (Z < 278) & (R > 330) & (R < 450)] = 3
        # winding copper: r in [357, 420], z < zt, rounded outer corners
        cu = (R > 357) & (R < 420) & (Z < zt)
        for (rcn, sgn) in [(357 + rad, -1), (420 - rad, 1)]:
            corner = (Z > zt - rad) & ((R - rcn) * sgn > 0)
            cu &= ~(corner & ((R - rcn) ** 2 + (Z - (zt - rad)) ** 2 > rad ** 2))
        # paper wrap 3 mm around copper (inner face, top face, outer face)
        wrap = np.zeros_like(cu)
        dist = np.full(cu.shape, np.inf)
        idx = np.argwhere(cu)
        # distance transform (cheap: only near boundary)
        from scipy.ndimage import distance_transform_edt
        dist = distance_transform_edt(~cu) * h
        wrap = (~cu) & (dist <= 3.0) & (R > 350) & (R < 430) & (Z < zt + 4)
        mat[wrap] = 1
        mat[cu] = -1
        self.mat = mat
        self.top_ground = True


def temperature_field(g, T_hot, T_cold, P=pp.NOMINAL):
    """Steady conduction with winding at T_hot and core/yoke at T_cold."""
    k = np.where(g.mat == 0, P['k_oil'], P['k_paper0'])
    k = np.where(g.mat == -1, 400.0, k)
    T = _laplace(g, k, fixed_mask=_electrode_mask(g), fixed_val=T_hot, ground_val=T_cold)
    return T


def _electrode_mask(g):
    return g.mat == -1


def _assemble(g, coef):
    """FV stiffness for div(coef grad .) in axisymmetric coordinates (unit radian)."""
    nr, nz, h = g.nr, g.nz, g.h * MM
    rc = g.rc * MM
    N = nr * nz
    idx = np.arange(N).reshape(nr, nz)
    rows, cols, vals = [], [], []
    diag = np.zeros(N)
    bnd_ground = np.zeros(N)          # conductance to grounded boundary (left r0, top z1)
    # radial faces
    cf = 2 * coef[:-1, :] * coef[1:, :] / (coef[:-1, :] + coef[1:, :] + 1e-300)
    rf = (g.r0 + (np.arange(1, nr)) * g.h) * MM
    G = cf * (rf[:, None] * h) / h
    a, b = idx[:-1, :].ravel(), idx[1:, :].ravel()
    Gv = G.ravel()
    rows += [a, b]; cols += [b, a]; vals += [-Gv, -Gv]
    np.add.at(diag, a, Gv); np.add.at(diag, b, Gv)
    # axial faces
    cf = 2 * coef[:, :-1] * coef[:, 1:] / (coef[:, :-1] + coef[:, 1:] + 1e-300)
    G = cf * (rc[:, None] * h) / h
    a, b = idx[:, :-1].ravel(), idx[:, 1:].ravel()
    Gv = G.ravel()
    rows += [a, b]; cols += [b, a]; vals += [-Gv, -Gv]
    np.add.at(diag, a, Gv); np.add.at(diag, b, Gv)
    # grounded boundaries: core surface r = r0 (half cell) and yoke z = z1
    Gl = coef[0, :] * (g.r0 * MM * h) / (h / 2)
    diag[idx[0, :]] += Gl; bnd_ground[idx[0, :]] += Gl
    if g.top_ground:
        Gt = coef[:, -1] * (rc * h) / (h / 2)
        diag[idx[:, -1]] += Gt; bnd_ground[idx[:, -1]] += Gt
    A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N))
    A = A + sp.diags(diag)
    return A.tocsr(), bnd_ground


def _laplace(g, k, fixed_mask, fixed_val, ground_val):
    A, bg = _assemble(g, k)
    f = fixed_mask.ravel()
    free = ~f
    rhs = -A[free][:, f] @ np.full(f.sum(), fixed_val) + bg[free] * ground_val
    x = np.full(g.nr * g.nz, fixed_val, float)
    x[free] = spla.spsolve(A[free][:, free].tocsc(), rhs)
    return x.reshape(g.nr, g.nz)


class EQS:
    def __init__(self, g, mats, T, P=pp.NOMINAL, D_o=1.0, D_p=1.0):
        self.g = g
        eps = np.full(g.mat.shape, pp.oil_permittivity('ne', P))
        sig = D_o * pp.oil_conductivity(T, 'ne', P)
        for code in range(1, 6):
            m = mats[code - 1] if isinstance(mats, (list, tuple)) else mats
            sel = g.mat == code
            eps[sel] = m.eps
            sig[sel] = D_p * m.sig(T[sel])
        eps[g.mat == -1] = 1.0
        sig[g.mat == -1] = 1.0
        self.eps, self.sig = eps * pp.E0, sig
        self.Ke, _ = _assemble(g, self.eps)
        self.Ks, _ = _assemble(g, self.sig)
        f = (g.mat == -1).ravel()
        self.f, self.free = f, ~f
        self.Kef = self.Ke[self.free][:, self.free].tocsc()
        self.Ksf = self.Ks[self.free][:, self.free].tocsc()
        self.Kec = self.Ke[self.free][:, f]
        self.Ksc = self.Ks[self.free][:, f]
        self._lu = {}

    def lu(self, dt):
        key = round(dt, 6)
        if key not in self._lu:
            if len(self._lu) >= 3:
                self._lu.pop(next(iter(self._lu)))
            self._lu[key] = spla.splu((self.Kef + dt * self.Ksf).tocsc())
        return self._lu[key]

    def capacitive(self, V):
        nf = self.f.sum()
        rhs = -self.Kec @ np.full(nf, V)
        x = spla.spsolve(self.Kef, rhs)
        return x

    def step(self, x, V_new, V_old, dt):
        nf = self.f.sum()
        # (Ke + dt Ks) x1 = Ke x0 - Kec (V1 - V0) - dt Ksc V1
        rhs = self.Kef @ x - self.Kec @ np.full(nf, V_new - V_old) - dt * (self.Ksc @ np.full(nf, V_new))
        return self.lu(dt).solve(rhs)

    def full(self, x, V):
        phi = np.full(self.g.nr * self.g.nz, V, float)
        phi[self.free] = x
        return phi.reshape(self.g.nr, self.g.nz)

    def face_peaks(self, phi):
        """Max |E| on faces whose two cells share the same material class (oil / solid), MV/m."""
        h = self.g.h * MM
        m = self.g.mat
        Er = np.abs(phi[1:] - phi[:-1]) / h
        Ez = np.abs(phi[:, 1:] - phi[:, :-1]) / h
        oil_r = (m[1:] == 0) & (m[:-1] == 0); oil_z = (m[:, 1:] == 0) & (m[:, :-1] == 0)
        sol_r = (m[1:] > 0) & (m[:-1] > 0); sol_z = (m[:, 1:] > 0) & (m[:, :-1] > 0)
        # oil faces: combine with the transverse component averaged to the face
        om = max(Er[oil_r].max(initial=0), Ez[oil_z].max(initial=0)) / 1e6
        pm = max(Er[sol_r].max(initial=0), Ez[sol_z].max(initial=0)) / 1e6
        return om, pm

    def efield(self, phi):
        h = self.g.h * MM
        Er = np.zeros_like(phi); Ez = np.zeros_like(phi)
        Er[1:-1] = -(phi[2:] - phi[:-2]) / (2 * h)
        Er[0] = -(phi[0] - 0.0) / (0.5 * h)          # ground at r0 face (half cell)
        Er[-1] = -(phi[-1] - phi[-2]) / h
        Ez[:, 1:-1] = -(phi[:, 2:] - phi[:, :-2]) / (2 * h)
        Ez[:, 0] = 0.0
        Ez[:, -1] = -(0.0 - phi[:, -1]) / (0.5 * h) if self.g.top_ground else 0.0
        return Er, Ez


def time_grid(T, dt0=0.05, per_level=6, dtmax=102.4):
    """Geometric ladder of time steps (dt0 * 2^k, `per_level` steps each) so that few LU factors are needed."""
    ts, t, dt, n = [], 0.0, dt0, 0
    while t < T - 1e-9:
        step = min(dt, T - t)
        ts.append(step)
        t += step
        n += 1
        if n % per_level == 0 and dt < dtmax:
            dt *= 2
    return ts


def run_pr(g, mats, T_hot, T_cold, t_r=10.0, U=mw1d.U_PR, P=pp.NOMINAL, D_o=1.0, D_p=1.0,
           snapshots=(), monitor=None):
    T = temperature_field(g, T_hot + 273.15, T_cold + 273.15, P)
    s = EQS(g, mats, T, P, D_o, D_p)
    oil = (g.mat == 0)
    solid = (g.mat > 0)
    # exclude the first oil cell next to the copper corner region from the peak (staircase singularity)
    from scipy.ndimage import binary_dilation
    near_cu = binary_dilation(g.mat == -1, iterations=1)
    oil_eval = oil & ~near_cu
    x = s.capacitive(-U)
    V = -U
    tnow = 0.0
    out = dict(t=[], oil_max=[], pap_max=[], V=[])
    snaps = {}
    peak = dict(oil=0.0, pap=0.0)

    def record(x, V):
        phi = s.full(x, V)
        Er, Ez = s.efield(phi)
        E = np.hypot(Er, Ez) / 1e6
        om, pm = s.face_peaks(phi)
        out['t'].append(tnow); out['oil_max'].append(om); out['pap_max'].append(pm); out['V'].append(V)
        peak['oil'] = max(peak['oil'], om); peak['pap'] = max(peak['pap'], pm)
        if monitor is not None:
            monitor(tnow, phi, E)
        return E

    record(x, V)
    segments = [(mw1d.T_STEP['pre'], 0.0), (t_r, 2 * U / t_r), (mw1d.T_STEP['mid'], 0.0),
                (t_r, -2 * U / t_r), (mw1d.T_STEP['post'], 0.0)]
    for si, (Tseg, slope) in enumerate(segments):
        if slope != 0.0:
            dts = [t_r / 80] * 80
        else:
            dts = time_grid(Tseg)
        for dt in dts:
            Vn = V + slope * dt
            x = s.step(x, Vn, V, dt)
            V = Vn
            tnow += dt
            E = record(x, V)
            for (name, tsnap) in snapshots:
                if name not in snaps and tnow >= tsnap:
                    snaps[name] = (tnow, E.copy(), s.full(x, V))
    out = {k: np.array(v) for k, v in out.items()}
    out['peak_oil'], out['peak_paper'] = peak['oil'], peak['pap']
    out['snaps'] = snaps
    out['T'] = T
    return out
