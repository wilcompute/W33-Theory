#!/usr/bin/env python3
"""
PART CCCXLII -- Anchor-Free Response Identities Compiler
=======================================================

CCCXLI moved empirical comparison from kappa to the kappa-free physical spectral
scale Lambda.  CCCXLII removes even Lambda from the front-facing tests by
writing direct response identities between channels.

For a one-sector W33 RG spinor observable packet, the following recovered scales
must all agree:

    mass^2
    -log(H/2)/tau
    (arcosh(T/2)/t)^2
    s^2 - 2s/R
    (2/zeta_p)^(1/p)
    (gap/2)^2

Equivalently, any one channel predicts every other channel directly.  These are
anchor-free, kappa-free, Lambda-eliminated consistency equations.
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
M2_DIMLESS = DELTA / 4.0

DEFAULT_TAU = 0.001
DEFAULT_T = 0.01
DEFAULT_S = 100.0
DEFAULT_P = 2


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def channels_from_scale(scale: float, tau: float = DEFAULT_TAU, t: float = DEFAULT_T, s: float = DEFAULT_S, p: int = DEFAULT_P) -> Dict[str, Any]:
    """Build physical response channels from Lambda=scale."""
    root = math.sqrt(scale)
    return {
        "mass": root,
        "gap": 2.0 * root,
        "heat_trace": 2.0 * math.exp(-scale * tau),
        "spinor_trace": 2.0 * math.cosh(root * t),
        "resolvent_trace": 2.0 * s / (s * s - scale),
        "zeta": 2.0 / (scale ** p),
        "samples": {"tau": tau, "t": t, "s": s, "p": p},
    }


def recover_scales(packet: Dict[str, Any]) -> Dict[str, float]:
    tau = packet["samples"]["tau"]
    t = packet["samples"]["t"]
    s = packet["samples"]["s"]
    p = packet["samples"]["p"]
    return {
        "mass": packet["mass"] ** 2,
        "gap": (packet["gap"] / 2.0) ** 2,
        "heat_trace": -math.log(packet["heat_trace"] / 2.0) / tau,
        "spinor_trace": (math.acosh(packet["spinor_trace"] / 2.0) / t) ** 2,
        "resolvent_trace": s * s - 2.0 * s / packet["resolvent_trace"],
        "zeta": (2.0 / packet["zeta"]) ** (1.0 / p),
    }


def scale_report(scales: Dict[str, float], tolerance: float = 1e-8) -> Dict[str, Any]:
    values = list(scales.values())
    mu = mean(values)
    max_dev = max(abs(v - mu) for v in values)
    rel = max_dev / abs(mu) if mu else float("inf")
    return {
        "scales": scales,
        "mean_scale": mu,
        "std_scale": pstdev(values),
        "max_abs_deviation": max_dev,
        "max_relative_deviation": rel,
        "tolerance": tolerance,
        "consistent": max_dev <= tolerance,
    }


def predict_from_heat(H: float, tau: float, t: float, s: float, p: int) -> Dict[str, float]:
    scale = -math.log(H / 2.0) / tau
    return channels_from_scale(scale, tau=tau, t=t, s=s, p=p)


def predict_from_spinor(T: float, tau: float, t: float, s: float, p: int) -> Dict[str, float]:
    scale = (math.acosh(T / 2.0) / t) ** 2
    return channels_from_scale(scale, tau=tau, t=t, s=s, p=p)


def predict_from_resolvent(R: float, tau: float, t: float, s: float, p: int) -> Dict[str, float]:
    scale = s * s - 2.0 * s / R
    return channels_from_scale(scale, tau=tau, t=t, s=s, p=p)


def predict_from_zeta(zeta: float, tau: float, t: float, s: float, p: int) -> Dict[str, float]:
    scale = (2.0 / zeta) ** (1.0 / p)
    return channels_from_scale(scale, tau=tau, t=t, s=s, p=p)


def predict_from_mass(mass: float, tau: float, t: float, s: float, p: int) -> Dict[str, float]:
    return channels_from_scale(mass * mass, tau=tau, t=t, s=s, p=p)


def predict_from_gap(gap: float, tau: float, t: float, s: float, p: int) -> Dict[str, float]:
    return channels_from_scale((gap / 2.0) ** 2, tau=tau, t=t, s=s, p=p)


def pairwise_identity_residuals(packet: Dict[str, Any]) -> Dict[str, float]:
    scales = recover_scales(packet)
    h = scales["heat_trace"]
    return {key + "_minus_heat_scale": value - h for key, value in scales.items() if key != "heat_trace"}


def corrupt_packet(packet: Dict[str, Any], key: str, factor: float) -> Dict[str, Any]:
    out = json.loads(json.dumps(packet))
    out[key] *= factor
    return out


def max_prediction_difference(pred: Dict[str, Any], ref: Dict[str, Any]) -> float:
    keys = ["mass", "gap", "heat_trace", "spinor_trace", "resolvent_trace", "zeta"]
    return max(abs(pred[key] - ref[key]) for key in keys)


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    kappa = 7.0 / 3.0
    scale = kappa * kappa * M2_DIMLESS
    packet = channels_from_scale(scale)
    scales = recover_scales(packet)
    report = scale_report(scales)
    residuals = pairwise_identity_residuals(packet)
    corrupted = corrupt_packet(packet, "spinor_trace", 1.001)
    corrupted_report = scale_report(recover_scales(corrupted))
    tau = packet["samples"]["tau"]
    t = packet["samples"]["t"]
    s = packet["samples"]["s"]
    p = packet["samples"]["p"]
    predictions = {
        "mass": predict_from_mass(packet["mass"], tau, t, s, p),
        "gap": predict_from_gap(packet["gap"], tau, t, s, p),
        "heat_trace": predict_from_heat(packet["heat_trace"], tau, t, s, p),
        "spinor_trace": predict_from_spinor(packet["spinor_trace"], tau, t, s, p),
        "resolvent_trace": predict_from_resolvent(packet["resolvent_trace"], tau, t, s, p),
        "zeta": predict_from_zeta(packet["zeta"], tau, t, s, p),
    }
    max_diffs = {key: max_prediction_difference(value, packet) for key, value in predictions.items()}

    checks.append(ok("dimensionless W33 M2=5049/4", abs(M2_DIMLESS - 5049.0 / 4.0) < 1e-15, M2_DIMLESS))
    checks.append(ok("all channels recover same scale", report["consistent"] is True, report))
    checks.append(ok("mass scale equals heat scale", abs(scales["mass"] - scales["heat_trace"]) < 1e-8, scales))
    checks.append(ok("gap scale equals heat scale", abs(scales["gap"] - scales["heat_trace"]) < 1e-8, scales))
    checks.append(ok("spinor scale equals heat scale", abs(scales["spinor_trace"] - scales["heat_trace"]) < 1e-8, scales))
    checks.append(ok("resolvent scale equals heat scale", abs(scales["resolvent_trace"] - scales["heat_trace"]) < 1e-8, scales))
    checks.append(ok("zeta scale equals heat scale", abs(scales["zeta"] - scales["heat_trace"]) < 1e-8, scales))
    checks.append(ok("all pairwise residuals near zero", max(abs(v) for v in residuals.values()) < 1e-8, residuals))
    checks.append(ok("corrupted packet fails anchor-free identities", corrupted_report["consistent"] is False, corrupted_report))
    checks.append(ok("mass predicts all other channels", max_diffs["mass"] < 1e-10, max_diffs["mass"]))
    checks.append(ok("heat predicts all other channels", max_diffs["heat_trace"] < 1e-10, max_diffs["heat_trace"]))
    checks.append(ok("spinor predicts all other channels", max_diffs["spinor_trace"] < 1e-10, max_diffs["spinor_trace"]))
    checks.append(ok("resolvent predicts all other channels", max_diffs["resolvent_trace"] < 1e-10, max_diffs["resolvent_trace"]))
    checks.append(ok("zeta predicts all other channels", max_diffs["zeta"] < 1e-10, max_diffs["zeta"]))
    checks.append(ok("gap/mass identity holds", abs(packet["gap"] - 2.0 * packet["mass"]) < 1e-12, {"gap": packet["gap"], "mass": packet["mass"]}))

    verified = all(check["passed"] for check in checks)

    identities = {
        "mass_heat": "mass^2 = -log(H/2)/tau",
        "gap_mass": "gap = 2 mass",
        "spinor_heat": "(arcosh(T/2)/t)^2 = -log(H/2)/tau",
        "resolvent_heat": "s^2 - 2s/R = -log(H/2)/tau",
        "zeta_heat": "(2/zeta_p)^(1/p) = -log(H/2)/tau",
        "all_channel_scale": "mass^2=(gap/2)^2=-log(H/2)/tau=(arcosh(T/2)/t)^2=s^2-2s/R=(2/zeta_p)^(1/p)",
    }

    return {
        "part": "CCCXLII",
        "title": "Anchor-Free Response Identities Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "dimensionless_kernel": {
            "M2": "5049/4",
            "role": "internal W33 scale; not needed for front-facing channel identities until kappa is reconstructed",
        },
        "sample_packet": packet,
        "recovered_channel_scales": scales,
        "scale_report": report,
        "pairwise_identity_residuals": residuals,
        "corrupted_report": corrupted_report,
        "anchor_free_identities": identities,
        "single_channel_prediction_max_diffs": max_diffs,
        "architecture_upgrade": (
            "CCCXLI made Lambda the kappa-free comparison object.  CCCXLII eliminates "
            "Lambda from the front-facing tests: every response channel must satisfy direct "
            "anchor-free identities against every other channel."
        ),
        "theorem": (
            "For a one-sector W33 observable packet, mass, gap, heat trace, spinor trace, "
            "resolvent trace, and zeta data are mutually constrained by direct response "
            "identities.  Any one channel predicts all others; violation of these identities "
            "falsifies the one-sector observable interpretation without choosing kappa or Lambda."
        ),
        "honesty_boundary": (
            "These are exact one-sector response identities.  They become empirical only after "
            "specific physical measurements are identified with the finite response channels."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXLII_anchor_free_response_identities_results.json"
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
