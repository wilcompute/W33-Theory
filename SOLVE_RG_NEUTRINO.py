"""
SOLVE_RG_NEUTRINO.py
====================
W(3,3) RG perturbation theory around the equal-eigenvalue fixed point,
plus the mu_eff^2 precision probe using quasi-degenerate neutrino masses.

Executes Parts (a) and (b) from the analysis:
  (a) Perturbative RG running away from the W(3,3) fixed point
  (b) mu2 ln(Phi4) hierarchy scan in the QD neutrino sector

All W(3,3) invariants from the parameter ring:
  k=12, g=15, f=24, v=40, Phi3=13, Phi4=10, Phi6=7, mu=4, two_k_minus1=23
"""

import numpy as np
from fractions import Fraction
import json

# ─────────────────────────────────────────────────────────────────────────────
# W(3,3) parameter ring
# ─────────────────────────────────────────────────────────────────────────────
W33 = dict(k=12, g=15, f=24, v=40, Phi3=13, Phi4=10, Phi6=7, mu=4,
           two_k1=23, q=3)

# W(3,3)-distinguished rational candidates for mu_eff^2
# drawn from the spectral invariants
MU2_CANDIDATES = {
    "1/mu":     Fraction(1, W33["mu"]),        # 1/4
    "1/Phi6":   Fraction(1, W33["Phi6"]),      # 1/7
    "1/Phi3":   Fraction(1, W33["Phi3"]),      # 1/13
    "1/two_k1": Fraction(1, W33["two_k1"]),    # 1/23
    "1/Phi4":   Fraction(1, W33["Phi4"]),      # 1/10
    "2/Phi4":   Fraction(2, W33["Phi4"]),      # 1/5
    "1/k":      Fraction(1, W33["k"]),         # 1/12
    "mu/Phi4":  Fraction(W33["mu"], W33["Phi4"]), # 2/5
}

# ─────────────────────────────────────────────────────────────────────────────
# PART (a): RG perturbation theory around the W(3,3) equal-eigenvalue FP
# ─────────────────────────────────────────────────────────────────────────────

SECTOR_DATA = {
    # Sector: (masses_eV)  — PDG 2024 central values
    "up_quarks":       [2.16e6, 1.27e9, 172.69e9],  # eV: u, c, t
    "down_quarks":     [4.67e6, 93e6,   4.18e9],     # eV: d, s, b
    "charged_leptons": [511e3,  105.66e6, 1776.86e6], # eV: e, mu, tau
    "neutrinos_NO_1meV": [1e-3,   np.sqrt(7.42e-5)*1e9, np.sqrt(2.51e-3)*1e9],  # rough
    "neutrinos_NO_50meV": [50e-3, np.sqrt((50e-3)**2 + 7.42e-5*1e18), np.sqrt((50e-3)**2 + 2.51e-3*1e18)],
    "neutrinos_NO_100meV": [100e-3, np.sqrt((100e-3)**2 + 7.42e-5*1e18), np.sqrt((100e-3)**2 + 2.51e-3*1e18)],
}

def rg_analysis(masses_eV, label):
    """Compute W(3,3) RG deviation metrics for a sector."""
    m = np.array(masses_eV, dtype=float)
    # Normalize to max=1
    m_norm = m / m.max()
    # Geometric mean of normalized values
    s_star = np.prod(m_norm) ** (1.0 / len(m_norm))
    # log deviations from geometric mean
    delta = np.log(m_norm) - np.log(s_star)
    delta2_mean = np.mean(delta**2)
    # Ratio R = sum(sigma^4)/sum(sigma^2)
    R = np.sum(m_norm**4) / np.sum(m_norm**2)
    ln_R = np.log(R)
    # RG distance in units of 1/(16pi^2)
    rg_efolds = delta2_mean / (1.0 / (16 * np.pi**2))
    # mu_eff^2 from s_star
    Phi4 = W33["Phi4"]
    mu2_eff = -np.log(s_star) / np.log(Phi4)
    # Perturbative accuracy: |R - s_star^2| / s_star^2
    R_fp = s_star**2  # leading-order FP prediction
    perturbative_error = abs(R - R_fp) / R_fp if R_fp > 0 else float('inf')
    return {
        "label": label,
        "s_star": s_star,
        "delta2_mean": delta2_mean,
        "R": R,
        "ln_R": ln_R,
        "rg_efolds_scaled": rg_efolds,
        "mu2_eff": mu2_eff,
        "perturbative_error_pct": perturbative_error * 100,
        "perturbative": delta2_mean < 0.1,
    }

print("=" * 70)
print("PART (a): W(3,3) RG Fixed-Point Analysis — All SM Fermion Sectors")
print("=" * 70)
results_a = {}
for sector, masses in SECTOR_DATA.items():
    r = rg_analysis(masses, sector)
    results_a[sector] = r
    mark = "✓ PERTURBATIVE" if r["perturbative"] else "✗ NON-PERTURBATIVE"
    print(f"{sector:30s}  |delta|^2={r['delta2_mean']:8.3f}  "
          f"RG-efolds={r['rg_efolds_scaled']:8.1f}  "
          f"mu2_eff={r['mu2_eff']:6.4f}  {mark}")

# ─────────────────────────────────────────────────────────────────────────────
# PART (b): mu_eff^2 matching to W(3,3)-distinguished rationals in QD regime
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("PART (b): mu_eff^2 matching to W(3,3) invariants — Neutrino sector")
print("=" * 70)

# Scan m1 from 1 meV to 200 meV (cosmological QD window)
m1_scan = np.logspace(-4, -1, 500)  # eV

# NuFIT 5.3 oscillation parameters (3-sigma central, NO)
dm21_sq = 7.42e-5 * 1e-18  # eV^2 (converted from eV^2 — already eV^2, no need)
# Wait — masses are in eV, so:
dm21_sq_eV2 = 7.42e-5   # actually these are in eV^2? No — they are in eV^2 (with eV as mass unit)
# PDG: delta_m21^2 = 7.42e-5 eV^2, delta_m31^2 = 2.510e-3 eV^2
dm21 = 7.42e-5   # eV^2
dm31 = 2.510e-3  # eV^2  (NO)

best_matches = []  # (m1, mu2_eff, best_candidate, residual)

for m1 in m1_scan:
    m2 = np.sqrt(m1**2 + dm21)
    m3 = np.sqrt(m1**2 + dm31)
    masses = [m1, m2, m3]
    r = rg_analysis(masses, f"nu_m1={m1*1e3:.2f}meV")
    mu2 = r["mu2_eff"]
    # Find nearest W(3,3) candidate
    best_name, best_frac, best_res = None, None, float('inf')
    for name, frac in MU2_CANDIDATES.items():
        res = abs(mu2 - float(frac))
        if res < best_res:
            best_res = res
            best_name = name
            best_frac = frac
    best_matches.append({
        "m1_meV": m1 * 1e3,
        "m_sum_eV": sum(masses),
        "mu2_eff": mu2,
        "s_star": r["s_star"],
        "delta2": r["delta2_mean"],
        "perturbative": r["perturbative"],
        "best_candidate": best_name,
        "best_value": float(best_frac),
        "residual": best_res,
        "residual_pct": best_res / float(best_frac) * 100 if best_frac != 0 else float('inf'),
    })

# Find where mu2_eff crosses each W(3,3) candidate
print("\nm1 values where mu_eff^2 matches a W(3,3) invariant (residual < 5%):")
print(f"{'Candidate':12s}  {'Value':6s}  {'m1 (meV)':12s}  {'Sum m (eV)':12s}  {'residual%':10s}  {'Perturb?':8s}")
for cname, cfrac in MU2_CANDIDATES.items():
    cval = float(cfrac)
    matches_for_c = [b for b in best_matches
                     if b["best_candidate"] == cname and b["residual_pct"] < 5.0]
    if matches_for_c:
        # find exact crossing (where residual is smallest)
        best = min(matches_for_c, key=lambda x: x["residual"])
        perturb = "YES" if best["perturbative"] else "NO"
        print(f"{cname:12s}  {cval:6.4f}  "
              f"{best['m1_meV']:12.3f}  "
              f"{best['m_sum_eV']:12.4f}  "
              f"{best['residual_pct']:10.3f}  {perturb:8s}")

# Special focus: 1/mu = 1/4 crossing (the top posterior candidate)
print("\n--- Precision crossing: mu_eff^2 = 1/mu = 1/4 ---")
crossings_14 = sorted(
    [b for b in best_matches if abs(b["mu2_eff"] - 0.25) < 0.005],
    key=lambda x: abs(x["mu2_eff"] - 0.25)
)
if crossings_14:
    bst = crossings_14[0]
    print(f"  m1 = {bst['m1_meV']:.3f} meV")
    print(f"  Sum m_nu = {bst['m_sum_eV']*1e3:.2f} meV = {bst['m_sum_eV']:.4f} eV")
    print(f"  mu_eff^2 = {bst['mu2_eff']:.6f} (target 0.2500)")
    print(f"  s* = {bst['s_star']:.6f}")
    print(f"  Phi4^{-mu2} = {W33['Phi4']**(-bst['mu2_eff']):.6f} (= s* by construction)")
    print(f"  Perturbative regime: {bst['perturbative']}")
else:
    print("  No crossing found in scan range.")

# ─────────────────────────────────────────────────────────────────────────────
# KATRIN / Cosmological upper bound constraint on mu2_eff
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("KATRIN / Cosmological bound on mu_eff^2")
print("=" * 70)

bounds = {
    "KATRIN kinematic": 0.8,         # sum < 2.4 eV
    "Planck LCDM":      0.12 / 3,    # sum < 0.12 eV -> rough avg
    "DESI w0CDM":       0.113,
    "DESI w0waCDM":     0.173,
    "DESI LCDM":        0.072,
}

print(f"{'Experiment':20s}  {'Sum UL (eV)':12s}  {'mu2_eff UL':12s}  {'Best W33 candidate':20s}")
for exp, sum_ul in [
    ("KATRIN kinematic", 2.4),
    ("Planck LCDM", 0.12),
    ("DESI LCDM", 0.072),
    ("DESI w0CDM", 0.113),
    ("DESI w0waCDM", 0.173),
]:
    # Convert sum upper limit to m1 upper limit (NO)
    # sum ~ m1 + sqrt(m1^2+dm21) + sqrt(m1^2+dm31) → solve for m1
    # use bisection
    def nu_sum(m1):
        return m1 + np.sqrt(m1**2 + dm21) + np.sqrt(m1**2 + dm31)
    # bisect
    lo, hi = 1e-6, 0.5
    for _ in range(60):
        mid = (lo + hi) / 2
        if nu_sum(mid) < sum_ul:
            lo = mid
        else:
            hi = mid
    m1_ul = (lo + hi) / 2
    r_ul = rg_analysis([m1_ul, np.sqrt(m1_ul**2+dm21), np.sqrt(m1_ul**2+dm31)], exp)
    mu2_ul = r_ul["mu2_eff"]
    # nearest W(3,3) invariant below this value
    candidates_below = {n: float(f) for n, f in MU2_CANDIDATES.items() if float(f) <= mu2_ul}
    nearest = max(candidates_below, key=candidates_below.get) if candidates_below else "none"
    print(f"{exp:20s}  {sum_ul:12.3f}  {mu2_ul:12.6f}  {nearest:20s}")

# ─────────────────────────────────────────────────────────────────────────────
# Save full scan to JSON for downstream analysis
# ─────────────────────────────────────────────────────────────────────────────
results = {
    "W33_params": W33,
    "mu2_candidates": {k: str(v) for k, v in MU2_CANDIDATES.items()},
    "sector_rg_analysis": results_a,
    "neutrino_scan_summary": {
        "n_points": len(best_matches),
        "m1_range_meV": [best_matches[0]["m1_meV"], best_matches[-1]["m1_meV"]],
        "perturbative_window_start_meV": next(
            (b["m1_meV"] for b in best_matches if b["perturbative"]), None
        ),
        "best_crossing_1over4": crossings_14[0] if crossings_14 else None,
    }
}
with open("rg_neutrino_results.json", "w") as fh:
    json.dump(results, fh, indent=2, default=str)
print("\nResults saved to rg_neutrino_results.json")
print("\nDone.")
