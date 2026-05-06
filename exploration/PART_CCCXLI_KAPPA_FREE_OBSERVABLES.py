#!/usr/bin/env python3
"""
PART CCCXLI -- Kappa-Free Observable Consistency Compiler
=========================================================

CCCXL made the unit map predictive once a calibration constant kappa is chosen.
CCCXLI eliminates kappa from the empirical side.

All one-sector physical response channels depend on the single physical spectral
scale

    Lambda = kappa^2 M^2,
    M^2 = 5049/4.

Thus the channels recover Lambda directly:

    mass:        Lambda = M_phys^2
    heat:        Lambda = -log(H/2)/tau
    spinor:      Lambda = (arcosh(T/2)/t)^2
    resolvent:   Lambda = s^2 - 2s/R
    zeta:        Lambda = (2/zeta_p)^(1/p)

The one-sector interpretation is kappa-free falsifiable iff all recovered
Lambda values agree.  After Lambda is recovered, kappa is obtained only at the
last step by

    kappa = sqrt(Lambda / (5049/4)).

This is the empirical scale layer: observable channels test one Lambda before
any convention about dimensionless W33 units is invoked.
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


def Lambda_from_kappa(kappa: float) -> float:
    return (kappa * kappa) * M2


def channels_from_Lambda(Lambda: float, tau: float = DEFAULT_TAU, t: float = DEFAULT_T, s: float = DEFAULT_S, p: int = DEFAULT_P) -> Dict[str, Any]:
    return {
        "Lambda": Lambda,
        "mass": math.sqrt(Lambda),
        "projective_gap": 2.0 * math.sqrt(Lambda),
        "heat_trace": 2.0 * math.exp(-Lambda * tau),
        "spinor_trace": 2.0 * math.cosh(math.sqrt(Lambda) * t),
        "resolvent_trace": 2.0 * s / (s * s - Lambda),
        "zeta": 2.0 / (Lambda ** p),
        "samples": {"tau": tau, "t": t, "s": s, "p": p},
    }


def recover_Lambda_from_mass(M_phys: float) -> float:
    return M_phys * M_phys


def recover_Lambda_from_heat(tau: float, H: float) -> float:
    return -math.log(H / 2.0) / tau


def recover_Lambda_from_spinor(t: float, T: float) -> float:
    return (math.acosh(T / 2.0) / t) ** 2


def recover_Lambda_from_resolvent(s: float, R: float) -> float:
    return s * s - 2.0 * s / R


def recover_Lambda_from_zeta(p: int, zeta: float) -> float:
    return (2.0 / zeta) ** (1.0 / p)


def recover_all_Lambdas(channels: Dict[str, Any]) -> Dict[str, float]:
    tau = channels["samples"]["tau"]
    t = channels["samples"]["t"]
    s = channels["samples"]["s"]
    p = channels["samples"]["p"]
    return {
        "mass": recover_Lambda_from_mass(channels["mass"]),
        "heat_trace": recover_Lambda_from_heat(tau, channels["heat_trace"]),
        "spinor_trace": recover_Lambda_from_spinor(t, channels["spinor_trace"]),
        "resolvent_trace": recover_Lambda_from_resolvent(s, channels["resolvent_trace"]),
        "zeta": recover_Lambda_from_zeta(p, channels["zeta"]),
    }


def consistency_report(values: Dict[str, float], tolerance: float = 1e-8) -> Dict[str, Any]:
    vals = list(values.values())
    mu = mean(vals)
    max_dev = max(abs(v - mu) for v in vals)
    rel_dev = max_dev / abs(mu) if mu != 0 else float("inf")
    return {
        "values": values,
        "mean_Lambda": mu,
        "std_Lambda": pstdev(vals),
        "max_abs_deviation": max_dev,
        "max_relative_deviation": rel_dev,
        "tolerance": tolerance,
        "consistent": max_dev <= tolerance,
    }


def kappa_from_Lambda(Lambda: float) -> float:
    return math.sqrt(Lambda / M2)


def corrupt_channel(channels: Dict[str, Any], channel: str, factor: float) -> Dict[str, Any]:
    out = json.loads(json.dumps(channels))
    out[channel] *= factor
    return out


def kappa_free_predictions_from_one_channel(anchor_type: str, value: float, *, tau: float = DEFAULT_TAU, t: float = DEFAULT_T, s: float = DEFAULT_S, p: int = DEFAULT_P) -> Dict[str, Any]:
    if anchor_type == "mass":
        Lambda = recover_Lambda_from_mass(value)
    elif anchor_type == "heat_trace":
        Lambda = recover_Lambda_from_heat(tau, value)
    elif anchor_type == "spinor_trace":
        Lambda = recover_Lambda_from_spinor(t, value)
    elif anchor_type == "resolvent_trace":
        Lambda = recover_Lambda_from_resolvent(s, value)
    elif anchor_type == "zeta":
        Lambda = recover_Lambda_from_zeta(p, value)
    else:
        raise ValueError(f"unknown anchor type: {anchor_type}")
    predictions = channels_from_Lambda(Lambda, tau=tau, t=t, s=s, p=p)
    predictions["recovered_kappa"] = kappa_from_Lambda(Lambda)
    return predictions


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    kappa = 7.0 / 3.0
    Lambda = Lambda_from_kappa(kappa)
    channels = channels_from_Lambda(Lambda)
    recovered = recover_all_Lambdas(channels)
    report = consistency_report(recovered)
    corrupted = corrupt_channel(channels, "heat_trace", 1.01)
    corrupted_report = consistency_report(recover_all_Lambdas(corrupted))
    one_anchor_predictions = {
        key: kappa_free_predictions_from_one_channel(key, channels[key])
        for key in ["mass", "heat_trace", "spinor_trace", "resolvent_trace", "zeta"]
    }
    max_prediction_diff = max(
        abs(one_anchor_predictions[key]["Lambda"] - Lambda)
        for key in one_anchor_predictions
    )

    checks.append(ok("dimensionless M2=5049/4", abs(M2 - 5049.0 / 4.0) < 1e-15, M2))
    checks.append(ok("Lambda=kappa^2 M2 for sample", abs(Lambda - (kappa * kappa * M2)) < 1e-12, Lambda))
    checks.append(ok("mass channel recovers Lambda", abs(recovered["mass"] - Lambda) < 1e-9, recovered["mass"]))
    checks.append(ok("heat channel recovers Lambda", abs(recovered["heat_trace"] - Lambda) < 1e-9, recovered["heat_trace"]))
    checks.append(ok("spinor channel recovers Lambda", abs(recovered["spinor_trace"] - Lambda) < 1e-9, recovered["spinor_trace"]))
    checks.append(ok("resolvent channel recovers Lambda", abs(recovered["resolvent_trace"] - Lambda) < 1e-9, recovered["resolvent_trace"]))
    checks.append(ok("zeta channel recovers Lambda", abs(recovered["zeta"] - Lambda) < 1e-9, recovered["zeta"]))
    checks.append(ok("consistent Lambda packet passes", report["consistent"] is True, report))
    checks.append(ok("corrupted Lambda packet fails", corrupted_report["consistent"] is False, corrupted_report))
    checks.append(ok("kappa recovered from Lambda", abs(kappa_from_Lambda(Lambda) - kappa) < 1e-12, kappa_from_Lambda(Lambda)))
    checks.append(ok("one-channel kappa-free predictions recover same Lambda", max_prediction_diff < 1e-9, max_prediction_diff))
    checks.append(ok("projective gap is 2 sqrt Lambda", abs(channels["projective_gap"] - 2.0 * math.sqrt(Lambda)) < 1e-12, channels["projective_gap"]))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXLI",
        "title": "Kappa-Free Observable Consistency Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "dimensionless_kernel": {
            "M2": "5049/4",
            "M": "sqrt(5049)/2",
            "kappa_relation": "Lambda=kappa^2 M2",
            "kappa_recovery": "kappa=sqrt(Lambda/(5049/4))",
        },
        "kappa_free_scale": {
            "symbol": "Lambda",
            "meaning": "physical squared spectral scale",
            "sample_Lambda": Lambda,
            "sample_kappa": kappa,
        },
        "channel_formulas": {
            "mass": "Lambda=M_phys^2",
            "heat_trace": "Lambda=-log(H/2)/tau",
            "spinor_trace": "Lambda=(arcosh(T/2)/t)^2",
            "resolvent_trace": "Lambda=s^2-2s/R",
            "zeta": "Lambda=(2/zeta_p)^(1/p)",
        },
        "sample_channels": channels,
        "recovered_Lambdas": recovered,
        "consistency_report": report,
        "corrupted_report": corrupted_report,
        "one_anchor_prediction_tables": one_anchor_predictions,
        "architecture_upgrade": (
            "CCCXL made kappa-calibrated prediction tables.  CCCXLI eliminates kappa "
            "from the empirical comparison: all channels must first agree on Lambda, "
            "then kappa is recovered only as sqrt(Lambda/M2)."
        ),
        "theorem": (
            "For the one-sector W33 unit map, the observable response channels depend "
            "on the single physical spectral scale Lambda=kappa^2M^2.  Mass, heat trace, "
            "spinor trace, resolvent trace, and zeta data independently recover Lambda. "
            "Agreement of these Lambda values is a kappa-free falsification test; kappa "
            "is recovered afterward by sqrt(Lambda/(5049/4))."
        ),
        "honesty_boundary": (
            "This is still a one-sector observable model.  Real physical use requires "
            "identifying which measured channels correspond to these finite traces."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXLI_kappa_free_observables_results.json"
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
