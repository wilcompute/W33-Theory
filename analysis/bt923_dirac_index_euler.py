#!/usr/bin/env python3
"""
BT923 - The Hodge-Dirac index = the Euler characteristic = -v
        (hard open #2: certifying the spectral triple).

The finite spectral triple (BT921) is (A, H, D) with
H = C_0 + C_1 + C_2 (440-dim) and D = d + d^* the Hodge-Dirac.
Equipping it with the chirality grading gamma (+1 on even cochains
C_0,C_2; -1 on odd C_1) makes it an EVEN spectral triple.  Checked:

  T1  gamma^2 = 1 and gamma D = -D gamma (D shifts cochain degree by
      +-1): a genuine Z2-grading.
  T2  McKean-Singer index: ind(D) = Tr(gamma e^{-tD^2}) = sum of
      gamma over the harmonic forms = (b_0 + b_2) - b_1
      = (1 + 40) - 81 = -40 = -v = the Euler characteristic
      chi = 40 - 240 + 160 of the W(3,3) 2-complex.
  T3  so the substrate's vertex count v = 40 is the (negative) index
      of its Hodge-Dirac operator - an index-theorem identity tying
      the NCG/Dirac structure to the substrate size, with the matter
      register (b_1 = 81 = Steinberg) dominating the odd sector.
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
    nv, ne, nt = 40, len(edges), len(tris)

    D1 = np.zeros((nv, ne))     # C1 -> C0
    for j, (a, b) in enumerate(edges):
        D1[b, j] = 1.0
        D1[a, j] = -1.0
    D2 = np.zeros((ne, nt))     # C2 -> C1
    for j, (x, y, z) in enumerate(tris):
        D2[eidx[(y, z)], j] = 1.0
        D2[eidx[(x, z)], j] = -1.0
        D2[eidx[(x, y)], j] = 1.0

    N = nv + ne + nt            # 440
    # Dirac D = d + d^* on C0+C1+C2: blocks
    #   D maps C1->C0 (D1) and C0->C1 (D1^T); C2->C1 (D2) and C1->C2 (D2^T)
    D = np.zeros((N, N))
    # index ranges: C0 [0:nv], C1 [nv:nv+ne], C2 [nv+ne:N]
    a0, a1, a2 = 0, nv, nv+ne
    D[a0:a1, a1:a2] = D1               # C1 -> C0
    D[a1:a2, a0:a1] = D1.T             # C0 -> C1
    D[a1:a2, a2:N] = D2                # C2 -> C1
    D[a2:N, a1:a2] = D2.T              # C1 -> C2
    assert np.allclose(D, D.T)

    # grading gamma: +1 on C0,C2 (even), -1 on C1 (odd)
    g = np.ones(N)
    g[a1:a2] = -1.0
    gamma = np.diag(g)

    # T1: gamma^2 = 1, gamma D = -D gamma
    assert np.allclose(gamma@gamma, np.eye(N))
    anti = np.allclose(gamma@D, -D@gamma)
    print(f"T1 gamma^2=1 and gamma D = -D gamma (Z2-graded Dirac): {anti}")
    assert anti

    # T2: harmonic forms and index
    D2mat = D @ D
    evals = np.linalg.eigvalsh(D2mat)
    nharm = int(np.sum(np.abs(evals) < 1e-8))
    # harmonic = ker D; split by grade
    L0 = D1 @ D1.T
    L1 = D1.T @ D1 + D2 @ D2.T
    L2 = D2.T @ D2
    b0 = int(np.sum(np.abs(np.linalg.eigvalsh(L0)) < 1e-8))
    b1 = int(np.sum(np.abs(np.linalg.eigvalsh(L1)) < 1e-8))
    b2 = int(np.sum(np.abs(np.linalg.eigvalsh(L2)) < 1e-8))
    print(f"T2 harmonic forms: b0={b0}, b1={b1}, b2={b2} "
          f"(total {b0+b1+b2} = ker D)")
    assert (b0, b1, b2) == (1, 81, 40) and nharm == b0+b1+b2
    index = (b0 + b2) - b1
    euler = nv - ne + nt
    print(f"T2 McKean-Singer index ind(D) = (b0+b2) - b1 = {b0+b2} - "
          f"{b1} = {index}")
    print(f"   Euler characteristic chi = {nv} - {ne} + {nt} = {euler}")
    assert index == euler == -40
    print(f"   ind(D) = chi = -40 = -v  [index theorem]")

    # T3
    print(f"T3 the substrate vertex count v = {nv} is MINUS the index of")
    print(f"   its Hodge-Dirac operator; the odd (b1=81=Steinberg) sector")
    print(f"   dominates, so the matter register drives the index.")

    out = {
        "theorem": "BT923 Hodge-Dirac index = Euler char = -v",
        "graded": bool(anti),
        "betti": [b0, b1, b2],
        "index": index, "euler": euler, "minus_v": -nv,
    }
    with open("data/bt923_dirac_index_euler.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt923_dirac_index_euler.json")


if __name__ == "__main__":
    main()
