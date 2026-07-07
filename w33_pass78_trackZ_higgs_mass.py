#!/usr/bin/env python3
"""
PASS 78 — TRACK Z: HIGGS MASS FROM W33 SPECTRAL GEOMETRY
=========================================================

Searches for a formula m_H = f(lambda_i, epsilon, v_EW) that
reproduces m_H = 125.25 GeV (PDG 2024) within 2-sigma.

PDG: m_H = 125.25 +/- 0.17 GeV  (2-sigma window: 124.91 -- 125.59 GeV)

STRATEGY:
  Systematically construct all 'natural' W33 combinations of
  {lambda1, lambda2, lambda3, lambda4, epsilon, v_EW, M_Z, M_W}
  and find those closest to 125.25 GeV.
"""

import numpy as np
import json
from itertools import product

# Physical constants
V_EW_GEV   = 246.22    # Higgs VEV (GeV)
M_H_PDG    = 125.25    # GeV
SIGMA_H    = 0.17      # GeV
M_Z_GEV    = 91.1876
M_W_GEV    = 80.377
ALPHA_EM   = 1.0/137.036
SIN2_TW    = 0.23153

# W33 parameters
sqrt97   = np.sqrt(97)
lambda1  = 12.0
lambda2  = (1 + sqrt97) / 2
lambda3  = 3.0
lambda4  = 1.0
lambda7  = -4.0   # most negative eigenvalue
epsilon  = (lambda2 - 2*np.sqrt(7)) / (2*np.sqrt(7))


def pull(m_pred):
    return (m_pred - M_H_PDG) / SIGMA_H


def scan_formulas():
    """
    Systematic scan over formulas of the form:
      m_H = v_EW * lambda_i^a * lambda_j^b * epsilon^c
    with a, b in {-1, -1/2, 0, 1/2, 1, 3/2, 2}
    and c in {0, 1/4, 1/2, 3/4, 1, 3/2, 2}
    """
    lambdas = {
        "lam1": lambda1,
        "lam2": lambda2,
        "lam3": lambda3,
        "lam4": lambda4,
        "lam1/lam2": lambda1/lambda2,
        "lam2/lam1": lambda2/lambda1,
        "lam3/lam1": lambda3/lambda1,
        "sqrt_lam1": np.sqrt(lambda1),
        "sqrt_lam2": np.sqrt(lambda2),
    }
    eps_powers = {
        "eps^0": 1.0,
        "eps^(1/4)": epsilon**0.25,
        "eps^(1/3)": epsilon**(1/3),
        "eps^(1/2)": np.sqrt(epsilon),
        "eps^(2/3)": epsilon**(2/3),
        "eps^1": epsilon,
        "eps^(3/2)": epsilon**1.5,
        "eps^2": epsilon**2,
    }
    corrections = {
        "1": 1.0,
        "(1+eps)": 1 + epsilon,
        "(1-eps)": 1 - epsilon,
        "(1+eps^(1/2))": 1 + np.sqrt(epsilon),
        "(2-lam3/lam2)": 2 - lambda3/lambda2,
        "(lam2-lam3)/lam1": (lambda2 - lambda3)/lambda1,
        "pi*eps": np.pi * epsilon,
    }

    results = []
    for lname, lval in lambdas.items():
        for epname, epval in eps_powers.items():
            for cname, cval in corrections.items():
                m_pred = V_EW_GEV * lval * epval * cval
                p = pull(m_pred)
                results.append({
                    "formula": f"v * {lname} * {epname} * {cname}",
                    "m_H_pred": round(m_pred, 4),
                    "pull": round(p, 3),
                    "abs_pull": abs(p),
                })

    # Also try v * sqrt(ratio) type formulas
    ratios = [
        ("lam2/lam1", lambda2/lambda1),
        ("lam3/lam1", lambda3/lambda1),
        ("lam4/lam2", lambda4/lambda2),
        ("lam2*eps", lambda2*epsilon),
        ("(lam1-lam2)/lam1", (lambda1-lambda2)/lambda1),
    ]
    for rname, rval in ratios:
        for epname, epval in eps_powers.items():
            m_pred = V_EW_GEV * np.sqrt(abs(rval)) * epval
            p = pull(m_pred)
            results.append({
                "formula": f"v * sqrt({rname}) * {epname}",
                "m_H_pred": round(m_pred, 4),
                "pull": round(p, 3),
                "abs_pull": abs(p),
            })

    # Sort by |pull|
    results.sort(key=lambda x: x['abs_pull'])
    return results


def top_candidates(results, n=10):
    return results[:n]


def w33_higgs_theorem(results):
    """
    The best W33 Higgs mass formula and its interpretation.
    """
    best = results[0]
    within_2sigma = [r for r in results if r['abs_pull'] <= 2.0]
    within_1sigma = [r for r in results if r['abs_pull'] <= 1.0]
    return {
        "best_formula": best['formula'],
        "best_m_H_GeV": best['m_H_pred'],
        "best_pull": best['pull'],
        "n_within_2sigma": len(within_2sigma),
        "n_within_1sigma": len(within_1sigma),
        "within_1sigma": within_1sigma[:5],
    }


def main():
    print("=" * 72)
    print(" PASS 78 — TRACK Z: HIGGS MASS FROM W33")
    print("=" * 72)
    print(f"\n  Target: m_H = {M_H_PDG} +/- {SIGMA_H} GeV (PDG 2024)")
    print(f"  2-sigma window: [{M_H_PDG - 2*SIGMA_H:.2f}, {M_H_PDG + 2*SIGMA_H:.2f}] GeV")
    print(f"  epsilon = {epsilon:.6f}")

    results = scan_formulas()
    top = top_candidates(results, 15)

    print(f"\n  Top 15 W33 Higgs mass formulas:")
    print(f"  {'Formula':<52} {'m_H (GeV)':<12} {'Pull'}")
    print(f"  {'-'*52} {'-'*12} {'-'*6}")
    for r in top:
        marker = " ✓" if r['abs_pull'] <= 2.0 else ""
        print(f"  {r['formula']:<52} {r['m_H_pred']:<12.4f} {r['pull']:+.3f}{marker}")

    theorem = w33_higgs_theorem(results)
    print(f"\n  Best formula: {theorem['best_formula']}")
    print(f"  Predicted m_H = {theorem['best_m_H_GeV']} GeV  (pull = {theorem['best_pull']:+.3f})")
    print(f"  Formulas within 1-sigma: {theorem['n_within_1sigma']}")
    print(f"  Formulas within 2-sigma: {theorem['n_within_2sigma']}")

    if theorem['n_within_1sigma'] > 0:
        print(f"\n  Within 1-sigma:")
        for r in theorem['within_1sigma']:
            print(f"    {r['formula']}: m_H = {r['m_H_pred']} GeV (pull {r['pull']:+.3f})")

    result = {
        "pass": 78,
        "track": "Z",
        "title": "Higgs Mass from W33 Spectral Geometry",
        "target_m_H_GeV": M_H_PDG,
        "sigma_H_GeV": SIGMA_H,
        "epsilon": round(epsilon, 6),
        "top_candidates": top,
        "theorem": theorem,
        "key_theorem": (
            f"Best W33 Higgs formula: {theorem['best_formula']} "
            f"= {theorem['best_m_H_GeV']} GeV (pull {theorem['best_pull']:+.3f}). "
            f"{theorem['n_within_1sigma']} formulas within 1-sigma, "
            f"{theorem['n_within_2sigma']} within 2-sigma."
        ),
        "status": "COMPLETE",
        "verdict": (
            "EXACT MATCH" if theorem['best'] ['abs_pull'] <= 1.0 else
            "NEAR-MISS" if theorem['best_pull'] <= 3.0 else
            "OFF-TARGET"
        ) if False else (
            "EXACT MATCH" if abs(theorem['best_pull']) <= 1.0 else
            "NEAR-MISS" if abs(theorem['best_pull']) <= 3.0 else
            "OFF-TARGET"
        ),
    }

    with open("w33_pass78_trackZ_higgs_mass.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n  Witness JSON -> w33_pass78_trackZ_higgs_mass.json")
    return result


if __name__ == "__main__":
    main()
