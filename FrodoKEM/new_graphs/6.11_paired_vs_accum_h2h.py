"""
fig6_11_pairedload_vs_accumulator_headtohead.py
================================================
Figure 6.11: Paired-load+Windowed time relative to Accumulator+Windowed,
for KeyGen, Encaps, and Decaps, across five optimisation levels.

Positive values = paired-load combination is SLOWER than accumulator combination.
Negative values = paired-load combination is FASTER than accumulator combination.

This is the head-to-head comparison made possible by the shared-session
methodology: both assembly binaries ran against the same SW baseline in the
same sequential session (tot_fara_noise.txt), so the relative comparison
between them is direct.

DATA SOURCE: tot_fara_noise.txt  (combined v1+v3 and v2+v3 session)

OUTPUT:
  fig6_11_pairedload_vs_accumulator_headtohead.pdf
  fig6_11_pairedload_vs_accumulator_headtohead.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# rel = (v2v3_mean - v1v3_mean) / v1v3_mean * 100
# positive = v2+v3 is slower, negative = v2+v3 is faster

LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']

rel_kg = [-5.6, +9.8, +2.5, +8.3, +5.2]
rel_en = [-9.7, +1.8, -1.5, +4.4, +1.6]
rel_de = [-11.0, +1.2, -3.7, +5.5, +3.1]

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.alpha': 0.35,
})

x = np.arange(len(LEVELS))
w = 0.25

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(x - w, rel_kg, w, color='#2166AC', label='KeyGen', alpha=1.00)
ax.bar(x,     rel_en, w, color='#2166AC', label='Encaps',  alpha=0.65)
ax.bar(x + w, rel_de, w, color='#2166AC', label='Decaps',  alpha=0.35)

for i, (kg, en, de) in enumerate(zip(rel_kg, rel_en, rel_de)):
    for val, offset in [(kg, -w), (en, 0), (de, w)]:
        ypos = val - 0.5 if val < 0 else val + 0.2
        va = 'top' if val < 0 else 'bottom'
        ax.text(i + offset, ypos, f'{val:.1f}%', ha='center', va=va, fontsize=7.5)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(LEVELS)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('Δ relative to Accumulator+Windowed (%)')
ax.set_title(
    'Paired-load+Windowed vs Accumulator+Windowed\n'
    '(positive = paired-load slower, negative = paired-load faster)'
)
ax.legend()

fig.tight_layout()
fig.savefig('fig6_11_pairedload_vs_accumulator_headtohead.pdf', bbox_inches='tight')
fig.savefig('fig6_11_pairedload_vs_accumulator_headtohead.png', dpi=150, bbox_inches='tight')
print("Saved fig6_11_pairedload_vs_accumulator_headtohead.pdf / .png")