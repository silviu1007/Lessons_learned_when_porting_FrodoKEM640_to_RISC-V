"""
fig6_8_combined_accumulator_windowed_percent.py
================================================
Figure 6.8: Percentage improvement of Accumulator+Windowed assembly over
SW-only, for KeyGen, Encaps, and Decaps, across five optimisation levels.

DATA SOURCE: tot_fara_noise.txt  (combined v1+v3 and v2+v3 session)
             → uses the SW-only and v1+v3 columns only

OUTPUT:
  fig6_8_combined_accumulator_windowed_percent.pdf
  fig6_8_combined_accumulator_windowed_percent.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']

# (v1v3_mean - sw_mean) / sw_mean * 100
kg_delta = [-52.8, -35.1, -22.9, -6.7, -35.5]
en_delta = [-35.8, -12.1,  -3.8, -4.4,  -9.1]
de_delta = [-33.9,  -9.3,  -3.9, -5.0,  -9.5]


plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.alpha': 0.35,
})

x = np.arange(len(LEVELS))
w = 0.25

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(x - w, kg_delta, w, color='green', label='KeyGen', alpha=1.00)
ax.bar(x,     en_delta, w, color='#C94316', label='Encaps',  alpha=1)
ax.bar(x + w, de_delta, w, color='#A8C916', label='Decaps',  alpha=1)

for i, (kg, en, de) in enumerate(zip(kg_delta, en_delta, de_delta)):
    ax.text(i - w, kg - 0.8, f'{kg:.1f}%', ha='center', va='top', fontsize=7.5)
    ax.text(i,     en - 0.8, f'{en:.1f}%', ha='center', va='top', fontsize=7.5)
    ax.text(i + w, de - 0.8, f'{de:.1f}%', ha='center', va='top', fontsize=7.5)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(LEVELS)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('Δ vs C-only (%)')
ax.set_title(
    'Accumulator and Windowed assembly improvement over C-only\n'
    '(negative = assembly faster)'
)
ax.legend()
ax.set_ylim(min(kg_delta + en_delta + de_delta) - 6, 5)

fig.tight_layout()
fig.savefig('fig6_8_combined_accumulator_windowed_percent.pdf', bbox_inches='tight')
fig.savefig('fig6_8_combined_accumulator_windowed_percent.png', dpi=150, bbox_inches='tight')
print("Saved fig6_8_combined_accumulator_windowed_percent.pdf / .png")