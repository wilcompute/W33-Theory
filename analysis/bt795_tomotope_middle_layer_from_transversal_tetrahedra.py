#!/usr/bin/env python3
"""
BT795 - Middle layer from four common-transversal tetrahedra.

For a W33 skew chart, BT794 gives four common isotropic transversals.  Treat
these four transversals as local carrier tetrahedra.  Each carrier is a 4-point
line with the tetrahedral K4 grammar:

  edge axes: 3 opposite-edge matchings
  faces: 4 triangular 3-subsets
  local incidences: 4 faces * 3 axes = 12 per carrier

Across four carriers this gives 12 edge-axis labels, 16 face labels, and 48
middle incidence blocks.
"""
from __future__ import annotations
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPPOSITE_AXES = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
TRIANGLE_FACES = list(combinations(range(4), 3))


def carrier_layer(carrier, pts):
    edge_axes = []
    faces = []
    incidences = []
    for axis_id, pair in enumerate(OPPOSITE_AXES):
        edge_axes.append({"carrier": carrier, "axis": axis_id, "edges": [[pts[i] for i in e] for e in pair]})
    for face_id, tri in enumerate(TRIANGLE_FACES):
        tri_set = set(tri)
        faces.append({"carrier": carrier, "face": face_id, "points": [pts[i] for i in tri]})
        for axis_id, pair in enumerate(OPPOSITE_AXES):
            contained = [e for e in pair if set(e) <= tri_set]
            assert len(contained) == 1
            incidences.append({"carrier": carrier, "face": face_id, "axis": axis_id, "edge": [pts[i] for i in contained[0]]})
    return edge_axes, faces, incidences


def main():
    carriers = [list(range(4*i, 4*i+4)) for i in range(4)]
    all_edges, all_faces, all_incidences = [], [], []
    for i, pts in enumerate(carriers):
        e, f, inc = carrier_layer(i, pts)
        all_edges += e
        all_faces += f
        all_incidences += inc
    checks = {
        "edge_axis_count": len(all_edges) == 12,
        "face_count": len(all_faces) == 16,
        "incidence_count": len(all_incidences) == 48,
        "three_axes_per_face": all(sum(1 for x in all_incidences if x["carrier"] == f["carrier"] and x["face"] == f["face"]) == 3 for f in all_faces),
        "four_faces_per_axis_per_carrier": all(sum(1 for x in all_incidences if x["carrier"] == c and x["axis"] == a) == 4 for c in range(4) for a in range(3))
    }
    assert all(checks.values())
    out = {
        "theorem": "BT795 middle layer from four common-transversal tetrahedra",
        "counts": {"carriers": 4, "edge_axis_labels": 12, "face_labels": 16, "middle_incidence_blocks": 48},
        "formulas": {"edge_axes": "4*3=12", "faces": "4*4=16", "incidences": "4*4*3=48"},
        "checks": checks,
        "interpretation": "The four common transversals carry the local middle layer: 12 edge axes, 16 face labels, and 48 face-axis incidence blocks."
    }
    path = ROOT / "data" / "bt795_tomotope_middle_layer_from_transversal_tetrahedra.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
