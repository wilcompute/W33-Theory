#!/usr/bin/env python3
"""Exact CSS-code audit for the W(3,3) finite substrate.

Purpose
-------
Recent notes proposed a vertex-qutrit code [[40,12,13]]_3.  This file
checks what the canonical W(3,3) incidence data actually gives without any
extra assumptions.

Result
------
The natural chain-complex CSS code lives on the 240 EDGES, not on the 40
vertices:

    H_X = d_1       : C_1 -> C_0
    H_Z = d_2^T     : C_1 -> C_2

where d_2 is built from the 160 triangles contained in the 40 isotropic
projective lines.  Over F_3:

    n       = 240
    rank HX = 39
    rank HZ = 120
    k       = 240 - 39 - 120 = 81
    d_Z     = 4
    d_X     = 3

so the exact canonical edge-carrier code is [[240,81,3]]_3, with asymmetric
witness distances (Z distance 4, X distance 3).  This preserves the central
81-protected-sector story but moves the rigorous QEC claim to the edge
carrier.

A vertex code [[40,12,13]]_3 may still exist as an additional construction,
but it requires explicit commuting stabilizer matrices and a distance proof;
it is not forced by W(3,3) graph counts alone.
"""
from __future__ import annotations

import json
from itertools import combinations, permutations, product
from pathlib import Path
from typing import Iterable

import numpy as np

P = 3
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


def gf_rref(M: np.ndarray, p: int = P) -> tuple[np.ndarray, list[int]]:
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
    return len(gf_rref(M, p)[1])


def gf_nullspace(M: np.ndarray, p: int = P) -> np.ndarray:
    R, pivots = gf_rref(M, p)
    m, n = R.shape
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for f in free:
        x = np.zeros(n, dtype=int)
        x[f] = 1
        for row, c in enumerate(pivots):
            x[c] = (-R[row, f]) % p
        basis.append(x)
    return np.array(basis, dtype=int)


def in_rowspace(v: np.ndarray, rows: np.ndarray, p: int = P) -> bool:
    rows = np.array(rows, dtype=int) % p
    v = np.array(v, dtype=int).reshape(1, -1) % p
    return gf_rank(np.vstack([rows, v]), p) == gf_rank(rows, p)


def in_colspace(v: np.ndarray, cols: np.ndarray, p: int = P) -> bool:
    return in_rowspace(v, np.array(cols, dtype=int).T, p)


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

    edges = [(i, j) for i, j in combinations(range(len(points)), 2) if omega(points[i], points[j]) == 0]
    edge_index = {e: n for n, e in enumerate(edges)}
    point_index = {p: i for i, p in enumerate(points)}

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
    return points, edges, edge_index, lines, triangles


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


def cycle_vector(vertices: tuple[int, ...], edges, edge_index) -> np.ndarray | None:
    v = np.zeros(len(edges), dtype=int)
    verts = list(vertices)
    for a, b in zip(verts, verts[1:] + verts[:1]):
        e = tuple(sorted((a, b)))
        if e not in edge_index:
            return None
        sign = 1 if (a, b) == e else -1
        v[edge_index[e]] = (v[edge_index[e]] + sign) % P
    return v


def find_z_distance(d1: np.ndarray, d2: np.ndarray, edges, edge_index) -> tuple[int, list[dict]]:
    # weight <= 3 cycles in a simple graph are either zero or triangles; all W33
    # triangles live inside an isotropic line and are columns of d2.  We still
    # search them explicitly, then search simple 4-cycles.
    n = len(edges)
    for w in range(1, 4):
        for support in combinations(range(n), w):
            ns = gf_nullspace(d1[:, support])
            for coeff in ns:
                if not np.any(coeff % P):
                    continue
                vec = np.zeros(n, dtype=int)
                for c, idx in zip(coeff, support):
                    vec[idx] = c % P
                if not in_colspace(vec, d2):
                    return w, [{"edge_index": int(i), "edge": list(edges[i]), "coeff": int(vec[i])} for i in support]

    for vertices in combinations(range(40), 4):
        for perm in permutations(vertices):
            if perm[0] != min(vertices):
                continue
            vec = cycle_vector(perm, edges, edge_index)
            if vec is None:
                continue
            if np.all(d1 @ vec % P == 0) and not in_colspace(vec, d2):
                witness = [
                    {"edge_index": int(i), "edge": list(edges[i]), "coeff": int(vec[i] % P)}
                    for i in np.nonzero(vec % P)[0]
                ]
                return 4, witness
    raise RuntimeError("Z distance not found through weight 4")


def find_x_distance(d1: np.ndarray, d2: np.ndarray, edges) -> tuple[int, list[dict]]:
    H = d2.T % P
    n = len(edges)
    for w in range(1, 5):
        for support in combinations(range(n), w):
            ns = gf_nullspace(H[:, support])
            for coeff in ns:
                if not np.any(coeff % P):
                    continue
                vec = np.zeros(n, dtype=int)
                for c, idx in zip(coeff, support):
                    vec[idx] = c % P
                if not in_rowspace(vec, d1):
                    witness = [
                        {"edge_index": int(i), "edge": list(edges[i]), "coeff": int(vec[i] % P)}
                        for i in support
                        if vec[i] % P
                    ]
                    return w, witness
    raise RuntimeError("X distance not found through weight 4")


def point_line_incidence_audit(points, lines) -> dict:
    B = np.zeros((len(lines), len(points)), dtype=int)
    for r, line in enumerate(lines):
        for p in line:
            B[r, p] = 1
    rank_B = gf_rank(B)
    gram = B @ B.T % P
    rank_gram = gf_rank(gram)
    return {
        "n_vertex_qutrits": len(points),
        "num_line_checks": len(lines),
        "rank_line_incidence": rank_B,
        "rank_line_gram_BBT": rank_gram,
        "commuting_if_HX_equals_HZ_line_incidence": bool(np.all(gram == 0)),
        "conclusion": "The raw line-point incidence matrix is not self-orthogonal over F_3, so it is not by itself a symmetric CSS stabilizer on 40 vertex qutrits.",
    }


def main() -> None:
    points, edges, edge_index, lines, triangles = build_w33()
    d1, d2 = boundary_matrices(points, edges, edge_index, triangles)

    rank_x = gf_rank(d1)
    rank_z = gf_rank(d2.T)
    commute = bool(np.all(d1 @ d2 % P == 0))
    k_logical = len(edges) - rank_x - rank_z
    d_z, z_witness = find_z_distance(d1, d2, edges, edge_index)
    d_x, x_witness = find_x_distance(d1, d2, edges)

    result = {
        "canonical_edge_css_code": {
            "field": "F_3",
            "physical_qutrits_n_edges": len(edges),
            "HX_shape": list(d1.shape),
            "HZ_shape": list(d2.T.shape),
            "rank_HX": rank_x,
            "rank_HZ": rank_z,
            "commuting_HX_HZ": commute,
            "logical_qutrits_k": k_logical,
            "Z_distance": d_z,
            "Z_witness": z_witness,
            "X_distance": d_x,
            "X_witness": x_witness,
            "symmetric_distance": min(d_x, d_z),
            "parameters": f"[[{len(edges)},{k_logical},{min(d_x,d_z)}]]_3 with asymmetric distances d_X={d_x}, d_Z={d_z}",
        },
        "vertex_code_warning": point_line_incidence_audit(points, lines),
        "interpretation": {
            "exact_statement": "The protected 81 sector is exactly the logical dimension of the canonical edge-chain CSS code.",
            "theorem_obligation": "A [[40,12,13]]_3 vertex code needs explicit commuting stabilizers and a distance-13 proof; it is not implied by W(3,3) counts alone.",
        },
    }

    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    Path("data/w33_css_exact_audit.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
