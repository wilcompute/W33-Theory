#!/usr/bin/env python3
r"""Geometric support theorem for the minimal logical W(3,3) CSS surface.

This script reconstructs W(3,3) as the symplectic polar space over F_3,
constructs the canonical edge/triangle chain complex used by the W33 CSS
experiments, and proves by enumeration that the previously discovered minimal
logical surface has a simple finite-geometric support model:

  X_min projective supports = isotropic line-stars.
      For every isotropic line L ~= K_4 and every point p in L, take the three
      W33 graph edges from p to L\{p}.  There are 40*4 = 160 such supports.

  Z_min projective supports = ordinary quadrangles.
      For every noncollinear point pair {a,b}, choose two of the four common
      neighbours and take the 4-cycle a-c-b-d-a.  The count is
      (number of nonedges)*C(4,2)/2 = 540*6/2 = 1620.

The signed projective pairing matrix built from the actual F_3 coefficients then
reproduces the earlier invariants:
  - support biregularity 160*81 = 1620*8 = 12960;
  - unsigned X-overlaps 1,3,9,27 with per-row counts 81,54,18,6;
  - signed phase-frame spectrum 160^81 + 0^79.
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

import numpy as np

P = 3
Vec = tuple[int, int, int, int]


def canonical(v: Iterable[int]) -> Vec:
    vv = tuple(int(x) % P for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector has no projective representative")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError("unreachable")


def omega(u: Vec, v: Vec) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % P


def canonical_projective_vector(v: np.ndarray) -> tuple[int, ...]:
    a = tuple(int(x) for x in v.tolist())
    b = tuple(int(x) for x in (2 * v % P).tolist())
    return min(a, b)


def build_w33():
    points: list[Vec] = []
    seen: set[Vec] = set()
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

    lines: set[tuple[int, int, int, int]] = set()
    for i, j in edges:
        u, v = points[i], points[j]
        line = set()
        for a, b in product(range(P), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(point_index[canonical((a * u[t] + b * v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines = sorted(lines)

    # The chain complex uses the 160 oriented triangles lying inside the 40 K_4 lines.
    triangles = sorted({tuple(sorted(t)) for line in lines for t in combinations(line, 3)})
    return points, edges, edge_index, adjacency, lines, triangles


def boundary_matrices(points, edges, edge_index, triangles):
    d1 = np.zeros((len(points), len(edges)), dtype=np.int8)
    for col, (i, j) in enumerate(edges):
        d1[i, col] = -1
        d1[j, col] = 1
    d1 %= P

    d2 = np.zeros((len(edges), len(triangles)), dtype=np.int8)
    for col, (a, b, c) in enumerate(triangles):
        # Oriented boundary of the 2-simplex (a,b,c), in global sorted-edge basis.
        for sign, e in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
            d2[edge_index[tuple(sorted(e))], col] += sign
    d2 %= P
    return d1, d2


def x_min_line_star_rays(lines, edges, edge_index, d2):
    """Return projective X rays satisfying d2^T x = 0, supported in K4 line triples."""
    HZ = d2.T % P
    rays: dict[tuple[int, ...], np.ndarray] = {}
    support_to_local_type: dict[tuple[int, ...], str] = {}

    for line in lines:
        line_edges = [edge_index[tuple(sorted(e))] for e in combinations(line, 2)]
        for support in combinations(line_edges, 3):
            for vals in product((1, 2), repeat=3):
                v = np.zeros(len(edges), dtype=np.int8)
                for val, s in zip(vals, support):
                    v[s] = val
                if np.all((HZ @ v) % P == 0):
                    key = canonical_projective_vector(v.astype(int))
                    rays.setdefault(key, v.copy())
                    support_to_local_type[tuple(sorted(support))] = classify_edge_triple(support, edges)
    return list(rays.values()), support_to_local_type


def classify_edge_triple(support, edges) -> str:
    vertices: list[int] = []
    for e in support:
        vertices.extend(edges[e])
    degrees = sorted(Counter(vertices).values(), reverse=True)
    if degrees == [3, 1, 1, 1]:
        return "line-star"
    if degrees == [2, 2, 2]:
        return "line-triangle"
    return f"other:{degrees}"


def oriented_cycle_vector(order, edges, edge_index) -> np.ndarray:
    v = np.zeros(len(edges), dtype=np.int8)
    for a, b in zip(order, order[1:] + [order[0]]):
        e = tuple(sorted((a, b)))
        idx = edge_index[e]
        sign = 1 if (a, b) == edges[idx] else 2
        v[idx] = sign
    return v


def z_min_quadrangle_rays(points, edges, edge_index, adjacency):
    rays: dict[tuple[int, ...], np.ndarray] = {}
    supports: set[tuple[int, int, int, int]] = set()
    for a, b in combinations(range(len(points)), 2):
        if adjacency[a][b]:
            continue
        common = [x for x in range(len(points)) if adjacency[a][x] and adjacency[b][x]]
        for c, d in combinations(common, 2):
            support = tuple(sorted(edge_index[tuple(sorted(e))] for e in ((a, c), (c, b), (b, d), (d, a))))
            if support in supports:
                continue
            supports.add(support)
            v = oriented_cycle_vector([a, c, b, d], edges, edge_index)
            rays.setdefault(canonical_projective_vector(v.astype(int)), v.copy())
    return list(rays.values())


def srg_parameters(adjacency):
    n = len(adjacency)
    degrees = Counter(sum(row) for row in adjacency)
    lambdas = []
    mus = []
    for i, j in combinations(range(n), 2):
        common = sum(adjacency[i][k] and adjacency[j][k] for k in range(n))
        if adjacency[i][j]:
            lambdas.append(common)
        else:
            mus.append(common)
    return degrees, Counter(lambdas), Counter(mus)


def payload():
    points, edges, edge_index, adjacency, lines, triangles = build_w33()
    d1, d2 = boundary_matrices(points, edges, edge_index, triangles)
    X, x_support_types = x_min_line_star_rays(lines, edges, edge_index, d2)
    Z = z_min_quadrangle_rays(points, edges, edge_index, adjacency)

    X_supports = [frozenset(np.nonzero(x)[0].tolist()) for x in X]
    Z_supports = [frozenset(np.nonzero(z)[0].tolist()) for z in Z]
    A_raw = (np.array(X, dtype=np.int16) @ np.array(Z, dtype=np.int16).T) % P
    U = (A_raw != 0).astype(np.int16)
    G = U @ U.T
    A_signed = np.where(A_raw == 2, -1, A_raw).astype(np.int16)
    S = A_signed @ A_signed.T

    degrees, lambdas, mus = srg_parameters(adjacency)
    off = Counter(int(x) for x in G[np.triu_indices(G.shape[0], 1)].tolist())
    row_dist = Counter(
        tuple(sorted((int(k), int(v)) for k, v in Counter(int(G[i, j]) for j in range(len(X)) if j != i).items()))
        for i in range(len(X))
    )
    signed_eigs = Counter(round(float(v), 6) for v in np.linalg.eigvalsh(S.astype(float)))

    result = {
        "theorem_name": "Minimal Support Geometry Theorem",
        "summary": {
            "points": len(points),
            "lines": len(lines),
            "edges": len(edges),
            "triangular_2_cells": len(triangles),
            "X_min_projective_rays": len(X),
            "Z_min_projective_rays": len(Z),
            "X_support_model": "isotropic line-stars: choose an isotropic K4 line and one incident point; take the three line-edges through that point",
            "Z_support_model": "ordinary quadrangles: induced 4-cycles determined by a noncollinear diagonal pair and two of its four common neighbours",
        },
        "srg_checks": {
            "degree_distribution": dict(degrees),
            "lambda_distribution": dict(lambdas),
            "mu_distribution": dict(mus),
        },
        "support_counts": {
            "X_unique_supports": len(set(X_supports)),
            "Z_unique_supports": len(set(Z_supports)),
            "X_support_type_distribution": dict(Counter(x_support_types.values())),
            "ordinary_quadrangle_count_formula": "nonedges*C(mu,2)/2 = 540*6/2 = 1620",
        },
        "pairing_checks": {
            "phase_distribution_projective": {str(int(k)): int(v) for k, v in Counter(A_raw.flatten().tolist()).items()},
            "support_biregularity_X_degree_distribution": {str(int(k)): int(v) for k, v in Counter(np.diag(G).tolist()).items()},
            "support_biregularity_Z_degree_distribution": {str(int(k)): int(v) for k, v in Counter(U.sum(axis=0).tolist()).items()},
            "support_incidence_total": int(U.sum()),
            "support_incidence_identity": "160*81 = 1620*8 = 12960",
        },
        "overlap_scheme": {
            "off_diagonal_distribution": {str(k): int(v) for k, v in sorted(off.items())},
            "per_row_distribution": {str(k): int(v) for k, v in row_dist.items()},
            "expected_per_row": {"1": 81, "3": 54, "9": 18, "27": 6},
        },
        "signed_phase_frame": {
            "rank": int(np.linalg.matrix_rank(A_signed.astype(float))),
            "eigenvalue_distribution": {str(k): int(v) for k, v in signed_eigs.items()},
            "idempotent_relation_holds": bool(np.max(np.abs(S @ S - 160 * S)) == 0),
            "relation": "S = A A^T satisfies S^2 = 160 S, hence A A^T / 160 is an exact rank-81 projector.",
        },
    }
    checks = {
        "w33_size": len(points) == 40 and len(edges) == 240 and len(lines) == 40,
        "srg": degrees == Counter({12: 40}) and lambdas == Counter({2: 240}) and mus == Counter({4: 540}),
        "x_count": len(X) == len(set(X_supports)) == 160,
        "z_count": len(Z) == len(set(Z_supports)) == 1620,
        "x_supports_are_line_stars": Counter(x_support_types.values()) == Counter({"line-star": 160}),
        "biregular": Counter(np.diag(G).tolist()) == Counter({81: 160}) and Counter(U.sum(axis=0).tolist()) == Counter({8: 1620}) and int(U.sum()) == 12960,
        "overlap_scheme": off == Counter({1: 6480, 3: 4320, 9: 1440, 27: 480}),
        "signed_rank_projector": int(np.linalg.matrix_rank(A_signed.astype(float))) == 81 and bool(np.max(np.abs(S @ S - 160 * S)) == 0),
    }
    result["checks"] = checks
    result["all_checks_passed"] = all(checks.values())
    return result


def main() -> int:
    result = payload()
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "w33_minimal_support_geometry.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"all_checks_passed": result["all_checks_passed"], **result["summary"]}, indent=2))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
