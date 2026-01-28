#!/usr/bin/env python3
"""Compute monomial symmetry subgroup preserving the 24-basis subset.

We restrict to monomial transformations: coordinate permutations (S4)
with independent cube-root phases (Z3^4). We test which preserve:
- the 40-ray set
- the 24-basis subset (as a set)

Outputs subgroup order and orbit sizes on rays and bases.
"""
from __future__ import annotations

import itertools
import json
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


def orthogonal(v1, v2, tol=1e-8):
    return abs(np.vdot(v1, v2)) < tol


def find_tetrads(rays):
    n = len(rays)
    ortho = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if orthogonal(rays[i], rays[j]):
                ortho[i, j] = ortho[j, i] = True
    tetrads = []
    for a in range(n):
        for b in range(a + 1, n):
            if not ortho[a, b]:
                continue
            for c in range(b + 1, n):
                if not (ortho[a, c] and ortho[b, c]):
                    continue
                for d in range(c + 1, n):
                    if ortho[a, d] and ortho[b, d] and ortho[c, d]:
                        tetrads.append((a, b, c, d))
    return tetrads


def normalize_ray(v):
    for x in v:
        if abs(x) > 1e-8:
            return v / x
    return v


def ray_key(v):
    v = normalize_ray(v)
    return tuple(round(float(x.real), 6) + 1j * round(float(x.imag), 6) for x in v)


def main():
    rays = construct_witting_40_rays()
    bases = find_tetrads(rays)
    ray_map = {ray_key(v): i for i, v in enumerate(rays)}

    # Load 24-basis subset indices
    subset_path = ROOT / "artifacts" / "witting_ks_reduce_bases.json"
    if not subset_path.exists():
        print("Missing artifacts/witting_ks_reduce_bases.json")
        return
    subset_indices = json.loads(subset_path.read_text()).get("bases", [])
    subset_bases = {tuple(sorted(bases[i])) for i in subset_indices}

    omega = np.exp(2j * np.pi / 3)
    phases = [1, omega, omega**2]

    valid = 0
    perms = []

    for perm in itertools.permutations(range(4)):
        for phase_tuple in itertools.product(phases, repeat=4):
            mapped = []
            ok = True
            for v in rays:
                w = np.array([phase_tuple[i] * v[perm[i]] for i in range(4)], dtype=complex)
                key = ray_key(w)
                if key not in ray_map:
                    ok = False
                    break
                mapped.append(ray_map[key])
            if not ok:
                continue

            mapped_subset = set()
            for base in subset_bases:
                mb = tuple(sorted(mapped[i] for i in base))
                mapped_subset.add(mb)

            if mapped_subset == subset_bases:
                valid += 1
                perms.append(mapped)

    # Compute orbits on rays and bases under the subgroup
    ray_orbits = []
    seen = set()
    for i in range(len(rays)):
        if i in seen:
            continue
        orbit = set()
        stack = [i]
        while stack:
            x = stack.pop()
            if x in orbit:
                continue
            orbit.add(x)
            for p in perms:
                y = p[x]
                if y not in orbit:
                    stack.append(y)
        seen |= orbit
        ray_orbits.append(sorted(orbit))

    base_orbits = []
    seen_b = set()
    subset_list = list(subset_bases)
    base_index = {b: i for i, b in enumerate(subset_list)}

    for b in subset_list:
        if b in seen_b:
            continue
        orbit = set()
        stack = [b]
        while stack:
            bb = stack.pop()
            if bb in orbit:
                continue
            orbit.add(bb)
            for p in perms:
                mb = tuple(sorted(p[i] for i in bb))
                if mb not in orbit:
                    stack.append(mb)
        seen_b |= orbit
        base_orbits.append(sorted(list(orbit), key=lambda x: base_index[x]))

    out = {
        "subgroup_order": valid,
        "ray_orbit_sizes": sorted([len(o) for o in ray_orbits], reverse=True),
        "basis_orbit_sizes": sorted([len(o) for o in base_orbits], reverse=True),
    }

    out_path = ROOT / "artifacts" / "witting_24basis_symmetry.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
