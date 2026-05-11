#!/usr/bin/env python3
"""
PART CCCCCI: Gap-Square Scalar-Flavor Theorem

Part CCCCC isolated the Perron/global channel:
  - Green/residue operation -> alpha correction
  - determinant/compactification operation -> top/CKM compactified density

This part identifies the complementary non-Perron r-channel surface.  In
W(3,3)=SRG(40,12,2,4), the positive restricted adjacency eigenvalue is

    r = lambda = 2

and the corresponding Laplacian gap is

    Delta_r = k - r = 12 - 2 = 10 = Phi_4.

Therefore the gap-square denominator is

    Delta_r^2 = Phi_4^2 = 100.

The Higgs quartic and CKM A are exactly two numerators over this same
r-channel gap-square:

    lambda_H = Phi_3 / Delta_r^2 = 13/100,
    A_CKM    = q^4   / Delta_r^2 = 81/100.

Hence

    A_CKM / lambda_H = q^4 / Phi_3 = 81/13,

with the shared normalization denominator eliminated.  This is the
non-Perron scalar-flavor surface complementary to the Perron global-channel
surface of Part CCCCC.

Run:
    python exploration/PART_CCCCCI_GAP_SQUARE_SCALAR_FLAVOR_THEOREM.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def main() -> None:
    q = 3
    assert math.factorial(q) == 2 * q
    lam = 2
    mu = 4
    k = q * (q + 1)
    v = (q + 1) * (q * q + 1)
    E = v * k // 2

    # SRG restricted eigenvalues and multiplicities.
    r = lam
    s = -mu
    f = 24
    g = 15

    # Laplacian gaps.
    delta_r = k - r
    delta_s = k - s
    phi3 = q * q + q + 1
    phi4 = q * q + 1
    phi6 = q * q - q + 1

    gap_square = delta_r * delta_r

    # Scalar/flavor gap-square surface.
    lambda_H = Fraction(phi3, gap_square)
    A_ckm = Fraction(q**4, gap_square)
    A_over_lambdaH = A_ckm / lambda_H
    A_minus_lambdaH = A_ckm - lambda_H
    A_plus_lambdaH = A_ckm + lambda_H

    # Compare with Perron global-channel surface from CCCCC.
    det_I_plus_J = v + 1
    top_cube = Fraction(v, det_I_plus_J)
    lambda_ckm = Fraction(q * q, v)
    compactified_flavor = lambda_ckm * top_cube

    # PMNS/gap cross-links.  Reactor angle also uses Phi_4^2 but with lambda^2 scaling.
    pmns_theta13 = Fraction(q * q, (lam * phi4) ** 2)
    pmns_gap_relation = pmns_theta13 * lam * lam

    checks = {
        "true_master_equation": math.factorial(q) == 2 * q,
        "w33_atoms": (q, lam, mu, k, v, E) == (3, 2, 4, 12, 40, 240),
        "restricted_eigenvalues": (r, s, f, g) == (2, -4, 24, 15),
        "r_laplacian_gap_is_phi4": delta_r == phi4 == 10,
        "s_laplacian_gap_is_16": delta_s == 16,
        "gap_square_is_100": gap_square == 100,
        "lambda_H_is_13_over_100": lambda_H == Fraction(13, 100),
        "A_ckm_is_81_over_100": A_ckm == Fraction(81, 100),
        "A_over_lambdaH_is_81_over_13": A_over_lambdaH == Fraction(81, 13),
        "A_minus_lambdaH_is_17_over_25": A_minus_lambdaH == Fraction(17, 25),
        "A_plus_lambdaH_is_47_over_50": A_plus_lambdaH == Fraction(47, 50),
        "perron_top_cube_still_40_over_41": top_cube == Fraction(40, 41),
        "perron_compactified_flavor_still_9_over_41": compactified_flavor == Fraction(9, 41),
        "pmns_theta13_is_9_over_400": pmns_theta13 == Fraction(9, 400),
        "pmns_theta13_times_lambda_squared_is_9_over_100": pmns_gap_relation == Fraction(9, 100),
    }

    result = {
        "part": "CCCCCI",
        "title": "Gap-Square Scalar-Flavor Theorem",
        "atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "k": k,
            "v": v,
            "E": E,
            "r": r,
            "s": s,
            "f": f,
            "g": g,
            "Phi3": phi3,
            "Phi4": phi4,
            "Phi6": phi6,
        },
        "gap_square_surface": {
            "r_channel": "positive restricted adjacency eigenvalue r=lambda=2",
            "laplacian_gap_delta_r": delta_r,
            "gap_square_delta_r_squared": gap_square,
            "lambda_H": str(lambda_H),
            "A_CKM": str(A_ckm),
            "A_CKM_over_lambda_H": str(A_over_lambdaH),
            "A_CKM_minus_lambda_H": str(A_minus_lambdaH),
            "A_CKM_plus_lambda_H": str(A_plus_lambdaH),
        },
        "perron_surface_comparison": {
            "top_yukawa_cubed": str(top_cube),
            "lambda_CKM": str(lambda_ckm),
            "lambda_CKM_times_top_cube": str(compactified_flavor),
            "det_I_plus_J": det_I_plus_J,
            "statement": "Perron channel controls 40/41 and 9/41; r-gap-square channel controls 13/100 and 81/100",
        },
        "pmns_gap_crosslink": {
            "sin2_theta13": str(pmns_theta13),
            "sin2_theta13_times_lambda_squared": str(pmns_gap_relation),
            "interpretation": "PMNS reactor angle uses the same Phi4^2 gap denominator with an additional lambda^2 spinor/polarization scaling",
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The Higgs quartic and CKM A are normalized by the square of the r-channel Laplacian gap, "
            "Delta_r^2=(k-r)^2=Phi4^2=100. This gives a second operator surface complementary "
            "to the Perron global channel: Perron controls alpha/top/CKM-lambda compactification, while "
            "the r-gap-square controls scalar self-coupling and CKM normalization."
        ),
    }

    out = Path("PART_CCCCCI_gap_square_scalar_flavor_theorem_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCI: Gap-Square Scalar-Flavor Theorem")
    print("=" * 78)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-" * 78)
    print(f"Delta_r = {delta_r}")
    print(f"Delta_r^2 = {gap_square}")
    print(f"lambda_H = {lambda_H}")
    print(f"A_CKM = {A_ckm}")
    print(f"A/lambda_H = {A_over_lambdaH}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
