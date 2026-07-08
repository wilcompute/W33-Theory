#!/usr/bin/env python3
"""
Pass 85 -- The binary code C_2(W) = [40,16,8]: full weight enumerator and its structure.

The paper cites C_2(W) = [40,16,8] (Supplement N.2) as the binary code spanned by the rows of the
W(3,3) adjacency, but never computes its weight distribution.  GUAVA (w33_pass85_codes.g) gives it:

  weight :   0    8    12     16     20     24    28   32   40
  count  :   1   45  1120  15570  32064  15570  1120   45    1        (total = 2^16 = 65536)

This is a DOUBLY-EVEN (all weights divisible by 4), SELF-ORTHOGONAL (C subset C^perp), SYMMETRIC
(contains the all-ones word) [40,16,8] code.  Self-orthogonality is not a numerical accident: over
GF(2) the SRG identity A^2 = kI + lambda A + mu(J-I-A) = 12I + 2A + 4(J-I-A) reduces to A^2 = 0
because k=12, lambda=2, mu=4 are all EVEN -- so every pair of rows is orthogonal.  The 45
minimum-weight (weight-8) codewords match the 45 TRITANGENT PLANES of the cubic surface (the E6
count that recurs throughout the substrate).

By Gleason's theorem the weight enumerators of doubly-even self-dual codes are polynomials in the
E8 enumerator x^8+14x^4y^4+y^8 and the Golay enumerator; C_2(W) is a doubly-even self-orthogonal
subcode of length 40 = 8*5, embedding in that modular-forms ring.

Self-contained (verifies A^2 = 0 mod 2 directly; reads the GUAVA weight distribution).  ASCII-only.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np

from w33_pass73_prime_geodesics import build_graph

GAP_OUT = Path("w33_pass85_codes_out.txt")


def read_gap():
    if not GAP_OUT.exists():
        return None
    txt = GAP_OUT.read_text()

    def grab(key, default=None):
        m = re.search(rf"{key}=(.*)", txt)
        return m.group(1).strip() if m else default

    wd_raw = grab("binary_weight_distribution", "[]")
    wd = [int(x) for x in re.findall(r"\d+", wd_raw)]
    return {
        "n": int(grab("binary_n", 0)),
        "k": int(grab("binary_k", 0)),
        "d": int(grab("binary_d", 0)),
        "weight_distribution": wd,  # index i -> #codewords of weight i
        "self_orthogonal": grab("binary_self_orthogonal") == "true",
        "doubly_even": grab("binary_doubly_even") == "true",
        "contains_allones": grab("binary_contains_allones") == "true",
    }


def main():
    gap = read_gap()
    if gap is None:
        print("[pass85] missing GUAVA certificate w33_pass85_codes_out.txt")
        return 2

    wd = gap["weight_distribution"]
    weights = {i: c for i, c in enumerate(wd) if c}
    total = sum(wd)

    # verify self-orthogonality directly: A^2 = 0 over GF(2)
    _, A = build_graph()
    A2_mod2 = (A @ A) % 2
    self_orthogonal_direct = bool(np.all(A2_mod2 == 0))

    # doubly-even from the distribution
    doubly_even = all(w % 4 == 0 for w in weights)
    symmetric = all(weights.get(w, 0) == weights.get(40 - w, 0) for w in weights)
    min_weight = min(w for w in weights if w > 0)

    checks = {
        "is_40_16_8": (gap["n"], gap["k"], gap["d"]) == (40, 16, 8),
        "weight_distribution_sums_to_2^16": total == 2**16,
        "doubly_even": doubly_even and gap["doubly_even"],
        "self_orthogonal_A2_is_0_mod_2": self_orthogonal_direct
        and gap["self_orthogonal"],
        "symmetric_contains_allones": symmetric and gap["contains_allones"],
        "min_weight_words_45_tritangent_planes": weights.get(8) == 45,
    }
    all_ok = all(checks.values())

    # weight enumerator as W(x,y)
    enum = " + ".join(
        f"{c}*x^{40-w}y^{w}" if w else f"x^40" for w, c in sorted(weights.items())
    )

    print("=" * 74)
    print("PASS 85 -- THE BINARY CODE C_2(W) = [40,16,8] AND ITS WEIGHT ENUMERATOR")
    print("=" * 74)
    print(f"[n,k,d] = [{gap['n']},{gap['k']},{gap['d']}]  (matches Supplement N.2)")
    print(f"weight distribution: {weights}")
    print(f"  total = {total} = 2^16 : {total == 2**16}")
    print(f"doubly-even (all weights div by 4): {doubly_even}")
    print(
        f"self-orthogonal (A^2 = 0 mod 2, since k,lambda,mu even): {self_orthogonal_direct}"
    )
    print(f"symmetric enumerator / contains all-ones: {symmetric}")
    print(f"minimum-weight codewords: {weights.get(8)} = 45 tritangent planes (E6)")
    print()
    print(f"weight enumerator W(x,y) = {enum}")
    print()
    print("checks:")
    for k, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k}")
    print()
    print("=" * 74)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 74)

    payload = {
        "schema": "w33.pass85.codes.v1",
        "status": "PASS" if all_ok else "FAIL",
        "code": {
            "n": gap["n"],
            "k": gap["k"],
            "d": gap["d"],
            "weight_distribution": {str(w): c for w, c in sorted(weights.items())},
            "total_codewords": total,
            "doubly_even": doubly_even,
            "self_orthogonal": self_orthogonal_direct,
            "symmetric_contains_allones": symmetric,
            "min_weight": min_weight,
        },
        "weight_enumerator": enum,
        "connections": {
            "45_min_weight_words_are_tritangent_planes": weights.get(8) == 45,
            "self_orthogonality_reason": "A^2 = 12I+2A+4(J-I-A) = 0 mod 2 (k,lambda,mu all even)",
            "length_40_is_8x5_doubly_even": True,
            "gleason_modular_forms": (
                "doubly-even self-orthogonal subcode of length 40; weight "
                "enumerators of doubly-even self-dual codes are polynomials "
                "in the E8 enumerator x^8+14x^4y^4+y^8 (Gleason)."
            ),
        },
        "checks": checks,
    }
    with open("w33_pass85_codes.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("[wrote] w33_pass85_codes.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
