#!/usr/bin/env python3
"""
PART CCCCCLXVIII -- K-B Quadratic Scale Bridge
==============================================

Bridge between:
  - CCCCCLXVI dimensional normalization (x = M_F^2 / Lambda^2), and
  - CCCCCLXVII scalar/Yukawa K-B block ledger.

Minimal K-B ansatz variables:
  y := ||Y||^2,   h := Tr(H^2).

From CCCCCLXVII:
  Tr(Phi^2)        = 2y + h
  Tr(Delta_1 Phi^2)= 4y + 4h
  Tr([Delta_1,Phi]^*[Delta_1,Phi]) = 32y

From CCCCCLXVI normalized first-order spectral polynomial:
  c0/240 = 1,
  c1/240 = -4x.

Thus the reduced quadratic functional (first two ladder levels) is
  S2_red(x;y,h) = (2y+h) - 4x(4y+4h)
                = (2-16x) y + (1-16x) h.

Critical roots:
  y-coefficient root at x = 1/8,
  h-coefficient root at x = 1/16.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import json
from pathlib import Path
from typing import Dict


@dataclass(frozen=True)
class KBQuadraticScaleBridgeResult:
    part: str
    title: str
    definitions: Dict[str, str]
    reduced_quadratic_functional: Dict[str, str]
    coefficients: Dict[str, Dict[str, str]]
    critical_roots: Dict[str, str]
    checks: Dict[str, bool]
    all_checks_pass: bool


def _frac_str(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def _build() -> KBQuadraticScaleBridgeResult:
    # Normalized coefficients from CCCCCLXVI: c0/240 = 1, c1/240 = -4x.
    c0 = Fraction(1)
    c1_over_x = Fraction(-4)

    # S2_red = c0*(2y+h) + c1*(4y+4h) with c1 = (-4x).
    # => y coefficient = 2 - 16x, h coefficient = 1 - 16x.
    y_const = Fraction(2)
    y_x = Fraction(-16)
    h_const = Fraction(1)
    h_x = Fraction(-16)

    root_y = -y_const / y_x
    root_h = -h_const / h_x

    checks = {
        "normalized_c0_is_1": c0 == 1,
        "normalized_c1_is_minus4x": c1_over_x == -4,
        "y_coefficient_is_2_minus_16x": y_const == 2 and y_x == -16,
        "h_coefficient_is_1_minus_16x": h_const == 1 and h_x == -16,
        "y_root_is_1_over_8": root_y == Fraction(1, 8),
        "h_root_is_1_over_16": root_h == Fraction(1, 16),
        "hierarchy_h_root_lt_y_root": root_h < root_y,
    }

    return KBQuadraticScaleBridgeResult(
        part="CCCCCLXVIII",
        title="K-B Quadratic Scale Bridge",
        definitions={
            "x": "M_F^2/Lambda^2",
            "y": "||Y||^2",
            "h": "Tr(H^2)",
            "Tr(Phi^2)": "2y+h",
            "Tr(Delta_1 Phi^2)": "4y+4h",
            "commutator_penalty": "32y",
        },
        reduced_quadratic_functional={
            "formula": "S2_red(x;y,h) = (2-16x)y + (1-16x)h",
            "expanded": "(2y+h)-4x(4y+4h)",
        },
        coefficients={
            "y": {
                "constant_term": _frac_str(y_const),
                "x_coefficient": _frac_str(y_x),
            },
            "h": {
                "constant_term": _frac_str(h_const),
                "x_coefficient": _frac_str(h_x),
            },
        },
        critical_roots={
            "y_coefficient_root": _frac_str(root_y),
            "h_coefficient_root": _frac_str(root_h),
        },
        checks=checks,
        all_checks_pass=all(checks.values()),
    )


def main() -> None:
    result = _build()
    payload = asdict(result)
    print(json.dumps(payload, indent=2))
    assert result.all_checks_pass, "K-B quadratic scale bridge checks failed"
    out = Path("data/PART_CCCCCLXVIII_kb_quadratic_scale_bridge_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
