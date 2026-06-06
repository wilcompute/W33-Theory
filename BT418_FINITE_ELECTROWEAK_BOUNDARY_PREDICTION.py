#!/usr/bin/env python3
"""
BT418: Finite Electroweak Boundary Prediction

BT415-BT417 identify a finite W33 threshold boundary:

  mean inverse coupling      = q*k + F5 = 41
  trace-zero threshold       = c*(1, mu, -F5)
  coefficient                = c = log(F5^2)/q!
  threshold scale            = M_W33 = 5e13 GeV

BT418 runs that boundary down to M_Z with the standard one-loop SM beta
coefficients. Unlike BT413/BT415, the observed gauge couplings are not used as
inputs to determine the boundary; they are used only as comparison targets.

Result against the repo's BT413 observable inputs:
  alpha_em^-1(M_Z) within 0.6 percent
  sin^2(theta_W)(M_Z) within 0.4 percent
  alpha_s(M_Z) within 3.3 percent

This is not a low-energy alpha(0) proof because the QED/hadronic threshold
from M_Z to zero remains a separate bridge. It is a finite electroweak boundary
prediction at M_Z.
"""

from __future__ import annotations

import json
import math


q = 3
lambda_ = 2
mu = 4
F5 = 5
k = 12
q_factorial = math.factorial(q)

M_Z = 91.1876
M_W33 = 5.0e13

# Comparison targets used by the local BT413/BT388 batch.
target_alpha_em_inv_MZ = 128.9
target_sin2_thetaW_MZ = 0.23122
target_alpha_s_MZ = 0.1181

# One-loop SM beta coefficients with GUT-normalized U(1).
b1 = 41.0 / 10.0
b2 = -19.0 / 6.0
b3 = -7.0


def rel_err(value, target):
    return abs(value - target) / abs(target)


mean_inverse_coupling = q * k + F5
threshold_direction = [1.0, float(mu), -float(F5)]
threshold_coefficient = math.log(F5**2) / q_factorial

high_scale_inverse_couplings = [
    mean_inverse_coupling + threshold_coefficient * component
    for component in threshold_direction
]

ln_ratio = math.log(M_W33 / M_Z)
beta_coefficients = [b1, b2, b3]

# alpha_i^{-1}(M_Z) = alpha_i^{-1}(M_W33) + b_i/(2*pi)*ln(M_W33/M_Z)
predicted_inverse_couplings_MZ = [
    high + beta / (2.0 * math.pi) * ln_ratio
    for high, beta in zip(high_scale_inverse_couplings, beta_coefficients)
]

alpha1_inv_MZ, alpha2_inv_MZ, alpha3_inv_MZ = predicted_inverse_couplings_MZ
alphaY_inv_MZ = (5.0 / 3.0) * alpha1_inv_MZ
alpha_em_inv_MZ = alpha2_inv_MZ + alphaY_inv_MZ
sin2_thetaW_MZ = alpha2_inv_MZ / alpha_em_inv_MZ
alpha_s_MZ = 1.0 / alpha3_inv_MZ

# GUT-normalized comparison values implied by the local target observables.
target_alpha2_inv = target_sin2_thetaW_MZ * target_alpha_em_inv_MZ
target_alphaY_inv = (1.0 - target_sin2_thetaW_MZ) * target_alpha_em_inv_MZ
target_alpha1_inv = (3.0 / 5.0) * target_alphaY_inv
target_alpha3_inv = 1.0 / target_alpha_s_MZ

checks = {
    "mean_inverse_coupling_is_qk_plus_F5": mean_inverse_coupling == 41,
    "threshold_direction_is_trace_zero": abs(sum(threshold_direction)) < 1e-15,
    "threshold_coefficient_is_log_F5_squared_over_qfactorial": abs(threshold_coefficient - math.log(25) / 6.0) < 1e-15,
    "alpha_em_inv_MZ_error_under_0p6pct": rel_err(alpha_em_inv_MZ, target_alpha_em_inv_MZ) < 0.006,
    "sin2_thetaW_MZ_error_under_0p5pct": rel_err(sin2_thetaW_MZ, target_sin2_thetaW_MZ) < 0.005,
    "alpha_s_MZ_error_under_3p6pct": rel_err(alpha_s_MZ, target_alpha_s_MZ) < 0.036,
    "alpha1_inv_error_under_0p6pct": rel_err(alpha1_inv_MZ, target_alpha1_inv) < 0.006,
    "alpha2_inv_error_under_1pct": rel_err(alpha2_inv_MZ, target_alpha2_inv) < 0.01,
    "alpha3_inv_error_under_3p2pct": rel_err(alpha3_inv_MZ, target_alpha3_inv) < 0.032,
}

for check_name, passed in checks.items():
    if not passed:
        raise AssertionError(f"BT418 check failed: {check_name}")

results = {
    "BT": 404,
    "title": "Finite Electroweak Boundary Prediction",
    "substrate_boundary": {
        "mean_inverse_coupling": mean_inverse_coupling,
        "mean_formula": "q*k + F5",
        "threshold_direction": threshold_direction,
        "threshold_direction_formula": "(1, mu, -F5)",
        "threshold_coefficient": threshold_coefficient,
        "threshold_coefficient_formula": "log(F5^2)/q!",
        "M_W33_GeV": M_W33,
        "high_scale_inverse_couplings": {
            "alpha1_inv": high_scale_inverse_couplings[0],
            "alpha2_inv": high_scale_inverse_couplings[1],
            "alpha3_inv": high_scale_inverse_couplings[2],
        },
    },
    "prediction_at_MZ": {
        "alpha1_inv_GUT_normalized": alpha1_inv_MZ,
        "alpha2_inv": alpha2_inv_MZ,
        "alpha3_inv": alpha3_inv_MZ,
        "alphaY_inv": alphaY_inv_MZ,
        "alpha_em_inv": alpha_em_inv_MZ,
        "sin2_thetaW": sin2_thetaW_MZ,
        "alpha_s": alpha_s_MZ,
    },
    "comparison_targets": {
        "alpha1_inv_GUT_normalized": target_alpha1_inv,
        "alpha2_inv": target_alpha2_inv,
        "alpha3_inv": target_alpha3_inv,
        "alpha_em_inv": target_alpha_em_inv_MZ,
        "sin2_thetaW": target_sin2_thetaW_MZ,
        "alpha_s": target_alpha_s_MZ,
    },
    "relative_errors": {
        "alpha1_inv_GUT_normalized": rel_err(alpha1_inv_MZ, target_alpha1_inv),
        "alpha2_inv": rel_err(alpha2_inv_MZ, target_alpha2_inv),
        "alpha3_inv": rel_err(alpha3_inv_MZ, target_alpha3_inv),
        "alpha_em_inv": rel_err(alpha_em_inv_MZ, target_alpha_em_inv_MZ),
        "sin2_thetaW": rel_err(sin2_thetaW_MZ, target_sin2_thetaW_MZ),
        "alpha_s": rel_err(alpha_s_MZ, target_alpha_s_MZ),
    },
    "boundary": {
        "uses_observed_couplings_as_boundary_inputs": False,
        "uses_observed_couplings_for_comparison_only": True,
        "closed_alpha_zero_momentum_proof": False,
        "next_target": "derive M_Z-to-zero QED/hadronic threshold and improve the SU(3) residual",
    },
    "checks": checks,
}

with open("BT418_results.json", "w") as fobj:
    json.dump(results, fobj, indent=2)

print("=" * 80)
print("BT418 FINITE ELECTROWEAK BOUNDARY PREDICTION")
print("=" * 80)
print("finite boundary:")
print(f"  mean inverse = q*k + F5 = {mean_inverse_coupling}")
print(f"  direction = {threshold_direction} = (1, mu, -F5)")
print(f"  c = log(F5^2)/q! = {threshold_coefficient:.12f}")
print(f"  M_W33 = {M_W33:.6e} GeV")
print("")
print("predictions at M_Z:")
print(f"  alpha_em^-1 = {alpha_em_inv_MZ:.6f}  target {target_alpha_em_inv_MZ:.6f}  error {rel_err(alpha_em_inv_MZ, target_alpha_em_inv_MZ)*100:.4f}%")
print(f"  sin^2 thetaW = {sin2_thetaW_MZ:.9f}  target {target_sin2_thetaW_MZ:.9f}  error {rel_err(sin2_thetaW_MZ, target_sin2_thetaW_MZ)*100:.4f}%")
print(f"  alpha_s = {alpha_s_MZ:.9f}  target {target_alpha_s_MZ:.9f}  error {rel_err(alpha_s_MZ, target_alpha_s_MZ)*100:.4f}%")
print("")
print("GUT-normalized inverse couplings at M_Z:")
print(f"  alpha1^-1 = {alpha1_inv_MZ:.6f}  target {target_alpha1_inv:.6f}")
print(f"  alpha2^-1 = {alpha2_inv_MZ:.6f}  target {target_alpha2_inv:.6f}")
print(f"  alpha3^-1 = {alpha3_inv_MZ:.6f}  target {target_alpha3_inv:.6f}")
print("BT418 checks passed.")
print("Results saved to BT418_results.json")
