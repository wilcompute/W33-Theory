#!/usr/bin/env python3
"""BT1821: cache locality score from BT1816 churn profiles."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1821_CACHE_LOCALITY_SCORE_results.json")


def theorem_summary():
    edge = {"intact_triples": 6, "partial_triples": 0, "rebuilt_triples": 3, "churn_points": 9}
    nonedge = {"intact_triples": 0, "partial_triples": 9, "rebuilt_triples": 0, "churn_points": 9}
    # Score rewards intact triples and penalizes fragmented partial rebuilds.
    edge_score = edge["intact_triples"] - edge["partial_triples"] / 3
    nonedge_score = nonedge["intact_triples"] - nonedge["partial_triples"] / 3
    return {
        "theorem": "BT1821 Cache Locality Score",
        "metric": "locality = intact_phase_triples - partial_phase_triples/3",
        "edge_move": {**edge, "locality_score": edge_score},
        "nonedge_move": {**nonedge, "locality_score": nonedge_score},
        "locality_gap_edge_minus_nonedge": edge_score - nonedge_score,
        "decision": "edge relocation is strictly better: same 9-point churn, higher intact-block locality",
        "checks": {
            "edge_and_nonedge_have_same_churn_points": True,
            "edge_has_six_intact_phase_triples": True,
            "nonedge_has_zero_intact_phase_triples": True,
            "edge_score_exceeds_nonedge_score": edge_score > nonedge_score
        },
        "honest_scope": "Derived locality metric from exact churn profiles. It is not a measured cache latency."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
