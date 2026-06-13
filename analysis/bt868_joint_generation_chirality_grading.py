#!/usr/bin/env python3
"""
BT868 - The joint generation x chirality grading: order-6 elements
        factor the matter register as Z6 = Z3 (generation) x Z2
        (chirality).

BT863: order-3 vanishing gives the 27+27+27 generation split.
BT862: H2 is the sign-twisted (chirality) carrier.
An order-6 element g has g^2 (order 3, generation) and g^3 (order 2,
chirality), so its Z6-eigengrading on the Steinberg matter register
is the JOINT structure.  Because chi_St vanishes on every 3-singular
element, chi(g^k)=0 for k in {1,2,4,5} (all have order divisible by
3); only chi(1)=81 and chi(g^3) (an involution) survive, so the six
eigenmultiplicities collapse to a clean chirality 2-split, each half
carrying 3 equal generations.

Computed here for ALL order-6 classes:
  m_j = (1/6) sum_k zeta6^{-jk} chi(g^k)
      = (81 + (-1)^j chi(g^3)) / 6,
  chirality halves  (81 +- chi(g^3))/2,  each = 3 equal generations.
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
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    edges = sorted({tuple(sorted((i, j))) for i, j in
                    combinations(range(n), 2) if adj[i][j]})
    eidx = {e: i for i, e in enumerate(edges)}
    tris = sorted({tuple(sorted(t)) for l in lines
                   for t in combinations(sorted(l), 3)})

    d0 = np.zeros((n, 240))
    for i, (a, b) in enumerate(edges):
        d0[b, i] = 1.0
        d0[a, i] = -1.0
    d1 = np.zeros((240, 160))
    for j, (x, y, z) in enumerate(tris):
        d1[eidx[(y, z)], j] = 1.0
        d1[eidx[(x, z)], j] = -1.0
        d1[eidx[(x, y)], j] = 1.0
    P = (np.eye(240) - d0.T @ np.linalg.pinv(d0 @ d0.T) @ d0
         - d1 @ np.linalg.pinv(d1.T @ d1) @ d1.T)

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

    def chi(gp):
        tr = 0.0
        for fi, (a, b) in enumerate(edges):
            ga, gb = gp[a], gp[b]
            if ga < gb:
                tr += P[fi, eidx[(ga, gb)]]
            else:
                tr -= P[fi, eidx[(gb, ga)]]
        v = round(tr)
        assert abs(tr - v) < 1e-6
        return v

    # representatives of order-6 classes, by (chi(g), chi(g^2),
    # chi(g^3)) signature
    seen_sig = {}
    inv_gens = []
    for g in gens:
        iv = [0]*n
        for i in range(n):
            iv[g[i]] = i
        inv_gens.append(tuple(iv))

    o6 = [gp for gp in psp if order_of(gp) == 6]
    print(f"order-6 elements: {len(o6)}")
    # group into conjugacy classes
    remaining = set(o6)
    reps = []
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
        reps.append((seed, len(cl)))
        remaining -= cl
    print(f"order-6 conjugacy classes: {len(reps)}")

    zeta = np.exp(2j*np.pi/6)
    out_classes = []
    for g, size in sorted(reps, key=lambda t: t[1]):
        powers = [ident]
        for _ in range(5):
            powers.append(compose(g, powers[-1]))
        chis = [chi(p) for p in powers]   # chi(g^0..g^5)
        ords = [order_of(p) for p in powers]
        # multiplicities
        mult = []
        for jj in range(6):
            m = sum(zeta**(-jj*k) * chis[k] for k in range(6)) / 6
            mr = round(m.real)
            assert abs(m - mr) < 1e-6, m
            mult.append(mr)
        chir_plus = (81 + chis[3]) // 2
        chir_minus = (81 - chis[3]) // 2
        # generation degeneracy: m_0=m_2=m_4 and m_1=m_3=m_5 ?
        even = mult[0::2]
        odd = mult[1::2]
        gen_deg = (len(set(even)) == 1 and len(set(odd)) == 1)
        print(f"  class size {size:4d}: chi(g^k)={chis} ord(g^k)={ords}")
        print(f"     Z6 multiplicities {mult}; chirality split "
              f"{chir_plus}+{chir_minus}; 3-equal-generations "
              f"per chirality: {gen_deg}")
        out_classes.append({"size": size, "chi": chis, "mult": mult,
                            "chirality": [chir_plus, chir_minus],
                            "gen_degenerate": gen_deg})

    print("\nTHEOREM: every order-6 element grades the Steinberg matter")
    print("register by Z6 = Z3(generation) x Z2(chirality).  Steinberg")
    print("vanishing on 3-singular powers forces only chi(1) and the")
    print("involution chi(g^3) to survive, so the 81 splits into a")
    print("chirality 2-block (81 +- chi(g^3))/2, each carrying 3 equal")
    print("generations: generation and chirality are SIMULTANEOUSLY")
    print("diagonalized, and independent (the grading factors).")

    out = {"theorem": "BT868 joint generation x chirality grading",
           "order6_count": len(o6),
           "classes": out_classes}
    with open("data/bt868_joint_generation_chirality_grading.json",
              "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt868_joint_generation_chirality_grading.json")


if __name__ == "__main__":
    main()
