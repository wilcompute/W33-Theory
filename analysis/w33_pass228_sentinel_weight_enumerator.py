#!/usr/bin/env python3
"""Pass 228: the exact weight enumerator of the q=3 sentinel, and the
MacWilliams bridge to the context code.

Pass 168 computed the CONTEXT code's theta (1 + 80 t^2 + 14640 t^4, i.e. the
[40,25,4] dual).  The SENTINEL's own complete weight enumerator was never
computed.  This witness enumerates all 2^15 codewords of the q=3 sentinel
[40,15,8] exactly, giving (A_0, ..., A_40), then applies the MacWilliams
identity

    W_C(x,y) = (1/|C^perp|) * W_{C^perp}(x+y, x-y),  C^perp = sentinel,

to RECONSTRUCT the context code [40,25,4] weight enumerator from the sentinel
alone.  The reconstruction is a stringent self-check: every reconstructed
coefficient must be a non-negative integer, they must sum to 2^25, and the
minimum-weight term must be B_4 = 40 -- the 40 isotropic lines, matching
Pass 168.  This is genuinely new (the sentinel enumerator + the exact bridge)
and certifies the whole doubly-even/self-orthogonal picture in one shot.
"""

from __future__ import annotations

from math import comb
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass224_shadow_code_tower import (
    doubly_even_subcode,
    f2_nullspace,
    f2_rowspace_basis,
    incidence_rows,
    isotropic_lines,
    pg3_points,
    popcount,
    rows_to_bitmasks,
)

OUT = ROOT / "data" / "w33_pass228_sentinel_weight_enumerator.json"


def sentinel_basis(q):
    points = pg3_points(q)
    n = len(points)
    lines = isotropic_lines(points, q)
    rows = incidence_rows(lines, n)
    masks = rows_to_bitmasks(rows)
    Cbasis = f2_rowspace_basis(masks)
    kC = len(Cbasis)
    gram_rows = [
        tuple(1 if popcount(a & b) & 1 else 0 for b in Cbasis) for a in Cbasis
    ]
    hull_coeffs = f2_nullspace(gram_rows, kC)
    hull_words = []
    for cc in hull_coeffs:
        w = 0
        for i in range(kC):
            if (cc >> i) & 1:
                w ^= Cbasis[i]
        if w:
            hull_words.append(w)
    hull_basis = f2_rowspace_basis(hull_words)
    return n, doubly_even_subcode(hull_basis)


def full_weight_distribution(basis, n):
    """Exact A_0..A_n by Gray-code enumeration of the 2^k codewords."""
    k = len(basis)
    A = [0] * (n + 1)
    A[0] = 1  # the zero word (counted once; loop below starts at 1)
    cur = 0
    for i in range(1, 1 << k):
        j = (i & -i).bit_length() - 1
        cur ^= basis[j]
        A[popcount(cur)] += 1
    return A


def macwilliams(A, n, dim_dual):
    """B_k = (1/2^{dim_dual}) * [y^k x^{n-k}] W_A(x+y, x-y),
    with W_A = sum_i A_i x^{n-i} y^i.  Returns exact integer list B_0..B_n."""
    scale = 1 << dim_dual
    B = [0] * (n + 1)
    for k in range(n + 1):
        total = 0
        for i in range(n + 1):
            if A[i] == 0:
                continue
            # coeff of y^k in (x+y)^{n-i} (x-y)^i  = sum_{a+b=k} C(n-i,a)C(i,b)(-1)^b
            s = 0
            for b in range(0, k + 1):
                a = k - b
                if a > n - i or b > i:
                    continue
                s += comb(n - i, a) * comb(i, b) * ((-1) ** b)
            total += A[i] * s
        assert total % scale == 0, (k, total, scale)
        B[k] = total // scale
    return B


def main():
    checks = {}
    n, sent = sentinel_basis(3)
    dim = len(sent)
    A = full_weight_distribution(sent, n)

    # sentinel is doubly-even: only weights == 0 mod 4 populated
    de = all(A[w] == 0 for w in range(n + 1) if w % 4 != 0)
    d_min = next(w for w in range(1, n + 1) if A[w] > 0)
    total_sent = sum(A)

    # MacWilliams -> context code [40,25,4] enumerator
    B = macwilliams(A, n, dim_dual=dim)  # dim_dual = dim(sentinel)=15
    nonneg = all(b >= 0 for b in B)
    integral = all(isinstance(b, int) for b in B)
    total_ctx = sum(B)
    d_ctx = next(w for w in range(1, n + 1) if B[w] > 0)

    checks["sentinel_dim_15"] = dim == 15
    checks["sentinel_total_2^15"] = total_sent == (1 << 15)
    checks["sentinel_doubly_even"] = bool(de)
    checks["sentinel_dmin_8"] = d_min == 8
    checks["macwilliams_nonneg_integers"] = bool(nonneg and integral)
    checks["context_total_2^25"] = total_ctx == (1 << 25)
    checks["context_dmin_4"] = d_ctx == 4
    checks["context_A4_eq_40_lines"] = B[4] == 40  # the 40 isotropic lines (Pass 168)

    # nonzero weights present, as (weight, count) pairs, for the record
    sent_spectrum = {str(w): A[w] for w in range(n + 1) if A[w] > 0}
    ctx_low = {str(w): B[w] for w in range(0, 13) if B[w] > 0}

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass228.sentinel_weight_enumerator.v1",
        "status": "PASS" if all_pass else "FAIL",
        "sentinel_40_15_8": {
            "dimension": dim,
            "min_distance": d_min,
            "doubly_even": bool(de),
            "A8_min_weight_words": A[8],
            "weight_spectrum": sent_spectrum,
            "total_words": total_sent,
        },
        "context_40_25_4_via_macwilliams": {
            "min_distance": d_ctx,
            "B4_lines": B[4],
            "low_weight_spectrum": ctx_low,
            "total_words": total_ctx,
            "reconstructed_from": "sentinel enumerator alone (MacWilliams)",
        },
        "reading": (
            "The q=3 sentinel [40,15,8] is doubly-even with A_8 minimum-weight "
            "words; MacWilliams reconstructs the context [40,25,4] enumerator "
            "from it exactly, with B_4 = 40 = the isotropic lines (Pass 168). "
            "The two dual codes' weight enumerators are locked together, "
            "certifying the doubly-even self-orthogonal shadow picture. The "
            "q=5,7 sentinel enumerators (dim 65,175) are beyond exhaustive "
            "reach -- the exact theta tower is open."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
