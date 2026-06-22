#!/usr/bin/env python3
"""BT1547: map E6/A2 singleton axes to fixed Szilassi hexagon sectors.

Inputs already in the repo:
- E6+A2 refinement: 240 = 72 + 6 + 81 + 81, with the 6 singleton axes as A2 roots.
- BT1543: A2 hexagon object test, mapping six symbolic roots to six fixed Szilassi boundary edges.
- BT1521: fixed Szilassi hexagon sectors map to BT1504 fiber classes.

This is an explicit object map at the finite opposition/dihedral level.  It is
not a metric root embedding or Magic-Star/W33 identity theorem.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1547_e6_a2_singleton_axis_object_map.json"
MD = ROOT / "analysis" / "BT1547_e6_a2_singleton_axis_object_map.md"
TEX = ROOT / "analysis" / "BT1547_e6_a2_singleton_axis_object_map.tex"

AXES = ["alpha", "beta", "alpha+beta", "-alpha", "-beta", "-(alpha+beta)"]


def d6_permutations() -> list[list[int]]:
    rots = [[(i + k) % 6 for i in range(6)] for k in range(6)]
    refl = [[(k - i) % 6 for i in range(6)] for k in range(6)]
    return rots + refl


def main() -> None:
    bt1543 = json.loads((ROOT / "data" / "bt1543_magic_star_hexagon_object_test.json").read_text(encoding="utf-8"))
    bt1521 = json.loads((ROOT / "data" / "bt1521_fixed_hexagon_sector_fiber_test.json").read_text(encoding="utf-8"))
    fixed_edges = bt1543["fixed_boundary_edge_ids"]
    pos_to_sector = {}
    pos_to_fiber = {}
    for sec in bt1521["sectors"]:
        for pos in sec["boundary_positions"]:
            pos_to_sector[pos] = sec["sector"]
            pos_to_fiber[pos] = sec["fiber_class"]
    rows = []
    for i, axis in enumerate(AXES):
        rows.append({
            "singleton_axis_index": i,
            "a2_root_label": axis,
            "opposite_axis_index": (i + 3) % 6,
            "fixed_hexagon_position": i,
            "fixed_szilassi_edge_id": fixed_edges[i],
            "sector": pos_to_sector[i],
            "fiber_class": pos_to_fiber[i],
        })
    d6 = d6_permutations()
    opposite_preserved = True
    for p in d6:
        for i in range(6):
            if p[(i + 3) % 6] != (p[i] + 3) % 6:
                opposite_preserved = False
    checks = {
        "bt1543_verified": bt1543.get("verified") is True,
        "bt1521_verified": bt1521.get("verified") is True,
        "six_singleton_axes": len(rows) == 6,
        "six_distinct_edges": len({r["fixed_szilassi_edge_id"] for r in rows}) == 6,
        "three_sector_classes": sorted({r["sector"] for r in rows}) == [0, 1, 2],
        "three_fiber_classes": sorted({r["fiber_class"] for r in rows}) == [0, 1, 2],
        "opposite_axes_share_sector": all(rows[i]["sector"] == rows[i + 3]["sector"] for i in range(3)),
        "opposite_axes_share_fiber": all(rows[i]["fiber_class"] == rows[i + 3]["fiber_class"] for i in range(3)),
        "d6_action_count_12": len({tuple(p) for p in d6}) == 12,
        "d6_preserves_opposition": opposite_preserved,
    }
    result = {
        "bt": 1547,
        "title": "E6/A2 singleton-axis object map",
        "verified": all(checks.values()),
        "source_packets": {
            "e6_a2_refinement": "docs/PART_CCCCCLXXXVIII_E6_A2_ROOT_REFINEMENT.md",
            "hexagon_object_test": "data/bt1543_magic_star_hexagon_object_test.json",
            "fixed_sector_fiber": "data/bt1521_fixed_hexagon_sector_fiber_test.json",
        },
        "rows": rows,
        "d6_action_count": len({tuple(p) for p in d6}),
        "interpretation": "The six E6/A2 singleton axes can be mapped objectwise to the six fixed Szilassi boundary edges. Opposite A2 axes land in the same fixed-hexagon sector and the same BT1504 fiber class, and the D6 hexagon action preserves the opposition relation.",
        "honesty_boundary": "This is finite object/opposition compatibility. It is not a metric A2 root embedding, Magic-Star vertex map, or global W33 identity theorem.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1547 E6/A2 Singleton-axis Object Map\n\nThe six E6/A2 singleton axes are mapped to the six fixed Szilassi boundary edges. Opposite singleton axes share the same fixed-hexagon sector and BT1504 fiber class. The D6 hexagon action preserves opposition. This is object/opposition compatibility, not a metric root embedding or Magic-Star/W33 identity theorem.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1547: six E6/A2 singleton axes map to six fixed Szilassi boundary edges, with opposite axes sharing the same sector and fiber class.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1547, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
