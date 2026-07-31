#!/usr/bin/env python3
"""Compact invariant certificate for the exact Passes 1380--1384 verifier."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import w33_pass1380_1384_mackey_selector_decomposition as detailed

DEFAULT_OUT = ROOT / "data" / "w33_pass1380_1384_mackey_selector_decomposition.json"


def build():
    full = detailed.analyze()
    p1380 = full["pass1380_little_group_character_table"]
    p1381 = full["pass1381_selector_permutation_character"]
    p1382 = full["pass1382_mackey_wedderburn_identification"]
    p1383 = full["pass1383_terwilliger_fusion_explanation"]

    assert p1380["dual_orbit_sizes"] == [1, 2, 4, 4, 8, 8]
    assert p1380["irreducible_count"] == 27
    assert p1380["irreducible_degree_census"] == {"1": 8, "2": 6, "4": 9, "8": 4}
    assert p1380["sum_squared_degrees"] == 432
    assert p1380["all_character_values_rational_integers"] is True

    assert p1381["nonzero_constituents"] == 14
    assert p1381["constituent_degree_profile"] == [1,1,1,2,2,2,4,4,4,4,8,8,8,8]
    assert p1381["multiplicity_profile"] == [1,1,1,1,1,1,1,2,2,3,3,3,4,5]
    assert p1381["dimension_check"] == 120
    assert p1381["commutant_dimension_from_multiplicities"] == 83

    assert p1382["dimension"] == 83
    assert p1382["center_dimension"] == 14
    assert p1382["exact_projector_matches"] == 14

    assert p1383["fusion_group_sizes"] == [1,1,1,1,1,1,1,2,2,3]
    assert p1383["schur_defect"] == 4
    packets = sorted(
        sorted(int(child["splitter_eigenvalue"]) for child in item["children"])
        for item in p1383["fusion"] if item["child_count"] > 1
    )
    assert packets == [[-4, -1, 2], [-3, 0], [-3, 3]]

    return {
      "schema": "w33.pass1380_1384.mackey_selector_decomposition.compact.v1",
      "status": "PASS",
      "pass1380_little_group_character_table": {
        "group": "C3^3 : (D8 x C2)",
        "group_order": 432,
        "dual_orbit_sizes": [1,2,4,4,8,8],
        "little_group_orders": [16,8,4,4,2,2],
        "little_group_types": ["D8xC2","D8","V4","V4","C2","C2"],
        "irreducible_count": 27,
        "irreducible_degree_census": {"1":8,"2":6,"4":9,"8":4},
        "sum_squared_degrees": 432,
        "all_character_values_rational_integers": True,
        "rational_group_algebra": "Q^8 + M2(Q)^6 + M4(Q)^9 + M8(Q)^4"
      },
      "pass1381_selector_permutation_character": {
        "degree": 120,
        "nonzero_constituents": 14,
        "constituent_degree_profile": [1,1,1,2,2,2,4,4,4,4,8,8,8,8],
        "multiplicity_profile": [1,1,1,1,1,1,1,2,2,3,3,3,4,5],
        "dimension_check": 120,
        "commutant_dimension_from_multiplicities": 83
      },
      "pass1382_mackey_wedderburn_identification": {
        "orbital_algebra": "End_H(Q^120)",
        "dimension": 83,
        "center_dimension": 14,
        "wedderburn": "Q^7 + M2(Q)^2 + M3(Q)^3 + M4(Q) + M5(Q)",
        "exact_projector_matches": 14
      },
      "pass1383_terwilliger_fusion_explanation": {
        "terwilliger_center_dimension": 10,
        "orbital_center_dimension": 14,
        "fusion_group_sizes": [1,1,1,1,1,1,1,2,2,3],
        "scalar_packet_sizes": [2,2,3],
        "scalar_splitter_eigenvalue_packets": [[-4,-1,2],[-3,0],[-3,3]],
        "schur_defect": 4
      },
      "pass1384_boundary": {
        "mathematics": "Literal permutation-group reconstruction, exact little-group induction, exact character projectors, and Z[omega] arithmetic; no database table or floating eigensolver.",
        "physics": "Finite rational representation theory only; no particle, gauge, generation, hardware, or laboratory identification."
      }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    digest = hashlib.sha256(encoded.encode()).hexdigest()
    if args.check:
        if not args.output.exists() or args.output.read_text() != encoded:
            raise SystemExit(f"certificate drift: {args.output}")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(f"PASS 1380-1384 compact certificate sha256={digest}")


if __name__ == "__main__":
    main()
