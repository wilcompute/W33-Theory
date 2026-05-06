#!/usr/bin/env python3
"""
PART CCCXXVIII -- Canonical Beta Flow Compiler
==============================================

CCCXXVII converted the finite Euler equation into the inverse-scale fixed-point
law

    y = 67 + 140/y.

CCCXXVIII promotes that fixed-point law to a finite beta-flow.  Define the
canonical inverse-scale beta numerator by

    B(y) = y * (F(y)-y) = 67y + 140 - y^2.

The fixed points are the same roots of

    y^2 - 67y - 140 = 0,

but now the flow has a factorized W33 form

    B(y)=-(y-y_+)(y-y_-),

with exact branch data, derivative spectrum, and basin classification.  This is
the first fully finite RG-like beta object in the W33 architecture.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

Q = 3
LAM = 2
MU = 4
K = 12
V = 40
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1

B_COEFF = 2 * V - PHI3       # 67
A_COEFF = (V // 2) * PHI6    # 140
DISCRIMINANT = B_COEFF * B_COEFF + 4 * A_COEFF
SQRT_DELTA = math.sqrt(DISCRIMINANT)
Y_PLUS = (B_COEFF + SQRT_DELTA) / 2
Y_MINUS = (B_COEFF - SQRT_DELTA) / 2


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def fixed_point_map(y: float) -> float:
    return B_COEFF + A_COEFF / y


def beta_rational(y: float) -> float:
    """Discrete beta: F(y)-y."""
    return fixed_point_map(y) - y


def beta_polynomial(y: float) -> float:
    """Polynomial beta numerator: y(F(y)-y)=67y+140-y^2."""
    return B_COEFF * y + A_COEFF - y * y


def beta_derivative(y: float) -> float:
    """Derivative of polynomial beta numerator."""
    return B_COEFF - 2 * y


def fixed_map_derivative(y: float) -> float:
    return -A_COEFF / (y * y)


def classify_y(y: float) -> str:
    """Classify sign of polynomial beta by intervals around the two fixed points."""
    b = beta_polynomial(y)
    if abs(b) < 1e-12:
        return "fixed"
    if b > 0:
        return "increasing-scale"
    return "decreasing-scale"


def sample_flow_grid() -> List[Dict[str, Any]]:
    samples = [-10, -3, -2.0281578469810335, -1, 1, 10, 67, 69.02815784698112, 80, 140]
    return [
        {"y": y, "beta_num": beta_polynomial(y), "class": classify_y(y)}
        for y in samples
    ]


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    beta_at_plus = beta_polynomial(Y_PLUS)
    beta_at_minus = beta_polynomial(Y_MINUS)
    rational_beta_at_plus = beta_rational(Y_PLUS)
    rational_beta_at_minus = beta_rational(Y_MINUS)
    deriv_plus = beta_derivative(Y_PLUS)
    deriv_minus = beta_derivative(Y_MINUS)
    fixed_deriv_plus = fixed_map_derivative(Y_PLUS)
    fixed_deriv_minus = fixed_map_derivative(Y_MINUS)

    checks.append(ok("B coefficient = 2v-Phi3 = 67", B_COEFF == 67, B_COEFF))
    checks.append(ok("A coefficient = (v/2)Phi6 = 140", A_COEFF == 140, A_COEFF))
    checks.append(ok("beta numerator is 67y+140-y^2", (B_COEFF, A_COEFF) == (67, 140), (B_COEFF, A_COEFF)))
    checks.append(ok("discriminant = q^3(k-1)(Phi4+Phi6)", DISCRIMINANT == Q ** 3 * (K - 1) * (PHI4 + PHI6), DISCRIMINANT))
    checks.append(ok("positive fixed point beta numerator vanishes", abs(beta_at_plus) < 1e-10, beta_at_plus))
    checks.append(ok("negative fixed point beta numerator vanishes", abs(beta_at_minus) < 1e-10, beta_at_minus))
    checks.append(ok("positive fixed point rational beta vanishes", abs(rational_beta_at_plus) < 1e-12, rational_beta_at_plus))
    checks.append(ok("negative fixed point rational beta vanishes", abs(rational_beta_at_minus) < 1e-12, rational_beta_at_minus))
    checks.append(ok("beta derivative at y+ is -sqrt(discriminant)", abs(deriv_plus + SQRT_DELTA) < 1e-12, deriv_plus))
    checks.append(ok("beta derivative at y- is +sqrt(discriminant)", abs(deriv_minus - SQRT_DELTA) < 1e-12, deriv_minus))
    checks.append(ok("fixed map derivative at y+ is attracting", abs(fixed_deriv_plus) < 1.0, fixed_deriv_plus))
    checks.append(ok("fixed map derivative at y- is repelling", abs(fixed_deriv_minus) > 1.0, fixed_deriv_minus))
    checks.append(ok("beta sign below y- is negative", classify_y(-10) == "decreasing-scale", classify_y(-10)))
    checks.append(ok("beta sign between y- and y+ is positive", classify_y(10) == "increasing-scale", classify_y(10)))
    checks.append(ok("beta sign above y+ is negative", classify_y(140) == "decreasing-scale", classify_y(140)))
    checks.append(ok("fixed point sum = 67", abs((Y_PLUS + Y_MINUS) - B_COEFF) < 1e-12, Y_PLUS + Y_MINUS))
    checks.append(ok("fixed point product = -140", abs((Y_PLUS * Y_MINUS) + A_COEFF) < 1e-10, Y_PLUS * Y_MINUS))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXXVIII",
        "title": "Canonical Beta Flow Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "inverse_scale_equation": "y^2 - 67y - 140 = 0",
        "fixed_point_law": "F(y)=67+140/y",
        "rational_beta": "beta(y)=F(y)-y=67+140/y-y",
        "polynomial_beta_numerator": "B(y)=y beta(y)=67y+140-y^2",
        "factorization": "B(y)=-(y-y_+)(y-y_-)",
        "coefficients": {
            "linear": B_COEFF,
            "linear_form": "2v-Phi3",
            "constant": A_COEFF,
            "constant_form": "(v/2)Phi6",
            "discriminant": DISCRIMINANT,
            "discriminant_form": "q^3(k-1)(Phi4+Phi6)",
        },
        "fixed_points": {
            "y_plus_exact": "(67+sqrt(5049))/2",
            "y_minus_exact": "(67-sqrt(5049))/2",
            "y_plus_decimal": Y_PLUS,
            "y_minus_decimal": Y_MINUS,
            "sum": Y_PLUS + Y_MINUS,
            "product": Y_PLUS * Y_MINUS,
        },
        "branch_derivatives": {
            "beta_prime_y_plus": deriv_plus,
            "beta_prime_y_minus": deriv_minus,
            "sqrt_discriminant": SQRT_DELTA,
            "fixed_map_prime_y_plus": fixed_deriv_plus,
            "fixed_map_prime_y_minus": fixed_deriv_minus,
        },
        "branch_classification": {
            "below_y_minus": "decreasing-scale",
            "between_roots": "increasing-scale",
            "above_y_plus": "decreasing-scale",
            "positive_fixed_point": "attracting under F(y)=67+140/y",
            "negative_fixed_point": "repelling under F(y)=67+140/y",
        },
        "sample_flow_grid": sample_flow_grid(),
        "theorem": (
            "The inverse-scale fixed-point law y=67+140/y induces the canonical finite "
            "beta numerator B(y)=67y+140-y^2.  Its zeros are the same W33 closed roots "
            "(67±sqrt(5049))/2, its derivative spectrum is ±sqrt(5049), and the "
            "positive branch is attracting while the negative branch is repelling."
        ),
        "architecture_upgrade": (
            "CCCXXVII gave a fixed-point law.  CCCXXVIII packages it as a finite beta "
            "flow with exact W33 coefficients, discriminant, branch derivatives, and "
            "basin signs.  This is the first canonical RG-like flow object in the TOE "
            "architecture."
        ),
        "honesty_boundary": (
            "This is a finite beta-flow for the inverse-scale coordinate y.  A physical "
            "renormalization-group interpretation requires a unit/scaling map from y to "
            "continuum energy, length, or coupling variables."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXVIII_canonical_beta_flow_results.json"
    out_path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "part": results["part"],
        "verified": results["verified"],
        "checks_passed": results["checks_passed"],
        "checks_total": results["checks_total"],
        "out_path": str(out_path),
    }, indent=2))


if __name__ == "__main__":
    main()
