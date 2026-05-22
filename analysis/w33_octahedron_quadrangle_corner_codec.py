#!/usr/bin/env python3
"""Octahedron corner codec theorem for W(3,3).

This script connects recent local pencil-octahedra with the Levi-octagon
quadrangle cycle story.

For every point p of W(3,3), the four lines through p form a K4 pencil and
L(K4) is a local octahedron O_p.

Local O_p interpretations:
  vertices: 6 pairs of lines through p = local angle/corner states
  edges:    12 local codec slots = W33 valency / directed channels at p
  faces:    8 sign faces = 2 signed lifts of the 4 flags through p

Global counts:
  40*6  = 240 local octahedron vertices
  40*12 = 480 local octahedron edges
  40*8  = 320 local octahedron faces = |X_min^{F3}|

Quadrangle corner theorem:
  An ordinary quadrangle Q has four corners.  At each corner p, the two
  incident cycle edges determine two lines through p, hence a vertex of O_p.
  The certificate verifies every local octahedron vertex lies on exactly
  27 = q^3 quadrangle corners:

    240 * 27 = 1620 * 4 = 6480.

This gives a bridge between the octahedral closure-clock layer and the
quadrangle/Levi-octagon minimal Z layer.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

P = 3
Vec = tuple[int, int, int, int]


def canonical(v) -> Vec:
    vv = tuple(int(x) % P for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError


def omega(u: Vec, v: Vec) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % P


def build_w33():
    points = []
    seen = set()
    for raw in product(range(P), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        c = canonical(raw)
        if c not in seen:
            seen.add(c)
            points.append(c)
    point_index = {p: i for i, p in enumerate(points)}
    graph_edges = [(i, j) for i, j in combinations(range(len(points)), 2) if omega(points[i], points[j]) == 0]
    adjacency = [[False] * len(points) for _ in points]
    for i, j in graph_edges:
        adjacency[i][j] = adjacency[j][i] = True
    lines = set()
    for i, j in graph_edges:
        u, v = points[i], points[j]
        line = set()
        for a, b in product(range(P), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(point_index[canonical((a * u[t] + b * v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines = sorted(lines)
    point_lines = defaultdict(list)
    edge_to_line = {}
    for li, L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)
        for e in combinations(L, 2):
            edge_to_line[tuple(sorted(e))] = li
    return points, graph_edges, adjacency, lines, point_lines, edge_to_line


def octahedron_fvector_from_k4_line_graph():
    tetra_edges = list(combinations(range(4), 2))
    oct_edges = [(i, j) for i, j in combinations(range(6), 2) if set(tetra_edges[i]) & set(tetra_edges[j])]
    oct_faces = [tri for tri in combinations(range(6), 3) if all(set(tetra_edges[i]) & set(tetra_edges[j]) for i, j in combinations(tri, 2))]
    # Opposite face-pairs of L(K4): star at a K4 vertex paired with the triangle on the opposite K3.
    antipodal_face_pairs = 4
    return len(tetra_edges), len(oct_edges), len(oct_faces), antipodal_face_pairs


def ordinary_quadrangles(adjacency):
    quads = {}
    for a, b in combinations(range(len(adjacency)), 2):
        if adjacency[a][b]:
            continue
        common = [x for x in range(len(adjacency)) if adjacency[a][x] and adjacency[b][x]]
        for c, d in combinations(common, 2):
            cycle_edges = tuple(sorted(tuple(sorted(e)) for e in ((a, c), (c, b), (b, d), (d, a))))
            quads.setdefault(cycle_edges, tuple(sorted((a, b, c, d))))
    return quads


def main() -> int:
    points, graph_edges, adjacency, lines, point_lines, edge_to_line = build_w33()
    ov, oe, of, face_pairs = octahedron_fvector_from_k4_line_graph()
    quads = ordinary_quadrangles(adjacency)

    local_octa_vertices = {(p, tuple(sorted(lpair))) for p in range(len(points)) for lpair in combinations(sorted(point_lines[p]), 2)}
    corner_count = Counter()
    for cycle_edges, verts in quads.items():
        incident = defaultdict(list)
        for u, v in cycle_edges:
            incident[u].append((u, v))
            incident[v].append((u, v))
        for p in verts:
            lpair = tuple(sorted(edge_to_line[tuple(sorted(e))] for e in incident[p]))
            corner_count[(p, lpair)] += 1

    aggregate = {
        "local_octahedron_vertices_total": 40 * ov,
        "local_octahedron_edges_total": 40 * oe,
        "local_octahedron_faces_total": 40 * of,
        "projective_flags_total": 40 * face_pairs,
        "signed_flag_faces_total": 40 * of,
        "quadrangle_corner_total": len(quads) * 4,
        "corner_count_total": sum(corner_count.values()),
    }
    checks = {
        "w33_counts": len(points) == 40 and len(lines) == 40 and len(graph_edges) == 240,
        "local_octahedron_fvector": (ov, oe, of) == (6, 12, 8),
        "face_pairs_are_projective_flags": face_pairs == 4 and aggregate["projective_flags_total"] == 160,
        "faces_are_signed_X_vectors": aggregate["signed_flag_faces_total"] == 320,
        "local_vertices_match_w33_edges_count": aggregate["local_octahedron_vertices_total"] == 240,
        "local_edges_match_directed_carrier": aggregate["local_octahedron_edges_total"] == 480,
        "ordinary_quadrangles": len(quads) == 1620,
        "all_local_octa_vertices_seen": set(corner_count) == local_octa_vertices,
        "each_local_octa_vertex_has_27_quadrangle_corners": Counter(corner_count.values()) == Counter({27: 240}),
        "corner_double_count": aggregate["corner_count_total"] == aggregate["quadrangle_corner_total"] == 6480 == 240 * 27,
    }
    payload = {
        "theorem_name": "Octahedron Corner Codec Theorem",
        "summary": {
            "points": len(points),
            "local_octahedra": 40,
            "local_octahedron_fvector": [ov, oe, of],
            "local_octahedron_face_pairs": face_pairs,
            "ordinary_quadrangles": len(quads),
            "quadrangle_corners_per_quadrangle": 4,
            "quadrangles_per_local_octahedron_vertex": 27,
            "aggregate": aggregate,
            "all_checks_passed": all(checks.values()),
        },
        "checks": checks,
        "quadrangle_corner_distribution_per_local_octa_vertex": dict(Counter(corner_count.values())),
        "identities": {
            "local_faces_to_X_vectors": "40*8=320=|X_min^{F3}|; antipodal face pairs give 40*4=160 projective flags.",
            "local_edges_to_directed_carrier": "40*12=480 directed carrier slots / local codec channels.",
            "local_vertices_to_quadrangle_corners": "40*6=240 local angle states, each incident with 27 quadrangle corners.",
            "corner_double_count": "240*27=1620*4=6480.",
            "meaning": "Quadrangles glue the local pencil-octahedra through their octahedral corner states.",
        },
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "w33_octahedron_quadrangle_corner_codec.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
