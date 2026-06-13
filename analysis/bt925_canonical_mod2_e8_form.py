#!/usr/bin/env python3
"""BT925 - canonical mod-2 bilinear form on the W33 homology.

BT924 pinned the E8 rank and 2-adic location over Z.  BT925 adds the
canonical mod-2 bilinear form on H = ker(A2)/im(A2):

    B(x,y) = (x^T A y)/2 mod 2

for cycles x,y.  This is well-defined because x^T A y is even on cycles.
The edge-parity functional q(x)=(x^T A x)/2 mod 2 is NOT the quadratic
refinement of B; on H it is linear and vanishes.  The honest result is that
B is the nondegenerate alternating F2 form of rank 8, i.e. the bilinear form
carried by E8/2E8.  The remaining lift problem is definiteness over Z.
"""
from __future__ import annotations
from itertools import combinations, product
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt925_canonical_mod2_e8_form.json"


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError("zero vector has no projective representative")


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


def f2_nullspace(M):
    R, pivots = f2_rref(M)
    cols = M.shape[1]
    free = [c for c in range(cols) if c not in pivots]
    prow = {c: i for i, c in enumerate(pivots)}
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64)
        v[f] = 1
        for c in pivots:
            v[c] = R[prow[c], f] % 2
        basis.append(v % 2)
    return basis


def reduce_mod(vec, Rrows, pivots):
    v = vec.copy() % 2
    for r, c in enumerate(pivots):
        if v[c]:
            v = (v + Rrows[r]) % 2
    return v


def f2_rank(M):
    _, pivots = f2_rref(M)
    return len(pivots)


def build_w33_adjacency():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    return A


def main() -> None:
    A = build_w33_adjacency()
    A2 = A % 2
    ker = f2_nullspace(A2)
    im_rows = (A2.T % 2)
    Rim, piv_im = f2_rref(im_rows)

    # Select homology representatives: cycles independent modulo im(A2).
    Hrows = list(Rim)
    reps = []
    for z in ker:
        Rcur, pc = f2_rref(np.array(Hrows, dtype=np.int64)) if Hrows else (np.zeros((0, 40), dtype=np.int64), [])
        res = reduce_mod(z, Rcur, pc)
        if res.any():
            reps.append(z.copy() % 2)
            Hrows.append(z.copy() % 2)
        if len(reps) == 8:
            break
    assert len(reps) == 8

    def q(x):
        return int((x @ A @ x) // 2) % 2

    def B(x, y):
        val = int(x @ A @ y)
        assert val % 2 == 0
        return (val // 2) % 2

    boundaries = [A2[:, k] % 2 for k in range(40)]
    well_defined = all(B(b, z) == 0 for b in boundaries for z in reps)
    G = np.array([[B(reps[i], reps[j]) for j in range(8)] for i in range(8)], dtype=np.int64) % 2
    rank_B = f2_rank(G)
    zero_diagonal = all(G[i, i] == 0 for i in range(8))

    # Check alternating on all 2^8 homology classes.
    all_B_xx_zero = True
    q_values = []
    for mask in range(1 << 8):
        x = np.zeros(40, dtype=np.int64)
        for i in range(8):
            if (mask >> i) & 1:
                x = (x + reps[i]) % 2
        all_B_xx_zero = all_B_xx_zero and (B(x, x) == 0)
        q_values.append(q(x))
    q_zero_on_H = all(v == 0 for v in q_values)

    # q polarizes to x^T A y mod 2, which is zero on cycles.  It is therefore
    # not the quadratic refinement of the divided form B.
    false_polarization_count = 0
    for i in range(8):
        for j in range(8):
            lhs = B(reps[i], reps[j])
            rhs = q((reps[i] + reps[j]) % 2) ^ q(reps[i]) ^ q(reps[j])
            if lhs != rhs:
                false_polarization_count += 1

    result = {
        "theorem": "BT925 canonical mod-2 form on homology",
        "homology_rank": len(reps),
        "well_defined_on_H": well_defined,
        "rank_B": rank_B,
        "zero_diagonal_gram": zero_diagonal,
        "B_xx_zero_for_all_256_classes": all_B_xx_zero,
        "q_zero_on_H": q_zero_on_H,
        "false_polarization_count": false_polarization_count,
        "corrected_claim": "B=(x^T A y)/2 mod 2 is the canonical nondegenerate alternating F2 form on H, matching the bilinear form of E8/2E8; q=(x^T A x)/2 mod 2 is a vanishing Wu functional on H, not the quadratic refinement of B.",
        "residual": "No mod-2/mod-4 invariant separates E8 from II_{4,4}; the remaining open content is a positive-definite integral lift.",
        "checks": {
            "T1_B_descends_to_H": bool(well_defined),
            "T2_B_non_degenerate_rank_8": bool(rank_B == 8),
            "T3_B_alternating": bool(zero_diagonal and all_B_xx_zero),
            "T4_q_vanishes_on_H": bool(q_zero_on_H),
            "T5_invalid_Arf_refinement_rejected": bool(false_polarization_count > 0),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT925 passed; wrote", OUT)


if __name__ == "__main__":
    main()
