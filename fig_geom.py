"""Fig. 2 (geometry) and Fig. 9 (2-D field maps)."""
import json, sys
import numpy as np
import figstyle as fs
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
import mw1d, fe2d

# ---------------- Fig. 2 ----------------
fig = plt.figure(figsize=(fs.COL2, 2.55))
ax = fig.add_axes([0.03, 0.12, 0.50, 0.78])
ax.set_xlim(-8, 60); ax.set_ylim(-9, 13); ax.axis('off')
x = 0.0
ax.add_patch(Rectangle((-6, 0), 6, 8, fc='k', ec='k'))
ax.text(-3, 9.0, 'HV valve\nwinding', ha='center', va='bottom', fontsize=6.5)
for k, (kind, t) in enumerate(mw1d.STACK):
    fc = '0.55' if kind == 'paper' else 'white'
    ax.add_patch(Rectangle((x, 0), t, 8, fc=fc, ec='k', lw=0.6))
    if kind == 'oil':
        ax.text(x + t / 2, 4, '%g' % t, ha='center', va='center', fontsize=6)
    x += t
ax.add_patch(Rectangle((x, 0), 4, 8, fc='0.85', ec='k', hatch='////', lw=0.6))
ax.text(x + 2, 9.0, 'core\n(0 V)', ha='center', va='bottom', fontsize=6.5)
ax.text(1.5, -1.0, 'wrap\n3 mm', ha='center', va='top', fontsize=6)
ax.text(27, 9.0, '4 pressboard barriers (3 mm), oil gaps in mm', ha='center', va='bottom', fontsize=6.3)
a = FancyArrowPatch((0, -5.6), (51, -5.6), arrowstyle='-|>', mutation_scale=8, lw=0.8, color='k')
ax.add_patch(a)
ax.text(0, -6.6, '$T_w$ (winding side)', ha='left', va='top', fontsize=6.3)
ax.text(51, -6.6, '$T_c$ (core side)', ha='right', va='top', fontsize=6.3)
ax.text(25.5, -4.9, 'linear temperature profile', ha='center', va='bottom', fontsize=6.0, style='italic')
ax.set_title('(a) 1-D barrier stack used in the robust design loop', fontsize=7.5, pad=2)

ax = fig.add_axes([0.61, 0.13, 0.36, 0.77])
g = fe2d.Geometry(h=1.0)
m = g.mat.T.astype(float)
img = np.where(m == -1, 0.0, np.where(m == 0, 1.0, 0.55))
ax.imshow(img, origin='lower', cmap='gray', vmin=0, vmax=1, extent=[g.r0, g.r1, g.z0, g.z1], aspect='auto',
          interpolation='nearest')
ax.set_xlabel('$r$ (mm)'); ax.set_ylabel('$z$ (mm)')
ax.text(388, 120, 'winding\n$V(t)$', color='w', ha='center', va='center', fontsize=6.5)
ax.text(395, 300, 'washer', ha='center', va='bottom', fontsize=6)
ax.text(452, 40, 'core at $r$ = 306 mm\n$\\phi=0$ (left edge)', ha='center', va='bottom', fontsize=5.8)
ax.text(400, 368, 'yoke, $\\phi=0$', ha='center', va='top', fontsize=6)
ax.text(470, 175, 'zero-flux edge', rotation=90, ha='center', va='center', fontsize=5.8)
ax.set_title('(b) 2-D axisymmetric verification model', fontsize=7.5, pad=2)
fig.savefig('fig2_geometry.png')

# ---------------- Fig. 9 ----------------
R = json.load(open('res_fe2d.json'))
keys = [('110-70|Kraft/NE', 'D0 kraft/NE'), ('110-70|Exact window matching', 'D5 exact matching'),
        ('110-70|Robust graded', 'D7 robust graded')]
fig, axs = plt.subplots(2, 3, figsize=(fs.COL2, 4.1), gridspec_kw=dict(wspace=0.08, hspace=0.32))
vmax = 16.0
for col, (k, lab) in enumerate(keys):
    rec = R[k]
    geo = rec['geom']
    mat = np.array(geo['mat']).T; r = np.array(geo['r']); z = np.array(geo['z'])
    for row, snap, ttl in [(0, 'dc', 'steady DC, $-U$'), (1, 'rev', '5 s after reversal ends')]:
        ax = axs[row, col]
        E = np.array(rec['maps'][snap]['E']).T
        E = np.where(mat == -1, np.nan, E)
        im = ax.imshow(E, origin='lower', extent=[r[0], r[-1], z[0], z[-1]], cmap='Greys', vmin=0, vmax=vmax,
                       aspect='auto', interpolation='nearest')
        ax.contour(r, z, (mat > 0).astype(float), levels=[0.5], colors='0.4', linewidths=0.35)
        ax.contour(r, z, (mat == -1).astype(float), levels=[0.5], colors='k', linewidths=0.6)
        ax.set_xlim(306, 470); ax.set_ylim(150, 380)
        ax.set_title('%s: %s' % (lab, ttl), fontsize=6.6, pad=2)
        if col == 0:
            ax.set_ylabel('$z$ (mm)')
        else:
            ax.set_yticklabels([])
        if row == 1:
            ax.set_xlabel('$r$ (mm)')
        else:
            ax.set_xticklabels([])
cax = fig.add_axes([0.92, 0.25, 0.012, 0.5])
cb = fig.colorbar(im, cax=cax); cb.set_label('$|\\mathbf{E}|$ (kV mm$^{-1}$)', fontsize=7); cb.ax.tick_params(labelsize=6)
fig.savefig('fig9_fe2d.png')
print('ok')
