#!/usr/bin/env python3
"""Signed flag tight-frame theorem for the W33 minimal logical surface.

Previous decoded layers:
  X_min = point-line flags of W(3,3)      (160)
  Z_min = ordinary quadrangles            (1620)
  U = unsigned flag-quadrangle incidence  (160 x 1620)
  A = signed F_3 phase matrix             (160 x 1620)

This script verifies that the signed Gram matrix S = A A^T is a signed lift of
the 3-adic flag association scheme:
  |S_ij| = (U U^T)_ij for all i,j.

The normalized rows of A have squared norm 81.  Thus their normalized inner
products are
  diagonal 1,
  off diagonal +/- 27/81 = +/- 1/3,
                 +/-  9/81 = +/- 1/9,
                 +/-  3/81 = +/- 1/27,
                 +/-  1/81.

Finally S^2 = 160 S, so S/160 is the exact rank-81 projector and S/81 is the
Gram matrix of a finite unit-norm tight frame of 160 vectors spanning an
81-dimensional real phase space, with frame bound 160/81.
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
    points: list[Vec] = []
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


def boundary_matrices(points, edges, edge_index, triangles):
    d1 = np.zeros((len(points), len(edges)), dtype=np.int8)
    for col, (i, j) in enumerate(edges):
        d1[i, col] = -1
        d1[j, col] = 1
    d1 %= P
    d2 = np.zeros((len(edges), len(triangles)), dtype=np.int8)
    for col, (a, b, c) in enumerate(triangles):
        for sign, e in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
            d2[edge_index[tuple(sorted(e))], col] += sign
    d2 %= P
    return d1, d2


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


def oriented_cycle_vector(order, edges, edge_index):
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
            v = oriented_cycle_vector([a, c, b, d], edges, edge_index)
            key = canonical_projective_vector(v.astype(int))
            rays.setdefault(key, v.copy())
    return list(rays.values())


def classify_flag_pair(f, g, lines, adjacency):
    p, li = f
    q, mj = g
    if f == g:
        return "same_flag"
    L = set(lines[li])
    M = set(lines[mj])
    if p == q:
        return "same_point"
    if li == mj:
        return "same_line"
    if q in L and p not in M:
        return "q_on_L_cross_incidence"
    if p in M and q not in L:
        return "p_on_M_cross_incidence"
    if L & M:
        return "lines_meet_elsewhere"
    if adjacency[p][q]:
        return "skew_lines_flag_points_collinear"
    return "skew_lines_flag_points_noncollinear"


def main() -> int:
    points, edges, edge_index, adjacency, lines, triangles = build_geometry()
    _, d2 = boundary_matrices(points, edges, edge_index, triangles)
    X, x_flags = x_rays(lines, edges, edge_index, d2)
    Z = z_rays(points, edges, edge_index, adjacency)
    raw = (np.array(X, dtype=np.int16) @ np.array(Z, dtype=np.int16).T) % P
    A = np.where(raw == 2, -1, raw).astype(np.int16)
    U = (A != 0).astype(np.int16)
    S = A @ A.T
    G = U @ U.T

    signed_entry_distribution = Counter(int(x) for x in S.flatten())
    off_signed_distribution = Counter(int(S[i, j]) for i in range(len(X)) for j in range(len(X)) if i != j)
    abs_off_distribution = Counter(abs(k) for k, v in off_signed_distribution.items() for _ in range(v))
    relation_signed = defaultdict(Counter)
    for i, f in enumerate(x_flags):
        for j, g in enumerate(x_flags):
            if i == j:
                continue
            relation_signed[classify_flag_pair(f, g, lines, adjacency)][int(S[i, j])] += 1

    eigenvals = Counter(round(float(x), 6) for x in np.linalg.eigvalsh(S.astype(float)))
    checks = {
        "geometry_counts": len(points) == 40 and len(edges) == 240 and len(lines) == 40 and len(X) == 160 and len(Z) == 1620,
        "absolute_signed_gram_equals_unsigned_gram": bool(np.array_equal(np.abs(S), G)),
        "signed_projector": bool(np.max(np.abs(S @ S - 160 * S)) == 0),
        "rank_81": int(np.linalg.matrix_rank(A.astype(float))) == 81,
        "row_norms_81": Counter(int(S[i, i]) for i in range(len(X))) == Counter({81: 160}),
        "off_absolute_values": set(abs(k) for k in off_signed_distribution) == {1, 3, 9, 27},
    }
    payload = {
        "theorem_name": "Signed 3-adic Flag Tight Frame Theorem",
        "summary": {
            "rows_flags": len(X),
            "columns_quadrangles": len(Z),
            "rank": int(np.linalg.matrix_rank(A.astype(float))),
            "row_norm_squared": 81,
            "projector_eigenvalue": 160,
            "frame_bound_normalized": "160/81",
            "normalized_off_diagonal_absolute_inner_products": ["1/3", "1/9", "1/27", "1/81"],
            "all_checks_passed": all(checks.values()),
        },
        "checks": checks,
        "signed_gram_entry_distribution_including_diagonal": dict(signed_entry_distribution),
        "signed_gram_off_diagonal_distribution": dict(off_signed_distribution),
        "absolute_off_diagonal_distribution": dict(abs_off_distribution),
        "signed_entries_by_flag_relation": {k: dict(v) for k, v in relation_signed.items()},
        "spectrum_S": dict(eigenvals),
        "identities": {
            "absolute_lift": "|A A^T| = U U^T entrywise",
            "projector": "S=A A^T satisfies S^2=160 S",
            "unit_norm_frame": "S/81 is the Gram matrix of 160 unit vectors in R^81 with frame bound 160/81",
            "adic_angles": "off-diagonal normalized absolute inner products are 3^-1, 3^-2, 3^-3, 3^-4",
        },
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "w33_signed_flag_tight_frame.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
