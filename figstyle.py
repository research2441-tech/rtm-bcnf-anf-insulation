import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif', 'font.serif': ['Liberation Serif', 'TeX Gyre Termes', 'DejaVu Serif'],
    'mathtext.fontset': 'stix', 'font.size': 8, 'axes.labelsize': 8, 'axes.titlesize': 8,
    'legend.fontsize': 7, 'xtick.labelsize': 7, 'ytick.labelsize': 7, 'axes.linewidth': 0.6,
    'lines.linewidth': 1.0, 'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.major.width': 0.6,
    'ytick.major.width': 0.6, 'savefig.dpi': 400, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.03,
    'legend.frameon': False, 'axes.prop_cycle': matplotlib.cycler(color=['k', '0.35', '0.6', '0.8']),
    'image.cmap': 'Greys',
})
COL1, COL2 = 3.45, 7.1
GRAYS = ['k', '0.3', '0.5', '0.7']
STYLES = ['-', '--', '-.', ':']
MARKERS = ['o', 's', '^', 'D', 'v', 'P', 'X', '*']
