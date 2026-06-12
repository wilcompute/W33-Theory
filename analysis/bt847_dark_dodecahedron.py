#!/usr/bin/env python3
"""
BT847 - The dark dodecahedron and the chart pentagon.

Closing BT846's two opens:

  T1  the 20-line dark carrier: A5-orbits on its C(20,2) = 190 pairs;
      if a 30-orbit exists, test its graph for the DODECAHEDRON
      skeleton (3-regular, girth 5, diameter 5, vertex-transitive on
      20 = the unique such with these parameters vs Desargues girth 6).
  T2  the schedule-line -> chart-pair map: the multigraph it induces
      on the 5 charts (10 lines, each joining one pair of charts):
      2.K5, pentagon+pentagram, or other.
"""
from __future__ import annotations

from itertools import combinations, product
from collections import Counter
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
    assert len(lines) == 40
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
    assert len(psp) == 25920
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

    rng = random.Random(23)   # same seed as BT846 -> same core
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

    # ----- T1: A5 orbits on pairs of the 20-orbit -----
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
    sizes = sorted(len(o) for o in pair_orbs)
    print(f"T1 A5 orbits on the 190 dark-line pairs: {sizes}")

    def graph_profile(edges, verts):
        Gd = {v: set() for v in verts}
        for pr in edges:
            a, b = tuple(pr)
            Gd[a].add(b)
            Gd[b].add(a)
        degs = sorted({len(Gd[v]) for v in Gd})
        # girth (BFS per vertex)
        import collections
        girth = None
        for s in verts:
            dist = {s: 0}
            par = {s: None}
            dq = collections.deque([s])
            while dq:
                u = dq.popleft()
                for w in Gd[u]:
                    if w not in dist:
                        dist[w] = dist[u] + 1
                        par[w] = u
                        dq.append(w)
                    elif par[u] != w:
                        cyc = dist[u] + dist[w] + 1
                        if girth is None or cyc < girth:
                            girth = cyc
        # diameter
        diam = 0
        conn = True
        for s in verts:
            dist = {s: 0}
            dq = collections.deque([s])
            while dq:
                u = dq.popleft()
                for w in Gd[u]:
                    if w not in dist:
                        dist[w] = dist[u] + 1
                        dq.append(w)
            if len(dist) < len(verts):
                conn = False
            else:
                diam = max(diam, max(dist.values()))
        return degs, girth, diam, conn

    n_dodeca = 0
    profiles = []
    for orb in pair_orbs:
        if len(orb) == 30:
            degs, girth, diam, conn = graph_profile(orb, o20)
            is_d = degs == [3] and girth == 5 and diam == 5 and conn
            profiles.append((degs, girth, diam, conn, is_d))
            print(f"T1 30-orbit graph: degrees {degs}, girth {girth}, "
                  f"diameter {diam}, connected {conn}, dodecahedron {is_d}")
            if is_d:
                n_dodeca += 1
    print(f"T1 dark carrier dodecahedron count: {n_dodeca} "
          f"of {len(profiles)} 30-orbits")

    # ----- T2: chart multigraph from schedule lines -----
    charts = []
    for a in p1:
        b = next(b for b in p2 if not (line_sets[a] & line_sets[b]))
        charts.append((a, b))
    edge_count = Counter()
    for li in sset:
        serving = [ci for ci, (a, b) in enumerate(charts)
                   if line_sets[li] & line_sets[a]
                   and line_sets[li] & line_sets[b]]
        assert len(serving) == 2
        edge_count[frozenset(serving)] += 1
    mult = Counter(edge_count.values())
    npairs = len(edge_count)
    print(f"T2 chart multigraph: {npairs} distinct chart pairs, "
          f"multiplicities {dict(mult)}")
    if npairs == 10 and mult == {1: 10}:
        verdict = ("K5 exactly: schedule lines <-> chart pairs bijectively"
                   " (10 lines = C(5,2) pairs)")
    elif npairs == 5:
        deg = Counter()
        for prr in edge_count:
            for c in prr:
                deg[c] += 1
        cyc = sorted(deg.values())
        verdict = f"5 pairs x2 = pentagon or pentagram (degrees {cyc})"
    else:
        verdict = f"other ({npairs} pairs)"
    print(f"T2 verdict: {verdict}")

    out = {
        "theorem": "BT847 dark dodecahedron and chart pentagon",
        "t1": {"pair_orbit_sizes": sizes, "dodecahedra": n_dodeca,
               "thirty_orbits": len(profiles)},
        "t2": {"distinct_chart_pairs": npairs,
               "multiplicities": {str(k): v for k, v in mult.items()},
               "verdict": verdict},
    }
    with open("data/bt847_dark_dodecahedron.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt847_dark_dodecahedron.json")


if __name__ == "__main__":
    main()
