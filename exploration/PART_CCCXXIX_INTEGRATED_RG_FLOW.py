#!/usr/bin/env python3
"""
PART CCCXXIX -- Integrated Finite RG Flow Compiler
=================================================

CCCXXVIII produced the canonical finite beta numerator

    B(y)=67y+140-y^2 = -(y-y_+)(y-y_-).

CCCXXIX integrates the flow

    dy/dt = B(y)

exactly.  Since y_+ - y_- = sqrt(5049), the flow linearizes under the
cross-ratio coordinate

    R(y) = (y-y_-)/(y_+-y),

with

    d/dt log R(y(t)) = sqrt(5049).

The solution is the logistic/Mobius interpolation

    y(t) = (y_- + R_0 exp(sqrt(5049)t) y_+) / (1 + R_0 exp(sqrt(5049)t)),

where R_0=R(y(0)).  This promotes the architecture from a beta object to an
integrated finite RG renderer with exact W33 time-scale sqrt(5049).
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
DELTA = B * B + 4 * A        # 5049
D = math.sqrt(DELTA)
Y_PLUS = (B + D) / 2
Y_MINUS = (B - D) / 2


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def beta(y: float) -> float:
    return B * y + A - y * y


def cross_ratio(y: float) -> float:
    return (y - Y_MINUS) / (Y_PLUS - y)


def rg_time_coordinate(y: float) -> float:
    return math.log(cross_ratio(y)) / D


def integrated_flow(y0: float, t: float) -> float:
    r0 = cross_ratio(y0)
    rt = r0 * math.exp(D * t)
    return (Y_MINUS + rt * Y_PLUS) / (1.0 + rt)


def flow_derivative_numeric(y0: float, t: float, h: float = 1e-6) -> float:
    return (integrated_flow(y0, t + h) - integrated_flow(y0, t - h)) / (2 * h)


def sample_integrated_flow(y0: float = B) -> List[Dict[str, float]]:
    times = [-0.1, -0.05, 0.0, 0.02, 0.05, 0.1]
    return [{"t": t, "y": integrated_flow(y0, t), "beta": beta(integrated_flow(y0, t))} for t in times]


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    y0 = float(B)
    r0 = cross_ratio(y0)
    t0 = rg_time_coordinate(y0)
    y_at_zero = integrated_flow(y0, 0.0)
    y_forward = integrated_flow(y0, 0.1)
    y_backward = integrated_flow(y0, -0.1)
    deriv_at_zero = flow_derivative_numeric(y0, 0.0)
    beta_at_y0 = beta(y0)
    t_forward = rg_time_coordinate(y_forward)

    checks.append(ok("A=(v/2)Phi6=140", A == 140, A))
    checks.append(ok("B=2v-Phi3=67", B == 67, B))
    checks.append(ok("Delta=q^3(k-1)(Phi4+Phi6)=5049", DELTA == Q ** 3 * (K - 1) * (PHI4 + PHI6), DELTA))
    checks.append(ok("fixed point gap D=sqrt(Delta)=y_plus-y_minus", abs((Y_PLUS - Y_MINUS) - D) < 1e-12, Y_PLUS - Y_MINUS))
    checks.append(ok("beta factorization at sample y=10", abs(beta(10) - (-(10 - Y_PLUS) * (10 - Y_MINUS))) < 1e-10, beta(10)))
    checks.append(ok("cross ratio at y0=B is positive", r0 > 0, r0))
    checks.append(ok("integrated flow recovers y0 at t=0", abs(y_at_zero - y0) < 1e-12, y_at_zero))
    checks.append(ok("integrated derivative equals beta at t=0", abs(deriv_at_zero - beta_at_y0) < 1e-4, (deriv_at_zero, beta_at_y0)))
    checks.append(ok("forward flow moves toward y_plus", y_forward > y0 and y_forward < Y_PLUS, y_forward))
    checks.append(ok("backward flow moves toward y_minus", y_backward < y0 and y_backward > Y_MINUS, y_backward))
    checks.append(ok("RG time shifts additively", abs((t_forward - t0) - 0.1) < 1e-10, t_forward - t0))
    checks.append(ok("positive fixed point is forward-time attractor", abs(integrated_flow(y0, 1.0) - Y_PLUS) < 1e-12, integrated_flow(y0, 1.0)))
    checks.append(ok("negative fixed point is backward-time attractor", abs(integrated_flow(y0, -1.0) - Y_MINUS) < 1e-12, integrated_flow(y0, -1.0)))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXXIX",
        "title": "Integrated Finite RG Flow Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "beta_flow": "dy/dt = 67y + 140 - y^2 = -(y-y_+)(y-y_-)",
        "fixed_points": {
            "y_plus_exact": "(67+sqrt(5049))/2",
            "y_minus_exact": "(67-sqrt(5049))/2",
            "y_plus_decimal": Y_PLUS,
            "y_minus_decimal": Y_MINUS,
            "gap_exact": "sqrt(5049)",
            "gap_decimal": D,
        },
        "linearizing_coordinate": {
            "R(y)": "(y-y_-)/(y_+-y)",
            "RG_time": "tau(y)=log(R(y))/sqrt(5049)",
            "law": "R(y(t)) = R(y0) exp(sqrt(5049)t)",
        },
        "integrated_solution": {
            "formula": "y(t)=(y_-+R0 exp(sqrt(5049)t) y_+)/(1+R0 exp(sqrt(5049)t))",
            "R0": r0,
            "y0": y0,
            "tau_y0": t0,
        },
        "sample_flow_from_y0_67": sample_integrated_flow(y0),
        "architecture_upgrade": (
            "CCCXXVIII gave the beta numerator.  CCCXXIX integrates it exactly.  The "
            "cross-ratio R(y) linearizes the finite RG flow, and sqrt(5049) is the "
            "canonical W33 RG-time eigenvalue."
        ),
        "theorem": (
            "The canonical finite beta flow dy/dt=67y+140-y^2 integrates exactly under "
            "R(y)=(y-y_-)/(y_+-y), with d log R/dt=sqrt(5049).  Thus the W33 action "
            "architecture contains an explicit finite RG renderer before continuum units "
            "are assigned."
        ),
        "honesty_boundary": (
            "This is an exact finite RG-like flow in the inverse-scale coordinate.  A "
            "physical RG interpretation still requires identifying t and y with continuum "
            "energy, length, or coupling variables."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXIX_integrated_rg_flow_results.json"
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
