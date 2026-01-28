#!/usr/bin/env python3
"""Probe permutation symmetries of the Witting 40-ray basis incidence structure.

We restrict to monomial symmetries that preserve the 4 canonical basis states:
- permutations of coordinates (S4)
- phase multipliers by cube roots of unity on each coordinate (Z3^4)

We test which of these symmetries preserve the 40-ray set and the 40 bases.
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
    # projective normalization: divide by first nonzero component phase
    for x in v:
        if abs(x) > 1e-8:
            return v / x
    return v


def ray_key(v):
    v = normalize_ray(v)
    # round to reduce numerical issues
    return tuple(round(float(x.real), 6) + 1j * round(float(x.imag), 6) for x in v)


def main():
    rays = construct_witting_40_rays()
    bases = find_tetrads(rays)
    ray_map = {ray_key(v): i for i, v in enumerate(rays)}

    omega = np.exp(2j * np.pi / 3)
    phases = [1, omega, omega**2]

    valid = 0
    total = 0

    # Monomial group: permute coordinates and multiply by phases
    for perm in itertools.permutations(range(4)):
        for phase_tuple in itertools.product(phases, repeat=4):
            total += 1
            # Build transformation matrix implicitly
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

            # Check if bases map to bases
            mapped_bases = set()
            for base in bases:
                mb = tuple(sorted(mapped[i] for i in base))
                mapped_bases.add(mb)
            if mapped_bases == set(bases):
                valid += 1

    print("Monomial symmetry count:", valid)

    out = {
        "total_checked": total,
        "valid": valid,
        "group_order": valid,
    }
    out_path = ROOT / "artifacts" / "witting_monomial_symmetry.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
