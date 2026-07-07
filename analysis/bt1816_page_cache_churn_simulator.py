#!/usr/bin/env python3
"""BT1816: exact page-cache churn simulator from BT1809 profiles."""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1807_defect_phase_plane_transversal_design as td43  # noqa: E402

OUT = Path("data/PART_BT1816_PAGE_CACHE_CHURN_SIMULATOR_results.json")


def move_profile(p, q, pts, adj):
    rows_p, _, _ = td43.vector_table(p, pts, adj)
    rows_q, _, _ = td43.vector_table(q, pts, adj)
    safe_p = {x for row in rows_p for x in row["triad"]}
    survival = [sum(1 for x in row["triad"] if x in safe_p) for row in rows_q]
    return Counter(survival)


def theorem_summary():
    pts, adj, _ = td43.build_w33()
    edge_profile_counts = Counter()
    nonedge_profile_counts = Counter()
    churn_points = Counter()
    block_rebuilds = Counter()
    for p in range(40):
        for q in range(40):
            if p == q:
                continue
            prof = move_profile(p, q, pts, adj)
            retained = sum(k * v for k, v in prof.items())
            churn = 27 - retained
            churn_points[churn] += 1
            if adj[p][q]:
                edge_profile_counts[tuple(sorted(prof.items()))] += 1
                block_rebuilds["edge_whole_phase_blocks"] += prof.get(0, 0)
                block_rebuilds["edge_partial_phase_blocks"] += sum(v for k, v in prof.items() if 0 < k < 3)
            else:
                nonedge_profile_counts[tuple(sorted(prof.items()))] += 1
                block_rebuilds["nonedge_whole_phase_blocks"] += prof.get(0, 0)
                block_rebuilds["nonedge_partial_phase_blocks"] += sum(v for k, v in prof.items() if 0 < k < 3)
    assert churn_points == Counter({9: 1560})
    assert edge_profile_counts == Counter({((0, 3), (3, 6)): 480})
    assert nonedge_profile_counts == Counter({((2, 9),): 1080})
    return {
        "theorem": "BT1816 Page-Cache Churn Simulator",
        "ordered_moves": 1560,
        "churn_points_per_move": 9,
        "edge_moves": 480,
        "nonedge_moves": 1080,
        "edge_profile": {"0_survivors": 3, "3_survivors": 6},
        "nonedge_profile": {"2_survivors": 9},
        "aggregate_block_rebuilds": dict(block_rebuilds),
        "interpretation": {
            "edge_move": "nine pages move as three whole phase triples; six phase triples remain intact",
            "nonedge_move": "nine pages move as one page in each of nine phase triples; no phase triple remains intact"
        },
        "checks": {
            "all_moves_churn_exactly_9_points": True,
            "all_edge_moves_have_whole_block_profile": True,
            "all_nonedge_moves_have_distributed_profile": True
        },
        "honest_scope": "Exact cache-churn accounting over the 27-point page directory. It is not a measured cache-latency benchmark."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
