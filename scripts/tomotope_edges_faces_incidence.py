#!/usr/bin/env python3
"""Tomotope edges–faces incidence builder (towards explicit Reye mapping).

This script computes, from the 192-flag tomotope model:

  - The 12 edge orbits as flag orbits under <r0, r2, r3> (same as in
    `scripts/tomotope_edge_orbit_report.py`).
  - The 16 face (triangle) orbits as flag orbits under <r0, r1, r3>, i.e.
    keeping the rank-2 component fixed while varying vertex, edge, cell.
  - The 12×16 incidence matrix M where

        M[i][j] = 1  iff  some flag lies in both edge-orbit E_i and face-orbit F_j.

It writes all of this to `data/tomotope_edges_faces_incidence.json`.

This is the Tomotope side of the Tomotope–Reye correspondence; a separate
script can then align this matrix with a standard Reye 12₄16₃ incidence
matrix to obtain a concrete Tomotope→Reye bijection.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
BUNDLE_DIR = ROOT / "TOE_tomotope_flag_model_conjugacy_v01_20260228_bundle" / "TOE_tomotope_flag_model_conjugacy_v01_20260228"


def load_flag_adjacency() -> Dict[str, List[int]]:
    path = BUNDLE_DIR / "flag_adjacency_r0_r3_permutations.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    result: Dict[str, List[int]] = {}
    for key in ["r0", "r1", "r2", "r3"]:
        perm = data[key]
        result[key] = [int(x) for x in perm]
    return result


def orbit_under(start: int, generators: List[List[int]]) -> List[int]:
    O = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for g in generators:
            v = g[u]
            if v not in O:
                O.add(v)
                stack.append(v)
    return sorted(O)


def compute_edge_orbits(flag_adj: Dict[str, List[int]]) -> List[List[int]]:
    r0, r2, r3 = flag_adj["r0"], flag_adj["r2"], flag_adj["r3"]
    edges: List[List[int]] = []
    visited: set[int] = set()
    for f in range(192):
        if f in visited:
            continue
        orb = orbit_under(f, [r0, r2, r3])
        visited.update(orb)
        edges.append(orb)
    return edges


def compute_face_orbits(flag_adj: Dict[str, List[int]]) -> List[List[int]]:
    # Faces (triangles) are rank-2 objects, so we keep r2 fixed and
    # move within the fibre using r0, r1, r3.
    r0, r1, r3 = flag_adj["r0"], flag_adj["r1"], flag_adj["r3"]
    faces: List[List[int]] = []
    visited: set[int] = set()
    for f in range(192):
        if f in visited:
            continue
        orb = orbit_under(f, [r0, r1, r3])
        visited.update(orb)
        faces.append(orb)
    return faces


def build_incidence(edges: List[List[int]], faces: List[List[int]]) -> List[List[int]]:
    # Precompute sets for speed
    edge_sets = [set(e) for e in edges]
    face_sets = [set(f) for f in faces]
    M: List[List[int]] = []
    for e_set in edge_sets:
        row: List[int] = []
        for f_set in face_sets:
            row.append(1 if e_set & f_set else 0)
        M.append(row)
    return M


def main() -> None:
    flag_adj = load_flag_adjacency()
    edges = compute_edge_orbits(flag_adj)
    faces = compute_face_orbits(flag_adj)

    edge_sizes = Counter(len(e) for e in edges)
    face_sizes = Counter(len(f) for f in faces)

    M = build_incidence(edges, faces)

    out = {
        "edge_orbits": edges,
        "face_orbits": faces,
        "edge_orbit_sizes": dict(edge_sizes),
        "face_orbit_sizes": dict(face_sizes),
        "edge_count": len(edges),
        "face_count": len(faces),
        "incidence": M,
        "note": (
            "M[i][j] = 1 iff there exists a flag belonging to edge-orbit i and face-orbit j. "
            "Row sums should all be 4, column sums all 3, giving a (12_4 16_3) configuration."
        ),
    }

    DATA_DIR.mkdir(exist_ok=True)
    out_path = DATA_DIR / "tomotope_edges_faces_incidence.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print("Tomotope edges/faces incidence written to", out_path)
    print("Edge count:", len(edges), "sizes:", edge_sizes)
    print("Face count:", len(faces), "sizes", face_sizes)


if __name__ == "__main__":
    main()
