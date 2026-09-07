"""
fig6_4_accumulator_vs_pairedload_percent.py
============================================
Figure 6.4: Percentage improvement of Accumulator and Paired-load assemblies
over SW-only for KeyGen, across five optimisation levels.

DATA SOURCES:
  sw_vs_asm1.txt  (v1 accumulator standalone)
  sw_vs_asm2.txt  (v2 paired-load standalone)

OUTPUT:
  fig6_4_accumulator_vs_pairedload_percent.pdf
  fig6_4_accumulator_vs_pairedload_percent.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ── Data (computed from sw_vs_asm1.txt and sw_vs_asm2.txt) ───────────────────
LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']

v1_delta = [-50.3, -32.8, -19.4, -6.7, -34.8]   # accumulator vs its SW
v2_delta = [-61.3, -27.7, -17.6, -3.0, -32.3]   # paired-load vs its SW

# ── Plot ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.alpha': 0.35,
})

x = np.arange(len(LEVELS))
w = 0.3

fig, ax = plt.subplots(figsize=(7, 3.8))

ax.bar(x - w/2, v1_delta, w, color='green', label='Accumulator')
ax.bar(x + w/2, v2_delta, w, color='orange', label='Paired-load')

for i, (d1, d2) in enumerate(zip(v1_delta, v2_delta)):
    ax.text(i - w/2, d1 - 1.2, f'{d1:.1f}%', ha='center', va='top', fontsize=8)
    ax.text(i + w/2, d2 - 1.2, f'{d2:.1f}%', ha='center', va='top', fontsize=8)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(LEVELS)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('Δ vs C-only (%)')
ax.set_title(
    'KeyGen improvement: Accumulator and Paired-load over C-only baseline\n'
    '(negative = assembly faster)'
)
ax.legend()
ax.set_ylim(min(v1_delta + v2_delta) - 8, 5)

fig.tight_layout()
fig.savefig('fig6_4_accumulator_vs_pairedload_percent.pdf', bbox_inches='tight')
fig.savefig('fig6_4_accumulator_vs_pairedload_percent.png', dpi=150, bbox_inches='tight')
print("Saved fig6_4_accumulator_vs_pairedload_percent.pdf / .png")