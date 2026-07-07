#!/usr/bin/env python3
"""BT1808: exact scheduler from the BT1807 TD(4,3) escape surface.

Every defect center has nine ground vectors, each exposing four cheap exits.
BT1807 proved these 40*9*4 exits cover the directed W33 fabric exactly three
times. This witness turns that cover into a deterministic scheduler: for every
directed fabric edge p->q there are exactly three vector rows at p exposing q;
we label them slots 0,1,2 and obtain a 3-slot balanced relocation schedule.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1807_defect_phase_plane_transversal_design as td43  # noqa: E402

OUT = Path("data/PART_BT1808_TD43_EDGE_SCHEDULER_results.json")


def build_schedule():
    pts, adj, lines = td43.build_w33()
    rows_by_center = {p: td43.vector_table(p, pts, adj)[0] for p in range(len(pts))}
    exposures = defaultdict(list)
    for p, rows in rows_by_center.items():
        for phase, row in enumerate(rows):
            for target in row["quad"]:
                exposures[(p, target)].append({"phase": phase, "triad": row["triad"], "quad": row["quad"]})

    schedule = []
    for edge in sorted(exposures):
        choices = sorted(exposures[edge], key=lambda x: (x["phase"], x["triad"], x["quad"]))
        for slot, choice in enumerate(choices):
            schedule.append({"from": edge[0], "to": edge[1], "slot": slot, "phase": choice["phase"]})
    return pts, adj, lines, rows_by_center, exposures, schedule


def theorem_summary():
    pts, adj, lines, rows_by_center, exposures, schedule = build_schedule()
    directed_edges = [(i, j) for i in range(len(pts)) for j in range(len(pts)) if adj[i][j]]
    assert len(directed_edges) == 480
    assert len(exposures) == 480
    assert len(schedule) == 1440
    assert {len(v) for v in exposures.values()} == {3}
    assert Counter(item["slot"] for item in schedule) == Counter({0: 480, 1: 480, 2: 480})
    assert Counter(item["from"] for item in schedule) == Counter({p: 36 for p in range(40)})
    assert Counter((item["from"], item["to"]) for item in schedule) == Counter({e: 3 for e in directed_edges})

    target_profile = Counter()
    for p in range(40):
        local = Counter(item["to"] for item in schedule if item["from"] == p)
        target_profile.update(local.values())
        assert set(local.values()) == {3}
        assert len(local) == 12

    return {
        "theorem": "BT1808 TD(4,3) Balanced Edge Scheduler Theorem",
        "directed_fabric_edges": 480,
        "scheduler_rows": 1440,
        "slot_count": 3,
        "slot_loads": dict(Counter(item["slot"] for item in schedule)),
        "per_center_exit_count": 36,
        "per_center_target_count": 12,
        "per_center_target_multiplicity": 3,
        "directed_edge_cover_multiplicity": 3,
        "identity": "40 centers * 9 phase rows * 4 exits = 1440 = 3 * 480 directed edges",
        "sample_schedule_rows": schedule[:12],
        "checks": {
            "each_directed_edge_has_three_phase_choices": True,
            "each_slot_has_480_rows": True,
            "each_center_has_36_rows": True,
            "each_center_hits_each_neighbor_three_times": True,
        },
        "honest_scope": "Exact scheduler over finite W33 incidence. It compiles allowed cheap relocations; it does not assert stochastic fairness or wall-clock timing."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
