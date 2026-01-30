#!/usr/bin/env python3
"""Compute cohomology dimensions of the Witting non-orthogonality 2-complex.

We use the 40-ray non-orthogonality graph and its triangle 2-skeleton.
Compute ranks of coboundary maps over GF(2) and GF(3).
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_witting_40_rays():
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays = []
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -(omega**mu), omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -(omega**mu), -(omega**nu)]) / sqrt3)
            rays.append(np.array([1, -(omega**mu), 0, omega**nu]) / sqrt3)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
    return rays


def build_nonorth_edges(rays, tol=1e-8):
    edges = []
    for i in range(len(rays)):
        for j in range(i + 1, len(rays)):
            if abs(np.vdot(rays[i], rays[j])) >= tol:
                edges.append((i, j))
    return edges


def build_triangles(edges, n):
    edge_set = set(edges)
    triangles = []
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) not in edge_set:
                continue
            for k in range(j + 1, n):
                if (i, k) in edge_set and (j, k) in edge_set:
                    triangles.append((i, j, k))
    return triangles


def gauss_rank_modp(A, p):
    A = A.copy() % p
    m, n = A.shape
    row = 0
    rank = 0
    for col in range(n):
        pivot = None
        for r in range(row, m):
            if A[r, col] % p != 0:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
        inv = pow(int(A[row, col]), -1, p)
        A[row] = (A[row] * inv) % p
        for r in range(m):
            if r == row:
                continue
            if A[r, col] % p != 0:
                factor = A[r, col] % p
                A[r] = (A[r] - factor * A[row]) % p
        rank += 1
        row += 1
        if row == m:
            break
    return rank


def main():
    print("WITTING 2-COMPLEX COHOMOLOGY")
    print("=" * 60)

    rays = construct_witting_40_rays()
    n = len(rays)
    edges = build_nonorth_edges(rays)
    triangles = build_triangles(edges, n)

    print(f"Vertices: {n}")
    print(f"Edges (non-orth): {len(edges)}")
    print(f"Triangles: {len(triangles)}")

    edge_index = {e: idx for idx, e in enumerate(edges)}

    # d0: C^0 -> C^1 (edges x vertices)
    d0 = np.zeros((len(edges), n), dtype=int)
    for idx, (i, j) in enumerate(edges):
        # oriented edge i->j (i<j)
        d0[idx, i] = -1
        d0[idx, j] = 1

    # d1: C^1 -> C^2 (triangles x edges)
    d1 = np.zeros((len(triangles), len(edges)), dtype=int)
    for t_idx, (i, j, k) in enumerate(triangles):
        # oriented triangle (i<j<k)
        e_jk = edge_index[(j, k)]
        e_ik = edge_index[(i, k)]
        e_ij = edge_index[(i, j)]
        d1[t_idx, e_jk] = 1
        d1[t_idx, e_ik] = -1
        d1[t_idx, e_ij] = 1

    for p in [2, 3]:
        r0 = gauss_rank_modp(d0, p)
        r1 = gauss_rank_modp(d1, p)
        dim_c0 = n
        dim_c1 = len(edges)
        dim_c2 = len(triangles)
        dim_h0 = dim_c0 - r0
        dim_h1 = (dim_c1 - r1) - r0
        dim_h2 = dim_c2 - r1
        print(f"GF({p}) ranks: rank(d0)={r0}, rank(d1)={r1}")
        print(f"GF({p}) H^0 dim = {dim_h0}")
        print(f"GF({p}) H^1 dim = {dim_h1}")
        print(f"GF({p}) H^2 dim = {dim_h2}")

    # save summary
    out_path = ROOT / "docs" / "witting_triangle_cohomology.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Vertices: {n}\n")
        f.write(f"Edges: {len(edges)}\n")
        f.write(f"Triangles: {len(triangles)}\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
