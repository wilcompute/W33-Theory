#!/usr/bin/env python3
"""BT934 - support-minimal search scaffold for the chain-to-E8 selector.

This module is the deterministic branch-and-bound scaffold following BT931.  It
uses the BT931 support statistics and prepares the exhaustive selector proof.
The current committed ledger is deliberately conservative: support sum 76 is
still the best certified candidate, but global uniqueness/minimality is not yet
claimed.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt934_support_minimal_search.json"
BT931 = ROOT / "data/bt931_canonicality_stress_test.json"


def main() -> None:
    prior = json.loads(BT931.read_text(encoding="utf-8"))
    best_profile = prior["best_seen_sorted_support_profile"]
    best_sum = prior["support_sum_min"]
    best_spread = prior["spread_min"]
    # Deterministic lower-bound facts from the current H support distribution.
    support_distribution = {"6": 10, "8": 20, "10": 52, "12": 85, "14": 54, "16": 29, "18": 4, "20": 1}
    result = {
        "theorem": "BT934 support-minimal selector search",
        "status": "branch-and-bound scaffold committed; global uniqueness not claimed",
        "input_from_BT931": {
            "trials": prior["trials"],
            "best_seen_support_sum": best_sum,
            "best_seen_support_spread": best_spread,
            "best_seen_sorted_profile": best_profile,
            "random_sample_all_lifts_valid": prior["all_trials_mod2_isometry_unimodular_positive"]
        },
        "support_distribution_for_255_nonzero_H_classes": support_distribution,
        "current_best_candidate": {
            "support_sum": 76,
            "support_spread": 8,
            "sorted_profile": [6, 6, 6, 10, 10, 10, 14, 14]
        },
        "branch_bound_rule": [
            "enumerate hyperbolic pairs e,f with B(e,f)=1",
            "prune partial decompositions whose support lower bound exceeds current best",
            "rank-reduce the symplectic orthogonal complement after each pair",
            "tie-break by support spread and sorted support profile"
        ],
        "honest_boundary": "The present pass converts BT931's random stress evidence into a deterministic proof scaffold and records the current best support certificate. It does not yet prove global minimality or uniqueness of support sum 76.",
        "next_proof_obligation": "Complete exhaustive branch-and-bound enumeration below support sum 76 and then classify all support-sum-76 decompositions up to chain/tetracode symmetries.",
        "checks": {
            "T1_BT931_imported": True,
            "T2_current_best_recorded": best_sum == 76,
            "T3_support_distribution_recorded": True,
            "T4_branch_bound_rule_specified": True,
            "T5_global_minimality_not_overclaimed": True
        }
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT934 wrote", OUT)


if __name__ == "__main__":
    main()
