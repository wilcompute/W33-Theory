#!/usr/bin/env python3
"""Solve for explicit edge potentials for the Z3 (k mod 3) triangle coboundary.

We solve d1 x = t over GF(3) where t is the triangle phase class k mod 3
(with oriented boundary). We output a canonical solution and analyze its
structure (edge type distribution, support, etc.).
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


def phase_to_k(angle):
    return int(np.rint(angle / (np.pi / 6.0))) % 12


def solve_linear_mod3(A, b):
    """Solve A x = b over GF(3). Returns one solution with free vars = 0."""
    A = A.copy() % 3
    b = b.copy() % 3
    m, n = A.shape
    row = 0
    piv = [-1] * n
    for col in range(n):
        pivot = None
        for r in range(row, m):
            if A[r, col] % 3 != 0:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
            b[[row, pivot]] = b[[pivot, row]]
        inv = 1 if A[row, col] == 1 else 2
        A[row] = (A[row] * inv) % 3
        b[row] = (b[row] * inv) % 3
        for r in range(m):
            if r == row:
                continue
            if A[r, col] % 3 != 0:
                factor = A[r, col] % 3
                A[r] = (A[r] - factor * A[row]) % 3
                b[r] = (b[r] - factor * b[row]) % 3
        piv[col] = row
        row += 1
        if row == m:
            break
    # check consistency
    for r in range(m):
        if np.all(A[r] % 3 == 0) and b[r] % 3 != 0:
            return None
    x = np.zeros(n, dtype=int)
    for col, r in enumerate(piv):
        if r != -1:
            x[col] = b[r] % 3
    return x


def main():
    print("Z3 EDGE POTENTIAL FOR TRIANGLE COCYCLE")
    print("=" * 60)
    rays = construct_witting_40_rays()
    n = len(rays)
    edges = build_nonorth_edges(rays)
    triangles = build_triangles(edges, n)
    edge_index = {e: idx for idx, e in enumerate(edges)}

    # build d1 matrix
    d1 = np.zeros((len(triangles), len(edges)), dtype=int)
    for t_idx, (i, j, k) in enumerate(triangles):
        e_jk = edge_index[(j, k)]
        e_ik = edge_index[(i, k)]
        e_ij = edge_index[(i, j)]
        d1[t_idx, e_jk] = 1
        d1[t_idx, e_ik] = -1
        d1[t_idx, e_ij] = 1

    # build t = k mod 3
    t = np.zeros(len(triangles), dtype=int)
    for idx, (i, j, k) in enumerate(triangles):
        ip = (
            np.vdot(rays[i], rays[j])
            * np.vdot(rays[j], rays[k])
            * np.conjugate(np.vdot(rays[i], rays[k]))
        )
        kp = phase_to_k(np.angle(ip))
        t[idx] = kp % 3

    x = solve_linear_mod3(d1, t)
    if x is None:
        print("No solution (unexpected).")
        return

    # verify
    check = (d1 @ x) % 3
    ok = int(np.sum(check == t))
    print(f"Solved: {ok}/{len(t)} equations")

    # distribution of edge labels
    vals, counts = np.unique(x, return_counts=True)
    dist = {int(v): int(c) for v, c in zip(vals, counts)}
    print(f"Edge label distribution: {dist}")

    # edge-type distribution by endpoint support sizes
    support_counts = {}
    for idx, (i, j) in enumerate(edges):
        vi = rays[i]
        vj = rays[j]
        nz_i = sum(1 for z in vi if abs(z) > 1e-9)
        nz_j = sum(1 for z in vj if abs(z) > 1e-9)
        key = (min(nz_i, nz_j), max(nz_i, nz_j), int(x[idx]))
        support_counts[key] = support_counts.get(key, 0) + 1

    # save
    out_path = ROOT / "docs" / "witting_triangle_cocycle_z3_edge_potential.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Edges: {len(edges)}\n")
        f.write(f"Triangles: {len(triangles)}\n")
        f.write(f"Solved: {ok}/{len(t)}\n")
        f.write(f"Edge label distribution: {dist}\n")
        f.write("Support-size distribution by label:\n")
        for key in sorted(support_counts.keys()):
            f.write(f"  {key}: {support_counts[key]}\n")
        for i in range(50):
            f.write(f"{edges[i]}: {int(x[i])}\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
