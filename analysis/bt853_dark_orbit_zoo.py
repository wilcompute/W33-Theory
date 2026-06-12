#!/usr/bin/env python3
"""
BT853 - The dark orbit zoo: identifying all six A5-orbits on the
        pentad core's dark-line pairs.

BT847 split the 190 dark pairs as [10, 30, 30, 30, 30, 60] and
identified two 30-orbits as a chiral pair of dodecahedron skeletons,
leaving the others unnamed.  Here each orbit's graph is identified:
component structure, degree, girth - completing the dictionary.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, product
import json
import random


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def main():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    n = 40
    pt_index = {p: i for i, p in enumerate(pts)}

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    line_index = {l: i for i, l in enumerate(lines)}
    line_sets = [set(l) for l in lines]

    def transvection_perm(v):
        out = []
        for x in pts:
            w = symp(x, v)
            out.append(pt_index[canon(tuple(
                (x[t] + w * v[t]) % 3 for t in range(4)))])
        return tuple(out)

    gens = [transvection_perm(v) for v in pts]
    ident = tuple(range(n))

    def compose(a, b):
        return tuple(a[b[i]] for i in range(n))

    psp = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for gp in frontier:
            for h in gens:
                gh = compose(h, gp)
                if gh not in psp:
                    psp.add(gh)
                    nxt.append(gh)
        frontier = nxt
    psp = list(psp)

    def line_perm(gp):
        return tuple(line_index[frozenset(gp[x] for x in lines[li])]
                     for li in range(40))

    lperms = {gp: line_perm(gp) for gp in psp}

    def order_of(gp):
        o, cur = 1, gp
        while cur != ident:
            cur = compose(gp, cur)
            o += 1
        return o

    spread = None

    def bt(used, chosen, start):
        nonlocal spread
        if spread:
            return
        if len(chosen) == 10:
            spread = list(chosen)
            return
        for li in range(start, 40):
            if not (line_sets[li] & used):
                bt(used | line_sets[li], chosen + [li], li + 1)

    bt(set(), [], 0)
    sset = frozenset(spread)
    stab = [gp for gp in psp
            if frozenset(lperms[gp][li] for li in spread) == sset]

    rng = random.Random(23)
    fives = [gp for gp in stab if order_of(gp) == 5]
    threes = [gp for gp in stab if order_of(gp) == 3]

    def line_orbits(core):
        rem = set(range(40))
        parts = []
        while rem:
            seed = next(iter(rem))
            orb = {seed}
            fr = [seed]
            while fr:
                nxt = []
                for li in fr:
                    for gp in core:
                        li2 = lperms[gp][li]
                        if li2 not in orb:
                            orb.add(li2)
                            nxt.append(li2)
                fr = nxt
            parts.append(frozenset(orb))
            rem -= orb
        return parts

    core, parts = None, None
    while core is None:
        g5, g3 = rng.choice(fives), rng.choice(threes)
        sub = {ident}
        fr = [ident]
        while fr and len(sub) <= 60:
            nxt = []
            for x in fr:
                for h in (g5, g3):
                    y = compose(h, x)
                    if y not in sub:
                        sub.add(y)
                        nxt.append(y)
            fr = nxt
        if len(sub) == 60:
            ps = line_orbits(frozenset(sub))
            if sorted(len(p) for p in ps) == [5, 5, 10, 20]:
                core = frozenset(sub)
                parts = ps
    o20 = sorted(next(p for p in parts if len(p) == 20))

    # A5 orbits on dark-line pairs
    pair_orbs = []
    rem = {frozenset(pr) for pr in combinations(o20, 2)}
    while rem:
        seed = next(iter(rem))
        orb = set()
        a0, b0 = tuple(seed)
        for gp in core:
            lp = lperms[gp]
            orb.add(frozenset((lp[a0], lp[b0])))
        pair_orbs.append(orb)
        rem -= orb

    def analyze(orb):
        Gd = {v: set() for v in o20}
        for pr in orb:
            a, b = tuple(pr)
            Gd[a].add(b)
            Gd[b].add(a)
        degs = sorted({len(Gd[v]) for v in o20})
        comps = []
        seen = set()
        for v in o20:
            if v in seen:
                continue
            comp = {v}
            fr = [v]
            while fr:
                nxt = []
                for u in fr:
                    for w in Gd[u]:
                        if w not in comp:
                            comp.add(w)
                            nxt.append(w)
                fr = nxt
            seen |= comp
            comps.append(sorted(comp))
        # identify small components
        kinds = Counter()
        for comp in comps:
            m = sum(1 for a, b in combinations(comp, 2) if b in Gd[a])
            k = len(comp)
            if m == k * (k - 1) // 2:
                kinds[f"K{k}"] += 1
            elif m == k:
                kinds[f"C{k}"] += 1
            else:
                kinds[f"({k}v,{m}e)"] += 1
        # geometric tag: do paired lines meet (1 pt) or are they skew?
        meets = Counter()
        for pr in orb:
            a, b = tuple(pr)
            meets[len(line_sets[a] & line_sets[b])] += 1
        return degs, dict(kinds), dict(meets)

    results = []
    for orb in sorted(pair_orbs, key=len):
        degs, kinds, meets = analyze(orb)
        results.append({"size": len(orb), "degrees": degs,
                        "components": kinds, "line_meets": meets})
        print(f"orbit size {len(orb):3d}: degrees {degs}, "
              f"components {kinds}, pair line-intersections {meets}")

    out = {"theorem": "BT853 dark orbit zoo", "orbits": results}
    with open("data/bt853_dark_orbit_zoo.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt853_dark_orbit_zoo.json")


if __name__ == "__main__":
    main()
