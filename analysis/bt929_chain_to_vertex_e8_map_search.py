#!/usr/bin/env python3
"""BT929 - map the BT925 chain symplectic form into the BT926 vertex E8 form.

Constructs an explicit F2 isometry M with M^T G_vertex M = B_chain, then lifts
M as a 0/1 integer matrix.  In this run det(M)=1, so the lift is unimodular
inside the vertex E8 lattice.  This links the chain shadow to the vertex E8
modulo 2 and gives an integral E8 basis in the target lattice, but it remains
basis-dependent rather than canonical.
"""
from __future__ import annotations
from itertools import combinations, product
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt929_chain_to_vertex_e8_map_search.json"
VERTEX_SUBSET = [0, 1, 4, 22, 27, 35, 23, 34]

# These are the BT928/BT926 computed matrices. The script also recomputes the
# vertex Gram from W33 to keep the target honest.
B_CHAIN = np.array([[0,1,0,0,1,0,0,1],[1,0,0,0,1,1,1,1],[0,0,0,1,1,0,0,1],[0,0,1,0,1,1,1,1],[1,1,1,1,0,1,0,1],[0,1,0,1,1,0,1,1],[0,1,0,1,0,1,0,0],[1,1,1,1,1,1,0,0]], dtype=np.int64) % 2
S_CHAIN = np.array([[1,0,1,0,1,0,0,0],[0,1,0,1,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1],[0,0,0,0,1,0,1,0],[0,0,0,0,0,1,0,1],[0,0,1,1,1,0,0,1],[0,0,0,1,1,1,1,0]], dtype=np.int64) % 2


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def build_adjacency():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3
    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    return A


def f2_rref(M):
    M = (np.array(M, dtype=np.int64) % 2).copy()
    rows, cols = M.shape
    pr = 0
    pivots = []
    for c in range(cols):
        piv = next((i for i in range(pr, rows) if M[i, c]), None)
        if piv is None:
            continue
        M[[pr, piv]] = M[[piv, pr]]
        for i in range(rows):
            if i != pr and M[i, c]:
                M[i] = (M[i] + M[pr]) % 2
        pivots.append(c)
        pr += 1
    return M[:pr], pivots


def f2_inv(M):
    M = (np.array(M, dtype=np.int64) % 2).copy()
    n = M.shape[0]
    aug = np.concatenate([M, np.eye(n, dtype=np.int64)], axis=1)
    row = 0
    for col in range(n):
        piv = next((i for i in range(row, n) if aug[i, col]), None)
        if piv is None:
            raise ValueError("singular over F2")
        aug[[row, piv]] = aug[[piv, row]]
        for i in range(n):
            if i != row and aug[i, col]:
                aug[i] ^= aug[row]
        row += 1
    return aug[:, n:] % 2


def symplectic_basis_from_gram(G):
    G = np.array(G, dtype=np.int64) % 2
    n = G.shape[0]
    basis = [np.eye(n, dtype=np.int64)[i] for i in range(n)]
    pairs = []
    while basis:
        e = basis.pop(0)
        j = next(i for i, f in enumerate(basis) if int(e @ G @ f) % 2 == 1)
        f = basis.pop(j)
        pairs.append((e.copy(), f.copy()))
        new = []
        for g in basis:
            be = int(g @ G @ e) % 2
            bf = int(g @ G @ f) % 2
            g2 = g.copy()
            if bf: g2 ^= e
            if be: g2 ^= f
            new.append(g2)
        if new:
            R, _ = f2_rref(np.array(new, dtype=np.int64))
            basis = [row.copy() % 2 for row in R]
        else:
            basis = []
    return np.column_stack([v for pair in pairs for v in pair]) % 2


def main():
    A = build_adjacency()
    Gv = 2*np.eye(8, dtype=np.int64) - A[np.ix_(VERTEX_SUBSET, VERTEX_SUBSET)]
    Gv2 = Gv % 2
    S_vertex = symplectic_basis_from_gram(Gv2)
    M = (S_vertex @ f2_inv(S_CHAIN)) % 2
    assert np.array_equal((M.T @ Gv2 @ M) % 2, B_CHAIN)
    Mint = M.astype(np.int64)
    det_M = round(np.linalg.det(Mint.astype(float)))
    G_lift = Mint.T @ Gv @ Mint
    det_lift = round(np.linalg.det(G_lift.astype(float)))
    eig = np.linalg.eigvalsh(G_lift.astype(float))
    result = {
        "theorem": "BT929 chain-to-vertex E8 map search",
        "vertex_subset": VERTEX_SUBSET,
        "mod2_isometry_matrix_M_chain_to_vertex": Mint.tolist(),
        "check_Mt_Gvertex_M_equals_Bchain_mod2": True,
        "integer_lift_det_M": int(det_M),
        "lifted_gram": G_lift.astype(int).tolist(),
        "lifted_gram_det": int(det_lift),
        "lifted_gram_positive_definite": bool(eig.min() > 1e-9),
        "lifted_gram_min_eigenvalue": float(eig.min()),
        "lifted_gram_even_diagonal": bool(all(int(x) % 2 == 0 for x in np.diag(G_lift))),
        "status": "explicit mod-2 chain-to-vertex isometry with unimodular 0/1 integral lift; basis-dependent, not canonical",
        "checks": {
            "T1_mod2_isometry_found": True,
            "T2_integral_lift_unimodular_det_1": bool(abs(det_M) == 1),
            "T3_lifted_gram_even_unimodular": bool(det_lift == 1 and all(int(x) % 2 == 0 for x in np.diag(G_lift))),
            "T4_lifted_gram_positive_definite": bool(eig.min() > 1e-9),
            "T5_canonicality_not_claimed": True,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT929 wrote", OUT)


if __name__ == "__main__":
    main()
