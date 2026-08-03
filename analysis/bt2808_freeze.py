#!/usr/bin/env python3
"""Freeze the compact public Pass 2808 certificate."""
from __future__ import annotations

import json
from pathlib import Path

from bt2808_pg32_tetrahedral_support_lift import build_certificate

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "PART_BT2808_PG32_TETRAHEDRAL_SUPPORT_LIFT_results.json"


def compact_certificate(certificate: dict) -> dict:
    return {
        "schema": certificate["schema"],
        "status": certificate["status"],
        "canonical_pass": certificate["canonical_pass"],
        "title": certificate["title"],
        "headline": certificate["headline"],
        "check_count": certificate["check_count"],
        "checks": certificate["checks"],
        "pg32": certificate["pg32"],
        "support_lift": {
            "definition": certificate["support_lift"]["definition"],
            "fiber_law": certificate["support_lift"]["fiber_law"],
            "fibers": [
                {
                    key: row[key]
                    for key in (
                        "mask",
                        "tetrahedral_role",
                        "support_weight",
                        "fiber_size",
                    )
                }
                for row in certificate["support_lift"]["fiber_rows"]
            ],
            "weight_total_profile": certificate["support_lift"][
                "weight_total_profile"
            ],
            "tomotope_f_vector": certificate["support_lift"]["tomotope_f_vector"],
            "interpretation": certificate["support_lift"]["interpretation"],
        },
        "equitable_quotients": {
            "matching_count": certificate["equitable_quotients"]["matching_count"],
            "closed_formula": certificate["equitable_quotients"]["closed_formula"],
            "zero_sum_sign_counts": certificate["equitable_quotients"][
                "zero_sum_sign_counts"
            ],
            "full_w33_spectrum": certificate["equitable_quotients"][
                "full_w33_spectrum"
            ],
            "binary_support_quotient_spectrum": certificate["equitable_quotients"][
                "binary_support_quotient_spectrum"
            ],
            "ternary_phase_residual_spectrum": certificate["equitable_quotients"][
                "ternary_phase_residual_spectrum"
            ],
            "quadratic_identity": certificate["equitable_quotients"][
                "quadratic_identity"
            ],
            "detailed_balance": certificate["equitable_quotients"][
                "detailed_balance"
            ],
            "matching_results": [
                {
                    "matching": row["matching"],
                    "involution": row["involution"],
                    "w33_srg": row["w33_srg"],
                    "quotient": {
                        key: row["quotient"][key]
                        for key in (
                            "equitable",
                            "row_sum_set",
                            "entry_histogram",
                            "eigenvalues",
                            "characteristic_factorization",
                            "residual_phase_eigenvalues",
                            "residual_characteristic_factorization",
                            "detailed_balance",
                            "quadratic_identity",
                            "closed_formula_verified",
                            "sha256",
                        )
                    },
                }
                for row in certificate["equitable_quotients"]["matching_results"]
            ],
        },
        "selector_bridge": certificate["selector_bridge"],
        "boundaries": certificate["boundaries"],
    }


def main() -> None:
    compact = compact_certificate(build_certificate())
    OUTPUT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n")
    print(f"PASS {compact['check_count']}/{compact['check_count']}")
    print(OUTPUT)


if __name__ == "__main__":
    main()
