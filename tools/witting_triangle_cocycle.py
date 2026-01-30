#!/usr/bin/env python3
"""Cocycle tests for Witting triangle phase classes.

We build the non-orthogonality graph on 40 rays and its triangle 2-complex.
We test whether the triangle phase labels are coboundaries of edge 1-cochains
(mod 2 and mod 3).
"""

from __future__ import annotations

import json
from itertools import combinations, product
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


def phase_to_k(angle):
    return int(np.rint(angle / (np.pi / 6.0))) % 12


def gauss_solve_modp(A, b, p):
    """Solve A x = b over GF(p). Returns (has_solution, rank)."""
    A = A.copy() % p
    b = b.copy() % p
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
            b[[row, pivot]] = b[[pivot, row]]
        inv = pow(int(A[row, col]), -1, p)
        A[row] = (A[row] * inv) % p
        b[row] = (b[row] * inv) % p
        for r in range(m):
            if r == row:
                continue
            if A[r, col] % p != 0:
                factor = A[r, col] % p
                A[r] = (A[r] - factor * A[row]) % p
                b[r] = (b[r] - factor * b[row]) % p
        rank += 1
        row += 1
        if row == m:
            break
    # check consistency
    for r in range(m):
        if np.all(A[r] % p == 0) and b[r] % p != 0:
            return False, rank
    return True, rank


def main():
    print("WITTING TRIANGLE COCYCLE TEST")
    print("=" * 60)

    rays = construct_witting_40_rays()
    n = len(rays)

    # build non-orth edges and index
    edges = []
    edge_index = {}
    for i in range(n):
        for j in range(i + 1, n):
            ip = np.vdot(rays[i], rays[j])
            if abs(ip) < 1e-8:
                continue
            edge_index[(i, j)] = len(edges)
            edges.append((i, j))

    # build triangles with all non-orth edges
    triangles = []
    tri_k = []
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) not in edge_index:
                continue
            for k in range(j + 1, n):
                if (i, k) not in edge_index or (j, k) not in edge_index:
                    continue
                # triangle phase
                phi = np.vdot(rays[i], rays[j])
                phi *= np.vdot(rays[j], rays[k])
                phi *= np.vdot(rays[k], rays[i])
                kphase = phase_to_k(np.angle(phi))
                triangles.append((i, j, k))
                tri_k.append(kphase)

    print(f"Non-orth edges: {len(edges)}")
    print(f"Non-orth triangles: {len(triangles)}")

    # build linear system: edge labels x_e, triangle constraints
    m = len(triangles)
    ecount = len(edges)

    # Z2: t=0 for |phase|=pi/6, t=1 for |phase|=pi/2
    b2 = np.zeros(m, dtype=int)
    A2 = np.zeros((m, ecount), dtype=int)
    for idx, (i, j, k) in enumerate(triangles):
        for a, b in [(i, j), (j, k), (i, k)]:
            e = edge_index[(a, b) if a < b else (b, a)]
            A2[idx, e] = 1
        kp = tri_k[idx] % 12
        mag_class = 0 if kp in (1, 11) else 1  # pi/6 vs pi/2
        b2[idx] = mag_class

    ok2, rank2 = gauss_solve_modp(A2, b2, 2)
    print(f"Z2 cocycle (|phase|): solvable={ok2}, rank={rank2}")

    # Z2 alt: sign class (+ vs -) where k in {1,3} positive, {9,11} negative
    b2s = np.zeros(m, dtype=int)
    A2s = A2.copy()
    for idx, kp in enumerate(tri_k):
        b2s[idx] = 0 if kp in (1, 3) else 1
    ok2s, rank2s = gauss_solve_modp(A2s, b2s, 2)
    print(f"Z2 cocycle (sign): solvable={ok2s}, rank={rank2s}")

    # Z3: t = k mod 3 with oriented d1 (1, -1, 1)
    b3 = np.array([k % 3 for k in tri_k], dtype=int)
    A3 = np.zeros((m, ecount), dtype=int)
    for idx, (i, j, k) in enumerate(triangles):
        e_jk = edge_index[(j, k)]
        e_ik = edge_index[(i, k)]
        e_ij = edge_index[(i, j)]
        A3[idx, e_jk] = 1
        A3[idx, e_ik] = -1
        A3[idx, e_ij] = 1
    ok3, rank3 = gauss_solve_modp(A3, b3, 3)
    print(f"Z3 cocycle (k mod 3): solvable={ok3}, rank={rank3}")

    out = {
        "edges": len(edges),
        "triangles": len(triangles),
        "z2_mag_solvable": bool(ok2),
        "z2_sign_solvable": bool(ok2s),
        "z3_solvable": bool(ok3),
        "rank_z2_mag": int(rank2),
        "rank_z2_sign": int(rank2s),
        "rank_z3": int(rank3),
    }
    out_path = ROOT / "artifacts" / "witting_triangle_cocycle.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
