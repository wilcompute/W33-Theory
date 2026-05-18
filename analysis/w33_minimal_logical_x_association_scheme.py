#!/usr/bin/env python3
"""X-side association scheme of the W(3,3) minimal logical surface.

This upgrades the 3-adic overlap histogram into an algebraic closure theorem.

Let U be the unsigned projective minimal logical incidence matrix:

    U[x,z] = 1 iff minimal X-ray x and minimal Z-ray z pair nontrivially.

Rows are the 160 minimal X-rays; columns are the 1620 minimal Z-rays.
The X-side Gram matrix G=U U^T has diagonal 81 and off-diagonal overlaps
only in {1,3,9,27}.  Define relation matrices:

    R_0  = I,
    R_1  = [G_ij = 1],
    R_3  = [G_ij = 3],
    R_9  = [G_ij = 9],
    R_27 = [G_ij = 27].

Then {R_0,R_1,R_3,R_9,R_27} partitions the complete directed relation
on 160 points and closes under multiplication.  Therefore the X-side
minimal logical visibility geometry is a 4-class association scheme.
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
MU = 4
H1 = Q ** (Q + 1)

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


def relation_matrices(G: np.ndarray) -> dict[str, np.ndarray]:
    rel = {"0": np.eye(G.shape[0], dtype=np.int16)}
    for val in [1, 3, 9, 27]:
        rel[str(val)] = (G == val).astype(np.int16)
    return rel


def intersection_numbers(rel: dict[str, np.ndarray]) -> dict[str, dict[str, dict[str, int]]]:
    names = ["0", "1", "3", "9", "27"]
    out: dict[str, dict[str, dict[str, int]]] = {}
    for i in names:
        out[i] = {}
        for j in names:
            product_matrix = rel[i] @ rel[j]
            row: dict[str, int] = {}
            for k in names:
                entries = product_matrix[rel[k].astype(bool)]
                vals = set(int(x) for x in entries.tolist())
                if len(vals) != 1:
                    raise AssertionError(f"not an association scheme at ({i},{j},{k}): {vals}")
                row[k] = vals.pop()
            out[i][j] = row
    return out


def build_payload() -> dict:
    points, edges, edge_index, adjacency, lines, triangles = build_w33()
    d1, d2 = boundary_matrices(points, edges, edge_index, triangles)
    X = x_min_rays(lines, edges, edge_index, d1, d2)
    Z = z_min_rays(points, edges, edge_index, adjacency, d1, d2)
    raw = (np.array(X, dtype=np.int16) @ np.array(Z, dtype=np.int16).T) % P
    U = (raw != 0).astype(np.int16)
    G = U @ U.T
    rel = relation_matrices(G)
    inter = intersection_numbers(rel)
    valencies = {name: int(mat.sum(axis=1)[0]) for name, mat in rel.items()}

    partition_ok = np.all(sum(rel.values()) == 1)
    commutative_ok = all(np.array_equal(rel[a] @ rel[b], rel[b] @ rel[a]) for a in rel for b in rel)
    symmetric_ok = all(np.array_equal(mat, mat.T) for mat in rel.values())

    identities = {
        "ray_counts": len(X) == 160 and len(Z) == 1620,
        "partition_complete": bool(partition_ok),
        "symmetric_relations": bool(symmetric_ok),
        "commutative_relations": bool(commutative_ok),
        "valencies": valencies == {"0": 1, "1": 81, "3": 54, "9": 18, "27": 6},
        "closed_under_multiplication": True,
        "rank_of_signed_phase": int(np.linalg.matrix_rank(((raw.astype(np.int16) + 1) % 3 - 1).astype(float))) == H1,
    }

    return {
        "summary": {
            "vertices_in_scheme": len(X),
            "classes_excluding_identity": 4,
            "relations": ["0", "1", "3", "9", "27"],
            "valencies": valencies,
            "all_identities_hold": all(identities.values()),
        },
        "association_scheme": {
            "relation_definition": "R_k connects two minimal X-rays iff their visible-Z overlap is k, for k in {1,3,9,27}; R_0 is identity.",
            "valencies": valencies,
            "intersection_numbers": inter,
            "partition_complete": bool(partition_ok),
            "symmetric": bool(symmetric_ok),
            "commutative": bool(commutative_ok),
        },
        "closed_forms": {
            "overlap_values": "1,3,9,27 = q^0,q^1,q^2,q^3",
            "valencies": "1,81,54,18,6 = identity plus 3^4, 2*3^3, 2*3^2, 2*3",
            "association_class_count": "4 nontrivial classes, matching d_Z=4 and q+1=4",
            "scheme_size": "160 minimal X-rays = 40 isotropic lines * 4 line-stars",
        },
        "identities": identities,
        "theorem": (
            "Minimal Logical X-Association Scheme Theorem.  The projective "
            "minimal X-rays of the canonical W(3,3) edge CSS code form a "
            "4-class commutative association scheme under visible-Z overlap. "
            "The nontrivial relations are indexed by overlap values 1,3,9,27, "
            "with valencies 81,54,18,6.  The relation matrices partition the "
            "complete relation on 160 points and close under matrix multiplication."
        ),
        "honesty_boundary": "This is an exact finite association-scheme invariant. It does not by itself assign continuum dynamics or empirical observables.",
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_minimal_logical_x_association_scheme.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
