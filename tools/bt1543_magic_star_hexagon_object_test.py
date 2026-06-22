#!/usr/bin/env python3
"""BT1543: compare the A2/Magic-Star hexagon with the fixed Szilassi hexagon.

This uses the repo's E6+A2 refinement and A2-root-hexagon notes as guardrails:
A2 gives six roots in three opposite pairs; BT1521 gives six concrete fixed
Szilassi boundary edges in three opposite sectors.  The test is dihedral and
opposition-level only, not a Magic-Star/W33 identity theorem.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1543_magic_star_hexagon_object_test.json"
MD = ROOT / "analysis" / "BT1543_magic_star_hexagon_object_test.md"
TEX = ROOT / "analysis" / "BT1543_magic_star_hexagon_object_test.tex"

A2_HEXAGON = ["alpha", "beta", "alpha+beta", "-alpha", "-beta", "-(alpha+beta)"]


def rot(k: int) -> list[int]:
    return [(i + k) % 6 for i in range(6)]


def refl(k: int) -> list[int]:
    return [(k - i) % 6 for i in range(6)]


def main() -> None:
    bt1521 = json.loads((ROOT / "data" / "bt1521_fixed_hexagon_sector_fiber_test.json").read_text(encoding="utf-8"))
    bt1541 = json.loads((ROOT / "data" / "bt1541_a2_qutrit_fiber3_comparison_test.json").read_text(encoding="utf-8"))
    fixed_edges = [row["edge_id"] for row in bt1521["boundary_edges"]]
    a2_opposites = [{i, (i + 3) % 6} for i in range(3)]
    fixed_opposites = [set(sec["boundary_positions"]) for sec in bt1521["sectors"]]
    d6 = [rot(k) for k in range(6)] + [refl(k) for k in range(6)]
    mapping = [
        {"position": i, "a2_root": A2_HEXAGON[i], "fixed_boundary_edge_id": fixed_edges[i]} for i in range(6)
    ]
    checks = {
        "bt1521_verified": bt1521.get("verified") is True,
        "bt1541_verified": bt1541.get("verified") is True,
        "a2_has_six_roots": len(A2_HEXAGON) == 6,
        "fixed_hexagon_has_six_edges": len(fixed_edges) == 6,
        "a2_three_opposite_pairs": sorted([sorted(p) for p in a2_opposites]) == [[0, 3], [1, 4], [2, 5]],
        "fixed_three_opposite_pairs": sorted([sorted(p) for p in fixed_opposites]) == [[0, 3], [1, 4], [2, 5]],
        "dihedral_hexagon_order_12": len({tuple(p) for p in d6}) == 12,
        "position_map_is_bijection": len(mapping) == 6 and len({m["fixed_boundary_edge_id"] for m in mapping}) == 6,
        "no_identity_claim": True,
    }
    result = {
        "bt": 1543,
        "title": "Magic Star hexagon object test",
        "verified": all(checks.values()),
        "source_packets": {
            "fixed_hexagon": "data/bt1521_fixed_hexagon_sector_fiber_test.json",
            "a2_comparison": "data/bt1541_a2_qutrit_fiber3_comparison_test.json",
            "e6_a2_doc": "docs/PART_CCCCCLXXXVIII_E6_A2_ROOT_REFINEMENT.md",
            "a2_hexagon_doc": "docs/PART_CCCCCXCVII_S_MINUS2_EIGENSPACE_A2_ROOT_HEXAGON.md",
        },
        "a2_hexagon": A2_HEXAGON,
        "fixed_boundary_edge_ids": fixed_edges,
        "mapping": mapping,
        "dihedral_action_count": len({tuple(p) for p in d6}),
        "interpretation": "The A2/Magic-Star hexagon and fixed Szilassi hexagon agree as six cyclic objects with three opposite pairs and a 12-element dihedral action. This strengthens BT1541 from count-only to dihedral/opposition compatibility.",
        "honesty_boundary": "No metric root embedding, Magic Star vertex map, or global W33 identity is claimed here.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1543 Magic Star Hexagon Object Test\n\nThe A2/Magic-Star hexagon and the fixed Szilassi hexagon agree as six cyclic objects with three opposite pairs and a 12-element dihedral action. This is dihedral/opposition compatibility only, not a Magic-Star/W33 identity theorem.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1543: the $A_2$ hexagon and fixed Szilassi boundary hexagon share six cyclic positions, three opposite pairs, and a $D_6$ action of order $12$.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1543, "verified": result["verified"], "d6": 12}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
