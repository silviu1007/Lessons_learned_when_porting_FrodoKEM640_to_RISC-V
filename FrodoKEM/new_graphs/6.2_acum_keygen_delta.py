"""
fig6_2_accumulator_keygen_percent.py
======================================
Figure 6.2: Percentage improvement of the Accumulator assembly over SW-only
for KeyGen, across five optimisation levels.

This was the figure that was BROKEN in the submitted draft — it showed the
windowed assembly's KeyGen sanity-check values (-0.4%, +0.6%, ...) instead
of the accumulator's actual KeyGen improvements.

DATA SOURCE: sw_vs_asm1.txt  (v1 accumulator standalone benchmark)

OUTPUT:
  fig6_2_accumulator_keygen_percent.pdf
  fig6_2_accumulator_keygen_percent.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ── Data (computed from sw_vs_asm1.txt) ──────────────────────────────────────
LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']

# (asm_mean - sw_mean) / sw_mean * 100, all negative = assembly is faster
delta_pct = [-50.3, -32.8, -19.4, -6.7, -34.8]

# ── Plot ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.alpha': 0.35,
})

x = np.arange(len(LEVELS))
fig, ax = plt.subplots(figsize=(6, 3.8))

bars = ax.bar(x, delta_pct, width=0.5, color='green')

# Label each bar with its value
for bar, val in zip(bars, delta_pct):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        val - 1.5,
        f'{val:.1f}%',
        ha='center', va='top', fontsize=9
    )

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(LEVELS)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('Δ vs C-only (%)')
ax.set_title(
    'KeyGen improvement: Accumulator over C-only baseline\n'
    '(negative = assembly faster)'
)
ax.set_ylim(min(delta_pct) - 8, 5)

fig.tight_layout()
fig.savefig('fig6_2_accumulator_keygen_percent.pdf', bbox_inches='tight')
fig.savefig('fig6_2_accumulator_keygen_percent.png', dpi=150, bbox_inches='tight')
print("Saved fig6_2_accumulator_keygen_percent.pdf / .png")