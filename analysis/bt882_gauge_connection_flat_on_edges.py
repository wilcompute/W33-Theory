#!/usr/bin/env python3
"""
BT882 - The gauge connection: flat along edges, curved on the matter
        graph.

BT881 made the 40 points the space of local gauge groups, each with
generation centre <R_p> (long-root Z3).  The "gauge connection" is
how adjacent local frames relate: the subgroup <R_p, R_p'> generated
by two points' generation centres = the holonomy between them.  Since
transvections t_p, t_p' commute iff symp(p,p')=0:

  T1  collinear (adjacent, the 12 = k edge-partners): <R_p,R_p'> =
      Z3 x Z3 (order 9, abelian) - the connection is FLAT along the
      240 W(3,3) edges (commuting local generation symmetries).
  T2  non-collinear (the 27 = q^q non-edge partners, the matter graph
      Q): <R_p,R_p'> = SL(2,3) = 2T (order 24, the binary tetrahedral
      / 24-cell group) - the connection is CURVED across non-edges.
  T3  so the gauge curvature lives EXACTLY on the matter graph Q
      (BT870's dual-gravity graph): flat gauge directions = the 240
      edges, curved (holonomy 2T) directions = the 540 non-edges /
      the 27-per-point matter shell.  Gauge-flat = collinear = the
      same line; curvature = non-collinearity = matter.
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

    def transvection_perm(v):
        out = []
        for x in pts:
            w = symp(x, v)
            out.append(pt_index[canon(tuple(
                (x[t] + w * v[t]) % 3 for t in range(4)))])
        return tuple(out)

    Rp = [transvection_perm(pts[i]) for i in range(n)]
    ident = tuple(range(n))

    def compose(a, b):
        return tuple(a[b[i]] for i in range(n))

    def gen_subgroup(elts, cap=2000):
        G = {ident}
        fr = [ident]
        while fr:
            nx = []
            for gp in fr:
                for h in elts:
                    gh = compose(h, gp)
                    if gh not in G:
                        G.add(gh)
                        nx.append(gh)
                        if len(G) > cap:
                            return G
            fr = nx
        return G

    def order_of(gp):
        o, cur = 1, gp
        while cur != ident:
            cur = compose(gp, cur)
            o += 1
        return o

    # census of <R_p, R_p'> over all pairs, split by adjacency
    p0 = 0
    coll = [j for j in range(n) if adj[p0][j]]
    nonc = [j for j in range(n) if j != p0 and not adj[p0][j]]
    assert len(coll) == 12 and len(nonc) == 27

    # T1: collinear -> Z3 x Z3 (commute)
    coll_orders = Counter()
    coll_commute = True
    for j in coll:
        H = gen_subgroup([Rp[p0], Rp[j]])
        coll_orders[len(H)] += 1
        if compose(Rp[p0], Rp[j]) != compose(Rp[j], Rp[p0]):
            coll_commute = False
    print(f"T1 collinear (12 edge-partners): <R_p,R_p'> orders "
          f"{dict(coll_orders)}; all commute: {coll_commute}")
    assert dict(coll_orders) == {9: 12} and coll_commute
    print("   => Z3 x Z3 (order 9, abelian): connection FLAT along the")
    print("      240 W(3,3) edges")

    # T2: non-collinear -> SL(2,3) order 24
    nonc_orders = Counter()
    for j in nonc:
        H = gen_subgroup([Rp[p0], Rp[j]])
        nonc_orders[len(H)] += 1
    print(f"T2 non-collinear (27 non-edge partners): <R_p,R_p'> orders "
          f"{dict(nonc_orders)}")
    assert dict(nonc_orders) == {24: 27}
    # identify SL(2,3): order 24, one involution (centre), 8 order-3,...
    Hs = gen_subgroup([Rp[p0], Rp[nonc[0]]])
    prof = Counter(order_of(g) for g in Hs)
    print(f"   order-24 group profile: {dict(sorted(prof.items()))}")
    # SL(2,3): orders {1:1, 2:1, 3:8, 4:6, 6:8}
    is_sl23 = dict(prof) == {1: 1, 2: 1, 3: 8, 4: 6, 6: 8}
    print(f"   = SL(2,3) = 2T (binary tetrahedral / 24-cell group): "
          f"{is_sl23}")
    assert is_sl23

    # T3: summary
    print("T3 gauge connection: FLAT (Z3xZ3) along the 240 collinear")
    print("   edges, CURVED (holonomy 2T = SL(2,3), the 24-cell group)")
    print("   across the 27-per-point non-collinear matter shell.")
    print("   Gauge curvature lives on the matter graph Q "
          "(BT870 dual-gravity graph); flat = collinearity, curved =")
    print("   non-collinearity = matter.")

    out = {
        "theorem": "BT882 gauge connection flat on edges",
        "collinear_holonomy": {"order": 9, "type": "Z3xZ3", "flat": True,
                               "count": 12},
        "noncollinear_holonomy": {"order": 24, "type": "SL(2,3)=2T",
                                  "curved": True, "count": 27},
        "curvature_lives_on": "matter graph Q (non-collinearity)",
    }
    with open("data/bt882_gauge_connection.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt882_gauge_connection.json")


if __name__ == "__main__":
    main()
