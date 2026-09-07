"""
fig6_3_accumulator_vs_pairedload_absolute.py
=============================================
Figure 6.3: KeyGen wall-clock time, SW-only vs Accumulator vs Paired-load,
across five optimisation levels. Error bars = 1 standard deviation over 100 runs.

DATA SOURCES:
  sw_vs_asm1.txt  (v1 accumulator standalone — provides SW and accumulator bars)
  sw_vs_asm2.txt  (v2 paired-load standalone — provides paired-load bars)

Note: each file has its own SW-only baseline. The SW bars shown are the average
of the two baselines, which are very close to each other.

OUTPUT:
  fig6_3_accumulator_vs_pairedload_absolute.pdf
  fig6_3_accumulator_vs_pairedload_absolute.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']

# From sw_vs_asm1.txt
sw1_mean = [46702.5, 13489.6, 21122.6, 14393.4, 14194.7]
sw1_sd   = [10183.0,  2440.6,  2878.3,   164.3,  2338.0]
v1_mean  = [23208.4,  9061.3, 17032.7, 13424.7,  9260.9]
v1_sd    = [ 5395.4,  1486.2,  4287.0,   213.0,   159.9]

# From sw_vs_asm2.txt
sw2_mean = [42563.2, 10785.0, 17338.5, 14371.8, 13100.2]
sw2_sd   = [ 6489.4,  1046.7,   212.5,   857.5,   195.4]
v2_mean  = [16488.6,  7799.6, 14293.8, 13936.7,  8873.5]
v2_sd    = [  350.0,  1027.2,  2100.9,   266.2,   806.4]

# Average the two SW baselines for display
sw_mean = [(a + b) / 2 for a, b in zip(sw1_mean, sw2_mean)]
sw_sd   = [(a + b) / 2 for a, b in zip(sw1_sd,   sw2_sd)]

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.alpha': 0.35,
})

x = np.arange(len(LEVELS))
w = 0.25

fig, ax = plt.subplots(figsize=(7, 4))

ax.bar(x - w, sw_mean, w, yerr=sw_sd,  color='#444444', label='C-only',
       capsize=3, error_kw={'elinewidth': 1})
ax.bar(x,     v1_mean, w, yerr=v1_sd,  color='green', label='Accumulator',
       capsize=3, error_kw={'elinewidth': 1})
ax.bar(x + w, v2_mean, w, yerr=v2_sd,  color='orange', label='Paired-load',
       capsize=3, error_kw={'elinewidth': 1})

ax.set_xticks(x)
ax.set_xticklabels(LEVELS)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('KeyGen time (µs)')
ax.set_title(
    'KeyGen: C-only vs Accumulator vs Paired-load under QEMU\n'
    '(100 runs, error bars = 1 std dev)'
)
ax.legend()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'{int(v):,}'))

fig.tight_layout()
fig.savefig('fig6_3_accumulator_vs_pairedload_absolute.pdf', bbox_inches='tight')
fig.savefig('fig6_3_accumulator_vs_pairedload_absolute.png', dpi=150, bbox_inches='tight')
print("Saved fig6_3_accumulator_vs_pairedload_absolute.pdf / .png")