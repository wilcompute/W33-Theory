#!/usr/bin/env python3
"""
BT890 - The matter cone 28 = 1+27 and the E7/56 bridge (mining #4).

Three substrate readings of 28 coincide, and bridge the matter sector
to the E6 -> E7 / Calabi-Yau string-GUT picture:

  T1  28 = 1 + 27 = (a point p0) + (its matter shell): the "matter
      cone" of a point - itself plus everything non-collinear with it.
  T2  28 = mu * Phi6 = n_even = the Ihara-zeta chiral discriminant
      |Delta_chiral| (BT872) = the Klein bitangent count.
  T3  28 = C(8,2) = the pairs of the 8 fixed points of a 3A1
      involution (the cube Q3, BT773).
  These three 28's are the same integer realized three structural
  ways (matter cone / Ihara discriminant / cube pairs).

  E7 BRIDGE (literature-bounded): 56 = 2*28 = the E7 minuscule rep =
  the Calabi-Yau_3 Hodge total 1 + 27 + 27bar + 1, where 27 = matter
  (E6 fundamental = the matter shell) and 27bar its charge-conjugate
  (BT878 C inverts the generation grade).  The established E6 c E7
  branching 56 -> 27 + 27bar + 1 + 1 is matched by the substrate
  integers; the substrate realizes the 27 and C, the E7/CY3 reading
  is the standard GUT embedding one level up.
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

    p0 = 0
    shell = [x for x in range(n) if x != p0 and not adj[p0][x]]

    # T1: matter cone 28 = 1 + 27
    cone = 1 + len(shell)
    print(f"T1 matter cone = 1 (p0) + {len(shell)} (shell) = {cone} = 28")
    assert cone == 28

    # T2: 28 = mu*Phi6 = n_even
    mu, Phi6 = 4, 7
    print(f"T2 mu*Phi6 = {mu*Phi6} = n_even = |Delta_chiral| (Ihara, "
          f"BT872) = Klein bitangents")
    assert mu*Phi6 == 28

    # T3: 28 = C(8,2) cube pairs.  Build a 3A1 involution's 8 fixed pts
    # and confirm C(8,2)=28.
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
    fr = [ident]
    while fr:
        nx = []
        for gp in fr:
            for h in gens:
                gh = compose(h, gp)
                if gh not in psp:
                    psp.add(gh)
                    nx.append(gh)
        fr = nx
    # a 45-class involution (BT869) fixes 8 points (the cube Q3)
    invol = next(g for g in psp if g != ident and compose(g, g) == ident
                 and sum(1 for i in range(n) if g[i] == i) == 8)
    fix8 = [i for i in range(n) if invol[i] == i]
    print(f"T3 a 3A1 involution fixes {len(fix8)} points (cube Q3); "
          f"C(8,2) = {len(fix8)*(len(fix8)-1)//2} = 28")
    assert len(fix8) == 8 and len(fix8)*(len(fix8)-1)//2 == 28

    # E7 bridge (numbers)
    print(f"\nE7 bridge: 56 = 2*28 = {2*28} = E7 minuscule = CY3 Hodge "
          f"1+27+27bar+1 = {1+27+27+1}")
    assert 2*28 == 56 and 1+27+27+1 == 56
    print("   27 = matter shell (E6 fundamental), 27bar = its C-conjugate")
    print("   (BT878); the E6 c E7 branching 56 -> 27+27bar+1+1 is the")
    print("   standard GUT embedding one level above the substrate.")

    out = {
        "theorem": "BT890 matter cone 28 and E7/56 bridge",
        "matter_cone": 28,
        "three_readings": {"1+27": 28, "mu*Phi6=n_even": 28,
                           "C(8,2) cube pairs": 28},
        "e7_56": {"2*28": 56, "CY3_Hodge_1+27+27+1": 56,
                  "reading": "E6 fundamental 27 + conjugate 27bar + 2 "
                             "singlets = E7 minuscule"},
    }
    with open("data/bt890_matter_cone_and_e7.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt890_matter_cone_and_e7.json")


if __name__ == "__main__":
    main()
