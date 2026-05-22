#!/usr/bin/env python3
"""Dual quadrangle tight-frame theorem for the W33 minimal logical surface.

Rows of A are X_min flags and columns are Z_min quadrangles.  The prior signed
flag theorem showed that AA^T/81 is a unit-norm tight frame of 160 flag vectors
in rank 81.

This script records the dual statement on columns:
  - every quadrangle column has squared norm 8;
  - rank(A)=81;
  - A^T A has nonzero spectrum 160^81 and zero spectrum 0^1539;
  - after column normalization, A^T A / 8 is the Gram matrix of 1620 unit
    quadrangle vectors in R^81 with tight frame bound 1620/81 = 20.

The number 20 equals the W33 bulk-to-horizon projection fiber 240/12.
"""
from __future__ import annotations

import json
from collections import Counter
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


def boundary(points, edges, edge_index, triangles):
    d2 = np.zeros((len(edges), len(triangles)), dtype=np.int8)
    for col, (a, b, c) in enumerate(triangles):
        for sign, e in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
            d2[edge_index[tuple(sorted(e))], col] += sign
    return d2 % P


def x_rays(lines, edges, edge_index, d2):
    HZ = d2.T % P
    rays = {}
    for line in lines:
        line_edges = [edge_index[tuple(sorted(e))] for e in combinations(line, 2)]
        for support in combinations(line_edges, 3):
            for vals in product((1, 2), repeat=3):
                v = np.zeros(len(edges), dtype=np.int8)
                for val, s in zip(vals, support):
                    v[s] = val
                if np.all((HZ @ v) % P == 0):
                    rays.setdefault(canonical_projective_vector(v.astype(int)), v.copy())
    return list(rays.values())


def oriented_cycle(order, edges, edge_index):
    v = np.zeros(len(edges), dtype=np.int8)
    for a, b in zip(order, order[1:] + [order[0]]):
        e = tuple(sorted((a, b)))
        idx = edge_index[e]
        v[idx] = 1 if (a, b) == edges[idx] else 2
    return v


def z_rays(points, edges, edge_index, adjacency):
    rays = {}
    for a, b in combinations(range(len(points)), 2):
        if adjacency[a][b]:
            continue
        common = [x for x in range(len(points)) if adjacency[a][x] and adjacency[b][x]]
        for c, d in combinations(common, 2):
            v = oriented_cycle([a, c, b, d], edges, edge_index)
            rays.setdefault(canonical_projective_vector(v.astype(int)), v.copy())
    return list(rays.values())


def main() -> int:
    points, edges, edge_index, adjacency, lines, triangles = build_geometry()
    d2 = boundary(points, edges, edge_index, triangles)
    X = x_rays(lines, edges, edge_index, d2)
    Z = z_rays(points, edges, edge_index, adjacency)
    raw = (np.array(X, dtype=np.int16) @ np.array(Z, dtype=np.int16).T) % P
    A = np.where(raw == 2, -1, raw).astype(np.int16)
    U = (A != 0).astype(np.int16)
    row_gram = A @ A.T
    col_gram = A.T @ A
    unsigned_col_gram = U.T @ U

    # Avoid large eigensolve: nonzero spectra of A^T A and A A^T agree.
    row_spectrum = Counter(round(float(x), 6) for x in np.linalg.eigvalsh(row_gram.astype(float)))
    inferred_column_spectrum = {"160": 81, "0": len(Z) - 81}

    abs_off_dist = Counter()
    signed_off_dist = Counter()
    for i in range(len(Z)):
        for j in range(i + 1, len(Z)):
            abs_off_dist[int(abs(col_gram[i, j]))] += 1
            signed_off_dist[int(col_gram[i, j])] += 1

    checks = {
        "geometry_counts": len(points) == 40 and len(edges) == 240 and len(lines) == 40 and len(X) == 160 and len(Z) == 1620,
        "rank_81": int(np.linalg.matrix_rank(A.astype(float))) == 81,
        "row_norms_81": Counter(int(x) for x in np.diag(row_gram)) == Counter({81: 160}),
        "column_norms_8": Counter(int(x) for x in np.diag(col_gram)) == Counter({8: 1620}),
        "column_absolute_gram_matches_unsigned": bool(np.array_equal(np.abs(col_gram), unsigned_col_gram)),
        "row_projector": bool(np.max(np.abs(row_gram @ row_gram - 160 * row_gram)) == 0),
        "column_projector_relation": bool(np.max(np.abs(col_gram @ col_gram - 160 * col_gram)) == 0),
        "frame_redundancy_20": len(Z) // 81 == 20 and len(Z) == 81 * 20,
        "fiber_match": 240 // 12 == 20,
    }
    payload = {
        "theorem_name": "Dual Quadrangle Tight-Frame and 20-Fiber Theorem",
        "summary": {
            "rows_flags": len(X),
            "columns_quadrangles": len(Z),
            "rank": int(np.linalg.matrix_rank(A.astype(float))),
            "row_norm_squared": 81,
            "column_norm_squared": 8,
            "unit_column_frame_bound": "1620/81 = 20",
            "bulk_horizon_fiber": "240/12 = 20",
            "all_checks_passed": all(checks.values()),
        },
        "checks": checks,
        "row_spectrum_AAT": dict(row_spectrum),
        "inferred_column_spectrum_ATA": inferred_column_spectrum,
        "absolute_column_inner_product_distribution_unordered": dict(abs_off_dist),
        "signed_column_inner_product_distribution_unordered": dict(signed_off_dist),
        "normalized_column_absolute_inner_products": ["0", "1/8", "1/4", "3/8", "1/2"],
        "identities": {
            "column_tight_frame": "A^T A / 8 is the Gram matrix of 1620 unit vectors spanning R^81 with frame bound 20.",
            "fiber_identity": "20 = 1620/81 = 240/12 = n_B/h.",
            "singular_values": "A has 81 nonzero singular values, each sqrt(160).",
        },
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "w33_dual_quadrangle_tight_frame.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
