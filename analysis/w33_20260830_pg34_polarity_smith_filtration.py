#!/usr/bin/env python3
"""Resolve the full integral Smith normal form of the 85x85 PG(3,4) polarity matrix.

The preceding polarity theorem gives H^2=16I+5J and det(H)=-21*4^84, while
the modular audit identified the exceptional primes 2,3,7.  Here we perform
local Smith elimination modulo prime powers.  The exact p-adic valuation
multiplicities are

  p=2: v=0^17, 1^8, 2^36, 3^8, 4^16;
  p=3: v=0^84, 1^1;
  p=7: v=0^84, 1^1.

The invariant-factor divisibility chain then forces

  SNF(H) = diag(1^17, 2^8, 4^36, 8^8, 16^15, 336).

Thus the 3- and 7-primary defects live only in the terminal invariant factor,
whereas characteristic two sees a four-layer 2-adic filtration.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

from w33_20260829_pg34_polarity_sentinel import geometry, trade_incidence, mm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260830_PG34_POLARITY_SMITH_FILTRATION.json"


def padic_local_counts(A, p, max_valuation):
    """Return counts of invariant factors with exact valuations 0..max_valuation.

    Work over Z/p^(max_valuation+1).  Unit row/column operations diagonalize
    all valuation-zero factors; the residual block is divisible by p, so divide
    it by p and iterate.  Unit scaling is valid over the local PID and does not
    change p-primary Smith data.
    """
    modulus = p ** (max_valuation + 1)
    M = [[x % modulus for x in row] for row in A]
    counts = []
    for _level in range(max_valuation + 1):
        rows = len(M); cols = len(M[0]) if rows else 0
        r = c = pivots = 0
        while r < rows and c < cols:
            found = None
            for i in range(r, rows):
                for j in range(c, cols):
                    if M[i][j] % p != 0:
                        found = (i, j); break
                if found is not None:
                    break
            if found is None:
                break
            i, j = found
            M[r], M[i] = M[i], M[r]
            for row in M:
                row[c], row[j] = row[j], row[c]
            u = M[r][c] % modulus
            inv = pow(u, -1, modulus)
            M[r] = [(x * inv) % modulus for x in M[r]]
            # Clear the pivot column by row operations.
            for i2 in range(rows):
                if i2 == r:
                    continue
                a = M[i2][c] % modulus
                if a:
                    M[i2] = [(M[i2][j2] - a * M[r][j2]) % modulus for j2 in range(cols)]
            # Clear the pivot row by column operations.
            for j2 in range(cols):
                if j2 == c:
                    continue
                a = M[r][j2] % modulus
                if a:
                    for i2 in range(rows):
                        M[i2][j2] = (M[i2][j2] - a * M[i2][c]) % modulus
            r += 1; c += 1; pivots += 1
        counts.append(pivots)
        M = [row[c:] for row in M[r:]]
        if not M:
            break
        assert all(x % p == 0 for row in M for x in row)
        modulus //= p
        assert modulus > 1
        M = [[(x // p) % modulus for x in row] for row in M]
    return counts


def main():
    N, A = geometry()
    B, G = trade_incidence(N)
    H = []
    for i in range(40):
        H.append(A[i] + B[i])
    for j in range(45):
        H.append([B[i][j] for i in range(40)] + [G[j][k] + (1 if j == k else 0) for k in range(45)])
    assert len(H) == 85 and all(len(r) == 85 for r in H)

    H2 = mm(H, H)
    assert all(H2[i][j] == (21 if i == j else 5) for i in range(85) for j in range(85))
    det_abs = 21 * 4 ** 84

    c2 = padic_local_counts(H, 2, 4)
    c3 = padic_local_counts(H, 3, 1)
    c7 = padic_local_counts(H, 7, 1)
    assert c2 == [17, 8, 36, 8, 16]
    assert c3 == [84, 1]
    assert c7 == [84, 1]
    assert sum(c2) == sum(c3) == sum(c7) == 85
    assert sum(v * n for v, n in enumerate(c2)) == 168
    assert sum(v * n for v, n in enumerate(c3)) == 1
    assert sum(v * n for v, n in enumerate(c7)) == 1

    v2 = [0] * 17 + [1] * 8 + [2] * 36 + [3] * 8 + [4] * 16
    v3 = [0] * 84 + [1]
    v7 = [0] * 84 + [1]
    snf = [2 ** a * 3 ** b * 7 ** c for a, b, c in zip(v2, v3, v7)]
    assert all(snf[i + 1] % snf[i] == 0 for i in range(84))
    assert math.prod(snf) == det_abs
    snf_counts = Counter(snf)
    assert snf_counts == Counter({1:17, 2:8, 4:36, 8:8, 16:15, 336:1})

    ge_layers = [sum(v >= k for v in v2) for k in range(1, 5)]
    assert ge_layers == [68, 60, 24, 16]

    out = {
        "schema": "w33.20260830.pg34-polarity-smith-filtration.v1",
        "status": "PASS",
        "matrix": {"size":85,"identity":"H^2 = 16 I + 5 J","determinant":"-21 * 4^84","exceptionalPrimes":[2,3,7]},
        "localSmith": {
            "2": {"exactValuationMultiplicities":{"0":17,"1":8,"2":36,"3":8,"4":16},"atLeastValuationDimensions":{"1":68,"2":60,"3":24,"4":16},"rankMod2":17},
            "3": {"exactValuationMultiplicities":{"0":84,"1":1},"rankMod3":84},
            "7": {"exactValuationMultiplicities":{"0":84,"1":1},"rankMod7":84},
        },
        "smithNormalForm": {
            "invariantFactors": "1^17, 2^8, 4^36, 8^8, 16^15, 336",
            "multiplicities":{"1":17,"2":8,"4":36,"8":8,"16":15,"336":1},
            "cokernel":"(Z/2)^8 + (Z/4)^36 + (Z/8)^8 + (Z/16)^15 + Z/336",
            "exponent":336,
        },
        "structuralReading": {
            "characteristic2":"the 68-dimensional mod-2 kernel is the first layer of a four-step 2-adic defect with valuation strata 8,36,8,16 above the 17 unit factors",
            "characteristic3and7":"each prime occurs only once, in the terminal invariant factor 336; both modular corank-one defects are the same global Smith direction",
            "inverseDenominator":"the cokernel exponent 336 matches the exact inverse formula H^{-1}=H/16-5J/336 and proves 336 is the minimal global denominator",
        },
        "theorem":"The full integral Smith form is diag(1^17,2^8,4^36,8^8,16^15,336). Characteristic two is a deep four-layer degeneration, while the 3- and 7-primary defects cohabit only the final global invariant factor.",
        "boundary":"This is an integral finite-design operator theorem. Any interpretation of the p-adic layers as physical scales or couplings requires an independent dynamical map.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":"PASS","SNF":"1^17 2^8 4^36 8^8 16^15 336","v2":[17,8,36,8,16],"v3":[84,1],"v7":[84,1]}, sort_keys=True))


if __name__ == "__main__":
    main()
