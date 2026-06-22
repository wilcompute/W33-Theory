#!/usr/bin/env python3
"""BT1544: obstruction test for promoting toroidal pointed stars to a Jordan pair.

The paired 12+12 toroidal pointed-star carrier has the correct *pair size* and
sign balance, but the repo currently supplies no quadratic/triple product table
U_x y or closure law.  Therefore the Magic-Star/Jordan-pair analogy remains an
external comparison until an explicit product is constructed and verified.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1544_jordan_pair_carrier_obstruction_test.json"
MD = ROOT / "analysis" / "BT1544_jordan_pair_carrier_obstruction_test.md"
TEX = ROOT / "analysis" / "BT1544_jordan_pair_carrier_obstruction_test.tex"

REQUIRED_FOR_JORDAN_PAIR = [
    "plus_module_elements",
    "minus_module_elements",
    "quadratic_maps_U_plus_and_U_minus",
    "linearized_V_maps",
    "closure_on_plus_minus_modules",
    "Jordan_pair_identities",
]

AVAILABLE_FROM_REPO = [
    "plus_minus_12_flag_carriers",
    "balanced_sign_profiles",
    "K4_24_flag_carrier",
    "incidence_order",
]


def main() -> None:
    bt1528 = json.loads((ROOT / "data" / "bt1528_tetrahedral_carrier_realization.json").read_text(encoding="utf-8"))
    bt1534 = json.loads((ROOT / "data" / "bt1534_toroidal_star_sign_lift.json").read_text(encoding="utf-8"))
    missing = [x for x in REQUIRED_FOR_JORDAN_PAIR if x not in AVAILABLE_FROM_REPO]
    checks = {
        "bt1528_verified": bt1528.get("verified") is True,
        "bt1534_verified": bt1534.get("verified") is True,
        "carrier_size_12_plus_12": bt1534["profiles"]["combined"] == {"plus": 12, "minus": 12},
        "k4_carrier_24": bt1528.get("flag_count") == 24 or bt1528.get("tetrahedron", {}).get("vertices") == [0, 1, 2, 3],
        "required_schema_has_six_items": len(REQUIRED_FOR_JORDAN_PAIR) == 6,
        "missing_product_data": "quadratic_maps_U_plus_and_U_minus" in missing and "Jordan_pair_identities" in missing,
        "analogy_remains_external": True,
    }
    result = {
        "bt": 1544,
        "title": "Jordan-pair carrier obstruction test",
        "verified": all(checks.values()),
        "source_packets": {
            "k4_carrier": "data/bt1528_tetrahedral_carrier_realization.json",
            "toroidal_sign_lift": "data/bt1534_toroidal_star_sign_lift.json",
            "magic_star_map": "data/bt1540_magic_star_object_map_scaffold.json",
        },
        "available_from_repo": AVAILABLE_FROM_REPO,
        "required_for_jordan_pair": REQUIRED_FOR_JORDAN_PAIR,
        "missing_requirements": missing,
        "interpretation": "The 12+12 pointed-star carrier matches the size/sign shape expected for a pair object, but it lacks quadratic U maps, V maps, closure data, and Jordan-pair identities. The Jordan-pair analogy is therefore obstructed as a theorem and must remain external-comparison/candidate until a product table is built.",
        "honesty_boundary": "This is a schema obstruction, not a proof that no Jordan-pair structure can ever exist on a future enriched carrier.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1544 Jordan-pair Carrier Obstruction Test\n\nThe paired 12+12 toroidal pointed-star carrier has the right size and sign balance, but the repo does not yet provide quadratic U maps, V maps, closure data, or Jordan-pair identities. The analogy remains external/candidate until a product table is built and verified.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1544: the $12+12$ carrier has pair shape but no verified Jordan-pair product; the claim remains external/candidate.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1544, "verified": result["verified"], "missing": len(missing)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
