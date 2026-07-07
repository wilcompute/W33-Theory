#!/usr/bin/env python3
"""
PASS 77 — TRACK X: SM GAUGE COUPLING UNIFICATION AT LAMBDA_W33
==============================================================

Checks whether g1, g2, g3 unify at Lambda_W33 = M_GUT * sqrt(epsilon)
under 1-loop RG running with W33 threshold corrections.

THRESHOLD CORRECTION FORMULA:
  alpha_i^{-1}(Lambda_W33) += Delta_i
  Delta_i = C_i * (lambda2 - lambda3) / (2 pi * lambda1)
where C_i is the quadratic Casimir of the i-th gauge group
in the W33 representation.
"""

import numpy as np
import json

# Physical constants
M_Z_GEV = 91.1876

# SM gauge couplings at M_Z (MS-bar scheme, PDG 2024)
ALPHA_1_MZ = 0.01695   # U(1)_Y  (= (5/3) * alpha_em / cos^2 theta_W)
ALPHA_2_MZ = 0.03374   # SU(2)_L
ALPHA_3_MZ = 0.11800   # SU(3)_c

# 1-loop SM beta function coefficients b_i (without SUSY)
# b_i: alpha_i^{-1}(mu) = alpha_i^{-1}(M_Z) - (b_i / 2pi) * ln(mu/M_Z)
B1_SM =  41.0/10    # U(1)_Y
B2_SM = -19.0/6     # SU(2)_L
B3_SM =  -7.0       # SU(3)_c

# W33 parameters
sqrt97    = np.sqrt(97)
lambda1   = 12.0
lambda2   = (1 + sqrt97) / 2
lambda3   = 3.0
lambda4   = 1.0
epsilon   = (lambda2 - 2*np.sqrt(7)) / (2*np.sqrt(7))
M_GUT_GEV = 2.0e16
LAMBDA_W33 = M_GUT_GEV * np.sqrt(epsilon)

# Quadratic Casimirs (fundamental representations)
C1 = 3.0/5   # U(1)_Y (GUT normalization)
C2 = 4.0/3   # SU(2)_L: C2(fund) = 1/2, but using adjoint = 2
C3 = 4.0/3   # SU(3)_c: C2(fund) = 4/3
# Revised: use standard Casimirs for threshold corrections
C1_thresh = 1.0    # singlet U(1)
C2_thresh = 3.0/4  # SU(2) fundamental: C(T) = 1/2, C(adj) = 2
C3_thresh = 4.0/3  # SU(3) fundamental


def run_coupling(alpha_inv_MZ, b_coeff, log_ratio):
    """1-loop RG running: alpha^{-1}(mu) = alpha^{-1}(M_Z) - (b/2pi)*log(mu/M_Z)"""
    return alpha_inv_MZ - (b_coeff / (2 * np.pi)) * log_ratio


def w33_threshold_correction(C_casimir):
    """
    W33 threshold correction at Lambda_W33:
    Delta = C * (lambda2 - lambda3) / (2 pi * lambda1)
           = C * (5.4244 - 3) / (2 pi * 12)
           = C * 2.4244 / 75.398
           = C * 0.03215
    """
    return C_casimir * (lambda2 - lambda3) / (2 * np.pi * lambda1)


def unification_analysis():
    log_ratio = np.log(LAMBDA_W33 / M_Z_GEV)

    # 1/alpha at M_Z
    inv1_MZ = 1.0 / ALPHA_1_MZ
    inv2_MZ = 1.0 / ALPHA_2_MZ
    inv3_MZ = 1.0 / ALPHA_3_MZ

    # Run to Lambda_W33 (SM only, no SUSY)
    inv1_run = run_coupling(inv1_MZ, B1_SM, log_ratio)
    inv2_run = run_coupling(inv2_MZ, B2_SM, log_ratio)
    inv3_run = run_coupling(inv3_MZ, B3_SM, log_ratio)

    # W33 threshold corrections
    delta1 = w33_threshold_correction(C1_thresh)
    delta2 = w33_threshold_correction(C2_thresh)
    delta3 = w33_threshold_correction(C3_thresh)

    inv1_corr = inv1_run + delta1
    inv2_corr = inv2_run + delta2
    inv3_corr = inv3_run + delta3

    # Unification measure: spread of 1/alpha values (ideally all equal)
    spread_run  = np.std([inv1_run, inv2_run, inv3_run])
    spread_corr = np.std([inv1_corr, inv2_corr, inv3_corr])
    mean_corr   = np.mean([inv1_corr, inv2_corr, inv3_corr])

    # Also run with SUSY-like beta coefficients for comparison
    # SUSY beta: b1=33/5, b2=1, b3=-3
    inv1_susy = run_coupling(inv1_MZ, 33.0/5, log_ratio)
    inv2_susy = run_coupling(inv2_MZ, 1.0, log_ratio)
    inv3_susy = run_coupling(inv3_MZ, -3.0, log_ratio)
    spread_susy = np.std([inv1_susy, inv2_susy, inv3_susy])

    # Unification scale for each pair (SM)
    def unification_scale(inv_a_MZ, b_a, inv_b_MZ, b_b):
        # inv_a(mu) = inv_b(mu) => solve for log(mu/M_Z)
        delta_inv = inv_a_MZ - inv_b_MZ
        delta_b   = (b_a - b_b) / (2 * np.pi)
        if abs(delta_b) < 1e-12:
            return None
        log_mu = delta_inv / delta_b
        return M_Z_GEV * np.exp(log_mu)

    mu_12 = unification_scale(inv1_MZ, B1_SM, inv2_MZ, B2_SM)
    mu_13 = unification_scale(inv1_MZ, B1_SM, inv3_MZ, B3_SM)
    mu_23 = unification_scale(inv2_MZ, B2_SM, inv3_MZ, B3_SM)

    return {
        "Lambda_W33_GeV": LAMBDA_W33,
        "log_Lambda_over_MZ": round(log_ratio, 4),
        "1_over_alpha_at_MZ": {
            "U1": round(inv1_MZ, 3),
            "SU2": round(inv2_MZ, 3),
            "SU3": round(inv3_MZ, 3),
        },
        "1_over_alpha_SM_run": {
            "U1": round(inv1_run, 3),
            "SU2": round(inv2_run, 3),
            "SU3": round(inv3_run, 3),
        },
        "W33_threshold_corrections": {
            "Delta_U1": round(delta1, 5),
            "Delta_SU2": round(delta2, 5),
            "Delta_SU3": round(delta3, 5),
        },
        "1_over_alpha_corrected": {
            "U1": round(inv1_corr, 3),
            "SU2": round(inv2_corr, 3),
            "SU3": round(inv3_corr, 3),
        },
        "spread_SM_only": round(spread_run, 3),
        "spread_W33_corrected": round(spread_corr, 3),
        "spread_SUSY": round(spread_susy, 3),
        "mean_unified_alpha_inv": round(mean_corr, 3),
        "spread_improvement": round((spread_run - spread_corr) / spread_run * 100, 1),
        "SM_pairwise_unification_scales_GeV": {
            "mu_12": round(mu_12, 3) if mu_12 else None,
            "mu_13": round(mu_13, 3) if mu_13 else None,
            "mu_23": round(mu_23, 3) if mu_23 else None,
        },
    }


def main():
    print("=" * 72)
    print(" PASS 77 — TRACK X: GAUGE COUPLING UNIFICATION")
    print("=" * 72)

    r = unification_analysis()
    print(f"\n  Lambda_W33 = {r['Lambda_W33_GeV']:.4e} GeV")
    print(f"  log(Lambda/M_Z) = {r['log_Lambda_over_MZ']}")

    print(f"\n  1/alpha at M_Z:       U1={r['1_over_alpha_at_MZ']['U1']:.2f}  "
          f"SU2={r['1_over_alpha_at_MZ']['SU2']:.2f}  SU3={r['1_over_alpha_at_MZ']['SU3']:.2f}")
    print(f"  1/alpha SM run:       U1={r['1_over_alpha_SM_run']['U1']:.2f}  "
          f"SU2={r['1_over_alpha_SM_run']['SU2']:.2f}  SU3={r['1_over_alpha_SM_run']['SU3']:.2f}")
    print(f"  W33 corrections:      Delta_U1={r['W33_threshold_corrections']['Delta_U1']:.5f}  "
          f"Delta_SU2={r['W33_threshold_corrections']['Delta_SU2']:.5f}  "
          f"Delta_SU3={r['W33_threshold_corrections']['Delta_SU3']:.5f}")
    print(f"  1/alpha corrected:    U1={r['1_over_alpha_corrected']['U1']:.2f}  "
          f"SU2={r['1_over_alpha_corrected']['SU2']:.2f}  SU3={r['1_over_alpha_corrected']['SU3']:.2f}")

    print(f"\n  Spread (SM only):       {r['spread_SM_only']:.3f}")
    print(f"  Spread (W33 corrected): {r['spread_W33_corrected']:.3f}")
    print(f"  Spread (SUSY):          {r['spread_SUSY']:.3f}")
    print(f"  Improvement from W33 threshold: {r['spread_improvement']}%")

    print(f"\n  SM pairwise unification scales:")
    for pair, mu in r['SM_pairwise_unification_scales_GeV'].items():
        print(f"    mu_{pair[-2:]} = {mu:.3e} GeV")

    # Verdict
    if r['spread_W33_corrected'] < 1.0:
        verdict = "NEAR-UNIFICATION: W33 threshold corrections bring spread < 1"
    elif r['spread_W33_corrected'] < r['spread_SM_only']:
        verdict = f"IMPROVEMENT: spread reduced from {r['spread_SM_only']:.2f} to {r['spread_W33_corrected']:.2f}"
    else:
        verdict = "NON-UNIFICATION at Lambda_W33 (SM running alone)"

    print(f"\n  Verdict: {verdict}")
    print(f"  Note: SUSY running gives spread = {r['spread_SUSY']:.2f} "
          f"({'better' if r['spread_SUSY'] < r['spread_W33_corrected'] else 'worse'} than W33 threshold).")

    result = {
        "pass": 77,
        "track": "X",
        "title": "SM Gauge Coupling Unification at Lambda_W33",
        "unification_analysis": r,
        "verdict": verdict,
        "key_theorem": (
            f"At Lambda_W33 = {r['Lambda_W33_GeV']:.3e} GeV: "
            f"1/alpha = ({r['1_over_alpha_corrected']['U1']:.1f}, "
            f"{r['1_over_alpha_corrected']['SU2']:.1f}, "
            f"{r['1_over_alpha_corrected']['SU3']:.1f}) after W33 threshold. "
            f"Spread = {r['spread_W33_corrected']:.2f} ({r['spread_improvement']}% improvement over SM). "
            f"Full unification requires additional contributions (2-loop or new W33 modes)."
        ),
        "status": "COMPLETE",
        "open_question": (
            "Complete unification at Lambda_W33 requires either: "
            "(a) 2-loop RG corrections, (b) additional W33 multiplet content, "
            "or (c) a different Lambda_W33 definition. Track X documents the "
            "1-loop result and identifies the required additional correction."
        ),
    }

    with open("w33_pass77_trackX_gauge_unification.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n  Witness JSON -> w33_pass77_trackX_gauge_unification.json")
    return result


if __name__ == "__main__":
    main()
