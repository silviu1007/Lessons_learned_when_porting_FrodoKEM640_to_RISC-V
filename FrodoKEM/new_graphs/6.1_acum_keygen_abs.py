"""
fig6_1_accumulator_keygen_absolute.py
======================================
Figure 6.1: KeyGen wall-clock time, SW-only vs Accumulator assembly, across
five optimisation levels. Error bars = 1 standard deviation over 100 runs.

DATA SOURCE: sw_vs_asm1.txt  (v1 accumulator standalone benchmark)

OUTPUT:
  fig6_1_accumulator_keygen_absolute.pdf  (for LaTeX inclusion)
  fig6_1_accumulator_keygen_absolute.png  (for preview)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── Data (from sw_vs_asm1.txt) ───────────────────────────────────────────────
LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']

sw_mean = [46702.5, 13489.6, 21122.6, 14393.4, 14194.7]
sw_sd   = [10183.0,  2440.6,  2878.3,   164.3,  2338.0]

asm_mean = [23208.4,  9061.3, 17032.7, 13424.7,  9260.9]
asm_sd   = [ 5395.4,  1486.2,  4287.0,   213.0,   159.9]

# ── Plot ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.alpha': 0.35,
})

x = np.arange(len(LEVELS))
w = 0.35

fig, ax = plt.subplots(figsize=(6, 4))

ax.bar(x - w/2, sw_mean,  w, yerr=sw_sd,  color='#444444', label='C-only',
       capsize=3, error_kw={'elinewidth': 1})
ax.bar(x + w/2, asm_mean, w, yerr=asm_sd, color='green', label='Accumulator',
       capsize=3, error_kw={'elinewidth': 1})

ax.set_xticks(x)
ax.set_xticklabels(LEVELS)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('KeyGen time (µs)')
ax.set_title(
    'KeyGen: C-only vs Accumulator under QEMU\n'
    '(100 runs, error bars = 1 std dev)'
)
ax.legend()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'{int(v):,}'))

fig.tight_layout()
fig.savefig('fig6_1_accumulator_keygen_absolute.pdf', bbox_inches='tight')
fig.savefig('fig6_1_accumulator_keygen_absolute.png', dpi=150, bbox_inches='tight')
print("Saved fig6_1_accumulator_keygen_absolute.pdf / .png")