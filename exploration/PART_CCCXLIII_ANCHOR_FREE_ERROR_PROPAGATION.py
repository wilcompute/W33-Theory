#!/usr/bin/env python3
"""
PART CCCXLIII -- Anchor-Free Error Propagation Compiler
======================================================

CCCXLII gave exact anchor-free response identities:

    m^2 = (g/2)^2 = -log(H/2)/tau
        = (arcosh(T/2)/t)^2 = s^2 - 2s/R = (2/zeta_p)^(1/p).

CCCXLIII makes those identities usable for empirical data with uncertainty.  It
computes the first-order sensitivity of the recovered squared scale X to each
channel and builds a weighted consensus estimator.

Recovered scale X and derivatives:

    X_m    = m^2,                         dX/dm = 2m
    X_g    = (g/2)^2,                     dX/dg = g/2
    X_H    = -log(H/2)/tau,               dX/dH = -1/(tau H)
    X_T    = (acosh(T/2)/t)^2,            dX/dT = acosh(T/2)/(t^2 sqrt((T/2)^2-1))
    X_R    = s^2 - 2s/R,                 dX/dR = 2s/R^2
    X_zeta = (2/zeta)^(1/p),              dX/dzeta = -X/(p zeta)

The output is a finite empirical test object: channel estimates, propagated
uncertainties, weighted mean, chi-square, and residual z-scores.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

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


def default_uncertainties(packet: Dict[str, Any], rel: float = 1e-6) -> Dict[str, float]:
    return {key: abs(packet[key]) * rel for key in ["mass", "gap", "heat_trace", "spinor_trace", "resolvent_trace", "zeta"]}


def scale_from_channel(name: str, value: float, samples: Dict[str, Any]) -> float:
    tau = samples["tau"]
    t = samples["t"]
    s = samples["s"]
    p = samples["p"]
    if name == "mass":
        return value * value
    if name == "gap":
        return (value / 2.0) ** 2
    if name == "heat_trace":
        return -math.log(value / 2.0) / tau
    if name == "spinor_trace":
        return (math.acosh(value / 2.0) / t) ** 2
    if name == "resolvent_trace":
        return s * s - 2.0 * s / value
    if name == "zeta":
        return (2.0 / value) ** (1.0 / p)
    raise ValueError(f"unknown channel {name}")


def derivative_scale_wrt_channel(name: str, value: float, samples: Dict[str, Any]) -> float:
    tau = samples["tau"]
    t = samples["t"]
    s = samples["s"]
    p = samples["p"]
    if name == "mass":
        return 2.0 * value
    if name == "gap":
        return value / 2.0
    if name == "heat_trace":
        return -1.0 / (tau * value)
    if name == "spinor_trace":
        u = value / 2.0
        return math.acosh(u) / (t * t * math.sqrt(u * u - 1.0))
    if name == "resolvent_trace":
        return 2.0 * s / (value * value)
    if name == "zeta":
        X = scale_from_channel(name, value, samples)
        return -X / (p * value)
    raise ValueError(f"unknown channel {name}")


def channel_estimate(packet: Dict[str, Any], uncertainties: Dict[str, float], name: str) -> Dict[str, float]:
    value = packet[name]
    sigma_value = uncertainties[name]
    samples = packet["samples"]
    X = scale_from_channel(name, value, samples)
    deriv = derivative_scale_wrt_channel(name, value, samples)
    sigma_X = abs(deriv) * sigma_value
    return {
        "channel": name,
        "value": value,
        "sigma_value": sigma_value,
        "scale_estimate": X,
        "derivative": deriv,
        "sigma_scale": sigma_X,
        "weight": 1.0 / (sigma_X * sigma_X),
    }


def all_channel_estimates(packet: Dict[str, Any], uncertainties: Dict[str, float]) -> Dict[str, Dict[str, float]]:
    return {name: channel_estimate(packet, uncertainties, name) for name in ["mass", "gap", "heat_trace", "spinor_trace", "resolvent_trace", "zeta"]}


def weighted_consensus(estimates: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
    weights = {name: est["weight"] for name, est in estimates.items()}
    total_weight = sum(weights.values())
    mean = sum(estimates[name]["scale_estimate"] * weights[name] for name in estimates) / total_weight
    sigma_mean = math.sqrt(1.0 / total_weight)
    residuals = {name: estimates[name]["scale_estimate"] - mean for name in estimates}
    z_scores = {name: residuals[name] / estimates[name]["sigma_scale"] for name in estimates}
    chi_square = sum(z_scores[name] ** 2 for name in estimates)
    dof = max(len(estimates) - 1, 1)
    reduced_chi_square = chi_square / dof
    return {
        "weighted_scale": mean,
        "sigma_weighted_scale": sigma_mean,
        "residuals": residuals,
        "z_scores": z_scores,
        "chi_square": chi_square,
        "degrees_of_freedom": dof,
        "reduced_chi_square": reduced_chi_square,
        "max_abs_z": max(abs(z) for z in z_scores.values()),
        "passes_3sigma_channel_test": max(abs(z) for z in z_scores.values()) <= 3.0,
    }


def perturb_packet(packet: Dict[str, Any], perturbations: Dict[str, float]) -> Dict[str, Any]:
    out = json.loads(json.dumps(packet))
    for key, rel_delta in perturbations.items():
        out[key] *= 1.0 + rel_delta
    return out


def finite_difference_derivative(name: str, value: float, samples: Dict[str, Any], h_rel: float = 1e-6) -> float:
    h = abs(value) * h_rel if value != 0 else h_rel
    return (scale_from_channel(name, value + h, samples) - scale_from_channel(name, value - h, samples)) / (2.0 * h)


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    kappa = 7.0 / 3.0
    true_scale = kappa * kappa * M2_DIMLESS
    clean_packet = channels_from_scale(true_scale)
    uncertainties = default_uncertainties(clean_packet, rel=1e-6)
    clean_estimates = all_channel_estimates(clean_packet, uncertainties)
    clean_consensus = weighted_consensus(clean_estimates)

    noisy_packet = perturb_packet(clean_packet, {
        "mass": 0.4e-6,
        "gap": -0.3e-6,
        "heat_trace": 0.2e-6,
        "spinor_trace": -0.1e-6,
        "resolvent_trace": 0.25e-6,
        "zeta": -0.35e-6,
    })
    noisy_estimates = all_channel_estimates(noisy_packet, uncertainties)
    noisy_consensus = weighted_consensus(noisy_estimates)

    bad_packet = perturb_packet(clean_packet, {"spinor_trace": 100e-6})
    bad_estimates = all_channel_estimates(bad_packet, uncertainties)
    bad_consensus = weighted_consensus(bad_estimates)

    derivative_checks = {
        name: {
            "analytic": derivative_scale_wrt_channel(name, clean_packet[name], clean_packet["samples"]),
            "finite_difference": finite_difference_derivative(name, clean_packet[name], clean_packet["samples"]),
        }
        for name in ["mass", "gap", "heat_trace", "spinor_trace", "resolvent_trace", "zeta"]
    }

    checks.append(ok("dimensionless W33 M2=5049/4", abs(M2_DIMLESS - 5049.0 / 4.0) < 1e-15, M2_DIMLESS))
    checks.append(ok("clean weighted scale recovers true scale", abs(clean_consensus["weighted_scale"] - true_scale) < 1e-8, clean_consensus["weighted_scale"]))
    checks.append(ok("clean packet passes 3sigma test", clean_consensus["passes_3sigma_channel_test"] is True, clean_consensus["max_abs_z"]))
    checks.append(ok("small noisy packet passes 3sigma test", noisy_consensus["passes_3sigma_channel_test"] is True, noisy_consensus["max_abs_z"]))
    checks.append(ok("bad packet fails 3sigma test", bad_consensus["passes_3sigma_channel_test"] is False, bad_consensus["max_abs_z"]))
    checks.append(ok("mass derivative matches finite difference", abs(derivative_checks["mass"]["analytic"] - derivative_checks["mass"]["finite_difference"]) < 1e-5, derivative_checks["mass"]))
    checks.append(ok("gap derivative matches finite difference", abs(derivative_checks["gap"]["analytic"] - derivative_checks["gap"]["finite_difference"]) < 1e-5, derivative_checks["gap"]))
    checks.append(ok("heat derivative matches finite difference", abs(derivative_checks["heat_trace"]["analytic"] - derivative_checks["heat_trace"]["finite_difference"]) / abs(derivative_checks["heat_trace"]["analytic"]) < 1e-6, derivative_checks["heat_trace"]))
    checks.append(ok("spinor derivative matches finite difference", abs(derivative_checks["spinor_trace"]["analytic"] - derivative_checks["spinor_trace"]["finite_difference"]) / abs(derivative_checks["spinor_trace"]["analytic"]) < 1e-6, derivative_checks["spinor_trace"]))
    checks.append(ok("resolvent derivative matches finite difference", abs(derivative_checks["resolvent_trace"]["analytic"] - derivative_checks["resolvent_trace"]["finite_difference"]) / abs(derivative_checks["resolvent_trace"]["analytic"]) < 1e-6, derivative_checks["resolvent_trace"]))
    checks.append(ok("zeta derivative matches finite difference", abs(derivative_checks["zeta"]["analytic"] - derivative_checks["zeta"]["finite_difference"]) / abs(derivative_checks["zeta"]["analytic"]) < 1e-6, derivative_checks["zeta"]))

    verified = all(check["passed"] for check in checks)

    derivative_formulas = {
        "mass": "dX/dm=2m",
        "gap": "dX/dg=g/2",
        "heat_trace": "dX/dH=-1/(tau H)",
        "spinor_trace": "dX/dT=acosh(T/2)/(t^2 sqrt((T/2)^2-1))",
        "resolvent_trace": "dX/dR=2s/R^2",
        "zeta": "dX/dzeta=-X/(p zeta)",
    }

    return {
        "part": "CCCXLIII",
        "title": "Anchor-Free Error Propagation Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "true_scale": true_scale,
        "dimensionless_kernel": {
            "M2": "5049/4",
            "role": "internal W33 dimensionless scale; physical packets estimate X=kappa^2 M2",
        },
        "derivative_formulas": derivative_formulas,
        "clean_packet": clean_packet,
        "uncertainties": uncertainties,
        "clean_channel_estimates": clean_estimates,
        "clean_consensus": clean_consensus,
        "noisy_packet": noisy_packet,
        "noisy_consensus": noisy_consensus,
        "bad_packet": bad_packet,
        "bad_consensus": bad_consensus,
        "derivative_checks": derivative_checks,
        "architecture_upgrade": (
            "CCCXLII gave exact anchor-free identities.  CCCXLIII turns them into an "
            "empirical error-propagation protocol with channel sensitivities, weighted "
            "scale estimates, residual z-scores, and chi-square diagnostics."
        ),
        "theorem": (
            "For the one-sector W33 response packet, every channel estimates the same "
            "squared scale X.  First-order uncertainty propagation gives sigma_X=|dX/dy|sigma_y "
            "for each channel, enabling a weighted consensus estimate and residual z-score "
            "test.  A packet passes only if the channel estimates agree within propagated "
            "uncertainty."
        ),
        "honesty_boundary": (
            "This is first-order Gaussian-style propagation.  Real experimental use must "
            "replace synthetic uncertainties with actual measurement models and correlations."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXLIII_anchor_free_error_propagation_results.json"
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
