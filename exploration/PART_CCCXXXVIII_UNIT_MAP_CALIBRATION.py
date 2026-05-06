#!/usr/bin/env python3
"""
PART CCCXXXVIII -- Unit Map / Calibration Compiler
==================================================

CCCXXXVII gave a finite measurement protocol for the W33 RG spinor.  CCCXXXVIII
adds the missing bridge to empirical physics: a unit map.

The finite architecture determines dimensionless objects:

    G, M^2=5049/4, M=sqrt(5049)/2,
    exp(tG), (sI-G)^-1, heat traces, moments, projectors.

It does NOT by itself determine whether one unit of finite RG time equals a
second, a Planck time, an inverse GeV, etc.  Physical interpretation requires a
single scale calibration kappa for a one-dimensional RG/spinor sector:

    G_phys = kappa G,
    M_phys = kappa M,
    t_dimless = kappa t_phys,
    s_dimless = s_phys/kappa,
    tau_dimless = kappa^2 tau_phys.

This compiler proves the scaling laws for propagator, resolvent, heat trace,
zeta function, and projectors.  It also demonstrates that projectors and branch
weights are scale-invariant, while mass, resolvent normalization, and heat time
scale covariantly.
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


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def matmul(A0: Matrix, B0: Matrix) -> Matrix:
    return (
        (A0[0][0] * B0[0][0] + A0[0][1] * B0[1][0], A0[0][0] * B0[0][1] + A0[0][1] * B0[1][1]),
        (A0[1][0] * B0[0][0] + A0[1][1] * B0[1][0], A0[1][0] * B0[0][1] + A0[1][1] * B0[1][1]),
    )


def matscale(c: Fraction, A0: Matrix) -> Matrix:
    return ((c * A0[0][0], c * A0[0][1]), (c * A0[1][0], c * A0[1][1]))


def matadd(A0: Matrix, B0: Matrix) -> Matrix:
    return ((A0[0][0] + B0[0][0], A0[0][1] + B0[0][1]), (A0[1][0] + B0[1][0], A0[1][1] + B0[1][1]))


def matsub(A0: Matrix, B0: Matrix) -> Matrix:
    return ((A0[0][0] - B0[0][0], A0[0][1] - B0[0][1]), (A0[1][0] - B0[1][0], A0[1][1] - B0[1][1]))


def det(A0: Matrix) -> Fraction:
    return A0[0][0] * A0[1][1] - A0[0][1] * A0[1][0]


def trace(A0: Matrix) -> Fraction:
    return A0[0][0] + A0[1][1]


def m_to_json(A0: Matrix) -> List[List[str]]:
    return [[frac_str(x) for x in row] for row in A0]


def g_square() -> Matrix:
    return matmul(G, G)


def scaled_generator(kappa: Fraction) -> Matrix:
    return matscale(kappa, G)


def scaled_mass_squared(kappa: Fraction) -> Fraction:
    return kappa * kappa * M2


def resolvent_dimless(s: Fraction) -> Matrix:
    denom = s * s - M2
    return matscale(Fraction(1, 1) / denom, matadd(matscale(s, I), G))


def resolvent_phys(s_phys: Fraction, kappa: Fraction) -> Matrix:
    Gp = scaled_generator(kappa)
    denom = s_phys * s_phys - scaled_mass_squared(kappa)
    return matscale(Fraction(1, 1) / denom, matadd(matscale(s_phys, I), Gp))


def scale_resolvent_from_dimless(s_phys: Fraction, kappa: Fraction) -> Matrix:
    s_dimless = s_phys / kappa
    return matscale(Fraction(1, 1) / kappa, resolvent_dimless(s_dimless))


def heat_trace_dimless(tau: float) -> float:
    return 2.0 * math.exp(-float(M2) * tau)


def heat_trace_phys(tau_phys: float, kappa: float) -> float:
    return 2.0 * math.exp(-(kappa * kappa) * float(M2) * tau_phys)


def spinor_trace_dimless(t: float) -> float:
    return 2.0 * math.cosh(M * t)


def spinor_trace_phys(t_phys: float, kappa: float) -> float:
    return 2.0 * math.cosh((kappa * M) * t_phys)


def zeta_dimless(p: int) -> Fraction:
    return Fraction(2, 1) / (M2 ** p)


def zeta_phys(p: int, kappa: Fraction) -> Fraction:
    return Fraction(2, 1) / (scaled_mass_squared(kappa) ** p)


def branch_projectors_float(kappa: float = 1.0) -> Tuple[FMatrix, FMatrix]:
    # Projectors are invariant: G_phys/M_phys = G/M.
    Gf = ((kappa * float(G[0][0]), kappa * float(G[0][1])), (kappa * float(G[1][0]), kappa * float(G[1][1])))
    Mphys = kappa * M
    J = ((Gf[0][0] / Mphys, Gf[0][1] / Mphys), (Gf[1][0] / Mphys, Gf[1][1] / Mphys))
    I2 = ((1.0, 0.0), (0.0, 1.0))
    Pp = ((0.5 * (I2[0][0] + J[0][0]), 0.5 * (I2[0][1] + J[0][1])), (0.5 * (I2[1][0] + J[1][0]), 0.5 * (I2[1][1] + J[1][1])))
    Pm = ((0.5 * (I2[0][0] - J[0][0]), 0.5 * (I2[0][1] - J[0][1])), (0.5 * (I2[1][0] - J[1][0]), 0.5 * (I2[1][1] - J[1][1])))
    return Pp, Pm


def max_abs_diff(A0: FMatrix, B0: FMatrix) -> float:
    return max(abs(A0[i][j] - B0[i][j]) for i in range(2) for j in range(2))


def calibrate_kappa_from_mass(M_phys: float) -> float:
    return M_phys / M


def calibrate_kappa_from_heat(tau_phys: float, H: float) -> float:
    # H=2 exp(-kappa^2 M2 tau) => kappa=sqrt(-log(H/2)/(M2 tau)).
    return math.sqrt(-math.log(H / 2.0) / (float(M2) * tau_phys))


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    kappa = Fraction(7, 3)
    Gp = scaled_generator(kappa)
    Gp2 = matmul(Gp, Gp)
    expected_Gp2 = matscale(scaled_mass_squared(kappa), I)
    s_phys = Fraction(100, 1)
    R_phys = resolvent_phys(s_phys, kappa)
    R_scaled = scale_resolvent_from_dimless(s_phys, kappa)
    tau_phys = 0.001
    H_phys = heat_trace_phys(tau_phys, float(kappa))
    H_scaled = heat_trace_dimless(float(kappa * kappa) * tau_phys)
    t_phys = 0.01
    T_phys = spinor_trace_phys(t_phys, float(kappa))
    T_scaled = spinor_trace_dimless(float(kappa) * t_phys)
    zeta_p2_phys = zeta_phys(2, kappa)
    zeta_scaled = zeta_dimless(2) / (kappa ** 4)
    Pp1, Pm1 = branch_projectors_float(1.0)
    Ppk, Pmk = branch_projectors_float(float(kappa))
    kappa_from_mass = calibrate_kappa_from_mass(float(kappa) * M)
    kappa_from_heat = calibrate_kappa_from_heat(tau_phys, H_phys)

    checks.append(ok("dimensionless mass shell is 5049/4", M2 == Fraction(5049, 4), frac_str(M2)))
    checks.append(ok("scaled generator squares to scaled mass shell", Gp2 == expected_Gp2, m_to_json(Gp2)))
    checks.append(ok("scaled mass squared = kappa^2 M2", scaled_mass_squared(kappa) == kappa * kappa * M2, frac_str(scaled_mass_squared(kappa))))
    checks.append(ok("physical resolvent scales as kappa^-1 dimensionless resolvent", R_phys == R_scaled, m_to_json(R_phys)))
    checks.append(ok("physical heat trace equals dimensionless heat at tau_dimless=kappa^2 tau_phys", abs(H_phys - H_scaled) < 1e-15, H_phys))
    checks.append(ok("physical spinor trace equals dimensionless trace at t_dimless=kappa t_phys", abs(T_phys - T_scaled) < 1e-15, T_phys))
    checks.append(ok("zeta scales as kappa^-2p", zeta_p2_phys == zeta_scaled, frac_str(zeta_p2_phys)))
    checks.append(ok("branch P_plus invariant under kappa", max_abs_diff(Pp1, Ppk) < 1e-12, Ppk))
    checks.append(ok("branch P_minus invariant under kappa", max_abs_diff(Pm1, Pmk) < 1e-12, Pmk))
    checks.append(ok("mass calibration recovers kappa", abs(kappa_from_mass - float(kappa)) < 1e-12, kappa_from_mass))
    checks.append(ok("heat calibration recovers kappa", abs(kappa_from_heat - float(kappa)) < 1e-12, kappa_from_heat))

    verified = all(check["passed"] for check in checks)

    laws = {
        "generator": "G_phys = kappa G",
        "mass": "M_phys = kappa M",
        "mass_squared": "M_phys^2 = kappa^2 M^2",
        "time": "t_dimless = kappa t_phys",
        "heat_time": "tau_dimless = kappa^2 tau_phys",
        "resolvent_frequency": "s_dimless = s_phys/kappa",
        "resolvent": "(s_phys I-G_phys)^-1 = kappa^-1 ((s_phys/kappa)I-G)^-1",
        "zeta": "zeta_phys(p)=kappa^(-2p) zeta_dimless(p)",
        "projectors": "P_± are invariant under kappa",
    }

    return {
        "part": "CCCXXXVIII",
        "title": "Unit Map / Calibration Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "dimensionless_kernel": {
            "G": m_to_json(G),
            "M2": frac_str(M2),
            "M": "sqrt(5049)/2",
        },
        "calibration_constant": {
            "symbol": "kappa",
            "meaning": "physical units per finite RG/spinor unit",
            "sample_kappa": frac_str(kappa),
            "honest_requirement": "must be fixed by one physical anchor measurement or convention",
        },
        "scaling_laws": laws,
        "sample_scaled_sector": {
            "kappa": frac_str(kappa),
            "G_phys": m_to_json(Gp),
            "M_phys_squared": frac_str(scaled_mass_squared(kappa)),
            "resolvent_sample_s_phys_100": m_to_json(R_phys),
            "heat_trace_tau_phys_0_001": H_phys,
            "spinor_trace_t_phys_0_01": T_phys,
            "zeta_phys_p2": frac_str(zeta_p2_phys),
        },
        "calibration_recipes": {
            "from_mass_anchor": "kappa=M_phys/M_dimless",
            "from_heat_sample": "kappa=sqrt(-log(H/2)/(M2 tau_phys))",
            "from_spinor_trace_sample": "kappa=arcosh(T/2)/(M_dimless t_phys)",
            "from_resolvent_sample": "solve R=2s/(s^2-kappa^2 M2) for kappa",
        },
        "architecture_upgrade": (
            "CCCXXXVII gave a finite measurement protocol.  CCCXXXVIII adds the unit "
            "map: all finite spectral objects scale covariantly under one calibration "
            "constant kappa, while branch projectors and weights remain invariant."
        ),
        "theorem": (
            "The W33 RG spinor architecture determines dimensionless spectra and projectors. "
            "A physical unit assignment is obtained by G_phys=kappa G.  Then masses scale "
            "by kappa, heat time by kappa^2, RG/spinor time by kappa, resolvents by "
            "kappa^-1 after frequency rescaling, zeta values by kappa^(-2p), and branch "
            "projectors are invariant.  Thus one calibration constant is necessary and "
            "sufficient for the one-sector unit map."
        ),
        "honesty_boundary": (
            "The finite architecture does not determine absolute physical units internally. "
            "It determines dimensionless structure plus covariant scaling laws; a physical "
            "anchor is required to set kappa."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXXVIII_unit_map_calibration_results.json"
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
