"""The non-Fricke side closes as linear eta branches plus one affine exceptional node.

The Fricke prime classes already close as quadratic trace/norm algebras:

    T_{pA} = X_p + k + p^{k/2} / X_p,
    X_p := (eta(tau) / eta(p tau))^k,     k = 24 / (p - 1).

The non-Fricke side is structurally different.  For the prime non-Fricke
classes

    2B, 3B, 5B, 7B, 13B,

the dual Atkin-Lehner term disappears and the Hauptmodul is exactly linear:

    T_{pB} = X_p + k.

The first composite non-Fricke eta branch behaves the same way:

    T_{4C} = (eta(tau) / eta(4 tau))^8 + 8.

There is then one exceptional linear branch:

    T_{3C}(q) = ch_{E8,1}(3 tau),

the exact q -> q^3 lift of the level-1 affine E8 character.

So the low-level moonshine carrier splits sharply:

    1A      : linear weight-12 quotient line,
    pA      : quadratic Fricke trace/norm branches,
    pB, 4C  : linear eta-unit branches,
    3C      : affine E8 exceptional linear branch.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_nonfricke_linear_moonshine_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_3c_affine_e8_moonshine_bridge import build_summary as build_3c_summary
from w33_fundamental_moonshine_algebra_bridge import build_summary as build_fundamental_summary
from w33_mckay_thompson_eta_quotients import eta_quotient_laurent
from scripts.w33_leech_monster import (
    mckay_thompson_series,
    verify_fricke_prime_replicability,
    verify_rogers_ramanujan_5b_identity,
)


NON_FRICKE_PRIME_ROWS: list[tuple[str, int, int]] = [
    ("2B", 2, 24),
    ("3B", 3, 12),
    ("5B", 5, 6),
    ("7B", 7, 4),
    ("13B", 13, 2),
]


def _linear_eta_row(class_name: str, level: int, k: int, n_terms: int = 12) -> dict[str, Any]:
    x = eta_quotient_laurent(level, k, n_terms)
    t = mckay_thompson_series(class_name, max_q_exp=n_terms)
    if t is None:
        raise RuntimeError(f"Series unavailable for {class_name}")

    exact = True
    mismatches = []
    for exp in range(-1, n_terms + 1):
        lhs = int(t.get(exp, 0))
        rhs = int(x[exp + 1] + (k if exp == 0 else 0))
        if lhs != rhs:
            exact = False
            mismatches.append((exp, lhs, rhs))

    rep = verify_fricke_prime_replicability(class_name, max_q_exp=n_terms)

    return {
        "class_name": class_name,
        "level": level,
        "k": k,
        "linear_eta_formula_q_minus_1_to_q12": {
            str(exp): int(x[exp + 1] + (k if exp == 0 else 0))
            for exp in range(-1, n_terms + 1)
            if int(x[exp + 1] + (k if exp == 0 else 0)) != 0
        },
        "monster_series_q_minus_1_to_q12": {
            str(exp): int(t.get(exp, 0))
            for exp in range(-1, n_terms + 1)
            if int(t.get(exp, 0)) != 0
        },
        "faber_coeffs": [int(c) for c in rep["faber_coeffs"]],
        "mismatches": mismatches,
        "theorems": {
            "linear_eta_formula_holds": exact,
            "prime_replicability_holds": bool(rep["verified"]),
        },
    }


def _four_c_row(n_terms: int = 15) -> dict[str, Any]:
    x = eta_quotient_laurent(4, 8, n_terms)
    t = mckay_thompson_series("4C", max_q_exp=n_terms)
    if t is None:
        raise RuntimeError("Series unavailable for 4C")

    exact = True
    mismatches = []
    for exp in range(-1, n_terms + 1):
        lhs = int(t.get(exp, 0))
        rhs = int(x[exp + 1] + (8 if exp == 0 else 0))
        if lhs != rhs:
            exact = False
            mismatches.append((exp, lhs, rhs))

    odd_support_only = all(
        int(t.get(exp, 0)) == 0 for exp in range(0, n_terms + 1) if exp % 2 == 0
    )

    return {
        "class_name": "4C",
        "level": 4,
        "k": 8,
        "linear_eta_formula_q_minus_1_to_q15": {
            str(exp): int(x[exp + 1] + (8 if exp == 0 else 0))
            for exp in range(-1, n_terms + 1)
            if int(x[exp + 1] + (8 if exp == 0 else 0)) != 0
        },
        "monster_series_q_minus_1_to_q15": {
            str(exp): int(t.get(exp, 0))
            for exp in range(-1, n_terms + 1)
            if int(t.get(exp, 0)) != 0
        },
        "mismatches": mismatches,
        "theorems": {
            "linear_eta_formula_holds": exact,
            "support_is_on_odd_positive_exponents_only": odd_support_only,
        },
    }


def build_summary() -> dict[str, Any]:
    prime_rows = [_linear_eta_row(*row) for row in NON_FRICKE_PRIME_ROWS]
    four_c = _four_c_row()
    five_b_rr = verify_rogers_ramanujan_5b_identity(max_q_exp=24)
    three_c = build_3c_summary()
    fundamental = build_fundamental_summary()

    theorem = {
        "the_fricke_prime_A_side_is_still_quadratic": (
            fundamental["fundamental_moonshine_algebra_theorem"][
                "each_prime_hauptmodul_satisfies_the_quadratic_polynomial_X2_minus_TminuskX_plus_norm"
            ]
        ),
        "all_five_nonfricke_prime_B_classes_are_exact_linear_eta_branches": all(
            all(row["theorems"].values()) for row in prime_rows
        ),
        "5B_has_the_exact_rogers_ramanujan_linear_rewrite": bool(five_b_rr["verified"]),
        "4C_is_the_first_composite_linear_eta_branch": all(four_c["theorems"].values()),
        "3C_is_the_affine_E8_exceptional_linear_branch": (
            three_c["threeC_affine_e8_theorem"][
                "the_3C_class_therefore_equals_the_affine_E8_character_under_q_to_q_cubed"
            ]
            and three_c["threeC_affine_e8_theorem"][
                "the_affine_E8_lift_is_therefore_already_on_the_1A_sourced_moonshine_recursion"
            ]
        ),
    }
    theorem["the_nonfricke_and_exceptional_side_close_on_one_linear_affine_moonshine_spine"] = all(
        theorem.values()
    )

    return {
        "nonfricke_linear_moonshine_dictionary": {
            "nonfricke_prime_rows": prime_rows,
            "fourC_row": four_c,
            "fiveB_rogers_ramanujan_identity": five_b_rr,
            "threeC_affine_bridge_theorem": three_c["threeC_affine_e8_theorem"],
        },
        "nonfricke_linear_moonshine_theorem": theorem,
        "interpretation": (
            "The moonshine base splits into two different algebraic geometries. "
            "The Fricke A-side classes are quadratic trace/norm branches, while "
            "the non-Fricke side is linear: pure eta-unit branches for pB and 4C, "
            "plus the affine E8 exceptional branch 3C. So the low-level moonshine "
            "carrier is not uniform genus-zero data; it is a linear/quadratic split "
            "with 3C as the exceptional affine node."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 NON-FRICKE LINEAR MOONSHINE BRIDGE")
    print("=" * 72)
    for key, value in summary["nonfricke_linear_moonshine_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
