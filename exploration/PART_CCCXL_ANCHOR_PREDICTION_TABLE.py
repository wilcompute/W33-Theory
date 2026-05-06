#!/usr/bin/env python3
"""
PART CCCXL -- Anchor Prediction Table Compiler
==============================================

CCCXXXIX made the one-sector unit map falsifiable: all independent anchors must
recover the same calibration constant kappa.  CCCXL turns that into prediction.

Given exactly one anchor, the finite W33 RG spinor architecture predicts all
other response channels:

    M_phys = kappa M,
    H(tau) = 2 exp(-kappa^2 M^2 tau),
    T(t)   = 2 cosh(kappa M t),
    R(s)   = 2s/(s^2-kappa^2 M^2),
    zeta_p = kappa^(-2p) 2(M^2)^(-p).

This compiler builds prediction tables from each possible anchor type and
verifies round-trip consistency.  It does not select a real-world anchor; it
provides the exact deterministic prediction machinery once an anchor is chosen.
"""

from __future__ import annotations

import json
import math
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

DEFAULT_TAU = 0.001
DEFAULT_T = 0.01
DEFAULT_S = 100.0
DEFAULT_P = 2


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def predictions_from_kappa(kappa: float, tau: float = DEFAULT_TAU, t: float = DEFAULT_T, s: float = DEFAULT_S, p: int = DEFAULT_P) -> Dict[str, Any]:
    mass = kappa * M
    heat = 2.0 * math.exp(-(kappa * kappa) * M2 * tau)
    spinor = 2.0 * math.cosh(kappa * M * t)
    resolvent = 2.0 * s / (s * s - (kappa * kappa) * M2)
    zeta_dimless = 2.0 / (M2 ** p)
    zeta = (kappa ** (-2 * p)) * zeta_dimless
    projective_gap = 2.0 * mass
    return {
        "kappa": kappa,
        "samples": {"tau": tau, "t": t, "s": s, "p": p},
        "mass": mass,
        "projective_gap": projective_gap,
        "projective_gap_over_mass": projective_gap / mass,
        "heat_trace": heat,
        "spinor_trace": spinor,
        "resolvent_trace": resolvent,
        "zeta": zeta,
    }


def kappa_from_anchor(anchor_type: str, value: float, *, tau: float = DEFAULT_TAU, t: float = DEFAULT_T, s: float = DEFAULT_S, p: int = DEFAULT_P) -> float:
    if anchor_type == "mass":
        return value / M
    if anchor_type == "heat_trace":
        return math.sqrt(-math.log(value / 2.0) / (M2 * tau))
    if anchor_type == "spinor_trace":
        return math.acosh(value / 2.0) / (M * t)
    if anchor_type == "resolvent_trace":
        return math.sqrt((s * s - 2.0 * s / value) / M2)
    if anchor_type == "zeta":
        zeta_dimless = 2.0 / (M2 ** p)
        return (zeta_dimless / value) ** (1.0 / (2.0 * p))
    raise ValueError(f"unknown anchor_type: {anchor_type}")


def prediction_table_from_anchor(anchor_type: str, value: float, *, tau: float = DEFAULT_TAU, t: float = DEFAULT_T, s: float = DEFAULT_S, p: int = DEFAULT_P) -> Dict[str, Any]:
    kappa = kappa_from_anchor(anchor_type, value, tau=tau, t=t, s=s, p=p)
    predictions = predictions_from_kappa(kappa, tau=tau, t=t, s=s, p=p)
    recovered = {
        "mass": kappa_from_anchor("mass", predictions["mass"], tau=tau, t=t, s=s, p=p),
        "heat_trace": kappa_from_anchor("heat_trace", predictions["heat_trace"], tau=tau, t=t, s=s, p=p),
        "spinor_trace": kappa_from_anchor("spinor_trace", predictions["spinor_trace"], tau=tau, t=t, s=s, p=p),
        "resolvent_trace": kappa_from_anchor("resolvent_trace", predictions["resolvent_trace"], tau=tau, t=t, s=s, p=p),
        "zeta": kappa_from_anchor("zeta", predictions["zeta"], tau=tau, t=t, s=s, p=p),
    }
    values = list(recovered.values())
    return {
        "input_anchor": {"type": anchor_type, "value": value},
        "recovered_kappa_from_anchor": kappa,
        "predictions": predictions,
        "round_trip_recovered_kappas": recovered,
        "round_trip_mean": mean(values),
        "round_trip_std": pstdev(values),
        "round_trip_max_deviation": max(abs(v - kappa) for v in values),
    }


def make_all_anchor_tables(kappa: float) -> Dict[str, Dict[str, Any]]:
    base = predictions_from_kappa(kappa)
    anchors = {
        "mass": base["mass"],
        "heat_trace": base["heat_trace"],
        "spinor_trace": base["spinor_trace"],
        "resolvent_trace": base["resolvent_trace"],
        "zeta": base["zeta"],
    }
    return {anchor_type: prediction_table_from_anchor(anchor_type, value) for anchor_type, value in anchors.items()}


def compare_prediction_tables(tables: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    keys = ["mass", "projective_gap", "heat_trace", "spinor_trace", "resolvent_trace", "zeta"]
    reference = next(iter(tables.values()))["predictions"]
    max_diffs = {}
    for key in keys:
        max_diffs[key] = max(abs(table["predictions"][key] - reference[key]) for table in tables.values())
    return {
        "reference_anchor": next(iter(tables.keys())),
        "max_prediction_differences": max_diffs,
        "all_tables_agree": all(diff < 1e-10 for diff in max_diffs.values()),
    }


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    kappa = 7.0 / 3.0
    base_predictions = predictions_from_kappa(kappa)
    tables = make_all_anchor_tables(kappa)
    comparison = compare_prediction_tables(tables)

    checks.append(ok("dimensionless mass shell M2=5049/4", abs(M2 - 5049.0 / 4.0) < 1e-15, M2))
    checks.append(ok("projective gap/mass prediction is 2", abs(base_predictions["projective_gap_over_mass"] - 2.0) < 1e-12, base_predictions["projective_gap_over_mass"]))
    checks.append(ok("mass anchor round-trips", tables["mass"]["round_trip_max_deviation"] < 1e-12, tables["mass"]["round_trip_max_deviation"]))
    checks.append(ok("heat anchor round-trips", tables["heat_trace"]["round_trip_max_deviation"] < 1e-12, tables["heat_trace"]["round_trip_max_deviation"]))
    checks.append(ok("spinor anchor round-trips", tables["spinor_trace"]["round_trip_max_deviation"] < 1e-12, tables["spinor_trace"]["round_trip_max_deviation"]))
    checks.append(ok("resolvent anchor round-trips", tables["resolvent_trace"]["round_trip_max_deviation"] < 1e-12, tables["resolvent_trace"]["round_trip_max_deviation"]))
    checks.append(ok("zeta anchor round-trips", tables["zeta"]["round_trip_max_deviation"] < 1e-12, tables["zeta"]["round_trip_max_deviation"]))
    checks.append(ok("all anchor prediction tables agree", comparison["all_tables_agree"] is True, comparison["max_prediction_differences"]))
    checks.append(ok("predicted heat trace is positive", base_predictions["heat_trace"] > 0, base_predictions["heat_trace"]))
    checks.append(ok("predicted spinor trace is at least 2", base_predictions["spinor_trace"] >= 2, base_predictions["spinor_trace"]))
    checks.append(ok("predicted zeta is positive", base_predictions["zeta"] > 0, base_predictions["zeta"]))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXL",
        "title": "Anchor Prediction Table Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "dimensionless_kernel": {
            "M2": "5049/4",
            "M": "sqrt(5049)/2",
            "projective_gap_over_M": 2,
        },
        "prediction_formulas": {
            "mass": "M_phys=kappa M",
            "projective_gap": "gap_phys=2 M_phys",
            "heat_trace": "H(tau)=2 exp(-kappa^2 M^2 tau)",
            "spinor_trace": "T(t)=2 cosh(kappa M t)",
            "resolvent_trace": "R(s)=2s/(s^2-kappa^2 M^2)",
            "zeta": "zeta_phys(p)=kappa^(-2p) 2(M^2)^(-p)",
        },
        "sample_kappa": kappa,
        "sample_predictions": base_predictions,
        "prediction_tables_by_anchor": tables,
        "table_comparison": comparison,
        "architecture_upgrade": (
            "CCCXXXIX made calibration falsifiable.  CCCXL makes it predictive: once "
            "any one anchor fixes kappa, the finite architecture deterministically predicts "
            "mass, projective gap, heat trace, spinor trace, resolvent trace, and zeta responses."
        ),
        "theorem": (
            "For the one-sector W33 unit map, any single valid anchor determines kappa. "
            "Once kappa is fixed, every other response channel is fixed by closed formulas. "
            "Anchor tables generated from mass, heat, spinor-trace, resolvent, or zeta anchors "
            "must agree; disagreement is a falsification of the one-sector interpretation."
        ),
        "honesty_boundary": (
            "This compiler produces deterministic prediction tables conditional on a chosen anchor. "
            "It does not claim which physical observable should be used as the real anchor."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXL_anchor_prediction_table_results.json"
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
