#!/usr/bin/env python3
"""
BT877 - Gauge parity is duality: the 4-line action lifts A4 -> S4
        across the W/Q duality, the odd permutations being exactly
        the anti-symplectic coset.

BT876: in PSp(4,3) the point stabiliser acts on the 4 lines through p0
as A4 (even permutations only), giving the gauge module 1+3+8.  A4 vs
S4 is a parity restriction.  Tested here:

  T1  build PGSp(4,3) = PSp:2 = W(E6) (order 51840) by adjoining the
      non-symplectic similitude M = diag(1,1,2,2) (scales the form by
      2); confirm order 51840 and that M is anti-symplectic.
  T2  Stab_PGSp(p0) (order 1296) acts on the 4 lines through p0 as
      FULL S4 (order 24), while Stab_PSp(p0) gives only A4 (order 12).
      The odd permutations of the 4 gauge lines are exactly the
      anti-symplectic (duality) coset.
  T3  reading: the gauge sector's parity (the missing odd
      permutations, A4 not S4, inside PSp) is the W/Q duality of
      BT772 - gauge parity violation is tied to the chirality/duality
      Z2, realised only in the full W(E6).
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json

import numpy as np


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
    assert len(psp) == 25920

    # T1: similitude M = diag(1,1,2,2), factor 2
    def Mraw(x):
        return (x[0], x[1], (2*x[2]) % 3, (2*x[3]) % 3)
    Mperm = tuple(pt_index[canon(Mraw(p))] for p in pts)
    # anti-symplectic: symp(Mx,My) = 2 symp(x,y) on RAW vectors
    ok = all(symp(Mraw(pts[i]), Mraw(pts[j]))
             == (2*symp(pts[i], pts[j])) % 3
             for i in range(n) for j in range(n))
    print(f"T1 M = diag(1,1,2,2) similitude (scales form by 2): {ok}")
    assert ok
    pgsp = set(psp)
    frontier = [Mperm]
    pgsp.add(Mperm)
    allg = gens + [Mperm]
    while frontier:
        nxt = []
        for gp in frontier:
            for h in allg:
                gh = compose(h, gp)
                if gh not in pgsp:
                    pgsp.add(gh)
                    nxt.append(gh)
        frontier = nxt
    print(f"T1 |PGSp(4,3)| = |W(E6)| = {len(pgsp)}")
    assert len(pgsp) == 51840

    # p0 and its 4 lines
    p0 = 0
    lines_through = []
    for L in [frozenset(q) for q in combinations(range(n), 4)
              if p0 in q and all(adj[i][j] for i, j in combinations(q, 2))]:
        lines_through.append(frozenset(L - {p0}))
    assert len(lines_through) == 4
    lidx = {L: i for i, L in enumerate(lines_through)}

    def image_on_lines(group):
        img = set()
        for c in group:
            if c[p0] != p0:
                continue
            perm = []
            okc = True
            for L in lines_through:
                iL = frozenset(c[x] for x in L)
                if iL in lidx:
                    perm.append(lidx[iL])
                else:
                    okc = False
                    break
            if okc:
                img.add(tuple(perm))
        return img

    imgP = image_on_lines(psp)
    imgG = image_on_lines(pgsp)
    print(f"T2 Stab_PSp(p0) on 4 lines: order {len(imgP)} "
          f"({'A4' if len(imgP) == 12 else '?'})")
    print(f"T2 Stab_PGSp(p0) on 4 lines: order {len(imgG)} "
          f"({'S4' if len(imgG) == 24 else '?'})")
    assert len(imgP) == 12 and len(imgG) == 24

    # parity of each permutation in S4
    def parity(perm):
        inv = sum(1 for a, b in combinations(range(4), 2)
                  if perm[a] > perm[b])
        return inv % 2
    odd_in_P = sum(1 for p in imgP if parity(p))
    odd_in_G = sum(1 for p in imgG if parity(p))
    print(f"T2 odd permutations: in PSp-image {odd_in_P}, "
          f"in PGSp-image {odd_in_G}")
    assert odd_in_P == 0 and odd_in_G == 12
    print("   => A4 (no odd) in PSp; S4 (12 odd) in PGSp: the odd")
    print("      permutations of the 4 gauge lines are exactly the")
    print("      anti-symplectic (W/Q duality) coset")

    # T3: confirm M itself (or its coset) supplies an odd permutation
    # find a duality element fixing p0 giving an odd 4-line permutation
    duality_odd = None
    for c in pgsp:
        if c in psp or c[p0] != p0:
            continue
        perm = []
        okc = True
        for L in lines_through:
            iL = frozenset(c[x] for x in L)
            if iL in lidx:
                perm.append(lidx[iL])
            else:
                okc = False
                break
        if okc and parity(tuple(perm)):
            duality_odd = tuple(perm)
            break
    print(f"T3 an anti-symplectic (outer) element fixing p0 acts as an "
          f"ODD 4-line permutation {duality_odd}: "
          f"{duality_odd is not None}")
    assert duality_odd is not None
    print("   gauge parity (A4->S4) = the W/Q duality / chirality Z2")
    print("   (BT772); parity lives only in the full W(E6).")

    out = {
        "theorem": "BT877 gauge parity is duality",
        "PGSp_order": len(pgsp),
        "PSp_4line_image": len(imgP),
        "PGSp_4line_image": len(imgG),
        "odd_in_PSp": odd_in_P, "odd_in_PGSp": odd_in_G,
        "duality_gives_odd": duality_odd is not None,
    }
    with open("data/bt877_gauge_parity_is_duality.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt877_gauge_parity_is_duality.json")


if __name__ == "__main__":
    main()
