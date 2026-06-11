#!/usr/bin/env python3
"""
BT814 - Tomotope middle layer from the residual transversal tetrahedra.

BT798 identified the residual 48-packet as the four common transversal K4s of
the base skew-line chart.  This verifier reads those four K4s as the local
tomotope middle layer:

    vertices:  four transversal tetrahedra
    edges:     4 tetrahedra * 3 opposite-edge axes = 12
    faces:     4 tetrahedra * 4 triangular faces   = 16
    cells:     4 tetrahedra * 2 antipode sheets     = 8
    middle:    12 edge-axis / 16 face incidences    = 48

The incidence profile is the same profile recorded by the true tomotope
<r0,r3> block data: 48 blocks, four blocks per tomotope edge, and three
blocks per tomotope face.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
import csv
import json
from pathlib import Path

from bt787_rank4_incidence_r11_handle import compute_rank32
from bt798_residual_tetrahedral_carrier import common_transversals


ROOT = Path(__file__).resolve().parents[1]
AXIS_ROOT = ROOT / "axis_bundle_content" / "TOE_tomotope_axis_block_twist_v02_20260228"


def opposite_edge_axes(points: tuple[int, ...]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    p = tuple(sorted(points))
    raw = [
        ((p[0], p[1]), (p[2], p[3])),
        ((p[0], p[2]), (p[1], p[3])),
        ((p[0], p[3]), (p[1], p[2])),
    ]
    return [
        tuple(sorted((tuple(sorted(a)), tuple(sorted(b)))))
        for a, b in raw
    ]


def triangular_faces(points: tuple[int, ...]) -> list[tuple[int, int, int]]:
    return [tuple(face) for face in combinations(sorted(points), 3)]


def contained_axis_edge(
    axis: tuple[tuple[int, int], tuple[int, int]],
    face: tuple[int, int, int],
) -> tuple[int, int]:
    face_set = set(face)
    hits = [edge for edge in axis if set(edge) <= face_set]
    if len(hits) != 1:
        raise AssertionError(f"face {face} should contain exactly one edge of axis {axis}")
    return hits[0]


def load_tomotope_block_summary() -> dict[str, object]:
    with (AXIS_ROOT / "SUMMARY.json").open() as f:
        summary = json.load(f)
    rows = []
    with (AXIS_ROOT / "blocks48_labeled_by_tomotope_edge_face.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return {"summary": summary, "block_rows": rows}


def main() -> None:
    rank32 = compute_rank32()
    geom = rank32["geometry"]
    base_a, base_b = geom["skew"][0]
    transversals = common_transversals(geom, base_a, base_b)
    tomotope_reference = load_tomotope_block_summary()

    vertex_rows = []
    edge_rows = []
    face_rows = []
    cell_rows = []
    block_rows = []

    for v_index, row in enumerate(transversals):
        points = tuple(row["points"])
        vertex_label = f"T{v_index}"
        vertex_rows.append({
            "vertex_label": vertex_label,
            "transversal_line_id": row["line_id"],
            "points": list(points),
        })
        for sheet, pair in (("base", row["base_points"]), ("shadow", row["shadow_points"])):
            cell_rows.append({
                "cell_label": f"{vertex_label}:{sheet}",
                "vertex_label": vertex_label,
                "sheet": sheet,
                "antipode_pair": list(pair),
            })

        axes = opposite_edge_axes(points)
        faces = triangular_faces(points)
        for a_index, axis in enumerate(axes):
            edge_label = f"{vertex_label}:axis{a_index}"
            edge_rows.append({
                "edge_label": edge_label,
                "vertex_label": vertex_label,
                "axis_edges": [list(edge) for edge in axis],
            })
            for f_index, face in enumerate(faces):
                face_label = f"{vertex_label}:face{f_index}"
                if a_index == 0:
                    face_rows.append({
                        "face_label": face_label,
                        "vertex_label": vertex_label,
                        "face_vertices": list(face),
                    })
                contained = contained_axis_edge(axis, face)
                other = next(edge for edge in axis if edge != contained)
                block_rows.append({
                    "block_label": f"{edge_label}|{face_label}",
                    "vertex_label": vertex_label,
                    "edge_label": edge_label,
                    "face_label": face_label,
                    "contained_axis_edge": list(contained),
                    "opposite_axis_edge": list(other),
                })

    edge_block_profile = Counter(block["edge_label"] for block in block_rows)
    face_block_profile = Counter(block["face_label"] for block in block_rows)
    vertex_block_profile = Counter(block["vertex_label"] for block in block_rows)
    reference_summary = tomotope_reference["summary"]
    reference_blocks = tomotope_reference["block_rows"]

    f_vector = {
        "vertices": len(vertex_rows),
        "edges": len(edge_rows),
        "faces": len(face_rows),
        "cells": len(cell_rows),
        "middle_blocks": len(block_rows),
        "flags_if_each_block_has_2x2_fiber": 4 * len(block_rows),
    }
    checks = {
        "four_transversal_vertices": f_vector["vertices"] == 4,
        "twelve_local_tomotope_edges": f_vector["edges"] == 12,
        "sixteen_local_tomotope_faces": f_vector["faces"] == 16,
        "eight_base_shadow_cells": f_vector["cells"] == 8,
        "forty_eight_middle_blocks": f_vector["middle_blocks"] == 48,
        "middle_blocks_give_192_flags_with_2x2_fiber": f_vector["flags_if_each_block_has_2x2_fiber"] == 192,
        "each_local_edge_has_four_blocks": set(edge_block_profile.values()) == {4},
        "each_local_face_has_three_blocks": set(face_block_profile.values()) == {3},
        "each_transversal_vertex_has_twelve_blocks": set(vertex_block_profile.values()) == {12},
        "tomotope_reference_has_48_blocks": reference_summary["blocks48"]["count"] == 48 == len(reference_blocks),
        "tomotope_reference_edge_profile_matches": reference_summary["blocks48"]["blocks_per_tomotope_edge_sizes"] == [4],
        "tomotope_reference_face_profile_matches": reference_summary["blocks48"]["blocks_per_tomotope_face_sizes"] == [3],
        "tomotope_f_vector_matches_reference": reference_summary["tomotope_counts"] == {
            "V": 4, "E": 12, "F": 16, "C": 8, "flags": 192
        },
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT814 check failed: {name}")

    out = {
        "theorem": "BT814 tomotope middle layer from residual transversal tetrahedra",
        "base_skew_pair": [base_a, base_b],
        "f_vector_from_transversal_tetrahedra": f_vector,
        "vertices": vertex_rows,
        "cells": cell_rows,
        "edges": edge_rows,
        "faces": face_rows,
        "middle_blocks_sample": block_rows[:16],
        "profiles": {
            "blocks_per_edge": dict(sorted(Counter(edge_block_profile.values()).items())),
            "blocks_per_face": dict(sorted(Counter(face_block_profile.values()).items())),
            "blocks_per_transversal_vertex": dict(sorted(Counter(vertex_block_profile.values()).items())),
        },
        "tomotope_reference": {
            "source": str((AXIS_ROOT / "SUMMARY.json").relative_to(ROOT)),
            "counts": reference_summary["tomotope_counts"],
            "blocks48": reference_summary["blocks48"],
        },
        "interpretation": {
            "middle_layer": "BT798's four transversal K4s realize the tomotope edge-face middle layer objectwise",
            "edge_labels": "each transversal K4 contributes its three opposite-edge axes",
            "face_labels": "each transversal K4 contributes its four triangular faces",
            "cell_labels": "the base/shadow antipode pairs give the eight local tomotope cells",
            "boundary": "this identifies the 48 middle blocks; the full 2x2 flag fiber is inherited from the tomotope block model",
        },
        "checks": checks,
    }
    path = ROOT / "data" / "bt814_tomotope_middle_layer_from_residual_tetrahedra.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
