#!/usr/bin/env python3
"""
BT855 - The dark sector is K5-complete: the dodecahedra are the
        double covers of the dark-chart Kneser graph.

BT854 left the two dark dodecahedra and the meeting frame as the only
non-K5 residents of the pentad core.  Classical fact: the dodecahedron
graph is the antipodal double cover of the Petersen graph.  Tested:

  T1  K5-relation census: every dark line has a distinguished K5 edge
      (its shadow class); for each A5-orbit of dark pairs, the
      relation between the two lines' edges (same / adjacent /
      disjoint) is constant - the zoo is graded by K5 relations.
  T2  dodecahedron antipodes (distance-5 pairs) = the shadow-matching
      partners; the quotient by the matching is the PETERSEN graph on
      the 10 dark charts with adjacency = DISJOINTNESS of K5 edges
      (the Kneser graph K(5,2) in edge labels): each chiral dark
      dodecahedron is a double cover of the dark-chart Kneser graph.
  T3  the meeting frame's quotient: identify its 10-chart graph in K5
      terms (expected: the Johnson/triangular graph = adjacency).
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
    p1, p2 = [p for p in parts if len(p) == 5]
    o20 = sorted(next(p for p in parts if len(p) == 20))

    # lit charts and K5 edge labels
    lit_charts = []
    for a in p1:
        b = next(b for b in p2 if not (line_sets[a] & line_sets[b]))
        lit_charts.append((a, b))
    line_to_k5edge = {}
    for li in sset:
        serving = frozenset(
            ci for ci, (a, b) in enumerate(lit_charts)
            if line_sets[li] & line_sets[a] and line_sets[li] & line_sets[b])
        line_to_k5edge[li] = serving

    def shadow(li):
        return frozenset(m for m in sset if line_sets[li] & line_sets[m])

    def distinguished_edge(li):
        sh = shadow(li)
        edges = [line_to_k5edge[m] for m in sh]
        for e in edges:
            others = [f for f in edges if f != e]
            comp = frozenset(range(5)) - e
            if all(f <= comp for f in others):
                return e
        raise AssertionError

    edge_of = {li: distinguished_edge(li) for li in o20}

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

    def orb_kind(orb):
        if len(orb) == 10:
            return "matching"
        if len(orb) == 60:
            return "meeting"
        Gd = {v: set() for v in o20}
        for pr in orb:
            a, b = tuple(pr)
            Gd[a].add(b)
            Gd[b].add(a)
        comp0 = {o20[0]}
        fr2 = [o20[0]]
        while fr2:
            nx2 = []
            for u in fr2:
                for w in Gd[u]:
                    if w not in comp0:
                        comp0.add(w)
                        nx2.append(w)
            fr2 = nx2
        return "dodecahedron" if len(comp0) == 20 else "tetrads"

    # ----- T1: K5-relation census per orbit -----
    def rel(e, f):
        if e == f:
            return "same"
        return "adjacent" if e & f else "disjoint"

    census = {}
    for orb in pair_orbs:
        kinds = Counter(rel(edge_of[tuple(pr)[0]], edge_of[tuple(pr)[1]])
                        for pr in orb)
        key = f"{orb_kind(orb)}({len(orb)})"
        census.setdefault(key, []).append(dict(kinds))
        print(f"T1 {key}: K5 relations {dict(kinds)}")

    # ----- T2: dodecahedron = double cover of the Kneser graph -----
    dodecas = [o for o in pair_orbs if orb_kind(o) == "dodecahedron"]
    matching = next(o for o in pair_orbs if len(o) == 10)
    partner = {}
    for pr in matching:
        a, b = tuple(pr)
        partner[a] = b
        partner[b] = a
    t2 = []
    for di, orb in enumerate(dodecas):
        Gd = {v: set() for v in o20}
        for pr in orb:
            a, b = tuple(pr)
            Gd[a].add(b)
            Gd[b].add(a)
        # antipodes = unique distance-5 vertex
        anti_ok = True
        for s in o20:
            dist = {s: 0}
            dq = deque([s])
            while dq:
                u = dq.popleft()
                for w in Gd[u]:
                    if w not in dist:
                        dist[w] = dist[u] + 1
                        dq.append(w)
            far = [v for v, d in dist.items() if d == 5]
            if far != [partner[s]]:
                anti_ok = False
        # quotient by matching: vertices = 10 charts (edge labels);
        # adjacency from dodeca edges
        qadj = set()
        for pr in orb:
            a, b = tuple(pr)
            qadj.add(frozenset((tuple(sorted(edge_of[a])),
                                tuple(sorted(edge_of[b])))))
        # Petersen-as-Kneser check: adjacency iff K5 edges disjoint
        kneser = all(
            not (frozenset(x) & frozenset(y))
            for x, y in (tuple(q) for q in qadj))
        nedges = len(qadj)
        print(f"T2 dodecahedron {di}: antipode = matching partner: "
              f"{anti_ok}; quotient edges {nedges}, all disjoint-pairs "
              f"(Kneser/Petersen): {kneser}")
        t2.append({"antipode_is_partner": anti_ok,
                   "quotient_edges": nedges, "kneser": kneser})
        assert anti_ok and kneser and nedges == 15

    # ----- T3: meeting frame quotient -----
    meeting = next(o for o in pair_orbs if len(o) == 60)
    qadj = Counter()
    for pr in meeting:
        a, b = tuple(pr)
        qadj[frozenset((tuple(sorted(edge_of[a])),
                        tuple(sorted(edge_of[b]))))] += 1
    rels = Counter()
    for q, m in qadj.items():
        x, y = tuple(q)
        rels[(rel(frozenset(x), frozenset(y)), m)] += 1
    print(f"T3 meeting-frame quotient: {len(qadj)} chart pairs, "
          f"(relation, multiplicity) census {dict(rels)}")

    out = {
        "theorem": "BT855 dark sector K5-complete",
        "t1": census,
        "t2": t2,
        "t3": {str(k): v for k, v in rels.items()},
    }
    with open("data/bt855_dark_sector_k5_complete.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt855_dark_sector_k5_complete.json")


if __name__ == "__main__":
    main()
