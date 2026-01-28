#!/usr/bin/env python3
"""Analyze Z3 edge potential labels vs ray families and symplectic data."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import product
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


def construct_f3_points():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]
    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)
    return proj_points


def omega_symp(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build_nonorth_edges(rays, tol=1e-8):
    edges = []
    for i in range(len(rays)):
        for j in range(i + 1, len(rays)):
            if abs(np.vdot(rays[i], rays[j])) >= tol:
                edges.append((i, j))
    return edges


def phase_to_k(angle):
    return int(np.rint(angle / (np.pi / 6.0))) % 12


def solve_edge_potential(rays):
    edges = build_nonorth_edges(rays)
    triangles = []
    edge_index = {e: idx for idx, e in enumerate(edges)}
    for i in range(40):
        for j in range(i + 1, 40):
            if (i, j) not in edge_index:
                continue
            for k in range(j + 1, 40):
                if (i, k) in edge_index and (j, k) in edge_index:
                    triangles.append((i, j, k))

    d1 = np.zeros((len(triangles), len(edges)), dtype=int)
    t = np.zeros(len(triangles), dtype=int)
    for t_idx, (i, j, k) in enumerate(triangles):
        e_jk = edge_index[(j, k)]
        e_ik = edge_index[(i, k)]
        e_ij = edge_index[(i, j)]
        d1[t_idx, e_jk] = 1
        d1[t_idx, e_ik] = -1
        d1[t_idx, e_ij] = 1
        ip = (
            np.vdot(rays[i], rays[j])
            * np.vdot(rays[j], rays[k])
            * np.conjugate(np.vdot(rays[i], rays[k]))
        )
        t[t_idx] = phase_to_k(np.angle(ip)) % 3

    # solve d1 x = t over GF(3)
    A = d1.copy() % 3
    b = t.copy() % 3
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
    x = np.zeros(n, dtype=int)
    for col, r in enumerate(piv):
        if r != -1:
            x[col] = b[r] % 3
    return edges, x


def ray_family(idx):
    if idx < 4:
        return ("B", None, None)
    t = idx - 4
    pair = t // 4
    fam = t % 4
    mu = pair // 3
    nu = pair % 3
    return (f"F{fam}", mu, nu)


def main():
    print("Z3 EDGE POTENTIAL ANALYSIS")
    print("=" * 60)
    rays = construct_witting_40_rays()
    edges, x = solve_edge_potential(rays)

    # load ray->F3 mapping (graph isomorphism)
    map_path = ROOT / "artifacts" / "witting_graph_isomorphism.json"
    if map_path.exists():
        mapping = json.loads(map_path.read_text())
        ray_to_f3_idx = {int(k): int(v) for k, v in mapping["mapping"].items()}
        f3_points = construct_f3_points()
    else:
        ray_to_f3_idx = None
        f3_points = None

    label_dist = Counter(x)
    print(f"Edge labels: {dict(label_dist)}")

    # by family pair
    fam_counts = defaultdict(Counter)
    for idx, (i, j) in enumerate(edges):
        fi, mui, nui = ray_family(i)
        fj, muj, nuj = ray_family(j)
        key = tuple(sorted((fi, fj)))
        fam_counts[key][int(x[idx])] += 1

    # by basis involvement
    basis_counts = Counter()
    for idx, (i, j) in enumerate(edges):
        bi = i < 4
        bj = j < 4
        key = "BB" if bi and bj else "BN" if (bi or bj) else "NN"
        basis_counts[(key, int(x[idx]))] += 1

    # by omega if mapping present
    omega_counts = Counter()
    if ray_to_f3_idx is not None:
        for idx, (i, j) in enumerate(edges):
            pi = f3_points[ray_to_f3_idx[i]]
            pj = f3_points[ray_to_f3_idx[j]]
            w = omega_symp(pi, pj)
            omega_counts[(w, int(x[idx]))] += 1

    out_path = ROOT / "docs" / "witting_z3_edge_potential_analysis.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Edge label distribution: {dict(label_dist)}\n")
        f.write("\nFamily-pair counts by label:\n")
        for key in sorted(fam_counts.keys()):
            f.write(f"  {key}: {dict(fam_counts[key])}\n")
        f.write("\nBasis involvement counts (BB/BN/NN) by label:\n")
        for key in sorted(basis_counts.keys()):
            f.write(f"  {key}: {basis_counts[key]}\n")
        if omega_counts:
            f.write("\nOmega_symp counts by label:\n")
            for key in sorted(omega_counts.keys()):
                f.write(f"  {key}: {omega_counts[key]}\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
