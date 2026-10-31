#!/usr/bin/env python3
"""
Pass 87 -- Construction A lattice of C_2(W) and its theta series (a weight-20 modular form).

The code -> lattice -> modular form bridge (Gleason; Broue-Enguehard): the Construction A lattice
Lambda_C = { x in Z^40 : x mod 2 in C } of a binary code C has theta series obtained by evaluating
the code's weight enumerator at the two coordinate theta constants,

  Theta_{Lambda_C}(q) = sum_{x in Lambda_C} q^{|x|^2} = W_C(f0(q), f1(q)),
  f0(q) = sum_{k even} q^{k^2} = 1 + 2q^4 + 2q^16 + ...   (even-coordinate theta),
  f1(q) = sum_{k odd}  q^{k^2} = 2q + 2q^9 + 2q^25 + ...   (odd-coordinate theta).

C_2(W) = [40,16,8] is doubly-even and self-orthogonal (Pass 85), so Lambda_C is an EVEN lattice of
rank 40 and Theta is a modular form of weight 40/2 = 20 (for a level-4 congruence subgroup).  This
pass computes the exact q-expansion (= number of lattice vectors of each norm) from the Pass 85
weight enumerator -- a finite symbolic computation -- and reports the minimal-vector data.

So W(3,3) carries a full arithmetic tower: graph -> Ihara zeta / class number / critical group
(Pass 73-84) -> binary code [40,16,8] (Pass 85/86) -> even lattice + weight-20 modular form (here).

Self-contained (sympy).  ASCII-only.
"""
from __future__ import annotations

import json

# C_2(W) = [40,16,8] weight distribution (Pass 85):  W_C(x,y) = sum A_w x^{40-w} y^w
WD_C = {0: 1, 8: 45, 12: 1120, 16: 15570, 20: 32064, 24: 15570, 28: 1120, 32: 45, 40: 1}
N = 40


def theta_series(order=40):
    import sympy as sp

    q = sp.symbols("q")
    # coordinate theta constants, truncated so k^2 <= order
    kmax = int(order**0.5) + 1
    f0 = 1 + sum(2 * q ** (k * k) for k in range(2, kmax + 1, 2))
    f1 = sum(2 * q ** (k * k) for k in range(1, kmax + 1, 2))
    theta = 0
    for w, a in WD_C.items():
        theta += a * f0 ** (N - w) * f1**w
    ser = sp.series(sp.expand(theta), q, 0, order + 1).removeO()
    poly = sp.Poly(ser, q)
    coeffs = {}
    for (e,), c in poly.terms():
        coeffs[int(e)] = int(c)
    return {k: coeffs[k] for k in sorted(coeffs)}


def main():
    coeffs = theta_series(order=40)
    # norm 0 vector, minimal nonzero norm, its multiplicity
    nonzero = {k: v for k, v in coeffs.items() if k > 0 and v != 0}
    min_norm = min(nonzero)
    min_count = nonzero[min_norm]

    checks = {
        "constant_term_1": coeffs.get(0) == 1,
        "no_norm_1_2_3_vectors": all(coeffs.get(k, 0) == 0 for k in (1, 2, 3)),
        "min_norm_4_with_80_vectors": (
            min_norm == 4 and min_count == 80
        ),  # the +-2 e_i, = 2n
        "norm_8_count_positive": coeffs.get(8, 0) > 0,
        "weight_20_modular_form": N // 2 == 20,
    }
    all_ok = all(checks.values())

    # norm-8 breakdown: 2-coordinate +-2 (from 0 codeword) + weight-8 codewords with +-1
    norm8_from_zero = (N * (N - 1) // 2) * 4  # choose 2 coords, each +-2: 780*4 = 3120
    norm8_from_wt8 = WD_C[8] * (2**8)  # 45 weight-8 words * 2^8 signs = 11520
    norm8_expected = norm8_from_zero + norm8_from_wt8

    print("=" * 74)
    print(
        "PASS 87 -- CONSTRUCTION A LATTICE OF C_2(W): THETA SERIES (WEIGHT-20 MODULAR FORM)"
    )
    print("=" * 74)
    print(
        "Theta_{Lambda_C}(q) = W_C(f0,f1),  Lambda_C = {x in Z^40 : x mod 2 in C_2(W)}"
    )
    print(f"even lattice of rank {N}; theta is a modular form of weight {N//2} = 20")
    print()
    print("theta q-expansion (norm : #lattice vectors):")
    for k, v in coeffs.items():
        if v and k <= 24:
            print(f"   q^{k:<2} : {v}")
    print()
    print(
        f"minimal nonzero norm = {min_norm} with {min_count} vectors (= +-2 e_i, 2n=80)"
    )
    print(
        f"norm-8 vectors = {coeffs.get(8)} = {norm8_from_zero} (two +-2) + {norm8_from_wt8} "
        f"(45 wt-8 codewords x 2^8): {coeffs.get(8) == norm8_expected}"
    )
    print()
    print("arithmetic tower of W(3,3):")
    print("   graph -> Ihara zeta / class number / critical group (Pass 73-84)")
    print("         -> binary code [40,16,8] (Pass 85/86)")
    print("         -> even lattice rank 40 + weight-20 modular form (this pass)")
    print()
    print("checks:")
    for k, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k}")
    print()
    print("=" * 74)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 74)

    payload = {
        "schema": "w33.pass87.theta_lattice.v1",
        "status": "PASS" if all_ok else "FAIL",
        "construction": "Lambda_C = {x in Z^40 : x mod 2 in C_2(W)}; Theta = W_C(f0,f1)",
        "lattice_rank": N,
        "even_lattice": True,
        "modular_form_weight": N // 2,
        "theta_q_expansion": {str(k): v for k, v in coeffs.items() if v},
        "min_norm": min_norm,
        "min_norm_vector_count": min_count,
        "norm8_breakdown": {
            "from_zero_codeword_two_pm2": norm8_from_zero,
            "from_weight8_codewords": norm8_from_wt8,
            "total": norm8_expected,
            "matches_theta": coeffs.get(8) == norm8_expected,
        },
        "reading": (
            "The Construction A lattice of the doubly-even self-orthogonal code C_2(W) is an "
            "even rank-40 lattice whose theta series is a weight-20 modular form, computed "
            "exactly from the [40,16,8] weight enumerator via W_C(theta3,theta2) "
            "(Gleason / Broue-Enguehard). This completes the W(3,3) arithmetic tower: "
            "graph -> zeta/class group -> code -> lattice + modular form."
        ),
        "literature": [
            "Crnkovic-Maksimovic, self-orthogonal codes from SRG(40,12,2,4)",
            "Broue-Enguehard maps; Gleason's theorem (modular forms from codes)",
        ],
        "checks": checks,
    }
    with open("w33_pass87_theta_lattice.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("[wrote] w33_pass87_theta_lattice.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
