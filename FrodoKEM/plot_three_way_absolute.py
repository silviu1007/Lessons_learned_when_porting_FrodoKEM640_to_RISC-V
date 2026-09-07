# plot_three_way_absolute.py

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

OPT = ['-O0', '-O1', '-O2', '-O3', '-Os']
x   = np.arange(len(OPT))
w   = 0.25

data = {
    'KeyGen': {
        'sw_mean':   [70924.8, 22448.0, 36731.9, 29292.0, 27828.1],
        'sw_sd':     [15142.8,  4167.8,  6581.8,  4163.9,  4190.8],
        'v1v3_mean': [29654.2, 13652.6, 25015.1, 24089.2, 15594.1],
        'v1v3_sd':   [ 3855.2,  1865.9,  2955.3,  2844.6,  2017.6],
        'v2v3_mean': [29846.7, 14349.0, 25367.2, 24384.0, 16804.2],
        'v2v3_sd':   [ 4351.1,  2656.6,  3883.4,  4197.8,  2654.9],
    },
    'Encaps': {
        'sw_mean':   [56083.8, 17837.8, 31081.0, 29991.5, 21439.3],
        'sw_sd':     [10922.5,  3421.7,  5281.8,  5791.1,  2998.9],
        'v1v3_mean': [30935.0, 14586.8, 25260.7, 25086.1, 16488.3],
        'v1v3_sd':   [ 4399.3,  2026.3,  3082.8,  3417.3,  1766.9],
        'v2v3_mean': [31041.4, 14061.5, 25180.0, 24717.9, 15988.1],
        'v2v3_sd':   [ 5304.5,  2505.1,  4288.4,  4161.7,  2841.1],
    },
    'Decaps': {
        'sw_mean':   [56321.7, 17366.2, 30376.1, 30133.7, 21513.4],
        'sw_sd':     [10902.5,  3450.4,  5139.0,  5460.0,  4671.4],
        'v1v3_mean': [31694.9, 14619.7, 25439.2, 25358.6, 16543.4],
        'v1v3_sd':   [ 4060.2,  2053.0,  2877.5,  3685.6,  2535.4],
        'v2v3_mean': [30956.8, 14344.8, 25257.0, 23999.7, 16250.2],
        'v2v3_sd':   [ 5669.3,  2022.7,  3409.9,  3664.5,  2428.6],
    },
}

COLORS = {
    'SW-only':              '#888888',
    'Accumulator+Windowed': '#4C72B0',
    'Paired-load+Windowed': '#E07B39',
}

fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=False)
fig.suptitle('Wall-clock time: SW-only vs combined assembly configurations\n'
             '(100 runs per binary, error bars = 1 std dev)', fontsize=11)

for ax, op in zip(axes, ['KeyGen', 'Encaps', 'Decaps']):
    d = data[op]
    kw = dict(capsize=3, error_kw={'linewidth': 0.8})
    ax.bar(x - w, d['sw_mean'],   w, yerr=d['sw_sd'],
           label='SW-only',              color=COLORS['SW-only'],              **kw)
    ax.bar(x,     d['v1v3_mean'], w, yerr=d['v1v3_sd'],
           label='Accumulator+Windowed', color=COLORS['Accumulator+Windowed'], **kw)
    ax.bar(x + w, d['v2v3_mean'], w, yerr=d['v2v3_sd'],
           label='Paired-load+Windowed', color=COLORS['Paired-load+Windowed'], **kw)
    ax.set_title(op)
    ax.set_xticks(x)
    ax.set_xticklabels(OPT)
    ax.set_xlabel('Optimisation level')
    ax.set_ylabel('Time (µs)')
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda v, _: f'{v/1000:.0f}k' if v >= 1000 else str(int(v))))
    ax.legend(fontsize=7)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('v2v3_three_way_absolute.pdf', bbox_inches='tight')
plt.savefig('v2v3_three_way_absolute.png', dpi=150, bbox_inches='tight')
print("Saved v2v3_three_way_absolute")
plt.close()