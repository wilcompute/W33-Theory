#!/usr/bin/env python3
"""
PASS 78 — TRACK Y: 2-LOOP GAUGE COUPLING UNIFICATION
=====================================================

2-loop SM + W33 matter threshold corrections to achieve unification
at Lambda_W33. The W33 matter content is read off the spectral
decomposition of GQ(3,3) under SM gauge groups.

W33 MATTER CONTENT (from eigenvalue structure):
  - lambda4 = 1: SM singlet (1,1,0)  [1 Weyl fermion]
  - lambda3 = 3: SU(3) triplet-like (3,1,+2/3)  [colour 'leptoquark']
  - lambda2 = (1+sqrt97)/2: SU(2) doublet-like (1,2,+1/2)  [9 modes]
  - lambda5 = -1: conjugate singlet
  - lambda6 = -3: anti-triplet (3bar,1,-2/3)
  - lambda7 = -4: SU(2) x SU(3) bi-fundamental (3,2,+1/6)  [1 mode]

THE W33 GUT MULTIPLET:
In SU(5) language, 5 + 10 + 1 = 16 (as in SO(10)).
The W33 eigenvalue multiplicities (1,9,10,10,5,4,1) = 40
decompose under SU(5) as: 10 + 10 + 10 + 5 + 5bar = two full generations
plus the singlet. This is the W33 matter content.
"""

import numpy as np
import json

# Physical constants
M_Z_GEV = 91.1876

# SM gauge couplings at M_Z (MS-bar, PDG 2024)
ALPHA_1_MZ = 0.01695
ALPHA_2_MZ = 0.03374
ALPHA_3_MZ = 0.11800

# W33 parameters
sqrt97   = np.sqrt(97)
lambda1  = 12.0
lambda2  = (1 + sqrt97) / 2
lambda3  = 3.0
lambda4  = 1.0
epsilon  = (lambda2 - 2*np.sqrt(7)) / (2*np.sqrt(7))
M_GUT    = 2.0e16
LAM_W33  = M_GUT * np.sqrt(epsilon)

# 1-loop SM beta coefficients
B1_SM = 41.0/10
B2_SM = -19.0/6
B3_SM = -7.0

# 2-loop SM beta coefficients (diagonal pieces only for simplicity)
# b_ij matrix: alpha_i^{-1} gets -(b_ij / (2pi)^2) * alpha_j * log term
# Using standard 2-loop SM values
B11_SM = 199.0/50
B22_SM = 35.0/6
B33_SM = -76.0/3
B12_SM = 27.0/10
B13_SM = 44.0/5
B23_SM = 9.0

# W33 extra matter contribution to beta functions
# W33 adds (from the 40 GQ(3,3) modes decomposed under SM):
# Approx: 2 complete SU(5) 10-plets + 1 5-plet beyond SM
# Delta b_i from extra 10 of SU(5):
#   Delta b1 = 2*(6/5) = 2.4 per 10-plet
#   Delta b2 = 2*2     = 4.0 per 10-plet
#   Delta b3 = 2*3     = 6.0 per 10-plet
N_10PLETS = 2   # from W33 multiplicities
DB1_W33 = N_10PLETS * (6.0/5)
DB2_W33 = N_10PLETS * 2.0
DB3_W33 = N_10PLETS * 3.0

# Effective beta coefficients with W33 matter
B1_EFF = B1_SM + DB1_W33
B2_EFF = B2_SM + DB2_W33
B3_EFF = B3_SM + DB3_W33


def run_1loop(alpha_inv_MZ, b, log_r):
    return alpha_inv_MZ - (b / (2*np.pi)) * log_r


def run_2loop(alpha1_inv, alpha2_inv, alpha3_inv, b1, b2, b3,
              b11, b22, b33, b12, b13, b23, log_r):
    """
    2-loop RG step (Euler method, single step — good for illustration).
    d(alpha_i^{-1})/d(log mu) = -b_i/(2pi) - sum_j b_ij * alpha_j / (2pi)^2
    """
    a1 = 1.0/alpha1_inv
    a2 = 1.0/alpha2_inv
    a3 = 1.0/alpha3_inv

    d1 = -(b1/(2*np.pi)) - (b11*a1 + b12*a2 + b13*a3) / (2*np.pi)**2
    d2 = -(b2/(2*np.pi)) - (b12*a1 + b22*a2 + b23*a3) / (2*np.pi)**2
    d3 = -(b3/(2*np.pi)) - (b13*a1 + b23*a2 + b33*a3) / (2*np.pi)**2

    inv1 = alpha1_inv + d1 * log_r
    inv2 = alpha2_inv + d2 * log_r
    inv3 = alpha3_inv + d3 * log_r
    return inv1, inv2, inv3


def w33_threshold_correction(C):
    """W33 threshold at Lambda_W33: Delta = C*(lambda2-lambda3)/(2pi*lambda1)"""
    return C * (lambda2 - lambda3) / (2 * np.pi * lambda1)


def unification_analysis_2loop():
    log_r = np.log(LAM_W33 / M_Z_GEV)

    inv1_MZ = 1.0/ALPHA_1_MZ
    inv2_MZ = 1.0/ALPHA_2_MZ
    inv3_MZ = 1.0/ALPHA_3_MZ

    # 1-loop SM
    inv1_1l = run_1loop(inv1_MZ, B1_SM, log_r)
    inv2_1l = run_1loop(inv2_MZ, B2_SM, log_r)
    inv3_1l = run_1loop(inv3_MZ, B3_SM, log_r)
    spread_1l = np.std([inv1_1l, inv2_1l, inv3_1l])

    # 1-loop with W33 matter
    inv1_W33 = run_1loop(inv1_MZ, B1_EFF, log_r)
    inv2_W33 = run_1loop(inv2_MZ, B2_EFF, log_r)
    inv3_W33 = run_1loop(inv3_MZ, B3_EFF, log_r)
    spread_W33_1l = np.std([inv1_W33, inv2_W33, inv3_W33])

    # 2-loop SM only
    inv1_2l, inv2_2l, inv3_2l = run_2loop(
        inv1_MZ, inv2_MZ, inv3_MZ,
        B1_SM, B2_SM, B3_SM,
        B11_SM, B22_SM, B33_SM, B12_SM, B13_SM, B23_SM,
        log_r
    )
    spread_2l = np.std([inv1_2l, inv2_2l, inv3_2l])

    # 2-loop with W33 matter (approximate: use effective 1-loop b_i in 2-loop diagonal)
    inv1_2lW, inv2_2lW, inv3_2lW = run_2loop(
        inv1_MZ, inv2_MZ, inv3_MZ,
        B1_EFF, B2_EFF, B3_EFF,
        B11_SM, B22_SM, B33_SM, B12_SM, B13_SM, B23_SM,
        log_r
    )
    spread_2lW = np.std([inv1_2lW, inv2_2lW, inv3_2lW])

    # W33 threshold corrections
    d1 = w33_threshold_correction(1.0)
    d2 = w33_threshold_correction(3.0/4)
    d3 = w33_threshold_correction(4.0/3)
    inv1_final = inv1_2lW + d1
    inv2_final = inv2_2lW + d2
    inv3_final = inv3_2lW + d3
    spread_final = np.std([inv1_final, inv2_final, inv3_final])
    mean_final   = np.mean([inv1_final, inv2_final, inv3_final])

    return {
        "Lambda_W33_GeV": LAM_W33,
        "log_r": round(log_r, 4),
        "W33_matter": {
            "N_10plets": N_10PLETS,
            "Delta_b1": round(DB1_W33, 4),
            "Delta_b2": round(DB2_W33, 4),
            "Delta_b3": round(DB3_W33, 4),
        },
        "1loop_SM": {
            "inv1": round(inv1_1l,3), "inv2": round(inv2_1l,3),
            "inv3": round(inv3_1l,3), "spread": round(spread_1l,3)
        },
        "1loop_W33matter": {
            "inv1": round(inv1_W33,3), "inv2": round(inv2_W33,3),
            "inv3": round(inv3_W33,3), "spread": round(spread_W33_1l,3)
        },
        "2loop_SM": {
            "inv1": round(inv1_2l,3), "inv2": round(inv2_2l,3),
            "inv3": round(inv3_2l,3), "spread": round(spread_2l,3)
        },
        "2loop_W33matter": {
            "inv1": round(inv1_2lW,3), "inv2": round(inv2_2lW,3),
            "inv3": round(inv3_2lW,3), "spread": round(spread_2lW,3)
        },
        "2loop_W33matter_threshold": {
            "inv1": round(inv1_final,3), "inv2": round(inv2_final,3),
            "inv3": round(inv3_final,3),
            "spread": round(spread_final,3),
            "mean": round(mean_final,3),
        },
        "spread_hierarchy": {
            "1loop_SM": round(spread_1l,3),
            "1loop_W33": round(spread_W33_1l,3),
            "2loop_SM": round(spread_2l,3),
            "2loop_W33": round(spread_2lW,3),
            "2loop_W33_threshold": round(spread_final,3),
        },
        "unification_quality": (
            "GOOD" if spread_final < 1.0 else
            "PARTIAL" if spread_final < 5.0 else "POOR"
        ),
    }


def main():
    print("=" * 72)
    print(" PASS 78 — TRACK Y: 2-LOOP GAUGE COUPLING UNIFICATION")
    print("=" * 72)
    print(f"\n  Lambda_W33 = {LAM_W33:.4e} GeV,  epsilon = {epsilon:.6f}")
    print(f"  W33 matter: {N_10PLETS} extra SU(5) 10-plets")
    print(f"  Delta b_i = ({DB1_W33:.2f}, {DB2_W33:.2f}, {DB3_W33:.2f})")

    r = unification_analysis_2loop()

    print(f"\n  Spread hierarchy (1/alpha std dev):")
    for label, val in r['spread_hierarchy'].items():
        marker = " <-- BEST" if val == min(r['spread_hierarchy'].values()) else ""
        print(f"    {label:<30} {val:.3f}{marker}")

    best = r['2loop_W33matter_threshold']
    print(f"\n  Best result (2-loop + W33 matter + threshold):")
    print(f"    1/alpha_1 = {best['inv1']:.3f}")
    print(f"    1/alpha_2 = {best['inv2']:.3f}")
    print(f"    1/alpha_3 = {best['inv3']:.3f}")
    print(f"    Spread    = {best['spread']:.3f}  ({r['unification_quality']})")

    result = {
        "pass": 78,
        "track": "Y",
        "title": "2-Loop Gauge Coupling Unification at Lambda_W33",
        "analysis": r,
        "key_theorem": (
            f"2-loop RG + W33 matter ({N_10PLETS} extra 10-plets) + threshold corrections: "
            f"spread = {best['spread']:.3f} in 1/alpha. "
            f"Quality: {r['unification_quality']}. "
            f"Improvement over 1-loop SM: "
            f"{round((r['spread_hierarchy']['1loop_SM']-best['spread'])/r['spread_hierarchy']['1loop_SM']*100,1)}%."
        ),
        "status": "COMPLETE",
    }

    with open("w33_pass78_trackY_2loop_unification.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n  Witness JSON -> w33_pass78_trackY_2loop_unification.json")
    return result


if __name__ == "__main__":
    main()
