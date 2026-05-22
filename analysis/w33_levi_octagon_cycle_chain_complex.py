#!/usr/bin/env python3
"""Levi octagon cycle-chain theorem for the W33 signed phase matrix.

The signed flag-quadrangle matrix A is best understood as a cycle-incidence
matrix for the Levi graph of W(3,3):

  C1 = R^{Flags}       dimension 160  (Levi edges)
  C0 = R^{Points+Lines} dimension 80  (Levi vertices)

The signed point/line relation matrix R from the nullspace theorem is an oriented
incidence matrix for the Levi graph.  Its transpose is the boundary operator

  partial : C1 -> C0.

Every ordinary quadrangle of the collinearity graph gives an 8-cycle in the Levi
graph.  The corresponding signed column of A is exactly a cycle vector.  The
certificate verifies:

  partial A = 0,
  rank(partial) = 79,
  dim ker(partial) = 160 - 79 = 81,
  rank(A) = 81,

hence

  im(A) = ker(partial) = H_1(Levi graph).

Thus the quadrangle columns generate the full Levi cycle space as a tight frame.
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


def canonical_projective_vector(v: np.ndarray) -> tuple[int, ...]:
    a = tuple(int(x) for x in v.tolist())
    b = tuple(int(x) for x in (2 * v % P).tolist())
    return min(a, b)


def build_geometry():
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
    edges = [(i, j) for i, j in combinations(range(len(points)), 2) if omega(points[i], points[j]) == 0]
    edge_index = {e: k for k, e in enumerate(edges)}
    adjacency = [[False] * len(points) for _ in points]
    for i, j in edges:
        adjacency[i][j] = adjacency[j][i] = True
    lines = set()
    for i, j in edges:
        u, v = points[i], points[j]
        line = set()
        for a, b in product(range(P), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(point_index[canonical((a * u[t] + b * v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines = sorted(lines)
    triangles = sorted({tuple(sorted(t)) for L in lines for t in combinations(L, 3)})
    return points, edges, edge_index, adjacency, lines, triangles


def triangle_boundary(edges, edge_index, triangles):
    d2 = np.zeros((len(edges), len(triangles)), dtype=np.int8)
    for col, (a, b, c) in enumerate(triangles):
        for sign, e in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
            d2[edge_index[tuple(sorted(e))], col] += sign
    return d2 % P


def x_rays(lines, edges, edge_index, d2):
    HZ = d2.T % P
    rays = {}
    flags = {}
    for li, line in enumerate(lines):
        line_edges = [edge_index[tuple(sorted(e))] for e in combinations(line, 2)]
        for support in combinations(line_edges, 3):
            for vals in product((1, 2), repeat=3):
                v = np.zeros(len(edges), dtype=np.int8)
                for val, s in zip(vals, support):
                    v[s] = val
                if np.all((HZ @ v) % P == 0):
                    key = canonical_projective_vector(v.astype(int))
                    if key not in rays:
                        cnt = Counter()
                        for s in support:
                            cnt.update(edges[s])
                        center = [p for p, c in cnt.items() if c == 3][0]
                        rays[key] = v.copy()
                        flags[key] = (center, li)
    ordered = sorted(rays.items(), key=lambda kv: flags[kv[0]])
    return [v for _, v in ordered], [flags[k] for k, _ in ordered]


def oriented_cycle(order, edges, edge_index):
    v = np.zeros(len(edges), dtype=np.int8)
    for a, b in zip(order, order[1:] + [order[0]]):
        e = tuple(sorted((a, b)))
        idx = edge_index[e]
        v[idx] = 1 if (a, b) == edges[idx] else 2
    return v


def z_rays(points, edges, edge_index, adjacency):
    rays = {}
    quad_vertices = {}
    for a, b in combinations(range(len(points)), 2):
        if adjacency[a][b]:
            continue
        common = [x for x in range(len(points)) if adjacency[a][x] and adjacency[b][x]]
        for c, d in combinations(common, 2):
            v = oriented_cycle([a, c, b, d], edges, edge_index)
            key = canonical_projective_vector(v.astype(int))
            if key not in rays:
                rays[key] = v.copy()
                quad_vertices[key] = tuple(sorted((a, b, c, d)))
    ordered = sorted(rays.items(), key=lambda kv: quad_vertices[kv[0]])
    return [v for _, v in ordered], [quad_vertices[k] for k, _ in ordered]


def signed_relation_boundary(A, x_flags, n_points=40, n_lines=40):
    """Return partial = R^T, where R has one signed local relation per Levi vertex."""
    point_flags = defaultdict(list)
    line_flags = defaultdict(list)
    for i, (p, L) in enumerate(x_flags):
        point_flags[p].append(i)
        line_flags[L].append(i)
    R = np.zeros((len(x_flags), n_points + n_lines), dtype=np.int16)
    for p, idxs in point_flags.items():
        for signs in product((1, -1), repeat=4):
            if np.all(sum(signs[k] * A[idxs[k], :] for k in range(4)) == 0):
                for s, row in zip(signs, idxs):
                    R[row, p] = s
                break
    for L, idxs in line_flags.items():
        for signs in product((1, -1), repeat=4):
            if np.all(sum(signs[k] * A[idxs[k], :] for k in range(4)) == 0):
                for s, row in zip(signs, idxs):
                    R[row, n_points + L] = s
                break
    return R.T


def main() -> int:
    points, graph_edges, edge_index, adjacency, lines, triangles = build_geometry()
    d2 = triangle_boundary(graph_edges, edge_index, triangles)
    X, x_flags = x_rays(lines, graph_edges, edge_index, d2)
    Z, quad_vertices = z_rays(points, graph_edges, edge_index, adjacency)
    raw = (np.array(X, dtype=np.int16) @ np.array(Z, dtype=np.int16).T) % P
    A = np.where(raw == 2, -1, raw).astype(np.int16)
    partial = signed_relation_boundary(A, x_flags)

    rank_partial = int(np.linalg.matrix_rank(partial.astype(float)))
    rank_A = int(np.linalg.matrix_rank(A.astype(float)))
    kernel_dim = A.shape[0] - rank_partial
    column_weights = Counter(int(np.count_nonzero(A[:, j])) for j in range(A.shape[1]))
    boundary_column_norms = Counter(int(x) for x in np.sum((partial @ A) ** 2, axis=0))

    S_row = A @ A.T
    S_col = A.T @ A

    checks = {
        "geometry_counts": len(points) == 40 and len(lines) == 40 and len(x_flags) == 160 and len(Z) == 1620,
        "quadrangle_columns_are_octagons": column_weights == Counter({8: 1620}),
        "boundary_zero": bool(np.max(np.abs(partial @ A)) == 0),
        "boundary_column_norms_zero": boundary_column_norms == Counter({0: 1620}),
        "rank_partial_79": rank_partial == 79,
        "kernel_dim_81": kernel_dim == 81,
        "rank_A_81": rank_A == 81,
        "image_equals_cycle_space_by_rank": rank_A == kernel_dim,
        "row_projector": bool(np.max(np.abs(S_row @ S_row - 160 * S_row)) == 0),
        "column_projector": bool(np.max(np.abs(S_col @ S_col - 160 * S_col)) == 0),
    }

    payload = {
        "theorem_name": "Levi Octagon Cycle-Chain Theorem",
        "summary": {
            "levi_vertices": 80,
            "levi_edges_flags": A.shape[0],
            "quadrangle_octagon_columns": A.shape[1],
            "column_weight": 8,
            "rank_boundary_partial": rank_partial,
            "cycle_space_dimension": kernel_dim,
            "rank_A": rank_A,
            "all_checks_passed": all(checks.values()),
        },
        "checks": checks,
        "column_weight_distribution": dict(column_weights),
        "boundary_column_norm_distribution": dict(boundary_column_norms),
        "exact_sequence": "R^Quadrangles_1620 --A--> C1(Levi)_160 --partial--> C0(Levi)_80, with im(A)=ker(partial)",
        "identities": {
            "octagon": "Each ordinary quadrangle of W33 becomes an 8-cycle in the Levi graph.",
            "cycle_generation": "partial A = 0 and rank(A)=dim ker(partial)=81, hence im(A)=ker(partial).",
            "tight_frame": "The 1620 Levi octagons form a tight frame for the 81-dimensional Levi cycle space.",
            "interpretation": "The signed phase matrix is the oriented edge-cycle incidence matrix of the W33 Levi graph's ordinary quadrangle octagons.",
        },
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "w33_levi_octagon_cycle_chain_complex.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
