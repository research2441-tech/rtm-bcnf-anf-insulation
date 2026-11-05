"""Composition-to-property model for ester-impregnated cellulose/aramid-nanofibre/BNNS paper.

Every nominal constant carries a tag:
  [M]  measured value taken from the literature (reference given in the manuscript)
  [A]  modelling assumption; swept in the uncertainty and Sobol analyses
"""
import numpy as np

KB = 8.617333e-5          # Boltzmann constant, eV/K
E0 = 8.8541878128e-12     # vacuum permittivity, F/m
COUL = 1.43996            # e^2/(4*pi*eps0) in eV*nm

NOMINAL = dict(
    eps_cell=6.0,         # [A] solid cellulose relative permittivity
    eps_anf=3.6,          # [A] aramid nanofibre relative permittivity
    eps_bn=3.76,          # [M] h-BN out-of-plane static permittivity (Laturia et al.)
    eps_ne=3.2,           # [M] natural ester (Rumpelt & Jenau)
    eps_mo=2.2,           # [M] mineral oil (Rumpelt & Jenau)
    rho_cell=1.50, rho_anf=1.44, rho_bn=2.10,   # [A] g/cm3
    p0=0.40,              # [A] porosity of a kraft-type handsheet
    beta_fill=0.40,       # [A] porosity reduction per unit nanofibril mass fraction
    p_min=0.12,
    sig_b50_ne=5.45e-14,  # [M] FR3-impregnated pressboard, 50 C (Rumpelt & Jenau)
    sig_b50_mo=3.99e-13,  # [M] mineral-oil-impregnated pressboard, 50 C (Rumpelt & Jenau)
    Ea_b=1.07,            # [M] impregnated pressboard DC activation energy, eV (Kierczynski et al.)
    m_arch=1.5,           # [A] cellulose-fraction exponent of base conduction
    sig_o50_ne=1.0e-12,   # [A] natural ester conductivity at 50 C (cross-checked against series data)
    Ea_o_ne=0.60,         # [A] natural ester conductivity activation energy, eV
    sig_o50_mo=1.0e-14,   # [A] mineral oil, two decades below ester (Rumpelt & Jenau ratio)
    Ea_o_mo=0.60,         # [A]
    ion_gain=10.0,        # [A] ionic channel / base conductivity at 50 C for w_c=0.2, c=1.0, eps_m=4.7
    E_mu=0.45,            # [A] ion hopping barrier, eV
    a_pair=0.45,          # [A] carboxylate-Na+ contact distance, nm
    alpha_bn=50.0,        # [A] BNNS aspect ratio for Nielsen tortuosity
    k_paper0=0.19,        # [A] through-plane conductivity of impregnated paper, W/(m K)
    k_bn_perp=4.0,        # [A] h-BN through-plane thermal conductivity, W/(m K)
    k_oil=0.17,           # [A] ester thermal conductivity, W/(m K)
    couple=True,          # dissociation energy follows the composite permittivity (model switch)
)


def volume_fractions(x, P=NOMINAL):
    """x = dict(w_a, c, w_c, w_b) mass fractions of ANF, B-CNF, BNNS; remainder kraft cellulose."""
    w_a, w_c, w_b = x['w_a'], x['w_c'], x['w_b']
    w_k = 1.0 - w_a - w_c - w_b
    vol = np.array([(w_k + w_c) / P['rho_cell'], w_a / P['rho_anf'], w_b / P['rho_bn']])
    solid = vol / vol.sum()
    p = max(P['p_min'], P['p0'] - P['beta_fill'] * (w_c + w_a))
    return solid * (1 - p), p      # [cellulose, anf, bn] of total volume, porosity


def permittivity(x, oil='ne', P=NOMINAL):
    """Looyenga cube-root mixing of solid phases and oil-filled pores."""
    v, p = volume_fractions(x, P)
    eo = P['eps_ne'] if oil == 'ne' else P['eps_mo']
    s = v[0] * P['eps_cell'] ** (1 / 3) + v[1] * P['eps_anf'] ** (1 / 3) \
        + v[2] * P['eps_bn'] ** (1 / 3) + p * eo ** (1 / 3)
    return s ** 3


def tortuosity(x, P=NOMINAL):
    v, _ = volume_fractions(x, P)
    return 1.0 + 0.5 * P['alpha_bn'] * v[2]


def dissociation_energy(eps_m, P=NOMINAL):
    return COUL / (eps_m * P['a_pair'])        # eV


KRAFT = dict(w_a=0.0, c=0.0, w_c=0.0, w_b=0.0)


def paper_conductivity(x, T, oil='ne', P=NOMINAL):
    """DC conductivity (S/m) at temperature T (K): base cellulose channel + carboxylate ionic channel."""
    T = np.asarray(T, float)
    v, _ = volume_fractions(x, P)
    v0, _ = volume_fractions(KRAFT, P)
    s50 = P['sig_b50_ne'] if oil == 'ne' else P['sig_b50_mo']
    T50 = 323.15
    base = s50 * (v[0] / v0[0]) ** P['m_arch'] * np.exp(-P['Ea_b'] / KB * (1 / T - 1 / T50))
    ion = 0.0
    if x['c'] > 0 and x['w_c'] > 0:
        eps_m = permittivity(x, oil, P) if P.get('couple', True) else 4.7
        U = dissociation_energy(eps_m, P)
        Uref = dissociation_energy(4.7, P)
        Ea_ion = P['E_mu'] + 0.5 * U
        Ea_ref = P['E_mu'] + 0.5 * Uref
        # reference ionic conductivity at 50 C for (w_c=0.2, c=1.0, eps_m=4.7)
        ion_ref50 = P['ion_gain'] * P['sig_b50_ne']
        # scale with number of carboxylates and with the change of dissociation/activation
        ion = ion_ref50 * (x['w_c'] / 0.2) * (x['c'] / 1.0) * \
            np.exp(-(Ea_ion - Ea_ref) / (KB * T50)) * np.exp(-Ea_ion / KB * (1 / T - 1 / T50))
    return (base + ion) / tortuosity(x, P)


def oil_conductivity(T, oil='ne', P=NOMINAL):
    T = np.asarray(T, float)
    s50 = P['sig_o50_ne'] if oil == 'ne' else P['sig_o50_mo']
    Ea = P['Ea_o_ne'] if oil == 'ne' else P['Ea_o_mo']
    return s50 * np.exp(-Ea / KB * (1 / T - 1 / 323.15))


def oil_permittivity(oil='ne', P=NOMINAL):
    return P['eps_ne'] if oil == 'ne' else P['eps_mo']


def thermal_conductivity(x, P=NOMINAL):
    """Through-plane conductivity: Maxwell-Garnett with flat-lying platelets (depolarisation ~1 along normal)."""
    v, p = volume_fractions(x, P)
    km = P['k_paper0']
    vb = v[2]
    kb = P['k_bn_perp']
    L = 0.95
    return km * (1 + vb * (kb - km) / (km + L * (1 - vb) * (kb - km)))


def apparent_activation(x, oil='ne', P=NOMINAL, T1=333.15, T2=383.15):
    s1, s2 = paper_conductivity(x, T1, oil, P), paper_conductivity(x, T2, oil, P)
    return KB * np.log(s2 / s1) / (1 / T1 - 1 / T2)


def tau_ratio(x, T, oil='ne', P=NOMINAL):
    """Paper-to-oil dielectric relaxation-time ratio."""
    tp = permittivity(x, oil, P) / paper_conductivity(x, T, oil, P)
    to = oil_permittivity(oil, P) / oil_conductivity(T, oil, P)
    return tp / to


if __name__ == '__main__':
    for name, x, oil in [('kraft/MO', KRAFT, 'mo'), ('kraft/NE', KRAFT, 'ne'),
                         ('A20 C20 c1.2 B3', dict(w_a=0.2, c=1.2, w_c=0.2, w_b=0.03), 'ne')]:
        print(name, 'eps=%.2f' % permittivity(x, oil), 'sig50=%.2e' % paper_conductivity(x, 323.15, oil),
              'Ea=%.2f' % apparent_activation(x, oil), 'tau_r(60,85,110)=',
              [round(float(tau_ratio(x, T, oil)), 2) for T in (333.15, 358.15, 383.15)],
              'k=%.3f' % thermal_conductivity(x))
