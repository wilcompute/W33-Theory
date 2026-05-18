#!/usr/bin/env python3
"""Dual visibility scheme for minimal logical rays in the W(3,3) edge CSS code.

The prior 3-adic overlap theorem studied the X-side Gram matrix

    U U^T,    U in {0,1}^{160 x 1620},

where U[x,z]=1 iff minimal X-ray x and minimal Z-ray z pair nontrivially.

This file computes the dual Z-side Gram matrix

    U^T U.

Exact result:

    column degree: 8
    pairwise Z-ray visibility overlaps: 0,1,2,3,4
    per Z-ray distribution:
        0^{1187}, 1^{288}, 2^{96}, 3^{32}, 4^{16}

Thus each minimal Z-ray shares at least one visible X-ray with exactly

    288 + 96 + 32 + 16 = 432 = 16 * 27

other minimal Z-rays.  Here 16 = 2^4 is the square of the tomotope cell
count's half-shell, and 27=q^q is the E6/cubic-surface count.

The X-side and Z-side schemes are dual:

    X rows: degree 81, overlaps 1,3,9,27 with per-row counts 81,54,18,6.
    Z cols: degree 8, overlaps 0,1,2,3,4 with per-col counts 1187,288,96,32,16.

Both are shadows of the same signed phase projector A A^T / 160 of rank 81.
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

import numpy as np

P = 3
Q = 3
V = 40
E = 240
MU = 4
H1 = Q ** (Q + 1)
Q_CUBED = Q ** Q
WE6 = 51_840

Vec = tuple[int, int, int, int]


def canonical(v: Iterable[int]) -> Vec:
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


def rref(M: np.ndarray, p: int = P) -> tuple[np.ndarray, list[int]]:
    A = np.array(M, dtype=int) % p
    m, n = A.shape
    rank = 0
    pivots: list[int] = []
    for col in range(n):
        pivot = None
        for row in range(rank, m):
            if A[row, col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        if pivot != rank:
            A[[rank, pivot]] = A[[pivot, rank]]
        inv = pow(int(A[rank, col]), -1, p)
        A[rank] = (A[rank] * inv) % p
        for row in range(m):
            if row != rank and A[row, col] % p:
                A[row] = (A[row] - A[row, col] * A[rank]) % p
        pivots.append(col)
        rank += 1
        if rank == m:
            break
    return A, pivots


def gf_rank(M: np.ndarray, p: int = P) -> int:
    return len(rref(M, p)[1])


def in_rowspace(v: np.ndarray, rows: np.ndarray, p: int = P) -> bool:
    return gf_rank(np.vstack([rows % p, v.reshape(1, -1) % p]), p) == gf_rank(rows, p)


def vector_canonical_projective(v: np.ndarray) -> tuple[int, ...]:
    t1 = tuple(v.tolist())
    t2 = tuple((2 * v % P).tolist())
    return min(t1, t2)


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
    triangles = sorted({tuple(sorted(t)) for line in lines for t in combinations(line, 3)})
    return points, edges, edge_index, adjacency, lines, triangles


def boundary_matrices(points, edges, edge_index, triangles):
    d1 = np.zeros((len(points), len(edges)), dtype=int)
    for col, (i, j) in enumerate(edges):
        d1[i, col] = -1
        d1[j, col] = 1
    d1 %= P
    d2 = np.zeros((len(edges), len(triangles)), dtype=int)
    for col, (a, b, c) in enumerate(triangles):
        for sign, e in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
            d2[edge_index[tuple(sorted(e))], col] += sign
    d2 %= P
    return d1, d2


def x_min_rays(lines, edges, edge_index, d1, d2) -> list[np.ndarray]:
    HZ = d2.T % P
    rays: dict[tuple[int, ...], np.ndarray] = {}
    for line in lines:
        line_edges = [edge_index[tuple(sorted(e))] for e in combinations(line, 2)]
        for support in combinations(line_edges, 3):
            for vals in product((1, 2), repeat=3):
                v = np.zeros(len(edges), dtype=int)
                for val, s in zip(vals, support):
                    v[s] = val
                if np.all((HZ @ v) % P == 0) and not in_rowspace(v, d1):
                    rays.setdefault(vector_canonical_projective(v), v.copy())
    return list(rays.values())


def oriented_cycle_vector(order: list[int], edges, edge_index) -> np.ndarray:
    v = np.zeros(len(edges), dtype=int)
    for a, b in zip(order, order[1:] + [order[0]]):
        e = tuple(sorted((a, b)))
        idx = edge_index[e]
        sign = 1 if (a, b) == edges[idx] else 2
        v[idx] = sign
    return v


def z_min_rays(points, edges, edge_index, adjacency, d1, d2) -> list[np.ndarray]:
    rank_d2 = gf_rank(d2)
    supports: set[tuple[int, int, int, int]] = set()
    rays: dict[tuple[int, ...], np.ndarray] = {}
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
            if gf_rank(np.column_stack([d2, v])) == rank_d2:
                raise AssertionError("unexpected boundary quadrangle")
            rays.setdefault(vector_canonical_projective(v), v.copy())
    return list(rays.values())


def signed_matrix(X: list[np.ndarray], Z: list[np.ndarray]) -> np.ndarray:
    raw = (np.array(X, dtype=np.int16) @ np.array(Z, dtype=np.int16).T) % P
    signed = raw.astype(np.int16)
    signed[signed == 2] = -1
    return signed


def count_distribution_per_axis(G: np.ndarray, values: list[int], axis: int) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for value in values:
        counts = (G == value).sum(axis=axis)
        out[str(value)] = {str(int(k)): int(v) for k, v in Counter(counts.tolist()).items()}
    return out


def build_payload() -> dict:
    points, edges, edge_index, adjacency, lines, triangles = build_w33()
    d1, d2 = boundary_matrices(points, edges, edge_index, triangles)
    X = x_min_rays(lines, edges, edge_index, d1, d2)
    Z = z_min_rays(points, edges, edge_index, adjacency, d1, d2)
    A = signed_matrix(X, Z)
    U = (A != 0).astype(np.int16)

    GX = U @ U.T
    GZ = U.T @ U
    X_diag = Counter(np.diag(GX).tolist())
    Z_diag = Counter(np.diag(GZ).tolist())
    X_off = {str(int(k)): int(v) for k, v in Counter(GX[np.triu_indices(GX.shape[0], 1)].tolist()).items()}
    Z_off = {str(int(k)): int(v) for k, v in Counter(GZ[np.triu_indices(GZ.shape[0], 1)].tolist()).items()}

    Z_per_col = count_distribution_per_axis(GZ, [0, 1, 2, 3, 4], axis=1)
    X_per_row = count_distribution_per_axis(GX, [1, 3, 9, 27], axis=1)
    Z_nonzero_degree = Counter(((GZ > 0).sum(axis=1) - 1).tolist())

    evals = np.linalg.eigvalsh(GX.astype(float))
    signed = A @ A.T

    identities = {
        "ray_counts": len(X) == 160 and len(Z) == 1620,
        "X_row_degree_81": X_diag == Counter({81: 160}),
        "Z_col_degree_8": Z_diag == Counter({8: 1620}),
        "X_overlap_scheme": X_per_row == {"1": {"81": 160}, "3": {"54": 160}, "9": {"18": 160}, "27": {"6": 160}},
        "Z_overlap_scheme": Z_per_col == {"0": {"1187": 1620}, "1": {"288": 1620}, "2": {"96": 1620}, "3": {"32": 1620}, "4": {"16": 1620}},
        "Z_nonzero_degree_432": Z_nonzero_degree == Counter({432: 1620}),
        "Z_nonzero_degree_formula": 432 == 16 * Q_CUBED,
        "Z_off_counts": Z_off == {"0": 961470, "1": 233280, "2": 77760, "3": 25920, "4": 12960},
        "signed_projector": bool(np.max(np.abs(signed @ signed - 160 * signed)) == 0),
    }

    return {
        "summary": {
            "X_rays": len(X),
            "Z_rays": len(Z),
            "X_row_degree": int(next(iter(X_diag.keys()))),
            "Z_column_degree": int(next(iter(Z_diag.keys()))),
            "Z_nonzero_overlap_degree": 432,
            "Z_nonzero_overlap_closed_form": "432 = 16 * 27 = 2^4 * 3^3",
            "all_identities_hold": all(identities.values()),
        },
        "X_side_3adic_scheme": {
            "diagonal_distribution": {str(int(k)): int(v) for k, v in X_diag.items()},
            "off_diagonal_distribution": X_off,
            "per_row_distribution": X_per_row,
            "spectrum_symbolic": {
                "648": 1,
                "144 + 36*sqrt(6)": 24,
                "72": 30,
                "144 - 36*sqrt(6)": 24,
                "40": 81,
            },
            "spectrum_numeric_min_max": [float(evals[0]), float(evals[-1])],
        },
        "Z_side_dual_visibility_scheme": {
            "diagonal_distribution": {str(int(k)): int(v) for k, v in Z_diag.items()},
            "off_diagonal_distribution": Z_off,
            "per_column_distribution": Z_per_col,
            "nonzero_overlap_degree_distribution": {str(int(k)): int(v) for k, v in Z_nonzero_degree.items()},
        },
        "signed_phase_projector": {
            "relation": "A A^T satisfies (A A^T)^2 = 160 A A^T exactly.",
            "rank": int(np.linalg.matrix_rank(A.astype(float))),
            "rank_expected_H1": H1,
        },
        "closed_forms": {
            "X_overlap_values": "1,3,9,27 = q^0,q^1,q^2,q^3",
            "X_per_row_counts": "81,54,18,6 = 3^4, 2*3^3, 2*3^2, 2*3",
            "Z_overlap_values": "0,1,2,3,4 = possible shared visible X-rays for two minimal Z-rays",
            "Z_per_column_counts": "1187,288,96,32,16 with nonzero total 432 = 16*27",
            "Z_nonzero_counts": "288,96,32 is a 3:1 cascade; 16 is the overlap-4 core",
            "dual_reading": "X-side is q-adic by overlap value; Z-side is bounded by d_Z=4 and q-adic by multiplicity cascade.",
        },
        "identities": identities,
        "theorem": (
            "Dual Visibility Scheme Theorem.  For the projective minimal "
            "logical incidence matrix U of the W(3,3) edge CSS code, the "
            "X-side overlaps are the 3-adic values 1,3,9,27 with per-row "
            "counts 81,54,18,6.  Dually, every minimal Z-ray has column "
            "degree 8, is disjoint from 1187 other Z-rays, and has pairwise "
            "visibility overlaps 1,2,3,4 with 288,96,32,16 other Z-rays.  "
            "In particular, every Z-ray overlaps nontrivially with exactly "
            "432 = 16*27 other Z-rays."
        ),
        "honesty_boundary": "This is an exact finite dual visibility scheme; physical probabilities and continuum dynamics are not inferred here.",
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_minimal_logical_dual_visibility_scheme.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
