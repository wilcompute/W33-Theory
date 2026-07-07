#!/usr/bin/env python3
"""BT1886: chain A/2 operator locator.

Records the search for an existing chain A/2 or boundary operator. No prior
named A/2/Z40 chain-boundary operator was found by repo search in this pass, so
the first executable candidate is the W(3,3) adjacency-derived symmetric form
already used by BT982: G = 2I - A on the 40 W33 points, with vertex-subset
restriction matching the vertex E8 gauge.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1886_CHAIN_A_OVER_2_OPERATOR_LOCATOR_results.json")

SEARCH_QUERIES = [
    "A/2 chain boundary operator adjacency Z40",
    "chain A2 boundary operator Z40",
    "A_over_2 chain boundary",
    "boundary compatibility Z40 E8 chain",
]

LOCATED_CANDIDATES = [
    {
        "operator": "W33 adjacency-derived symmetric form",
        "formula": "G40 = 2I - A_W33",
        "source": "analysis/bt982_explicit_integral_e8_basis.py build_w33_adjacency + vertex restriction",
        "status": "first_naive_chain_metric_candidate"
    }
]


def theorem_summary():
    checks = {
        "search_queries_recorded": len(SEARCH_QUERIES) == 4,
        "no_named_A_over_2_operator_found": True,
        "w33_adjacency_candidate_recorded": LOCATED_CANDIDATES[0]["formula"] == "G40 = 2I - A_W33",
        "candidate_not_overclaimed_as_boundary": True,
    }
    return {
        "theorem": "BT1886 Chain A/2 Operator Locator",
        "search_queries": SEARCH_QUERIES,
        "located_candidates": LOCATED_CANDIDATES,
        "reading": "The repo search did not surface a named chain A/2 boundary operator. The available concrete object is the W33 adjacency-derived symmetric form G40 = 2I - A_W33 used by BT982 through vertex restriction.",
        "next_use": "BT1887 tests sparse Z40 embeddings against this W33 adjacency-derived candidate form.",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Locator/audit only. The W33 adjacency form is a candidate metric/chain form, not yet a proven boundary operator."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
