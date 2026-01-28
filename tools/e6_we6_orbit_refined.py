#!/usr/bin/env python3
"""Refined E6 embedding in E8 and orbit analysis.

Build E8 roots (scaled by 2 for integer arithmetic), then define E6 as the
subset orthogonal to u1=(1,1,1,1,1,1,1,1) and u2=(1,1,1,1,1,1,-1,-1).
Compute simple roots of E6 via a generic rho, and analyze W(E6) orbits
on the full E8 root set.
"""

from __future__ import annotations

import json
import random
from collections import Counter, deque
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_e8_roots_scaled():
    """Return E8 roots scaled by 2 as integer 8-tuples."""
    roots = []
    # Type 1: (+-1, +-1, 0^6) scaled by 2 => (+-2, +-2)
    for i in range(8):
        for j in range(i + 1, 8):
            for s1 in (2, -2):
                for s2 in (2, -2):
                    r = [0] * 8
                    r[i] = s1
                    r[j] = s2
                    roots.append(tuple(r))
    # Type 2: (+-1/2)^8 with even number of minus signs => (+-1)^8
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(signs))
    return roots


def dot(a, b):
    return sum(a[i] * b[i] for i in range(8))


def e6_subset(roots):
    """E6 roots are E8 roots orthogonal to u1 and u2."""
    u1 = (1, 1, 1, 1, 1, 1, 1, 1)
    u2 = (1, 1, 1, 1, 1, 1, -1, -1)
    return [r for r in roots if dot(r, u1) == 0 and dot(r, u2) == 0]


def pick_generic_rho(roots, seed=7):
    """Pick a random float rho not orthogonal to any root."""
    random.seed(seed)
    while True:
        rho = [random.random() for _ in range(8)]
        if all(abs(dot(r, rho)) > 1e-9 for r in roots):
            return rho


def simple_roots_from_positive(roots):
    """Compute simple roots from a positive system."""
    rho = pick_generic_rho(roots)
    pos = [r for r in roots if dot(r, rho) > 0]
    pos_set = set(pos)
    simples = []
    for r in pos:
        is_simple = True
        for s in pos:
            if s == r:
                continue
            t = tuple(r[i] - s[i] for i in range(8))
            if t in pos_set:
                is_simple = False
                break
        if is_simple:
            simples.append(r)
    return simples


def reflect(R, A):
    """Reflect root R across root A (scaled coords)."""
    # For scaled coords, A.A = 8 and R.A is divisible by 4
    k = dot(R, A) // 4
    return tuple(R[i] - k * A[i] for i in range(8))


def build_reflections(roots, simples):
    root_idx = {r: i for i, r in enumerate(roots)}
    perms = []
    for A in simples:
        perm = [0] * len(roots)
        for i, R in enumerate(roots):
            R2 = reflect(R, A)
            perm[i] = root_idx[R2]
        perms.append(perm)
    return perms


def orbit_size(perms, start=0):
    seen = {start}
    q = deque([start])
    while q:
        x = q.popleft()
        for g in perms:
            y = g[x]
            if y not in seen:
                seen.add(y)
                q.append(y)
    return len(seen), seen


def partition_orbits(perms, n):
    remaining = set(range(n))
    orbits = []
    while remaining:
        start = next(iter(remaining))
        size, orb = orbit_size(perms, start)
        orbits.append(orb)
        remaining -= orb
    return [len(o) for o in orbits]


def main():
    roots = build_e8_roots_scaled()
    e6 = e6_subset(roots)

    print("E8 roots:", len(roots))
    print("E6 roots:", len(e6))

    # Simple roots for E6
    simples = simple_roots_from_positive(e6)
    print("E6 simple roots found:", len(simples))

    # Build reflections and compute orbits on full E8 roots
    perms = build_reflections(roots, simples)

    # Orbit partition
    orbit_sizes = partition_orbits(perms, len(roots))
    orbit_sizes_sorted = sorted(orbit_sizes, reverse=True)
    print("W(E6) orbits on E8 roots:", orbit_sizes_sorted)

    results = {
        "e8_roots": len(roots),
        "e6_roots": len(e6),
        "e6_simple_roots": len(simples),
        "orbit_sizes": orbit_sizes_sorted,
    }

    out_path = ROOT / "artifacts" / "e6_we6_orbit_refined.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
