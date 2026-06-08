#!/usr/bin/env python3
"""BT555: W33 Levi Cycle Frame Cubic Obstruction Decomposition.

BT554 proved that the 160-vector W33 Levi cycle frame in R^81 is a spherical
2-design but not a 3-design.  The first nonzero Gegenbauer row-sum is

    C_3 moment = 17205568/243.

BT555 decomposes that cubic obstruction inside the Bose--Mesner/Krein algebra.
Let E4 be the protected primitive idempotent and let

    G = (160/81) E4

be the unit-diagonal Gram matrix of the cycle frame.  For dimension d=81,
alpha=(d-2)/2=79/2, and

    C_3^{alpha}(x) = (177039/2)x^3 - (6399/2)x.

The matrix C_3(G) expands in primitive idempotents as a nonzero combination of
all five sectors.  Its E0 coefficient is exactly 17205568/243, which is the
per-row spherical 3-design obstruction because E0=J/160 is the only sector
with nonzero row sum.
"""

from __future__ import annotations

import json
from pathlib import Path
import sympy as sp


def main() -> dict:
    v = sp.Integer(160)
    d = sp.Integer(81)
    alpha = sp.Rational(d - 2, 2)
    s = sp.sqrt(6)
    valencies = [1, 6, 18, 54, 81]
    multiplicities = [1, 24, 30, 24, 81]
    P = sp.Matrix([
        [1, 6, 18, 54, 81],
        [1, 2+s, 2*s, 6-3*s, -9],
        [1, 2, -6, -6, 9],
        [1, 2-s, -2*s, 6+3*s, -9],
        [1, -2, 2, -2, 1],
    ])
    Q = sp.zeros(5, 5)
    for r in range(5):
        for i in range(5):
            Q[r, i] = sp.simplify(sp.Integer(multiplicities[i]) * P[i, r] / sp.Integer(valencies[r]))

    krein = [[[sp.simplify(sum(Q[l, i] * Q[l, j] * P[k, l] for l in range(5)) / v)
               for k in range(5)] for j in range(5)] for i in range(5)]

    def schur(a: list[sp.Expr], b: list[sp.Expr]) -> list[sp.Expr]:
        return [sp.simplify(sum(a[i] * b[j] * krein[i][j][k] for i in range(5) for j in range(5)) / v)
                for k in range(5)]

    # G=(160/81)E4 in primitive-idempotent coordinates.
    G = [sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Rational(160, 81)]
    G2 = schur(G, G)
    G3 = schur(G2, G)

    x = sp.symbols("x")
    C3 = sp.expand(sp.gegenbauer(3, alpha, x))
    coeff_x3 = sp.Rational(177039, 2)
    coeff_x1 = -sp.Rational(6399, 2)
    C3_expansion = [sp.simplify(coeff_x3 * G3[i] + coeff_x1 * G[i]) for i in range(5)]

    # Direct radial row-sum check from the BT549 profile.
    profile = {
        sp.Rational(1, 1): 1,
        sp.Rational(-1, 3): 6,
        sp.Rational(1, 9): 18,
        sp.Rational(-1, 27): 54,
        sp.Rational(1, 81): 81,
    }
    radial_row_sum = sp.simplify(sum(count * C3.subs(x, val) for val, count in profile.items()))

    checks = {
        "gegenbauer_C3_formula": C3 == coeff_x3 * x**3 + coeff_x1 * x,
        "E0_coeff_equals_radial_row_sum": sp.simplify(C3_expansion[0] - radial_row_sum) == 0,
        "E0_coeff_is_BT554_obstruction": C3_expansion[0] == sp.Rational(17205568, 243),
        "all_five_sectors_present": all(sp.simplify(c) != 0 for c in C3_expansion),
        "degree_1_design_zero": sp.simplify(sum(count * sp.gegenbauer(1, alpha, x).subs(x, val) for val, count in profile.items())) == 0,
        "degree_2_design_zero": sp.simplify(sum(count * sp.gegenbauer(2, alpha, x).subs(x, val) for val, count in profile.items())) == 0,
    }

    result = {
        "theorem": "BT555 W33 Levi Cycle Frame Cubic Obstruction Decomposition",
        "frame": {"vectors": 160, "ambient_dimension": 81, "alpha": str(alpha)},
        "gegenbauer_C3": str(C3),
        "G_expansion": [str(c) for c in G],
        "G_schur_square_expansion": [str(sp.factor(c)) for c in G2],
        "G_schur_cube_expansion": [str(sp.factor(c)) for c in G3],
        "C3_of_G_primitive_expansion": [str(sp.factor(c)) for c in C3_expansion],
        "cubic_obstruction_sector": "E0=J/160",
        "cubic_obstruction_value": str(C3_expansion[0]),
        "interpretation": "The first spherical-design failure is exactly the E0 row-sum component of C_3(G); the cubic Schur/Krein transform is nonzero in all five primitive sectors, but only E0 contributes to the global design obstruction.",
        "all_identities": {k: bool(vv) for k, vv in checks.items()},
        "all_identities_hold": all(bool(vv) for vv in checks.values()),
    }
    out = Path("data/PART_BT555_W33_LEVI_CYCLE_FRAME_CUBIC_OBSTRUCTION_DECOMPOSITION_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
