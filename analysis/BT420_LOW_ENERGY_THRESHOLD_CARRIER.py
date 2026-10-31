#!/usr/bin/env python3
"""
BT420: Low-Energy 80/9 Threshold Carrier

BT419 numerically closes alpha(0) using

    Delta alpha^{-1}_{MZ -> 0} = 80/9.

BT420 identifies the finite W33 carrier of that number:

    80/9 = (lambda^mu line stabilizers) * (F5 closure) / (q^2 color-family grid)
         = 16 * 5 / 9.

The 16 comes from the BT385 two-code rank ledger as the common line-stabilizer
count. The 5 comes from the BT416 qutrit-sheet closure. The q^2 denominator is
the color-by-generation averaging grid.

This still does not prove the continuum QED/hadronic decoupling integral. It
does prove that the exact threshold value used by BT419 has a finite carrier
already present in the W33 two-code/selector architecture.
"""

from __future__ import annotations

import json
from pathlib import Path


q = 3
lambda_ = 2
mu = 4
F5 = 5


def load(path: str):
    with Path(path).open() as fobj:
        return json.load(fobj)


bt385 = load("data/w33_BREAKTHROUGH_385_two_code_correction_rank_ledger.json")
bt402 = load("BT416_results.json")
bt405 = load("BT419_results.json")

ledger = {entry["interp"]: entry for entry in bt385["rank_ledger"]}
line_stabilizers = ledger["line stabilizers in common"]["value"]
closure_count = bt402["carrier_derivation"]["closure_count"]
color_generation_grid = q**2
threshold_value = line_stabilizers * closure_count / color_generation_grid

checks = {
    "BT416_checks_hold": all(bt402["checks"].values()),
    "BT419_checks_hold": all(bt405["checks"].values()),
    "line_stabilizers_are_lambda_mu": line_stabilizers == lambda_**mu == 16,
    "closure_count_is_F5": closure_count == F5 == 5,
    "color_generation_grid_is_q_squared": color_generation_grid == q**2 == 9,
    "threshold_value_is_80_over_9": abs(threshold_value - 80.0 / 9.0) < 1e-15,
    "threshold_matches_BT419_delta": abs(threshold_value - bt405["prediction"]["delta_alpha_inv_MZ_to_0"]) < 1e-15,
}

for check_name, passed in checks.items():
    if not passed:
        raise AssertionError(f"BT420 check failed: {check_name}")

results = {
    "BT": 406,
    "title": "Low-Energy 80/9 Threshold Carrier",
    "carrier": {
        "line_stabilizers": line_stabilizers,
        "line_stabilizers_source": "BT385 rank ledger",
        "line_stabilizers_formula": "lambda^mu",
        "closure_count": closure_count,
        "closure_count_source": "BT416 qutrit-sheet closure",
        "closure_count_formula": "F5",
        "color_generation_grid": color_generation_grid,
        "color_generation_grid_formula": "q^2",
        "threshold_value": threshold_value,
        "threshold_formula": "lambda^mu * F5 / q^2 = 80/9",
    },
    "bridge_to_BT419": {
        "BT419_delta_alpha_inv": bt405["prediction"]["delta_alpha_inv_MZ_to_0"],
        "BT419_alpha_inv_0_pred": bt405["prediction"]["alpha_inv_0_pred"],
        "BT419_alpha_inv_0_relative_error_pct": bt405["prediction"]["relative_error_pct"],
    },
    "boundary": {
        "finite_threshold_carrier_identified": True,
        "continuum_decoupling_integral_derived": False,
        "next_target": "realize the 16*5/q^2 carrier as the charged-sector MZ-to-zero decoupling operator",
    },
    "checks": checks,
}

with open("BT420_results.json", "w") as fobj:
    json.dump(results, fobj, indent=2)

print("=" * 80)
print("BT420 LOW-ENERGY 80/9 THRESHOLD CARRIER")
print("=" * 80)
print(f"line stabilizers = {line_stabilizers} = lambda^mu")
print(f"closure count = {closure_count} = F5")
print(f"color-generation grid = {color_generation_grid} = q^2")
print(f"threshold = {line_stabilizers}*{closure_count}/{color_generation_grid} = {threshold_value:.9f}")
print(f"BT419 alpha^-1(0) = {bt405['prediction']['alpha_inv_0_pred']:.9f}")
print("BT420 checks passed.")
print("Results saved to BT420_results.json")
