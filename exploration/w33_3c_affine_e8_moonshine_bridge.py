"""The Monster class 3C is the exact affine E8 character on the q -> q^3 lift.

The level-1 affine E8 character is

    ch_{E8,1}(tau) = q^(-1/3) (1 + 248 q + 4124 q^2 + 34752 q^3 + ...).

The Monster 3C McKay-Thompson series begins

    T_3C(q) = q^(-1) + 248 q^2 + 4124 q^5 + 34752 q^8 + ...

So the exponents and coefficients line up exactly:

    T_3C(q) = ch_{E8,1}(3 tau)
            = q^(-1) (1 + 248 q^3 + 4124 q^6 + 34752 q^9 + ...).

This is stronger than a few matching coefficients.  Up to the verified range,
every nonzero 3C coefficient sits on the congruence class e ≡ -1 (mod 3), and
the coefficient at e = 3n - 1 is the n-th affine E8 coefficient.

The same class also satisfies the p=3 replicability identity.  In this case the
Faber polynomial collapses to

    Phi_3(x) = x^3 - 744,

so the affine E8 lift already lives on the 1A-sourced moonshine recursion:

    T_3C(q)^3 - 744 = J(q^3) + 3 (T_3C |_U_3)(q).
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_3c_affine_e8_moonshine_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import affine_e8_series
from scripts.w33_leech_monster import (
    mckay_thompson_series,
    verify_fricke_prime_replicability,
)


def build_summary(affine_terms: int = 10) -> dict[str, Any]:
    affine = affine_e8_series(q_order=max(affine_terms + 2, 12))
    t3c = mckay_thompson_series("3C", max_q_exp=3 * affine_terms + 5)
    if t3c is None:
        raise RuntimeError("3C McKay-Thompson series unavailable")

    comparison_rows = []
    all_match = True
    for n, coeff in enumerate(affine["series"][:affine_terms]):
        exp = 3 * n - 1
        got = int(t3c.get(exp, 0))
        match = got == int(coeff)
        all_match = all_match and match
        comparison_rows.append(
            {
                "n": n,
                "affine_exponent": n,
                "monster_exponent": exp,
                "affine_coeff": int(coeff),
                "T_3C_coeff": got,
                "match": match,
            }
        )

    max_exp = 3 * affine_terms - 1
    off_grid_terms = {
        str(exp): int(t3c.get(exp, 0))
        for exp in range(0, max_exp + 1)
        if (exp + 1) % 3 != 0 and int(t3c.get(exp, 0)) != 0
    }

    replicability = verify_fricke_prime_replicability("3C", max_q_exp=max_exp)
    faber_coeffs = [int(c) for c in replicability["faber_coeffs"]]

    return {
        "threeC_affine_e8_dictionary": {
            "affine_shift": str(affine["shift"]),
            "affine_e8_coefficients": [int(c) for c in affine["series"][:affine_terms]],
            "threeC_coefficients_on_exp_3n_minus_1": comparison_rows,
            "threeC_off_grid_nonzero_terms": off_grid_terms,
            "threeC_replicability": {
                "verified": bool(replicability["verified"]),
                "faber_coeffs": faber_coeffs,
                "n_mismatches": int(replicability["n_mismatches"]),
            },
            "first_affine_packet_hits": {
                "248_at_q2": int(t3c.get(2, 0)),
                "4124_at_q5": int(t3c.get(5, 0)),
                "34752_at_q8": int(t3c.get(8, 0)),
            },
        },
        "threeC_affine_e8_theorem": {
            "the_affine_e8_shift_is_exactly_minus_one_third": str(affine["shift"]) == "-1/3",
            "the_3C_series_matches_the_affine_E8_character_on_every_exp_3n_minus_1_slot_checked": all_match,
            "the_3C_series_has_no_off_grid_nonzero_terms_in_the_checked_range": off_grid_terms == {},
            "the_first_three_nontrivial_3C_coefficients_are_248_4124_34752": (
                int(t3c.get(2, 0)) == 248
                and int(t3c.get(5, 0)) == 4124
                and int(t3c.get(8, 0)) == 34752
            ),
            "the_3C_class_therefore_equals_the_affine_E8_character_under_q_to_q_cubed": (
                all_match and off_grid_terms == {}
            ),
            "the_3C_class_satisfies_prime_replicability": bool(replicability["verified"]),
            "the_3C_faber_polynomial_is_exactly_x_cubed_minus_744": faber_coeffs == [-744, 0, 0],
            "the_affine_E8_lift_is_therefore_already_on_the_1A_sourced_moonshine_recursion": (
                bool(replicability["verified"]) and faber_coeffs == [-744, 0, 0]
            ),
        },
        "interpretation": (
            "The Monster class 3C is not merely adjacent to the affine E8 modular "
            "layer. It is the exact q -> q^3 realization of the level-1 affine E8 "
            "character. The coefficients 248, 4124, 34752, 213126, ... are therefore "
            "simultaneously affine E8 excitation counts and moonshine coefficients, "
            "and the same class already satisfies the cubic 1A-sourced replicability "
            "law T_3C^3 - 744 = J(q^3) + 3 U_3(T_3C)."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 3C AFFINE E8 MOONSHINE BRIDGE")
    print("=" * 72)
    for key, value in summary["threeC_affine_e8_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
