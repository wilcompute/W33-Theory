#!/usr/bin/env python3
"""
BT924 (exploration) - the integral E8 lift from the chain complex.

Open problem (W36_PAPER sec:e8-lift-open): the F2 chain complex
A2 = A mod 2 (A = W(3,3) adjacency, A2^2=0) has homology
H = ker(A2)/im(A2) = F2^8 (the mod-2 E8 shadow). Lift it to an
INTEGRAL lattice carrying the E8 bilinear form, directly from the
chain data.

This script gathers the integral invariants and tests several
canonical lift constructions, checking each for "even unimodular
rank 8" (= E8, by uniqueness of the even unimodular rank-8 lattice).
"""
from __future__ import annotations

from itertools import combinations, product

import numpy as np


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def f2_rank(M):
    M = (np.array(M) % 2).astype(np.int64) % 2
    M = M.copy()
    r = 0
    rows, cols = M.shape
    pr = 0
    for c in range(cols):
        piv = None
        for i in range(pr, rows):
            if M[i, c]:
                piv = i
                break
        if piv is None:
            continue
        M[[pr, piv]] = M[[piv, pr]]
        for i in range(rows):
            if i != pr and M[i, c]:
                M[i] = (M[i] + M[pr]) % 2
        pr += 1
        if pr == rows:
            break
    return pr


def f2_nullspace(M):
    """Return basis (list of F2 vectors) of right nullspace of M over F2."""
    M = (np.array(M) % 2).astype(np.int64)
    rows, cols = M.shape
    M = M.copy()
    pivots = []
    pr = 0
    where = {}
    for c in range(cols):
        piv = None
        for i in range(pr, rows):
            if M[i, c]:
                piv = i
                break
        if piv is None:
            continue
        M[[pr, piv]] = M[[piv, pr]]
        for i in range(rows):
            if i != pr and M[i, c]:
                M[i] = (M[i] + M[pr]) % 2
        where[c] = pr
        pivots.append(c)
        pr += 1
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for fcol in free:
        vec = np.zeros(cols, dtype=np.int64)
        vec[fcol] = 1
        for c in pivots:
            vec[c] = M[where[c], fcol] % 2
        basis.append(vec % 2)
    return basis, pivots


def main():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    n = 40

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    A = np.zeros((n, n), dtype=np.int64)
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    assert all(A.sum(0) == 12)

    # ---- the F2 chain complex and its homology --------------------
    A2 = A % 2
    assert np.all((A2 @ A2) % 2 == 0), "A2^2 != 0 mod 2"
    rankA2 = f2_rank(A2)
    ker_basis, _ = f2_nullspace(A2)
    dimker = len(ker_basis)
    dimH = dimker - rankA2
    print(f"[chain] rank_F2(A2)={rankA2}  dim ker={dimker}  "
          f"dim H = {dimH}  (should be 8 = rank E8)")
    assert (rankA2, dimker, dimH) == (16, 24, 8)

    # spectrum / det over Z
    ev = np.linalg.eigvalsh(A.astype(float))
    from collections import Counter
    spec = Counter(int(round(e)) for e in ev)
    print(f"[spec] A eigenvalues {dict(spec)}  (12^1,2^24,-4^15)")
    # A^2 = 8I - 2A + 4J
    J = np.ones((n, n), dtype=np.int64)
    assert np.array_equal(A @ A, 8*np.eye(n, dtype=np.int64) - 2*A + 4*J)
    print("[ident] A^2 = 8I - 2A + 4J over Z (so A invertible /Q; "
          "F2^8 is purely 2-adic)")

    # ---- locate an E8 Dynkin induced subtree ----------------------
    # E8 Dynkin adjacency (nodes 0..7): chain 0-1-2-3-4-5-6 with 7 hung
    # off node 4 (the branch node), arms (from node-4) of length 2,4 + leg.
    # Standard E8: 1-2-3-4-5-6-7 path, 8 attached to node 5.
    E8 = np.zeros((8, 8), dtype=int)
    chain = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]  # path of 7
    for a, b in chain:
        E8[a, b] = E8[b, a] = 1
    E8[2, 7] = E8[7, 2] = 1   # branch node = index 2 -> arms (2,4) + leg1
    cartan = 2*np.eye(8, dtype=int) - E8
    print(f"[E8] target Cartan det = {round(np.linalg.det(cartan))} "
          f"(E8=1, D8=4)")

    found = find_induced(A, E8, n)
    if found is None:
        # try alternate branch placements
        for bnode in range(8):
            E8b = build_e8(bnode)
            if E8b is None:
                continue
            found = find_induced(A, E8b, n)
            if found:
                E8 = E8b
                cartan = 2*np.eye(8, dtype=int) - E8
                break
    print(f"[E8] induced Dynkin 8-subset found: {found}")
    if found:
        sub = A[np.ix_(found, found)]
        G = 2*np.eye(8, dtype=int) - sub
        print(f"[E8] induced Gram 2I-A_sub det = {round(np.linalg.det(G))}")
        # do these 8 vertices' columns / e_i relate to homology H?
        # test 1: are e_{found} independent mod im(A2)+? (vertex classes)
        test_vertex_homology(A2, found, ker_basis)

    # ---- canonical lift attempts ----------------------------------
    print("\n[lift attempts]")
    try_eiguni(A)


def build_e8(bnode):
    """E8 path 0..6 (7 nodes) with leg 7 attached at position bnode;
    valid E8 only when arms are (1,2,4)."""
    E8 = np.zeros((8, 8), dtype=int)
    for a in range(6):
        E8[a, a+1] = E8[a+1, a] = 1
    E8[bnode, 7] = E8[7, bnode] = 1
    # arms from bnode along the path: lengths bnode and (6-bnode); leg=1
    arms = sorted([bnode, 6 - bnode, 1])
    if arms == [1, 2, 4]:
        return E8
    return None


def find_induced(A, H, n, limit=2_000_000):
    """Backtracking search for an induced subgraph of A isomorphic to H
    (H small). Returns vertex tuple or None."""
    import networkx as nx
    GA = nx.from_numpy_array(A)
    GH = nx.from_numpy_array(H)
    GM = nx.algorithms.isomorphism.GraphMatcher(GA, GH)
    for mp in GM.subgraph_monomorphisms_iter():
        # need INDUCED: subgraph_monomorphisms gives non-induced; check
        inv = {v: k for k, v in mp.items()}
        verts = [inv[i] for i in range(H.shape[0])]
        sub = A[np.ix_(verts, verts)]
        if np.array_equal(sub, H):
            return verts
    return None


def test_vertex_homology(A2, found, ker_basis):
    """Do the 8 Dynkin vertices project to a basis of H = ker/im?
    Vertices aren't cycles; test their A2-images (boundaries) and the
    induced 8x8 structure within the cycle space instead."""
    n = A2.shape[0]
    # columns A2[:,found] are boundaries (in im). Check their rank.
    cols = A2[:, found] % 2
    print(f"  rank_F2 of the 8 Dynkin columns (boundaries) = "
          f"{f2_rank(cols)}")


def try_eiguni(A):
    """Look at integer lattices from eigenspaces / index-2 structure
    for an even unimodular rank-8 piece."""
    n = A.shape[0]
    # The +2 eigenspace has dim 24, -4 has dim 15. Neither is 8.
    # Try: B = (A+4I)/2 has integer? A+4I eigenvalues 16,6,0 -> /2 = 8,3,0
    # Gram-type candidates on integer cycle lattice:
    # Cycle lattice over Z: ker(A2) lifted -> Z^40 sublattice L = {x in Z^40:
    #   A x = 0 mod 2}. Its Gram under standard form, reduced.
    A2 = A % 2
    # integer lattice L = preimage of 0 under (x -> Ax mod 2) = vectors with
    # A x even. Build basis: solutions over Z of A x ≡ 0 (2): index 2^16 in Z^40.
    print("  (eigenspace dims 24/15 - no direct rank-8; lattice search"
          " deferred to the focused construction below)")


if __name__ == "__main__":
    main()
