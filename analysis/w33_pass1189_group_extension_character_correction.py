#!/usr/bin/env python3
"""Pass 1189: exact group-extension, coset, and character-degree correction."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1189_group_extension_character_correction.json"

WE6_IRREP_DEGREES = [
    1, 1, 6, 6, 10, 15, 15, 15, 15, 20, 20, 20, 24, 24,
    30, 30, 60, 60, 60, 64, 64, 80, 81, 81, 90,
]
REJECTED_PASS1160_DEGREES = [
    1, 6, 6, 10, 15, 15, 20, 20, 24, 24, 30, 60, 60, 64, 80,
    81, 90, 90, 120, 120, 160, 216, 240, 270, 360,
]


def main() -> dict:
    psp_order = 25920
    sp_order = 51840
    we6_order = 51840
    exact_square_sum = sum(d * d for d in WE6_IRREP_DEGREES)
    rejected_square_sum = sum(d * d for d in REJECTED_PASS1160_DEGREES)

    assert len(WE6_IRREP_DEGREES) == 25
    assert exact_square_sum == we6_order
    assert rejected_square_sum == 405088
    assert sp_order == 2 * psp_order
    assert we6_order == 2 * psp_order

    # Correct 432-coset arithmetic.
    assert we6_order // 120 == 432
    assert psp_order // 60 == 432
    assert sp_order // 120 == 432

    # S5 has trivial center and no normal subgroup of order 2, so it cannot
    # quotient to A5 by killing a central involution.  The valid mechanism is
    # restriction from W(E6)=PSp(4,3):2 to its index-two normal PSp subgroup,
    # provided H=S5 meets PSp in A5.
    s5_normal_subgroup_orders = {1, 60, 120}
    assert 2 not in s5_normal_subgroup_orders

    result = {
        "schema": "w33.pass1189.group_extension_character_correction.v1",
        "status": "PASS",
        "orders": {
            "PSp(4,3)": psp_order,
            "Sp(4,3)": sp_order,
            "W(E6)": we6_order,
        },
        "extension_types": {
            "Sp(4,3)": "central double cover of PSp(4,3); its center is invisible on projective points",
            "W(E6)": "outer split extension PSp(4,3):2",
            "nonconflation": "The two order-51840 groups are different extensions and no quotient W(E6)->Sp(4,3) is asserted.",
        },
        "coset_432_correction": {
            "W(E6)/S5": we6_order // 120,
            "PSp(4,3)/A5": psp_order // 60,
            "Sp(4,3)/order120": sp_order // 120,
            "valid_possible_bridge": "Restrict the W(E6)/S5 action to normal PSp(4,3). If S5 intersects PSp in A5, the same 432-element set is PSp/A5.",
            "explicit_intersection_still_required": True,
            "rejected_mechanism": "S5 cannot map onto A5 by quotienting a central C2: S5 has trivial center and no normal subgroup of order 2.",
        },
        "exact_character_degrees": WE6_IRREP_DEGREES,
        "exact_sum_of_squares": exact_square_sum,
        "rejected_pass1160_degree_list": REJECTED_PASS1160_DEGREES,
        "rejected_sum_of_squares": rejected_square_sum,
        "checks": {
            "twenty_five_irreducibles": len(WE6_IRREP_DEGREES) == 25,
            "sum_squares_is_51840": exact_square_sum == 51840,
            "both_extensions_have_order_51840": sp_order == we6_order == 51840,
            "projective_index_two": sp_order == 2 * psp_order,
            "coset_sizes_432": [we6_order // 120, psp_order // 60, sp_order // 120] == [432, 432, 432],
            "s5_has_no_normal_c2": 2 not in s5_normal_subgroup_orders,
            "rejected_list_fails": rejected_square_sum == 405088,
        },
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1189 extension types separated; 432 restriction criterion locked")
    return result


if __name__ == "__main__":
    main()
