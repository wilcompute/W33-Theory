#!/usr/bin/env python3
"""Compute the exact Smith invariant factors of the 85x85 PG(3,4) polarity design.

The preceding polarity audit proves H^2=16I+5J and det(H)=-21*4^84.
This audit performs p-adic Smith elimination at the only singular primes
2, 3, and 7, then combines the primary invariant factors into the full
integral Smith normal form.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

from w33_20260829_pg34_polarity_sentinel import geometry, trade_incidence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260830_PG34_POLARITY_SMITH.json"


def build_H():
    N, A = geometry()
    B, G = trade_incidence(N)
    H = [A[i] + B[i] for i in range(40)]
    for j in range(45):
        H.append(
            [B[i][j] for i in range(40)]
            + [G[j][k] + (1 if j == k else 0) for k in range(45)]
        )
    assert len(H) == 85 and all(len(r) == 85 for r in H)
    return H


def padic_snf_exponents(A, p, K):
    """Return p-adic Smith exponents, truncated at K, over Z/p^K Z.

    At each step choose an entry of least p-valuation.  In the finite chain
    ring Z/p^K Z it generates the smallest principal ideal present in the
    remaining block, so its unit part can clear the pivot row and column.
    """
    modulus = p ** K
    M = [[x % modulus for x in row] for row in A]
    n = len(M)

    def vp(x):
        x %= modulus
        if x == 0:
            return K
        e = 0
        while x % p == 0:
            x //= p
            e += 1
        return e

    exponents = []
    for k in range(n):
        best = K
        pos = None
        for i in range(k, n):
            for j in range(k, n):
                e = vp(M[i][j])
                if e < best:
                    best = e
                    pos = (i, j)
                    if e == 0:
                        break
            if best == 0:
                break
        if pos is None or best == K:
            exponents.extend([K] * (n - k))
            break

        i0, j0 = pos
        M[k], M[i0] = M[i0], M[k]
        for row in M:
            row[k], row[j0] = row[j0], row[k]

        pe = p ** best
        qmod = p ** (K - best)
        unit = (M[k][k] // pe) % qmod
        invunit = pow(unit, -1, qmod)

        for i in range(k + 1, n):
            b = M[i][k]
            assert b % pe == 0
            q = ((b // pe) * invunit) % qmod
            if q:
                M[i] = [(M[i][j] - q * M[k][j]) % modulus for j in range(n)]
            assert M[i][k] == 0

        for j in range(k + 1, n):
            b = M[k][j]
            assert b % pe == 0
            q = ((b // pe) * invunit) % qmod
            if q:
                for i in range(n):
                    M[i][j] = (M[i][j] - q * M[i][k]) % modulus
            assert M[k][j] == 0

        exponents.append(best)

    assert len(exponents) == n
    return sorted(exponents)


def main():
    H = build_H()

    e2 = padic_snf_exponents(H, 2, 5)
    e3 = padic_snf_exponents(H, 3, 2)
    e7 = padic_snf_exponents(H, 7, 2)

    c2 = Counter(e2)
    c3 = Counter(e3)
    c7 = Counter(e7)
    assert c2 == Counter({0:17, 1:8, 2:36, 3:8, 4:16})
    assert c3 == Counter({0:84, 1:1})
    assert c7 == Counter({0:84, 1:1})

    # Primary exponent sequences are already nondecreasing.  Combining their
    # coordinates yields the invariant factors d_1 | ... | d_85.
    invariants = [2**e2[i] * 3**e3[i] * 7**e7[i] for i in range(85)]
    assert all(invariants[i+1] % invariants[i] == 0 for i in range(84))
    expected = [1]*17 + [2]*8 + [4]*36 + [8]*8 + [16]*15 + [336]
    assert invariants == expected
    assert math.prod(invariants) == 21 * (4 ** 84)

    out = {
        "schema": "w33.20260830.pg34-polarity-smith.v1",
        "status": "PASS",
        "matrix": "85x85 symmetric PG(3,4) point-plane polarity design H",
        "identity": "H^2 = 16 I + 5 J",
        "determinantAbsolute": "21 * 4^84",
        "smithNormalForm": [
            {"invariantFactor":1, "multiplicity":17},
            {"invariantFactor":2, "multiplicity":8},
            {"invariantFactor":4, "multiplicity":36},
            {"invariantFactor":8, "multiplicity":8},
            {"invariantFactor":16, "multiplicity":15},
            {"invariantFactor":336, "multiplicity":1}
        ],
        "primaryExponents": {
            "2": {str(k):v for k,v in sorted(c2.items())},
            "3": {str(k):v for k,v in sorted(c3.items())},
            "7": {str(k):v for k,v in sorted(c7.items())}
        },
        "cokernel": "(Z/2)^8 x (Z/4)^36 x (Z/8)^8 x (Z/16)^15 x Z/336",
        "theorem": "SNF(H)=diag(1^17,2^8,4^36,8^8,16^15,336).",
        "reading": "The characteristic-2 rank 17 is the 17 unit invariant factors. The unique mod-3 and mod-7 null directions occupy the final invariant factor 336=16*3*7, while the remaining torsion is purely 2-primary.",
        "boundary": "This is an exact integral matrix invariant. No physical interpretation of its torsion factors is asserted by the certificate."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":"PASS","SNF":"1^17 2^8 4^36 8^8 16^15 336"}))


if __name__ == "__main__":
    main()
