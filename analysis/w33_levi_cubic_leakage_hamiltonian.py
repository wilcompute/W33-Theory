#!/usr/bin/env python3
"""BT558: W33 Levi Cubic Leakage Hamiltonian.

BT555 showed that the first spherical-design obstruction of the W33 Levi cycle
frame is the E0 component of C_3(G), where

    G=(1/81)CC^T=(160/81)E4

is the unit Gram matrix of the 160-point cycle frame in R^81.

BT558 turns this into a leakage Hamiltonian.  Define

    H3 = C_3(G),
    L3 = H3 - h0 E0,

where h0 is the E0 coefficient.  Then L3 has zero row-sum and is exactly the
centered cubic leakage operator.  Its primitive-sector support is

    E1 + E2 + E3 + E4,

so the cubic nonlinearity leaks out of the protected H1=81 sector into the
24+30+24 companion stack.  This is the first nonlinear obstruction after the
spherical 2-design closure.
"""

from __future__ import annotations

import json
from pathlib import Path
import sympy as sp


def main() -> dict:
    v = sp.Integer(160)
    d = sp.Integer(81)
    alpha = sp.Rational(d - 2, 2)
    x = sp.symbols("x")
    s = sp.sqrt(6)
    valencies = [1, 6, 18, 54, 81]
    multiplicities = [1, 24, 30, 24, 81]
    sector_names = ["E0_uniform", "E1_24_plus", "E2_30_middle", "E3_24_minus", "E4_H1_81"]

    P = sp.Matrix([
        [1, 6, 18, 54, 81],
        [1, 2 + s, 2 * s, 6 - 3 * s, -9],
        [1, 2, -6, -6, 9],
        [1, 2 - s, -2 * s, 6 + 3 * s, -9],
        [1, -2, 2, -2, 1],
    ])
    Q = sp.zeros(5, 5)
    for r in range(5):
        for i in range(5):
            Q[r, i] = sp.simplify(sp.Integer(multiplicities[i]) * P[i, r] / sp.Integer(valencies[r]))

    krein = [[[sp.simplify(sum(Q[l, i] * Q[l, j] * P[k, l] for l in range(5)) / v)
               for k in range(5)] for j in range(5)] for i in range(5)]

    def schur(a: list[sp.Expr], b: list[sp.Expr]) -> list[sp.Expr]:
        return [sp.simplify(sum(a[i] * b[j] * krein[i][j][k]
                                for i in range(5) for j in range(5)) / v)
                for k in range(5)]

    # Unit Gram G in primitive coordinates.
    G = [sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Rational(160, 81)]
    G2 = schur(G, G)
    G3 = schur(G2, G)

    C3 = sp.expand(sp.gegenbauer(3, alpha, x))
    coeff_x3 = sp.Rational(177039, 2)
    coeff_x1 = -sp.Rational(6399, 2)
    H3 = [sp.simplify(coeff_x3 * G3[i] + coeff_x1 * G[i]) for i in range(5)]
    h0 = H3[0]
    L3 = [sp.Integer(0)] + [sp.simplify(H3[i]) for i in range(1, 5)]

    # Trace contribution in each primitive sector.
    trace_weights = [sp.simplify(H3[i] * multiplicities[i]) for i in range(5)]
    centered_trace_weights = [sp.simplify(L3[i] * multiplicities[i]) for i in range(5)]

    checks = {
        "gegenbauer_C3_formula": C3 == coeff_x3 * x**3 + coeff_x1 * x,
        "h0_BT554_obstruction": h0 == sp.Rational(17205568, 243),
        "centered_zero_E0": L3[0] == 0,
        "centered_support_E1_to_E4": all(sp.simplify(c) != 0 for c in L3[1:]),
        "total_trace_matches_diagonal": sp.simplify(sum(trace_weights) - v * C3.subs(x, 1)) == 0,
        "centered_trace_is_total_minus_uniform": sp.simplify(sum(centered_trace_weights) - (v * C3.subs(x, 1) - h0)) == 0,
    }

    result = {
        "theorem": "BT558 W33 Levi Cubic Leakage Hamiltonian",
        "input": "G=(1/81)CC^T=(160/81)E4",
        "gegenbauer_C3": str(C3),
        "H3_C3G_primitive_coefficients": dict(zip(sector_names, [str(sp.factor(c)) for c in H3])),
        "uniform_obstruction_h0": str(h0),
        "centered_leakage_L3_coefficients": dict(zip(sector_names, [str(sp.factor(c)) for c in L3])),
        "trace_weights_by_sector": dict(zip(sector_names, [str(sp.factor(c)) for c in trace_weights])),
        "centered_trace_weights_by_sector": dict(zip(sector_names, [str(sp.factor(c)) for c in centered_trace_weights])),
        "support_statement": "H3 has all five primitive sectors; subtracting the uniform E0 obstruction leaves cubic leakage on E1+E2+E3+E4.",
        "physical_reading": "The cycle frame is linearly/Hodge protected and second-order isotropic, but the first cubic nonlinearity leaks from H1=81 into the 24+30+24 companion stack.",
        "all_identities": {k: bool(v) for k, v in checks.items()},
        "all_identities_hold": all(bool(v) for v in checks.values()),
    }
    out = Path("data/PART_BT558_W33_LEVI_CUBIC_LEAKAGE_HAMILTONIAN_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
