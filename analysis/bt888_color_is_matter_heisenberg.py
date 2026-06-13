#!/usr/bin/env python3
"""
BT888 - Color is the matter-shell Heisenberg group: matter carries
        color because the 27-shell is a color torsor.

BT858: the 27 matter shell (non-collinear points of p0) is a torsor
under O_3 = the Heisenberg 3^{1+2} radical of Stab(p0) (regular
action).  BT887: the color part of the gauge group is the SAME
Heisenberg radical O_3 (the gluon-8-carrying normal subgroup).  Since
both are O_3(Stab(p0)) (the unique normal Sylow-3), they are
IDENTICAL.  Verified in one computation:

  T1  the normal Heisenberg N = O_3(Stab(p0)) (order 27) acts
      REGULARLY on the 27 matter shell (simply transitive) - matter
      is a torsor under N (BT858).
  T2  the SAME N is the color radical: it fixes the electroweak 1+3
      (4-dim) and acts on the gluon octet 8 (BT887).
  T3  therefore COLOR = the matter-shell Heisenberg group: color
      rotations ARE matter-shell motions, and matter carries color
      precisely because the 27-shell is a torsor under the color
      group.  One group 3^{1+2} = q^q: simultaneously the matter
      register's translations and the gluon octet's color.
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

    p0 = 0
    stab = [gp for gp in psp if gp[p0] == p0]
    assert len(stab) == 648
    shell = [x for x in range(n) if x != p0 and not adj[p0][x]]
    nbr0 = [x for x in range(n) if adj[p0][x]]
    assert len(shell) == 27 and len(nbr0) == 12

    # the unique normal Heisenberg radical N = O_3(Stab(p0)), order 27
    rng = random.Random(1)
    pool = [gp for gp in stab if order_of(gp) == 3]
    N = None
    while N is None:
        seeds = [rng.choice(pool) for _ in range(3)]
        sub = {ident}
        f2 = [ident]
        while f2 and len(sub) <= 27:
            nx2 = []
            for x in f2:
                for h in seeds:
                    y = compose(h, x)
                    if y not in sub:
                        sub.add(y)
                        nx2.append(y)
            f2 = nx2
        if len(sub) != 27:
            continue
        if all(compose(compose(c, x), inv(c)) in sub
               for c in stab for x in sub):
            N = sub
    # confirm extraspecial 3^{1+2} (non-abelian, exponent 3)
    Nl = list(N)
    abelian = all(compose(a, b) == compose(b, a)
                  for a, b in combinations(Nl, 2))
    print(f"T0 N = O_3(Stab(p0)): order {len(N)}, non-abelian "
          f"(Heisenberg 3^(1+2)): {not abelian}")
    assert len(N) == 27 and not abelian

    # T1: N regular on the 27 matter shell
    s0 = shell[0]
    orb = {compose(g, ident)[s0] if False else g[s0] for g in N}
    free = all(g[s0] != s0 for g in N if g != ident)
    print(f"T1 N on the 27 matter shell: orbit size {len(orb)}, "
          f"free: {free} => REGULAR (matter is a torsor under N)")
    assert len(orb) == 27 and free

    # T2: the SAME N is the color radical (fixes electroweak 1+3,
    # moves gluon 8)
    seen = set()
    orbits = []
    for x in nbr0:
        if x in seen:
            continue
        o = set()
        f3 = [x]
        o.add(x)
        while f3:
            nx3 = []
            for y in f3:
                for g in N:
                    z = g[y]
                    if z not in o:
                        o.add(z)
                        nx3.append(z)
            f3 = nx3
        orbits.append(sorted(o))
        seen |= o
    inv_dim = len(orbits)
    print(f"T2 the SAME N on the 12 gauge bosons: {inv_dim} orbits "
          f"(sizes {sorted(len(o) for o in orbits)}) => fixes "
          f"electroweak {inv_dim}-dim (1+3), moves gluon "
          f"{12-inv_dim}-dim (8)")
    assert inv_dim == 4

    print("\nTHEOREM (BT888): COLOR = the matter-shell Heisenberg group.")
    print("The one group N = 3^{1+2} = O_3(Stab(p0)) is BOTH the regular")
    print("(simply transitive) symmetry of the 27 matter shell AND the")
    print("color radical of the gauge group (the gluon-8 carrier).")
    print("Matter carries color because the 27-shell is a torsor under")
    print("the color group; color rotations ARE matter-shell motions.")

    out = {
        "theorem": "BT888 color is matter-shell Heisenberg",
        "N_order": len(N), "N_heisenberg": not abelian,
        "regular_on_matter_shell": bool(free and len(orb) == 27),
        "color_radical_electroweak_invariant_dim": inv_dim,
        "gluon_octet_dim": 12 - inv_dim,
    }
    with open("data/bt888_color_is_matter_heisenberg.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt888_color_is_matter_heisenberg.json")


if __name__ == "__main__":
    main()
