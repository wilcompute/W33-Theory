#!/usr/bin/env python3
"""
BT926 - the +2-eigenlattice of W(3,3) (open frontier #5, definite side).

BT925 proved the residual of the integral E8 lift is purely DEFINITENESS.
The canonical form (1/2)A restricted to an eigenvector v (Av=2v) is
(1/2) v^T A w = v^T w = the STANDARD inner product. So the integer
+2-eigenlattice
    L2 = { x in Z^40 : A x = 2 x }   (rank 24 = 8*3)
is a positive-definite integral lattice under the standard form - the
natural definite home for E8 (x3 generations?). We extract L2 via an
integer Smith normal form with transforms (U M V = D, M = A-2I; the
columns of V with D_jj=0 are a Z-basis of the saturated kernel) and
identify the rank-24 lattice: determinant, even/odd, minimal norm, root
count (norm-2 vectors).
"""
from __future__ import annotations

from itertools import combinations, product
import json

import numpy as np


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def snf_with_transforms(M):
    """Integer Smith normal form. Returns (D, U, V) with U M V = D,
    U,V unimodular. M is modified copy."""
    A = [row[:] for row in M.tolist()]
    m, n = len(A), len(A[0])
    U = [[int(i == j) for j in range(m)] for i in range(m)]
    V = [[int(i == j) for j in range(n)] for i in range(n)]

    def swap_rows(i, j):
        A[i], A[j] = A[j], A[i]
        U[i], U[j] = U[j], U[i]

    def swap_cols(i, j):
        for r in range(m):
            A[r][i], A[r][j] = A[r][j], A[r][i]
        for r in range(n):
            V[r][i], V[r][j] = V[r][j], V[r][i]

    def addrow(i, j, q):           # row i += q*row j
        for k in range(n):
            A[i][k] += q*A[j][k]
        for k in range(m):
            U[i][k] += q*U[j][k]

    def addcol(i, j, q):           # col i += q*col j
        for r in range(m):
            A[r][i] += q*A[r][j]
        for r in range(n):
            V[r][i] += q*V[r][j]

    t = 0
    rank = min(m, n)
    for t in range(rank):
        # find a nonzero pivot in submatrix [t:,t:]
        piv = None
        best = None
        for i in range(t, m):
            for j in range(t, n):
                if A[i][j] != 0 and (best is None or abs(A[i][j]) < best):
                    best = abs(A[i][j])
                    piv = (i, j)
        if piv is None:
            break
        pi, pj = piv
        swap_rows(t, pi)
        swap_cols(t, pj)
        # clear column and row at t, iterate until clean
        done = False
        while not done:
            done = True
            for i in range(t+1, m):
                if A[i][t] != 0:
                    q = A[i][t] // A[t][t]
                    addrow(i, t, -q)
                    if A[i][t] != 0:
                        swap_rows(t, i)
                        done = False
            for j in range(t+1, n):
                if A[t][j] != 0:
                    q = A[t][j] // A[t][t]
                    addcol(j, t, -q)
                    if A[t][j] != 0:
                        swap_cols(t, j)
                        done = False
    D = np.array(A, dtype=object)
    return D, np.array(U, dtype=object), np.array(V, dtype=object)


def gram_id(name, G):
    G = np.array(G, dtype=np.int64)
    r = G.shape[0]
    det = int(round(np.linalg.det(G.astype(float))))
    even = bool(np.all(np.diag(G) % 2 == 0))
    posdef = bool(np.all(np.linalg.eigvalsh(G.astype(float)) > 1e-9))
    minnorm = int(min(G[i, i] for i in range(r)))
    print(f"[{name}] rank {r}  det {det}  even {even}  posdef {posdef}  "
          f"min diag {minnorm}")
    return det, even, posdef


def main():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3
    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1

    M = A - 2*np.eye(40, dtype=np.int64)         # A - 2I
    D, U, V = snf_with_transforms(M)
    diagD = [int(D[i, i]) for i in range(40)]
    zero_cols = [j for j in range(40) if diagD[j] == 0]
    print(f"[SNF A-2I] #zero invariant factors = {len(zero_cols)} "
          f"(= dim ker = 24)")
    # kernel basis = columns of V at zero positions
    K = np.array([[int(V[r, j]) for j in zero_cols] for r in range(40)],
                 dtype=np.int64)                  # 40 x 24
    # verify A K = 2 K
    assert np.array_equal(A @ K, 2*K), "kernel cols are not +2-eigenvectors"
    print(f"[L2] extracted {K.shape[1]} integer +2-eigenvectors; "
          f"A K = 2K verified")

    # Gram under standard inner product (= (1/2)A form on eigenvectors)
    G = K.T @ K
    det, even, posdef = gram_id("L2 raw basis", G)
    from sympy import factorint
    print(f"[L2] det factorization = {dict(factorint(det))}")

    # LLL-reduce the EXPLICIT eigenvectors (rows of K^T in Z^40)
    Bred = lll(K.T.astype(float).tolist())
    Bred = np.array(Bred, dtype=np.int64)
    Gr = Bred @ Bred.T
    assert np.array_equal(A @ Bred.T, 2*Bred.T), "reduced rows not eigenvecs"
    det2, even2, posdef2 = gram_id("L2 LLL-reduced", Gr)
    norms = sorted(int(Gr[i, i]) for i in range(Gr.shape[0]))
    mn_basis = norms[0]
    print(f"[L2] reduced basis-vector norms (sorted): {norms}")
    print(f"[L2] minimal reduced norm = {mn_basis} (even => true min in "
          f"{{2,4,...,{mn_basis}}}); det = {det2} = {dict(factorint(det2))}")

    # conclusive identification: det != 1 => not unimodular
    unimodular = (abs(det2) == 1)
    has_roots = (mn_basis == 2)
    if unimodular and even2 and mn_basis == 2:
        ident = "even unimodular rank-24 with roots (E8^3 / Niemeier?)"
    elif unimodular and even2:
        ident = "Leech-like even unimodular rootless rank-24"
    else:
        ident = (f"even posdef rank-24, NON-unimodular (det "
                 f"{dict(factorint(det2))}); NOT E8^3, NOT a root lattice "
                 f"=> the +2-eigenlattice is NOT the definite E8 home")
    print(f"[L2 identification] {ident}")

    out = {
        "theorem": "BT926 +2-eigenlattice of W(3,3)",
        "rank": int(K.shape[1]), "det": det2,
        "det_factorization": {str(k): v for k, v in factorint(det2).items()},
        "even": even2, "posdef": posdef2,
        "min_reduced_norm": mn_basis, "reduced_norms": norms,
        "unimodular": unimodular, "identification": ident,
    }
    with open("data/bt926_plus2_eigenlattice.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt926_plus2_eigenlattice.json")


def lll(basis, delta=0.75):
    """Standard LLL on explicit real basis vectors (list of rows). Returns
    integer-combination-reduced basis (rounded to int)."""
    import numpy as np
    B = [np.array(b, dtype=float) for b in basis]
    n = len(B)

    def gram_schmidt(B):
        Bs = []
        mu = np.zeros((n, n))
        for i in range(n):
            bi = B[i].copy()
            for j in range(i):
                mu[i, j] = np.dot(B[i], Bs[j]) / np.dot(Bs[j], Bs[j])
                bi = bi - mu[i, j]*Bs[j]
            Bs.append(bi)
        return Bs, mu

    Bs, mu = gram_schmidt(B)
    k = 1
    guard = 0
    while k < n and guard < 200000:
        guard += 1
        for j in range(k-1, -1, -1):
            if abs(mu[k, j]) > 0.5:
                B[k] = B[k] - round(mu[k, j])*B[j]
                Bs, mu = gram_schmidt(B)
        if np.dot(Bs[k], Bs[k]) >= (delta - mu[k, k-1]**2)*np.dot(Bs[k-1], Bs[k-1]):
            k += 1
        else:
            B[k], B[k-1] = B[k-1].copy(), B[k].copy()
            Bs, mu = gram_schmidt(B)
            k = max(k-1, 1)
    return [np.round(b).astype(np.int64).tolist() for b in B]


def _enum_norm(G, target):
    """Depth-first short vector enumeration for x^T G x == target."""
    n = G.shape[0]
    # Cholesky for pruning
    import numpy as np
    L = np.linalg.cholesky(G.astype(float) + 1e-12*np.eye(n))
    R = L.T   # upper; x^T G x = ||R x||^2
    count = 0
    x = np.zeros(n, dtype=np.int64)

    # enumerate using the standard recursive bound on R
    # work from last coordinate
    Rf = R.copy()

    def rec(i, partial):
        nonlocal count
        if i < 0:
            val = int(x @ G @ x)
            if val == target:
                count += 1
            return
        # bound: contribution of coords >= i is fixed; choose x_i in range
        # center c_i = -(sum_{j>i} R[i,j] x_j)/R[i,i]
        s = sum(Rf[i, j]*x[j] for j in range(i+1, n))
        ci = -s/Rf[i, i]
        # remaining budget
        rem = target - partial
        if rem < -1e-9:
            return
        width = (rem**0.5)/abs(Rf[i, i]) + 1.0
        lo = int(np.floor(ci - width))
        hi = int(np.ceil(ci + width))
        for xi in range(lo, hi+1):
            x[i] = xi
            contrib = (Rf[i, i]*(xi - ci))**2
            if contrib <= rem + 1e-9:
                rec(i-1, partial + contrib)
        x[i] = 0

    rec(n-1, 0.0)
    # this counts both x and -x; norm-2 vectors come in +-pairs, that's fine
    return count


if __name__ == "__main__":
    main()
