#!/usr/bin/env python3
"""BT1176 -- intrinsic Sp(4,2) ~= S6 mask-pair dictionary.

Use the standard genus-2 symplectic model over F2.  The six odd quadratic
refinements of the symplectic form form the natural 6-set.  Every unordered pair
of odd quadratic forms differs by a nonzero linear form, and the symplectic form
identifies nonzero linear forms with the 15 nonzero vectors of F2^4.  Hence the
15 masks are intrinsically the 15 duads of the six odd forms.
"""

from __future__ import annotations

import itertools
import json

V = list(itertools.product([0, 1], repeat=4))
NONZERO = [v for v in V if any(v)]


def dot2(u, v):
    return sum(a * b for a, b in zip(u, v)) % 2


def q_eval(a, b, x):
    x0, x1, y0, y1 = x
    return (x0 * y0 + x1 * y1 + a[0] * x0 + a[1] * x1 + b[0] * y0 + b[1] * y1) % 2


def arf(a, b):
    return dot2(a, b)


def lin_coeff_between(q1, q2):
    a1, b1 = q1
    a2, b2 = q2
    return tuple((a1[i] ^ a2[i]) for i in range(2)) + tuple((b1[i] ^ b2[i]) for i in range(2))


def mask_of(v):
    return sum(bit << i for i, bit in enumerate(v))


def main():
    abs_ = list(itertools.product([0, 1], repeat=2))
    odd_forms = [(a, b) for a in abs_ for b in abs_ if arf(a, b) == 1]
    duad_by_mask = {}
    for i, q1 in enumerate(odd_forms):
        for j, q2 in enumerate(odd_forms):
            if i >= j:
                continue
            coeff = lin_coeff_between(q1, q2)
            duad_by_mask[mask_of(coeff)] = (i, j)

    payload = {
        "bt": 1176,
        "title": "intrinsic Sp(4,2)-S6 dictionary from odd quadratic forms",
        "odd_quadratic_forms": [
            {"index": i, "a": list(a), "b": list(b)} for i, (a, b) in enumerate(odd_forms)
        ],
        "duad_by_mask": {str(k): list(v) for k, v in sorted(duad_by_mask.items())},
        "status": "nonzero masks are duads of the six odd quadratic refinements; natural up to relabeling the odd forms",
        "checks": {
            "six_odd_forms": len(odd_forms) == 6,
            "fifteen_duads": len(duad_by_mask) == 15,
            "all_nonzero_masks_hit": sorted(duad_by_mask) == list(range(1, 16)),
            "each_duad_unique": len(set(duad_by_mask.values())) == 15,
        },
    }
    payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
