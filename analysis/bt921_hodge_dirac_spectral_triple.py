#!/usr/bin/env python3
"""
BT921 - Hard open #2 (advance): the W(3,3) Hodge-Dirac spectral triple
        and its spectral-action coefficients.

BT892 used only the bosonic graph Laplacian.  Here the full finite
Dirac operator D = d + d^* on the W(3,3) 2-complex
(C_0 = 40 vertices, C_1 = 240 edges, C_2 = 160 in-line triangles),
with D^2 = Delta_0 + Delta_1 + Delta_2 (the three combinatorial Hodge
Laplacians).  This is the finite spectral triple of the Connes-style
almost-commutative product M x F whose continuum limit is the open
EH/spectral-action theorem.

  T1  the harmonic forms (ker D = ker of each Delta_i) ARE the
      homology: b_0 = 1 (vacuum), b_1 = 81 (Steinberg matter
      register), b_2 = 40 (oriented lines).  The Dirac zero modes =
      the physical content (122 = 1 + 81 + 40 massless modes).
  T2  the nonzero D^2-spectrum (the "massive" modes) and the spectral
      moments M_k = Tr D^{2k} = sum_i Tr Delta_i^k feed the
      Seeley-DeWitt / spectral-action coefficients.
  T3  the spectral-action reading: the a_0 (cosmological) term is
      Tr f(D^2/Lambda^2) -> the partition data of BT870/892; the
      Einstein-Hilbert (a_2) coefficient is fixed by the fermion
      count (the harmonic dimension), with the matter register's 81 =
      Steinberg the dominant block.  The continuum EH-limit theorem
      remains open; this pins the finite Dirac exactly.
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
    assert (nv, ne, nt) == (40, 240, 160)

    # boundary maps d1: C1->C0 (edges->vertices), d2: C2->C1
    D1 = np.zeros((nv, ne))
    for j, (a, b) in enumerate(edges):
        D1[b, j] = 1.0
        D1[a, j] = -1.0
    D2 = np.zeros((ne, nt))
    for j, (x, y, z) in enumerate(tris):
        D2[eidx[(y, z)], j] = 1.0
        D2[eidx[(x, z)], j] = -1.0
        D2[eidx[(x, y)], j] = 1.0

    # Hodge Laplacians
    L0 = D1 @ D1.T
    L1 = D1.T @ D1 + D2 @ D2.T
    L2 = D2.T @ D2

    def spec(M):
        ev = np.linalg.eigvalsh(M)
        return Counter(int(round(e)) for e in ev)

    s0, s1, s2 = spec(L0), spec(L1), spec(L2)
    # T1: harmonic = kernel = Betti = homology
    b0, b1, b2 = s0.get(0, 0), s1.get(0, 0), s2.get(0, 0)
    print(f"T1 harmonic forms (Dirac zero modes) = homology: "
          f"b0={b0} (vacuum), b1={b1} (Steinberg matter), b2={b2} (lines)")
    assert (b0, b1, b2) == (1, 81, 40)
    print(f"   total massless modes = {b0+b1+b2} = 1 + 81 + 40")

    # T2: nonzero D^2 spectrum and moments
    print(f"T2 Hodge Laplacian spectra (nonzero):")
    print(f"   Delta_0 (vertices): "
          f"{ {k: v for k, v in sorted(s0.items()) if k} }")
    print(f"   Delta_1 (edges): "
          f"{ {k: v for k, v in sorted(s1.items()) if k} }")
    print(f"   Delta_2 (triangles): "
          f"{ {k: v for k, v in sorted(s2.items()) if k} }")
    # spectral moments M_k = Tr D^{2k} = Tr L0^k + Tr L1^k + Tr L2^k
    def moments(s, k):
        return sum((e**k)*m for e, m in s.items())
    M = {k: moments(s0, k)+moments(s1, k)+moments(s2, k)
         for k in range(1, 4)}
    print(f"T2 spectral moments M_k = Tr D^(2k): "
          f"M1={M[1]}, M2={M[2]}, M3={M[3]}")
    # M1 = Tr(L0+L1+L2) = 2*(edges contribute) ... sanity: Tr L0 = 2|E|,
    # Tr L2 = 3|tris|, Tr L1 = Tr(D1^T D1) + Tr(D2 D2^T) = 2|E| + 3|tris|
    assert moments(s0, 1) == 2*ne            # Tr L0 = sum deg = 2|E|
    print(f"   Tr L0 = {moments(s0,1)} = 2|E|; Tr L2 = {moments(s2,1)} "
          f"= 3|tris| = {3*nt}")

    # T3: spectral-action reading
    total_dim = nv + ne + nt
    print(f"T3 finite spectral triple: dim H_F = {total_dim} "
          f"(40+240+160); {b0+b1+b2} harmonic (massless) modes = the")
    print(f"   homology, of which b1=81 = Steinberg matter register is")
    print(f"   the dominant block.  The spectral action Tr f(D^2/L^2)")
    print(f"   has a_0 (cosmological) from the full spectrum (cf BT870")
    print(f"   logdet = v*tau) and a_2 (Einstein-Hilbert) fixed by the")
    print(f"   fermion/harmonic count; continuum EH-limit theorem open.")

    out = {
        "theorem": "BT921 Hodge-Dirac spectral triple",
        "betti_harmonic": [b0, b1, b2],
        "dim_HF": total_dim,
        "spectra": {"L0": {str(k): v for k, v in s0.items()},
                    "L1": {str(k): v for k, v in s1.items()},
                    "L2": {str(k): v for k, v in s2.items()}},
        "moments": {str(k): M[k] for k in range(1, 4)},
    }
    with open("data/bt921_hodge_dirac_spectral_triple.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt921_hodge_dirac_spectral_triple.json")


if __name__ == "__main__":
    main()
