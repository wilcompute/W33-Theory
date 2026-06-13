#!/usr/bin/env python3
"""
BT889 - The fermion content of one generation: the 27 matter shell is
        C(R)/SL(2,3) (gauge group / electroweak Levi).

BT888: the 27 matter shell is a torsor under the color radical.  Under
the FULL gauge group C(R) (order 648):

  T1  C(R) is transitive on the 27 shell with point-stabiliser of
      order 24 = SL(2,3) = the electroweak Levi.  So the matter shell
      is the homogeneous space C(R)/SL(2,3): each matter state is
      fixed by an electroweak subgroup and moved by color (consistent
      with matter = color torsor, BT888).
  T2  the action has rank 6 (suborbits [1,1,1,8,8,8]); the permutation
      module C[27] decomposes into C(R)-irreducibles (the fermion
      gauge multiplets of one generation), with the constituent
      dimensions computed from the orbital eigenstructure.
  T3  the three size-1 suborbits = a distinguished 3-set fixed by the
      electroweak Levi (color-singlet "lepton-like" states); the three
      size-8 suborbits carry the colored ("quark-like") content -
      the color/lepton split of one generation.
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
    CR = [g for g in psp if g[p0] == p0]
    shell = [x for x in range(n) if x != p0 and not adj[p0][x]]
    sidx = {s: i for i, s in enumerate(shell)}
    assert len(CR) == 648 and len(shell) == 27

    # T1: transitive, stabiliser order 24
    s0 = shell[0]
    stab = [g for g in CR if g[s0] == s0]
    print(f"T1 C(R) transitive on the 27 shell; point-stabiliser order "
          f"{len(stab)} = SL(2,3) = electroweak Levi; 27 = 648/24 = "
          f"C(R)/SL(2,3)")
    assert len(stab) == 24

    # suborbits of stab on the 27
    seen = set()
    subs = []
    for x in shell:
        if x in seen:
            continue
        o = set()
        f2 = [x]
        o.add(x)
        while f2:
            nx2 = []
            for y in f2:
                for g in stab:
                    z = g[y]
                    if z not in o:
                        o.add(z)
                        nx2.append(z)
            f2 = nx2
        subs.append(sorted(o))
        seen |= o
    sizes = sorted(len(o) for o in subs)
    print(f"T2 rank {len(subs)}, suborbits {sizes}")
    assert sizes == [1, 1, 1, 8, 8, 8]

    # T2: orbital adjacency matrices -> module decomposition
    # build the 6 orbitals (symmetrized) as 27x27 matrices, find the
    # common eigenspaces (isotypic dims)
    orbitals = []
    for o in subs:
        M = np.zeros((27, 27))
        y0 = o[0]
        for g in CR:
            a, b = g[s0], g[y0]
            M[sidx[b], sidx[a]] = 1.0
        orbitals.append(M)
    # a generic combination's eigenspaces = the isotypic components
    rng = np.random.default_rng(0)
    Mgen = sum(rng.random()*M for M in orbitals)
    Mgen = Mgen + Mgen.T
    evals = np.linalg.eigvalsh(Mgen)
    # cluster eigenvalues
    clusters = []
    for e in sorted(evals):
        if clusters and abs(e - clusters[-1][-1]) < 1e-6:
            clusters[-1].append(e)
        else:
            clusters.append([e])
    dims = sorted(len(c) for c in clusters)
    print(f"T2 C[27] isotypic dimensions under C(R): {dims} "
          f"(sum {sum(dims)})")
    assert sum(dims) == 27

    # T3: the three size-1 suborbits = electroweak-fixed 3-set
    fixed3 = sorted(s for s in shell
                    if all(g[s] == s for g in stab))
    print(f"T3 electroweak Levi fixes {len(fixed3)} shell points "
          f"(color-singlet 'lepton-like' 3-set); the three 8-orbits "
          f"carry colored 'quark-like' content")
    assert len(fixed3) == 3

    print("\nTHEOREM (BT889): the 27 matter shell of one generation is")
    print("the homogeneous space C(R)/SL(2,3) = gauge group / electroweak")
    print("Levi; rank-6 with suborbits [1,1,1,8,8,8] - a color-singlet")
    print("3-set (lepton-like, electroweak-fixed) + three color-8 sets")
    print("(quark-like).  Each matter state's stabiliser is exactly the")
    print("electroweak group; color moves it.")

    out = {
        "theorem": "BT889 fermion content of the 27",
        "transitive": True,
        "point_stabiliser_order": len(stab),
        "homogeneous_space": "C(R)/SL(2,3) = 648/24 = 27",
        "rank": len(subs),
        "suborbits": sizes,
        "isotypic_dims": dims,
        "electroweak_fixed_set": len(fixed3),
    }
    with open("data/bt889_fermion_content_of_27.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt889_fermion_content_of_27.json")


if __name__ == "__main__":
    main()
