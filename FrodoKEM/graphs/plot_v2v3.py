import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Data from benchmark output 
OPT = ['-O0', '-O1', '-O2', '-O3', '-Os']

data = {
    'KeyGen': {
        'sw_mean':   [36026.9, 11071.2, 17264.2, 14133.8, 13034.1],
        'sw_sd':     [  910.6,   569.2,   534.7,   265.6,   236.9],
        'asm_mean':  [16894.4,  7707.1, 13804.8, 13529.4,  8874.8],
        'asm_sd':    [  408.4,   379.2,   668.8,   289.1,   158.7],
    },
    'Encaps': {
        'sw_mean':   [28306.0,  8319.5, 14627.4, 14157.9,  9632.1],
        'sw_sd':     [  829.4,   427.8,   683.0,   388.0,   334.6],
        'asm_mean':  [17502.6,  7511.0, 13685.1, 13468.8,  8627.0],
        'asm_sd':    [  396.2,   503.5,   526.8,   294.9,   142.4],
    },
    'Decaps': {
        'sw_mean':   [28407.4,  8402.4, 14518.6, 14117.8,  9710.7],
        'sw_sd':     [  827.1,   397.6,   461.0,   285.9,   178.1],
        'asm_mean':  [17622.4,  7620.3, 13697.2, 13424.1,  8677.7],
        'asm_sd':    [  398.2,   327.0,   269.7,   270.3,   146.4],
    },
}

deltas = {
    'KeyGen': [-53.1, -30.4, -20.0, -4.3, -31.9],
    'Encaps': [-38.2,  -9.7,  -6.4, -4.9, -10.4],
    'Decaps': [-38.0,  -9.3,  -5.7, -4.9, -10.6],
}

COLORS = {'SW-only': '#5B8DB8', 'Assembly v2+v3': '#E07B39'}
x = np.arange(len(OPT))
w = 0.35

# Figure 1: Absolute times 
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)
fig.suptitle('Wall-clock time: SW-only vs Assembly v2+v3 under QEMU\n'
             '(100 runs, error bars = 1 std dev)', fontsize=12)

for ax, op in zip(axes, ['KeyGen', 'Encaps', 'Decaps']):
    d = data[op]
    ax.bar(x - w/2, d['sw_mean'],  w, yerr=d['sw_sd'],
           label='SW-only', color=COLORS['SW-only'],
           capsize=4, error_kw={'linewidth': 1})
    ax.bar(x + w/2, d['asm_mean'], w, yerr=d['asm_sd'],
           label='Assembly v2+v3', color=COLORS['Assembly v2+v3'],
           capsize=4, error_kw={'linewidth': 1})
    ax.set_title(op)
    ax.set_xticks(x)
    ax.set_xticklabels(OPT)
    ax.set_xlabel('Optimisation level')
    ax.set_ylabel('Time (µs)')
    ax.legend(fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda v, _: f'{v/1000:.0f}k' if v >= 1000 else str(int(v))))
    ax.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('v2v3_absolute.pdf', bbox_inches='tight')
plt.savefig('v2v3_absolute.png', dpi=150, bbox_inches='tight')
print("Saved v2v3_absolute.pdf")
plt.close()

# Figure 2: Delta bars 
fig, ax = plt.subplots(figsize=(10, 5))
bw = 0.22
offsets = {'KeyGen': -bw, 'Encaps': 0, 'Decaps': bw}
op_colors = {'KeyGen': '#4C72B0', 'Encaps': '#DD8452', 'Decaps': '#55A868'}

for op, off in offsets.items():
    vals = deltas[op]
    bars = ax.bar(x + off, vals, bw, label=op,
                  color=op_colors[op], alpha=0.88)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2,
                val - 0.8, f'{val:.1f}%',
                ha='center', va='top', fontsize=7.5)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(OPT)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('Delta vs SW-only (%)')
ax.set_title('Assembly v2+v3 improvement over SW-only baseline\n'
             '(negative = assembly faster)')
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.set_ylim(min(min(v) for v in deltas.values()) - 5, 5)

plt.tight_layout()
plt.savefig('v2v3_delta.pdf', bbox_inches='tight')
plt.savefig('v2v3_delta.png', dpi=150, bbox_inches='tight')
print("Saved v2v3_delta.pdf")
plt.close()

print("Done. Copy v2v3_absolute.pdf and v2v3_delta.pdf into your thesis images folder.")