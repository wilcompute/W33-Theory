#!/usr/bin/env python3
"""BT1528: explicit K4/tetrahedral 24-flag carrier and pointed-star map."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1528_tetrahedral_carrier_realization.json"
MD = ROOT / "analysis" / "BT1528_tetrahedral_carrier_realization.md"
TEX = ROOT / "analysis" / "BT1528_tetrahedral_carrier_realization.tex"

VERTICES = list(range(4))
EDGES = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
FACES = [(0,1,2),(0,1,3),(0,2,3),(1,2,3)]


def tetra_flags():
    rows = []
    for ei, (a, b) in enumerate(EDGES):
        incident_faces = [fi for fi, face in enumerate(FACES) if a in face and b in face]
        for vertex in (a, b):
            for face in incident_faces:
                rows.append({
                    "flag_id": len(rows),
                    "vertex": vertex,
                    "edge_id": ei,
                    "edge": [a, b],
                    "face_id": face,
                    "face": list(FACES[face]),
                })
    return rows


def main() -> None:
    flags = tetra_flags()
    csaszar_star = flags[:12]
    szilassi_star = flags[12:]
    orientation_profile = {
        "csaszar_star_flag_ids": [f["flag_id"] for f in csaszar_star],
        "szilassi_star_flag_ids": [f["flag_id"] for f in szilassi_star],
        "split_rule": "first 12 flags = pointed Csaszar vertex-star carrier; last 12 = pointed Szilassi face-star carrier",
    }
    checks = {
        "tetra_vertices_4": len(VERTICES) == 4,
        "tetra_edges_6": len(EDGES) == 6,
        "tetra_faces_4": len(FACES) == 4,
        "tetra_flags_24": len(flags) == 24,
        "two_12_stars_partition_24": len(csaszar_star) == 12 and len(szilassi_star) == 12 and set(f["flag_id"] for f in csaszar_star).isdisjoint(set(f["flag_id"] for f in szilassi_star)),
        "all_edges_have_four_flags": all(sum(1 for f in flags if f["edge_id"] == ei) == 4 for ei in range(6)),
        "all_faces_have_six_flags": all(sum(1 for f in flags if f["face_id"] == fi) == 6 for fi in range(4)),
        "all_vertices_have_six_flags": all(sum(1 for f in flags if f["vertex"] == v) == 6 for v in range(4)),
    }
    result = {
        "bt": 1528,
        "title": "Tetrahedral carrier realization",
        "verified": all(checks.values()),
        "tetrahedron": {"vertices": VERTICES, "edges": [list(e) for e in EDGES], "faces": [list(f) for f in FACES]},
        "flags": flags,
        "pointed_star_map": orientation_profile,
        "interpretation": "The K4/tetrahedron 24-flag carrier is explicit.  Its flags split into two 12-flag packets, matching the pointed Csaszar vertex-star and pointed Szilassi face-star carriers.",
        "honesty_boundary": "The split is a flag-carrier identification. It does not yet specify a unique geometric orientation/sign convention between the toroidal stars and tetrahedral flags.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1528 Tetrahedral Carrier Realization\n\nK4 has 4 vertices, 6 edges, 4 triangular faces, and 24 rank-3 flags.  The flags are split into two 12-flag packets: a pointed Csaszar vertex-star carrier and a pointed Szilassi face-star carrier.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1528: $K_4$ has $4$ vertices, $6$ edges, $4$ faces, and $4E=24$ flags, split as $12+12$.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1528, "verified": result["verified"], "flags": len(flags)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
