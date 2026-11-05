"""Design-space figure: stress trade-off of uniform compositions and the carboxylate response."""
import json
import numpy as np
import figstyle as fs
import matplotlib.pyplot as plt

S = np.array(json.load(open('res_space.json')))
T = json.load(open('res_designs.json'))['table']
fig, axs = plt.subplots(1, 2, figsize=(fs.COL2, 2.45), gridspec_kw=dict(wspace=0.3))
ax = axs[0]
sc = ax.scatter(S[:, 6], S[:, 5], c=S[:, 4], cmap='Greys_r', s=7, lw=0, vmin=S[:, 4].min(), vmax=8.4)
cb = fig.colorbar(sc, ax=ax, pad=0.02, fraction=0.05); cb.set_label('$J$ (kV mm$^{-1}$)', fontsize=7)
cb.ax.tick_params(labelsize=6)
marks = [('D0 Kraft/NE', 'D0', 'o', 'white'), ('D5 Exact window matching', 'D5', '^', 'white'),
         ('D6 Robust uniform (proposed)', 'D6', 's', 'white'), ('D7 Robust graded (proposed)', 'D7', 's', 'k')]
offs = {'D0': (6, 4), 'D5': (6, -10), 'D6': (-16, 7), 'D7': (8, -9)}
for key, lab, mk, fc in marks:
    t = T[key]
    ax.plot(t['peak_paper_mean'], t['peak_oil_mean'], marker=mk, ms=6, mfc=fc, mec='k', mew=0.9, ls='none')
    ax.annotate(lab, (t['peak_paper_mean'], t['peak_oil_mean']), textcoords='offset points', xytext=offs[lab],
                fontsize=6.5)
ax.set_xlabel('scenario-mean $E_p^{\\max}$ (kV mm$^{-1}$)'); ax.set_ylabel('scenario-mean $E_o^{\\max}$ (kV mm$^{-1}$)')
ax.set_title('(a) %d uniform compositions' % len(S), pad=4)
ax = axs[1]
wcs = np.unique(S[:, 1]); was = np.unique(S[:, 0])
wc = wcs[np.argmin(np.abs(wcs - 0.15))]
sty = ['-', '--', '-.', ':']
sel_wa = [was[0], was[2], was[4], was[-1]]
for k, wa in enumerate(sel_wa):
    m = (np.isclose(S[:, 0], wa)) & (np.isclose(S[:, 1], wc)) & (np.isclose(S[:, 3], 0.10))
    if m.sum() < 2:
        continue
    o = np.argsort(S[m, 2])
    ax.plot(S[m, 2][o], S[m, 4][o], color='k', ls=sty[k], lw=1.0, label='$w_A$ = %.2f' % wa)
ax.axhline(T['D0 Kraft/NE']['util_mean'], color='0.6', lw=0.6, ls=':')
ax.text(0.05, T['D0 Kraft/NE']['util_mean'] + 0.04, 'kraft', fontsize=6, color='0.35')
ax.set_xlabel('carboxylate content $c$ (mmol g$^{-1}$)'); ax.set_ylabel('$J$ (kV mm$^{-1}$)')
ax.set_title('(b) $w_C$ = %.2f, $w_B$ = 0.10' % wc, pad=4)
ax.legend(loc='upper left', fontsize=6)
fig.savefig('fig_space.png')
print('ok', len(S), wc)
