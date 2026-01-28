#!/usr/bin/env python3
"""Find monomial subgroup elements that preserve the phase law.

For each monomial symmetry g (order 243), we transport the ray→F3 mapping by
  m_g = m ∘ g^{-1}
and test if the phase law holds for all non-orthogonal triangles.
We count how many g give zero violations.
"""
from __future__ import annotations

import json
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
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def phase_cluster(angle):
    a = np.arctan2(np.sin(angle), np.cos(angle))
    targets = [np.pi/6, -np.pi/6, np.pi/2, -np.pi/2]
    nearest = min(targets, key=lambda t: abs(a - t))
    return round(float(nearest), 6)


def main():
    rays = construct_witting_40_rays()
    f3_points = construct_f3_points()
    mapping_path = ROOT / "artifacts" / "witting_graph_isomorphism.json"
    base_map = {int(k): int(v) for k, v in json.loads(mapping_path.read_text())["mapping"].items()}

    # precompute overlaps and triangle phases
    n = len(rays)
    overlap = {}
    for i in range(n):
        for j in range(i + 1, n):
            overlap[(i, j)] = np.vdot(rays[i], rays[j])

    triangles = []
    tri_phase = []
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

    allowed = {
        -1: set([-0.523599, 1.570796]),
        1: set([0.523599, -1.570796]),
    }

    group = build_monomial_group(rays)
    violations = Counter()

    for g in group:
        # compute inverse permutation
        inv = [0]*n
        for i, gi in enumerate(g):
            inv[gi] = i
        # transported mapping
        def m(i):
            return base_map[inv[i]]

        bad = 0
        for idx, (i, j, k) in enumerate(triangles):
            p_i = f3_points[m(i)]
            p_j = f3_points[m(j)]
            p_k = f3_points[m(k)]
            w12 = omega_symp(p_i, p_j)
            w23 = omega_symp(p_j, p_k)
            w31 = omega_symp(p_k, p_i)
            sign = (1 if w12 == 1 else -1) * (1 if w23 == 1 else -1) * (1 if w31 == 1 else -1)
            if tri_phase[idx] not in allowed[sign]:
                bad += 1
        violations[bad] += 1

    out = {
        "group_size": len(group),
        "triangles": len(triangles),
        "violations": {str(k): v for k, v in sorted(violations.items())},
        "preserving": violations.get(0, 0),
    }

    out_path = ROOT / "artifacts" / "witting_phase_law_monomial_subgroup.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_phase_law_monomial_subgroup.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Phase‑Law Preservers in Monomial Group\n\n")
        f.write(f"Monomial group size: **{len(group)}**\n")
        f.write(f"Triangles: **{len(triangles)}**\n")
        f.write(f"Preserving elements (0 violations): **{out['preserving']}**\n\n")
        f.write("violations | elements\n")
        f.write("--- | ---\n")
        for k, v in sorted(violations.items()):
            f.write(f"{k} | {v}\n")
    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
