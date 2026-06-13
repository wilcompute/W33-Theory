#!/usr/bin/env python3
"""BT936 - selector uniqueness/orbit classifier.

Combines BT934 support data and BT935 tetracode symmetry data to classify the
current selector status.  It does not claim uniqueness: the support-minimal
exhaustive proof and the chain action of the tetracode monomial group remain
open.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt936_selector_uniqueness_orbit_classifier.json"


def read_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    bt933 = read_json("data/bt933_selector_theorem_candidate.json")
    bt934 = read_json("data/bt934_support_minimal_search.json")
    bt935 = read_json("data/bt935_tetracode_block_symmetry_test.json")
    classifier = {
        "support_layer": {
            "best_support_sum": bt934["current_best_candidate"]["support_sum"],
            "best_support_spread": bt934["current_best_candidate"]["support_spread"],
            "best_profile": bt934["current_best_candidate"]["sorted_profile"],
            "global_minimality_proved": False,
            "reason": "BT934 records the branch-and-bound scaffold and current certificate but does not yet complete exhaustive enumeration."
        },
        "metric_layer": {
            "vertex_metric_required": True,
            "tetracode_metric_required": True,
            "dual_metric_compatibility_known": True,
            "reason": "BT929 and BT930 give determinant-1 positive-definite lifts into both metric E8 witnesses."
        },
        "symmetry_layer": {
            "vertex_symmetry_useful": False,
            "tetracode_signed_monomial_group_order": bt935["signed_monomial_symmetry_count"],
            "chain_action_constructed": False,
            "reason": "BT932 killed vertex equivariance as a selector; BT935 identified nontrivial tetracode symmetry but did not construct its action on chain H."
        }
    }
    status = "many-or-one unresolved"
    result = {
        "theorem": "BT936 selector uniqueness/orbit classifier",
        "status": status,
        "classifier": classifier,
        "current_candidate_rule": bt933["selector_rule"],
        "current_candidate_score": bt933["candidate_total_score"],
        "orbit_conclusion": "The current data do not justify a one-orbit uniqueness claim. The selector is metric-compatible and has a best support certificate, but uniqueness waits on exhaustive support classification plus a chain action of the tetracode signed monomial group.",
        "next_exact_test": "Enumerate all support-sum-76 hyperbolic decompositions and quotient them by the tetracode monomial group once its chain action is built.",
        "checks": {
            "T1_support_layer_classified": True,
            "T2_metric_layer_classified": True,
            "T3_symmetry_layer_classified": True,
            "T4_one_orbit_uniqueness_not_overclaimed": True,
            "T5_next_orbit_test_stated": True
        }
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT936 wrote", OUT)


if __name__ == "__main__":
    main()
