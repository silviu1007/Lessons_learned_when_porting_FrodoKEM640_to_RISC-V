"""
fig6_9_all_three_absolute.py
=============================
Figure 6.9: Wall-clock time for KeyGen, Encaps, and Decaps, comparing all
three configurations: SW-only, Accumulator+Windowed, and Paired-load+Windowed,
across five optimisation levels. Error bars = 1 standard deviation over 100 runs.

All three binaries were run in the SAME sequential session to share a single
SW-only baseline, which is what makes the head-to-head comparison in Fig 6.11
valid.

DATA SOURCE: tot_fara_noise.txt  (combined v1+v3 and v2+v3 session)

OUTPUT:
  fig6_9_all_three_absolute.pdf
  fig6_9_all_three_absolute.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']

sw_kg_mean = [43131.2, 11317.8, 17808.6, 14657.6, 13486.2]
sw_kg_sd   = [10037.0,  1788.5,  2280.0,  1764.8,   647.9]
sw_en_mean = [33858.4,  8625.4, 14874.0, 14736.3,  9807.4]
sw_en_sd   = [ 6382.9,  1468.8,  2009.6,  1581.4,  1236.9]
sw_de_mean = [33682.4,  8604.6, 14907.4, 14611.1, 10001.1]
sw_de_sd   = [10365.8,  1410.4,  1646.9,  1835.4,   835.0]

v1v3_kg_mean = [20341.9,  7350.8, 13734.6, 13669.4,  8693.8]
v1v3_kg_sd   = [ 4754.4,   363.0,  1867.7,  1077.5,   426.8]
v1v3_en_mean = [21723.9,  7584.1, 14305.2, 14094.1,  8919.3]
v1v3_en_sd   = [ 3535.2,   932.4,  1499.9,  1645.8,  1328.5]
v1v3_de_mean = [22278.2,  7800.7, 14321.0, 13878.0,  9052.1]
v1v3_de_sd   = [ 3576.1,   364.7,  1199.1,  1745.4,  1086.6]

v2v3_kg_mean = [19204.2,  8073.9, 14082.6, 14808.1,  9149.6]
v2v3_kg_sd   = [ 3138.5,   428.7,  1770.6,  3548.5,  1501.0]
v2v3_en_mean = [19617.6,  7717.8, 14085.9, 14708.1,  9063.4]
v2v3_en_sd   = [ 3210.9,  1109.5,  1096.7,  2224.1,  1144.7]
v2v3_de_mean = [19831.6,  7894.1, 13795.0, 14647.7,  9332.2]
v2v3_de_sd   = [ 2435.2,   935.0,  1782.1,  2483.3,   206.4]

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.alpha': 0.35,
})

x = np.arange(len(LEVELS))
w = 0.25

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

ops = [
    ('KeyGen', sw_kg_mean, sw_kg_sd, v1v3_kg_mean, v1v3_kg_sd, v2v3_kg_mean, v2v3_kg_sd),
    ('Encaps', sw_en_mean, sw_en_sd, v1v3_en_mean, v1v3_en_sd, v2v3_en_mean, v2v3_en_sd),
    ('Decaps', sw_de_mean, sw_de_sd, v1v3_de_mean, v1v3_de_sd, v2v3_de_mean, v2v3_de_sd),
]

for ax, (title, sw_m, sw_s, a1m, a1s, a2m, a2s) in zip(axes, ops):
    ax.bar(x - w, sw_m, w, yerr=sw_s, color='#444444', label='C-only',
           capsize=3, error_kw={'elinewidth': 1})
    ax.bar(x,     a1m,  w, yerr=a1s,  color='#2166AC', label='Accumulator+Windowed',
           capsize=3, error_kw={'elinewidth': 1})
    ax.bar(x + w, a2m,  w, yerr=a2s,  color='#D6604D', label='Paired-load+Windowed',
           capsize=3, error_kw={'elinewidth': 1})
    ax.set_xticks(x)
    ax.set_xticklabels(LEVELS)
    ax.set_xlabel('Optimisation level')
    ax.set_ylabel('Time (µs)' if title == 'KeyGen' else '')
    ax.set_title(title)
    ax.legend(fontsize=6.5)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'{int(v):,}'))

fig.suptitle(
    'Wall-clock time: C-only vs both combined assembly configurations\n'
    '(100 runs, error bars = 1 std dev)',
    fontsize=11
)
fig.tight_layout()
fig.savefig('fig6_9_all_three_absolute.pdf', bbox_inches='tight')
fig.savefig('fig6_9_all_three_absolute.png', dpi=150, bbox_inches='tight')
print("Saved fig6_9_all_three_absolute.pdf / .png")