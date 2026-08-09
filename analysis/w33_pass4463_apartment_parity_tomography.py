#!/usr/bin/env python3
"""Pass 4463 -- apartment-parity tomography for W(3,3) line signings.

Let H be the 40 x 1620 binary line/apartment incidence matrix from Pass 4461.
Encode a line signing sigma_l in {+1,-1} by b_l in F_2 with
sigma_l=(-1)^b_l.  The 1620 apartment parities are then

    y = H^T b  (mod 2).

This verifier proves

    rank_F2(H) = 39,
    ker_F2(H^T) = <1_40>.

Therefore the complete apartment-parity vector determines all 40 line signs
up to the unavoidable global reversal b -> b + 1, equivalently sigma -> -sigma.
Since every apartment contains four lines, that reversal is necessarily
invisible, and the theorem says it is the ONLY invisible line-signing degree of
freedom.

Additional exact structure:

  * the apartment-parity image is a binary [1620,39] linear code;
  * every one-line generator has Hamming weight 162;
  * the XOR of two line generators has weight 270 when the two lines meet and
    weight 312 when they are disjoint;
  * over F_2, H H^T = A_dual, because the integer identity from Pass 4461

        H H^T = 156 I + 21 A_dual + 6 J

    reduces to A_dual modulo two.

Boundary: this is a finite-geometric identifiability theorem.  It does not say
that apartment parity is a physically complete observable in an optical setup;
it says that within the 40-bit line-signing model no nontrivial signing gauge
other than global reversal survives all 1620 apartment products.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles

ROOT = Path(__file__).resolve().parents[1]


def rank_mod2(M: np.ndarray) -> int:
    A = (np.asarray(M, dtype=np.uint8) & 1).copy()
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i, c]), None)
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        r += 1
        if r == m:
            break
    return r


def main() -> int:
    _, lines, A, _, edge_line = geometry()
    cycles = simple_four_cycles(A)
    supports = [frozenset(edge_line[e] for e in C) for C in cycles]
    assert len(supports) == 1620

    H = np.zeros((40, 1620), dtype=np.uint8)
    for j, support in enumerate(supports):
        for li in support:
            H[li, j] = 1

    Adual = np.zeros((40, 40), dtype=np.uint8)
    for i in range(40):
        for j in range(i + 1, 40):
            if lines[i] & lines[j]:
                Adual[i, j] = Adual[j, i] = 1

    rank_h = rank_mod2(H)
    assert rank_h == 39
    assert np.all((H.T @ np.ones(40, dtype=np.uint8)) % 2 == 0)
    assert 40 - rank_h == 1

    gram2 = (H @ H.T) % 2
    assert np.array_equal(gram2, Adual)

    row_weights = [int(row.sum()) for row in H]
    assert set(row_weights) == {162}

    adjacent_pair_weights = set()
    disjoint_pair_weights = set()
    for i in range(40):
        for j in range(i + 1, 40):
            w = int(np.count_nonzero(H[i] ^ H[j]))
            (adjacent_pair_weights if Adual[i, j] else disjoint_pair_weights).add(w)
    assert adjacent_pair_weights == {270}
    assert disjoint_pair_weights == {312}

    result = {
        "pass": 4463,
        "theorem": "W33 apartment-parity tomography theorem",
        "line_bits": 40,
        "apartment_parity_bits": 1620,
        "rank_F2_H": 39,
        "kernel_dimension_Ht": 1,
        "kernel_generator": "all-ones 40-vector (global sign reversal)",
        "image_code": "binary [1620,39] apartment-parity code",
        "generator_weight": 162,
        "two_generator_weights": {
            "intersecting_lines": 270,
            "disjoint_lines": 312
        },
        "mod2_gram_identity": "H H^T = A_dual over F_2",
        "boundary": (
            "Finite-geometric identifiability only.  The theorem concerns the 40-bit line-signing model; "
            "it does not assert physical measurement completeness."
        )
    }

    out = ROOT / "data" / "PART_W33_PASS4463_APARTMENT_PARITY_TOMOGRAPHY.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4463 -- apartment-parity tomography")
    print("  rank_F2(H) = 39")
    print("  ker(H^T) = <1_40>")
    print("  image code = [1620,39]")
    print("  one-line syndrome weight = 162")
    print("  two-line weights: 270 intersecting, 312 disjoint")
    print("  H H^T = A_dual (mod 2)")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
