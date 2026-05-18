#!/usr/bin/env python3
"""Minimal logical E6 pairing theorem for the W(3,3) edge CSS code.

This script corrects the vector-count convention from the first minimal
witness census and then computes the full minimal X/Z commutation pairing.

Canonical W(3,3) edge CSS code:

    H_X = d1      : C1 -> C0
    H_Z = d2^T    : C1 -> C2
    [[240,81,3]]_3 with d_X=3, d_Z=4.

Minimal witnesses:

    X_min supports = 160, unique F_3 vectors = 320.
    Z_min supports = 1620, unique F_3 vectors = 3240.

Important convention correction:

    A Z quadrangle support has two unique F_3 vector representatives up to
    nonzero scalar.  If one additionally counts oriented-walk presentations,
    there are four presentations per support, hence 6480 oriented
    presentations.  The unique vector count is 3240, not 6480.

Breakthrough invariant:

    # { (x,z) in X_min x Z_min : <x,z> != 0 } = 51840 = |W(E6)|.

The nonzero phases split evenly:

    phase 1: 25920, phase 2: 25920.

The support-level incidence graph is also exact:

    160 * 81 = 1620 * 8 = 12960.

This makes W(E6) the commutation-shadow of the minimal logical error
surface of the W(3,3) edge code.
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
        raise ValueError("zero vector has no projective representative")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError("unreachable")


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


def x_min_vectors(lines, edges, edge_index, d1, d2) -> tuple[list[np.ndarray], set[tuple[int, int, int]]]:
    HZ = d2.T % P
    supports: set[tuple[int, int, int]] = set()
    vecs: dict[tuple[int, ...], np.ndarray] = {}
    for line in lines:
        line_edges = [edge_index[tuple(sorted(e))] for e in combinations(line, 2)]
        for support in combinations(line_edges, 3):
            for vals in product((1, 2), repeat=3):
                vec = np.zeros(len(edges), dtype=int)
                for val, s in zip(vals, support):
                    vec[s] = val
                if np.all((HZ @ vec) % P == 0) and not in_rowspace(vec, d1):
                    supports.add(tuple(sorted(support)))
                    vecs[tuple(vec.tolist())] = vec.copy()
    return list(vecs.values()), supports


def oriented_cycle_vector(order: list[int], edges, edge_index) -> np.ndarray:
    vec = np.zeros(len(edges), dtype=int)
    for u, v in zip(order, order[1:] + [order[0]]):
        e = tuple(sorted((u, v)))
        idx = edge_index[e]
        sign = 1 if (u, v) == edges[idx] else 2
        vec[idx] = sign
    return vec


def z_min_vectors(points, edges, edge_index, adjacency, d1, d2) -> tuple[list[np.ndarray], set[tuple[int, int, int, int]], list[dict]]:
    rank_d2 = gf_rank(d2)
    supports: set[tuple[int, int, int, int]] = set()
    vecs: dict[tuple[int, ...], np.ndarray] = {}
    examples: list[dict] = []
    for a, b in combinations(range(len(points)), 2):
        if adjacency[a][b]:
            continue
        common = [x for x in range(len(points)) if adjacency[a][x] and adjacency[b][x]]
        if len(common) != MU:
            raise AssertionError(f"expected mu={MU} common neighbours, got {len(common)}")
        for c, d in combinations(common, 2):
            support = tuple(sorted(edge_index[tuple(sorted(e))] for e in ((a, c), (c, b), (b, d), (d, a))))
            if support in supports:
                continue
            supports.add(support)
            vec = oriented_cycle_vector([a, c, b, d], edges, edge_index)
            if not np.all((d1 @ vec) % P == 0):
                raise AssertionError("quadrangle is not a cycle")
            if gf_rank(np.column_stack([d2, vec])) == rank_d2:
                raise AssertionError("quadrangle unexpectedly boundary")
            for scalar in (1, 2):
                vecs[tuple((scalar * vec % P).tolist())] = scalar * vec % P
            if len(examples) < 4:
                examples.append(
                    {
                        "cycle_order": [a, c, b, d],
                        "support_edges": [list(edges[i]) for i in support],
                        "coefficients": [int(vec[i]) for i in support],
                    }
                )
    return list(vecs.values()), supports, examples


def support_incidence(x_supports, z_supports) -> dict:
    x_supports = sorted(x_supports)
    z_supports = sorted(z_supports)
    zsets = [set(s) for s in z_supports]
    x_degrees: list[int] = []
    z_degrees = [0] * len(z_supports)
    total = 0
    for xs in x_supports:
        xset = set(xs)
        deg = 0
        for j, zs in enumerate(zsets):
            if xset & zs:
                total += 1
                deg += 1
                z_degrees[j] += 1
        x_degrees.append(deg)
    return {
        "total_support_incidences": total,
        "X_support_degree_distribution": dict(Counter(x_degrees)),
        "Z_support_degree_distribution": dict(Counter(z_degrees)),
        "biregular_identity": f"{len(x_supports)}*81 = {len(z_supports)}*8 = {total}",
    }


def vector_pairing(x_vecs: list[np.ndarray], z_vecs: list[np.ndarray]) -> dict:
    X = np.array(x_vecs, dtype=int)
    Z = np.array(z_vecs, dtype=int)
    pair = (X @ Z.T) % P
    phase_counts = {str(int(k)): int(v) for k, v in zip(*np.unique(pair, return_counts=True))}
    x_nonzero = (pair != 0).sum(axis=1)
    z_nonzero = (pair != 0).sum(axis=0)
    nonzero = int((pair != 0).sum())
    return {
        "matrix_shape": [int(pair.shape[0]), int(pair.shape[1])],
        "total_pairs": int(pair.size),
        "phase_counts": phase_counts,
        "nonzero_pairings": nonzero,
        "phase_1_pairings": phase_counts.get("1", 0),
        "phase_2_pairings": phase_counts.get("2", 0),
        "X_vector_nonzero_degree_distribution": {str(int(k)): int(v) for k, v in Counter(x_nonzero.tolist()).items()},
        "Z_vector_nonzero_degree_distribution": {str(int(k)): int(v) for k, v in Counter(z_nonzero.tolist()).items()},
        "W_E6_identity": nonzero == WE6,
        "phase_balance": phase_counts.get("1", 0) == phase_counts.get("2", 0) == WE6 // 2,
        "biregular_identity": f"{len(x_vecs)}*162 = {len(z_vecs)}*16 = {nonzero}",
    }


def build_payload() -> dict:
    points, edges, edge_index, adjacency, lines, triangles = build_w33()
    d1, d2 = boundary_matrices(points, edges, edge_index, triangles)
    x_vecs, x_supports = x_min_vectors(lines, edges, edge_index, d1, d2)
    z_vecs, z_supports, z_examples = z_min_vectors(points, edges, edge_index, adjacency, d1, d2)
    supp = support_incidence(x_supports, z_supports)
    vec = vector_pairing(x_vecs, z_vecs)

    oriented_presentations_per_z_support = 4
    oriented_z_presentations = oriented_presentations_per_z_support * len(z_supports)
    nonedges = len(points) * (len(points) - 1) // 2 - len(edges)

    identities = {
        "points_40": len(points) == V,
        "edges_240": len(edges) == E,
        "lines_40": len(lines) == V,
        "triangles_160": len(triangles) == 160,
        "X_supports_160": len(x_supports) == 160,
        "X_vectors_320": len(x_vecs) == 320,
        "Z_supports_1620": len(z_supports) == 1620,
        "Z_unique_vectors_3240": len(z_vecs) == 3240,
        "Z_oriented_presentations_6480": oriented_z_presentations == 6480,
        "support_incidence_total_12960": supp["total_support_incidences"] == 12_960,
        "support_X_degree_81": supp["X_support_degree_distribution"] == {81: 160},
        "support_Z_degree_8": supp["Z_support_degree_distribution"] == {8: 1620},
        "vector_nonzero_pairings_WE6": vec["nonzero_pairings"] == WE6,
        "vector_phase_balance": vec["phase_balance"],
        "vector_X_degree_162": vec["X_vector_nonzero_degree_distribution"] == {"162": 320},
        "vector_Z_degree_16": vec["Z_vector_nonzero_degree_distribution"] == {"16": 3240},
        "Z_support_formula": len(z_supports) == nonedges * (MU * (MU - 1) // 2) // 2,
    }

    theorem = (
        "Minimal Logical E6 Pairing Theorem.  In the canonical W(3,3) edge CSS "
        "code over F_3, there are 320 minimal X logical vectors and 3240 unique "
        "minimal Z logical vectors.  The number of nonzero symplectic pairings "
        "between them is exactly 51840 = |W(E6)|, split evenly into 25920 phase-1 "
        "and 25920 phase-2 pairings.  Equivalently, the noncommutation graph is "
        "biregular with X-degree 162 and Z-degree 16."
    )

    return {
        "summary": {
            "X_supports": len(x_supports),
            "X_unique_vectors": len(x_vecs),
            "Z_supports": len(z_supports),
            "Z_unique_F3_vectors": len(z_vecs),
            "Z_oriented_walk_presentations": oriented_z_presentations,
            "support_nonempty_intersections": supp["total_support_incidences"],
            "vector_nonzero_pairings": vec["nonzero_pairings"],
            "W_E6_order": WE6,
            "all_identities_hold": all(identities.values()),
        },
        "substrate_counts": {
            "points": len(points),
            "edges": len(edges),
            "lines": len(lines),
            "line_triangles": len(triangles),
            "nonedges": nonedges,
            "mu_common_neighbors_for_nonedge": MU,
        },
        "minimal_witness_counts": {
            "X_supports": len(x_supports),
            "X_unique_vectors": len(x_vecs),
            "Z_supports": len(z_supports),
            "Z_unique_F3_vectors": len(z_vecs),
            "Z_oriented_walk_presentations": oriented_z_presentations,
            "convention_correction": "6480 counts oriented-walk presentations; the unique F_3 Z-vector count is 3240.",
            "Z_examples": z_examples,
        },
        "support_incidence_graph": supp,
        "vector_pairing_graph": vec,
        "closed_forms": {
            "X_supports": "160 = 40 lines * 4 line-stars",
            "X_vectors": "320 = 2 * 160 = 40 * 2^3",
            "Z_supports": "1620 = 540 nonedges * C(4,2) / 2 = 20 * 81 = 60 * 27",
            "Z_unique_vectors": "3240 = 2 * 1620 = 40 * 81",
            "Z_oriented_presentations": "6480 = 4 * 1620 = 240 * 27 = 80 * 81 = |W(E6)|/8",
            "support_pairings": "12960 = 160 * 81 = 1620 * 8",
            "nonzero_vector_pairings": "51840 = 320 * 162 = 3240 * 16 = |W(E6)|",
            "phase_split": "51840 = 25920 + 25920",
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": "This is an exact finite CSS commutation census.  It identifies |W(E6)| as the nonzero minimal-logical pairing count; physical TQC/SM interpretations are separate bridges.",
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_minimal_logical_e6_pairing.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
