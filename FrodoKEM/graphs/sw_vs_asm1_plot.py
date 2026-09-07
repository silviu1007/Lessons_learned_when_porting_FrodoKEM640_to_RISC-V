import matplotlib.pyplot as plt
import numpy as np

OPT_LEVELS = ["O0", "O1", "O2", "O3", "Os"]
labels = [f"-{o}" for o in OPT_LEVELS]

# ── Data from 100-run benchmark ────────────────────────────────────────────────
sw_keygen_mean  = [46702.5, 13489.6, 21122.6, 14393.4, 14194.7]
sw_keygen_sd    = [10183.0,  2440.6,  2878.3,   164.3,  2338.0]
asm_keygen_mean = [23208.4,  9061.3, 17032.7, 13424.7,  9260.9]
asm_keygen_sd   = [ 5395.4,  1486.2,  4287.0,   213.0,   159.9]

keygen_delta = [
    (asm_keygen_mean[i] - sw_keygen_mean[i]) / sw_keygen_mean[i] * 100
    for i in range(len(OPT_LEVELS))
]

SW_COLOR  = "#4C72B0"
ASM_COLOR = "#DD8452"
plt.rcParams.update({
    "font.family": "serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

x = np.arange(len(OPT_LEVELS))
width = 0.35

# ── Plot 1: Absolute times ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(x - width/2, sw_keygen_mean,  width, yerr=sw_keygen_sd,
       label="SW only", color=SW_COLOR, capsize=5, alpha=0.85,
       error_kw={"elinewidth": 1.5})
ax.bar(x + width/2, asm_keygen_mean, width, yerr=asm_keygen_sd,
       label="Assembly v1", color=ASM_COLOR, capsize=5, alpha=0.85,
       error_kw={"elinewidth": 1.5})

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_xlabel("Optimisation level")
ax.set_ylabel("KeyGen time (µs)")
ax.set_title(
    "KeyGen: SW-only vs Assembly v1 under QEMU\n"
    "(100 runs, error bars = 1 std dev)"
)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("keygen_absolute.pdf", bbox_inches="tight")
plt.savefig("keygen_absolute.png", dpi=150, bbox_inches="tight")
print("Saved keygen_absolute")
plt.close()

# ── Plot 2: Delta % bar chart ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(labels, keygen_delta, color=ASM_COLOR, alpha=0.85, width=0.5)

ax.axhline(0, color="black", linewidth=0.8)
ax.set_xlabel("Optimisation level")
ax.set_ylabel("Delta vs SW-only (%)")
ax.set_title(
    "KeyGen improvement: Assembly v1 over SW-only baseline\n"
    "(negative = assembly faster)"
)
ax.grid(axis="y", linestyle="--", alpha=0.4)

for bar, val in zip(bars, keygen_delta):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() - 0.8,
        f"{val:.1f}%",
        ha="center", va="top",
        fontsize=10, fontweight="bold", color="white"
    )

plt.tight_layout()
plt.savefig("keygen_delta.pdf", bbox_inches="tight")
plt.savefig("keygen_delta.png", dpi=150, bbox_inches="tight")
print("Saved keygen_delta")
plt.close()

print("Done.")