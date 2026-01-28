#!/usr/bin/env python3
"""Analyze Z3 edge labels by monomial-group orbits on non-orth edges."""

from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
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
            phase_vec = np.array(
                [omega**a0, omega**a1, omega**a2, omega**a3], dtype=complex
            )
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


def phase_to_k(angle):
    return int(np.rint(angle / (np.pi / 6.0))) % 12


def solve_edge_potential(rays):
    edges = build_nonorth_edges(rays)
    edge_index = {e: idx for idx, e in enumerate(edges)}
    triangles = []
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


def main():
    print("Z3 EDGE LABELS BY MONOMIAL ORBITS")
    print("=" * 60)
    rays = construct_witting_40_rays()
    edges, labels = solve_edge_potential(rays)

    edge_index = {e: idx for idx, e in enumerate(edges)}

    group = build_monomial_group(rays)
    print(f"Monomial group size: {len(group)}")

    # build edge permutation generators from group elements
    edge_maps = []
    for g in group:
        emap = []
        for i, j in edges:
            a, b = g[i], g[j]
            if a > b:
                a, b = b, a
            emap.append(edge_index[(a, b)])
        edge_maps.append(emap)

    # orbit decomposition
    seen = set()
    orbits = []
    for e_idx in range(len(edges)):
        if e_idx in seen:
            continue
        orb = set()
        queue = deque([e_idx])
        seen.add(e_idx)
        while queue:
            cur = queue.popleft()
            orb.add(cur)
            for emap in edge_maps:
                nxt = emap[cur]
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        orbits.append(sorted(orb))

    print(f"Number of edge orbits: {len(orbits)}")
    sizes = [len(o) for o in orbits]
    print(f"Orbit sizes: {sorted(sizes)}")

    # label distribution per orbit
    out_path = ROOT / "docs" / "witting_z3_edge_orbits.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Orbits: {len(orbits)}\n")
        f.write(f"Sizes: {sorted(sizes)}\n")
        for idx, orb in enumerate(orbits):
            dist = Counter(int(labels[e]) for e in orb)
            f.write(f"Orbit {idx} size {len(orb)} label dist {dict(dist)}\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
