"""
fig6_10_both_combinations_percent.py
======================================
Figure 6.10: Percentage improvement of both assembly combinations over SW-only,
shown in two side-by-side panels: Accumulator+Windowed (left) and
Paired-load+Windowed (right), across five optimisation levels.

DATA SOURCE: tot_fara_noise.txt  (combined v1+v3 and v2+v3 session)

OUTPUT:
  fig6_10_both_combinations_percent.pdf
  fig6_10_both_combinations_percent.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']

# v1+v3 vs SW
v1v3_kg = [-52.8, -35.1, -22.9,  -6.7, -35.5]
v1v3_en = [-35.8, -12.1,  -3.8,  -4.4,  -9.1]
v1v3_de = [-33.9,  -9.3,  -3.9,  -5.0,  -9.5]

# v2+v3 vs SW
v2v3_kg = [-55.5, -28.7, -20.9,  +1.0, -32.2]
v2v3_en = [-42.1, -10.5,  -5.3,  -0.2,  -7.6]
v2v3_de = [-41.1,  -8.3,  -7.5,  +0.3,  -6.7]

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.alpha': 0.35,
})

x = np.arange(len(LEVELS))
w = 0.25

fig, axes = plt.subplots(1, 2, figsize=(13, 4), sharey=True)

for ax, (d_kg, d_en, d_de), combo_label, colour in [
    (axes[0], (v1v3_kg, v1v3_en, v1v3_de), 'Accumulator + Windowed', '#2166AC'),
    (axes[1], (v2v3_kg, v2v3_en, v2v3_de), 'Paired-load + Windowed', '#D6604D'),
]:
    ax.bar(x - w, d_kg, w, color=colour, label='KeyGen', alpha=1.00)
    ax.bar(x,     d_en, w, color=colour, label='Encaps',  alpha=0.65)
    ax.bar(x + w, d_de, w, color=colour, label='Decaps',  alpha=0.35)

    for i, (kg, en, de) in enumerate(zip(d_kg, d_en, d_de)):
        for val, offset in [(kg, -w), (en, 0), (de, w)]:
            ypos = val - 0.8 if val < 0 else val + 0.3
            va = 'top' if val < 0 else 'bottom'
            ax.text(i + offset, ypos, f'{val:.1f}%', ha='center', va=va, fontsize=7.5)

    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(LEVELS)
    ax.set_xlabel('Optimisation level')
    ax.set_ylabel('Δ vs C-only (%)')
    ax.set_title(combo_label)
    ax.legend()

fig.suptitle('Improvement over C-only baseline (negative = faster)', fontsize=11)
fig.tight_layout()
fig.savefig('fig6_10_both_combinations_percent.pdf', bbox_inches='tight')
fig.savefig('fig6_10_both_combinations_percent.png', dpi=150, bbox_inches='tight')
print("Saved fig6_10_both_combinations_percent.pdf / .png")