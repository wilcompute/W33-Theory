#!/usr/bin/env python3
"""Test Z6 cocycle solvability and orbit under monomial symmetry.

We use the triangle phase class k (mod 6) and test whether there exists
edge labels x_e in Z6 with x_ij + x_jk + x_ki = t_ijk (mod 6).
Over Z6, solvable iff solvable mod 2 and mod 3 (CRT).
We also test cohomology equivalence under monomial symmetries via the same rule.
"""
from __future__ import annotations

import itertools
from collections import Counter
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
            rays.append(np.array([0, 1, -omega**mu, omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -omega**mu, -omega**nu]) / sqrt3)
            rays.append(np.array([1, -omega**mu, 0, omega**nu]) / sqrt3)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
    return rays


def canonical_key(ray, tol=1e-6):
    idx = None
    for i, z in enumerate(ray):
        if abs(z) > tol:
            idx = i
            break
    if idx is None:
        return None
    ray_n = ray / ray[idx]
    key = tuple((round(float(z.real), 6), round(float(z.imag), 6)) for z in ray_n)
    return key


def build_monomial_group(rays):
    omega = np.exp(2j * np.pi / 3)
    phases = [0, 1, 2]
    ray_key = [canonical_key(r) for r in rays]
    key_to_idx = {k: i for i, k in enumerate(ray_key)}
    elements = []
    for perm in itertools.permutations(range(4)):
        for a0, a1, a2, a3 in itertools.product(phases, repeat=4):
            phase_vec = np.array([omega**a0, omega**a1, omega**a2, omega**a3], dtype=complex)
            mapping = []
            valid = True
            for r in rays:
                v = r[list(perm)] * phase_vec
                key = canonical_key(v)
                if key not in key_to_idx:
                    valid = False
                    break
                mapping.append(key_to_idx[key])
            if valid:
                elements.append(mapping)
    return elements


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


def gauss_elim_ops(A, p):
    A = A.copy() % p
    m, n = A.shape
    row = 0
    ops = []
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
            ops.append(("swap", row, pivot))
        inv = pow(int(A[row, col]), -1, p)
        if inv != 1:
            A[row] = (A[row] * inv) % p
            ops.append(("scale", row, inv))
        for r in range(row + 1, m):
            if A[r, col] % p != 0:
                factor = A[r, col] % p
                A[r] = (A[r] - factor * A[row]) % p
                ops.append(("add", r, row, (-factor) % p))
        row += 1
        if row == m:
            break
    rank = row
    return ops, rank


def apply_ops_to_vec(b, ops, p):
    b = b.copy() % p
    for op in ops:
        if op[0] == "swap":
            _, i, j = op
            b[i], b[j] = b[j], b[i]
        elif op[0] == "scale":
            _, i, inv = op
            b[i] = (b[i] * inv) % p
        elif op[0] == "add":
            _, i, j, factor = op
            b[i] = (b[i] + factor * b[j]) % p
    return b


def in_image(b, ops, rank, p):
    b2 = apply_ops_to_vec(b, ops, p)
    return bool(np.all(b2[rank:] % p == 0))


def main():
    print("Z6 TRIANGLE COCYCLE TEST")
    print("=" * 60)
    rays = construct_witting_40_rays()
    n = len(rays)
    edges = build_nonorth_edges(rays)
    triangles = build_triangles(edges, n)

    edge_index = {e: idx for idx, e in enumerate(edges)}
    d1 = np.zeros((len(triangles), len(edges)), dtype=int)
    for t_idx, (i, j, k) in enumerate(triangles):
        e_jk = edge_index[(j, k)]
        e_ik = edge_index[(i, k)]
        e_ij = edge_index[(i, j)]
        d1[t_idx, e_jk] = 1
        d1[t_idx, e_ik] = -1
        d1[t_idx, e_ij] = 1

    ops2, rank2 = gauss_elim_ops(d1, 2)
    ops3, rank3 = gauss_elim_ops(d1, 3)

    # base labels
    t6 = np.zeros(len(triangles), dtype=int)
    for idx, (i, j, k) in enumerate(triangles):
        ip_ij = np.vdot(rays[i], rays[j])
        ip_jk = np.vdot(rays[j], rays[k])
        ip_ik = np.vdot(rays[i], rays[k])
        ip = ip_ij * ip_jk * np.conjugate(ip_ik)
        kp = phase_to_k(np.angle(ip))
        t6[idx] = kp % 6

    # solvable mod6 iff solvable mod2 and mod3
    ok2 = in_image(t6 % 2, ops2, rank2, 2)
    ok3 = in_image(t6 % 3, ops3, rank3, 3)
    ok6 = ok2 and ok3
    print(f"Base t6 solvable mod2: {ok2}")
    print(f"Base t6 solvable mod3: {ok3}")
    print(f"Base t6 solvable mod6: {ok6}")

    # orbit under monomial symmetry
    group = build_monomial_group(rays)
    counts = Counter()
    for g in group:
        t6_g = np.zeros(len(triangles), dtype=int)
        for idx, (i, j, k) in enumerate(triangles):
            i2, j2, k2 = g[i], g[j], g[k]
            arr = [i2, j2, k2]
            a, b, c = sorted(arr)
            ip_ab = np.vdot(rays[a], rays[b])
            ip_bc = np.vdot(rays[b], rays[c])
            ip_ac = np.vdot(rays[a], rays[c])
            ip = ip_ab * ip_bc * np.conjugate(ip_ac)
            kp = phase_to_k(np.angle(ip)) % 6
            # orientation sign: odd permutation flips phase sign
            inv = 0
            for p in range(3):
                for q in range(p + 1, 3):
                    if arr[p] > arr[q]:
                        inv += 1
            if inv % 2 == 1:
                kp = (-kp) % 6
            t6_g[idx] = kp
        d2 = (t6_g - t6) % 2
        d3 = (t6_g - t6) % 3
        ok = in_image(d2, ops2, rank2, 2) and in_image(d3, ops3, rank3, 3)
        counts[ok] += 1

    print(f"Z6 cohomology orbit: {dict(counts)}")

    out_path = ROOT / "docs" / "witting_triangle_cocycle_z6.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Base solvable mod2: {ok2}\n")
        f.write(f"Base solvable mod3: {ok3}\n")
        f.write(f"Base solvable mod6: {ok6}\n")
        f.write(f"Orbit cohomology counts: {dict(counts)}\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
