"""Figs. 5-8: design comparison, BO convergence, ablation + Sobol, Monte-Carlo robustness."""
import json
import numpy as np
import figstyle as fs
import matplotlib.pyplot as plt

DZ = json.load(open('res_designs.json'))
T = DZ['table']
names = list(T.keys())
short = ['D0 kraft/NE', 'D1 aramid-pulp proxy', 'D2 NFC presspaper', 'D3 BNNS/CNF paper', 'D4 $\\varepsilon$-minimised',
         'D5 exact matching', 'D6 robust uniform', 'D7 robust graded', 'D8 low-$\\varepsilon$ + D7 (hyp.)']

# ---------------- Fig. 5 ----------------
metrics = [('util_mean', 'mean utilisation $J$ (kV mm$^{-1}$)'), ('peak_oil_mean', 'mean $E_o^{\\max}$ (kV mm$^{-1}$)'),
           ('peak_paper_mean', 'mean $E_p^{\\max}$ (kV mm$^{-1}$)'), ('q_int_mean', 'mean $Q_i$ ($\\mu$C m$^{-2}$)')]
fig, axs = plt.subplots(1, 4, figsize=(fs.COL2, 2.6), sharey=True, gridspec_kw=dict(wspace=0.12))
y = np.arange(len(names))[::-1]
for ax, (k, lab) in zip(axs, metrics):
    v = np.array([T[n][k] for n in names])
    ref = v[0]
    ax.axvline(ref, color='0.6', lw=0.6, ls='--')
    for yi, vi, n in zip(y, v, names):
        mk = 's' if n.startswith('D7') or n.startswith('D6') else ('D' if n.startswith('D8') else 'o')
        fc = 'k' if n.startswith('D7') else ('white' if n.startswith('D8') else '0.55')
        ax.plot([ref, vi], [yi, yi], color='0.75', lw=0.8)
        ax.plot(vi, yi, marker=mk, ms=4.2, mfc=fc, mec='k', mew=0.6, ls='none')
    ax.set_xlabel(lab)
    ax.grid(axis='x', color='0.9', lw=0.4)
    lo, hi = v.min(), v.max(); pad = 0.12 * (hi - lo)
    ax.set_xlim(lo - pad, hi + pad)
axs[0].set_yticks(y); axs[0].set_yticklabels(short)
fig.savefig('fig5_designs.png')

# ---------------- Fig. 6 ----------------
BO = json.load(open('res_bo.json'))
Jstar = min(DZ['opt_graded']['J'], min(min(v for v in run if v is not None) for m in BO.values() for run in m))
lab = dict(gpei='GP-EI (proposed loop)', cma='CMA-ES', random='random search', sobol='scrambled Sobol')
sty = dict(gpei=('k', '-', 1.4), cma=('0.35', '--', 1.0), random=('0.55', '-.', 1.0), sobol=('0.7', ':', 1.2))
fig, ax = plt.subplots(figsize=(fs.COL1, 2.35))
for m in ['random', 'sobol', 'cma', 'gpei']:
    R = []
    for run in BO[m]:
        a = np.array([np.inf if v is None else v for v in run], float)
        R.append(np.minimum.accumulate(a) - Jstar)
    R = np.maximum(np.array(R), 1e-4)
    med = np.median(R, 0); q1, q3 = np.percentile(R, 25, 0), np.percentile(R, 75, 0)
    n = np.arange(1, R.shape[1] + 1)
    c, ls, lw = sty[m]
    ax.fill_between(n, q1, q3, color=c, alpha=0.15, lw=0)
    ax.plot(n, med, color=c, ls=ls, lw=lw, label=lab[m])
ax.axvline(10.5, color='0.6', lw=0.5, ls=':')
ax.text(11.5, 1.3, 'initial design', fontsize=6, color='0.3', va='top')
ax.set_yscale('log'); ax.set_xlim(1, 80)
ax.set_xlabel('objective evaluations (handsheet trials)'); ax.set_ylabel('simple regret $J_{\\mathrm{best}}-J^{\\star}$')
ax.legend(loc='upper right', fontsize=6)
fig.savefig('fig6_bo.png')

# ---------------- Fig. 7 ----------------
AB = json.load(open('res_ablation.json'))
SB = json.load(open('res_sobol.json'))
fig, axs = plt.subplots(1, 2, figsize=(fs.COL2, 2.35), gridspec_kw=dict(wspace=0.42, width_ratios=[1.15, 1.0]))
ax = axs[0]
keys = [k for k in AB if k != 'A0 Full']
J0 = AB['A0 Full']['util_mean']
d = np.array([100 * (AB[k]['util_mean'] / J0 - 1) for k in keys])
yy = np.arange(len(keys))[::-1]
ax.barh(yy, d, color='0.55', ec='k', lw=0.5, height=0.6)
for yi, di in zip(yy, d):
    ax.text(di + 0.08, yi, '+%.1f%%' % di, va='center', fontsize=6)
ax.set_yticks(yy); ax.set_yticklabels([k.split(' ', 1)[1] for k in keys])
ax.set_xlabel('increase of $J$ over the full design (%)')
ax.set_xlim(0, max(d) * 1.35)
ax.set_title('(a) ablation (each variant re-optimised)', pad=4)
ax = axs[1]
nm = ['$\\varepsilon_{cell}$', '$\\varepsilon_{A}$', '$p_0$', '$\\beta_f$', '$E_{a,b}$', '$\\sigma_{o,50}$',
      '$E_{a,o}$', '$G_{ion}$', '$E_\\mu$', '$a$', '$\\alpha_B$', '$D$']
S1 = np.array(SB['rel_gain']['S1']); ST = np.array(SB['rel_gain']['ST']); STc = np.array(SB['rel_gain']['ST_conf'])
order = np.argsort(ST)
yy = np.arange(len(nm))
ax.barh(yy - 0.18, ST[order], height=0.34, color='0.35', ec='k', lw=0.4, label='total $S_T$', xerr=STc[order],
        error_kw=dict(lw=0.5, capsize=1.2))
ax.barh(yy + 0.18, np.clip(S1[order], 0, None), height=0.34, color='white', ec='k', lw=0.4, label='first order $S_1$')
ax.set_yticks(yy); ax.set_yticklabels([nm[i] for i in order])
ax.set_xlabel('Sobol index of relative gain $g$')
ax.legend(loc='lower right', fontsize=6)
ax.set_title('(b) variance-based sensitivity', pad=4)
fig.savefig('fig7_ablation_sobol.png')

# ---------------- Fig. 8 ----------------
MC = json.load(open('res_mc.json'))
J = {k: np.array(v)[:, 0] for k, v in MC.items()}
fig, axs = plt.subplots(1, 2, figsize=(fs.COL2, 2.25), gridspec_kw=dict(wspace=0.32))
ax = axs[0]
lab = dict(aramid_proxy='D1 aramid-pulp proxy', strict='D5 exact matching', uniform='D6 robust uniform',
           graded='D7 robust graded')
sty = dict(aramid_proxy=('0.55', '-.'), strict=('0.4', '--'), uniform=('0.7', ':'), graded=('k', '-'))
for k in ['strict', 'aramid_proxy', 'uniform', 'graded']:
    g = np.sort(100 * (1 - J[k] / J['kraft']))
    ax.plot(g, np.arange(1, len(g) + 1) / len(g), color=sty[k][0], ls=sty[k][1], lw=1.3 if k == 'graded' else 1.0,
            label=lab[k])
ax.axvline(0, color='0.6', lw=0.5)
ax.set_xlabel('relative gain over kraft $g$ (%)'); ax.set_ylabel('empirical CDF')
ax.legend(loc='upper left', fontsize=6)
ax.set_title('(a) 300 parameter draws', pad=4)
ax = axs[1]
A = np.array(MC['kraft']); G = np.array(MC['graded'])
ax.scatter(A[:, 1], G[:, 1], s=6, facecolors='white', edgecolors='k', lw=0.4, label='oil $E_o^{\\max}$')
ax.scatter(A[:, 2] / 3, G[:, 2] / 3, s=6, marker='^', facecolors='0.6', edgecolors='0.3', lw=0.3,
           label='paper $E_p^{\\max}/\\kappa$')
lo = min(A[:, 1].min(), (G[:, 2] / 3).min()) * 0.95; hi = max(A[:, 2].max() / 3, A[:, 1].max()) * 1.03
ax.plot([lo, hi], [lo, hi], color='0.5', lw=0.6, ls='--')
ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
ax.set_xlabel('kraft/NE (kV mm$^{-1}$)'); ax.set_ylabel('D7 robust graded (kV mm$^{-1}$)')
ax.legend(loc='upper left', fontsize=6)
ax.set_title('(b) paired scenario-mean stresses', pad=4)
fig.savefig('fig8_mc.png')
print('ok', Jstar)
