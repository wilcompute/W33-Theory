#!/usr/bin/env python3
"""
BT880 - The generation symmetry is the centre of the gauge group.

C(R) = Stab(p0) is the gauge group (BT876, order 648, module 1+3+8 =
SU(3)xSU(2)xU(1)).  R = the generation symmetry (BT874) sits inside
C(R) (it commutes with itself), and BT874 showed R fixes all 12 gauge
neighbours pointwise (acts trivially on the gauge bosons).  So R is a
gauge-trivial central element.  Computed here:

  T1  R is in Z(C(R)) (central in the gauge group).
  T2  Z(C(R)) = <R> = Z3 (order 3): the generation symmetry IS the
      centre of the gauge group, and the centre is exactly the
      generation Z3 - the Z3 centre of the colour SU(3) factor (the
      centre acts trivially on the adjoint 8, matching R fixing all
      12 gauge bosons).
  T3  reading: generations = the centre of the gauge group; generation
      number is gauge-blind (BT864) precisely because R is central and
      acts trivially on the gauge module.  This is the SU(3)-centre Z3
      flagged in BT871, now identified with the generation Z3.
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

    def order_of(gp):
        o, cur = 1, gp
        while cur != ident:
            cur = compose(gp, cur)
            o += 1
        return o

    def inv(gp):
        iv = [0]*n
        for i in range(n):
            iv[gp[i]] = i
        return tuple(iv)

    p0 = 0
    stab = [gp for gp in psp if gp[p0] == p0]
    shell = [x for x in range(n) if x != p0 and not adj[p0][x]]
    nbr0 = [x for x in range(n) if adj[p0][x]]
    rng = random.Random(3)
    threes = [gp for gp in stab if order_of(gp) == 3]
    O3 = None
    while O3 is None:
        gs = [rng.choice(threes) for _ in range(3)]
        sub = {ident}
        fr = [ident]
        while fr and len(sub) <= 27:
            nx2 = []
            for x in fr:
                for h in gs:
                    y = compose(h, x)
                    if y not in sub:
                        sub.add(y)
                        nx2.append(y)
            fr = nx2
        if len(sub) != 27 or any(order_of(g) != 3 for g in sub
                                 if g != ident):
            continue
        if all(compose(compose(c, x), inv(c)) in sub
               for c in stab for x in sub):
            O3 = sub
    R = next(g for g in O3 if g != ident
             and all(compose(g, x) == compose(x, g) for x in O3))

    # gauge group = C(R) = Stab(p0)
    CR = [g for g in psp if compose(g, R) == compose(R, g)]
    assert len(CR) == 648 and set(CR) == set(stab)

    # T1: R central in C(R)?
    R_central = all(compose(g, R) == compose(R, g) for g in CR)
    print(f"T1 R is central in the gauge group C(R): {R_central}")
    assert R_central

    # T2: Z(C(R))
    CRset = set(CR)
    Z = [g for g in CR if all(compose(g, h) == compose(h, g) for h in CR)]
    print(f"T2 |Z(gauge group C(R))| = {len(Z)}")
    ords = Counter(order_of(g) for g in Z)
    print(f"   Z element orders: {dict(sorted(ords.items()))}")
    R_in_Z = R in Z
    Z_eq_R = set(Z) == {ident, R, compose(R, R)}
    print(f"   R in Z(C(R)): {R_in_Z}; Z(C(R)) = <R> = Z3: {Z_eq_R}")
    assert R_in_Z and Z_eq_R

    # T3: R acts trivially on the 12 gauge bosons (fixes all)
    fixes_gauge = all(R[x] == x for x in nbr0)
    print(f"T3 R fixes all 12 gauge bosons (acts trivially on the gauge "
          f"module 1+3+8): {fixes_gauge}")
    assert fixes_gauge
    print("   => the generation Z3 IS the centre of the gauge group,")
    print("      acting trivially on the adjoint (the Z3 centre of the")
    print("      colour SU(3)); generations are gauge-blind because the")
    print("      generation symmetry is the gauge centre (BT871's SU(3)")
    print("      centre = the generation Z3).")

    out = {
        "theorem": "BT880 generation = gauge centre",
        "gauge_order": len(CR),
        "R_central": R_central,
        "Z_gauge_order": len(Z),
        "Z_equals_R_Z3": bool(Z_eq_R),
        "R_trivial_on_gauge_bosons": bool(fixes_gauge),
    }
    with open("data/bt880_generation_is_gauge_center.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt880_generation_is_gauge_center.json")


if __name__ == "__main__":
    main()
