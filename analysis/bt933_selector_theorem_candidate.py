#!/usr/bin/env python3
"""BT933 - selector theorem candidate for the chain-to-E8 lift.

Packages BT931/BT932 into a candidate selector.  It does not claim a theorem;
it proposes the least-arbitrary rule surviving the stress tests:

  minimize support sum, then support spread, then require dual vertex+tetracode
  metric compatibility and reject pure equivariance because the vertex witness
  has trivial preserving symmetry.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt933_selector_theorem_candidate.json"


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main():
    bt931 = read_json("data/bt931_canonicality_stress_test.json")
    bt932 = read_json("data/bt932_symmetry_equivariance_test.json")
    bt929 = read_json("data/bt929_chain_to_vertex_e8_map_search.json")
    bt930 = read_json("data/bt930_chain_to_tetracode_e8_map_search.json")
    candidate_profile = bt931["best_seen_key_support_spread_sorted_profile"]
    energy = {
        "support_sum": candidate_profile[0],
        "support_spread": candidate_profile[1],
        "vertex_metric_penalty": 0 if bt929["checks"]["T4_lifted_gram_positive_definite"] else 1,
        "tetracode_metric_penalty": 0 if bt930["checks"]["T4_integral_lift_positive_definite"] else 1,
        "equivariance_penalty": 0 if bt932["checks"]["T2_vertex_preserving_symmetry_trivial"] else 1,
    }
    total = energy["support_sum"] + energy["support_spread"] + 1000*(energy["vertex_metric_penalty"] + energy["tetracode_metric_penalty"] + energy["equivariance_penalty"])
    result = {
        "theorem": "BT933 selector theorem candidate",
        "status": "candidate selector, not proven unique",
        "selector_rule": [
            "minimize total support of the four hyperbolic pairs in the chain representatives",
            "tie-break by minimizing support spread",
            "require determinant-1 positive-definite lift into the BT926 vertex E8 witness",
            "require determinant-1 positive-definite lift into the MCCCLXXXVIII tetracode E8 witness",
            "do not use vertex equivariance as a selector because BT932 found the vertex witness symmetry-isolated"
        ],
        "candidate_energy": energy,
        "candidate_total_score": total,
        "best_seen_sorted_support_profile": candidate_profile[2],
        "basis_profile_raw": bt931["best_seen_raw_profile"],
        "stress_context": {"trials": bt931["trials"], "support_sum_min": bt931["support_sum_min"], "support_sum_max": bt931["support_sum_max"], "all_trials_valid_lifts": bt931["all_trials_mod2_isometry_unimodular_positive"]},
        "equivariance_context": {"w33_self_maps_preserving_subset": bt932["w33_self_maps_preserving_subset"], "nontrivial_preserving_maps": bt932["nontrivial_preserving_maps"], "e8_diagram_self_maps": bt932["e8_diagram_self_maps"]},
        "exact_conclusion": "The best current selector candidate is not pure positivity or pure equivariance. It is support-minimal/balance-minimal among chain symplectic bases, with mandatory compatibility with both metric E8 witnesses. This is a concrete theorem candidate, not a proved canonical theorem.",
        "next_proof_obligation": "Exhaustively classify support-minimal symplectic bases, then test whether the dual vertex+tetracode compatibility leaves a single orbit under the remaining chain symmetries.",
        "checks": {"T1_selector_rule_defined": True, "T2_uses_BT931_stress_data": True, "T3_uses_BT932_equivariance_negative": True, "T4_requires_dual_metric_compatibility": True, "T5_uniqueness_not_claimed": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT933 wrote", OUT)

if __name__ == "__main__": main()
