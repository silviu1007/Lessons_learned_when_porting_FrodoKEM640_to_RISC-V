import matplotlib.pyplot as plt
import numpy as np

OPT_LEVELS = ["O0", "O1", "O2", "O3", "Os"]
labels = [f"-{o}" for o in OPT_LEVELS]

# Version 1 data (inner_mul_row)
v1_sw_mean  = [46702.5, 13489.6, 21122.6, 14393.4, 14194.7]
v1_sw_sd    = [10183.0,  2440.6,  2878.3,   164.3,  2338.0]
v1_asm_mean = [23208.4,  9061.3, 17032.7, 13424.7,  9260.9]
v1_asm_sd   = [ 5395.4,  1486.2,  4287.0,   213.0,   159.9]

#  Version 2 data (inner_mul_row_v2) 
v2_sw_mean  = [42563.2, 10785.0, 17338.5, 14371.8, 13100.2]
v2_sw_sd    = [ 6489.4,  1046.7,   212.5,   857.5,   195.4]
v2_asm_mean = [16488.6,  7799.6, 14293.8, 13936.7,  8873.5]
v2_asm_sd   = [  350.0,  1027.2,  2100.9,   266.2,   806.4]

v1_delta = [
    (v1_asm_mean[i] - v1_sw_mean[i]) / v1_sw_mean[i] * 100
    for i in range(len(OPT_LEVELS))
]
v2_delta = [
    (v2_asm_mean[i] - v2_sw_mean[i]) / v2_sw_mean[i] * 100
    for i in range(len(OPT_LEVELS))
]

SW_COLOR = "#4C72B0"
V1_COLOR = "#DD8452"
V2_COLOR = "#55A868"
plt.rcParams.update({
    "font.family": "serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

x = np.arange(len(OPT_LEVELS))
width = 0.25


# Use v2 sw as the baseline (they differ slightly due to different runs, so show all three: sw_v1, asm_v1, asm_v2)
fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(x - width,     v1_sw_mean,  width, yerr=v1_sw_sd,
       label="SW only",      color=SW_COLOR, capsize=4, alpha=0.85,
       error_kw={"elinewidth": 1.2})
ax.bar(x,             v1_asm_mean, width, yerr=v1_asm_sd,
       label="Assembly v1",  color=V1_COLOR, capsize=4, alpha=0.85,
       error_kw={"elinewidth": 1.2})
ax.bar(x + width,     v2_asm_mean, width, yerr=v2_asm_sd,
       label="Assembly v2",  color=V2_COLOR, capsize=4, alpha=0.85,
       error_kw={"elinewidth": 1.2})

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_xlabel("Optimisation level")
ax.set_ylabel("KeyGen time (µs)")
ax.set_title(
    "KeyGen: SW-only vs Assembly v1 vs Assembly v2 under QEMU\n"
    "(100 runs, error bars = 1 std dev)"
)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("keygen_absolute_v1v2.pdf", bbox_inches="tight")
plt.savefig("keygen_absolute_v1v2.png", dpi=150, bbox_inches="tight")
print("Saved keygen_absolute_v1v2")
plt.close()

# Delta % both versions side by side
fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(x - width/2, v1_delta, width, label="Assembly v1",
       color=V1_COLOR, alpha=0.85)
ax.bar(x + width/2, v2_delta, width, label="Assembly v2",
       color=V2_COLOR, alpha=0.85)

ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_xlabel("Optimisation level")
ax.set_ylabel("Delta vs SW-only (%)")
ax.set_title(
    "KeyGen improvement: Assembly v1 and v2 over SW-only baseline\n"
    "(negative = assembly faster)"
)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.4)

for i, (d1, d2) in enumerate(zip(v1_delta, v2_delta)):
    ax.text(x[i] - width/2, d1 - 0.8, f"{d1:.1f}%",
            ha="center", va="top", fontsize=8,
            fontweight="bold", color="white")
    ax.text(x[i] + width/2, d2 - 0.8, f"{d2:.1f}%",
            ha="center", va="top", fontsize=8,
            fontweight="bold", color="white")

plt.tight_layout()
plt.savefig("keygen_delta_v1v2.pdf", bbox_inches="tight")
plt.savefig("keygen_delta_v1v2.png", dpi=150, bbox_inches="tight")
print("Saved keygen_delta_v1v2")
plt.close()

print("Done.")