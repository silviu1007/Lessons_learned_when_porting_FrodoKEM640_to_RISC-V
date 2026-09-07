"""
fig6_6_windowed_encaps_decaps_percent.py
=========================================
Figure 6.6: Percentage improvement of Windowed assembly over SW-only for
Encaps and Decaps, across five optimisation levels.

DATA SOURCE: sw_vs_asm3.txt  (v3 windowed standalone benchmark)

OUTPUT:
  fig6_6_windowed_encaps_decaps_percent.pdf
  fig6_6_windowed_encaps_decaps_percent.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']

enc_delta = [-39.1, -8.3, -4.8, -5.2, -14.3]
dec_delta = [-38.8, -8.2, -4.8, -5.2, -13.0]

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.alpha': 0.35,
})

x = np.arange(len(LEVELS))
w = 0.3

fig, ax = plt.subplots(figsize=(7, 3.8))

ax.bar(x - w/2, enc_delta, w, color='#C94316',  label='Encaps')
ax.bar(x + w/2, dec_delta, w, color='#A8C916', label='Decaps')

for i, (e, d) in enumerate(zip(enc_delta, dec_delta)):
    ax.text(i - w/2, e - 1.2, f'{e:.1f}%', ha='center', va='top', fontsize=8)
    ax.text(i + w/2, d - 1.2, f'{d:.1f}%', ha='center', va='top', fontsize=8)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(LEVELS)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('Δ vs C-only (%)')
ax.set_title(
    'Encaps and Decaps improvement: Windowed over C-only baseline\n'
    '(negative = assembly faster)'
)
ax.legend()
ax.set_ylim(min(enc_delta + dec_delta) - 8, 5)

fig.tight_layout()
fig.savefig('fig6_6_windowed_encaps_decaps_percent.pdf', bbox_inches='tight')
fig.savefig('fig6_6_windowed_encaps_decaps_percent.png', dpi=150, bbox_inches='tight')
print("Saved fig6_6_windowed_encaps_decaps_percent.pdf / .png")