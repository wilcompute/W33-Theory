#!/usr/bin/env python3
"""
PART CCCXXXIII -- Finite Propagator / Resolvent Compiler
========================================================

CCCXXXII produced the finite Dirac/Klein-Gordon factorization

    (D-G)(D+G) = D^2 - (5049/4)I.

CCCXXXIII turns this into the propagator/resolvent layer.  Since

    G^2 = m^2 I,      m^2 = 5049/4,

we have the exact resolvent identity

    (sI-G)^(-1) = (sI+G)/(s^2-m^2),

and the exact branch-propagator decomposition

    exp(tG) = exp(mt) P_+ + exp(-mt) P_-,

where

    P_± = (I ± G/m)/2.

This is the finite Green's-function layer of the W33 RG spinor architecture.
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
FMatrix = Tuple[Tuple[float, float], Tuple[float, float]]
G: Matrix = ((Fraction(B, 2), Fraction(A, 1)), (Fraction(1, 1), Fraction(-B, 2)))
I: Matrix = ((Fraction(1, 1), Fraction(0, 1)), (Fraction(0, 1), Fraction(1, 1)))
ZERO: Matrix = ((Fraction(0, 1), Fraction(0, 1)), (Fraction(0, 1), Fraction(0, 1)))


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


def m_to_json(A0: Matrix) -> List[List[str]]:
    return [[frac_str(x) for x in row] for row in A0]


def g_square() -> Matrix:
    return matmul(G, G)


def sI_minus_G(s: Fraction) -> Matrix:
    return matsub(matscale(s, I), G)


def sI_plus_G(s: Fraction) -> Matrix:
    return matadd(matscale(s, I), G)


def resolvent(s: Fraction) -> Matrix:
    denom = s * s - M2
    return matscale(Fraction(1, 1) / denom, sI_plus_G(s))


def max_abs_float(A0: FMatrix) -> float:
    return max(abs(A0[i][j]) for i in range(2) for j in range(2))


def matmul_float(A0: FMatrix, B0: FMatrix) -> FMatrix:
    return (
        (A0[0][0] * B0[0][0] + A0[0][1] * B0[1][0], A0[0][0] * B0[0][1] + A0[0][1] * B0[1][1]),
        (A0[1][0] * B0[0][0] + A0[1][1] * B0[1][0], A0[1][0] * B0[0][1] + A0[1][1] * B0[1][1]),
    )


def matadd_float(A0: FMatrix, B0: FMatrix) -> FMatrix:
    return ((A0[0][0] + B0[0][0], A0[0][1] + B0[0][1]), (A0[1][0] + B0[1][0], A0[1][1] + B0[1][1]))


def matsub_float(A0: FMatrix, B0: FMatrix) -> FMatrix:
    return ((A0[0][0] - B0[0][0], A0[0][1] - B0[0][1]), (A0[1][0] - B0[1][0], A0[1][1] - B0[1][1]))


def matscale_float(c: float, A0: FMatrix) -> FMatrix:
    return ((c * A0[0][0], c * A0[0][1]), (c * A0[1][0], c * A0[1][1]))


def G_float() -> FMatrix:
    return ((float(G[0][0]), float(G[0][1])), (float(G[1][0]), float(G[1][1])))


def I_float() -> FMatrix:
    return ((1.0, 0.0), (0.0, 1.0))


def branch_projectors() -> Tuple[FMatrix, FMatrix]:
    J = matscale_float(1.0 / M, G_float())
    Pp = matscale_float(0.5, matadd_float(I_float(), J))
    Pm = matscale_float(0.5, matsub_float(I_float(), J))
    return Pp, Pm


def exp_hyperbolic(t: float) -> FMatrix:
    cosh = math.cosh(M * t)
    sinh_over_m = math.sinh(M * t) / M
    return matadd_float(matscale_float(cosh, I_float()), matscale_float(sinh_over_m, G_float()))


def exp_projector(t: float) -> FMatrix:
    Pp, Pm = branch_projectors()
    return matadd_float(matscale_float(math.exp(M * t), Pp), matscale_float(math.exp(-M * t), Pm))


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    G2 = g_square()
    expected_G2 = matscale(M2, I)
    s = Fraction(100, 1)
    R = resolvent(s)
    left_identity = matmul(sI_minus_G(s), R)
    right_identity = matmul(R, sI_minus_G(s))
    t1 = 0.01
    t2 = 0.02
    U1 = exp_projector(t1)
    U2 = exp_projector(t2)
    U12 = exp_projector(t1 + t2)
    U_semigroup = matmul_float(U1, U2)
    U_hyp = exp_hyperbolic(t1)
    U_proj = exp_projector(t1)
    Pp, Pm = branch_projectors()

    checks.append(ok("G^2=m^2 I", G2 == expected_G2, m_to_json(G2)))
    checks.append(ok("mass squared is 5049/4", M2 == Fraction(5049, 4), frac_str(M2)))
    checks.append(ok("resolvent left inverse exact", left_identity == I, m_to_json(left_identity)))
    checks.append(ok("resolvent right inverse exact", right_identity == I, m_to_json(right_identity)))
    checks.append(ok("resolvent denominator at s=100", s * s - M2 == Fraction(34951, 4), frac_str(s * s - M2)))
    checks.append(ok("projector exponential equals hyperbolic exponential", max_abs_float(matsub_float(U_hyp, U_proj)) < 1e-12, U_proj))
    checks.append(ok("projector propagator semigroup law", max_abs_float(matsub_float(U_semigroup, U12)) < 1e-10, U_semigroup))
    checks.append(ok("P_plus idempotent numeric", max_abs_float(matsub_float(matmul_float(Pp, Pp), Pp)) < 1e-12, Pp))
    checks.append(ok("P_minus idempotent numeric", max_abs_float(matsub_float(matmul_float(Pm, Pm), Pm)) < 1e-12, Pm))
    checks.append(ok("P_plus P_minus orthogonal", max_abs_float(matmul_float(Pp, Pm)) < 1e-12, matmul_float(Pp, Pm)))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXXXIII",
        "title": "Finite Propagator / Resolvent Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "mass_shell": {
            "G_squared": m_to_json(G2),
            "mass_squared": frac_str(M2),
            "mass": "sqrt(5049)/2",
        },
        "resolvent": {
            "formula": "(sI-G)^(-1)=(sI+G)/(s^2-5049/4)",
            "sample_s": frac_str(s),
            "sample_denominator": frac_str(s * s - M2),
            "sample_resolvent": m_to_json(R),
        },
        "propagator": {
            "hyperbolic_form": "exp(tG)=cosh(mt)I+sinh(mt)G/m",
            "branch_form": "exp(tG)=exp(mt)P_+ + exp(-mt)P_-",
            "P_plus_numeric": Pp,
            "P_minus_numeric": Pm,
            "sample_t": t1,
            "sample_exp_tG": U_proj,
        },
        "architecture_upgrade": (
            "CCCXXXII supplied the finite Dirac factorization.  CCCXXXIII adds the "
            "Green's-function layer: the exact resolvent (sI-G)^(-1) and the branch "
            "propagator exp(tG)=e^{mt}P_+ + e^{-mt}P_-."
        ),
        "theorem": (
            "Since G^2=(5049/4)I, the Dirac resolvent is exactly "
            "(sI-G)^(-1)=(sI+G)/(s^2-5049/4), and the spinor propagator decomposes "
            "over the Clifford branch projectors as exp(tG)=e^{mt}P_+ + e^{-mt}P_- "
            "with m=sqrt(5049)/2."
        ),
        "honesty_boundary": (
            "This is a finite Green's-function/propagator layer for the RG spinor. "
            "Physical scattering amplitudes or continuum QFT propagators still require "
            "a physical unit map and spacetime representation."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXXIII_finite_propagator_resolvent_results.json"
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
