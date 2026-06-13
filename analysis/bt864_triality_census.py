#!/usr/bin/env python3
"""
BT864 - The triality census: generation symmetry is matter-blind but
        gauge-visible.

BT863: EVERY order-3 element splits the Steinberg matter register
27+27+27 - so the choice of physical triality cannot be seen by the
matter sector at all.  Where the classes DO differ is the gauge/point
sector.  Census over all order-3 conjugacy classes of PSp(4,3):

  per class: size, #fixed points, #fixed lines, #fixed schedules,
  free-on-points?, free-on-lines?, gauge-sector eigensplit
  (multiplicities of 1, w, w^2 on C[40 points] = (40+2f)/3,
  (40-f)/3, (40-f)/3 with f = #fixed points).

Identifications sought: the transvection class (f = 13 = Phi_3, the
hyperplane count), the Heisenberg-center class, and the FREE classes
(candidates for Pillar 68's texture triality R, which acted with 9
free 3-orbits and no fixed points).
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json


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
    assert len(psp) == 25920

    def order_of(gp):
        o, cur = 1, gp
        while cur != ident:
            cur = compose(gp, cur)
            o += 1
        return o

    # spreads (schedules)
    pt_lines = [[li for li in range(40) if i in line_sets[li]]
                for i in range(n)]
    spreads = []

    def cover(used, chosen):
        if len(chosen) == 10:
            spreads.append(frozenset(chosen))
            return
        r = min(set(range(n)) - used)
        for li in pt_lines[r]:
            if not (line_sets[li] & used):
                cover(used | line_sets[li], chosen + [li])

    cover(set(), [])
    assert len(spreads) == 36

    # order-3 elements -> conjugacy classes (BFS by generator conjugation)
    o3 = [gp for gp in psp if order_of(gp) == 3]
    print(f"order-3 elements: {len(o3)}")
    inv_gens = []
    for g in gens:
        iv = [0]*n
        for i in range(n):
            iv[g[i]] = i
        inv_gens.append(tuple(iv))
    remaining = set(o3)
    classes = []
    while remaining:
        seed = next(iter(remaining))
        cl = {seed}
        fr = [seed]
        while fr:
            nx2 = []
            for x in fr:
                for g, gi in zip(gens, inv_gens):
                    y = compose(compose(g, x), gi)
                    if y not in cl:
                        cl.add(y)
                        nx2.append(y)
            fr = nx2
        classes.append(cl)
        remaining -= cl

    def line_perm(gp):
        return tuple(line_index[frozenset(gp[x] for x in lines[li])]
                     for li in range(40))

    print(f"order-3 conjugacy classes: {len(classes)}")
    rows = []
    for cl in sorted(classes, key=len):
        gp = next(iter(cl))
        lp = line_perm(gp)
        fixp = sum(1 for i in range(n) if gp[i] == i)
        fixl = sum(1 for i in range(40) if lp[i] == i)
        fixs = sum(1 for S in spreads
                   if frozenset(lp[li] for li in S) == S)
        free_p = fixp == 0
        free_l = fixl == 0
        m0 = (40 + 2*fixp)//3
        m12 = (40 - fixp)//3
        tag = ""
        if fixp == 13:
            tag = "TRANSVECTION (fixes hyperplane, 13 = Phi_3)"
        if free_p and free_l:
            tag = "FREE (texture-triality candidate)"
        rows.append((len(cl), fixp, fixl, fixs,
                     (m0, m12, m12), tag))
        print(f"  class size {len(cl):5d}: fixpts {fixp:2d}, "
              f"fixlines {fixl:2d}, fixschedules {fixs:2d}, "
              f"gauge split {m0}+{m12}+{m12}  {tag}")

    # transvections sanity: our generators
    g0 = gens[0]
    fix_g0 = sum(1 for i in range(n) if g0[i] == i)
    print(f"sanity: a generator transvection fixes {fix_g0} points")

    out = {
        "theorem": "BT864 triality census",
        "order3_total": len(o3),
        "classes": [{"size": r[0], "fixpts": r[1], "fixlines": r[2],
                     "fixschedules": r[3], "gauge_split": r[4],
                     "tag": r[5]} for r in rows],
        "matter_blind": "all classes split Steinberg 27+27+27 (BT863)",
    }
    with open("data/bt864_triality_census.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt864_triality_census.json")


if __name__ == "__main__":
    main()
