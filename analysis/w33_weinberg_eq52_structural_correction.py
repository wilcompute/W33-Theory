#!/usr/bin/env python3
"""Eq. 52 Weinberg angle: structural derivation and Z-pole correction.

This file separates three statements that were previously blurred:

1. Q-matrix / GUT normalization:
   Q[2,2] = 5/3, hence sin^2(theta_W)_GUT = 3/8.

2. W33 finite-geometric tree generator:
   x0 = q / Phi_3 = 3 / 13.

3. Z-pole effective correction:
   x_eff(MZ) = x0 + alpha_hat(MZ)/(k-1), where k-1=11 is the
   nonbacktracking outdegree in W33/Ihara transport.

Numerically, with alpha_hat(MZ)^(-1)=127.930 and PDG live average
sin^2(theta_eff^lept)=0.23148, this gives agreement at the 1e-7 level:

    3/13 + 1/(11*127.930) = 0.23147985...

The point is not to claim Eq. 52 is proved by numerical coincidence.  Eq. 52 is
best read as the uncorrected finite-geometric generator; the observed effective
angle includes the natural nonbacktracking one-loop scale.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def second_eigenmatrix_q():
    P = np.array([[1, 12, 27], [1, 2, -3], [1, -4, 3]], dtype=float)
    Q = 40 * np.linalg.inv(P)
    return P, Q


def main() -> int:
    q = 3
    phi3 = q*q + q + 1
    k = 12
    nb = k - 1

    # Current external constants used only for the numerical Z-pole comparison.
    pdg_sin2_eff = 0.23148
    pdg_sin2_eff_unc = 0.00012
    alpha_inv_mz = 127.930
    alpha_inv_mz_unc = 0.008

    x0 = Fraction(q, phi3)
    alpha_mz = 1.0 / alpha_inv_mz
    correction = alpha_mz / nb
    x_eff = float(x0) + correction
    residual = x_eff - pdg_sin2_eff
    zscore = residual / pdg_sin2_eff_unc

    P, Q = second_eigenmatrix_q()
    kappa_y = Q[2, 2]
    sin2_gut = 1 / (1 + kappa_y)

    checks = {
        "phi3_projective_denominator": phi3 == 13,
        "tree_generator_exact": x0 == Fraction(3, 13),
        "nonbacktracking_degree": nb == 11,
        "q_matrix_hypercharge_normalization": abs(kappa_y - 5/3) < 1e-12,
        "gut_weinberg_angle": abs(sin2_gut - 3/8) < 1e-12,
        "z_pole_correction_matches_pdg_live": abs(residual) < pdg_sin2_eff_unc,
    }

    payload = {
        "theorem_name": "Eq52 Weinberg Structural Generator and Nonbacktracking Correction",
        "all_checks_passed": all(checks.values()),
        "summary": {
            "q": q,
            "Phi3": phi3,
            "W33_degree_k": k,
            "nonbacktracking_degree_k_minus_1": nb,
            "tree_generator_q_over_Phi3_exact": "3/13",
            "tree_generator_q_over_Phi3_float": float(x0),
            "Q_matrix_Q22": kappa_y,
            "GUT_normalized_sin2_thetaW": sin2_gut,
            "alpha_hat_inverse_MZ_used": alpha_inv_mz,
            "radiative_correction_alpha_over_11": correction,
            "corrected_Z_pole_prediction": x_eff,
            "PDG_live_sin2_eff_lept_used": pdg_sin2_eff,
            "residual_prediction_minus_PDG": residual,
            "residual_in_sigma_units": zscore,
        },
        "checks": checks,
        "identities": {
            "GUT_scale_structural_normalization": "Q[2,2]=5/3 => sin^2(theta_W)_GUT = 1/(1+5/3)=3/8",
            "finite_geometric_tree_generator": "x0 = q/Phi3 = 3/13",
            "nonbacktracking_radiative_refinement": "x_eff(MZ) = 3/13 + alpha_hat(MZ)/(k-1), with k-1=11",
            "numerical_refinement": "3/13 + 1/(11*127.930) = 0.23147985...",
        },
        "interpretation": (
            "Eq. 52 should be rewritten as a structural generator, not a bare measured-angle equality. "
            "The W33 Q-matrix supplies the standard GUT normalization 3/8, while the projective W33/Heawood denominator "
            "supplies the IR tree generator 3/13. The observed effective Z-pole value is then captured by the natural "
            "one-step W33 nonbacktracking radiative correction alpha_hat(MZ)/(k-1)."
        ),
        "boundary": (
            "The alpha/(k-1) correction is a new structural refinement and should be presented as a conjectural leading correction "
            "until derived from the W33 transport effective action. It makes a precise testable statement rather than relying on the raw 3/13 coincidence."
        ),
    }

    path = ROOT / "data" / "w33_weinberg_eq52_structural_correction.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
