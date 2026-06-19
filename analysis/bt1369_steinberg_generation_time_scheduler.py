#!/usr/bin/env python3
"""BT1369: test the 2160 phase grading as a generation-time scheduler."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1369_steinberg_generation_time_scheduler.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_result() -> dict[str, object]:
    bt1366 = load_json(ROOT / "data" / "bt1366_global_2160_d12_clock_grading.json")
    bt1365 = load_json(ROOT / "data" / "bt1365_qutrit_phase_sheet_alignment.json")
    bt863 = load_json(ROOT / "data" / "bt863_generations_steinberg_vanishing.json")
    bt868 = load_json(ROOT / "data" / "bt868_joint_generation_chirality_grading.json")

    phase_orbits = int(bt1366["grading"]["descended_global_orbits"])
    orbit_size = int(bt1366["grading"]["descended_global_orbit_size"])
    total_slots = phase_orbits * orbit_size
    generation_dims = bt863["t2_generations"]
    generation_count = len(generation_dims)
    generation_dim = generation_dims[0]
    phase_count = int(bt1365["local_bt1363_phase_bus"]["phase_count"])
    geographies = int(bt1366["inputs"]["polar_pair_geography"])

    chi9_classes = [
        cls
        for cls in bt868["classes"]
        if cls["chirality"] == [45, 36] and cls["mult"] == [15, 12, 15, 12, 15, 12]
    ]
    order2160_classes = [cls for cls in bt868["classes"] if cls["size"] == 2160]

    lanes_per_generation_state = phase_orbits // generation_dim
    slots_per_generation_state = lanes_per_generation_state * orbit_size
    positive_chirality_channels = 15
    time_residues = geographies // positive_chirality_channels

    scheduler = {
        "shape": "generation_state x lane x tomotope_face_register",
        "phase_orbits": phase_orbits,
        "orbit_size": orbit_size,
        "total_slots": total_slots,
        "generation_count": generation_count,
        "generation_dim": generation_dim,
        "lanes_per_generation_state": lanes_per_generation_state,
        "slots_per_generation_state": slots_per_generation_state,
        "per_generation_phase_orbits": geographies,
        "per_generation_phase_slots": geographies * orbit_size,
        "chirality_time_factorization": (
            "135 = 3 generations * 3 time residues * 15 positive-chirality channels"
        ),
        "spinor_register_reading": "each sixteen-slot orbit is one tomotope face / SO(10)-spinor register",
    }

    checks = {
        "bt1366_bus_slots_are_2160": total_slots == 2160,
        "phase_count_matches_steinberg_generation_count": phase_count
        == generation_count
        == 3,
        "steinberg_generations_are_27_each": generation_dims == [27, 27, 27],
        "phase_orbits_are_five_lanes_per_generation_state": phase_orbits
        == 5 * generation_dim,
        "each_generation_state_gets_80_slots": slots_per_generation_state == 80,
        "per_generation_phase_is_45_orbits": phase_orbits
        == generation_count * geographies,
        "geography_is_time_lift_of_bt868_positive_chirality": time_residues == 3
        and geographies == time_residues * positive_chirality_channels,
        "bt868_has_positive_45_chirality_classes": len(chi9_classes) == 5,
        "bt868_has_order6_class_of_size_2160": len(order2160_classes) == 1,
        "sixteen_slot_orbit_matches_local_face_register": bt1365[
            "local_bt1363_phase_bus"
        ]["face_labels_per_phase"]
        == [16, 16, 16],
    }

    return {
        "bt": 1369,
        "title": "Steinberg generation-time scheduler",
        "verified": all(checks.values()),
        "scheduler": scheduler,
        "source_identities": {
            "bt1366": bt1366["grading"]["identity"],
            "bt1365": bt1365["alignment"]["identity"],
            "bt863_generations": generation_dims,
            "bt868_chi9_class_count": len(chi9_classes),
            "bt868_order2160_class": (
                order2160_classes[0] if order2160_classes else None
            ),
        },
        "interpretation": (
            "The 135 sixteen-slot phase orbits have exactly the shape of a "
            "generation-time scheduler: five lanes for each of the 27 Steinberg "
            "states, or equivalently three generation phases times a 45-geometry "
            "time wheel.  The 45 wheel is the 3-time-residue lift of the "
            "15-channel positive chirality branch in the BT868 order-6 grading."
        ),
        "boundary": (
            "This is an exact dimensional and character-profile scheduler test. "
            "It does not yet construct a basis-level action of the 2160 slots on "
            "the Steinberg module."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "scheduler_shape": result["scheduler"]["shape"],
                "total_slots": result["scheduler"]["total_slots"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
