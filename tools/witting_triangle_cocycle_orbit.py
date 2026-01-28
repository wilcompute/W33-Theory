#!/usr/bin/env python3
"""Cocycle orbit under monomial symmetries.

We compute how the triangle-phase labeling transforms under the monomial
symmetry group (order 243) and test cohomology equivalence:
  t_g - t in im(d1) ?
for mod 2 and mod 3 labelings.
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
    """Gaussian elimination with operation logging. Returns ops and rank."""
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
    # rows rank..end must be zero
    return bool(np.all(b2[rank:] % p == 0))


def main():
    print("TRIANGLE COCYCLE ORBIT TEST")
    print("=" * 60)
    rays = construct_witting_40_rays()
    n = len(rays)
    edges = build_nonorth_edges(rays)
    triangles = build_triangles(edges, n)

    # triangle label base
    tri_label_k = {}
    for (i, j, k) in triangles:
        ip = np.vdot(rays[i], rays[j]) * np.vdot(rays[j], rays[k]) * np.vdot(rays[k], rays[i])
        tri_label_k[(i, j, k)] = phase_to_k(np.angle(ip))

    # d1 matrix for cohomology checks
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

    # base label vectors
    t_mag = np.array([0 if (tri_label_k[t] % 12) in (1, 11) else 1 for t in triangles], dtype=int)
    t_sign = np.array([0 if (tri_label_k[t] % 12) in (1, 3) else 1 for t in triangles], dtype=int)
    t_mod3 = np.array([tri_label_k[t] % 3 for t in triangles], dtype=int)

    # monomial group
    group = build_monomial_group(rays)
    print(f"Monomial group size: {len(group)}")

    orbit_counts = {
        "mag_mod2": Counter(),
        "sign_mod2": Counter(),
        "mod3": Counter(),
    }

    for g in group:
        # permute triangles via mapping g
        # note: monomial symmetry preserves triangle phase for mapped indices
        t_g_mag = np.zeros(len(triangles), dtype=int)
        t_g_sign = np.zeros(len(triangles), dtype=int)
        t_g_mod3 = np.zeros(len(triangles), dtype=int)
        for idx, (i, j, k) in enumerate(triangles):
            i2, j2, k2 = g[i], g[j], g[k]
            a, b, c = sorted((i2, j2, k2))
            kp = tri_label_k[(a, b, c)]
            t_g_mag[idx] = 0 if kp in (1, 11) else 1
            t_g_sign[idx] = 0 if kp in (1, 3) else 1
            t_g_mod3[idx] = kp % 3

        # differences
        d_mag = (t_g_mag - t_mag) % 2
        d_sign = (t_g_sign - t_sign) % 2
        d_mod3 = (t_g_mod3 - t_mod3) % 3

        ok_mag = in_image(d_mag, ops2, rank2, 2)
        ok_sign = in_image(d_sign, ops2, rank2, 2)
        ok_mod3 = in_image(d_mod3, ops3, rank3, 3)

        orbit_counts["mag_mod2"][ok_mag] += 1
        orbit_counts["sign_mod2"][ok_sign] += 1
        orbit_counts["mod3"][ok_mod3] += 1

    print("Cohomology equivalence counts:")
    print(f"  mag_mod2: {dict(orbit_counts['mag_mod2'])}")
    print(f"  sign_mod2: {dict(orbit_counts['sign_mod2'])}")
    print(f"  mod3: {dict(orbit_counts['mod3'])}")

    out_path = ROOT / "docs" / "witting_triangle_cocycle_orbit.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Monomial group size: {len(group)}\n")
        f.write(f"mag_mod2: {dict(orbit_counts['mag_mod2'])}\n")
        f.write(f"sign_mod2: {dict(orbit_counts['sign_mod2'])}\n")
        f.write(f"mod3: {dict(orbit_counts['mod3'])}\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
