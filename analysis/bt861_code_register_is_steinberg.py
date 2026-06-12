#!/usr/bin/env python3
"""
BT861 - The code register IS the Steinberg module.

The single-photon paper's CSS code [[240, 81, 4, 3]]_3 stores its 81
logical qutrits in H1 of the W(3,3) 2-complex (vertices 40, edges 240,
triangles 160 - all triangles lie inside the 40 line-K4s).  The
holonet's protected memory is the STEINBERG module, the unique 81-dim
irreducible of U4(2) (BT742: GAP-verified uniqueness).  Tested here by
complete character computation over ALL 25920 group elements:

  T1  dim H1 = 81 (240 - 39 - 120), dim H2 = 40.
  T2  the character of PSp(4,3) on H1 (tensored to C) has norm
      <chi, chi> = 1: H1 is IRREDUCIBLE - hence it is THE 81-dim
      irrep, the Steinberg module.
  T3  cross-check: chi_H1(g) = chi_St(g) = #fixflags - #fixpoints
      - #fixlines + 1 for all g (Solomon-Tits alternating sum over
      the rank-2 building: chambers - vertices of both types + 1).

Consequence: the QECC logical space and the holonet's Schur-protected
register are ONE object; protection by symmetry extends to the code.
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
    assert len(lines) == 40

    edges = sorted({tuple(sorted((i, j))) for i, j in
                    combinations(range(n), 2) if adj[i][j]})
    assert len(edges) == 240
    eidx = {e: i for i, e in enumerate(edges)}
    tris = sorted({tuple(sorted(t)) for l in lines
                   for t in combinations(sorted(l), 3)})
    assert len(tris) == 160

    # boundary maps
    d0 = np.zeros((n, 240))
    for i, (a, b) in enumerate(edges):
        d0[b, i] = 1.0
        d0[a, i] = -1.0
    d1 = np.zeros((240, 160))
    for j, (x, y, z) in enumerate(tris):
        d1[eidx[(y, z)], j] = 1.0
        d1[eidx[(x, z)], j] = -1.0
        d1[eidx[(x, y)], j] = 1.0

    r0 = np.linalg.matrix_rank(d0)
    r1 = np.linalg.matrix_rank(d1)
    dimH1 = 240 - r0 - r1
    print(f"T1 ranks: d0 {r0}, d1 {r1}; dim H1 = {dimH1}, "
          f"dim H2 = {160 - r1}")
    assert dimH1 == 81

    # orthogonal projectors (im d1 is inside ker d0)
    P_ker = np.eye(240) - d0.T @ np.linalg.pinv(d0 @ d0.T) @ d0
    P_im = d1 @ np.linalg.pinv(d1.T @ d1) @ d1.T
    P_H1 = P_ker - P_im
    assert abs(np.trace(P_H1) - 81) < 1e-6

    # group
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

    # line lookup for flags
    line_of = {}
    for li, l in enumerate(lines):
        for pr in combinations(sorted(l), 2):
            line_of[pr] = li
    lines_sets = [frozenset(l) for l in lines]

    norm_acc = 0.0
    match = True
    chi_vals = Counter()
    for gp in psp:
        # chi_H1(g) = sum_f sign(f) * P_H1[f, g(f)]
        tr = 0.0
        for fi, (a, b) in enumerate(edges):
            ga, gb = gp[a], gp[b]
            if ga < gb:
                gi, s = eidx[(ga, gb)], 1.0
            else:
                gi, s = eidx[(gb, ga)], -1.0
            tr += s * P_H1[fi, gi]
        chi = round(tr)
        assert abs(tr - chi) < 1e-6
        norm_acc += chi * chi
        # Solomon-Tits: chi_St = fixflags - fixpoints - fixlines + 1
        fixp = sum(1 for i in range(n) if gp[i] == i)
        fixl = 0
        fixflags = 0
        for li, l in enumerate(lines_sets):
            if frozenset(gp[x] for x in l) == l:
                fixl += 1
                fixflags += sum(1 for x in l if gp[x] == x)
        st = fixflags - fixp - fixl + 1
        if st != chi:
            match = False
        chi_vals[chi] += 1

    norm = norm_acc / 25920
    print(f"T2 <chi_H1, chi_H1> = {norm} (1.0 = irreducible)")
    assert abs(norm - 1.0) < 1e-9
    print("   => H1 is IRREDUCIBLE of dim 81 = the unique 81-dim irrep")
    print("      = THE STEINBERG MODULE")
    print(f"T3 chi_H1(g) == fixflags - fixpoints - fixlines + 1 "
          f"(Solomon-Tits) for ALL 25920 g: {match}")
    assert match
    print("\nTHEOREM: the [[240,81,4,3]]_3 code's logical space = H1 of")
    print("the W(3,3) 2-complex = the Steinberg module, as PSp-reps.")
    print("Schur protection extends to the QECC: any equivariant logical")
    print("error operator is a scalar.")

    out = {
        "theorem": "BT861 code register is Steinberg",
        "dims": {"H1": 81, "H2": 160 - int(r1),
                 "rank_d0": int(r0), "rank_d1": int(r1)},
        "norm": 1.0,
        "flag_formula_match": match,
        "character_value_distribution": {str(k): v for k, v in
                                         sorted(chi_vals.items())},
    }
    with open("data/bt861_code_register_is_steinberg.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt861_code_register_is_steinberg.json")


if __name__ == "__main__":
    main()
