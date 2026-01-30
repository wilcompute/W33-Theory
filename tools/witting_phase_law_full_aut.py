#!/usr/bin/env python3
"""Enumerate PSp(4,3) action and count phase-law preservers.

We generate the symplectic group from standard generators (as permutations
of W33 rays via the explicit ray->F3 mapping), then test the phase law on all
non-orthogonal triangles.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter, deque
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
    vectors = [v for v in itertools.product(F3, repeat=4) if any(x != 0 for x in v)]
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


def phase_cluster(angle):
    a = np.arctan2(np.sin(angle), np.cos(angle))
    targets = [np.pi / 6, -np.pi / 6, np.pi / 2, -np.pi / 2]
    nearest = min(targets, key=lambda t: abs(a - t))
    return round(float(nearest), 6)


def check_symplectic(M):
    Omega = [[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]]

    def mat_mult(A, B):
        n, k, m = len(A), len(B), len(B[0])
        res = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                for l in range(k):
                    res[i][j] = (res[i][j] + A[i][l] * B[l][j]) % 3
        return res

    MT = [[M[j][i] for j in range(4)] for i in range(4)]
    return mat_mult(mat_mult(MT, Omega), M) == Omega


def normalize_proj(v):
    v = list(v)
    for i in range(4):
        if v[i] != 0:
            inv = 1 if v[i] == 1 else 2
            v = [(x * inv) % 3 for x in v]
            break
    return tuple(v)


def apply_matrix(M, v):
    result = [sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4)]
    return normalize_proj(result)


def perm_from_matrix(M, mapping, f3_index):
    # mapping: ray -> f3 index; f3_index: f3 point -> index
    perm = []
    inv_mapping = {v: k for k, v in mapping.items()}
    for i in range(40):
        p = f3_points[mapping[i]]
        p2 = apply_matrix(M, p)
        idx2 = f3_index[p2]
        perm.append(inv_mapping[idx2])
    return tuple(perm)


def main():
    rays = construct_witting_40_rays()
    global f3_points
    f3_points = construct_f3_points()
    f3_index = {tuple(p): i for i, p in enumerate(f3_points)}

    mapping_path = ROOT / "artifacts" / "witting_graph_isomorphism.json"
    mapping = {
        int(k): int(v)
        for k, v in json.loads(mapping_path.read_text())["mapping"].items()
    }

    # symplectic generators
    gen_matrices = [
        [[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1]],
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 2, 1]],
        [[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 2], [0, 0, 0, 1]],
        [[0, 0, 1, 0], [0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0]],
    ]
    gens = [M for M in gen_matrices if check_symplectic(M)]
    gen_perms = [perm_from_matrix(M, mapping, f3_index) for M in gens]

    # group enumeration (BFS)
    group = set()
    queue = deque()
    id_perm = tuple(range(40))
    group.add(id_perm)
    queue.append(id_perm)

    while queue:
        p = queue.popleft()
        for g in gen_perms:
            comp = tuple(p[g[i]] for i in range(40))
            if comp not in group:
                group.add(comp)
                queue.append(comp)

    # precompute triangle phases and signs
    overlap = {}
    n = len(rays)
    for i in range(n):
        for j in range(i + 1, n):
            overlap[(i, j)] = np.vdot(rays[i], rays[j])

    triangles = []
    tri_phase = []
    tri_sign = []
    for i, j, k in itertools.combinations(range(n), 3):
        ip_ij = overlap[(i, j)]
        ip_jk = overlap[(j, k)]
        ip_ik = overlap[(i, k)]
        if abs(ip_ij) < 1e-8 or abs(ip_jk) < 1e-8 or abs(ip_ik) < 1e-8:
            continue
        prod = ip_ij * ip_jk * np.conjugate(ip_ik)
        if abs(prod) < 1e-12:
            continue
        triangles.append((i, j, k))
        tri_phase.append(phase_cluster(np.angle(prod)))
        p_i = f3_points[mapping[i]]
        p_j = f3_points[mapping[j]]
        p_k = f3_points[mapping[k]]
        w12 = omega_symp(p_i, p_j)
        w23 = omega_symp(p_j, p_k)
        w31 = omega_symp(p_k, p_i)
        sign = (
            (1 if w12 == 1 else -1) * (1 if w23 == 1 else -1) * (1 if w31 == 1 else -1)
        )
        tri_sign.append(sign)

    tri_index = {tuple(sorted(t)): idx for idx, t in enumerate(triangles)}
    allowed = {
        -1: set([-0.523599, 1.570796]),
        1: set([0.523599, -1.570796]),
    }

    violations = Counter()
    for p in group:
        bad = 0
        for idx, (i, j, k) in enumerate(triangles):
            ii, jj, kk = p[i], p[j], p[k]
            if ii == jj or jj == kk or ii == kk:
                continue
            a, b, c = sorted((ii, jj, kk))
            jdx = tri_index.get((a, b, c))
            if jdx is None:
                continue
            ph = tri_phase[jdx]
            if ph not in allowed[tri_sign[idx]]:
                bad += 1
        violations[bad] += 1

    out = {
        "group_size": len(group),
        "violations": {str(k): v for k, v in sorted(violations.items())},
        "preserving": violations.get(0, 0),
    }

    out_path = ROOT / "artifacts" / "witting_phase_law_full_aut.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_phase_law_full_aut.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Phase-Law Preservation over PSp(4,3)\n\n")
        f.write(f"Group size: **{len(group)}**\n\n")
        f.write(f"Preserving elements: **{out['preserving']}**\n\n")
        f.write("violations | elements\n")
        f.write("--- | ---\n")
        for k, v in sorted(violations.items()):
            f.write(f"{k} | {v}\n")
    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
