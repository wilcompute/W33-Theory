#!/usr/bin/env python3
"""
BT843 - The icosahedral compass: the 216 = 6^3 cores as a G-set, the
        Petersen flags, and an honest non-isomorphism.

GAP facts (witness .tmp/gap_bt843*.g):
  * PSp(4,3) has exactly TWO conjugacy classes of A5, both with
    normalizer S5 and 216 conjugates, NOT fused by Out = 2:
      class "spread compass": line orbits [10,30] (BT836/837 cores -
        the 10 is a spread), point orbits [20,20];
      class "pentad compass": line orbits [5,5,10,20] - two
        distinguished line PENTADS (an F5 = 5 echo), points [20,20].
  * BOTH 216-core actions are transitive of RANK 10 and imprimitive
    with unique block system of size 6 (quotient = a 36-set), but they
    are NOT isomorphic G-sets - the suborbit spectra differ:
      spread compass: [1,5,10,10,20,20,20,30,40,60]
      pentad compass: [1,5,10,10,20,20,30,30,30,60]
    The 5-suborbit = the 5 same-block partner cores in each case.

Python here:
  T1  the 3240 Petersen flags (schedule, core, 15-orbit pair) form a
      SINGLE transitive PSp orbit with stabilizer of order 8;
      identify its isomorphism type.
  T2  honest refutation: 3240 = #triangles of the complement graph Q
      (Pillar 109) is a numerical coincidence ONLY - Q's triangles
      split into orbits [360, 2880], so the two G-sets are NOT
      isomorphic.
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

    # one spread, its stabilizer, one icosahedral core, one Petersen pair
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

    def order_of(gp):
        o, cur = 1, gp
        while cur != ident:
            cur = compose(gp, cur)
            o += 1
        return o

    rng = random.Random(7)
    fives = [gp for gp in stab if order_of(gp) == 5]
    threes = [gp for gp in stab if order_of(gp) == 3]
    A5 = None
    while A5 is None:
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
            A5 = frozenset(sub)

    # the core's 15-orbit and one Petersen pair
    pairs = {frozenset(p) for p in combinations(sorted(spread), 2)}
    rem = set(pairs)
    o15 = None
    while rem:
        seed = next(iter(rem))
        orb = set()
        a0, b0 = tuple(seed)
        for gp in A5:
            lp = lperms[gp]
            orb.add(frozenset((lp[a0], lp[b0])))
        if len(orb) == 15:
            o15 = orb
        rem -= orb
    assert o15 is not None
    pair0 = next(iter(o15))

    # ----- T1: transitivity of the 3240 Petersen flags -----
    # flag = (spread image, core image, pair image); orbit by BFS over gens
    def act_flag(gp, flag):
        sp, core, pr = flag
        lp = lperms[gp]
        sp2 = frozenset(lp[li] for li in sp)
        # conjugate the core
        inv = [0]*n
        for i in range(n):
            inv[gp[i]] = i
        inv = tuple(inv)
        core2 = frozenset(compose(compose(gp, a), inv) for a in core)
        a0, b0 = tuple(pr)
        pr2 = frozenset((lp[a0], lp[b0]))
        return (sp2, core2, pr2)

    flag0 = (sset, A5, pair0)
    seen = {flag0}
    fr = [flag0]
    while fr:
        nxt = []
        for fl in fr:
            for gp in gens:
                fl2 = act_flag(gp, fl)
                if fl2 not in seen:
                    seen.add(fl2)
                    nxt.append(fl2)
        fr = nxt
    print(f"T1 Petersen-flag orbit size: {len(seen)} (= 3240 = 36x6x15)")
    assert len(seen) == 3240

    stab_fl = [gp for gp in psp if act_flag(gp, flag0) == flag0]
    so = len(stab_fl)
    ords = sorted(order_of(gp) for gp in stab_fl)
    abelian = all(compose(a, b) == compose(b, a)
                  for a, b in combinations(stab_fl, 2))
    print(f"T1 flag stabilizer: order {so}, element orders {ords}, "
          f"abelian: {abelian}")
    assert so == 8
    if abelian and ords.count(2) == 7:
        styp = "Z2^3"
    elif abelian:
        styp = "Z4xZ2"
    else:
        styp = "D4"
    print(f"   type: {styp}")

    # ----- T2: honest comparison with Q triangles -----
    # Q = complement of W33 collinearity on points; triangles = pairwise
    # non-collinear triples
    tris = [frozenset(t) for t in combinations(range(n), 3)
            if not any(adj[a][b] for a, b in combinations(t, 2))
            and all(symp(pts[a], pts[b]) != 0
                    for a, b in combinations(t, 2))]
    assert len(tris) == 3240
    # orbit split under psp
    tri_set = set(tris)
    orbs = []
    rem = set(tri_set)
    while rem:
        seed = next(iter(rem))
        orb = {seed}
        fr = [seed]
        while fr:
            nxt = []
            for t in fr:
                for gp in gens:
                    t2 = frozenset(gp[x] for x in t)
                    if t2 not in orb:
                        orb.add(t2)
                        nxt.append(t2)
            fr = nxt
        orbs.append(len(orb))
        rem -= orb
    orbs.sort()
    print(f"T2 Q-triangle orbits under PSp: {orbs}")
    assert orbs == [360, 2880]
    print("   => 3240 Petersen flags (transitive, stab order 8) and 3240")
    print("      Q-triangles (orbits [360,2880], stabs 72 and 9) are NOT")
    print("      isomorphic G-sets - the count match is numerology only.")

    out = {
        "theorem": "BT843 icosahedral compass",
        "gap": {
            "a5_classes": 2,
            "normalizer": "S5",
            "conjugates_each": 216,
            "spread_class_line_orbits": [10, 30],
            "pentad_class_line_orbits": [5, 5, 10, 20],
            "core216_rank": 10,
            "spread_class_216_suborbits":
                [1, 5, 10, 10, 20, 20, 20, 30, 40, 60],
            "pentad_class_216_suborbits":
                [1, 5, 10, 10, 20, 20, 30, 30, 30, 60],
            "core216_blocks": [6],
            "two_compasses_isomorphic": False,
        },
        "t1": {"flag_orbit": 3240, "stab_order": so, "stab_type": styp},
        "t2": {"q_triangle_orbits": orbs, "iso": False},
    }
    with open("data/bt843_icosahedral_compass.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt843_icosahedral_compass.json")


if __name__ == "__main__":
    main()
