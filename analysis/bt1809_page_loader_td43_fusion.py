#!/usr/bin/env python3
"""BT1809: page-loader fusion with the TD(4,3) interrupt design.

Pass 65 proved the relocation page bill is always nine points. BT1809 refines
what that bill means at phase-directory level:

  * edge move p->q: six of the new nine phase triples survive whole and three
    rebuild whole, i.e. survival histogram {3: 6, 0: 3};
  * nonedge move p->q: all nine new triples retain two points and rebuild one,
    i.e. survival histogram {2: 9};
  * both cases have the same nine-point bill, but edge moves preserve phase
    blocks and therefore win together with the Pass-64 ray price law.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1807_defect_phase_plane_transversal_design as td43  # noqa: E402

OUT = Path("data/PART_BT1809_PAGE_LOADER_TD43_FUSION_results.json")


def _hist_for_move(p, q, pts, adj):
    rows_p, _, _ = td43.vector_table(p, pts, adj)
    rows_q, _, _ = td43.vector_table(q, pts, adj)
    safe_p = {x for row in rows_p for x in row["triad"]}
    survival = [sum(1 for x in row["triad"] if x in safe_p) for row in rows_q]
    return tuple(sorted(Counter(survival).items()))


def theorem_summary():
    pts, adj, _ = td43.build_w33()
    edge_hists = Counter()
    nonedge_hists = Counter()
    overlap_profile = Counter()
    for p in range(40):
        rows_p, _, _ = td43.vector_table(p, pts, adj)
        safe_p = {x for row in rows_p for x in row["triad"]}
        for q in range(40):
            if p == q:
                continue
            rows_q, _, _ = td43.vector_table(q, pts, adj)
            safe_q = {x for row in rows_q for x in row["triad"]}
            overlap_profile[len(safe_p & safe_q)] += 1
            hist = tuple(sorted(Counter(sum(1 for x in row["triad"] if x in safe_p) for row in rows_q).items()))
            if adj[p][q]:
                edge_hists[hist] += 1
            else:
                nonedge_hists[hist] += 1

    expected_edge = ((0, 3), (3, 6))
    expected_nonedge = ((2, 9),)
    assert edge_hists == Counter({expected_edge: 480})
    assert nonedge_hists == Counter({expected_nonedge: 1080})
    assert overlap_profile == Counter({18: 1560})

    summary = {
        "theorem": "BT1809 Page-Loader TD(4,3) Fusion Theorem",
        "safe_zone_overlap": {"ordered_center_moves": 1560, "overlap_points": 18, "page_bill_points": 9},
        "edge_move_profile": {
            "ordered_edge_moves": 480,
            "phase_triples_survive_whole": 6,
            "phase_triples_rebuild_whole": 3,
            "histogram_survivors_per_new_triple": {"0": 3, "3": 6},
            "interpretation": "edge move preserves six phase blocks exactly and rebuilds three complete phase blocks",
        },
        "nonedge_move_profile": {
            "ordered_nonedge_moves": 1080,
            "phase_triples_degrade": 9,
            "histogram_survivors_per_new_triple": {"2": 9},
            "interpretation": "nonedge move keeps two points in every phase block and rebuilds one point in each block",
        },
        "decision_law": "page bill ties at nine points, but edge moves preserve phase blocks and Pass 64 also prices them at 3 rays, so edge relocation strictly wins.",
        "checks": {
            "all_edge_moves_have_6_survive_3_rebuild_profile": True,
            "all_nonedge_moves_have_9_partial_rebuild_profile": True,
            "all_ordered_moves_have_safe_overlap_18": True,
        },
        "honest_scope": "Exact phase-directory migration law. It describes address survival/rebuild structure, not measured cache latency."
    }
    return summary


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
