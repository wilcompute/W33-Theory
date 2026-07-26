#!/usr/bin/env python3
"""Pass 1059b: audit the late parallel Pass5 continuation.

This companion belongs to the sixth workstream. It separates valid arithmetic
from the unsupported amplitude, Ihara, Coxeter-angle, Fisher, and Lean-build
promotions that landed after the first Pass-1059 release.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main() -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]

    binomial_sector_sum = sum(math.comb(11, index) for index in range(2, 10))
    mhv_arithmetic = math.comb(14, 2) - 1

    spectrum = {12: 1, 2: 24, -4: 15}
    nontrivial_pole_count = 2 * (spectrum[2] + spectrum[-4])
    edge_count = 40 * 12 // 2
    bass_exponent = edge_count - 40

    # For the trivial adjacency eigenvalue 12,
    # 1 - 12u + 11u^2 = (1-u)(1-11u).
    trivial_factor_product = (1, -12, 11)
    claimed_trivial_factor_product = (1, -13, 12)  # (1-u)(1-12u)

    alpha = (1.0, -1.0)
    beta = (0.0, 2.0)
    dot = alpha[0] * beta[0] + alpha[1] * beta[1]
    norm_alpha = math.hypot(*alpha)
    norm_beta = math.hypot(*beta)
    c2_cosine = dot / (norm_alpha * norm_beta)
    bc_cosine = -2 / 3

    actual_formal_module = root / "formal" / "W33" / "Pass575CyclotomicDVRKernel.lean"
    late_parallel_file = root / "lean" / "Pass575CyclotomicDVRKernel.lean"

    checks = {
        "late_binomial_sum_is_2024_not_2048": binomial_sector_sum == 2024,
        "ninety_equals_choose_14_2_minus_one_arithmetically": mhv_arithmetic == 90,
        "correct_W33_spectrum_is_12_1_2_24_minus4_15": spectrum == {12: 1, 2: 24, -4: 15},
        "nontrivial_Ihara_pole_count_is_78": nontrivial_pole_count == 78,
        "late_Ihara_multiplicities_26_13_are_wrong": (26, 13) != (spectrum[2], spectrum[-4]),
        "trivial_Ihara_factor_is_1_minus_u_times_1_minus_11u": trivial_factor_product != claimed_trivial_factor_product and trivial_factor_product == (1, -12, 11),
        "Bass_positive_200_exponent_belongs_to_inverse_zeta": bass_exponent == 200,
        "C2_simple_root_cosine_is_minus_one_over_sqrt2_not_minus_two_thirds": abs(c2_cosine + 1 / math.sqrt(2)) < 1e-12 and abs(c2_cosine - bc_cosine) > 1e-3,
        "late_Lean_file_is_separate_from_actual_formal_module": actual_formal_module.exists() and late_parallel_file.exists() and actual_formal_module != late_parallel_file,
    }
    if not all(checks.values()):
        raise AssertionError([name for name, passed in checks.items() if not passed])

    return {
        "schema": "w33.pass1059b.parallel_continue_audit.v1",
        "status": "PASS",
        "headline": "The late parallel continuation retains the corrected W33 spectrum and the arithmetic 90=C(14,2)-1, but its BCFW total, Ihara factorization, Coxeter-angle identification, and Lean-build claim fail exact checks.",
        "retained": {
            "W33_spectrum": "12^1, 2^24, (-4)^15",
            "nontrivial_Ihara_poles": nontrivial_pole_count,
            "MHV_arithmetic_only": "90 = C(14,2)-1",
        },
        "corrections": {
            "binomial_sum": {"claimed": 2048, "exact": binomial_sector_sum, "formula": "sum_{j=2}^9 C(11,j)"},
            "Ihara": {
                "correct_inverse_zeta": "Z(u)^(-1)=(1-u^2)^200(1-u)(1-11u)(1-2u+11u^2)^24(1+4u+11u^2)^15",
                "late_claim_errors": ["uses multiplicities 26 and 13", "uses (1-u)(1-12u)", "places (1-u^2)^200 in Z rather than Z^(-1)", "calls poles zeros"],
            },
            "C2_angle": {"simple_roots": [list(alpha), list(beta)], "cosine": c2_cosine, "angle_degrees": math.degrees(math.acos(c2_cosine)), "BC_cosine": bc_cosine, "conclusion": "The displayed eigenvalue ratio is a tautological construction of -2/3, not the Coxeter angle of type C2/Sp4."},
            "Pass575": {"actual_formal_module": str(actual_formal_module.relative_to(root)), "late_parallel_file": str(late_parallel_file.relative_to(root)), "conclusion": "The late file is a separate proposal. It neither replaces the actual imported module nor supplies a successful Lake build artifact."},
            "Fisher_and_amplitude": "No data likelihood, symplectic order-48 subgroup, BCFW cell complex, or W33-to-amplitude incidence map is constructed by the continuation commit.",
        },
        "check_count": len(checks),
        "checks": checks,
        "scope": "Exact arithmetic and repository-path audit. The physical and representation-theoretic interpretations remain conjectural until their missing objects are built.",
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1059b_parallel_continue_audit.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "headline": result["headline"], "check_count": result["check_count"]}, indent=2))
