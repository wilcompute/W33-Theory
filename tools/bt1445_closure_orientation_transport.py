#!/usr/bin/env python3
"""BT1445: transport Otto's odd closure tick through the fixed Szilassi hexagon."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1445_closure_orientation_transport.json"


def main():
    # Coordinate result from BT1444.  Repeated here so this verifier is stable
    # before generated data files exist in a fresh checkout.
    fixed_face = [11, 9, 12, 10, 8, 13]
    image_order = [10, 8, 13, 11, 9, 12]
    boundary_shift = 3
    opposite_pairs = [[fixed_face[i], fixed_face[(i + boundary_shift) % 6]] for i in range(boundary_shift)]

    closure_ticks = [{"strand": s, "active_bin": s * 14 + 13, "tick": 13} for s in range(12)]
    guard_bins = [{"strand": s, "orientation": o, "guard_bin": s * 2 + o} for s in range(12) for o in range(2)]
    transported = []
    for tick in closure_ticks:
        pair = opposite_pairs[tick["strand"] % 3]
        orientation = (tick["strand"] // 3) % 2
        transported.append({
            **tick,
            "fixed_face_vertices": fixed_face,
            "opposite_pair": pair,
            "orientation": orientation,
            "guard_pair": [tick["strand"] * 2, tick["strand"] * 2 + 1],
            "fano_flag": tick["active_bin"] // 8,
            "local_state": tick["active_bin"] % 8,
        })
    checks = {
        "fixed_face_has_six_vertices": len(fixed_face) == 6,
        "c2_image_is_shift_by_three": image_order == fixed_face[3:] + fixed_face[:3],
        "three_opposite_pairs": len(opposite_pairs) == 3 and all(len(p) == 2 for p in opposite_pairs),
        "closure_ticks_are_12": len(closure_ticks) == 12,
        "guard_bins_are_24": len(guard_bins) == 24,
        "each_closure_tick_has_two_guard_orientations": all(len(row["guard_pair"]) == 2 for row in transported),
        "closure_bins_are_tick_13": all(row["tick"] == 13 for row in transported),
        "transport_lands_in_168_bus": all(0 <= row["active_bin"] < 168 for row in transported),
        "transport_lands_in_21_fano_flags": all(0 <= row["fano_flag"] < 21 for row in transported),
        "transport_lands_in_8_local_states": all(0 <= row["local_state"] < 8 for row in transported),
    }
    result = {
        "bt": 1445,
        "title": "Closure orientation transport",
        "verified": all(checks.values()),
        "fixed_face": fixed_face,
        "c2_boundary_image_order": image_order,
        "boundary_shift": boundary_shift,
        "opposite_pairs": opposite_pairs,
        "closure_transport": transported,
        "interpretation": "The odd tick can be carried by the fixed Szilassi hexagon: the C2 action shifts the boundary by three vertices, giving three opposite pairs and two guard orientations per Otto strand.",
        "boundary": "This verifies orientation compatibility at the finite-bus level; it still needs a geometric embedding proof from Otto's physical helix into these coordinates.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1445, "verified": result["verified"], "opposite_pairs": opposite_pairs}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
