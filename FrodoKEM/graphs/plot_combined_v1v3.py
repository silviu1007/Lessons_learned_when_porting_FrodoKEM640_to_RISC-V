# plot_combined_v1v3.py  ← for section 6.6

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

OPT = ['-O0', '-O1', '-O2', '-O3', '-Os']
x   = np.arange(len(OPT))
w   = 0.35

data = {
    'KeyGen': {
        'sw_mean':   [43131.2, 11317.8, 17808.6, 14657.6, 13486.2],
        'sw_sd':     [10037.0,  1788.5,  2280.0,  1764.8,   647.9],
        'asm_mean':  [20341.9,  7350.8, 13734.6, 13669.4,  8693.8],
        'asm_sd':    [ 4754.4,   363.0,  1867.7,  1077.5,   426.8],
    },
    'Encaps': {
        'sw_mean':   [33858.4,  8625.4, 14874.0, 14736.3,  9807.4],
        'sw_sd':     [ 6382.9,  1468.8,  2009.6,  1581.4,  1236.9],
        'asm_mean':  [21723.9,  7584.1, 14305.2, 14094.1,  8919.3],
        'asm_sd':    [ 3535.2,   932.4,  1499.9,  1645.8,  1328.5],
    },
    'Decaps': {
        'sw_mean':   [33682.4,  8604.6, 14907.4, 14611.1, 10001.1],
        'sw_sd':     [10365.8,  1410.4,  1646.9,  1835.4,   835.0],
        'asm_mean':  [22278.2,  7800.7, 14321.0, 13878.0,  9052.1],
        'asm_sd':    [ 3576.1,   364.7,  1199.1,  1745.4,  1086.6],
    },
}

COLORS = {'SW-only': '#5B8DB8', 'Accumulator+Windowed': '#4C72B0'}

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)
fig.suptitle('Wall-clock time: SW-only vs accumulator and windowed assembly\n'
             '(100 runs, error bars = 1 std dev)', fontsize=11)

for ax, op in zip(axes, ['KeyGen', 'Encaps', 'Decaps']):
    d = data[op]
    kw = dict(capsize=4, error_kw={'linewidth': 1})
    ax.bar(x - w/2, d['sw_mean'],  w, yerr=d['sw_sd'],
           label='SW-only',              color='#888888', **kw)
    ax.bar(x + w/2, d['asm_mean'], w, yerr=d['asm_sd'],
           label='Accumulator+Windowed', color='#4C72B0', **kw)
    ax.set_title(op)
    ax.set_xticks(x); ax.set_xticklabels(OPT)
    ax.set_xlabel('Optimisation level')
    ax.set_ylabel('Time (µs)')
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda v, _: f'{v/1000:.0f}k' if v >= 1000 else str(int(v))))
    ax.legend(fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('combined_absolute_v1v3.pdf', bbox_inches='tight')
plt.savefig('combined_absolute_v1v3.png', dpi=150, bbox_inches='tight')
print("Saved combined_absolute_v1v3")
plt.close()

deltas = {
    'KeyGen': [-52.8, -35.1, -22.9, -6.7, -35.5],
    'Encaps': [-35.8, -12.1,  -3.8, -4.4,  -9.1],
    'Decaps': [-33.9,  -9.3,  -3.9, -5.0,  -9.5],
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
        ax.text(bar.get_x() + bar.get_width() / 2,
                val - 0.5, f'{val:.1f}%',
                ha='center', va='top', fontsize=7.5)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x); ax.set_xticklabels(OPT)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('Δ vs SW-only (%)')
ax.set_title('Accumulator and windowed assembly improvement over SW-only\n'
             '(negative = assembly faster)', fontsize=11)
ax.legend(); ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.set_ylim(min(min(v) for v in deltas.values()) - 5, 5)

plt.tight_layout()
plt.savefig('combined_delta_v1v3.pdf', bbox_inches='tight')
plt.savefig('combined_delta_v1v3.png', dpi=150, bbox_inches='tight')
print("Saved combined_delta_v1v3")
plt.close()