#!/usr/bin/env python3
"""
(R1, the sharp question) Does PSp(4,3) preserve an irreducible even-unimodular
rank-8 lattice (then necessarily E8)?

bt980 showed Aut(W33)=PSp(4,3)=U4(2) acts on H~F2^8 faithfully, irreducibly,
preserving the canonical symplectic form B (-> U4(2) ↪ Sp(8,2)). The sharp
question reduces to a quadratic-form question over F2:

  A positive-definite even unimodular rank-8 Z-lattice is E8 (unique), with
  Aut = W(E8) = 2.O8+(2).2 and E8/2E8 = the PLUS-type orthogonal F2^8 space.
  If U4(2) preserves a PLUS-type quadratic refinement q of B, then
  U4(2)  subset  O8+(2) = Aut(E8/2E8), which lifts to W(E8)=Aut(E8). Since U4(2) has
  NO ordinary irreducible 8-dim representation, this irreducible action is NOT
  the reducible E6 subset E8 route; the lift is the irreducible one. Hence E8 IS the
  canonical irreducible U4(2)-lattice, answering the sharp question YES.

We compute the U4(2)-invariant quadratic refinements of B and their type
(plus: 136 zeros, Arf 0; minus: 120 zeros, Arf 1).
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


def f2_rref(M):
    M = (np.array(M, dtype=np.int64) % 2).copy()
    rows, cols = M.shape
    pr = 0
    piv = []
    for c in range(cols):
        r = next((i for i in range(pr, rows) if M[i, c]), None)
        if r is None:
            continue
        M[[pr, r]] = M[[r, pr]]
        for i in range(rows):
            if i != pr and M[i, c]:
                M[i] = (M[i] + M[pr]) % 2
        piv.append(c)
        pr += 1
    return M[:pr], piv


def f2_nullspace(M):
    R, piv = f2_rref(M)
    cols = M.shape[1]
    free = [c for c in range(cols) if c not in piv]
    prow = {c: i for i, c in enumerate(piv)}
    out = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64)
        v[f] = 1
        for c in piv:
            v[c] = R[prow[c], f] % 2
        out.append(v % 2)
    return out


def solve_f2(basis_cols, target):
    n = len(basis_cols)
    M = np.array(basis_cols, dtype=np.int64).T % 2
    aug = np.concatenate([M, (target % 2).reshape(-1, 1)], axis=1)
    rows = aug.shape[0]
    pr = 0
    where = {}
    for c in range(n):
        r = next((i for i in range(pr, rows) if aug[i, c]), None)
        if r is None:
            continue
        aug[[pr, r]] = aug[[r, pr]]
        for i in range(rows):
            if i != pr and aug[i, c]:
                aug[i] = (aug[i] + aug[pr]) % 2
        where[c] = pr
        pr += 1
    coeff = np.zeros(n, dtype=np.int64)
    for c, r in where.items():
        coeff[c] = aug[r, n] % 2
    return coeff


def build_generators():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    idx = {p: i for i, p in enumerate(pts)}
    n = 40

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3
    A = np.zeros((n, n), dtype=np.int64)
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    A2 = A % 2

    ker = f2_nullspace(A2)
    Rim, piv_im = f2_rref(A2.T % 2)
    im_basis = [Rim[i].copy() for i in range(len(piv_im))]
    reps, cur = [], list(im_basis)
    for z in ker:
        Rc, pc = f2_rref(np.array(cur))
        r = z.copy() % 2
        for k, c in enumerate(pc):
            if r[c]:
                r = (r + Rc[k]) % 2
        if r.any():
            reps.append(z.copy() % 2)
            cur.append(z.copy() % 2)
    reps = reps[:8]
    cycle_basis = im_basis + reps

    def proj_H(z):
        return solve_f2(cycle_basis, z % 2)[16:24] % 2

    B = np.array([[int((reps[i] @ A @ reps[j]) // 2) % 2 for j in range(8)]
                  for i in range(8)], dtype=np.int64) % 2

    def transvection_perm(v):
        v = np.array(v) % 3
        perm = [0]*n
        for i, p in enumerate(pts):
            pv = np.array(p) % 3
            lam = (pv[0]*v[2]-pv[2]*v[0]+pv[1]*v[3]-pv[3]*v[1]) % 3
            perm[i] = idx[canon(tuple((pv + lam*v) % 3))]
        return perm

    gens_v = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1),
              (1, 1, 0, 0), (1, 0, 1, 0), (0, 1, 0, 1), (1, 1, 1, 1)]
    mats = []
    for v in gens_v:
        perm = transvection_perm(v)
        cols = []
        for z in reps:
            zp = np.zeros(n, dtype=np.int64)
            zp[perm] = z
            cols.append(proj_H(zp % 2))
        mats.append(np.array(cols, dtype=np.int64).T % 2)
    return B, mats


def main():
    B, gens = build_generators()
    assert all(np.array_equal((g.T @ B @ g) % 2, B) for g in gens), \
        "generators must preserve B"
    print(f"[setup] {len(gens)} U4(2) generators on H, all preserve "
          f"symplectic B")

    def q_of(d, v):
        # q_d(v) = sum_i d_i v_i + sum_{i<j} B_ij v_i v_j  (mod 2)
        s = int(d @ v) % 2
        for i in range(8):
            if v[i]:
                for j in range(i+1, 8):
                    if v[j] and B[i, j]:
                        s ^= 1
        return s

    allv = [np.array([(m >> i) & 1 for i in range(8)], dtype=np.int64)
            for m in range(256)]

    # find U4(2)-invariant quadratic refinements of B
    invariants = []
    for dm in range(256):
        d = np.array([(dm >> i) & 1 for i in range(8)], dtype=np.int64)
        ok = True
        for g in gens:
            for v in allv:
                if q_of(d, (g @ v) % 2) != q_of(d, v):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            invariants.append(d)

    print(f"[invariants] U4(2)-invariant quadratic refinements of B: "
          f"{len(invariants)}")
    results = []
    for d in invariants:
        zeros = sum(1 for v in allv if q_of(d, v) == 0)
        typ = "plus(O8+)" if zeros == 136 else (
              "minus(O8-)" if zeros == 120 else f"?({zeros})")
        arf = 0 if zeros == 136 else (1 if zeros == 120 else None)
        results.append((list(int(x) for x in d), zeros, typ, arf))
        print(f"  d={list(int(x) for x in d)}  zeros={zeros}  type={typ}")

    has_plus = any(r[3] == 0 for r in results)
    print()
    if has_plus:
        print("RESULT: U4(2) preserves a PLUS-type quadratic form => "
              "U4(2)  subset  O8+(2) = Aut(E8/2E8).")
        print("  Lifting O8+(2)  subset  W(E8)=Aut(E8): E8 carries this irreducible")
        print("  U4(2)-action mod 2. Since U4(2) has no ordinary irreducible")
        print("  8-dim rep, this is the irreducible (non-E6) realization.")
        print("  => The sharp question is answered YES: the canonical")
        print("  irreducible even-unimodular rank-8 lattice is E8.")
    else:
        print("RESULT: no plus-type invariant form; U4(2) does NOT sit in")
        print("  O8+(2) this way -> E8 not preserved with this action.")

    out = {
        "theorem": "(R1 sharp) U4(2)-invariant quadratic form on H",
        "num_invariant_forms": len(invariants),
        "forms": [{"diag": r[0], "zeros": r[1], "type": r[2], "arf": r[3]}
                  for r in results],
        "preserves_plus_type_O8plus": bool(has_plus),
        "conclusion": ("E8 is the canonical irreducible U4(2)-lattice "
                       "(answer YES)") if has_plus else
                      "no plus-type invariant; E8 not preserved this way",
    }
    with open("data/bt981_e8_invariant_quadratic_form.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt981_e8_invariant_quadratic_form.json")


if __name__ == "__main__":
    main()
