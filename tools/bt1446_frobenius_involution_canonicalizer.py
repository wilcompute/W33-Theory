#!/usr/bin/env python3
"""BT1446: canonicalize the Otto/Szilassi/Fano ordering by F42 involutions."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1446_frobenius_involution_canonicalizer.json"


def tau_for_fixed_point(fp: int):
    # affine involution x -> -x + b with fixed point fp, so b = 2*fp mod 7
    b = (2 * fp) % 7
    return {x: (b - x) % 7 for x in range(7)}


def cycles_of(p):
    seen = set()
    cycles = []
    for x in range(7):
        if x in seen:
            continue
        cur = []
        y = x
        while y not in seen:
            seen.add(y)
            cur.append(y)
            y = p[y]
        cycles.append(cur)
    return cycles


def main():
    involutions = []
    for fp in range(7):
        p = tau_for_fixed_point(fp)
        cycles = cycles_of(p)
        pairs = sorted([c for c in cycles if len(c) == 2])
        fixed = [c[0] for c in cycles if len(c) == 1]
        involutions.append({"fixed_point": fp, "b": (2 * fp) % 7, "map": {str(k): v for k, v in p.items()}, "pairs": pairs, "fixed": fixed})
    closure_face = 4
    canonical = involutions[closure_face]
    strand_order = []
    for pair_index, pair in enumerate(canonical["pairs"]):
        for side, face in enumerate(pair):
            for orient in range(2):
                strand_order.append({"strand": len(strand_order), "pair_index": pair_index, "side": side, "orientation": orient, "face": face})
    fano_flag_order = []
    for face in [closure_face] + [x for pair in canonical["pairs"] for x in pair]:
        for local_dir in range(3):
            fano_flag_order.append({"flag_index": len(fano_flag_order), "face": face, "local_dir": local_dir})
    checks = {
        "seven_involutions": len(involutions) == 7,
        "all_are_one_fixed_three_pairs": all(len(inv["fixed"]) == 1 and len(inv["pairs"]) == 3 for inv in involutions),
        "canonical_fixed_face_is_4": canonical["fixed"] == [4],
        "canonical_pairs_are_expected": canonical["pairs"] == [[0, 1], [2, 6], [3, 5]],
        "strand_order_has_12": len(strand_order) == 12,
        "fano_flag_order_has_21": len(fano_flag_order) == 21,
        "closure_face_first_in_fano_order": fano_flag_order[0]["face"] == 4,
        "three_local_dirs_per_face": len(fano_flag_order) == 7 * 3,
    }
    result = {
        "bt": 1446,
        "title": "Frobenius involution canonicalizer",
        "verified": all(checks.values()),
        "group_model": "F42 = affine maps x -> a*x + b over Z7; involutions are x -> -x + b",
        "all_involutions": involutions,
        "canonical_choice": {
            "reason": "BT1444 fixed Szilassi face has index 4, so choose the unique F42 involution with fixed point 4.",
            "involution": canonical,
        },
        "canonical_strand_order": strand_order,
        "canonical_fano_flag_order": fano_flag_order,
        "interpretation": "The unique involution fixing the Szilassi closure face supplies a convention-free ordering seed for Otto strands and Fano flags, modulo the remaining choice of local direction labels.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1446, "verified": result["verified"], "fixed": canonical["fixed"], "pairs": canonical["pairs"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
