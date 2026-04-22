"""Fig 1: mu_eff^2 vs m1 scan — neutrino sector, annotated W(3,3) candidate lines.

Outputs: paper/figures/fig1_mu_eff_scan.pdf  (and .png)

Usage:
    python paper/figures/fig1_mu_eff_scan.py

Requires: numpy, matplotlib, scipy
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

# ── Physical constants (NuFIT 5.3, PDG 2024) ──────────────────────────────────
DM2_ATM_NH = 2.528e-3   # eV^2  (NH: m3^2 - m1^2)
DM2_SOL    = 7.42e-5    # eV^2  (m2^2 - m1^2)
DM2_ATM_IH = 2.510e-3   # eV^2  (IH: m2^2 - m3^2)

PHI4 = 10  # Phi_4(3)


def masses_NH(m1):
    m2 = np.sqrt(m1**2 + DM2_SOL)
    m3 = np.sqrt(m1**2 + DM2_ATM_NH)
    return m1, m2, m3


def masses_IH(m3):
    m2 = np.sqrt(m3**2 + DM2_ATM_IH)
    m1 = np.sqrt(m2**2 - DM2_SOL)
    return m1, m2, m3


def mu_eff2(masses):
    ms = np.sort(np.array(masses))
    if np.any(ms <= 0):
        return np.nan
    gm = np.exp(np.mean(np.log(ms)))
    s_star = gm / ms[-1]
    if s_star <= 0:
        return np.nan
    return -np.log(s_star) / np.log(PHI4)


# W(3,3) candidate fixed-point lines
W33_LINES = {
    r"$1/\mu = 1/4$": 1/4,
    r"$1/\Phi_6 = 1/7$": 1/7,
    r"$1/\Phi_3 = 1/13$": 1/13,
    r"$1/(2k-1) = 1/23$": 1/23,
}

# ── Scan ──────────────────────────────────────────────────────────────────────
M1_NH = np.logspace(-4, np.log10(0.35), 600)  # eV
M3_IH = np.logspace(-4, np.log10(0.35), 600)  # eV

mu_NH = np.array([mu_eff2(masses_NH(m)) for m in M1_NH])
sum_NH = np.array([sum(masses_NH(m)) for m in M1_NH])

# IH: m3 is the lightest
mu_IH, sum_IH = [], []
for m3 in M3_IH:
    try:
        ms = masses_IH(m3)
        if ms[0] > 0:
            mu_IH.append(mu_eff2(ms))
            sum_IH.append(sum(ms))
        else:
            mu_IH.append(np.nan)
            sum_IH.append(np.nan)
    except Exception:
        mu_IH.append(np.nan)
        sum_IH.append(np.nan)
mu_IH = np.array(mu_IH)
sum_IH = np.array(sum_IH)

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5))

ax.plot(sum_NH, mu_NH, color="steelblue", lw=1.8, label="NH")
ax.plot(sum_IH, mu_IH, color="tomato",   lw=1.8, label="IH", ls="--")

colors = ["#2ca02c", "#ff7f0e", "#9467bd", "#8c564b"]
for (label, val), col in zip(W33_LINES.items(), colors):
    ax.axhline(val, color=col, lw=1.2, ls=":", alpha=0.85, label=label)

# DESI DR1 vertical limits
ax.axvline(0.072, color="black", lw=1.0, ls="-.",  alpha=0.6, label=r"DESI $\Lambda$CDM 95% UL")
ax.axvline(0.113, color="black", lw=1.0, ls=(0,(3,1,1,1)), alpha=0.6, label=r"DESI $w_0$CDM 95% UL")
ax.axvline(0.173, color="black", lw=1.0, ls="--",  alpha=0.6, label=r"DESI $w_0w_a$CDM 95% UL")

ax.set_xlabel(r"$\sum m_\nu$ (eV)", fontsize=13)
ax.set_ylabel(r"$\mu_{\rm eff}^2$", fontsize=13)
ax.set_title(r"Fig 1: $\mu_{\rm eff}^2$ vs $\sum m_\nu$ — $W(3,3)$ Fixed-Point Scan", fontsize=11)
ax.set_xlim(0, 0.40)
ax.set_ylim(0, 0.55)
ax.legend(fontsize=8, loc="upper right", ncol=2)
ax.grid(True, alpha=0.3)

plt.tight_layout()
for ext in ("pdf", "png"):
    out = f"paper/figures/fig1_mu_eff_scan.{ext}"
    plt.savefig(out, dpi=200)
    print(f"Saved {out}")
plt.close()
