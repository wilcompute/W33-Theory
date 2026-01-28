#!/usr/bin/env python3
"""Search different Coxeter element orderings and compare pattern-class histograms.

We sample random permutations of simple reflections (1..8), build Coxeter element
c = s_{p1}...s_{p8}, compute c^5 (order-6), build Coxeter-6 orbits, and compare
intersection-pattern histogram with W(E6) orbit decomposition.

Outputs artifacts/coxeter_gauge_search.json
"""
from __future__ import annotations

import json
import random
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


def coxeter_orbits(roots, c5):
    remaining = set(roots)
    orbits = []
    while remaining:
        r = next(iter(remaining))
        orb = {r}
        cur = r
        for _ in range(5):
            cur = act(c5, cur)
            orb.add(cur)
        orbits.append(orb)
        remaining -= orb
    return orbits


def we6_orbits(roots, s):
    gens = [s[i] for i in [1,2,3,4,5,6]]
    remaining = set(roots)
    orbits = []
    while remaining:
        r = next(iter(remaining))
        orb = orbit(gens, r)
        orbits.append(orb)
        remaining -= orb
    # sort by size desc
    orbits = sorted(orbits, key=lambda o: -len(o))
    return orbits


def pattern_hist(c6_orbits, we6_orbits):
    patterns = []
    for o6 in c6_orbits:
        row = [len(o6 & ow) for ow in we6_orbits]
        patterns.append(tuple(row))
    return Counter(patterns)


def main():
    R8 = RootSystem(['E',8]).ambient_space()
    roots = list(R8.roots())
    W8 = WeylGroup(['E',8])
    s = W8.simple_reflections()

    we6 = we6_orbits(roots, s)
    base_perm = list(range(1,9))

    results = []
    for t in range(20):
        perm = base_perm[:]
        random.shuffle(perm)
        c = s[perm[0]]
        for i in perm[1:]:
            c = c * s[i]
        c5 = c**5
        c6 = coxeter_orbits(roots, c5)
        hist = pattern_hist(c6, we6)
        # encode histogram as sorted list of (pattern,count)
        key = sorted([(str(k), v) for k, v in hist.items()])
        results.append({"perm": perm, "hist": key})
        print(f"trial {t+1}: distinct patterns {len(hist)}")

    out = {"trials": results}
    with open("artifacts/coxeter_gauge_search.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("Wrote artifacts/coxeter_gauge_search.json")


if __name__ == "__main__":
    main()
