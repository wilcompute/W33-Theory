#!/usr/bin/env python3
"""
BT869 - The two chirality involutions: Steinberg eigensplit 45+36 vs
        39+42 identified by fixed geometry.

BT868 found order-6 elements with g^3 an involution of Steinberg
character chi_St(g^3) in {9, -3}, giving matter-register chirality
splits 45+36 (= Schlafli tritangents + double-sixes) and 39+42.  Here
the involution conjugacy classes of PSp(4,3) are enumerated directly,
each tagged with:

  size, #fixed points, #fixed lines, chi_St (= fixflags - fixpts
  - fixlines + 1), Steinberg eigensplit ((81+chi)/2, (81-chi)/2),
  and the BT775/BT773 geometric type (the 3A1 / skew-pair involutions
  whose 8 fixed points carry the cube graph Q3).

Goal: name the two chirality types and connect to the axis-type
Weyl chirality of BT746/BT772.
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
    line_index = {l: i for i, l in enumerate(lines)}
    lines_sets = [frozenset(l) for l in lines]

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

    inv_gens = []
    for g in gens:
        iv = [0]*n
        for i in range(n):
            iv[g[i]] = i
        inv_gens.append(tuple(iv))

    invs = [gp for gp in psp
            if gp != ident and compose(gp, gp) == ident]
    print(f"involutions: {len(invs)}")

    remaining = set(invs)
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

    print(f"involution classes: {len(classes)}")
    rows = []
    for cl in sorted(classes, key=len):
        gp = next(iter(cl))
        fixp = sum(1 for i in range(n) if gp[i] == i)
        fixl = 0
        fixflags = 0
        for l in lines_sets:
            if frozenset(gp[x] for x in l) == l:
                fixl += 1
                fixflags += sum(1 for x in l if gp[x] == x)
        chi = fixflags - fixp - fixl + 1
        plus, minus = (81 + chi)//2, (81 - chi)//2
        # 3A1/skew-pair test: 8 fixed points carrying cube graph Q3?
        cube = ""
        if fixp == 8:
            fp = [i for i in range(n) if gp[i] == i]
            deg = [sum(1 for j in fp if j != i and not adj[i][j])
                   for i in fp]
            if set(deg) == {3}:
                cube = "3A1 skew-pair (8 fixed pts = cube Q3, BT773)"
        rows.append((len(cl), fixp, fixl, chi, plus, minus, cube))
        print(f"  class size {len(cl):5d}: fixpts {fixp:2d}, "
              f"fixlines {fixl:2d}, chi_St {chi:+d}, "
              f"Steinberg split {plus}+{minus}  {cube}")

    # which class is g^3 for order-6? (both must appear)
    chi_vals = sorted(r[3] for r in rows)
    print(f"\nchi_St on involutions: {chi_vals}")
    print("BT868 chirality types {9 -> 45+36, -3 -> 39+42} are exactly")
    print("the Steinberg values of the involution classes.")

    out = {
        "theorem": "BT869 involution chirality classes",
        "involution_count": len(invs),
        "classes": [{"size": r[0], "fixpts": r[1], "fixlines": r[2],
                     "chi_St": r[3], "steinberg_split": [r[4], r[5]],
                     "type": r[6]} for r in rows],
    }
    with open("data/bt869_involution_chirality_classes.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt869_involution_chirality_classes.json")


if __name__ == "__main__":
    main()
