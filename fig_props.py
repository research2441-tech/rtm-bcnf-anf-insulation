"""Property-model behaviour: permittivity, dissociation coupling and relaxation-time ratio over temperature."""
import json, sys
import numpy as np
import figstyle as fs
import matplotlib.pyplot as plt
import props as pp, design as D

DZ = json.load(open('res_designs.json'))
fig, axs = plt.subplots(1, 3, figsize=(fs.COL2, 2.3), gridspec_kw=dict(wspace=0.42))
ax = axs[0]
wa = np.linspace(0, 0.35, 36)
for wc, ls in [(0.05, '-'), (0.15, '--'), (0.30, ':')]:
    ax.plot(wa, [pp.permittivity(dict(w_a=a, w_c=wc, c=1.0, w_b=0.0)) for a in wa], 'k', ls=ls, label='$w_C$ = %.2f' % wc)
ax.axhline(pp.permittivity(pp.KRAFT), color='0.6', lw=0.6, ls='-.')
ax.text(0.01, pp.permittivity(pp.KRAFT) + 0.02, 'kraft', fontsize=6, color='0.35')
ax.set_xlabel('ANF fraction $w_A$'); ax.set_ylabel('$\\varepsilon_p$ in ester')
ax.legend(loc='lower left', fontsize=6); ax.set_title('(a) sheet permittivity', pad=4)

ax = axs[1]
cc = np.linspace(0, 1.7, 35)
s0 = pp.paper_conductivity(pp.KRAFT, 323.15)
Pn = dict(pp.NOMINAL); Pn['couple'] = False
for a, ls in [(0.0, '-'), (0.175, '--'), (0.35, ':')]:
    ax.semilogy(cc, [pp.paper_conductivity(dict(w_a=a, w_c=0.15, c=c, w_b=0.0), 323.15) / s0 for c in cc], 'k', ls=ls,
                label='$w_A$ = %.3g' % a)
ax.semilogy(cc, [pp.paper_conductivity(dict(w_a=0.35, w_c=0.15, c=c, w_b=0.0), 323.15, 'ne', Pn) / s0 for c in cc],
            color='0.6', ls=':', lw=1.4, label='$w_A$ = 0.35, uncoupled')
ax.set_xlabel('carboxylate content $c$ (mmol g$^{-1}$)'); ax.set_ylabel('$\\sigma_p/\\sigma_{p,\\mathrm{kraft}}$ at 50 °C')
ax.legend(loc='upper left', fontsize=5.8); ax.set_title('(b) ionic channel, $w_C$ = 0.15', pad=4)

ax = axs[2]
Tc = np.linspace(40, 120, 81)
ax.axvspan(60, 110, color='0.92', lw=0)
ax.axhline(1.0, color='0.5', lw=0.6, ls='--')
curves = [('kraft', pp.KRAFT, 'k', '-'), ('D5', D.to_x(DZ['strict_match']['v']), '0.5', '--'),
          ('D7 wrap', D.to_x(DZ['opt_graded']['v'], 0), 'k', ':'), ('D7 core side', D.to_x(DZ['opt_graded']['v'], 4), 'k', '-.')]
for lab, x, c, ls in curves:
    ax.semilogy(Tc, [pp.tau_ratio(x, t + 273.15) for t in Tc], color=c, ls=ls, lw=1.1, label=lab)
ax.set_xlabel('temperature (°C)'); ax.set_ylabel('$\\rho_\\tau=\\tau_p/\\tau_o$')
ax.text(85, 40, 'design\nwindow', ha='center', va='center', fontsize=6, color='0.35')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize=6); ax.set_title('(c) relaxation-time ratio', pad=4)
fig.savefig('fig_props.png')
print('ok')
