# plot_delta_vs_sw.py

import matplotlib.pyplot as plt
import numpy as np

OPT = ['-O0', '-O1', '-O2', '-O3', '-Os']
x   = np.arange(len(OPT))

deltas_v1v3 = {
    'KeyGen': [-58.2, -39.2, -31.9, -17.8, -44.0],
    'Encaps': [-44.8, -18.2, -18.7, -16.4, -23.1],
    'Decaps': [-43.7, -15.8, -16.3, -15.8, -23.1],
}
deltas_v2v3 = {
    'KeyGen': [-57.9, -36.1, -30.9, -16.8, -39.6],
    'Encaps': [-44.7, -21.2, -19.0, -17.6, -25.4],
    'Decaps': [-45.0, -17.4, -16.9, -20.4, -24.5],
}

ops    = ['KeyGen', 'Encaps', 'Decaps']
colors = {'KeyGen': '#4C72B0', 'Encaps': '#DD8452', 'Decaps': '#55A868'}
bw     = 0.13

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
fig.suptitle('Improvement over SW-only baseline\n'
             '(negative = assembly faster)', fontsize=11)

for ax, (label, deltas) in zip(axes,
        [('Accumulator + Windowed', deltas_v1v3),
         ('Paired-load + Windowed',  deltas_v2v3)]):
    offsets = [-bw, 0, bw]
    for op, off in zip(ops, offsets):
        bars = ax.bar(x + off, deltas[op], bw * 0.95,
                      label=op, color=colors[op], alpha=0.88)
        for bar, val in zip(bars, deltas[op]):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    val - 0.8, f'{val:.1f}%',
                    ha='center', va='top', fontsize=6.5)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_title(label)
    ax.set_xticks(x)
    ax.set_xticklabels(OPT)
    ax.set_xlabel('Optimisation level')
    ax.set_ylabel('Δ vs SW-only (%)')
    ax.legend(fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_ylim(-70, 5)

plt.tight_layout()
plt.savefig('v2v3_delta_vs_sw.pdf', bbox_inches='tight')
plt.savefig('v2v3_delta_vs_sw.png', dpi=150, bbox_inches='tight')
print("Saved v2v3_delta_vs_sw")
plt.close()