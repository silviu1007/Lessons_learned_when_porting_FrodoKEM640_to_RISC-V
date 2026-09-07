# plot_delta_h2h.py

import matplotlib.pyplot as plt
import numpy as np

OPT = ['-O0', '-O1', '-O2', '-O3', '-Os']
x   = np.arange(len(OPT))

# positive = v2+v3 slower than v1+v3
deltas = {
    'KeyGen': [+0.6, +5.1, +1.4, +1.2, +7.8],
    'Encaps': [+0.3, -3.6, -0.3, -1.5, -3.0],
    'Decaps': [-2.3, -1.9, -0.7, -5.4, -1.8],
}

ops    = ['KeyGen', 'Encaps', 'Decaps']
colors = {'KeyGen': '#4C72B0', 'Encaps': '#DD8452', 'Decaps': '#55A868'}
bw     = 0.22
offsets = {'KeyGen': -bw, 'Encaps': 0, 'Decaps': bw}

fig, ax = plt.subplots(figsize=(10, 5))

for op, off in offsets.items():
    bars = ax.bar(x + off, deltas[op], bw * 0.95,
                  label=op, color=colors[op], alpha=0.88)
    for bar, val in zip(bars, deltas[op]):
        va   = 'bottom' if val >= 0 else 'top'
        ypos = val + 0.2 if val >= 0 else val - 0.2
        ax.text(bar.get_x() + bar.get_width() / 2,
                ypos, f'{val:+.1f}%',
                ha='center', va=va, fontsize=7.5)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(OPT)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('Δ relative to accumulator+windowed (%)')
ax.set_title('Paired-load+windowed vs accumulator+windowed\n'
             '(positive = paired-load is slower, negative = paired-load is faster)',
             fontsize=10)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.set_ylim(-10, 12)

plt.tight_layout()
plt.savefig('v2v3_delta_h2h.pdf', bbox_inches='tight')
plt.savefig('v2v3_delta_h2h.png', dpi=150, bbox_inches='tight')
print("Saved v2v3_delta_h2h")
plt.close()