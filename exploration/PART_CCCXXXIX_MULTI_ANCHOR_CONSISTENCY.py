#!/usr/bin/env python3
"""
PART CCCXXXIX -- Multi-Anchor Calibration Consistency Compiler
==============================================================

CCCXXXVIII introduced the one-sector unit map

    G_phys = kappa G,
    M_phys = kappa M,

and proved the covariant scaling laws.  CCCXXXIX makes this layer falsifiable:
multiple physical anchors must recover the same kappa.

For the W33 RG spinor, the following anchors independently determine kappa:

    mass anchor:       kappa = M_phys/M
    heat anchor:       kappa = sqrt(-log(H/2)/(M^2 tau_phys))
    spinor trace:      kappa = arcosh(T/2)/(M t_phys)
    resolvent trace:   kappa = sqrt((s^2 - 2s/R)/M^2)
    zeta anchor:       kappa = (zeta_dimless(p)/zeta_phys(p))^(1/(2p))

The one-sector empirical interpretation is internally consistent iff all anchors
agree within tolerance.  This compiler generates a self-consistent synthetic
anchor packet and a deliberately inconsistent packet to prove the detection
logic.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

Q = 3
K = 12
V = 40
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
B = 2 * V - PHI3
A = (V // 2) * PHI6
DELTA = B * B + 4 * A
M2 = DELTA / 4.0
M = math.sqrt(M2)
ZETA_DIMLESS_P2 = 2.0 / (M2 ** 2)


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def heat_trace(tau_phys: float, kappa: float) -> float:
    return 2.0 * math.exp(-(kappa * kappa) * M2 * tau_phys)


def spinor_trace(t_phys: float, kappa: float) -> float:
    return 2.0 * math.cosh((kappa * M) * t_phys)


def resolvent_trace(s_phys: float, kappa: float) -> float:
    return 2.0 * s_phys / (s_phys * s_phys - (kappa * kappa) * M2)


def zeta_phys(p: int, kappa: float) -> float:
    return 2.0 / (((kappa * kappa) * M2) ** p)


def kappa_from_mass(M_phys: float) -> float:
    return M_phys / M


def kappa_from_heat(tau_phys: float, H: float) -> float:
    return math.sqrt(-math.log(H / 2.0) / (M2 * tau_phys))


def kappa_from_spinor_trace(t_phys: float, T: float) -> float:
    return math.acosh(T / 2.0) / (M * t_phys)


def kappa_from_resolvent(s_phys: float, R: float) -> float:
    return math.sqrt((s_phys * s_phys - 2.0 * s_phys / R) / M2)


def kappa_from_zeta(p: int, zeta_value: float) -> float:
    zeta_dimless = 2.0 / (M2 ** p)
    return (zeta_dimless / zeta_value) ** (1.0 / (2.0 * p))


def make_anchor_packet(kappa: float) -> Dict[str, Any]:
    tau = 0.001
    t = 0.01
    s = 100.0
    p = 2
    return {
        "kappa_true": kappa,
        "mass": {"M_phys": kappa * M},
        "heat": {"tau_phys": tau, "trace": heat_trace(tau, kappa)},
        "spinor_trace": {"t_phys": t, "trace": spinor_trace(t, kappa)},
        "resolvent": {"s_phys": s, "trace": resolvent_trace(s, kappa)},
        "zeta": {"p": p, "value": zeta_phys(p, kappa)},
    }


def recover_kappas(packet: Dict[str, Any]) -> Dict[str, float]:
    return {
        "mass": kappa_from_mass(packet["mass"]["M_phys"]),
        "heat": kappa_from_heat(packet["heat"]["tau_phys"], packet["heat"]["trace"]),
        "spinor_trace": kappa_from_spinor_trace(packet["spinor_trace"]["t_phys"], packet["spinor_trace"]["trace"]),
        "resolvent": kappa_from_resolvent(packet["resolvent"]["s_phys"], packet["resolvent"]["trace"]),
        "zeta": kappa_from_zeta(packet["zeta"]["p"], packet["zeta"]["value"]),
    }


def consistency_report(kappas: Dict[str, float], tolerance: float = 1e-9) -> Dict[str, Any]:
    values = list(kappas.values())
    mu = mean(values)
    spread = max(abs(v - mu) for v in values)
    return {
        "kappas": kappas,
        "mean_kappa": mu,
        "std_kappa": pstdev(values),
        "max_abs_deviation": spread,
        "tolerance": tolerance,
        "consistent": spread <= tolerance,
    }


def make_inconsistent_packet(kappa: float) -> Dict[str, Any]:
    packet = make_anchor_packet(kappa)
    # Corrupt exactly one anchor by 1%.  This should be easily detected.
    packet["heat"] = dict(packet["heat"])
    packet["heat"]["trace"] *= 1.01
    return packet


def dimensionless_ratios(kappa: float) -> Dict[str, float]:
    """Ratios that are invariant under the calibration gauge."""
    M_phys = kappa * M
    G_gap_phys = kappa * math.sqrt(DELTA)  # projective eigenvalue gap
    return {
        "projective_gap_over_mass": G_gap_phys / M_phys,
        "M_phys_squared_over_kappa_squared": (M_phys * M_phys) / (kappa * kappa),
        "zeta_p2_scaled_back": zeta_phys(2, kappa) * (kappa ** 4),
    }


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    kappa = 7.0 / 3.0
    packet = make_anchor_packet(kappa)
    kappas = recover_kappas(packet)
    report = consistency_report(kappas)
    bad_packet = make_inconsistent_packet(kappa)
    bad_report = consistency_report(recover_kappas(bad_packet))
    ratios_1 = dimensionless_ratios(1.0)
    ratios_k = dimensionless_ratios(kappa)

    checks.append(ok("dimensionless M2=5049/4", abs(M2 - 5049.0 / 4.0) < 1e-15, M2))
    checks.append(ok("mass anchor recovers kappa", abs(kappas["mass"] - kappa) < 1e-12, kappas["mass"]))
    checks.append(ok("heat anchor recovers kappa", abs(kappas["heat"] - kappa) < 1e-12, kappas["heat"]))
    checks.append(ok("spinor trace anchor recovers kappa", abs(kappas["spinor_trace"] - kappa) < 1e-12, kappas["spinor_trace"]))
    checks.append(ok("resolvent anchor recovers kappa", abs(kappas["resolvent"] - kappa) < 1e-12, kappas["resolvent"]))
    checks.append(ok("zeta anchor recovers kappa", abs(kappas["zeta"] - kappa) < 1e-12, kappas["zeta"]))
    checks.append(ok("consistent packet passes", report["consistent"] is True, report))
    checks.append(ok("corrupted packet fails", bad_report["consistent"] is False, bad_report))
    checks.append(ok("projective gap/mass ratio is invariant and equals 2", abs(ratios_k["projective_gap_over_mass"] - 2.0) < 1e-12, ratios_k["projective_gap_over_mass"]))
    checks.append(ok("M^2 scaled back is invariant", abs(ratios_k["M_phys_squared_over_kappa_squared"] - ratios_1["M_phys_squared_over_kappa_squared"]) < 1e-12, ratios_k))
    checks.append(ok("zeta p=2 scaled back is invariant", abs(ratios_k["zeta_p2_scaled_back"] - ratios_1["zeta_p2_scaled_back"]) < 1e-18, ratios_k))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXXXIX",
        "title": "Multi-Anchor Calibration Consistency Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "dimensionless_kernel": {
            "M2": "5049/4",
            "M": "sqrt(5049)/2",
            "projective_gap": "sqrt(5049)",
            "projective_gap_over_M": 2,
        },
        "anchor_formulas": {
            "mass": "kappa=M_phys/M",
            "heat": "kappa=sqrt(-log(H/2)/(M2 tau_phys))",
            "spinor_trace": "kappa=arcosh(T/2)/(M t_phys)",
            "resolvent": "kappa=sqrt((s^2-2s/R)/M2)",
            "zeta": "kappa=(zeta_dimless(p)/zeta_phys(p))^(1/(2p))",
        },
        "consistent_anchor_packet": packet,
        "recovered_kappas": kappas,
        "consistency_report": report,
        "inconsistent_anchor_packet": bad_packet,
        "inconsistent_report": bad_report,
        "calibration_invariants": ratios_k,
        "architecture_upgrade": (
            "CCCXXXVIII established the unit map.  CCCXXXIX makes it falsifiable: "
            "independent anchors must return the same kappa, while dimensionless ratios "
            "remain invariant under calibration gauge."
        ),
        "theorem": (
            "For the one-sector W33 RG spinor unit map, mass, heat trace, spinor trace, "
            "resolvent trace, and zeta anchors each recover kappa independently.  The "
            "physical interpretation is calibration-consistent iff all recovered kappas "
            "agree within tolerance; otherwise the one-sector unit assignment is falsified."
        ),
        "honesty_boundary": (
            "The compiler proves internal consistency and falsifiability of calibration. "
            "It does not choose a real-world anchor or claim that any specific physical "
            "quantity is the correct anchor."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXXIX_multi_anchor_consistency_results.json"
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
