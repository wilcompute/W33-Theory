#!/usr/bin/env python3
"""
Topological order from the substrate: the matter-graph 2T gauge theory is the
quantum double D(2T), a non-abelian anyon model with 42 anyons and total quantum
dimension f = 24.

The matter graph Q carries a finite-group 2T = SL(2,3) lattice gauge theory
(w33_lattice_to_continuum_ym.py). Its exactly-solvable topological phase is the
Kitaev quantum double / Dijkgraaf-Witten model D(2T). Its anyons (the
superselection sectors) are the irreps of the quantum double, labelled by pairs
([g], chi) with [g] a conjugacy class of 2T and chi an irrep of the centralizer
C(g); the count is

    N_anyons = sum over conjugacy classes [g] of k(C(g)),

with k = number of conjugacy classes (= number of irreps). The total quantum
dimension obeys D^2 = sum_a d_a^2 = |G|^2, so D = |2T| = 24 = f.

Computed here from 2T = SL(2,3) directly:
  - 7 conjugacy classes (sizes 1,1,6,4,4,4,4);
  - centralizers: G (for +-I), C4 (order-4 class), C6 (order-3/6 classes);
  - N_anyons = 7 + 7 + 4 + 6 + 6 + 6 + 6 = 42 = Catalan C5 = 2q*Phi_6;
  - total quantum dimension D = 24 = f.

So the substrate's topological protection is concrete: logical information is the
fusion/braiding data of a D(2T) anyon model whose total quantum dimension is the
matter count f = 24 and whose anyon count is 42 = C5.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter

F = 3


def matmul(A, B):
    return tuple(
        tuple(sum(A[i][k] * B[k][j] for k in range(2)) % F for j in range(2))
        for i in range(2)
    )


def det(A):
    return (A[0][0] * A[1][1] - A[0][1] * A[1][0]) % F


def sl23():
    G = []
    for a, b, c, d in itertools.product(range(F), repeat=4):
        M = ((a, b), (c, d))
        if det(M) == 1:
            G.append(M)
    return G


def order(M, G_index, I):
    P, k = M, 1
    while P != I:
        P = matmul(P, M)
        k += 1
    return k


def conjugacy_classes(G):
    Gset = set(G)
    seen, classes = set(), []
    for g in G:
        if g in seen:
            continue
        cls = set()
        for x in G:
            xi = inverse(x)
            cls.add(matmul(matmul(x, g), xi))
        classes.append(sorted(cls))
        seen |= cls
    return classes


def inverse(M):
    (a, b), (c, d) = M
    # det = 1, so inverse = [[d,-b],[-c,a]]
    return ((d % F, (-b) % F), ((-c) % F, a % F))


def centralizer(g, G):
    return [x for x in G if matmul(x, g) == matmul(g, x)]


def num_classes(H):
    Hset = set(H)
    seen, n = set(), 0
    for g in H:
        if g in seen:
            continue
        cls = {matmul(matmul(x, g), inverse(x)) for x in H}
        seen |= cls
        n += 1
    return n


def main():
    out = {}
    G = sl23()
    assert len(G) == 24
    I = ((1, 0), (0, 1))
    print(f"[2T = SL(2,3)] order {len(G)} (binary tetrahedral)")

    classes = conjugacy_classes(G)
    sizes = sorted(len(c) for c in classes)
    print(f"  {len(classes)} conjugacy classes, sizes {sizes}")
    assert len(classes) == 7 and sizes == [1, 1, 4, 4, 4, 4, 6]

    # anyons of D(2T): sum over classes of k(centralizer)
    anyons, table = 0, []
    for cls in classes:
        g = cls[0]
        C = centralizer(g, G)
        kC = num_classes(C)
        anyons += kC
        o = order(g, None, I)
        table.append(
            {
                "class_size": len(cls),
                "rep_order": o,
                "centralizer_order": len(C),
                "k_centralizer": kC,
            }
        )
    print(f"\n[D(2T) anyons] N = sum k(C(g)) over classes:")
    for row in sorted(table, key=lambda r: (r["class_size"], r["rep_order"])):
        print(
            f"  class size {row['class_size']:2d} (ord {row['rep_order']}): "
            f"|C|={row['centralizer_order']:2d}, k(C)={row['k_centralizer']}"
        )
    print(f"  => N_anyons = {anyons}")
    assert anyons == 42

    D2 = len(G) ** 2
    D = len(G)
    q, f, Phi6 = 3, 24, 7
    catalan5 = 42
    print(f"\n[total quantum dimension] D^2 = |2T|^2 = {D2}, D = {D} = f")
    print(
        f"[resonances] N_anyons = 42 = Catalan C5 = 2q*Phi_6 = {2*q*Phi6}; "
        f"D = 24 = f"
    )
    assert D == f == 24 and anyons == catalan5 == 2 * q * Phi6
    out["n_anyons"] = anyons
    out["total_quantum_dimension"] = D
    out["D_squared"] = D2
    out["anyon_table"] = table

    print("\nRESULT: the substrate's matter-graph 2T gauge theory is the quantum")
    print("  double D(2T) -- a non-abelian topological order with 42 anyon types")
    print("  (= Catalan C5 = 2q*Phi_6) and total quantum dimension D = 24 = f. The")
    print("  7 pure-flux sectors are the 7 conjugacy classes of 2T; the charges are")
    print("  centralizer irreps. Topological protection is then concrete: logical")
    print("  information lives in the fusion and braiding of these anyons, and the")
    print("  total quantum dimension is exactly the matter count f. (The non-abelian")
    print("  2T anyons are computationally richer than abelian toric-code anyons,")
    print("  matching the holonet's need for non-Clifford magic.)")

    out["summary"] = (
        "matter-graph 2T=SL(2,3) gauge theory = quantum double D(2T): "
        "7 flux sectors (conjugacy classes), 42 anyons (= Catalan C5 "
        "= 2q*Phi_6), total quantum dimension D = |2T| = 24 = f. "
        "Non-abelian topological order; logical info = anyon fusion/"
        "braiding; D = matter count f."
    )
    out["sources"] = [
        "Kitaev, Fault-tolerant quantum computation by anyons, "
        "Ann. Phys. 303 (2003); Dijkgraaf-Witten quantum double D(G); "
        "w33_lattice_to_continuum_ym.py (2T lattice gauge theory)"
    ]
    with open("data/w33_anyons_from_2T.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_anyons_from_2T.json")


if __name__ == "__main__":
    main()
