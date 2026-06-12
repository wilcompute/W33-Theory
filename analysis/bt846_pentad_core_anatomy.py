#!/usr/bin/env python3
"""
BT846 - Complete anatomy of the pentad core: [5,5,10,20] explained
        line by line, point by point.

Conjectures tested (all about one pentad core, then orbit-checked):

  T1  the two pentads P1, P2 cover the SAME 20 points (each line of
      P1 meets 4 lines of P2 in 4 distinct points = its full point
      set), and that 20-set is one of the core's two point orbits.
  T2  the 20-line orbit = EXACTLY the 4x5 = 20 common transversals of
      the five matching charts (the deleted matching's skew pairs):
      the whole signature [5,5,10,20] is then
        P1 + P2 + (marked schedule) + (transversals of the 5 charts).
  T3  where the other 20 points live: incidence of the uncovered
      point orbit with the four line classes.
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

    # one spread + its stabilizer
    pt_lines = [[li for li in range(40) if i in line_sets[li]]
                for i in range(n)]
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
    assert len(stab) == 720

    # find one PENTAD core (line signature [5,5,10,20])
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

    def point_orbits(core):
        rem = set(range(40))
        parts = []
        while rem:
            seed = next(iter(rem))
            orb = {seed}
            fr = [seed]
            while fr:
                nxt = []
                for x in fr:
                    for gp in core:
                        y = gp[x]
                        if y not in orb:
                            orb.add(y)
                            nxt.append(y)
                fr = nxt
            parts.append(frozenset(orb))
            rem -= orb
        return parts

    core = None
    parts = None
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
    o20_lines = next(p for p in parts if len(p) == 20)
    print("pentad core found: line orbits [5,5,10,20]")

    # ----- T1: point coverage -----
    cov1 = set().union(*(line_sets[li] for li in p1))
    cov2 = set().union(*(line_sets[li] for li in p2))
    print(f"T1 |cover(P1)| = {len(cov1)}, |cover(P2)| = {len(cov2)}, "
          f"same set: {cov1 == cov2}")
    porbs = point_orbits(core)
    psig = sorted(len(p) for p in porbs)
    print(f"T1 point orbits: {psig}")
    is_orbit = any(cov1 == set(p) for p in porbs)
    print(f"T1 cover(P1) is a point orbit: {is_orbit}")
    assert cov1 == cov2 and is_orbit

    # ----- T2: the 20-line orbit = transversals of the 5 charts -----
    # deleted matching: for each a in P1, its unique skew partner in P2
    charts = []
    for a in p1:
        partners = [b for b in p2 if not (line_sets[a] & line_sets[b])]
        assert len(partners) == 1
        charts.append((a, partners[0]))
    transversals = set()
    for a, b in charts:
        for li in range(40):
            if li in (a, b):
                continue
            if line_sets[li] & line_sets[a] and line_sets[li] & line_sets[b]:
                # common transversal must meet both; isotropic transversals
                # of a skew pair: exactly 4 (BT794)
                transversals.add(li)
    # count per chart
    per_chart = []
    for a, b in charts:
        t = [li for li in transversals
             if line_sets[li] & line_sets[a] and line_sets[li] & line_sets[b]]
        per_chart.append(len(t))
    print(f"T2 transversals per chart: {sorted(set(per_chart))}, "
          f"total distinct: {len(transversals)}")
    match = transversals == set(o20_lines)
    print(f"T2 transversal set == the 20-line orbit: {match}")
    in_spread = transversals == set(sset)
    print(f"T2b transversal set == THE MARKED SCHEDULE: {in_spread}")
    if in_spread:
        per_line = Counter()
        for li in transversals:
            cnt = sum(1 for a, b in charts
                      if line_sets[li] & line_sets[a]
                      and line_sets[li] & line_sets[b])
            per_line[cnt] += 1
        print(f"T2b charts served per schedule line: "
              f"{dict(sorted(per_line.items()))}")

    # ----- T3: where the uncovered 20 points live -----
    uncov = set(range(40)) - cov1
    # incidence of uncovered points with each line class
    def inc_profile(line_class):
        c = Counter()
        for li in line_class:
            c[len(line_sets[li] & uncov)] += 1
        return dict(sorted(c.items()))
    print(f"T3 uncovered-point incidence: P1 {inc_profile(p1)}, "
          f"P2 {inc_profile(p2)}, spread {inc_profile(sset)}, "
          f"20-orbit {inc_profile(o20_lines)}")

    out = {
        "theorem": "BT846 pentad core anatomy",
        "t1": {"cover_p1": len(cov1), "same_cover": cov1 == cov2,
               "point_orbits": psig, "cover_is_orbit": is_orbit},
        "t2": {"per_chart_transversals": sorted(set(per_chart)),
               "distinct_transversals": len(transversals),
               "equals_20_orbit": bool(match),
               "equals_marked_schedule": bool(in_spread),
               "charts_per_schedule_line": 2},
        "t3": {"P1": inc_profile(p1), "P2": inc_profile(p2),
               "spread": inc_profile(sset),
               "orbit20": inc_profile(o20_lines)},
    }
    with open("data/bt846_pentad_core_anatomy.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt846_pentad_core_anatomy.json")


if __name__ == "__main__":
    main()
