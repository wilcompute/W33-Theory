#!/usr/bin/env python3
"""
Pass 97 -- The 5-adic mirror: why E8 lives at p=2 and nowhere else.

The critical group of W(3,3) is K = (Z/10)^8 (+) Z/40 (+) (Z/160)^14 (Pass 82), of order
|K| = 2^81 * 5^23 -- exactly two primes.  This pass explains the sharp asymmetry between them via
the SRG eigenvalue arithmetic (k,r,s) = (12, 2, -4), with r - s = 6, k - r = 10, k - s = 16.

Ducey's theorem: for a strongly regular graph the p-part of the critical/Smith group is determined
by the parameters UNLESS p | (r - s).  Here r - s = 6, so the only "bad" primes are p = 2 and p = 3.

  p = 2  (bad, 2 | r-s):  2 | k-r and 2 | k-s, and the collinearity code is doubly-even
         self-orthogonal.  The 2-part is rich and non-parameter-determined: 2^81, and the
         Construction-A code-lattice has discriminant form E8/2E8 = O+_8(2) (Pass 92).  <-- E8 lives here.

  p = 3  (bad, 3 | r-s):  but 3 does NOT divide k-r=10 or k-s=16, so the 3-part is TRIVIAL.
         Ducey's condition p|(r-s) is necessary, not sufficient -- a "bad prime with nothing there."

  p = 5  (GOOD, 5 does not divide r-s=6):  the 5-part is parameter-determined and must be elementary.
         5 exactly divides k-r=10 (5^1 || 10) and 5 does not divide k-s=16, so
              5-part of K = (Z/5)^(f-1) = (Z/5)^23,   f = mult(r) = 24,
         living entirely in the r-eigenspace.  Clean, boring, forced.

MECHANISM (the missing 1).  Mod 5 the valency k = 12 collides with r = 2 (12 = 2 mod 5), so A is NOT
diagonalizable mod 5: nullity(A-2I) = 24 but nullity((A-2I)^2) = 25 -- a single size-2 Jordan block
at eigenvalue 2 couples the all-ones vector to the r-eigenspace.  That, together with the spanning-
tree normalization 1/40 (one factor of 5), turns (Z/5)^24 into (Z/5)^{24-1} = (Z/5)^23.

READING.  The exceptional E8 structure of W(3,3) is intrinsically a p=2 phenomenon: it needs both
2 | (r-s) (a bad prime, leaving room for non-parameter-determined structure) and the doubly-even
self-orthogonal binary code.  No odd prime meets this: 3 is bad but empty, 5 is good hence elementary.
There is no "E8 at 5" -- the 5-adic mirror is elementary abelian by theorem, and that asymmetry is
exactly why E8 appears at 2 alone.

Self-contained (build_graph + GF(p) ranks + eigenvalue arithmetic).  ASCII-only.
"""

from __future__ import annotations

import json

import numpy as np

from w33_pass73_prime_geodesics import build_graph


def prank(M, p):
    M = [[int(x) % p for x in row] for row in M]
    N = len(M)
    r = 0
    for c in range(N):
        piv = next((i for i in range(r, N) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(N):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r


def main():
    _, A = build_graph()
    A = np.array(A)
    n = 40
    I = np.eye(n, dtype=int)
    k, r, s = 12, 2, -4
    f, g = 24, 15  # multiplicities of r, s

    # |K| = (1/n) (k-r)^f (k-s)^g
    Kord = (k - r) ** f * (k - s) ** g // n
    # its prime factorization (only 2 and 5 expected)
    two_part = 0
    m = Kord
    while m % 2 == 0:
        m //= 2
        two_part += 1
    five_part = 0
    while m % 5 == 0:
        m //= 5
        five_part += 1
    only_2_and_5 = m == 1

    bad_primes = [p for p in (2, 3, 5, 7) if (r - s) % p == 0]

    # mod-5 Jordan structure
    B = A - 2 * I
    null_B = n - prank(B, 5)
    null_B2 = n - prank(B.dot(B), 5)
    jordan_block = null_B == 24 and null_B2 == 25

    checks = {
        "|K|_is_2^81_5^23": two_part == 81 and five_part == 23 and only_2_and_5,
        "bad_primes_2_and_3": bad_primes == [2, 3],
        "p2_bad_and_2_divides_kr_ks": (r - s) % 2 == 0
        and (k - r) % 2 == 0
        and (k - s) % 2 == 0,
        "p3_bad_but_empty": (r - s) % 3 == 0 and (k - r) % 3 != 0 and (k - s) % 3 != 0,
        "p5_good_5_notdiv_rs": (r - s) % 5 != 0,
        "5_exactly_divides_kr": (k - r) % 5 == 0 and (k - r) % 25 != 0,
        "5_notdiv_ks": (k - s) % 5 != 0,
        "five_part_is_Z5_f_minus_1": five_part == f - 1 == 23,
        "mod5_valency_collides_with_r": (12 % 5) == (2 % 5),
        "mod5_jordan_block_size2": jordan_block,
        "5code_ker_A_2I_is_40_24": null_B == f == 24,
    }
    all_ok = all(checks.values())

    print("=" * 78)
    print("PASS 97 -- THE 5-ADIC MIRROR: WHY E8 LIVES AT p=2 AND NOWHERE ELSE")
    print("=" * 78)
    print(f"SRG(40,12,2,4): (k,r,s)=({k},{r},{s});  r-s={r-s}, k-r={k-r}, k-s={k-s}")
    print(
        f"|K(W)| = 2^{two_part} * 5^{five_part}   (only primes 2 and 5; Ducey bad primes p|r-s: {bad_primes})"
    )
    print()
    print(
        "  p=2 (bad): 2|k-r, 2|k-s, doubly-even self-orthog code -> E8/2E8 = O+_8(2) (Pass 92)."
    )
    print(
        "  p=3 (bad): 3 does not divide k-r=10 or k-s=16 -> 3-part TRIVIAL (necessary != sufficient)."
    )
    print(
        f"  p=5 (GOOD): 5||k-r=10, 5 not| k-s=16 -> 5-part = (Z/5)^(f-1) = (Z/5)^{f-1}, f=mult(r)={f}."
    )
    print()
    print("MECHANISM: mod 5, k=12 = 2 = r, so A is non-diagonalizable:")
    print(
        f"   nullity(A-2I)={null_B}, nullity((A-2I)^2)={null_B2}  -> one size-2 Jordan block."
    )
    print(f"   (Z/5)^{f} - one factor (tree-number /40) = (Z/5)^{f-1}.")
    print()
    print(
        "=> E8 is a p=2 phenomenon: needs 2|(r-s) AND the doubly-even self-orthogonal code."
    )
    print(
        "   No odd prime qualifies; the 5-adic mirror is elementary abelian by theorem."
    )
    print()
    print("checks:")
    for kk, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {kk}")
    print()
    print("=" * 78)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 78)

    payload = {
        "schema": "w33.pass97.five_adic_mirror.v1",
        "status": "PASS" if all_ok else "FAIL",
        "parameters": {
            "k": k,
            "r": r,
            "s": s,
            "r_minus_s": r - s,
            "k_minus_r": k - r,
            "k_minus_s": k - s,
        },
        "critical_group_order": {
            "two_part": two_part,
            "five_part": five_part,
            "only_2_and_5": only_2_and_5,
        },
        "ducey_bad_primes_p_div_rs": bad_primes,
        "p2": "bad prime; 2|k-r,2|k-s; doubly-even self-orthogonal code -> E8/2E8 = O+_8(2)",
        "p3": "bad prime but 3 does not divide k-r or k-s -> 3-part trivial (necessary != sufficient)",
        "p5": "good prime (5 not| r-s); 5||k-r, 5 not|k-s -> (Z/5)^(f-1) = (Z/5)^23 in the r-eigenspace",
        "mod5_jordan": {
            "valency_collides_with_r": True,
            "nullity_A_2I": null_B,
            "nullity_A_2I_squared": null_B2,
            "one_size2_jordan_block": jordan_block,
            "five_code_ker_A_2I": "[40,24]_5",
        },
        "reading": (
            "The critical group of W(3,3) has order 2^81 * 5^23.  The exceptional E8/2E8 = O+_8(2) "
            "structure is intrinsically 2-adic: it requires 2 | (r-s)=6 (a Ducey bad prime, so the "
            "2-part is not parameter-determined) together with the doubly-even self-orthogonal binary "
            "code.  The prime 3 is also bad (3|r-s) but empty (3 does not divide k-r or k-s).  The "
            "prime 5 is good (5 not| r-s), so its part is elementary abelian by theorem: (Z/5)^{f-1} = "
            "(Z/5)^23, f=mult(r)=24, forced clean by 5||(k-r) and a size-2 Jordan block from the "
            "k=r mod 5 collision.  There is no E8 at 5 -- that asymmetry is exactly why E8 sits at 2."
        ),
        "checks": checks,
    }
    with open("w33_pass97_five_adic_mirror.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("[wrote] w33_pass97_five_adic_mirror.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
