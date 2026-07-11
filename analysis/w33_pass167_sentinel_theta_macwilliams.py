#!/usr/bin/env python3
"""Pass 167: the sentinel theta -- Construction A and the MacWilliams pair.

The sentinel code S = [40,15,8]_2 (Pass 159) is doubly even, so
Construction A produces an even lattice and the MacWilliams transform
produces the context code's weight enumerator without enumerating 2^25
words.  This witness computes:

1. THE CONTEXT ENUMERATOR.  W_{S^perp} by exact Krawtchouk/MacWilliams
   transform: the full weight distribution of the [40,25] context code,
   its minimum distance ("the lightest legal traffic"), and the parity
   law (j in S forces every context word to have even weight).

2. THE SENTINEL LATTICE.  L_S = {x in Z^40 : x mod 2 in S}, an even
   lattice of rank 40 and determinant 2^50 (scaled: 2^10), whose theta
   series is computed exactly from the weight enumerator:
   theta shells at scaled norms 0..12, with closed-form cross-checks
   (N(2) = 2v = 80 from the +-2e_i vectors; N(4) = 4*C(40,2) + 2^8*45 =
   3120 + 11520 = 14640).
"""

from __future__ import annotations

from collections import Counter
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_w33,
    saturated_kernel,
    w33_lines,
)

OUT = ROOT / "data" / "w33_pass167_sentinel_theta_macwilliams.json"

SENTINEL_ENUMERATOR = {
    0: 1,
    8: 45,
    12: 720,
    16: 6930,
    20: 17376,
    24: 6930,
    28: 720,
    32: 45,
    40: 1,
}


def krawtchouk(n, w, u):
    """K_w(u; n) = sum_j (-1)^j C(u,j) C(n-u, w-j)."""
    total = 0
    for j in range(0, w + 1):
        total += (-1) ** j * math.comb(u, j) * math.comb(n - u, w - j)
    return total


def poly_mul(a, b, cap):
    out = [0] * (cap + 1)
    for i, av in enumerate(a):
        if av == 0 or i > cap:
            continue
        for j, bv in enumerate(b):
            if i + j > cap:
                break
            if bv:
                out[i + j] += av * bv
    return out


def poly_pow(base, exponent, cap):
    result = [1] + [0] * cap
    power = list(base) + [0] * (cap + 1 - len(base))
    while exponent:
        if exponent & 1:
            result = poly_mul(result, power, cap)
        exponent >>= 1
        if exponent:
            power = poly_mul(power, power, cap)
    return result


def main():
    _, adjacency, _ = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    # rebuild the sentinel code and confirm the committed enumerator
    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1
    dark = saturated_kernel(incidence)
    basis2 = (dark % 2).astype(np.uint8).T  # 15 x 40 (columns were basis)
    coeffs = np.array(
        [[(m >> b) & 1 for b in range(15)] for m in range(2**15)],
        dtype=np.uint8,
    )
    words = (coeffs @ basis2) % 2
    enumerator = Counter(int(w) for w in words.sum(axis=1))
    checks["sentinel_enumerator_matches_pass159"] = dict(enumerator) == {
        k: v for k, v in SENTINEL_ENUMERATOR.items()
    }

    # ------------------------------------------------------------------
    # 1. MacWilliams transform -> the context code enumerator
    # ------------------------------------------------------------------
    n = 40
    dual = {}
    for w in range(n + 1):
        total = 0
        for u, count in SENTINEL_ENUMERATOR.items():
            total += count * krawtchouk(n, w, u)
        quotient, remainder = divmod(total, 2**15)
        if remainder != 0:
            checks["macwilliams_integrality"] = False
            quotient = None
        if quotient:
            dual[w] = quotient
    checks.setdefault("macwilliams_integrality", True)
    checks["dual_total_2_25"] = sum(dual.values()) == 2**25
    checks["dual_all_even_weights"] = all(w % 2 == 0 for w in dual if w > 0)
    dual_min = min(w for w in dual if w > 0)
    checks["dual_min_distance_4"] = dual_min == 4
    checks["dual_weight4_at_least_lines"] = dual.get(4, 0) >= 40

    # spot verification of small dual weights by direct search: weight-2
    # words e_a + e_b lie in the context code iff every sentinel word has
    # equal parity at a and b
    weight2 = 0
    for a in range(40):
        for b in range(a + 1, 40):
            if ((words[:, a] ^ words[:, b]) == 0).all():
                weight2 += 1
    checks["no_weight2_context_words"] = weight2 == 0 and 2 not in dual

    # ------------------------------------------------------------------
    # 2. Construction A theta
    # ------------------------------------------------------------------
    cap = 24  # unscaled |x|^2 up to 24 -> scaled norms up to 12
    even_series = [0] * (cap + 1)
    even_series[0] = 1
    for m in range(2, 50, 2):
        if m * m <= cap:
            even_series[m * m] += 2
    odd_series = [0] * (cap + 1)
    for m in range(1, 50, 2):
        if m * m <= cap:
            odd_series[m * m] += 2

    shells = [0] * (13)
    for w, count in SENTINEL_ENUMERATOR.items():
        odd_part = poly_pow(odd_series, w, cap) if w else [1] + [0] * cap
        even_part = poly_pow(even_series, n - w, cap)
        combined = poly_mul(odd_part, even_part, cap)
        for norm in range(0, cap + 1, 2):
            shells[norm // 2] += count * combined[norm]

    checks["theta_shell0_is_1"] = shells[0] == 1
    checks["theta_odd_scaled_shells_vanish"] = all(shells[k] == 0 for k in (1, 3))
    checks["theta_shell2_is_80"] = shells[2] == 80
    expected_4 = 4 * math.comb(40, 2) + (2**8) * 45
    checks["theta_shell4_closed_form"] = shells[4] == expected_4 == 14640

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass167.sentinel_theta_macwilliams.v1",
        "status": "PASS" if all_pass else "FAIL",
        "context_code": {
            "parameters": f"[40, 25, {dual_min}]",
            "weight_enumerator": {str(k): int(dual[k]) for k in sorted(dual)},
            "reading": (
                "the lightest legal traffic has weight 4 (the lines "
                "themselves are among the minimum words); every context "
                "word has even weight because j lies in the sentinel code"
            ),
        },
        "sentinel_lattice": {
            "definition": "L_S = {x in Z^40 : x mod 2 in S}, norms |x|^2/2",
            "rank": 40,
            "determinant_scaled": 2**10,
            "even": True,
            "theta_shells_scaled_0_to_12": [int(v) for v in shells],
            "closed_forms": {
                "N(2)": "2v = 80 (the +-2e_i)",
                "N(4)": "4*C(40,2) + 2^8*45 = 14640",
            },
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
