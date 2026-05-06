#!/usr/bin/env python3
"""
PART CCCXLIV -- Correlated Covariance Fit Compiler
==================================================

CCCXLIII turned anchor-free response identities into first-order independent
error propagation.  CCCXLIV upgrades the empirical layer to correlated
covariance fitting.

Real response channels may share systematic uncertainties.  Therefore the scale
estimates

    X_i = f_i(y_i)

must be fit with a full covariance matrix, not only independent variances.

Given channel-value covariance C_y and Jacobian J=diag(dX_i/dy_i), the scale
covariance is

    C_X = J C_y J^T.

The common-scale generalized least-squares estimator is

    X_hat = (1^T C_X^-1 X)/(1^T C_X^-1 1),
    sigma_hat^2 = 1/(1^T C_X^-1 1),

and the correlated residual diagnostic is

    chi^2 = (X-X_hat 1)^T C_X^-1 (X-X_hat 1),
    dof = N-1.

This is the covariance-ready empirical test layer for the one-sector W33
observable model.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
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

CHANNELS = ["mass", "gap", "heat_trace", "spinor_trace", "resolvent_trace", "zeta"]
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
    raise ValueError(f"unknown channel: {name}")


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
        x = scale_from_channel(name, value, samples)
        return -x / (p * value)
    raise ValueError(f"unknown channel: {name}")


def default_sigmas(packet: Dict[str, Any], rel: float = 1e-6) -> List[float]:
    return [abs(packet[name]) * rel for name in CHANNELS]


def make_value_covariance(sigmas: List[float], rho: float = 0.0, systematic_fraction: float = 0.0) -> List[List[float]]:
    """Build a positive covariance matrix for channel measurements.

    rho gives a common pairwise correlation in the statistical component.
    systematic_fraction adds a rank-one fully correlated contribution.
    """
    n = len(sigmas)
    cov = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            corr = 1.0 if i == j else rho
            cov[i][j] = corr * sigmas[i] * sigmas[j]
            if systematic_fraction:
                cov[i][j] += (systematic_fraction * sigmas[i]) * (systematic_fraction * sigmas[j])
    return cov


def jacobian(packet: Dict[str, Any]) -> List[float]:
    return [derivative_scale_wrt_channel(name, packet[name], packet["samples"]) for name in CHANNELS]


def propagate_covariance(value_cov: List[List[float]], derivs: List[float]) -> List[List[float]]:
    n = len(derivs)
    return [[derivs[i] * value_cov[i][j] * derivs[j] for j in range(n)] for i in range(n)]


def invert_matrix(mat: List[List[float]]) -> List[List[float]]:
    n = len(mat)
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(mat)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-30:
            raise ValueError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            aug[r] = [aug[r][c] - factor * aug[col][c] for c in range(2 * n)]
    return [row[n:] for row in aug]


def mat_vec(mat: List[List[float]], vec: List[float]) -> List[float]:
    return [sum(mat[i][j] * vec[j] for j in range(len(vec))) for i in range(len(mat))]


def dot(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def channel_scale_vector(packet: Dict[str, Any]) -> List[float]:
    return [scale_from_channel(name, packet[name], packet["samples"]) for name in CHANNELS]


def gls_common_scale(scale_values: List[float], scale_cov: List[List[float]]) -> Dict[str, Any]:
    n = len(scale_values)
    ones = [1.0] * n
    inv = invert_matrix(scale_cov)
    inv_ones = mat_vec(inv, ones)
    denom = dot(ones, inv_ones)
    inv_x = mat_vec(inv, scale_values)
    numer = dot(ones, inv_x)
    xhat = numer / denom
    sigma = math.sqrt(1.0 / denom)
    residuals = [x - xhat for x in scale_values]
    inv_res = mat_vec(inv, residuals)
    chi2 = dot(residuals, inv_res)
    dof = n - 1
    # Decorrelated pull proxy: residual divided by marginal sigma.  Full chi2 is authoritative.
    pulls = [residuals[i] / math.sqrt(scale_cov[i][i]) for i in range(n)]
    return {
        "scale_values": scale_values,
        "weighted_scale": xhat,
        "sigma_weighted_scale": sigma,
        "residuals": residuals,
        "pulls_marginal": pulls,
        "max_abs_marginal_pull": max(abs(p) for p in pulls),
        "chi_square": chi2,
        "degrees_of_freedom": dof,
        "reduced_chi_square": chi2 / dof,
        "passes_reduced_chi_square_lt_3": (chi2 / dof) < 3.0,
    }


def correlated_fit(packet: Dict[str, Any], value_cov: List[List[float]]) -> Dict[str, Any]:
    derivs = jacobian(packet)
    scale_cov = propagate_covariance(value_cov, derivs)
    values = channel_scale_vector(packet)
    fit = gls_common_scale(values, scale_cov)
    return {
        "channels": CHANNELS,
        "jacobian": derivs,
        "value_covariance": value_cov,
        "scale_covariance": scale_cov,
        "fit": fit,
    }


def perturb_packet(packet: Dict[str, Any], perturbations: Dict[str, float]) -> Dict[str, Any]:
    out = json.loads(json.dumps(packet))
    for key, rel_delta in perturbations.items():
        out[key] *= 1.0 + rel_delta
    return out


def max_abs_matrix_diff(a: List[List[float]], b: List[List[float]]) -> float:
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a)))


def covariance_is_symmetric(cov: List[List[float]], tol: float = 1e-18) -> bool:
    return max_abs_matrix_diff(cov, [list(row) for row in zip(*cov)]) < tol


def quadratic_form(cov: List[List[float]], vec: List[float]) -> float:
    return dot(vec, mat_vec(cov, vec))


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    kappa = 7.0 / 3.0
    true_scale = kappa * kappa * M2_DIMLESS
    clean_packet = channels_from_scale(true_scale)
    sigmas = default_sigmas(clean_packet, rel=1e-6)
    independent_cov = make_value_covariance(sigmas, rho=0.0)
    correlated_cov = make_value_covariance(sigmas, rho=0.25, systematic_fraction=0.35)

    clean_independent = correlated_fit(clean_packet, independent_cov)
    clean_correlated = correlated_fit(clean_packet, correlated_cov)

    small_noisy_packet = perturb_packet(clean_packet, {
        "mass": 0.25e-6,
        "gap": -0.20e-6,
        "heat_trace": 0.15e-6,
        "spinor_trace": -0.10e-6,
        "resolvent_trace": 0.18e-6,
        "zeta": -0.22e-6,
    })
    noisy_correlated = correlated_fit(small_noisy_packet, correlated_cov)

    bad_packet = perturb_packet(clean_packet, {"spinor_trace": 150e-6})
    bad_correlated = correlated_fit(bad_packet, correlated_cov)

    scale_cov = clean_correlated["scale_covariance"]
    inv_scale_cov = invert_matrix(scale_cov)
    identity_check = [[sum(scale_cov[i][k] * inv_scale_cov[k][j] for k in range(len(CHANNELS))) for j in range(len(CHANNELS))] for i in range(len(CHANNELS))]
    identity = [[1.0 if i == j else 0.0 for j in range(len(CHANNELS))] for i in range(len(CHANNELS))]

    checks.append(ok("dimensionless W33 M2=5049/4", abs(M2_DIMLESS - 5049.0 / 4.0) < 1e-15, M2_DIMLESS))
    checks.append(ok("value covariance is symmetric", covariance_is_symmetric(correlated_cov), True))
    checks.append(ok("scale covariance is symmetric", covariance_is_symmetric(scale_cov, tol=1e-10), True))
    checks.append(ok("scale covariance inverse is valid", max_abs_matrix_diff(identity_check, identity) < 1e-6, max_abs_matrix_diff(identity_check, identity)))
    checks.append(ok("positive quadratic form test", quadratic_form(scale_cov, [1, -1, 2, -2, 3, -3]) > 0, quadratic_form(scale_cov, [1, -1, 2, -2, 3, -3])))
    checks.append(ok("clean independent fit recovers true scale", abs(clean_independent["fit"]["weighted_scale"] - true_scale) < 1e-8, clean_independent["fit"]["weighted_scale"]))
    checks.append(ok("clean correlated fit recovers true scale", abs(clean_correlated["fit"]["weighted_scale"] - true_scale) < 1e-8, clean_correlated["fit"]["weighted_scale"]))
    checks.append(ok("clean correlated fit passes chi-square", clean_correlated["fit"]["passes_reduced_chi_square_lt_3"] is True, clean_correlated["fit"]["reduced_chi_square"]))
    checks.append(ok("small noisy correlated fit passes chi-square", noisy_correlated["fit"]["passes_reduced_chi_square_lt_3"] is True, noisy_correlated["fit"]["reduced_chi_square"]))
    checks.append(ok("bad correlated fit fails chi-square", bad_correlated["fit"]["passes_reduced_chi_square_lt_3"] is False, bad_correlated["fit"]["reduced_chi_square"]))
    checks.append(ok("correlated and independent sigmas differ", abs(clean_correlated["fit"]["sigma_weighted_scale"] - clean_independent["fit"]["sigma_weighted_scale"]) > 1e-12, {"independent": clean_independent["fit"]["sigma_weighted_scale"], "correlated": clean_correlated["fit"]["sigma_weighted_scale"]}))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXLIV",
        "title": "Correlated Covariance Fit Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "true_scale": true_scale,
        "dimensionless_kernel": {
            "M2": "5049/4",
            "role": "internal W33 dimensionless mass shell; physical channel estimates fit X=kappa^2M2",
        },
        "gls_formulas": {
            "covariance_propagation": "C_X = J C_y J^T",
            "estimator": "X_hat=(1^T C_X^-1 X)/(1^T C_X^-1 1)",
            "variance": "sigma_Xhat^2=1/(1^T C_X^-1 1)",
            "chi_square": "chi2=(X-X_hat 1)^T C_X^-1 (X-X_hat 1)",
            "dof": "N-1",
        },
        "clean_independent_fit": clean_independent["fit"],
        "clean_correlated_fit": clean_correlated["fit"],
        "small_noisy_correlated_fit": noisy_correlated["fit"],
        "bad_correlated_fit": bad_correlated["fit"],
        "correlated_fit_summary": {
            "channels": CHANNELS,
            "jacobian": clean_correlated["jacobian"],
            "value_covariance": correlated_cov,
            "scale_covariance": scale_cov,
        },
        "architecture_upgrade": (
            "CCCXLIII propagated independent channel errors.  CCCXLIV upgrades the "
            "measurement layer to full correlated covariance fitting with GLS consensus, "
            "covariance propagation C_X=J C_y J^T, and correlated chi-square diagnostics."
        ),
        "theorem": (
            "For a one-sector W33 response packet with correlated channel uncertainties, "
            "the channel-value covariance C_y propagates to scale covariance C_X=J C_y J^T. "
            "The common physical scale is optimally estimated by generalized least squares, "
            "and the one-sector model is tested by the correlated residual chi-square with N-1 degrees of freedom."
        ),
        "honesty_boundary": (
            "This is a covariance-ready fitting layer, but the covariance used here is synthetic. "
            "Real empirical use requires experimentally justified covariance matrices, nuisance parameters, and systematic-error modeling."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXLIV_correlated_covariance_fit_results.json"
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
