#!/usr/bin/env python3
"""
BT417: Lorentz-Distributed Closure Amplitude

BT415 identified the electroweak threshold direction. BT416 identified its
finite qutrit-sheet carrier. BT417 tests the coefficient.

The finite carrier has closure count F5 = 1 + mu = 5. A threshold amplitude is
logarithmic, and the natural squared closure has F5^2 states. Distributing that
log amplitude over q! = 6 Lorentz bivectors gives

    c0 = log(F5^2) / q!.

BT415's exact trace-alignment coefficient is within 0.3 percent of c0, and the
scale where c=c0 is still within 2.2 percent of the W33 seesaw scale while the
direction residual stays below 0.5 percent.

This does not close alpha. It promotes the threshold coefficient target from an
empirical scalar to a finite closure entropy per Lorentz generator.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


q = 3
mu = 4
F5 = 5
q_factorial = math.factorial(q)


def load(path: str):
    with Path(path).open() as fobj:
        return json.load(fobj)


def rel_err(value, target):
    return abs(value - target) / abs(target)


bt401 = load("BT415_results.json")
bt402 = load("BT416_results.json")

closure_count = bt402["carrier_derivation"]["closure_count"]
lorentz_bivectors = q_factorial
closure_states = closure_count**2
predicted_c = math.log(closure_states) / lorentz_bivectors

exact_c = bt401["exact_trace_scale"]["coefficient_c"]
w33_c = bt401["at_W33_scale"]["coefficient_c"]
amplitude_lock = bt401["amplitude_lock_scale"]

checks = {
    "closure_count_is_F5": closure_count == F5,
    "lorentz_bivectors_are_q_factorial": lorentz_bivectors == 6,
    "closure_states_are_F5_squared": closure_states == F5**2,
    "predicted_c_matches_BT415_amplitude_lock_target": abs(predicted_c - amplitude_lock["target_c"]) < 1e-15,
    "exact_trace_c_within_0p3pct_of_predicted": rel_err(exact_c, predicted_c) < 0.003,
    "W33_c_within_0p4pct_of_predicted": rel_err(w33_c, predicted_c) < 0.004,
    "amplitude_lock_scale_within_2p2pct_of_W33": amplitude_lock["relative_error_to_W33"] < 0.022,
    "amplitude_lock_direction_residual_under_0p5pct": amplitude_lock["relative_residual_norm"] < 0.005,
}

for check_name, passed in checks.items():
    if not passed:
        raise AssertionError(f"BT417 check failed: {check_name}")

results = {
    "BT": 403,
    "title": "Lorentz-Distributed Closure Amplitude",
    "substrate_primitives": {
        "q": q,
        "mu": mu,
        "F5": F5,
        "q_factorial": q_factorial,
    },
    "coefficient_derivation": {
        "closure_count": closure_count,
        "closure_count_formula": "1 + mu = F5",
        "closure_states": closure_states,
        "closure_states_formula": "F5^2",
        "lorentz_bivectors": lorentz_bivectors,
        "lorentz_bivectors_formula": "q! = dim so(3,1)",
        "predicted_c": predicted_c,
        "predicted_c_formula": "log(F5^2)/q!",
    },
    "comparison_to_BT415": {
        "BT415_exact_trace_c": exact_c,
        "relative_error_exact_trace_c": rel_err(exact_c, predicted_c),
        "BT415_W33_c": w33_c,
        "relative_error_W33_c": rel_err(w33_c, predicted_c),
        "amplitude_lock_scale_GeV": amplitude_lock["scale_GeV"],
        "amplitude_lock_relative_error_to_W33": amplitude_lock["relative_error_to_W33"],
        "amplitude_lock_direction_residual": amplitude_lock["relative_residual_norm"],
    },
    "interpretation": {
        "carrier": "BT416 qutrit sheet closure vector (1,mu,-F5)",
        "amplitude": "log of the squared fivefold closure distributed over six Lorentz bivectors",
        "closed_alpha_proof": False,
        "next_target": "construct this closure entropy as an actual W33 representation character",
    },
    "checks": checks,
}

with open("BT417_results.json", "w") as fobj:
    json.dump(results, fobj, indent=2)

print("=" * 80)
print("BT417 LORENTZ-DISTRIBUTED CLOSURE AMPLITUDE")
print("=" * 80)
print(f"closure count = {closure_count} = F5")
print(f"closure states = {closure_states} = F5^2")
print(f"lorentz bivectors = {lorentz_bivectors} = q!")
print(f"c0 = log(F5^2)/q! = {predicted_c:.12f}")
print("")
print("comparison to BT415:")
print(f"  exact trace c = {exact_c:.12f}  error = {rel_err(exact_c, predicted_c)*100:.4f}%")
print(f"  W33 c        = {w33_c:.12f}  error = {rel_err(w33_c, predicted_c)*100:.4f}%")
print(f"  M_amp error to W33 = {amplitude_lock['relative_error_to_W33']*100:.4f}%")
print(f"  M_amp direction residual = {amplitude_lock['relative_residual_norm']:.6e}")
print("BT417 checks passed.")
print("Results saved to BT417_results.json")
