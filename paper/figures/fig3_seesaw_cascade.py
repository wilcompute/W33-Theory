"""Fig 3: Seesaw cascade ladder — T^0 -> T^3 with W(3,3) rungs.

Outputs: paper/figures/fig3_seesaw_cascade.pdf  (and .png)

Usage:
    python paper/figures/fig3_seesaw_cascade.py

Requires: numpy, matplotlib
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# ── W(3,3) cascade data ───────────────────────────────────────────────────────
STEPS = [
    {"step": r"$T^0$", "mu2": 1/4,   "rung": r"$1/\mu = 1/4$",
     "scale": r"LH neutrinos\n$m_\nu \sim 0.05$ eV",
     "energy": 0.05e-9,   "color": "steelblue"},
    {"step": r"$T^1$", "mu2": 0.140, "rung": r"$1/\Phi_6 = 1/7$",
     "scale": r"RH neutrinos\n$M_R \sim 10^{14.9}$ GeV",
     "energy": 10**14.9,  "color": "#2ca02c"},
    {"step": r"$T^2$", "mu2": 0.075, "rung": r"$1/\Phi_3 = 1/13$",
     "scale": r"2nd seesaw\n$\sim 10^{13}$ GeV",
     "energy": 1e13,      "color": "#ff7f0e"},
    {"step": r"$T^3$", "mu2": 0.040, "rung": r"$1/(2k-1) = 1/23$",
     "scale": r"3rd seesaw\n$\sim 10^{11}$ GeV",
     "energy": 1e11,      "color": "#9467bd"},
]

W33_FP = {1/4: r"$1/\mu$", 1/7: r"$1/\Phi_6$",
          1/13: r"$1/\Phi_3$", 1/23: r"$1/(2k-1)$"}

# ── Build figure ──────────────────────────────────────────────────────────────
fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11, 5.5),
                                         gridspec_kw={"width_ratios": [1.6, 1]})

# Left panel: ladder diagram
ax = ax_left
N = len(STEPS)
Y = [N - i for i in range(N)]  # top to bottom

for i, (step, y) in enumerate(zip(STEPS, Y)):
    col = step["color"]
    ax.hlines(y, 0.2, 0.8, color=col, lw=3, zorder=3)
    ax.text(0.05, y, step["step"], va="center", ha="center", fontsize=13,
            fontweight="bold", color=col)
    ax.text(0.95, y, step["rung"], va="center", ha="left", fontsize=10, color=col)
    ax.text(0.50, y + 0.18, step["scale"], va="bottom", ha="center",
            fontsize=8, color="gray", style="italic")

# Vertical arrows between rungs
for i in range(N - 1):
    y1, y2 = Y[i], Y[i+1]
    ratio = STEPS[i+1]["mu2"] / STEPS[i]["mu2"]
    ax.annotate("", xy=(0.50, y2 + 0.06), xytext=(0.50, y1 - 0.06),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.text(0.60, (y1 + y2) / 2, f"\u00d7{ratio:.3f}",
            va="center", ha="left", fontsize=9, color="darkred")

ax.set_xlim(-0.1, 1.5)
ax.set_ylim(0.3, N + 0.8)
ax.axis("off")
ax.set_title(r"Fig 3a: $W(3,3)$ Seesaw Cascade Ladder", fontsize=11, pad=8)

# Right panel: mu_eff^2 convergence plot
ax2 = ax_right
step_nums = [0, 1, 2, 3]
mu2_vals = [s["mu2"] for s in STEPS]
W33_vals = [1/4, 1/7, 1/13, 1/23]

ax2.plot(step_nums, mu2_vals, "o-", color="black", lw=2,
         label=r"Cascade $\mu_{\rm eff}^2$", zorder=5)
ax2.plot(step_nums, W33_vals, "s--", color="steelblue", lw=1.5, alpha=0.7,
         label=r"$W(3,3)$ fixed points")

for i, (s, w) in enumerate(zip(mu2_vals, W33_vals)):
    ax2.annotate(STEPS[i]["step"], xy=(i, s), xytext=(i + 0.1, s + 0.005),
                 fontsize=9, color="black")

converge_ratio = 0.5225
ax2.text(2.3, 0.03, f"convergence ratio\n$\\approx {converge_ratio}$\n"
         r"$\approx\sqrt{\Phi_4/\Phi_6^2}$",
         fontsize=9, color="darkred",
         bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", alpha=0.8))

ax2.set_xlabel("Cascade step $n$", fontsize=11)
ax2.set_ylabel(r"$\mu_{\rm eff}^2$", fontsize=11)
ax2.set_title(r"Fig 3b: Spectral RG Descent", fontsize=11)
ax2.set_xticks(step_nums)
ax2.set_xticklabels([s["step"] for s in STEPS])
ax2.set_ylim(0, 0.32)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
for ext in ("pdf", "png"):
    out = f"paper/figures/fig3_seesaw_cascade.{ext}"
    plt.savefig(out, dpi=200)
    print(f"Saved {out}")
plt.close()
