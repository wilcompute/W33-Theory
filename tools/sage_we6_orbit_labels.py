#!/usr/bin/env python3
"""Sage: label each E8 root by its W(E6) orbit (parabolic subgroup s1..s6).

Outputs artifacts/we6_orbit_labels.json with:
- root_key = tuple of 2*coords (integers)
- orbit_id, orbit_size
- summary sizes
"""

from __future__ import annotations

import json
from collections import Counter, deque

from sage.all import RootSystem, WeylGroup


def act(g, v):
    try:
        return g.action(v)
    except Exception:
        try:
            return g * v
        except Exception:
            return g.matrix() * v


def orbit(generators, start):
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


def root_key(v):
    vec = list(v.to_vector())
    return tuple(int(2 * x) for x in vec)


def main():
    R8 = RootSystem(["E", 8]).ambient_space()
    roots = list(R8.roots())

    W8 = WeylGroup(["E", 8])
    s = W8.simple_reflections()
    subset = [1, 2, 3, 4, 5, 6]
    gens = [s[i] for i in subset]
    WE6 = W8.subgroup(gens)

    # Orbits
    remaining = set(roots)
    orbits = []
    while remaining:
        r = next(iter(remaining))
        orb = orbit(gens, r)
        orbits.append(orb)
        remaining -= orb

    sizes = [len(o) for o in orbits]
    size_counts = Counter(sizes)

    mapping = {}
    for oid, orb in enumerate(orbits):
        osize = len(orb)
        for r in orb:
            mapping[str(root_key(r))] = {
                "orbit_id": oid,
                "orbit_size": osize,
            }

    out = {
        "we6_order": int(WE6.order()),
        "orbit_sizes": sorted(sizes, reverse=True),
        "orbit_size_counts": dict(size_counts),
        "mapping": mapping,
    }

    with open("artifacts/we6_orbit_labels.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)

    print("Wrote artifacts/we6_orbit_labels.json")


if __name__ == "__main__":
    main()
