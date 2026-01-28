#!/usr/bin/env python3
"""Compute triangle orbits under monomial symmetries by phase cluster.

We build the monomial symmetry group (243 elements) that preserves the 40-ray set,
then compute orbit sizes on the 3240 non-orthogonal triangles, separated by
phase cluster (±pi/6, ±pi/2).
"""
from __future__ import annotations

import json
import itertools
from collections import defaultdict, Counter
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


def phase_cluster(angle):
    a = np.arctan2(np.sin(angle), np.cos(angle))
    targets = [np.pi/6, -np.pi/6, np.pi/2, -np.pi/2]
    nearest = min(targets, key=lambda t: abs(a - t))
    return round(float(nearest), 6)


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


def main():
    rays = construct_witting_40_rays()
    n = len(rays)
    group = build_monomial_group(rays)

    # collect non-orthogonal triangles and their phase clusters
    triangles = []
    tri_phase = []
    for i, j, k in itertools.combinations(range(n), 3):
        ip_ij = np.vdot(rays[i], rays[j])
        ip_jk = np.vdot(rays[j], rays[k])
        ip_ik = np.vdot(rays[i], rays[k])
        if abs(ip_ij) < 1e-8 or abs(ip_jk) < 1e-8 or abs(ip_ik) < 1e-8:
            continue
        prod = ip_ij * ip_jk * np.conjugate(ip_ik)
        if abs(prod) < 1e-12:
            continue
        triangles.append(tuple(sorted((i, j, k))))
        tri_phase.append(phase_cluster(np.angle(prod)))

    tri_index = {t: idx for idx, t in enumerate(triangles)}

    # compute orbits
    visited = set()
    orbit_sizes = defaultdict(list)  # phase -> list of sizes

    for idx, tri in enumerate(triangles):
        if idx in visited:
            continue
        # BFS orbit
        orbit = set([idx])
        queue = [tri]
        while queue:
            t = queue.pop()
            for g in group:
                tt = tuple(sorted((g[t[0]], g[t[1]], g[t[2]])))
                j = tri_index.get(tt)
                if j is not None and j not in orbit:
                    orbit.add(j)
                    queue.append(tt)
        for j in orbit:
            visited.add(j)
        # phase class of this orbit (use first element)
        ph = tri_phase[next(iter(orbit))]
        orbit_sizes[ph].append(len(orbit))

    out = {
        "group_elements": len(group),
        "triangles": len(triangles),
        "orbit_sizes_by_phase": {
            str(k): Counter(v) for k, v in orbit_sizes.items()
        },
    }

    out_path = ROOT / "artifacts" / "witting_triangle_phase_orbits.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_triangle_phase_orbits.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Triangle Orbits under Monomial Symmetries\n\n")
        f.write(f"Group elements: **{len(group)}**\n\n")
        f.write(f"Non‑orthogonal triangles: **{len(triangles)}**\n\n")
        f.write("## Orbit size distributions by phase cluster\n\n")
        for ph in sorted(orbit_sizes.keys()):
            f.write(f"### Phase {ph}\n\n")
            f.write("orbit size | count\n")
            f.write("--- | ---\n")
            counts = Counter(orbit_sizes[ph])
            for size, cnt in sorted(counts.items()):
                f.write(f"{size} | {cnt}\n")
            f.write("\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
