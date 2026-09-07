"""
fig6_5_windowed_encaps_decaps_absolute.py
==========================================
Figure 6.5: Encaps and Decaps wall-clock time, SW-only vs Windowed assembly,
across five optimisation levels. Error bars = 1 standard deviation over 100 runs.

The windowed assembly only modifies frodo_mul_add_sa_plus_e (the SA multiply),
which is called in Encaps and Decaps but not KeyGen. KeyGen values are included
as a sanity check (they should be ~0% delta).

DATA SOURCE: sw_vs_asm3.txt  (v3 windowed standalone benchmark)

OUTPUT:
  fig6_5_windowed_encaps_decaps_absolute.pdf
  fig6_5_windowed_encaps_decaps_absolute.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']

enc_sw_mean  = [27518.9,  8117.4, 14689.8, 14453.2,  9838.5]
enc_sw_sd    = [ 1680.1,   106.6,   175.4,   274.3,   771.3]
enc_asm_mean = [16767.7,  7441.9, 13984.0, 13704.7,  8431.2]
enc_asm_sd   = [  204.7,    86.5,   192.3,   299.8,   142.2]

dec_sw_mean  = [27546.0,  8170.7, 14622.5, 14395.5,  9817.2]
dec_sw_sd    = [  701.5,   105.6,   170.3,   282.2,   133.5]
dec_asm_mean = [16864.8,  7502.5, 13916.7, 13640.2,  8544.3]
dec_asm_sd   = [  238.2,    94.1,   208.0,   243.8,   715.6]

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.alpha': 0.35,
})

x = np.arange(len(LEVELS))
w = 0.35

fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=False)

for ax, sw_m, sw_s, am_m, am_s, op_title in [
    (axes[0], enc_sw_mean, enc_sw_sd, enc_asm_mean, enc_asm_sd, 'Encaps'),
    (axes[1], dec_sw_mean, dec_sw_sd, dec_asm_mean, dec_asm_sd, 'Decaps'),
]:
    ax.bar(x - w/2, sw_m, w, yerr=sw_s, color='#444444', label='C-only',
           capsize=3, error_kw={'elinewidth': 1})
    ax.bar(x + w/2, am_m, w, yerr=am_s, color='#16B9C9', label='Windowed',
           capsize=3, error_kw={'elinewidth': 1})
    ax.set_xticks(x)
    ax.set_xticklabels(LEVELS)
    ax.set_xlabel('Optimisation level')
    ax.set_ylabel('Time (µs)')
    ax.set_title(op_title)
    ax.legend()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'{int(v):,}'))

fig.suptitle(
    'Encaps and Decaps: C-only vs Windowed under QEMU\n'
    '(100 runs, error bars = 1 std dev)',
    fontsize=11
)
fig.tight_layout()
fig.savefig('fig6_5_windowed_encaps_decaps_absolute.pdf', bbox_inches='tight')
fig.savefig('fig6_5_windowed_encaps_decaps_absolute.png', dpi=150, bbox_inches='tight')
print("Saved fig6_5_windowed_encaps_decaps_absolute.pdf / .png")