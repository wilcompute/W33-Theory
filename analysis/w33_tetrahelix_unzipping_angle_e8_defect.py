#!/usr/bin/env python3
"""BT506: Tetrahelix Unzipping Angle E8-Defect Theorem.

The uploaded BC/Qi Men paper quotes the standard BC/tetrahelix gap:
  regular tetrahedron dihedral angle delta = acos(1/3),
  five tetrahedra around an edge give 5*delta = 352.643895... degrees,
  leaving the unzipping gap epsilon = 2*pi - 5*delta = 7.356105... degrees.

This theorem extracts the exact identity:
  cos(epsilon) = 241/243 = (240+1)/3^5,
  sin(epsilon) = 22*sqrt(2)/243,
  tan(epsilon) = 22*sqrt(2)/241.

Thus the almost-closed fivefold BC edge-packing has an exact E8-root-count
shadow: the cosine numerator is 240+1 over 3^5.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def main() -> dict:
    delta = sp.acos(sp.Rational(1, 3))
    epsilon = 2 * sp.pi - 5 * delta

    # Exact values via Chebyshev/trig simplification.
    cos_eps = sp.simplify(sp.cos(epsilon))
    sin_eps = sp.simplify(sp.sin(epsilon))
    tan_eps = sp.simplify(sp.tan(epsilon))
    assert cos_eps == sp.Rational(241, 243)
    assert sin_eps == 22 * sp.sqrt(2) / 243
    assert tan_eps == 22 * sp.sqrt(2) / 241

    # Chebyshev polynomial certificate for cos(5*delta).
    x = sp.Symbol("x")
    T5 = sp.chebyshevt(5, x)
    assert sp.expand(T5) == 16 * x**5 - 20 * x**3 + 5 * x
    assert sp.simplify(T5.subs(x, sp.Rational(1, 3))) == sp.Rational(241, 243)

    # Numeric checks.
    delta_deg = float(sp.N(delta * 180 / sp.pi, 16))
    five_delta_deg = float(sp.N(5 * delta * 180 / sp.pi, 16))
    epsilon_deg = float(sp.N(epsilon * 180 / sp.pi, 16))
    assert 70.52 < delta_deg < 70.54
    assert 352.64 < five_delta_deg < 352.65
    assert 7.35 < epsilon_deg < 7.37

    # Denominator/numerator signatures.
    q = 3
    assert q**5 == 243
    assert 241 == 240 + 1
    assert sp.Rational(1, 1) - cos_eps == sp.Rational(2, 243)
    assert (1 - cos_eps) / 2 == sp.Rational(1, 243)  # sin^2(epsilon/2)
    assert sp.simplify(sp.sin(epsilon / 2)) == 1 / (9 * sp.sqrt(3))

    results = {
        "theorem": "BT506 Tetrahelix Unzipping Angle E8-Defect Theorem",
        "input_geometry": {
            "tetrahedron_dihedral_delta": "acos(1/3)",
            "fivefold_edge_pack": "5*delta",
            "unzipping_gap_epsilon": "2*pi - 5*acos(1/3)",
            "delta_degrees": delta_deg,
            "five_delta_degrees": five_delta_deg,
            "epsilon_degrees": epsilon_deg,
        },
        "exact_defect_trigonometry": {
            "cos_epsilon": str(cos_eps),
            "sin_epsilon": str(sin_eps),
            "tan_epsilon": str(tan_eps),
            "one_minus_cos_epsilon": "2/243",
            "sin_squared_half_epsilon": "1/243",
            "sin_half_epsilon": "1/(9*sqrt(3))",
        },
        "chebyshev_certificate": {
            "T5(x)": "16*x^5 - 20*x^3 + 5*x",
            "T5(1/3)": "241/243",
        },
        "substrate_reading": {
            "3^5": "ternary five-step denominator of the edge-packing defect",
            "241": "240+1: E8 root shell plus scalar closure term",
            "2/243": "cosine closure deficit",
            "22sqrt2/243": "sine defect amplitude",
            "fivefold": "BC local quasicrystal attempt: five tetrahedra almost close but unzip",
        },
    }

    out = Path("data/PART_BT506_TETRAHELIX_UNZIPPING_ANGLE_E8_DEFECT_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
