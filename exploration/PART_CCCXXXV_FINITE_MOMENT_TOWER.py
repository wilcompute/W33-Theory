#!/usr/bin/env python3
"""
PART CCCXXXV -- Finite Spectral Moment Tower Compiler
=====================================================

CCCXXXIV closed the finite spectral-action package for the W33 RG spinor:

    spec(G) = {+sqrt(5049)/2, -sqrt(5049)/2},
    G^2 = (5049/4)I.

CCCXXXV extracts the moment tower and expansion data that a continuum spectral
action would see:

    tr(G^(2r+1)) = 0,
    tr(G^(2r))   = 2(5049/4)^r,

plus the large-s resolvent expansion, small-t heat/spinor trace expansions, and
large-s log-determinant expansion.  This packages the finite observable tower
that sits between the exact W33 spinor and any continuum asymptotic theory.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

Q = 3
K = 12
V = 40
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
B = 2 * V - PHI3           # 67
A = (V // 2) * PHI6        # 140
DELTA = B * B + 4 * A      # 5049
M2 = Fraction(DELTA, 4)


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def trace_power(n: int) -> Fraction:
    """Trace of G^n from spectrum {+m,-m}."""
    if n == 0:
        return Fraction(2, 1)
    if n % 2 == 1:
        return Fraction(0, 1)
    return Fraction(2, 1) * (M2 ** (n // 2))


def moment_table(nmax: int = 8) -> List[Dict[str, str]]:
    return [{"n": n, "trace_G_power_n": frac_str(trace_power(n))} for n in range(nmax + 1)]


def resolvent_large_s_coefficients(rmax: int = 4) -> List[Dict[str, str]]:
    """tr((sI-G)^-1)=sum_r 2 m2^r s^-(2r+1)."""
    return [
        {"r": r, "power": f"s^-{2*r+1}", "coefficient": frac_str(Fraction(2, 1) * (M2 ** r))}
        for r in range(rmax + 1)
    ]


def spinor_trace_coefficients(rmax: int = 4) -> List[Dict[str, str]]:
    """tr(exp(tG))=sum_r 2 m2^r t^(2r)/(2r)!"""
    return [
        {"r": r, "power": f"t^{2*r}", "coefficient": frac_str(Fraction(2, 1) * (M2 ** r) / math.factorial(2*r))}
        for r in range(rmax + 1)
    ]


def kg_heat_coefficients(rmax: int = 4) -> List[Dict[str, str]]:
    """tr(exp(-tau G^2))=sum_r 2(-m2)^r tau^r/r!."""
    return [
        {"r": r, "power": f"tau^{r}", "coefficient": frac_str(Fraction(2, 1) * ((-M2) ** r) / math.factorial(r))}
        for r in range(rmax + 1)
    ]


def logdet_large_s_coefficients(rmax: int = 4) -> List[Dict[str, str]]:
    """log det(sI-G)=2log(s)-sum_{r>=1} m2^r/(r s^(2r))."""
    return [
        {"r": r, "power": f"s^-{2*r}", "coefficient_after_2log_s": frac_str(-(M2 ** r) / r)}
        for r in range(1, rmax + 1)
    ]


def evaluate_resolvent_trace_exact(s: Fraction) -> Fraction:
    return Fraction(2, 1) * s / (s * s - M2)


def evaluate_resolvent_trace_series(s: Fraction, rmax: int) -> Fraction:
    return sum(Fraction(2, 1) * (M2 ** r) / (s ** (2*r + 1)) for r in range(rmax + 1))


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    moments = moment_table(8)
    res_coeffs = resolvent_large_s_coefficients(4)
    spinor_coeffs = spinor_trace_coefficients(4)
    heat_coeffs = kg_heat_coefficients(4)
    logdet_coeffs = logdet_large_s_coefficients(4)
    s = Fraction(100, 1)
    exact_res = evaluate_resolvent_trace_exact(s)
    series_res_4 = evaluate_resolvent_trace_series(s, 4)
    remainder = exact_res - series_res_4

    checks.append(ok("mass squared = 5049/4", M2 == Fraction(5049, 4), frac_str(M2)))
    checks.append(ok("trace G^0 = 2", trace_power(0) == 2, frac_str(trace_power(0))))
    checks.append(ok("trace G odd powers vanish", all(trace_power(n) == 0 for n in [1, 3, 5, 7]), [frac_str(trace_power(n)) for n in [1, 3, 5, 7]]))
    checks.append(ok("trace G^2 = 5049/2", trace_power(2) == Fraction(5049, 2), frac_str(trace_power(2))))
    checks.append(ok("trace G^4 = 2(5049/4)^2", trace_power(4) == Fraction(2, 1) * M2 * M2, frac_str(trace_power(4))))
    checks.append(ok("resolvent coefficient r=0 is 2", res_coeffs[0]["coefficient"] == "2", res_coeffs[0]))
    checks.append(ok("resolvent coefficient r=1 is 5049/2", res_coeffs[1]["coefficient"] == "5049/2", res_coeffs[1]))
    checks.append(ok("spinor trace t^0 coefficient is 2", spinor_coeffs[0]["coefficient"] == "2", spinor_coeffs[0]))
    checks.append(ok("spinor trace t^2 coefficient is 5049/4", spinor_coeffs[1]["coefficient"] == "5049/4", spinor_coeffs[1]))
    checks.append(ok("heat trace tau coefficient is -5049/2", heat_coeffs[1]["coefficient"] == "-5049/2", heat_coeffs[1]))
    checks.append(ok("logdet first correction is -5049/4", logdet_coeffs[0]["coefficient_after_2log_s"] == "-5049/4", logdet_coeffs[0]))
    checks.append(ok("large-s resolvent partial series underestimates exact positive trace", remainder > 0, frac_str(remainder))))
    checks.append(ok("large-s resolvent remainder is small at s=100", abs(float(remainder)) < 1e-12, float(remainder)))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXXXV",
        "title": "Finite Spectral Moment Tower Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "mass_shell": {
            "m_squared": frac_str(M2),
            "m": "sqrt(5049)/2",
            "w33_form": "q^3(k-1)(Phi4+Phi6)/4",
        },
        "moment_table_n0_to_n8": moments,
        "expansions": {
            "resolvent_large_s": {
                "formula": "tr((sI-G)^-1)=sum_{r>=0} 2(m^2)^r s^-(2r+1)",
                "coefficients_r0_to_r4": res_coeffs,
            },
            "spinor_trace_small_t": {
                "formula": "tr(exp(tG))=sum_{r>=0} 2(m^2)^r t^(2r)/(2r)!",
                "coefficients_r0_to_r4": spinor_coeffs,
            },
            "kg_heat_trace_small_tau": {
                "formula": "tr(exp(-tau G^2))=sum_{r>=0} 2(-m^2)^r tau^r/r!",
                "coefficients_r0_to_r4": heat_coeffs,
            },
            "logdet_large_s": {
                "formula": "log det(sI-G)=2log(s)-sum_{r>=1}(m^2)^r/(r s^(2r))",
                "coefficients_r1_to_r4": logdet_coeffs,
            },
        },
        "sample_large_s_check": {
            "s": frac_str(s),
            "exact_resolvent_trace": frac_str(exact_res),
            "partial_series_r0_to_r4": frac_str(series_res_4),
            "remainder": frac_str(remainder),
        },
        "architecture_upgrade": (
            "CCCXXXIV gave finite spectral traces.  CCCXXXV organizes those traces into "
            "the full observable moment tower and asymptotic expansions seen by a future "
            "continuum spectral-action approximation."
        ),
        "theorem": (
            "For the W33 RG spinor, all odd trace moments vanish and all even moments are "
            "tr(G^(2r))=2(5049/4)^r.  Consequently the resolvent, heat trace, spinor trace, "
            "and log determinant have closed coefficient towers generated by the single "
            "mass-shell atom 5049/4."
        ),
        "honesty_boundary": (
            "This is a finite moment/asymptotic tower.  Matching these coefficients to a "
            "continuum spectral action still requires a scaling family and physical unit map."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXXV_finite_moment_tower_results.json"
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
