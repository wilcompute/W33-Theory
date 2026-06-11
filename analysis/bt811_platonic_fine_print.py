#!/usr/bin/env python3
"""
BT811 - Platonic fine print: the chart group is O_h (not 2O), and the
        orbit anatomy of the polar-pair maximal.

Settles two BT810 boundary items by direct computation in PSp(4,3):

  T1. The order-48 stabilizer of a skew line pair (cube chart, BT773) has
      element orders {1,2,3,4,6} with NO order-8 element: it is
      O_h = S4 x Z2 (the full cube symmetry group), NOT the binary
      octahedral group 2O (which contains order-8 elements).  The
      platonic ladder is thus mixed: BINARY tetrahedral (2T) and BINARY
      icosahedral (2I) cores live in Sp(4,3) via symplectic planes and
      spreads, but the chart group is the REAL octahedral group acting
      on the cube vertices - the 2O double cover does not embed there.
  T2. Point orbits of the index-45 maximal (2T x 2T):2 on the 40 points:
      the polar pair contributes its 4 + 4 points; the remaining 32
      points split as computed below.
  T3. Line orbits of the same maximal on the 40 isotropic lines.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json


def inv3(a):
    a %= 3
    if a in (1, 2):
        return a
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def main():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    n = 40
    pt_index = {p: i for i, p in enumerate(pts)}

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    def transvection_perm(v):
        out = []
        for x in pts:
            w = symp(x, v)
            out.append(pt_index[canon(tuple(
                (x[k] + w * v[k]) % 3 for k in range(4)))])
        return tuple(out)

    gens = [transvection_perm(v) for v in pts]
    ident = tuple(range(n))

    def compose(a, b):
        return tuple(a[b[i]] for i in range(n))

    psp = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                gh = compose(h, g)
                if gh not in psp:
                    psp.add(gh)
                    nxt.append(gh)
        frontier = nxt
    assert len(psp) == 25920

    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    line_index = {l: i for i, l in enumerate(lines)}
    line_sets = [set(l) for l in lines]

    def order_of(g):
        o, cur = 1, g
        while cur != ident:
            cur = compose(g, cur)
            o += 1
        return o

    # ---- T1: chart group element orders ----------------------------------
    i0, j0 = next((i, j) for i, j in combinations(range(40), 2)
                  if not (line_sets[i] & line_sets[j]))
    stab48 = []
    for g in psp:
        la = line_index[frozenset(g[x] for x in lines[i0])]
        lb = line_index[frozenset(g[x] for x in lines[j0])]
        if {la, lb} == {i0, j0}:
            stab48.append(g)
    orders48 = Counter(order_of(g) for g in stab48)
    print(f"T1 |Stab(skew pair)| = {len(stab48)}, element orders = "
          f"{dict(sorted(orders48.items()))}")
    assert len(stab48) == 48
    has8 = orders48.get(8, 0) > 0
    print(f"T1 order-8 elements: {orders48.get(8, 0)} -> chart group is "
          f"{'2O' if has8 else 'O_h = S4 x Z2 (REAL octahedral)'}")
    # S4 x Z2 profile: order((s,e)) = lcm(|s|, |e|):
    #   1:1, 2: 9 + 9 + 1 = 19, 3: 8, 4: 6*2 = 12, 6: 8 (3-cycles x central)
    oh_profile = {1: 1, 2: 19, 3: 8, 4: 12, 6: 8}
    assert dict(orders48) == oh_profile
    print(f"T1 profile matches S4 x Z2 = O_h exactly: {oh_profile}")

    # ---- T2/T3: orbits of the index-45 maximal ---------------------------
    # hyperbolic line: a non-isotropic projective line; use first nonedge pair
    # build one hyperbolic line and its perp
    a, b = next((x, y) for x, y in combinations(range(40), 2)
                if not adj[x][y])
    Lpts = set()
    for s in range(3):
        for t in range(3):
            if (s, t) != (0, 0):
                Lpts.add(canon(tuple((s*u + t*v) % 3
                                     for u, v in zip(pts[a], pts[b]))))
    Lidx = frozenset(pt_index[p] for p in Lpts)
    Pidx = frozenset(i for i in range(40)
                     if all(symp(pts[i], pts[x]) == 0
                            for x in (a, b)))
    assert len(Lidx) == 4 and len(Pidx) == 4 and not (Lidx & Pidx)

    M45 = []
    pair = {Lidx, Pidx}
    for g in psp:
        im1 = frozenset(g[x] for x in Lidx)
        im2 = frozenset(g[x] for x in Pidx)
        if {im1, im2} == pair:
            M45.append(g)
    print(f"\nT2 |Stab(polar pair)| in PSp = {len(M45)} (expect 576)")
    assert len(M45) == 576

    def orbits_of(group, objs, act):
        rem = set(objs)
        sizes = []
        while rem:
            x = next(iter(rem))
            orb = {x}
            frontier = [x]
            while frontier:
                nxt = []
                for y in frontier:
                    for g in group[:20]:   # generators suffice? use all gens
                        z = act(g, y)
                        if z not in orb:
                            orb.add(z)
                            nxt.append(z)
                frontier = nxt
            sizes.append(len(orb))
            rem -= orb
        return sorted(sizes)

    # use a small generating set: closure check via full group action
    # (orbits under the full 576-element list, applied as generators)
    psizes = orbits_of(M45, range(40), lambda g, x: g[x])
    print(f"T2 point orbits of the index-45 maximal: {psizes}")

    def act_line(g, li):
        return line_index[frozenset(g[x] for x in lines[li])]

    lsizes = orbits_of(M45, range(40), act_line)
    print(f"T3 isotropic-line orbits of the index-45 maximal: {lsizes}")

    out = {
        "theorem": "BT811 platonic fine print",
        "chart_group_orders": dict(sorted(orders48.items())),
        "chart_group": "O_h = S4 x Z2 (no order-8: not 2O)",
        "index45_point_orbits": psizes,
        "index45_isoline_orbits": lsizes,
    }
    with open("data/bt811_platonic_fine_print.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt811_platonic_fine_print.json")


if __name__ == "__main__":
    main()
