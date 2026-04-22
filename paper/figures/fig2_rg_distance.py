"""Fig 2: RG distance |delta|^2 bar chart — all SM sectors vs W(3,3) fixed points.

Outputs: paper/figures/fig2_rg_distance.pdf  (and .png)

Usage:
    python paper/figures/fig2_rg_distance.py

Requires: numpy, matplotlib
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── W(3,3) spectral fixed-point grid ──────────────────────────────────────────
W33_FP = np.array([1/4, 1/7, 1/13, 1/23])
W33_LABELS = [r"$1/\mu$", r"$1/\Phi_6$", r"$1/\Phi_3$", r"$1/(2k-1)$"]

# ── SM sector mu_eff^2 estimates (from oscillation data + RG running, PDG 2024)
# Each entry: (sector_label, mu_eff^2_central, uncertainty)
SECTORS = [
    (r"$\nu$ NH ($\sum=0.101$)",  0.2500, 0.002),
    (r"$\nu$ IH ($\sum=0.110$)",  0.2500, 0.003),
    (r"$\nu$ NH ($\sum=0.128$)",  1/6,    0.005),
    (r"$\nu$ IH ($\sum=0.122$)",  1/6,    0.005),
    (r"Charged leptons (RG)",      0.148,  0.010),
    (r"Up quarks (RG)",            0.134,  0.012),
    (r"Down quarks (RG)",          0.144,  0.011),
]

# RG distance: |mu_eff^2_sector - nearest W33 fixed point|^2
def rg_distance(mu_val):
    return float(np.min((W33_FP - mu_val)**2))

labels = [s[0] for s in SECTORS]
dists  = [rg_distance(s[1]) for s in SECTORS]
errs   = [2 * s[2] * abs(s[1] - W33_FP[np.argmin((W33_FP - s[1])**2)]) for s in SECTORS]

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4.5))

colors = ["steelblue", "steelblue", "tomato", "tomato",
          "#2ca02c", "#ff7f0e", "#9467bd"]
x = np.arange(len(labels))
bars = ax.bar(x, dists, color=colors, alpha=0.80, yerr=errs,
              capsize=4, error_kw={"elinewidth": 1.2})

ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=22, ha="right", fontsize=9)
ax.set_ylabel(r"$|\delta|^2 = (\mu_{\rm eff}^2 - \mu_{\rm W33}^2)^2$", fontsize=11)
ax.set_title(r"Fig 2: RG Distance to Nearest $W(3,3)$ Fixed Point — All SM Sectors",
             fontsize=10)
ax.set_yscale("log")
ax.set_ylim(1e-7, 1e-1)
ax.grid(axis="y", alpha=0.3)

# Annotate nearest fixed point
for xi, (s, d) in enumerate(zip(SECTORS, dists)):
    nearest = W33_LABELS[int(np.argmin((W33_FP - s[1])**2))]
    ax.text(xi, d * 3.5, nearest, ha="center", va="bottom", fontsize=7,
            color="black", rotation=0)

plt.tight_layout()
for ext in ("pdf", "png"):
    out = f"paper/figures/fig2_rg_distance.{ext}"
    plt.savefig(out, dpi=200)
    print(f"Saved {out}")
plt.close()
