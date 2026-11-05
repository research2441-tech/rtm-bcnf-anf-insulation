"""Fig. 1: design framework (grayscale block diagram with explicit, non-overlapping arrows)."""
import figstyle as fs
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(fs.COL2, 3.05))
ax.set_xlim(0, 100); ax.set_ylim(0, 44); ax.axis('off')

def box(x, y, w, h, title, body, fc='white', lw=0.8, ls='-'):
    p = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.25,rounding_size=0.8', fc=fc, ec='k', lw=lw, ls=ls)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h - 1.6, title, ha='center', va='top', fontsize=7.4, fontweight='bold')
    ax.text(x + w / 2, y + h - 4.6, body, ha='center', va='top', fontsize=6.4, linespacing=1.25)
    return (x, y, w, h)

def arrow(p0, p1, ls='-', rad=0.0, text=None, toff=(0, 1.2), lw=0.9):
    a = FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=8, lw=lw, color='k', ls=ls,
                        connectionstyle='arc3,rad=%g' % rad, shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    if text:
        ax.text((p0[0] + p1[0]) / 2 + toff[0], (p0[1] + p1[1]) / 2 + toff[1], text, ha='center', va='bottom',
                fontsize=6.2, style='italic')

# top row
b1 = box(1, 26, 17, 15, 'Composition', 'ANF fraction $w_A$\nB-CNF fraction $w_C$\ncarboxylate $c_w$, $c_k$\nBNNS fraction $w_B$', fc='0.93')
b2 = box(23, 26, 18, 15, 'Property model', 'Looyenga $\\varepsilon_p$, porosity $p$\nbase + ionic $\\sigma_p(T)$\nFuoss dissociation $U_d(\\varepsilon_m)$\nNielsen tortuosity, $k_p$')
b3 = box(46, 26, 18, 15, 'Service scenarios', '5 thermal profiles\n$t_r$ = 10 s and 120 s\n4 ageing states\n(40 scenarios)')
b4 = box(69, 26, 30, 15, 'Exact RC-ladder solver', 'IEC polarity-reversal sequence\nmodal solution, no time-step error\npeak oil and paper fields,\ninterface charge')
# bottom row
b5 = box(69, 3, 30, 15, 'Robust utilisation', '$u_s=\\max(E_{o}^{\\max},E_{p}^{\\max}/\\kappa)$\n$J=\\overline{u_s}$ over scenarios', fc='0.93')
b6 = box(38, 3, 25, 15, 'GP surrogate + EI', 'Matérn-5/2 ARD kernel\nfeasible-set acquisition\nnext composition', fc='0.93')
b7 = box(1, 3, 31, 15, '2-D axisymmetric check', 'EQS finite volumes, $h$ = 1 and 0.5 mm\nRichardson extrapolation\nwinding corner, barriers, washer', ls='--')

# arrows (horizontal gaps kept clear of the boxes)
arrow((18.5, 33.5), (22.5, 33.5))
arrow((41.5, 33.5), (45.5, 33.5))
arrow((64.5, 33.5), (68.5, 33.5))
arrow((84, 25.5), (84, 18.5))                    # solver -> utilisation
arrow((68.5, 10.5), (63.5, 10.5))                # utilisation -> GP
# dashed feedback: GP proposes the next composition (reverse path, routed around the property box)
ax.plot([50.5, 50.5, 9.5], [18.6, 22.0, 22.0], 'k--', lw=0.9)
arrow((9.5, 22.0), (9.5, 25.6), ls='--')
ax.text(30.0, 22.5, 'next query $\\mathbf{x}_{n+1}$ (reverse path)', ha='center', va='bottom', fontsize=6.2, style='italic')
# best design goes to the 2-D check
arrow((37.5, 7.5), (32.5, 7.5), ls='--')
ax.text(35.0, 8.4, 'best $\\mathbf{x}^{\\star}$', ha='center', va='bottom', fontsize=6.2, style='italic')
fig.savefig('fig1_framework.png')
print('ok')
