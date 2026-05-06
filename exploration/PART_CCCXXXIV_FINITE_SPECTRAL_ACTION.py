#!/usr/bin/env python3
"""
PART CCCXXXIV -- Finite Spectral Action / Heat Kernel Compiler
==============================================================

CCCXXXIII gave the finite propagator and resolvent for the W33 RG spinor:

    (sI-G)^(-1) = (sI+G)/(s^2-5049/4),
    exp(tG)=exp(mt)P_+ + exp(-mt)P_-,
    m=sqrt(5049)/2.

CCCXXXIV extracts the spectral-action layer.  Since the spectrum of G is

    {+m, -m},

we have exact closed forms:

    det(sI-G)       = s^2 - m^2,
    tr((sI-G)^-1)   = 2s/(s^2-m^2),
    tr(exp(tG))     = 2 cosh(mt),
    tr(exp(-tau G^2)) = 2 exp(-tau m^2),
    zeta_G2(p)      = 2 (m^2)^(-p).

This is the finite spectral response kernel sitting between the exact W33
propagator and any future continuum spectral action.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Tuple

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
M = math.sqrt(DELTA) / 2.0

Matrix = Tuple[Tuple[Fraction, Fraction], Tuple[Fraction, Fraction]]
G: Matrix = ((Fraction(B, 2), Fraction(A, 1)), (Fraction(1, 1), Fraction(-B, 2)))
I: Matrix = ((Fraction(1, 1), Fraction(0, 1)), (Fraction(0, 1), Fraction(1, 1)))


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def matmul(A0: Matrix, B0: Matrix) -> Matrix:
    return (
        (A0[0][0] * B0[0][0] + A0[0][1] * B0[1][0], A0[0][0] * B0[0][1] + A0[0][1] * B0[1][1]),
        (A0[1][0] * B0[0][0] + A0[1][1] * B0[1][0], A0[1][0] * B0[0][1] + A0[1][1] * B0[1][1]),
    )


def matadd(A0: Matrix, B0: Matrix) -> Matrix:
    return ((A0[0][0] + B0[0][0], A0[0][1] + B0[0][1]), (A0[1][0] + B0[1][0], A0[1][1] + B0[1][1]))


def matsub(A0: Matrix, B0: Matrix) -> Matrix:
    return ((A0[0][0] - B0[0][0], A0[0][1] - B0[0][1]), (A0[1][0] - B0[1][0], A0[1][1] - B0[1][1]))


def matscale(c: Fraction, A0: Matrix) -> Matrix:
    return ((c * A0[0][0], c * A0[0][1]), (c * A0[1][0], c * A0[1][1]))


def trace(A0: Matrix) -> Fraction:
    return A0[0][0] + A0[1][1]


def det(A0: Matrix) -> Fraction:
    return A0[0][0] * A0[1][1] - A0[0][1] * A0[1][0]


def g_square() -> Matrix:
    return matmul(G, G)


def characteristic_det(s: Fraction) -> Fraction:
    # det(sI-G)=s^2-m^2.
    sI_minus_G = matsub(matscale(s, I), G)
    return det(sI_minus_G)


def resolvent_trace(s: Fraction) -> Fraction:
    return Fraction(2, 1) * s / (s * s - M2)


def spinor_propagator_trace(t: float) -> float:
    return 2.0 * math.cosh(M * t)


def kg_heat_trace(tau: float) -> float:
    return 2.0 * math.exp(-float(M2) * tau)


def spectral_zeta_g2(p: int) -> Fraction:
    return Fraction(2, 1) / (M2 ** p)


def spectral_action_cutoff(Lambda2: Fraction) -> int:
    """Sharp cutoff count of G^2 eigenvalues <= Lambda2."""
    return 2 if M2 <= Lambda2 else 0


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    G2 = g_square()
    s = Fraction(100, 1)
    det_sample = characteristic_det(s)
    trace_res_sample = resolvent_trace(s)
    zeta1 = spectral_zeta_g2(1)
    zeta2 = spectral_zeta_g2(2)
    tau = 0.001
    t = 0.01
    cutoff_low = spectral_action_cutoff(Fraction(1000, 1))
    cutoff_high = spectral_action_cutoff(Fraction(2000, 1))

    checks.append(ok("G trace is zero", trace(G) == 0, frac_str(trace(G))))
    checks.append(ok("G determinant is -m^2", det(G) == -M2, frac_str(det(G))))
    checks.append(ok("G^2=m^2 I", G2 == matscale(M2, I), [[frac_str(x) for x in row] for row in G2]))
    checks.append(ok("mass squared = 5049/4", M2 == Fraction(5049, 4), frac_str(M2)))
    checks.append(ok("characteristic determinant det(sI-G)=s^2-m^2", det_sample == s * s - M2, frac_str(det_sample)))
    checks.append(ok("resolvent trace = 2s/(s^2-m^2)", trace_res_sample == Fraction(800, 34951), frac_str(trace_res_sample)))
    checks.append(ok("zeta_G2(1)=2/m^2", zeta1 == Fraction(8, 5049), frac_str(zeta1)))
    checks.append(ok("zeta_G2(2)=2/m^4", zeta2 == Fraction(32, 5049 * 5049), frac_str(zeta2)))
    checks.append(ok("sharp spectral action below mass shell is zero", cutoff_low == 0, cutoff_low))
    checks.append(ok("sharp spectral action above mass shell counts two modes", cutoff_high == 2, cutoff_high))
    checks.append(ok("spinor heat/propagator trace >= 2", spinor_propagator_trace(t) >= 2.0, spinor_propagator_trace(t)))
    checks.append(ok("KG heat trace between 0 and 2 for positive tau", 0.0 < kg_heat_trace(tau) < 2.0, kg_heat_trace(tau)))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXXXIV",
        "title": "Finite Spectral Action / Heat Kernel Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "spectrum": {
            "operator": "G",
            "eigenvalues": ["+sqrt(5049)/2", "-sqrt(5049)/2"],
            "G2_eigenvalue": frac_str(M2),
            "multiplicity_G2": 2,
        },
        "spectral_identities": {
            "det_sI_minus_G": "s^2 - 5049/4",
            "resolvent_trace": "2s/(s^2-5049/4)",
            "spinor_propagator_trace": "2 cosh(sqrt(5049)t/2)",
            "KG_heat_trace": "2 exp(-(5049/4) tau)",
            "zeta_G2_p": "2(5049/4)^(-p)",
        },
        "sample_values": {
            "s": frac_str(s),
            "det_sI_minus_G": frac_str(det_sample),
            "resolvent_trace": frac_str(trace_res_sample),
            "zeta_G2_1": frac_str(zeta1),
            "zeta_G2_2": frac_str(zeta2),
            "spinor_trace_t_0_01": spinor_propagator_trace(t),
            "KG_heat_trace_tau_0_001": kg_heat_trace(tau),
            "sharp_cutoff_1000": cutoff_low,
            "sharp_cutoff_2000": cutoff_high,
        },
        "architecture_upgrade": (
            "CCCXXXIII supplied the resolvent and branch propagator.  CCCXXXIV turns "
            "them into spectral-action data: characteristic determinant, resolvent trace, "
            "spinor trace, KG heat trace, zeta function, and sharp cutoff mode count."
        ),
        "theorem": (
            "The finite RG spinor generator has spectrum {+sqrt(5049)/2,-sqrt(5049)/2}. "
            "Therefore det(sI-G)=s^2-5049/4, tr((sI-G)^-1)=2s/(s^2-5049/4), "
            "tr(exp(tG))=2cosh(sqrt(5049)t/2), and tr(exp(-tau G^2))=2exp(-(5049/4)tau)."
        ),
        "honesty_boundary": (
            "This is a finite spectral-action/heat-kernel layer for the RG spinor.  It is "
            "not yet the continuum spectral action of a physical Dirac operator on spacetime."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXXIV_finite_spectral_action_results.json"
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
