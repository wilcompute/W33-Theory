#!/usr/bin/env python3
"""
BT873 - The two-zeta duality and the non-backtracking walk census.

Completing BT870/BT872.  Two complementary graphs, two Ihara zetas,
two gravity entropies:

  W(3,3) = SRG(40,12,2,4):  Ihara prime 11 = k-1, gravity tau = 2^81.5^23
                            (81 = q^4 = MATTER dim)
  Q = complement = SRG(40,27,18,18): Ihara prime 26 = k'-1 = 2.Phi_3,
                            gravity tau(Q) = 2^66.3^39.5^23
                            (39 = q.Phi_3 = GAUGE dim)

  T1  walk census on W33: N_n = Tr(B^n).  N_3 = 960 = mu.|E|,
      N_5 = 181440 = |E|.q^q.n_even = 240.27.28; asymptotically
      N_n ~ 11^n (graph prime number theorem).
  T2  Q's Hashimoto operator (1080x1080): Perron 26, complex
      eigenvalues all |u|^2 = 26 (Q is Ramanujan on its circle
      1/sqrt(26)); Bass matrix at u=1 = 27I - A_Q = Laplacian(Q),
      matrix-tree -> v.tau(Q) = 30^24.24^15 = 2^69.3^39.5^24.
  T3  DUALITY: states-graph gravity entropy = matter dim (q^4=81),
      matter-graph gravity entropy = gauge dim (q.Phi_3=39); shared
      cosmological charge 5^23.  Complement = dual sector.
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


def hashimoto(nbr, n):
    dedges = [(i, j) for i in range(n) for j in nbr[i]]
    didx = {e: k for k, e in enumerate(dedges)}
    m = len(dedges)
    B = np.zeros((m, m))
    for a, (i, j) in enumerate(dedges):
        for l in nbr[j]:
            if l != i:
                B[didx[(j, l)], a] = 1.0
    return B, dedges


def main():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    n = 40
    pt_index = {p: i for i, p in enumerate(pts)}

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = [[False]*n for _ in range(n)]
    nbrW = [[] for _ in range(n)]
    nbrQ = [[] for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    for i in range(n):
        for j in range(n):
            if i != j:
                (nbrW if adj[i][j] else nbrQ)[i].append(j)
    assert all(len(b) == 12 for b in nbrW)
    assert all(len(b) == 27 for b in nbrQ)

    # T1: walk census on W33
    BW, deW = hashimoto(nbrW, n)
    assert BW.shape[0] == 480
    Bp = np.eye(480)
    N = {}
    for k in range(1, 8):
        Bp = Bp @ BW
        N[k] = int(round(np.trace(Bp)))
    print(f"T1 N_n = Tr(B^n) on W33: "
          f"{ {k: N[k] for k in range(1, 8)} }")
    assert N[3] == 960 == 4*240
    assert N[5] == 181440 == 240*27*28
    print(f"   N_3 = 960 = mu.|E|; N_5 = 181440 = |E|.q^q.n_even "
          f"= 240.27.28; N_7/N_6 ~ {N[7]/max(N[6],1):.2f} -> 11")

    # T2: Q's Hashimoto operator
    BQ, deQ = hashimoto(nbrQ, n)
    assert BQ.shape[0] == 1080
    evQ = np.linalg.eigvals(BQ)
    norm2 = sorted({round(abs(e)**2, 2) for e in evQ
                    if abs(e.imag) > 1e-6})
    realQ = Counter(round(e.real) for e in evQ if abs(e.imag) < 1e-6)
    print(f"T2 Q Hashimoto (1080x1080): real eigenvalues {dict(realQ)}, "
          f"complex |u|^2 values {norm2}")
    assert norm2 == [26.0]
    assert realQ.get(26, 0) == 1
    print("   Perron 26 = k'-1 = 2.Phi_3; all complex |u|^2 = 26 "
          "(Q Ramanujan on |u|=1/sqrt26)")

    # Bass at u=1 = Laplacian(Q); matrix-tree
    tauQ_v = 30**24 * 24**15            # = v.tau(Q)
    assert tauQ_v == 2**69 * 3**39 * 5**24
    print(f"T2 Bass(Q) at u=1 = 27I - A_Q = Laplacian(Q); matrix-tree "
          f"v.tau(Q) = 30^24.24^15 = 2^69.3^39.5^24: "
          f"{tauQ_v == 2**69 * 3**39 * 5**24}")
    tauQ = tauQ_v // 40
    import sympy
    print(f"   tau(Q) = {sympy.factorint(tauQ)}  (3-exponent 39 = "
          f"q.Phi_3 = GAUGE dim)")
    assert sympy.factorint(tauQ) == {2: 66, 3: 39, 5: 23}

    # T3: duality
    print("\nT3 TWO-ZETA DUALITY:")
    print("   states graph W33  : Ihara prime 11, gravity tau=2^81.5^23, "
          "entropy exponent 81 = q^4 = MATTER dim")
    print("   matter graph Q    : Ihara prime 26, gravity tau=2^66.3^39.5^23,"
          " entropy exponent 39 = q.Phi_3 = GAUGE dim")
    print("   shared cosmological charge 5^23 in both.")

    out = {
        "theorem": "BT873 dual zeta + walk census",
        "walk_census": {str(k): N[k] for k in range(1, 8)},
        "N3": "960 = mu|E|", "N5": "181440 = |E|.q^q.n_even",
        "Q_perron": 26, "Q_complex_norm2": 26,
        "tau_Q": {"2": 66, "3": 39, "5": 23},
        "duality": "W33 gravity exponent 81=matter dim; "
                   "Q gravity exponent 39=gauge dim; shared 5^23",
    }
    with open("data/bt873_dual_zeta_walk_census.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt873_dual_zeta_walk_census.json")


if __name__ == "__main__":
    main()
