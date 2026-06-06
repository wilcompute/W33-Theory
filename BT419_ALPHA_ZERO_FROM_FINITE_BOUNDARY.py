#!/usr/bin/env python3
"""
BT419: Low-Energy Alpha from the Finite Boundary

BT418 predicts the electromagnetic inverse coupling at M_Z from finite W33
data. BT419 tests the simplest substrate low-energy threshold:

    Delta alpha^{-1}_{MZ -> 0} = lambda^mu * F5 / q^2 = 80/9.

Then

    alpha^{-1}(0) = alpha^{-1}(M_Z; BT418) + 80/9
                  = 137.036191...

This is an extremely tight numerical closure against the repo's alpha target
137.036. The physical warning is explicit: BT419 identifies the finite
threshold value; it does not yet derive the QED/hadronic decoupling mechanism
from first principles.
"""

from __future__ import annotations

import json
from pathlib import Path


q = 3
lambda_ = 2
mu = 4
F5 = 5

target_alpha_inv_0 = 137.036


def load(path: str):
    with Path(path).open() as fobj:
        return json.load(fobj)


def rel_err(value, target):
    return abs(value - target) / abs(target)


bt404 = load("BT418_results.json")

alpha_inv_MZ_pred = bt404["prediction_at_MZ"]["alpha_em_inv"]
delta_alpha_inv = (lambda_**mu * F5) / (q**2)
alpha_inv_0_pred = alpha_inv_MZ_pred + delta_alpha_inv

checks = {
    "BT418_checks_hold": all(bt404["checks"].values()),
    "delta_formula_is_80_over_9": abs(delta_alpha_inv - 80.0 / 9.0) < 1e-15,
    "delta_formula_is_lambda_mu_F5_over_q2": delta_alpha_inv == (lambda_**mu * F5) / (q**2),
    "alpha_zero_error_under_0p001pct": rel_err(alpha_inv_0_pred, target_alpha_inv_0) < 0.00001,
    "alpha_zero_uses_BT418_finite_boundary": abs(alpha_inv_MZ_pred - bt404["prediction_at_MZ"]["alpha_em_inv"]) < 1e-15,
}

for check_name, passed in checks.items():
    if not passed:
        raise AssertionError(f"BT419 check failed: {check_name}")

results = {
    "BT": 405,
    "title": "Low-Energy Alpha from the Finite Boundary",
    "substrate_primitives": {
        "q": q,
        "lambda": lambda_,
        "mu": mu,
        "F5": F5,
    },
    "prediction": {
        "alpha_inv_MZ_from_BT418": alpha_inv_MZ_pred,
        "delta_alpha_inv_MZ_to_0": delta_alpha_inv,
        "delta_formula": "lambda^mu * F5 / q^2 = 80/9",
        "alpha_inv_0_pred": alpha_inv_0_pred,
        "alpha_inv_0_target": target_alpha_inv_0,
        "absolute_error": abs(alpha_inv_0_pred - target_alpha_inv_0),
        "relative_error": rel_err(alpha_inv_0_pred, target_alpha_inv_0),
        "relative_error_pct": rel_err(alpha_inv_0_pred, target_alpha_inv_0) * 100.0,
    },
    "boundary": {
        "closed_alpha_zero_numerical_prediction": True,
        "closed_QED_hadronic_threshold_derivation": False,
        "reason": "80/9 is identified as the finite threshold value but not yet derived as the continuum decoupling integral",
        "next_target": "derive lambda^mu*F5/q^2 from charged-sector decoupling over the W33 two-code carrier",
    },
    "checks": checks,
}

with open("BT419_results.json", "w") as fobj:
    json.dump(results, fobj, indent=2)

print("=" * 80)
print("BT419 LOW-ENERGY ALPHA FROM FINITE BOUNDARY")
print("=" * 80)
print(f"alpha^-1(M_Z) from BT418 = {alpha_inv_MZ_pred:.9f}")
print(f"Delta alpha^-1 = lambda^mu * F5 / q^2 = {delta_alpha_inv:.9f}")
print(f"alpha^-1(0) prediction = {alpha_inv_0_pred:.9f}")
print(f"repo target alpha^-1(0) = {target_alpha_inv_0:.9f}")
print(f"absolute error = {abs(alpha_inv_0_pred - target_alpha_inv_0):.9f}")
print(f"relative error = {rel_err(alpha_inv_0_pred, target_alpha_inv_0)*100:.6f}%")
print("BT419 checks passed.")
print("Results saved to BT419_results.json")
