#!/usr/bin/env python3
"""
BT416: Qutrit Sheet Threshold Carrier

BT415 identified the electroweak threshold direction as

    (1, mu, -F5) = (1, 4, -5).

This script derives that vector from the finite selector/qutrit machinery:

  * BT363: the golden obstruction is one selected qutrit phase sheet;
  * BT362: each local Z-min support has four boundary lines;
  * W33 arithmetic: one selected sheet + four boundary lines = fivefold
    closure, i.e. F5 = mu + 1.

So the threshold vector is the trace-zero closure ledger:

    selected sheet, boundary lines, negative closure
      = (1, mu, -(1+mu))
      = (1, mu, -F5).

This is not yet a representation-theoretic derivation of the threshold
coefficient c. It is the finite carrier that BT415 says the coefficient must
live on.
"""

from __future__ import annotations

import json
from pathlib import Path


q = 3
lambda_ = 2
mu = 4
F5 = 5
q3 = q**3


def load(path: str):
    with Path(path).open() as fobj:
        return json.load(fobj)


bt362 = load("data/w33_BREAKTHROUGH_362_zmin_local_d4_phase_lift.json")
bt363 = load("data/w33_BREAKTHROUGH_363_golden_failure_single_phase_sheet.json")
bt364 = load("data/w33_BREAKTHROUGH_364_z20_anchor_bipartition_lift.json")
bt365 = load("data/w33_BREAKTHROUGH_365_unique_anchor_bipartition_correction.json")
bt401 = load("BT415_results.json")

selected_sheet_count = 1
boundary_line_count = bt362["summary"]["boundary_lines_per_support"]
closure_count = selected_sheet_count + boundary_line_count
carrier_vector = [selected_sheet_count, boundary_line_count, -closure_count]

bt401_vector = [int(value) for value in bt401["threshold_direction"]["vector"]]

selected_sheet_supports = bt363["summary"]["selected_sheet_supports"]
ordered_failures = bt363["summary"]["ordered_failures"]
incident_sheets = bt362["summary"]["incident_sheets_per_support"]
present_phases = bt362["summary"]["phases_present_per_boundary_line"]
selected_edges = bt364["summary"]["selected_edge_count"]

working_bipartition = next(
    record for record in bt365["bipartitions"]
    if record["left_side_corrected_failures"] == 0
    and record["right_side_corrected_failures"] == 0
)
active_cross_pairs = len(working_bipartition["cross_pairs"])
inactive_same_side_pairs = len(working_bipartition["same_side_pairs"])

checks = {
    "BT362_identities_hold": bt362["summary"]["all_identities_hold"],
    "BT363_identities_hold": bt363["summary"]["all_identities_hold"],
    "BT364_identities_hold": bt364["summary"]["all_identities_hold"],
    "BT365_identities_hold": bt365["summary"]["all_identities_hold"],
    "BT415_identities_hold": all(bt401["checks"].values()),
    "one_selected_sheet_plus_mu_boundary_lines_closes_to_F5": closure_count == F5 == mu + 1,
    "carrier_vector_matches_BT415_threshold_direction": carrier_vector == bt401_vector,
    "carrier_vector_is_trace_zero": sum(carrier_vector) == 0,
    "selected_sheet_supports_are_mu_q3": selected_sheet_supports == mu * q3 == 108,
    "ordered_failures_are_selected_sheet_times_2q": ordered_failures == selected_sheet_supports * (2**q) == 864,
    "local_incident_sheets_are_mu_times_lambda_and_2q": incident_sheets == boundary_line_count * present_phases == mu * lambda_ == 2**q,
    "selected_z20_edges_are_lambda_q3": selected_edges == lambda_ * q3 == 54,
    "working_cross_pairs_are_mu": active_cross_pairs == mu,
    "working_same_side_pairs_are_lambda": inactive_same_side_pairs == lambda_,
}

for check_name, passed in checks.items():
    if not passed:
        raise AssertionError(f"BT416 check failed: {check_name}")

results = {
    "BT": 402,
    "title": "Qutrit Sheet Threshold Carrier",
    "substrate_primitives": {
        "q": q,
        "lambda": lambda_,
        "mu": mu,
        "F5": F5,
        "q_cubed": q3,
    },
    "carrier_derivation": {
        "selected_qutrit_phase_sheet": selected_sheet_count,
        "boundary_lines_per_support": boundary_line_count,
        "closure_count": closure_count,
        "closure_formula": "1 + mu = F5",
        "carrier_vector": carrier_vector,
        "carrier_formula": "(1, mu, -F5)",
        "trace": sum(carrier_vector),
        "matches_BT415_threshold_direction": carrier_vector == bt401_vector,
    },
    "finite_support_arithmetic": {
        "selected_sheet_supports": selected_sheet_supports,
        "selected_sheet_supports_formula": "mu*q^3",
        "ordered_failures": ordered_failures,
        "ordered_failures_formula": "mu*q^3*2^q",
        "incident_sheets_per_support": incident_sheets,
        "incident_sheets_formula": "mu*lambda = 2^q",
        "selected_z20_edges": selected_edges,
        "selected_z20_edges_formula": "lambda*q^3",
        "active_cross_pairs": active_cross_pairs,
        "active_cross_pairs_formula": "mu",
        "inactive_same_side_pairs": inactive_same_side_pairs,
        "inactive_same_side_pairs_formula": "lambda",
    },
    "bridge_to_BT415": {
        "BT415_exact_trace_scale_GeV": bt401["exact_trace_scale"]["scale_GeV"],
        "BT415_relative_error_to_W33": bt401["exact_trace_scale"]["relative_error_to_W33"],
        "BT415_exp_qfactorial_c": bt401["exact_trace_scale"]["exp_qfactorial_c"],
        "BT415_exp_qfactorial_c_target": F5**2,
        "interpretation": "BT416 supplies the finite carrier; BT415 supplies the observed electroweak coefficient on that carrier",
    },
    "boundary": {
        "closed_alpha_proof": False,
        "closed_threshold_coefficient_proof": False,
        "next_target": "derive BT415 coefficient c from a representation character on the BT416 carrier",
    },
    "checks": checks,
}

with open("BT416_results.json", "w") as fobj:
    json.dump(results, fobj, indent=2)

print("=" * 80)
print("BT416 QUTRIT SHEET THRESHOLD CARRIER")
print("=" * 80)
print(f"carrier = selected sheet + boundary lines - closure")
print(f"        = {selected_sheet_count} + {boundary_line_count} - {closure_count}")
print(f"        = {carrier_vector} = (1, mu, -F5)")
print("")
print("finite arithmetic:")
print(f"  selected sheet supports = {selected_sheet_supports} = mu*q^3")
print(f"  ordered failures = {ordered_failures} = mu*q^3*2^q")
print(f"  incident sheets/support = {incident_sheets} = mu*lambda = 2^q")
print(f"  selected Z20 edges = {selected_edges} = lambda*q^3")
print(f"  active cross pairs = {active_cross_pairs} = mu")
print(f"  inactive same-side pairs = {inactive_same_side_pairs} = lambda")
print("")
print("BT416 checks passed.")
print("Results saved to BT416_results.json")
