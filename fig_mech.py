"""Fig. 3 (mechanism maps) and Fig. 4 (PR traces, hardest thermal scenario)."""
import json
import numpy as np
import figstyle as fs
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

R = json.load(open('res_maps.json'))

# ---------------- Fig. 3 ----------------
fig, axs = plt.subplots(1, 3, figsize=(fs.COL2, 2.25), gridspec_kw=dict(wspace=0.75))
iso = R['iso']
taus, trs = np.array(iso['taus']), np.array(iso['trs'])
G = np.array(iso['gamma'])
ax = axs[0]
cs = ax.contourf(trs, taus, G, levels=np.linspace(0.6, 2.0, 15), cmap='Greys')
cl = ax.contour(trs, taus, G, levels=[1.0, 1.2, 1.4, 1.6, 1.8], colors='k', linewidths=0.5)
ax.clabel(cl, fmt='%.1f', fontsize=5.5, inline_spacing=2)
ax.axhline(1.0, color='w', lw=1.0, ls='--')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('reversal time $t_r$ (s)'); ax.set_ylabel(r'relaxation-time ratio $\rho_\tau$ at 85 °C')
ax.set_title('(a) isothermal oil overshoot $\\Gamma_o$', pad=4)
cb = fig.colorbar(cs, ax=ax, fraction=0.05, pad=0.03); cb.ax.tick_params(labelsize=6)

ax = axs[1]
Q = np.array(iso['q']); P = np.array(iso['pap'])
j = int(np.argmin(np.abs(trs - 10)))
ax.loglog(taus, np.maximum(Q[:, j], 1.0), 'k-', label='interface charge $Q_i$')
ax.set_ylim(0.7, 2e4)
ax.set_xlabel(r'$\rho_\tau$ at 85 °C'); ax.set_ylabel(r'$Q_i$ ($\mu$C m$^{-2}$)')
ax2 = ax.twinx()
ax2.semilogx(taus, P[:, j], 'k--', label='paper peak / capacitive')
ax2.set_ylabel('$E_p^{\\max}/E_p^{C}$')
ax.axvline(1.0, color='0.5', lw=0.6, ls=':')
ax.set_title('(b) isothermal, $t_r$ = 10 s', pad=4)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, ['$Q_i$ (left)', '$E_p^{\\max}/E_p^C$ (right)'], loc='center left', bbox_to_anchor=(0.02, 0.42), fontsize=6)

ax = axs[2]
gr = R['grad']
dTs = np.array(gr['dTs']); taus_g = np.array(gr['taus'])
F = np.array(gr['Ea_kraft']['F'])
cs = ax.contourf(dTs, taus_g, F, levels=np.linspace(1.0, 3.0, 11), cmap='Greys', extend='max')
cl = ax.contour(dTs, taus_g, F, levels=[1.2, 1.5, 2.0, 2.5], colors='k', linewidths=0.5)
ax.clabel(cl, fmt='%.1f', fontsize=5.5)
ax.axhline(1.0, color='w', lw=1.0, ls='--')
ax.set_yscale('log')
ax.set_xlabel(r'radial temperature drop $\Delta T$ (K)'); ax.set_ylabel(r'$\rho_\tau$ (85 °C)', labelpad=1)
ax.set_title('(c) oil peak / capacitive, $t_r$ = 10 s', pad=4)
cb = fig.colorbar(cs, ax=ax, fraction=0.05, pad=0.03); cb.ax.tick_params(labelsize=6)
fig.savefig('fig3_mechanism.png')

# ---------------- Fig. 4 ----------------
tr = R['traces']
lab = {'kraft': 'D0 kraft/NE', 'strict': 'D5 exact window matching', 'graded': 'D7 robust graded'}
sty = {'kraft': ('k', '-', 1.0), 'strict': ('0.5', '--', 1.0), 'graded': ('k', ':', 1.4)}
fig, axs = plt.subplots(1, 2, figsize=(fs.COL2, 2.2), gridspec_kw=dict(wspace=0.32))
t_rev = 5400.0
for k in ['kraft', 'strict', 'graded']:
    t = np.array(tr[k]['t'])
    sel = (t > t_rev + 0.3) & (t < 2 * t_rev + 10.0)
    pre = np.argmin(np.abs(t - (t_rev - 1)))
    c, ls, lw = sty[k]
    for ax, key in zip(axs, ['oil_max', 'pap_max']):
        y = np.array(tr[k][key])
        ax.plot(t[sel] - t_rev, y[sel], color=c, ls=ls, lw=lw, label=lab[k])
        ax.plot([0.3], [y[pre]], marker='o', ms=3, mfc='white', mec=c, ls='none')
for ax, yl, ttl in zip(axs, ['max oil-gap field (kV mm$^{-1}$)', 'max paper/barrier field (kV mm$^{-1}$)'],
                       ['(a) oil gaps', '(b) solid layers']):
    ax.set_xscale('log'); ax.set_xlim(0.25, 5600)
    ax.axvline(10.0, color='0.6', lw=0.5, ls=':')
    yl0, yl1 = ax.get_ylim(); ax.text(11.5, yl0 + 0.03 * (yl1 - yl0), 'end of ramp', fontsize=6, va='bottom', color='0.3')
    ax.set_xlabel('time after start of first reversal (s)'); ax.set_ylabel(yl); ax.set_title(ttl, pad=4)
axs[0].legend(loc='upper center', bbox_to_anchor=(1.12, -0.24), ncol=3)
fig.savefig('fig4_traces.png')
print('ok')
