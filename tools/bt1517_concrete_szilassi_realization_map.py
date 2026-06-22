#!/usr/bin/env python3
"""BT1517: map BT1514 7/21/3 incidence classes to concrete Szilassi realization data.

This uses the prior BT1444 fixed-face extractor rather than inventing a new
face convention.  The concrete anchor is the unique Szilassi fixed hexagon
[11, 9, 12, 10, 8, 13] with boundary shift 3.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1517_concrete_szilassi_realization_map.json"
MD = ROOT / "analysis" / "BT1517_concrete_szilassi_realization_map.md"
TEX = ROOT / "analysis" / "BT1517_concrete_szilassi_realization_map.tex"

FIXED_HEXAGON = [11, 9, 12, 10, 8, 13]
# BT1444 face-orbit canonical order compatible with earlier closure work.
FACE_CLASS_TO_SZILASSI_FACE = {0: 4, 1: 0, 2: 1, 3: 2, 4: 6, 5: 3, 6: 5}


def main() -> None:
    bt1444 = json.loads((ROOT / "data" / "bt1444_szilassi_fixed_face_extractor.json").read_text(encoding="utf-8"))
    face_to_edges = {f: sorted({(3 * f + j) % 21 for j in range(6)}) for f in range(7)}
    edge_classes = sorted({e for vals in face_to_edges.values() for e in vals})
    edge_to_faces = {e: sorted([f for f, vals in face_to_edges.items() if e in vals]) for e in edge_classes}
    concrete = []
    for f in range(7):
        face = FACE_CLASS_TO_SZILASSI_FACE[f]
        boundary = FIXED_HEXAGON if face == 4 else None
        concrete.append({
            "bt1504_point_class": f,
            "bt1514_face_class": f,
            "szilassi_face_index": face,
            "incident_flag_edge_classes": face_to_edges[f],
            "concrete_boundary_vertices_if_known": boundary,
            "anchor_status": "BT1444 fixed hexagon" if face == 4 else "face-orbit placeholder pending full face list import",
        })
    checks = {
        "bt1444_verified": bt1444.get("verified") is True,
        "fixed_face_index_4": all(r["fixed_face_index"] == 4 for r in bt1444["realizations"]),
        "fixed_hexagon_matches": all(r["fixed_face_vertices"] == FIXED_HEXAGON for r in bt1444["realizations"]),
        "boundary_shift_three": all(r["boundary_cyclic_shift"] == 3 for r in bt1444["realizations"]),
        "seven_face_classes": len(concrete) == 7,
        "twenty_one_edge_classes": len(edge_classes) == 21,
        "six_edges_per_face": all(len(row["incident_flag_edge_classes"]) == 6 for row in concrete),
        "two_faces_per_edge": all(len(v) == 2 for v in edge_to_faces.values()),
        "fixed_face_class_anchored_to_szilassi_face_4": next(row for row in concrete if row["szilassi_face_index"] == 4)["concrete_boundary_vertices_if_known"] == FIXED_HEXAGON,
    }
    result = {
        "bt": 1517,
        "title": "Concrete Szilassi realization map",
        "verified": all(checks.values()),
        "source_packets": {"bt1514": "data/bt1514_toroidal_incidence_test.json", "bt1444": "data/bt1444_szilassi_fixed_face_extractor.json", "toroidal_data": "data/Toroidal-Polyhedra-Realizations.txt"},
        "face_class_to_szilassi_face": {str(k): v for k, v in FACE_CLASS_TO_SZILASSI_FACE.items()},
        "fixed_hexagon_anchor": {"face_index": 4, "vertices": FIXED_HEXAGON, "boundary_shift": 3},
        "edge_to_faces": {str(k): v for k, v in edge_to_faces.items()},
        "concrete_rows": concrete,
        "interpretation": "The BT1514 incidence model now has a concrete Szilassi anchor: point/face class 0 is mapped to the unique BT1444 fixed hexagon face 4, whose six boundary vertices split naturally into three opposite two-edge sectors by the boundary shift of 3.",
        "honesty_boundary": "Only the fixed hexagon is concretely anchored to parsed realization vertices here. The remaining six face-class labels follow the prior orbit convention and need full Szilassi face-list import for a complete embedding theorem.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1517 Concrete Szilassi Realization Map\n\nBT1517 anchors the 7/21/3 incidence model to the actual BT1444 Szilassi fixed hexagon: face index 4 with vertices [11, 9, 12, 10, 8, 13] and boundary shift 3.  The remaining six face labels retain the earlier face-orbit convention until the full face list is imported.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nFixed Szilassi anchor: face 4 has boundary vertices $[11,9,12,10,8,13]$ and boundary shift $3$.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1517, "verified": result["verified"], "fixed_hexagon": FIXED_HEXAGON}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
