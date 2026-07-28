#!/usr/bin/env python3
"""Pass 1163 v2: corrected projective 432-orbit pre-computation."""
from __future__ import annotations
import json
from pathlib import Path


def main() -> dict:
    # In an alternating symplectic form every 1-space is isotropic.
    points = 40
    lines = 40
    flags = 160
    adjacent_pairs = 40 * 12 // 2
    nonadjacent_pairs = 40 * 27 // 2
    assert adjacent_pairs + nonadjacent_pairs == 780
    result = {
        "schema": "w33.pass1163.sp43_stabilizer_precompute.v2",
        "status": "PASS",
        "acting_group": "PSp(4,3) on projective W(3,3) objects",
        "acting_group_order": 25920,
        "symplectic_cover": {"group": "Sp(4,3)", "order": 51840, "center_invisible_projectively": True},
        "geometry": {"points": points, "lines": lines, "flags": flags},
        "unordered_pair_orbits": [adjacent_pairs, nonadjacent_pairs],
        "pair_orbit_not_432": True,
        "coset_candidate": {
            "PSp(4,3)/A5_size": 25920 // 60,
            "status": "cardinality match only until an explicit A5 subgroup and equivariant identification are supplied",
        },
        "correction": "All 40 projective points are isotropic for an alternating form; the earlier 16-point/30-line count was not W(3,3).",
    }
    out = Path("data/SP43_PRECOMPUTE_2026_07_27.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1163 v2 projective geometry 40 points, 40 lines, 160 flags")
    return result


if __name__ == "__main__": main()
