#!/usr/bin/env python3
"""
PART CCCXXVII -- Inverse Scale Flow Compiler
============================================

CCCXXVI derived the finite Euler stationarity equation

    140 x^2 + 67 x - 1 = 0.

CCCXXVII changes variables to the inverse scale

    y = 1/x.

The finite Euler equation becomes

    y^2 - 67 y - 140 = 0,

or equivalently the feedback/fixed-point law

    y = 67 + 140/y.

The positive branch is attracting; the negative branch is repelling.  This gives
the first finite RG-like runtime flow extracted from the canonical W33 action
kernel.
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

A = (V // 2) * PHI6          # 140
B = 2 * V - PHI3             # 67
DISCRIMINANT = B * B + 4 * A # 5049


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def y_roots() -> Dict[str, float]:
    sqrt_delta = math.sqrt(DISCRIMINANT)
    y_plus = (B + sqrt_delta) / 2
    y_minus = (B - sqrt_delta) / 2
    return {"y_plus": y_plus, "y_minus": y_minus}


def fixed_point_map(y: float) -> float:
    return B + A / y


def derivative_magnitude(y: float) -> float:
    return abs(-A / (y * y))


def iterate_flow(y0: float, steps: int = 8) -> List[float]:
    ys = [float(y0)]
    y = float(y0)
    for _ in range(steps):
        y = fixed_point_map(y)
        ys.append(y)
    return ys


def continued_fraction(x: float, terms: int = 10) -> List[int]:
    out: List[int] = []
    y = float(x)
    for _ in range(terms):
        a = math.floor(y)
        out.append(a)
        frac = y - a
        if abs(frac) < 1e-14:
            break
        y = 1.0 / frac
    return out


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    roots = y_roots()
    y_plus = roots["y_plus"]
    y_minus = roots["y_minus"]
    flow_from_B = iterate_flow(B, 8)
    cf_plus = continued_fraction(y_plus, 12)

    checks.append(ok("inverse-scale equation coefficient B = 2v-Phi3 = 67", B == 67, B))
    checks.append(ok("inverse-scale equation coefficient A = (v/2)Phi6 = 140", A == 140, A))
    checks.append(ok("inverse-scale equation is y^2 - 67y - 140 = 0", (B, A) == (67, 140), (B, A)))
    checks.append(ok("discriminant = q^3(k-1)(Phi4+Phi6)", DISCRIMINANT == Q ** 3 * (K - 1) * (PHI4 + PHI6), DISCRIMINANT))
    checks.append(ok("positive root is approximately 69.028", 69.0 < y_plus < 69.1, y_plus))
    checks.append(ok("negative root is approximately -2.028", -2.1 < y_minus < -2.0, y_minus))
    checks.append(ok("root sum y+ + y- = 67", abs((y_plus + y_minus) - B) < 1e-12, y_plus + y_minus))
    checks.append(ok("root product y+ y- = -140", abs((y_plus * y_minus) + A) < 1e-10, y_plus * y_minus))
    checks.append(ok("positive branch is attracting", derivative_magnitude(y_plus) < 1.0, derivative_magnitude(y_plus)))
    checks.append(ok("negative branch is repelling", derivative_magnitude(y_minus) > 1.0, derivative_magnitude(y_minus)))
    checks.append(ok("flow from y0=B converges near positive root", abs(flow_from_B[-1] - y_plus) < 1e-8, flow_from_B[-1]))
    checks.append(ok("continued fraction starts with 69", cf_plus[0] == 69, cf_plus[:6]))
    checks.append(ok("continued fraction exposes W33 tower entries 17,3,8,7", all(x in cf_plus for x in [17, 3, 8, 7]), cf_plus))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXXVII",
        "title": "Inverse Scale Flow Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "finite_euler_x_equation": "140x^2 + 67x - 1 = 0",
        "inverse_scale_substitution": "y = 1/x",
        "inverse_scale_equation": "y^2 - 67y - 140 = 0",
        "fixed_point_law": "y = 67 + 140/y",
        "coefficients": {
            "B": B,
            "B_form": "2v - Phi3",
            "A": A,
            "A_form": "(v/2) Phi6",
            "discriminant": DISCRIMINANT,
            "discriminant_form": "q^3(k-1)(Phi4+Phi6)",
        },
        "roots": {
            "y_plus_exact": "(67 + sqrt(5049))/2",
            "y_minus_exact": "(67 - sqrt(5049))/2",
            "y_plus_decimal": y_plus,
            "y_minus_decimal": y_minus,
            "x_plus_decimal": 1 / y_plus,
            "x_minus_decimal": 1 / y_minus,
        },
        "stability": {
            "positive_derivative_magnitude": derivative_magnitude(y_plus),
            "negative_derivative_magnitude": derivative_magnitude(y_minus),
            "positive_branch": "attracting",
            "negative_branch": "repelling",
        },
        "iteration_from_B": flow_from_B,
        "continued_fraction_y_plus": cf_plus,
        "theorem": (
            "Under y=1/x, the finite Euler equation becomes y^2-67y-140=0, "
            "equivalently y=67+140/y.  The positive root (67+sqrt(5049))/2 is "
            "an attracting fixed point, while the negative root is repelling.  Thus "
            "the canonical W33 action kernel induces a finite inverse-scale flow."
        ),
        "architecture_upgrade": (
            "CCCXXVI produced stationarity.  CCCXXVII turns stationarity into a "
            "runtime-scale flow with stable and unstable branches.  This is the first "
            "RG-like feedback law extracted from the finite W33 action."
        ),
        "honesty_boundary": (
            "The inverse-scale variable y is a finite runtime scale, not yet proven to "
            "be a physical Hubble, mass, or coupling scale.  Physical identification "
            "requires a separately derived unit map and RG/scaling interpretation."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXVII_inverse_scale_flow_results.json"
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
