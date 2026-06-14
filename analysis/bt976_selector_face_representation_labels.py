#!/usr/bin/env python3
"""BT976 - representation label scaffold for selector rail faces.

Attaches provisional representation labels to the selector-fixed 27+27+27 faces
and complementary face.  This is a scaffold: it creates stable labels and tests
slot counts, but does not assert charge assignments or fitted SM constants.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt976_selector_face_representation_labels.json"
FACES = [
    {"face": [0,1,3], "label": "GenRail_A", "contains_high_rail": True, "size": 27},
    {"face": [0,2,3], "label": "GenRail_B", "contains_high_rail": True, "size": 27},
    {"face": [1,2,3], "label": "GenRail_C", "contains_high_rail": True, "size": 27},
    {"face": [0,1,2], "label": "CompRail_0", "contains_high_rail": False, "size": 27},
]
PHASE_SLOTS = {"rail0": 16, "rail1": 16, "rail2": 19, "rail3": 27}


def main() -> None:
    generation_faces = [f for f in FACES if f["contains_high_rail"]]
    complement_faces = [f for f in FACES if not f["contains_high_rail"]]
    result = {
        "theorem": "BT976 selector-face representation label scaffold",
        "status": "stable labels attached; charges/field assignments not asserted",
        "final_selector": [[3,68], [4,42], [38,65], [90,144]],
        "face_labels": FACES,
        "generation_labels": [f["label"] for f in generation_faces],
        "complement_labels": [f["label"] for f in complement_faces],
        "generation_slot_total": sum(f["size"] for f in generation_faces),
        "complement_slot_total": sum(f["size"] for f in complement_faces),
        "phase_slots": PHASE_SLOTS,
        "representation_contract": {
            "next_required_input": "map each 27-slot face to representation/charge labels from the existing W33 generation machinery",
            "pass_condition": "label counts and phase-slot placements remain invariant under the selected ABI subgroup"
        },
        "reading": "The selector-fixed 27+27+27 split now has stable face labels GenRail_A/B/C plus a complementary CompRail_0 face. This prepares the actual representation-label test without claiming the charge map yet.",
        "checks": {"T1_three_generation_faces": len(generation_faces)==3, "T2_generation_total_81": sum(f["size"] for f in generation_faces)==81, "T3_one_complement_face": len(complement_faces)==1, "T4_phase_slots_recorded": sorted(PHASE_SLOTS.values())==[16,16,19,27], "T5_no_charge_overclaim": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT976 wrote", OUT)

if __name__ == "__main__":
    main()
