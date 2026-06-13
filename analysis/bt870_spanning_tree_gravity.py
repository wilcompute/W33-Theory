#!/usr/bin/env python3
"""
BT870 - Gravity from spanning trees: tau(W33) = 2^81 . 5^23, the
        matter-sector dimension as the 2-exponent.

W33_FOR_EVERYONE.tex (mined): the finite gravitational bridge is the
discrete Matrix-Tree action S = (M_P^2/2) ln tau(G), tau = number of
spanning trees.  For an SRG the spanning-tree count is exact via the
Matrix-Tree theorem (tau = product of nonzero Laplacian eigenvalues
/ v).  Computed and factored here:

  W33 = SRG(40,12,2,4): Laplacian spectrum {0, 10^(f=24), 16^(g=15)}
     tau(W33) = 10^24 . 16^15 / 40 = 2^81 . 5^23
       * 2-exponent  81 = q^4 = dim(matter sector) = dim Steinberg
       * base        5  = F_5 (the tier-ladder prime, r = 27/80)
       * 5-exponent  23 = f - 1

  Q = complement = SRG(40,27,18,18): Laplacian {0, 30^24, 24^15}
     tau(Q) = 30^24 . 24^15 / 40 = 2^66 . 3^39 . 5^23
       * 3-exponent  39 = q.Phi_3 = dim(gauge sector) = rank(d0)

So the gravitational partition function of the substrate writes the
matter-sector dimension into the exponent of 2, and (on the matter
graph Q) the gauge-sector dimension into the exponent of 3.  The
Matrix-Tree action is S = (M_P^2/2)(81 ln2 + 23 ln5).
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json

import numpy as np
import sympy


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

    A = np.zeros((n, n))
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i][j] = A[j][i] = 1.0

    # T1: adjacency spectrum confirms SRG(40,12,2,4)
    ev = sorted(np.linalg.eigvalsh(A), reverse=True)
    spec = Counter(int(round(e)) for e in ev)
    print(f"T1 adjacency spectrum: {dict(sorted(spec.items(), reverse=True))}")
    assert spec == {12: 1, 2: 24, -4: 15}

    # T2: Matrix-Tree on W33 (exact integer)
    tauW = 10**24 * 16**15 // 40
    fW = sympy.factorint(tauW)
    print(f"T2 tau(W33) = 10^24 . 16^15 / 40 = {dict(fW)}")
    assert fW == {2: 81, 5: 23}
    # cross-check via integer cofactor determinant of the Laplacian
    L = (np.diag(A.sum(1)) - A).astype(np.int64)
    # exact: reduced Laplacian determinant equals tau; use sympy for exactness
    Lr = sympy.Matrix((np.diag(A.sum(1)) - A)[1:, 1:].astype(int).tolist())
    tau_det = int(Lr.det())
    print(f"T2 cofactor determinant = {sympy.factorint(tau_det)} "
          f"(matches: {tau_det == tauW})")
    assert tau_det == tauW
    print("   => 2-exponent 81 = q^4 = matter/Steinberg dim; "
          "base 5 = F_5; 5-exponent 23 = f-1")

    # T3: complement Q = SRG(40,27,18,18)
    Acomp = (np.ones((n, n)) - np.eye(n)) - A
    evc = Counter(int(round(e)) for e in
                  np.linalg.eigvalsh(Acomp))
    print(f"T3 complement spectrum: {dict(sorted(evc.items(), reverse=True))}")
    assert evc == {27: 1, 3: 15, -3: 24}
    tauQ = 30**24 * 24**15 // 40
    fQ = sympy.factorint(tauQ)
    print(f"T3 tau(Q) = 30^24 . 24^15 / 40 = {dict(fQ)}")
    assert fQ == {2: 66, 3: 39, 5: 23}
    print("   => 3-exponent 39 = q.Phi_3 = gauge-sector dim = rank(d0)")

    # action readings
    lnW = 81*np.log(2) + 23*np.log(5)
    print(f"\nMatrix-Tree action ln tau(W33) = 81 ln2 + 23 ln5 = {lnW:.4f}")
    print("THEOREM: the substrate gravitational partition function")
    print("(spanning-tree count) is tau(W33) = 2^81 . 5^23 - the")
    print("matter-sector dimension q^4 = 81 IS the exponent of 2; the")
    print("matter graph Q writes the gauge dimension 39 into the")
    print("exponent of 3.")

    out = {
        "theorem": "BT870 spanning-tree gravity",
        "tau_W33": {"2": 81, "5": 23,
                    "readings": {"81": "q^4 = matter/Steinberg dim",
                                 "5": "F_5", "23": "f-1"}},
        "tau_Q": {"2": 66, "3": 39, "5": 23,
                  "readings": {"39": "q*Phi_3 = gauge dim = rank(d0)"}},
        "action_lnTau_W33": lnW,
    }
    with open("data/bt870_spanning_tree_gravity.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt870_spanning_tree_gravity.json")


if __name__ == "__main__":
    main()
