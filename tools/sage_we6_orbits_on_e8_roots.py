#!/usr/bin/env python3
"""Sage: compute W(E6) orbits on E8 roots via parabolic subgroup.

We use the ambient space model for E8 roots so Weyl group actions apply.
Outputs an artifact with orbit sizes and sample reps.
"""

from __future__ import annotations

import json
from collections import Counter, deque

from sage.all import RootSystem, WeylGroup


def act(g, v):
    """Apply Weyl group element to ambient-space vector v."""
    try:
        return g.action(v)
    except Exception:
        try:
            return g * v
        except Exception:
            return g.matrix() * v


def orbit(generators, start):
    """Compute orbit under generators."""
    seen = {start}
    q = deque([start])
    while q:
        x = q.popleft()
        for g in generators:
            y = act(g, x)
            if y not in seen:
                seen.add(y)
                q.append(y)
    return seen


def vec_to_list(v):
    try:
        coords = list(v.to_vector())
    except Exception:
        coords = list(v)
    out = []
    for x in coords:
        try:
            out.append(float(x))
        except Exception:
            # Fallback for nested tuples
            out.append(float(x[0]))
    return out


def main():
    R8 = RootSystem(["E", 8]).ambient_space()
    roots = list(R8.roots())
    print(f"E8 roots: {len(roots)}")

    W8 = WeylGroup(["E", 8])
    s = W8.simple_reflections()

    # Subset (1..6) yields W(E6) (order 51840)
    subset = [1, 2, 3, 4, 5, 6]
    gens = [s[i] for i in subset]
    WE6 = W8.subgroup(gens)
    print(f"W(E6) order (as subgroup of W(E8)): {WE6.order()}")

    # Compute orbits on roots
    remaining = set(roots)
    orbits = []
    while remaining:
        r = next(iter(remaining))
        orb = orbit(gens, r)
        orbits.append(orb)
        remaining -= orb

    sizes = sorted([len(o) for o in orbits], reverse=True)
    print(f"Number of orbits: {len(orbits)}")
    print(f"Orbit sizes: {sizes}")

    size_counts = Counter(sizes)
    print("Orbit size multiplicities:")
    for size in sorted(size_counts):
        print(f"  {size}: {size_counts[size]}")

    # Representatives for each orbit size
    reps = {}
    for size in size_counts:
        reps[size] = [vec_to_list(next(iter(o))) for o in orbits if len(o) == size][:3]

    # Save artifact
    out = {
        "we6_order": int(WE6.order()),
        "orbit_sizes": sizes,
        "orbit_size_counts": dict(size_counts),
        "representatives": reps,
        "decomposition": "72 + 6*27 + 6*1 = 240",
    }

    with open("artifacts/we6_orbits_on_e8_roots.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)

    print("Wrote artifacts/we6_orbits_on_e8_roots.json")


if __name__ == "__main__":
    main()
