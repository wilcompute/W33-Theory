"""SOLVE_RG_NEUTRINO.py

Solves for the lightest neutrino mass m1 (NH) or m3 (IH) at each W(3,3)
spectral fixed point, using NuFIT 5.3 oscillation parameters.

Outputs:
  artifacts/rg_neutrino_results.json  -- full precision numerical results

Usage:
    python scripts/SOLVE_RG_NEUTRINO.py

References:
  - NuFIT 5.3: https://www.nu-fit.org
  - PDG 2024: https://pdg.lbl.gov
  - W(3,3) spectral parameters: paper/EXTENSIONS.md
"""
import json
import pathlib
import numpy as np
from scipy.optimize import brentq

# ── Oscillation parameters (NuFIT 5.3 best-fit) ──────────────────────────────
DM2_SOL    = 7.42e-5    # eV²  Δm²_21
DM2_ATM_NH = 2.528e-3   # eV²  Δm²_31 (NH)
DM2_ATM_IH = 2.510e-3   # eV²  |Δm²_32| (IH)

# ── W(3,3) spectral parameters ───────────────────────────────────────────────
k, g, f, v = 12, 15, 24, 40
q = 3
PHI3, PHI4, PHI6 = 13, 10, 7
MU = q + 1  # 4
TWO_K_MINUS_1 = 23

# ── W(3,3) fixed-point targets ───────────────────────────────────────────────
W33_TARGETS = {
    "1/mu":     1 / MU,
    "1/Phi6":   1 / PHI6,
    "1/Phi3":   1 / PHI3,
    "1/(2k-1)": 1 / TWO_K_MINUS_1,
    "1/6":      1 / 6,
}


def masses_NH(m1: float) -> tuple:
    """Return (m1, m2, m3) for normal hierarchy given m1 in eV."""
    return (
        m1,
        np.sqrt(m1**2 + DM2_SOL),
        np.sqrt(m1**2 + DM2_ATM_NH),
    )


def masses_IH(m3: float) -> tuple:
    """Return (m1, m2, m3) for inverted hierarchy given m3 (lightest) in eV."""
    m2 = np.sqrt(m3**2 + DM2_ATM_IH)
    m1 = np.sqrt(m2**2 - DM2_SOL)
    return m1, m2, m3


def mu_eff2(masses: tuple) -> float:
    """Compute mu_eff^2 = -log(s*) / log(Phi4).

    s* = geom_mean / max.
    Returns inf for degenerate/zero masses.
    """
    ms = np.sort(np.array(masses))
    if np.any(ms <= 0):
        return np.inf
    gm = np.exp(np.mean(np.log(ms)))
    s_star = gm / ms[-1]
    if s_star <= 0:
        return np.inf
    return -np.log(s_star) / np.log(PHI4)


def solve_NH(target: float, m1_lo: float = 1e-6, m1_hi: float = 0.5):
    """Find m1 such that mu_eff2(NH(m1)) == target."""
    try:
        m1 = brentq(
            lambda m: mu_eff2(masses_NH(m)) - target,
            m1_lo, m1_hi, xtol=1e-14, maxiter=500,
        )
        ms = masses_NH(m1)
        return {
            "m1_eV":   float(m1),
            "m1_meV":  float(m1 * 1e3),
            "m2_eV":   float(ms[1]),
            "m3_eV":   float(ms[2]),
            "sum_eV":  float(sum(ms)),
            "sum_meV": float(sum(ms) * 1e3),
            "mu_eff2": float(mu_eff2(ms)),
        }
    except ValueError:
        return None


def solve_IH(target: float, m3_lo: float = 1e-6, m3_hi: float = 0.4):
    """Find m3 (lightest) such that mu_eff2(IH(m3)) == target."""
    try:
        m3 = brentq(
            lambda m: mu_eff2(masses_IH(m)) - target,
            m3_lo, m3_hi, xtol=1e-14, maxiter=500,
        )
        ms = masses_IH(m3)
        return {
            "m3_eV":   float(m3),
            "m3_meV":  float(m3 * 1e3),
            "m1_eV":   float(ms[0]),
            "m2_eV":   float(ms[1]),
            "sum_eV":  float(sum(ms)),
            "sum_meV": float(sum(ms) * 1e3),
            "mu_eff2": float(mu_eff2(ms)),
        }
    except ValueError:
        return None


def main() -> None:
    results = {}
    print(f"{'Label':12s}  {'Target':10s}  {'NH Σ (meV)':12s}  {'IH Σ (meV)':12s}")
    print("-" * 52)
    for label, target in W33_TARGETS.items():
        entry = {"target": target, "label": label}
        nh = solve_NH(target)
        ih = solve_IH(target)
        if nh:
            entry["NH"] = nh
        if ih:
            entry["IH"] = ih
        results[label] = entry
        nh_sum = f"{nh['sum_meV']:.4f}" if nh else "no solution"
        ih_sum = f"{ih['sum_meV']:.4f}" if ih else "no solution"
        print(f"{label:12s}  {target:.6f}  {nh_sum:12s}  {ih_sum:12s}")

    out_path = pathlib.Path("artifacts") / "rg_neutrino_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
