#!/usr/bin/env python3
"""
Pass 94 -- The dual GQ's code-lattice: W(3,3) and Q(4,3) separate AGAIN at the lattice level.

W(3,3) and Q(4,3) are cospectral non-isomorphic SRG(40,12,2,4) (Pass 76/84, the Sunada-Gassmann
pair -- "can you hear the shape?").  Their binary codes already differ: C_2(W)=[40,16,8] (Pass 85)
vs C_2(Q)=[40,10,12] (Pass 88).  This pass pushes the separation into the Construction-A code-lattice
discriminant forms.

For a doubly-even self-orthogonal code C=[40,k] the glue group C^perp/C = (Z/2)^(40-2k) carries a
nondegenerate quadratic form q(v)=wt(v)/2 mod 2 (the discriminant form of the even lattice Lambda_C).
Its type is fixed by the Arf invariant:

    W(3,3): k=16 -> glue (Z/2)^8,  Arf=0 -> O+_8(2)  = the E8/2E8 form (Pass 92, 135 isotropic)
    Q(4,3): k=10 -> glue (Z/2)^20, Arf=0 -> O+_20(2)                    (524799 isotropic)

Both plus-type, but of DIFFERENT RANK (8 vs 20 = 40-2k).  So the two cospectral quadrangles, which
share adjacency spectrum, critical/Smith 5-parts, and much else, are told apart cleanly by their
code-lattice discriminant forms: the E8 form falls out of W (maximal 2-rank code -> minimal glue),
never out of Q.  (Note 8 + 20 = 28, the size of the SRG(40,12,2,4) census of Pass 89.)

Self-contained (GF(2) linear algebra + Arf via symplectic reduction).  ASCII-only.
"""

from __future__ import annotations

import json
from collections import Counter

import numpy as np

from w33_pass73_prime_geodesics import build_graph as build_W
from w33_pass76_cospectral_mates import build_Q43
from w33_pass92_discriminant_e8 import nullspace_basis, rowspace_basis, to_int


def glue_form(A):
    n = A.shape[0]
    C = rowspace_basis([to_int(A[i]) for i in range(n)])
    Cp = nullspace_basis(A)
    allb = list(C)
    glue = []
    for v in Cp:
        r = v
        for b in allb:
            r = min(r, r ^ b)
        if r:
            allb.append(r)
            allb.sort(reverse=True)
            glue.append(v)
    q = [(g.bit_count() // 2) % 2 for g in glue]
    k = len(glue)
    B = [[(glue[i] & glue[j]).bit_count() % 2 for j in range(k)] for i in range(k)]
    return glue, q, B, len(C), len(Cp)


def weight_enum(C_basis):
    words = [0]
    for b in C_basis:
        words = words + [x ^ b for x in words]
    return dict(sorted(Counter(w.bit_count() for w in words).items()))


def _qval(v, q, B):
    bits = [i for i in range(len(q)) if (v >> i) & 1]
    s = 0
    for i in bits:
        s ^= q[i]
    for a in range(len(bits)):
        for c in range(a + 1, len(bits)):
            s ^= B[bits[a]][bits[c]]
    return s


def _Bval(u, v, B):
    s = 0
    k = len(B)
    for i in range(k):
        if (u >> i) & 1:
            for j in range(k):
                if (v >> j) & 1:
                    s ^= B[i][j]
    return s


def arf(q, B):
    """Arf invariant of nondegenerate quadratic form q (polar form B) via symplectic reduction."""
    k = len(q)
    remaining = [1 << i for i in range(k)]
    qv = {v: _qval(v, q, B) for v in remaining}
    a = 0
    while remaining:
        e1 = remaining.pop(0)
        e2 = next((w for w in remaining if _Bval(e1, w, B) == 1), None)
        if e2 is None:
            continue
        remaining.remove(e2)
        a ^= qv[e1] & qv[e2]
        newrem = []
        for w in remaining:
            w2 = w ^ (_Bval(w, e2, B) * e1) ^ (_Bval(w, e1, B) * e2)
            qv[w2] = _qval(w2, q, B)
            newrem.append(w2)
        remaining = newrem
    return a


def analyze(name, A):
    A = np.array(A)
    C = rowspace_basis([to_int(A[i]) for i in range(A.shape[0])])
    we = weight_enum(C)
    glue, q, B, kC, kCp = glue_form(A)
    k = len(glue)
    m = k // 2
    a = arf(q, B)
    typ = "plus" if a == 0 else "minus"
    iso_incl0 = 2 ** (k - 1) + (2 ** (m - 1) if a == 0 else -(2 ** (m - 1)))
    doubly_even = all(w % 4 == 0 for w in we)
    return {
        "name": name,
        "code": f"[40,{kC},{min(w for w in we if w > 0)}]",
        "weight_enumerator": {str(w): c for w, c in we.items()},
        "doubly_even": doubly_even,
        "glue_dim": k,
        "glue_dim_formula_n_minus_2k": 40 - 2 * kC,
        "arf": a,
        "disc_form": f"O{'+' if a == 0 else '-'}_{k}(2)",
        "type": typ,
        "nonzero_isotropic": iso_incl0 - 1,
    }


def main():
    W = analyze("W(3,3)", build_W()[1])
    Q = analyze("Q(4,3)", build_Q43()[1])

    checks = {
        "W_code_40_16_8": W["code"] == "[40,16,8]",
        "Q_code_40_10_12": Q["code"] == "[40,10,12]",
        "both_doubly_even": W["doubly_even"] and Q["doubly_even"],
        "W_glue_8_Q_glue_20": W["glue_dim"] == 8 and Q["glue_dim"] == 20,
        "glue_formula_n_minus_2k": (
            W["glue_dim"] == W["glue_dim_formula_n_minus_2k"]
            and Q["glue_dim"] == Q["glue_dim_formula_n_minus_2k"]
        ),
        "W_disc_O+8_E8": W["disc_form"] == "O+_8(2)" and W["nonzero_isotropic"] == 135,
        "Q_disc_O+20": Q["disc_form"] == "O+_20(2)",
        "ranks_differ_8_vs_20": W["glue_dim"] != Q["glue_dim"],
        "glue_sum_28_census": W["glue_dim"] + Q["glue_dim"] == 28,
    }
    all_ok = all(checks.values())

    print("=" * 78)
    print(
        "PASS 94 -- W(3,3) vs Q(4,3): CODE-LATTICE DISCRIMINANT FORMS SEPARATE THE MATES"
    )
    print("=" * 78)
    for D in (W, Q):
        print(
            f"{D['name']}: C_2 = {D['code']}, doubly-even={D['doubly_even']}, "
            f"glue (Z/2)^{D['glue_dim']} (= 40-2k)"
        )
        print(
            f"        discriminant form: {D['disc_form']}  (Arf={D['arf']}, "
            f"{D['nonzero_isotropic']} nonzero isotropic)"
        )
    print()
    print(
        "SEPARATOR: cospectral mates, same adjacency spectrum -- but W -> O+_8(2) (the E8/2E8 form,"
    )
    print(
        "   Pass 92) of rank 8, while Q -> O+_20(2) of rank 20.  The E8 form falls out of W only."
    )
    print(f"   glue ranks 8 + 20 = 28 = the SRG(40,12,2,4) census size (Pass 89).")
    print()
    print("checks:")
    for k_, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k_}")
    print()
    print("=" * 78)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 78)

    payload = {
        "schema": "w33.pass94.dual_lattice.v1",
        "status": "PASS" if all_ok else "FAIL",
        "W": W,
        "Q": Q,
        "reading": (
            "The cospectral non-isomorphic mates W(3,3) and Q(4,3) separate again at the "
            "code-lattice level: both binary codes are doubly-even self-orthogonal, but the "
            "Construction-A discriminant forms are O+_8(2) (= E8/2E8, rank 8) for W and O+_20(2) "
            "(rank 20) for Q.  W's maximal 2-rank code (16) gives the minimal glue (8) and hence "
            "the E8 form; Q's lower 2-rank (10) gives rank-20 glue.  glue rank = n - 2k; 8 + 20 = 28."
        ),
        "checks": checks,
    }
    with open("w33_pass94_dual_lattice.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("[wrote] w33_pass94_dual_lattice.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
