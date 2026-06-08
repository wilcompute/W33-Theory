#!/usr/bin/env python3
"""BT554: W33 Levi Cycle Frame Spherical Design Strength Theorem.

BT549 normalized the protected cycle projector into a centered unit-norm tight
frame of 160 vectors in R^81 with inner products by line-graph distance

    1, -1/3, 1/9, -1/27, 1/81.

BT554 tests spherical design strength using Gegenbauer moment sums.  A finite
unit set in S^{d-1} is a spherical t-design iff the Gegenbauer sums vanish for
all degrees 1..t.

Result: the frame is a spherical 2-design but not a 3-design.  The first
obstruction is the exact nonzero degree-3 Gegenbauer moment

    17205568 / 243.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import sympy as sp


def fracstr(x: sp.Rational) -> str:
    x = sp.factor(x)
    return str(x)


def main() -> dict:
    d = sp.Integer(81)
    alpha = sp.Rational(d - 2, 2)
    x = sp.symbols("x")
    profile = {
        sp.Rational(1, 1): 1,
        sp.Rational(-1, 3): 6,
        sp.Rational(1, 9): 18,
        sp.Rational(-1, 27): 54,
        sp.Rational(1, 81): 81,
    }

    moments = {}
    for ell in range(1, 8):
        C = sp.gegenbauer(ell, alpha, x)
        moment = sp.simplify(sum(count * C.subs(x, val) for val, count in profile.items()))
        moments[str(ell)] = str(sp.factor(moment))

    checks = {
        "degree_1_zero": sp.simplify(moments["1"]) == 0,
        "degree_2_zero": sp.simplify(moments["2"]) == 0,
        "degree_3_nonzero": sp.simplify(moments["3"]) != 0,
        "degree_3_exact": moments["3"] == "17205568/243",
    }

    result = {
        "theorem": "BT554 W33 Levi Cycle Frame Spherical Design Strength Theorem",
        "frame": {
            "vectors": 160,
            "ambient_dimension": 81,
            "inner_product_profile_per_vector": {
                "1": 1,
                "-1/3": 6,
                "1/9": 18,
                "-1/27": 54,
                "1/81": 81,
            },
        },
        "gegenbauer_parameter_alpha": "79/2",
        "gegenbauer_moments_degrees_1_to_7": moments,
        "design_strength": 2,
        "first_failure_degree": 3,
        "first_failure_moment": moments["3"],
        "interpretation": "The protected H1=81 cycle frame is exactly a centered unit-norm tight frame / spherical 2-design, but not a 3-design; the first obstruction occurs at cubic moment level.",
        "all_identities": {k: bool(v) for k, v in checks.items()},
        "all_identities_hold": all(bool(v) for v in checks.values()),
    }
    out = Path("data/PART_BT554_W33_LEVI_CYCLE_FRAME_SPHERICAL_DESIGN_STRENGTH_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
