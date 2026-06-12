#!/usr/bin/env python3
"""
BT854 - Dark chart/tetrad transversal duality: the dark sector's three
        structures are one structure.

BT853 named the dark sector's A5-orbits: a perfect matching of 10 dark
charts (skew pairs), two chiral 5xK4 partitions into skew tetrads, two
chiral dodecahedra, one meeting frame.  BT777: the 4 common
transversals of any chart are pairwise disjoint - a skew tetrad.

Conjecture tested here: the transversal tetrads of the 10 dark charts
are exactly the 10 K4 components (5 from each chiral partition) - the
matching and the two tetrad partitions are linked by the transversal
operation.  Also computed: where the dark transversals live (dark vs
lit vs schedule), and the induced map structure.
"""
from __future__ import annotations

from collections import Counter
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
    p1, p2 = [p for p in parts if len(p) == 5]
    o20 = sorted(next(p for p in parts if len(p) == 20))
    dark = set(o20)
    lit = set(p1) | set(p2)

    # dark pair orbits
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

    matching = next(o for o in pair_orbs if len(o) == 10)
    k4_orbs = []
    for o in pair_orbs:
        if len(o) == 30:
            # K4 partition iff 5 components of size 4 (girth 3)
            Gd = {v: set() for v in o20}
            for pr in o:
                a, b = tuple(pr)
                Gd[a].add(b)
                Gd[b].add(a)
            comps = []
            seen = set()
            for v in o20:
                if v in seen:
                    continue
                comp = {v}
                fr2 = [v]
                while fr2:
                    nx2 = []
                    for u in fr2:
                        for w in Gd[u]:
                            if w not in comp:
                                comp.add(w)
                                nx2.append(w)
                    fr2 = nx2
                seen |= comp
                comps.append(frozenset(comp))
            if all(len(c) == 4 for c in comps):
                k4_orbs.append(comps)
    assert len(k4_orbs) == 2
    tetrads = {t for comps in k4_orbs for t in comps}
    print(f"setup: 10 dark charts (matching), {len(tetrads)} K4 tetrads "
          f"(5 + 5 chiral)")

    # ----- T1: transversal tetrads of the dark charts -----
    def transversals(a, b):
        return frozenset(
            li for li in range(40)
            if li not in (a, b)
            and line_sets[li] & line_sets[a]
            and line_sets[li] & line_sets[b])

    hits = Counter()
    where = Counter()
    chart_to_tetrad = {}
    for pr in matching:
        a, b = tuple(pr)
        T = transversals(a, b)
        assert len(T) == 4
        loc = ("dark" if T <= dark else
               "lit" if T <= lit else
               "schedule" if T <= sset else "mixed")
        where[loc] += 1
        if T in tetrads:
            hits[True] += 1
            chart_to_tetrad[pr] = T
        else:
            hits[False] += 1
    print(f"T1 dark-chart transversal tetrads: location census {dict(where)}")
    print(f"T1 tetrad-match census: {dict(hits)}")

    if hits[True] == 10:
        # bijection? which chirality?
        used = Counter()
        for comps in k4_orbs:
            for t in comps:
                used[tuple(sorted(t))] = 0
        for T in chart_to_tetrad.values():
            used[tuple(sorted(T))] += 1
        print(f"T1 each tetrad used: {dict(Counter(used.values()))}")
        per_orb = [sum(1 for T in chart_to_tetrad.values() if T in comps)
                   for comps in k4_orbs]
        print(f"T1 split across the two chiral partitions: {per_orb}")

    # ----- T1b: the schedule shadow and the K5 structure -----
    # each dark line meets exactly 4 schedule lines (spread partitions
    # the points); a dark chart's two lines share the SAME 4-shadow
    # (that is why the matching exists).  Express shadows in the K5
    # labeling of BT847 (schedule line <-> pair of lit charts).
    lit_charts = []
    for a in p1:
        b = next(b for b in p2 if not (line_sets[a] & line_sets[b]))
        lit_charts.append((a, b))
    chart_idx = {c: i for i, c in enumerate(lit_charts)}
    line_to_k5edge = {}
    for li in sset:
        serving = frozenset(
            ci for ci, (a, b) in enumerate(lit_charts)
            if line_sets[li] & line_sets[a] and line_sets[li] & line_sets[b])
        assert len(serving) == 2
        line_to_k5edge[li] = serving

    def shadow(li):
        return frozenset(m for m in sset if line_sets[li] & line_sets[m])

    # verify matching = equal shadows
    same_shadow = all(shadow(tuple(pr)[0]) == shadow(tuple(pr)[1])
                      for pr in matching)
    print(f"T1b matched dark lines share their 4-line schedule shadow: "
          f"{same_shadow}")
    assert same_shadow

    # shadow in K5 terms: 4 schedule lines -> 4 K5 edges
    patterns = Counter()
    bijection = {}
    for pr in matching:
        a, _ = tuple(pr)
        sh = shadow(a)
        edges = [line_to_k5edge[m] for m in sh]
        # is it {e} + triangle on the complementary 3 vertices?
        found = None
        for e in edges:
            others = [f for f in edges if f != e]
            comp = frozenset(range(5)) - e
            if all(f <= comp for f in others) and len(set(others)) == 3:
                found = e
        patterns["edge+opposite_triangle" if found else "other"] += 1
        if found:
            bijection[pr] = found
    print(f"T1b shadow pattern census (in K5 edge terms): {dict(patterns)}")
    if patterns["edge+opposite_triangle"] == 10:
        distinct = len(set(bijection.values()))
        print(f"T1b distinct distinguished K5 edges: {distinct} of 10")
        print("    => CANONICAL BIJECTION dark chart <-> K5 edge <-> "
              "schedule line")

    # ----- T2: reverse - transversals of tetrad-internal pairs -----
    # each K4 edge is itself a dark skew pair (from a 30-orbit); where do
    # ITS transversals live?
    sample = next(iter(k4_orbs[0]))
    locs = Counter()
    for a, b in combinations(sorted(sample), 2):
        T = transversals(a, b)
        loc = ("dark" if T <= dark else
               "lit" if T <= lit else
               "schedule" if T <= sset else "mixed")
        locs[loc] += 1
    print(f"T2 transversals of one tetrad's 6 internal pairs: {dict(locs)}")

    # ----- T3: tetrads <-> K5 vertices (lit charts) -----
    # A tetrad contains NO matching pair (first guess refuted): its 4
    # lines lie in 4 DISTINCT shadow classes.  Conjecture: the 4
    # distinguished K5 edges form a STAR - all through one common
    # vertex - so each tetrad marks one lit chart, and the 5 tetrads
    # of each chiral partition mark all 5 exactly once.
    def distinguished_edge(li):
        sh = shadow(li)
        edges = [line_to_k5edge[m] for m in sh]
        for e in edges:
            others = [f for f in edges if f != e]
            comp = frozenset(range(5)) - e
            if all(f <= comp for f in others):
                return e
        raise AssertionError

    ok3 = True
    vertex_maps = []
    for pi, comps in enumerate(k4_orbs):
        seen_v = []
        for t in comps:
            edges = [distinguished_edge(li) for li in sorted(t)]
            common = frozenset(range(5))
            for e in edges:
                common = common & e
            if len(set(edges)) == 4 and len(common) == 1:
                seen_v.append(next(iter(common)))
            else:
                ok3 = False
        print(f"T3 partition {pi}: tetrad star-centers {sorted(seen_v)}")
        if sorted(seen_v) != [0, 1, 2, 3, 4]:
            ok3 = False
        vertex_maps.append(sorted(seen_v))
    print(f"T3 each tetrad's 4 distinguished edges = K5 STAR at one vertex;")
    print(f"   tetrads <-> K5 vertices (lit charts), both chiralities: {ok3}")
    assert ok3

    out = {
        "theorem": "BT854 dark chart-tetrad transversal duality",
        "t3": {"tetrads_are_k5_vertices": ok3},
        "t1": {"where": dict(where), "tetrad_hits": dict(hits)},
        "t1b": {"same_shadow": same_shadow,
                "patterns": dict(patterns),
                "distinct_edges": len(set(bijection.values()))},
        "t2": {"tetrad_pair_transversal_locations": dict(locs)},
    }
    with open("data/bt854_dark_chart_transversal_duality.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt854_dark_chart_transversal_duality.json")


if __name__ == "__main__":
    main()
