#!/usr/bin/env python3
"""
PART CCCCCXXIII: Moment-Ratio Scalar Action Theorem

PART CCCCCXXII proved the spectral moment identity:

    Tr(A^3) / Tr(A^2) = r = 2.

PART CCCCCXXI proved the scalar topology action:

    lambda_H = (Delta_s/Delta_r) * dim(E6) / Tr(A^3).

This part fuses them. Since Tr(A^3)=r*Tr(A^2), the Higgs quartic also has the
moment-ratio compressed form

    lambda_H = (Delta_s/Delta_r) * dim(E6) / (r * Tr(A^2)).

For W(3,3):

    Delta_s/Delta_r = 16/10 = 8/5,
    dim(E6) = 78,
    r = 2,
    Tr(A^2) = 480,

so

    lambda_H = (8/5)*78/(2*480)=13/100.

The scalar sector is therefore normalized by the second spectral moment once
the Master-Equation moment identity Tr(A^3)/Tr(A^2)=r is imposed.

Run:
    python exploration/PART_CCCCCXXIII_MOMENT_RATIO_SCALAR_ACTION.py
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
    v = (q + 1) * (q*q + 1)
    E = v * k // 2
    directed_edges = 2 * E
    triangles = 160

    # W(3,3) restricted spectrum.
    r = lam
    s = -mu
    f = 24
    g = 15

    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1

    delta_r = k - r
    delta_s = k - s
    gap_ratio = Fraction(delta_s, delta_r)

    # Spectral moments.
    trA2 = k*k + f*r*r + g*s*s
    trA3 = k**3 + f*r**3 + g*s**3
    moment_ratio = Fraction(trA3, trA2)

    # Exceptional/scalar data.
    dim_E6 = lam * q * phi3
    dim_E8 = E + lam**3
    dim_SU5 = f

    # Three equivalent scalar/Higgs forms.
    lambda_H_triangle = gap_ratio * Fraction(dim_E6, trA3)
    lambda_H_moment_ratio = gap_ratio * Fraction(dim_E6, r * trA2)
    lambda_H_cyclotomic = Fraction(phi3, phi4*phi4)

    # Inverse action forms.
    lambda_inv_triangle = Fraction(trA3, 1) / (gap_ratio * dim_E6)
    lambda_inv_moment = Fraction(r * trA2, 1) / (gap_ratio * dim_E6)
    lambda_inv_cyclotomic = Fraction(phi4*phi4, phi3)

    # Latest-commit spectral action consistency.
    zero_modes = directed_edges - 320 - 48 - 30
    zero_modes_perron = 2 * (v + 1)
    a6_correct = 4**3 * 320 + 10**3 * 48 + 16**3 * 30

    # Ihara zeta exponents/carriers from latest commit.
    ihara_trivial_exp = E - v
    ihara_perron_factor = (1, -k, -(k-1))      # 1 - 12u - 11u^2
    ihara_r_factor = (1, -r, k-1)              # 1 - 2u + 11u^2
    ihara_s_factor = (1, -s, k-1)              # 1 + 4u + 11u^2

    # Descendants of the compressed scalar action.
    A_CKM = Fraction(q**4, phi3) * lambda_H_moment_ratio
    PMNS_theta13 = Fraction(q*q, lam*lam*phi3) * lambda_H_moment_ratio

    D_t = v + 1
    D_b = q*D_t + lam
    D_c = D_b + k
    y_b = Fraction(q, D_b)
    y_c = Fraction(1, D_c)
    y_tau = lambda_H_moment_ratio * y_b*y_b/y_c

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "w33_atoms": (q,lam,mu,k,v,E,directed_edges,r,s,f,g)==(3,2,4,12,40,240,480,2,-4,24,15),
        "spectral_moments": (trA2,trA3) == (480,960),
        "moment_ratio_equals_r": moment_ratio == r == 2,
        "triangle_trace": trA3 == 6*triangles == 960,
        "gap_ratio": gap_ratio == Fraction(8,5),
        "dim_E6": dim_E6 == 78,
        "lambda_H_triangle": lambda_H_triangle == Fraction(13,100),
        "lambda_H_moment_ratio": lambda_H_moment_ratio == Fraction(13,100),
        "lambda_H_cyclotomic": lambda_H_cyclotomic == Fraction(13,100),
        "inverse_action_forms": lambda_inv_triangle == lambda_inv_moment == lambda_inv_cyclotomic == Fraction(100,13),
        "zero_modes_perron_identity": zero_modes == zero_modes_perron == 82,
        "a6_corrected": a6_correct == 191360,
        "ihara_trivial_exponent": ihara_trivial_exp == 200,
        "ihara_factors": (ihara_perron_factor, ihara_r_factor, ihara_s_factor) == ((1,-12,-11),(1,-2,11),(1,4,11)),
        "descendants": (A_CKM, PMNS_theta13, y_tau) == (Fraction(81,100), Fraction(9,400), Fraction(16029,1562500)),
        "heavy_ladder": (D_t, D_b, D_c, y_b, y_c) == (41, 125, 137, Fraction(3,125), Fraction(1,137)),
        "exceptional_dimensions": (dim_SU5, dim_E6, dim_E8) == (24,78,248),
    }

    result = {
        "part": "CCCCCXXIII",
        "title": "Moment-Ratio Scalar Action Theorem",
        "atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "k": k,
            "v": v,
            "E": E,
            "directed_edges": directed_edges,
            "triangles": triangles,
            "r": r,
            "s": s,
            "f": f,
            "g": g,
            "Phi3": phi3,
            "Phi4": phi4,
            "Phi6": phi6,
        },
        "moment_identity": {
            "Tr_A2": trA2,
            "Tr_A3": trA3,
            "Tr_A3_over_Tr_A2": str(moment_ratio),
            "r": r,
            "statement": "Tr(A^3)/Tr(A^2)=r=2",
        },
        "scalar_action_compression": {
            "triangle_trace_formula": "lambda_H=(Delta_s/Delta_r)*dim(E6)/Tr(A^3)",
            "moment_ratio_formula": "lambda_H=(Delta_s/Delta_r)*dim(E6)/(r*Tr(A^2))",
            "gap_ratio": str(gap_ratio),
            "dim_E6": dim_E6,
            "lambda_H_triangle": str(lambda_H_triangle),
            "lambda_H_moment_ratio": str(lambda_H_moment_ratio),
            "lambda_H_inverse": str(lambda_inv_moment),
        },
        "latest_commit_consistency": {
            "zero_modes": zero_modes,
            "zero_modes_as_2_det": zero_modes_perron,
            "a6_Tr_DF6": a6_correct,
            "ihara_trivial_exponent": ihara_trivial_exp,
            "ihara_factors": {
                "perron": "1-12u-11u^2",
                "r": "1-2u+11u^2",
                "s": "1+4u+11u^2",
            },
        },
        "descendants": {
            "A_CKM": str(A_CKM),
            "PMNS_theta13": str(PMNS_theta13),
            "y_tau": str(y_tau),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The latest spectral moment identity compresses the triangle-trace Higgs mechanism by replacing Tr(A^3) "
            "with r*Tr(A^2). Thus the scalar coupling can be read directly from the second spectral moment once the "
            "Master-Equation identity Tr(A^3)/Tr(A^2)=r is imposed. This fuses the moment-ratio theorem, scalar topology "
            "action, zero-mode Perron identity, sixth spectral-action coefficient, and Ihara zeta carrier."
        ),
    }

    out = Path("PART_CCCCCXXIII_moment_ratio_scalar_action_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCXXIII: Moment-Ratio Scalar Action Theorem")
    print("="*92)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-"*92)
    print(f"lambda_H = (Delta_s/Delta_r)*dim(E6)/(r*Tr(A^2)) = {lambda_H_moment_ratio}")
    print(f"TrA2={trA2}, TrA3={trA3}, ratio={moment_ratio}")
    print(f"a6={a6_correct}, zero_modes={zero_modes}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
