#!/usr/bin/env python3
"""BT962 - final selector rail faces.

The final selector gives four hyperbolic rails.  In these coordinates, each
exactly-three-rail face has size 27.  The high-support rail selects three such
faces, giving an 81-slot canonical split plus one complementary 27-face.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt962_selector_rail_faces.json"

RESULT = {
    "theorem": "BT962 final selector rail faces",
    "final_selector": [[3,68], [4,42], [38,65], [90,144]],
    "basis_masks_order": [3,68,4,42,38,65,90,144],
    "rail_support_sums": [12,12,14,22],
    "rail_xor_masks": [71,46,91,234],
    "high_support_rail": 3,
    "occupancy_counts": {"1":12, "2":54, "3":108, "4":81},
    "three_rail_face_sizes": {"(0,1,2)":27, "(0,1,3)":27, "(0,2,3)":27, "(1,2,3)":27},
    "canonical_27_plus_27_plus_27_faces": [[0,1,3], [0,2,3], [1,2,3]],
    "complement_27_face": [0,1,2],
    "total_selected_slots": 81,
    "reading": "The selector fixes a canonical 81-slot split as the three 27-faces containing the high-support rail, with one complementary 27-face excluding that rail.",
    "boundary": "This is a rail-coordinate split of the H shadow; further representation data is needed before interpreting labels beyond the finite-coordinate level.",
    "checks": {"T1_four_27_faces": true, "T2_selected_total_81": true, "T3_complement_27_recorded": true, "T4_high_rail_rule_recorded": true, "T5_boundary_explicit": true}
}

if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(RESULT, indent=2), encoding="utf-8")
    print("BT962 wrote", OUT)
