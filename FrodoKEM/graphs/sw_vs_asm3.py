import matplotlib.pyplot as plt
import numpy as np

OPT_LEVELS = ["O0", "O1", "O2", "O3", "Os"]
labels = [f"-{o}" for o in OPT_LEVELS]

# Version 3 data (sa_mul_row)
sw_encaps_mean  = [27518.9,  8117.4, 14689.8, 14453.2,  9838.5]
sw_encaps_sd    = [ 1680.1,   106.6,   175.4,   274.3,   771.3]
asm_encaps_mean = [16767.7,  7441.9, 13984.0, 13704.7,  8431.2]
asm_encaps_sd   = [  204.7,    86.5,   192.3,   299.8,   142.2]

sw_decaps_mean  = [27546.0,  8170.7, 14622.5, 14395.5,  9817.2]
sw_decaps_sd    = [  701.5,   105.6,   170.3,   282.2,   133.5]
asm_decaps_mean = [16864.8,  7502.5, 13916.7, 13640.2,  8544.3]
asm_decaps_sd   = [  238.2,    94.1,   208.0,   243.8,   715.6]

encaps_delta = [
    (asm_encaps_mean[i] - sw_encaps_mean[i]) / sw_encaps_mean[i] * 100
    for i in range(len(OPT_LEVELS))
]
decaps_delta = [
    (asm_decaps_mean[i] - sw_decaps_mean[i]) / sw_decaps_mean[i] * 100
    for i in range(len(OPT_LEVELS))
]

SW_COLOR     = "#4C72B0"
ENCAPS_COLOR = "#DD8452"
DECAPS_COLOR = "#55A868"

plt.rcParams.update({
    "font.family": "serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

x = np.arange(len(OPT_LEVELS))
width = 0.25

# Plot 1: Absolute times (Encaps + Decaps side by side) 
fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)

for ax, op, sw_m, sw_s, asm_m, asm_s, color in [
    (axes[0], "Encaps", sw_encaps_mean, sw_encaps_sd,
     asm_encaps_mean, asm_encaps_sd, ENCAPS_COLOR),
    (axes[1], "Decaps", sw_decaps_mean, sw_decaps_sd,
     asm_decaps_mean, asm_decaps_sd, DECAPS_COLOR),
]:
    ax.bar(x - width/2, sw_m,  width, yerr=sw_s,
           label="SW only",     color=SW_COLOR, capsize=4, alpha=0.85,
           error_kw={"elinewidth": 1.2})
    ax.bar(x + width/2, asm_m, width, yerr=asm_s,
           label="Assembly v3", color=color,    capsize=4, alpha=0.85,
           error_kw={"elinewidth": 1.2})
    ax.set_title(op)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Optimisation level")
    ax.set_ylabel("Time (µs)")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)

fig.suptitle(
    "Encaps and Decaps: SW-only vs Assembly v3 under QEMU\n"
    "(100 runs, error bars = 1 std dev)",
    fontsize=12
)
plt.tight_layout()
plt.savefig("encaps_decaps_absolute_v3.pdf", bbox_inches="tight")
plt.savefig("encaps_decaps_absolute_v3.png", dpi=150, bbox_inches="tight")
print("Saved encaps_decaps_absolute_v3")
plt.close()

# Plot 2: Delta % both operations
fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(x - width/2, encaps_delta, width, label="Encaps",
       color=ENCAPS_COLOR, alpha=0.85)
ax.bar(x + width/2, decaps_delta, width, label="Decaps",
       color=DECAPS_COLOR, alpha=0.85)

ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_xlabel("Optimisation level")
ax.set_ylabel("Delta vs SW-only (%)")
ax.set_title(
    "Encaps and Decaps improvement: Assembly v3 over SW-only baseline\n"
    "(negative = assembly faster)"
)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.4)

for i, (de, dd) in enumerate(zip(encaps_delta, decaps_delta)):
    ax.text(x[i] - width/2, de - 0.5, f"{de:.1f}%",
            ha="center", va="top", fontsize=8,
            fontweight="bold", color="white")
    ax.text(x[i] + width/2, dd - 0.5, f"{dd:.1f}%",
            ha="center", va="top", fontsize=8,
            fontweight="bold", color="white")

plt.tight_layout()
plt.savefig("encaps_decaps_delta_v3.pdf", bbox_inches="tight")
plt.savefig("encaps_decaps_delta_v3.png", dpi=150, bbox_inches="tight")
print("Saved encaps_decaps_delta_v3")
plt.close()

print("Done.")