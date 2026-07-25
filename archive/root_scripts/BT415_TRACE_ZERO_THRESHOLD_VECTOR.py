#!/usr/bin/env python3
"""
BT415: Trace-Zero Electroweak Threshold Vector

BT413 showed that the W33 scale sits at a substrate-clean position in the
one-loop pairwise crossing lattice. BT414 showed the scalar-side reciprocal
lift. This script extracts the actual threshold direction.

At a scale M_trace close to M_W33, the centered inverse-coupling vector

    (alpha1^-1, alpha2^-1, alpha3^-1) - mean

is exactly collinear with

    (1, mu, -F5) = (1, 4, -5).

That vector is trace-zero and substrate-native: one abelian channel, four
spacetime/SU(2)-side channels, and five Fibonacci/color-side counterchannels.
The scalar coefficient c satisfies exp(q! c) ~= F5^2, connecting the threshold
amplitude to the same F5^2 ladder found in BT413.

No alpha closure is claimed. This identifies the finite threshold vector that
the next proof must derive from W33 representation/phase-sheet data.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


q = 3
mu = 4
F5 = 5
q_factorial = math.factorial(q)

M_Z = 91.1876
M_W33 = 5.0e13

alpha_em_inv_MZ_obs = 128.9
sin2_thetaW_MZ_obs = 0.23122
alpha_s_MZ_obs = 0.1181

b = [41.0 / 10.0, -19.0 / 6.0, -7.0]
threshold_direction = [1.0, float(mu), -float(F5)]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def sub(left, right):
    return [a - b for a, b in zip(left, right)]


def mul(scalar, vector):
    return [scalar * x for x in vector]


def norm(vector):
    return math.sqrt(dot(vector, vector))


def center(vector):
    mean = sum(vector) / len(vector)
    return [value - mean for value in vector], mean


def rel_err(value, target):
    return abs(value - target) / abs(target)


def inverse_couplings_at_mz():
    cos2 = 1.0 - sin2_thetaW_MZ_obs
    alpha2_inv = sin2_thetaW_MZ_obs * alpha_em_inv_MZ_obs
    alpha_y_inv = cos2 * alpha_em_inv_MZ_obs
    alpha1_inv = (3.0 / 5.0) * alpha_y_inv
    alpha3_inv = 1.0 / alpha_s_MZ_obs
    return [alpha1_inv, alpha2_inv, alpha3_inv]


def run_vector(scale):
    ln_mu_over_mz = math.log(scale / M_Z)
    at_mz = inverse_couplings_at_mz()
    values = [
        alpha_inv - beta / (2.0 * math.pi) * ln_mu_over_mz
        for alpha_inv, beta in zip(at_mz, b)
    ]
    centered, mean = center(values)
    return {
        "scale_GeV": scale,
        "ln_scale_over_MZ": ln_mu_over_mz,
        "alpha_inv_values": values,
        "mean_alpha_inv": mean,
        "centered": centered,
    }


def residual_to_direction(centered):
    c = dot(centered, threshold_direction) / dot(threshold_direction, threshold_direction)
    reconstruction = mul(c, threshold_direction)
    residual = sub(centered, reconstruction)
    return c, reconstruction, residual


def solve_exact_collinearity_scale():
    """Solve for the scale where the residual to span(1,mu,-F5) vanishes."""
    at_mz = inverse_couplings_at_mz()
    centered_mz, _ = center(at_mz)
    beta_centered, _ = center(b)
    slope = [value / (2.0 * math.pi) for value in beta_centered]

    # v(t) = centered_mz - slope*t. In the trace-zero plane, exact collinearity
    # with w means the 2D cross product vanishes. Use the pair (0,1):
    #   (v0 - s0*t)/w0 = (v1 - s1*t)/w1.
    w0, w1 = threshold_direction[0], threshold_direction[1]
    numerator = centered_mz[0] * w1 - centered_mz[1] * w0
    denominator = slope[0] * w1 - slope[1] * w0
    t = numerator / denominator
    scale = M_Z * math.exp(t)
    packet = run_vector(scale)
    c, reconstruction, residual = residual_to_direction(packet["centered"])
    packet.update(
        {
            "coefficient_c": c,
            "reconstruction": reconstruction,
            "residual": residual,
            "residual_rms": norm(residual) / math.sqrt(3.0),
            "relative_residual_norm": norm(residual) / norm(packet["centered"]),
            "exp_qfactorial_c": math.exp(q_factorial * c),
        }
    )
    return packet


def solve_amplitude_lock_scale():
    """Solve for the scale where c = log(F5^2)/q!."""
    c_target = math.log(F5**2) / q_factorial

    at_mz = inverse_couplings_at_mz()
    centered_mz, _ = center(at_mz)
    beta_centered, _ = center(b)
    slope = [value / (2.0 * math.pi) for value in beta_centered]

    c0 = dot(centered_mz, threshold_direction) / dot(threshold_direction, threshold_direction)
    c_slope = dot(slope, threshold_direction) / dot(threshold_direction, threshold_direction)
    t = (c0 - c_target) / c_slope
    scale = M_Z * math.exp(t)
    packet = run_vector(scale)
    c, reconstruction, residual = residual_to_direction(packet["centered"])
    packet.update(
        {
            "target_c": c_target,
            "coefficient_c": c,
            "reconstruction": reconstruction,
            "residual": residual,
            "residual_rms": norm(residual) / math.sqrt(3.0),
            "relative_residual_norm": norm(residual) / norm(packet["centered"]),
            "exp_qfactorial_c": math.exp(q_factorial * c),
        }
    )
    return packet


def load_bt399():
    path = Path("BT413_results.json")
    if not path.exists():
        return None
    with path.open() as fobj:
        return json.load(fobj)


bt399 = load_bt399()
bt399_target_scale = None
if bt399 is not None:
    bt399_target_scale = bt399["w33_scale_center"]["target_scale_GeV"]

at_w33 = run_vector(M_W33)
c_w33, recon_w33, resid_w33 = residual_to_direction(at_w33["centered"])
at_w33.update(
    {
        "coefficient_c": c_w33,
        "reconstruction": recon_w33,
        "residual": resid_w33,
        "residual_rms": norm(resid_w33) / math.sqrt(3.0),
        "relative_residual_norm": norm(resid_w33) / norm(at_w33["centered"]),
        "exp_qfactorial_c": math.exp(q_factorial * c_w33),
    }
)

exact_trace = solve_exact_collinearity_scale()
amplitude_lock = solve_amplitude_lock_scale()

checks = {
    "threshold_direction_is_trace_zero": abs(sum(threshold_direction)) < 1e-15,
    "threshold_direction_is_1_mu_minus_F5": threshold_direction == [1.0, 4.0, -5.0],
    "w33_residual_to_direction_under_0p2pct": at_w33["relative_residual_norm"] < 0.002,
    "exact_trace_scale_within_0p6pct_of_W33": rel_err(exact_trace["scale_GeV"], M_W33) < 0.006,
    "exact_trace_residual_is_zero": exact_trace["relative_residual_norm"] < 1e-12,
    "exp_qfactorial_c_within_1pct_of_F5_squared": rel_err(exact_trace["exp_qfactorial_c"], F5**2) < 0.01,
    "amplitude_lock_scale_within_2p2pct_of_W33": rel_err(amplitude_lock["scale_GeV"], M_W33) < 0.022,
    "amplitude_lock_direction_residual_under_0p5pct": amplitude_lock["relative_residual_norm"] < 0.005,
}

if bt399_target_scale is not None:
    checks["exact_trace_scale_within_1pct_of_BT413_target"] = rel_err(exact_trace["scale_GeV"], bt399_target_scale) < 0.01

for check_name, passed in checks.items():
    if not passed:
        raise AssertionError(f"BT415 check failed: {check_name}")

results = {
    "BT": 401,
    "title": "Trace-Zero Electroweak Threshold Vector",
    "substrate_primitives": {
        "q": q,
        "mu": mu,
        "F5": F5,
        "q_factorial": q_factorial,
    },
    "inputs": {
        "M_Z_GeV": M_Z,
        "M_W33_GeV": M_W33,
        "alpha_em_inv_MZ_obs": alpha_em_inv_MZ_obs,
        "sin2_thetaW_MZ_obs": sin2_thetaW_MZ_obs,
        "alpha_s_MZ_obs": alpha_s_MZ_obs,
        "beta_coefficients": {"b1": b[0], "b2": b[1], "b3": b[2]},
    },
    "threshold_direction": {
        "vector": threshold_direction,
        "formula": "(1, mu, -F5)",
        "trace": sum(threshold_direction),
        "interpretation": "one abelian channel, four spacetime/SU2-side channels, five Fibonacci/SU3-side counterchannels",
    },
    "at_W33_scale": at_w33,
    "exact_trace_scale": {
        **exact_trace,
        "relative_error_to_W33": rel_err(exact_trace["scale_GeV"], M_W33),
        "relative_error_to_BT413_target": (
            rel_err(exact_trace["scale_GeV"], bt399_target_scale)
            if bt399_target_scale is not None else None
        ),
        "relative_error_exp_qfactorial_c_to_F5_squared": rel_err(exact_trace["exp_qfactorial_c"], F5**2),
    },
    "amplitude_lock_scale": {
        **amplitude_lock,
        "target_c_formula": "log(F5^2)/q!",
        "relative_error_to_W33": rel_err(amplitude_lock["scale_GeV"], M_W33),
    },
    "boundary": {
        "closed_alpha_proof": False,
        "claim": "the missing threshold vector is identified, not yet derived from a finite W33 representation",
        "next_target": "derive (1,mu,-F5) from the qutrit sheet / two-code / E6 branching carrier",
    },
    "checks": checks,
}

with open("BT415_results.json", "w") as fobj:
    json.dump(results, fobj, indent=2)

print("=" * 80)
print("BT415 TRACE-ZERO ELECTROWEAK THRESHOLD VECTOR")
print("=" * 80)
print(f"threshold direction = {threshold_direction} = (1, mu, -F5)")
print("")
print("At M_W33:")
print(f"  centered vector = {[round(x, 9) for x in at_w33['centered']]}")
print(f"  best c = {at_w33['coefficient_c']:.12f}")
print(f"  residual norm / vector norm = {at_w33['relative_residual_norm']:.6e}")
print("")
print("Exact trace-zero alignment:")
print(f"  M_trace = {exact_trace['scale_GeV']:.6e} GeV")
print(f"  M_trace / M_W33 = {exact_trace['scale_GeV']/M_W33:.9f}")
print(f"  c = {exact_trace['coefficient_c']:.12f}")
print(f"  exp(q!*c) = {exact_trace['exp_qfactorial_c']:.9f}  target F5^2 = {F5**2}")
print(f"  residual norm / vector norm = {exact_trace['relative_residual_norm']:.6e}")
print("")
print("Amplitude lock:")
print(f"  c_target = log(F5^2)/q! = {amplitude_lock['target_c']:.12f}")
print(f"  M_amp = {amplitude_lock['scale_GeV']:.6e} GeV")
print(f"  residual norm / vector norm = {amplitude_lock['relative_residual_norm']:.6e}")
print("BT415 checks passed.")
print("Results saved to BT415_results.json")
