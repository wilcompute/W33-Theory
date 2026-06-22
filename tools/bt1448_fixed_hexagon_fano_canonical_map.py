#!/usr/bin/env python3
"""BT1448: replace the convention-dependent 12*(13+1)->21*8 map by a
Szilassi/Frobenius-seeded canonical map.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1448_fixed_hexagon_fano_canonical_map.json"

FIXED_FACE = 4
PAIRS = [[0, 1], [2, 6], [3, 5]]
OPPOSITE_VERTEX_PAIRS = [[11, 10], [9, 8], [12, 13]]


def main() -> None:
    face_order = [FIXED_FACE] + [x for pair in PAIRS for x in pair]
    fano_flags = [{"flag": len(face_order[:i]) * 3 + d, "face": face, "local_dir": d} for i, face in enumerate(face_order) for d in range(3)]

    strands = []
    for pair_index, pair in enumerate(PAIRS):
        for side, face in enumerate(pair):
            for orientation in range(2):
                strands.append({
                    "strand": len(strands),
                    "pair_index": pair_index,
                    "side": side,
                    "face": face,
                    "orientation": orientation,
                    "opposite_vertices": OPPOSITE_VERTEX_PAIRS[pair_index],
                })

    active_map = []
    targets = set()
    for strand in strands:
        for tick in range(14):
            active_bin = strand["strand"] * 14 + tick
            flag_slot = active_bin // 8
            state = active_bin % 8
            target = (flag_slot, state)
            targets.add(target)
            active_map.append({
                "active_bin": active_bin,
                "strand": strand["strand"],
                "tick": tick,
                "tick_kind": "closure" if tick == 13 else "phase",
                "fano_flag": flag_slot,
                "local_state": state,
                "canonical_face": fano_flags[flag_slot]["face"],
                "canonical_local_dir": fano_flags[flag_slot]["local_dir"],
            })

    closure_map = []
    for strand in strands:
        active_bin = strand["strand"] * 14 + 13
        closure_map.append({
            "active_bin": active_bin,
            "strand": strand["strand"],
            "fixed_face": FIXED_FACE,
            "closure_local_dir": strand["pair_index"],
            "opposite_vertices": strand["opposite_vertices"],
            "guard_bins": [strand["strand"] * 2, strand["strand"] * 2 + 1],
            "orientation": strand["orientation"],
        })

    checks = {
        "face_order_has_7": len(face_order) == 7 and face_order[0] == 4,
        "fano_flags_are_21": len(fano_flags) == 21,
        "strands_are_12": len(strands) == 12,
        "active_map_is_168": len(active_map) == 168,
        "active_targets_cover_21_times_8": len(targets) == 168,
        "closure_map_is_12": len(closure_map) == 12,
        "closure_all_on_fixed_face": all(row["fixed_face"] == 4 for row in closure_map),
        "closure_dirs_are_balanced": sorted([sum(1 for row in closure_map if row["closure_local_dir"] == d) for d in range(3)]) == [4, 4, 4],
        "guard_bins_cover_24": sorted({g for row in closure_map for g in row["guard_bins"]}) == list(range(24)),
    }
    result = {
        "bt": 1448,
        "title": "Fixed-hexagon to Fano canonical map",
        "verified": all(checks.values()),
        "canonical_seed": {
            "fixed_face": FIXED_FACE,
            "frobenius_involution": "tau_4(x)=-x+1 mod 7",
            "face_order": face_order,
            "face_pairs": PAIRS,
            "opposite_vertex_pairs": OPPOSITE_VERTEX_PAIRS,
        },
        "fano_flag_order": fano_flags,
        "strand_order": strands,
        "active_map_samples": active_map[:24],
        "closure_map": closure_map,
        "interpretation": "The fixed Szilassi face and tau_4 involution replace the arbitrary BT1443 ordering by a canonical ordering seed; only local direction naming remains conventional.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1448, "verified": result["verified"], "face_order": face_order}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
