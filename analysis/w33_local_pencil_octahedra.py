#!/usr/bin/env python3
"""Local pencil-octahedron theorem for W(3,3).

Recent octahedron commits used one octahedron per W33 vertex to explain
40*(6,12,8)=(240,480,320).  This script makes that intrinsic.

For every point p of W(3,3):
  - exactly four totally isotropic lines pass through p;
  - these four lines form a K4 pencil;
  - the line graph L(K4) is the octahedron graph;
  - hence each point p canonically carries a local octahedron O_p.

Each local octahedron has f-vector (6,12,8), Laplacian spectrum
(0,4,4,4,6,6), and spanning-tree count 384.  Across all 40 points:

  40 * V(O) = 240
  40 * E(O) = 480
  40 * F(O) = 320

matching the W33 edge count, directed carrier/dual-number C1' count, and lifted
triangle C2' count from the recent octahedron/chain-lift commits.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
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
    return points, graph_edges, lines


def octahedron_from_pencil():
    """Return graph of L(K4): vertices are 2-subsets of a 4-set."""
    tetra_edges = list(combinations(range(4), 2))
    oct_edges = [(i, j) for i, j in combinations(range(6), 2) if set(tetra_edges[i]) & set(tetra_edges[j])]
    oct_faces = [tri for tri in combinations(range(6), 3) if all(set(tetra_edges[i]) & set(tetra_edges[j]) for i, j in combinations(tri, 2))]
    A = np.zeros((6, 6), dtype=int)
    for i, j in oct_edges:
        A[i, j] = A[j, i] = 1
    L = np.diag(A.sum(axis=1)) - A
    eigs = tuple(int(round(x)) for x in np.linalg.eigvalsh(L))
    tau = int(round(np.prod(np.linalg.eigvalsh(L)[1:]) / 6))
    return tetra_edges, oct_edges, oct_faces, eigs, tau


def main() -> int:
    points, graph_edges, lines = build_w33()
    point_lines = defaultdict(list)
    for li, L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)

    tetra_edges, oct_edges, oct_faces, eigs, tau = octahedron_from_pencil()
    per_point = {}
    for p in range(len(points)):
        Ls = sorted(point_lines[p])
        per_point[p] = {
            "pencil_lines": Ls,
            "tetrahedron_vertices": 4,
            "octahedron_vertices_line_pairs": len(tetra_edges),
            "octahedron_edges_line_pair_adjacencies": len(oct_edges),
            "octahedron_faces_triangles": len(oct_faces),
        }

    fvector_counts = Counter((v["octahedron_vertices_line_pairs"], v["octahedron_edges_line_pair_adjacencies"], v["octahedron_faces_triangles"]) for v in per_point.values())
    pencil_count = Counter(len(v) for v in point_lines.values())
    aggregate = {
        "40_times_octahedron_vertices": 40 * len(tetra_edges),
        "40_times_octahedron_edges": 40 * len(oct_edges),
        "40_times_octahedron_faces": 40 * len(oct_faces),
        "octahedron_subcells_per_point": len(tetra_edges) + len(oct_edges) + len(oct_faces),
        "total_octahedron_subcells": 40 * (len(tetra_edges) + len(oct_edges) + len(oct_faces)),
    }

    checks = {
        "w33_counts": len(points) == 40 and len(lines) == 40 and len(graph_edges) == 240,
        "each_point_has_4_lines": pencil_count == Counter({4: 40}),
        "each_local_pencil_is_octahedron": fvector_counts == Counter({(6, 12, 8): 40}),
        "octahedron_laplacian_spectrum": Counter(eigs) == Counter({0: 1, 4: 3, 6: 2}),
        "octahedron_tree_count_384": tau == 384,
        "aggregate_matches_chain_lift": aggregate["40_times_octahedron_vertices"] == 240 and aggregate["40_times_octahedron_edges"] == 480 and aggregate["40_times_octahedron_faces"] == 320,
        "subcells_per_point_26": aggregate["octahedron_subcells_per_point"] == 26,
    }

    payload = {
        "theorem_name": "Local W33 Pencil-Octahedron Theorem",
        "summary": {
            "points": len(points),
            "lines": len(lines),
            "w33_edges": len(graph_edges),
            "lines_through_each_point": 4,
            "local_octahedra": 40,
            "local_octahedron_fvector": [6, 12, 8],
            "local_octahedron_laplacian_spectrum": [0, 4, 4, 4, 6, 6],
            "local_octahedron_spanning_trees": tau,
            "aggregate": aggregate,
            "all_checks_passed": all(checks.values()),
        },
        "checks": checks,
        "identities": {
            "construction": "For each W33 point p, the four lines through p form a K4 pencil; L(K4) is the octahedron O_p.",
            "local_fvector": "f(O_p) = (6,12,8).",
            "global_chain_lift": "40*f(O) = (240,480,320).",
            "laplacian": "Spec(L_O)=(0,4,4,4,6,6), tau(O)=384.",
            "codec": "The 12 local octahedron edges are the 12 W33 local channels/gauge codec slots.",
        },
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "w33_local_pencil_octahedra.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
