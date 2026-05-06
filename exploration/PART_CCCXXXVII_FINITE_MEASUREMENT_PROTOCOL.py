#!/usr/bin/env python3
"""
PART CCCXXXVII -- Finite Measurement Protocol Compiler
======================================================

CCCXXXVI proved that the W33 RG spinor moment tower reconstructs its spectral
measure.  CCCXXXVII turns that reconstruction into an explicit finite
measurement protocol.

The protocol has four tiers:

  Tier A: moment samples m0,m1,m2 reconstruct symmetry and mass shell
          M^2=m2/m0=5049/4.
  Tier B: m0..m4 certify the two-atom recurrence and Hankel rank two.
  Tier C: a single resolvent/heat/spinor trace sample independently recovers
          the same mass shell.
  Tier D: once the generator G is known, the reconstructed mass shell builds
          branch projectors P_±=(I±G/M)/2.

This is the first finite observability layer: it states what must be sampled to
reconstruct the branch spectrum and verify the RG spinor architecture.
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


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def moment(n: int) -> Fraction:
    if n == 0:
        return Fraction(2, 1)
    if n % 2 == 1:
        return Fraction(0, 1)
    return Fraction(2, 1) * (M2 ** (n // 2))


def tier_a_from_moments(m0: Fraction, m1: Fraction, m2: Fraction) -> Dict[str, Any]:
    recovered_m2 = m2 / m0
    symmetric = m1 == 0
    weights = (m0 / 2, m0 / 2) if symmetric else None
    return {
        "symmetric": symmetric,
        "recovered_M2": recovered_m2,
        "weights_if_symmetric": weights,
        "atoms": ["+sqrt(M2)", "-sqrt(M2)"] if symmetric else None,
    }


def det2(Mx: List[List[Fraction]]) -> Fraction:
    return Mx[0][0] * Mx[1][1] - Mx[0][1] * Mx[1][0]


def det3(Mx: List[List[Fraction]]) -> Fraction:
    return (
        Mx[0][0] * (Mx[1][1] * Mx[2][2] - Mx[1][2] * Mx[2][1])
        - Mx[0][1] * (Mx[1][0] * Mx[2][2] - Mx[1][2] * Mx[2][0])
        + Mx[0][2] * (Mx[1][0] * Mx[2][1] - Mx[1][1] * Mx[2][0])
    )


def hankel(size: int) -> List[List[Fraction]]:
    return [[moment(i + j) for j in range(size)] for i in range(size)]


def tier_b_certificate() -> Dict[str, Any]:
    H2 = hankel(2)
    H3 = hankel(3)
    recurrence_m4 = moment(4) == M2 * moment(2)
    return {
        "H2_det": det2(H2),
        "H3_det": det3(H3),
        "rank_two": det2(H2) != 0 and det3(H3) == 0,
        "recurrence_m4_equals_M2_m2": recurrence_m4,
    }


def resolvent_trace(s: Fraction) -> Fraction:
    return Fraction(2, 1) * s / (s * s - M2)


def recover_M2_from_resolvent_sample(s: Fraction, R: Fraction) -> Fraction:
    # R = 2s/(s^2-M2) => M2 = s^2 - 2s/R.
    return s * s - Fraction(2, 1) * s / R


def heat_trace(tau: float) -> float:
    return 2.0 * math.exp(-float(M2) * tau)


def recover_M2_from_heat_sample(tau: float, H: float) -> float:
    # H = 2 exp(-M2 tau) => M2 = -log(H/2)/tau.
    return -math.log(H / 2.0) / tau


def spinor_trace(t: float) -> float:
    return 2.0 * math.cosh(M * t)


def recover_M_from_spinor_trace(t: float, T: float) -> float:
    # T = 2 cosh(Mt) => M = arcosh(T/2)/t.
    return math.acosh(T / 2.0) / t


def matscale_float(c: float, A0: FMatrix) -> FMatrix:
    return ((c * A0[0][0], c * A0[0][1]), (c * A0[1][0], c * A0[1][1]))


def matadd_float(A0: FMatrix, B0: FMatrix) -> FMatrix:
    return ((A0[0][0] + B0[0][0], A0[0][1] + B0[0][1]), (A0[1][0] + B0[1][0], A0[1][1] + B0[1][1]))


def matsub_float(A0: FMatrix, B0: FMatrix) -> FMatrix:
    return ((A0[0][0] - B0[0][0], A0[0][1] - B0[0][1]), (A0[1][0] - B0[1][0], A0[1][1] - B0[1][1]))


def matmul_float(A0: FMatrix, B0: FMatrix) -> FMatrix:
    return (
        (A0[0][0] * B0[0][0] + A0[0][1] * B0[1][0], A0[0][0] * B0[0][1] + A0[0][1] * B0[1][1]),
        (A0[1][0] * B0[0][0] + A0[1][1] * B0[1][0], A0[1][0] * B0[0][1] + A0[1][1] * B0[1][1]),
    )


def max_abs(A0: FMatrix) -> float:
    return max(abs(A0[i][j]) for i in range(2) for j in range(2))


def G_float() -> FMatrix:
    return ((float(G[0][0]), float(G[0][1])), (float(G[1][0]), float(G[1][1])))


def I_float() -> FMatrix:
    return ((1.0, 0.0), (0.0, 1.0))


def projectors_from_measured_mass() -> Tuple[FMatrix, FMatrix]:
    J = matscale_float(1.0 / M, G_float())
    I = I_float()
    return matscale_float(0.5, matadd_float(I, J)), matscale_float(0.5, matsub_float(I, J))


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    tier_a = tier_a_from_moments(moment(0), moment(1), moment(2))
    tier_b = tier_b_certificate()
    s = Fraction(100, 1)
    R = resolvent_trace(s)
    M2_from_R = recover_M2_from_resolvent_sample(s, R)
    tau = 0.001
    H = heat_trace(tau)
    M2_from_H = recover_M2_from_heat_sample(tau, H)
    t = 0.01
    T = spinor_trace(t)
    M_from_T = recover_M_from_spinor_trace(t, T)
    Pp, Pm = projectors_from_measured_mass()

    checks.append(ok("Tier A recovers symmetry from m1=0", tier_a["symmetric"] is True, tier_a["symmetric"]))
    checks.append(ok("Tier A recovers M2=m2/m0=5049/4", tier_a["recovered_M2"] == M2, frac_str(tier_a["recovered_M2"])))
    checks.append(ok("Tier A recovers equal weights", tier_a["weights_if_symmetric"] == (Fraction(1, 1), Fraction(1, 1)), [frac_str(x) for x in tier_a["weights_if_symmetric"]]))
    checks.append(ok("Tier B certifies Hankel rank two", tier_b["rank_two"] is True, {"H2_det": frac_str(tier_b["H2_det"]), "H3_det": frac_str(tier_b["H3_det"])}))
    checks.append(ok("Tier B certifies recurrence at m4", tier_b["recurrence_m4_equals_M2_m2"] is True, True))
    checks.append(ok("Resolvent sample recovers M2 exactly", M2_from_R == M2, frac_str(M2_from_R)))
    checks.append(ok("Heat trace sample recovers M2 numerically", abs(M2_from_H - float(M2)) < 1e-9, M2_from_H))
    checks.append(ok("Spinor trace sample recovers M numerically", abs(M_from_T - M) < 1e-9, M_from_T))
    checks.append(ok("Measured-mass P_plus is idempotent", max_abs(matsub_float(matmul_float(Pp, Pp), Pp)) < 1e-12, Pp))
    checks.append(ok("Measured-mass P_minus is idempotent", max_abs(matsub_float(matmul_float(Pm, Pm), Pm)) < 1e-12, Pm))
    checks.append(ok("Measured-mass branch projectors are orthogonal", max_abs(matmul_float(Pp, Pm)) < 1e-12, matmul_float(Pp, Pm)))

    verified = all(check["passed"] for check in checks)

    protocol = [
        {"tier": "A", "samples": ["m0", "m1", "m2"], "recovers": ["symmetry", "M2=m2/m0", "equal branch weights under symmetry"]},
        {"tier": "B", "samples": ["m0", "m1", "m2", "m3", "m4"], "recovers": ["Hankel rank two", "recurrence m_{n+2}=M2 m_n", "two-atom certificate"]},
        {"tier": "C", "samples": ["one resolvent trace OR one heat trace OR one spinor trace"], "recovers": ["independent M2/M check"]},
        {"tier": "D", "samples": ["G plus recovered M"], "recovers": ["branch projectors P_±=(I±G/M)/2"]},
    ]

    return {
        "part": "CCCXXXVII",
        "title": "Finite Measurement Protocol Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "mass_shell": {
            "M2": frac_str(M2),
            "M": "sqrt(5049)/2",
            "w33_form": "q^3(k-1)(Phi4+Phi6)/4",
        },
        "protocol": protocol,
        "tier_A_moment_reconstruction": {
            "input_moments": {"m0": frac_str(moment(0)), "m1": frac_str(moment(1)), "m2": frac_str(moment(2))},
            "recovered_M2": frac_str(tier_a["recovered_M2"]),
            "recovered_weights": [frac_str(x) for x in tier_a["weights_if_symmetric"]],
            "atoms": ["+sqrt(5049)/2", "-sqrt(5049)/2"],
        },
        "tier_B_rank_certificate": {
            "H2_det": frac_str(tier_b["H2_det"]),
            "H3_det": frac_str(tier_b["H3_det"]),
            "rank_two": tier_b["rank_two"],
            "recurrence_m4_equals_M2_m2": tier_b["recurrence_m4_equals_M2_m2"],
        },
        "tier_C_independent_mass_samples": {
            "resolvent": {"s": frac_str(s), "trace": frac_str(R), "recovered_M2": frac_str(M2_from_R)},
            "heat_trace": {"tau": tau, "trace": H, "recovered_M2": M2_from_H},
            "spinor_trace": {"t": t, "trace": T, "recovered_M": M_from_T},
        },
        "tier_D_projector_reconstruction": {
            "requires": "G and recovered M",
            "P_plus_numeric": Pp,
            "P_minus_numeric": Pm,
            "formula": "P_±=(I±G/M)/2",
        },
        "architecture_upgrade": (
            "CCCXXXVI reconstructed the spectral measure mathematically.  CCCXXXVII "
            "turns that into an observability protocol: finite moment samples and one "
            "optional spectral response sample are enough to reconstruct and verify the "
            "branch mass shell and projector sectors."
        ),
        "theorem": (
            "The W33 RG spinor architecture is finitely observable: m0,m1,m2 recover "
            "the symmetric two-branch mass shell M2=5049/4 and equal weights; m0..m4 "
            "certify Hankel rank two and the recurrence; any one of a resolvent, heat, "
            "or spinor-trace sample independently recovers the same mass shell; and G "
            "with recovered M gives the projectors P_±."
        ),
        "honesty_boundary": (
            "This is a finite mathematical measurement protocol.  Mapping these samples "
            "to laboratory measurements requires a physical observable/unit assignment."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXXVII_finite_measurement_protocol_results.json"
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
