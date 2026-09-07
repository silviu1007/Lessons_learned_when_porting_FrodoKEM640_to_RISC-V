# plot_section67.py  ← three plots for section 6.7

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

OPT = ['-O0', '-O1', '-O2', '-O3', '-Os']
x   = np.arange(len(OPT))

# ── Data ──────────────────────────────────────────────────────────────────────
sw_keygen  = [43131.2, 11317.8, 17808.6, 14657.6, 13486.2]
sw_enc     = [33858.4,  8625.4, 14874.0, 14736.3,  9807.4]
sw_dec     = [33682.4,  8604.6, 14907.4, 14611.1, 10001.1]
sw_keygen_sd = [10037.0, 1788.5, 2280.0, 1764.8,  647.9]
sw_enc_sd    = [ 6382.9, 1468.8, 2009.6, 1581.4, 1236.9]
sw_dec_sd    = [10365.8, 1410.4, 1646.9, 1835.4,  835.0]

v1_keygen  = [20341.9,  7350.8, 13734.6, 13669.4,  8693.8]
v1_enc     = [21723.9,  7584.1, 14305.2, 14094.1,  8919.3]
v1_dec     = [22278.2,  7800.7, 14321.0, 13878.0,  9052.1]
v1_keygen_sd = [4754.4,  363.0, 1867.7, 1077.5,  426.8]
v1_enc_sd    = [3535.2,  932.4, 1499.9, 1645.8, 1328.5]
v1_dec_sd    = [3576.1,  364.7, 1199.1, 1745.4, 1086.6]

v2_keygen  = [19204.2,  8073.9, 14082.6, 14808.1,  9149.6]
v2_enc     = [19617.6,  7717.8, 14085.9, 14708.1,  9063.4]
v2_dec     = [19831.6,  7894.1, 13795.0, 14647.7,  9332.2]
v2_keygen_sd = [3138.5,  428.7, 1770.6, 3548.5, 1501.0]
v2_enc_sd    = [3210.9, 1109.5, 1096.7, 2224.1, 1144.7]
v2_dec_sd    = [2435.2,  935.0, 1782.1, 2483.3,  206.4]

# ── Plot 1: Three-way absolute ────────────────────────────────────────────────
w = 0.25
fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=False)
fig.suptitle('Wall-clock time: SW-only vs both combined assembly configurations\n'
             '(100 runs, error bars = 1 std dev)', fontsize=11)

plot_data = [
    ('KeyGen', sw_keygen, sw_keygen_sd, v1_keygen, v1_keygen_sd, v2_keygen, v2_keygen_sd),
    ('Encaps', sw_enc,    sw_enc_sd,    v1_enc,    v1_enc_sd,    v2_enc,    v2_enc_sd),
    ('Decaps', sw_dec,    sw_dec_sd,    v1_dec,    v1_dec_sd,    v2_dec,    v2_dec_sd),
]
kw = dict(capsize=3, error_kw={'linewidth': 0.8})
for ax, (op, sm, ss, v1m, v1s, v2m, v2s) in zip(axes, plot_data):
    ax.bar(x - w, sm,  w, yerr=ss,  label='SW-only',              color='#888888', **kw)
    ax.bar(x,     v1m, w, yerr=v1s, label='Accumulator+Windowed', color='#4C72B0', **kw)
    ax.bar(x + w, v2m, w, yerr=v2s, label='Paired-load+Windowed', color='#E07B39', **kw)
    ax.set_title(op)
    ax.set_xticks(x); ax.set_xticklabels(OPT)
    ax.set_xlabel('Optimisation level'); ax.set_ylabel('Time (µs)')
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda v, _: f'{v/1000:.0f}k' if v >= 1000 else str(int(v))))
    ax.legend(fontsize=7); ax.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('v2v3_three_way_absolute.pdf', bbox_inches='tight')
plt.savefig('v2v3_three_way_absolute.png', dpi=150, bbox_inches='tight')
print("Saved v2v3_three_way_absolute")
plt.close()

# ── Plot 2: Both deltas vs SW ─────────────────────────────────────────────────
deltas_v1 = {'KeyGen': [-52.8,-35.1,-22.9, -6.7,-35.5],
             'Encaps': [-35.8,-12.1, -3.8, -4.4, -9.1],
             'Decaps': [-33.9, -9.3, -3.9, -5.0, -9.5]}
deltas_v2 = {'KeyGen': [-55.5,-28.7,-20.9, +1.0,-32.2],
             'Encaps': [-42.1,-10.5, -5.3, -0.2, -7.6],
             'Decaps': [-41.1, -8.3, -7.5, +0.3, -6.7]}

ops    = ['KeyGen','Encaps','Decaps']
colors = {'KeyGen':'#4C72B0','Encaps':'#DD8452','Decaps':'#55A868'}
bw_d   = 0.13

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
fig.suptitle('Improvement over SW-only baseline (negative = faster)', fontsize=11)

for ax, (title, deltas) in zip(axes,
    [('Accumulator + Windowed', deltas_v1),
     ('Paired-load + Windowed', deltas_v2)]):
    for op, off in zip(ops, [-bw_d, 0, bw_d]):
        bars = ax.bar(x + off, deltas[op], bw_d * 0.95,
                      label=op, color=colors[op], alpha=0.88)
        for bar, val in zip(bars, deltas[op]):
            ax.text(bar.get_x() + bar.get_width()/2,
                    val - 0.6, f'{val:.1f}%',
                    ha='center', va='top', fontsize=6.5)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_title(title); ax.set_xticks(x); ax.set_xticklabels(OPT)
    ax.set_xlabel('Optimisation level'); ax.set_ylabel('Δ vs SW-only (%)')
    ax.legend(fontsize=8); ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_ylim(-65, 8)

plt.tight_layout()
plt.savefig('v2v3_delta_vs_sw.pdf', bbox_inches='tight')
plt.savefig('v2v3_delta_vs_sw.png', dpi=150, bbox_inches='tight')
print("Saved v2v3_delta_vs_sw")
plt.close()

# ── Plot 3: Head-to-head ──────────────────────────────────────────────────────
h2h = {'KeyGen': [-5.6, +9.8, +2.5, +8.3, +5.2],
       'Encaps': [-9.7, +1.8, -1.5, +4.4, +1.6],
       'Decaps': [-11.0, +1.2, -3.7, +5.5, +3.1]}
bw_h = 0.22
offsets_h = {'KeyGen': -bw_h, 'Encaps': 0, 'Decaps': bw_h}

fig, ax = plt.subplots(figsize=(10, 5))
for op, off in offsets_h.items():
    bars = ax.bar(x + off, h2h[op], bw_h * 0.95,
                  label=op, color=colors[op], alpha=0.88)
    for bar, val in zip(bars, h2h[op]):
        va   = 'bottom' if val >= 0 else 'top'
        ypos = val + 0.2 if val >= 0 else val - 0.2
        ax.text(bar.get_x() + bar.get_width()/2,
                ypos, f'{val:+.1f}%',
                ha='center', va=va, fontsize=7.5)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x); ax.set_xticklabels(OPT)
ax.set_xlabel('Optimisation level')
ax.set_ylabel('Δ relative to accumulator+windowed (%)')
ax.set_title('Paired-load+windowed vs accumulator+windowed\n'
             '(positive = paired-load slower, negative = paired-load faster)',
             fontsize=10)
ax.legend(); ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.set_ylim(-15, 14)

plt.tight_layout()
plt.savefig('v2v3_delta_h2h.pdf', bbox_inches='tight')
plt.savefig('v2v3_delta_h2h.png', dpi=150, bbox_inches='tight')
print("Saved v2v3_delta_h2h")
plt.close()