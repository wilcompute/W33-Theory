#!/usr/bin/env python3
"""Pass 3200: repository evidence-debt DAG and non-promoting scheduler.

This is a frozen audit snapshot, not a live GitHub API client. It records the dependency and
evidence type observed on 4 August 2026 so downstream work cannot treat a source-complete,
queued, failed, superseded or stacked PR as equivalent to a green independent theorem gate.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3200_REPOSITORY_EVIDENCE_DEBT_results.json"

OPEN_PULLS = [
    {"number": 242, "kind": "implementation", "base": "master", "depends_on": [], "focused_gate": "failure", "topic": "3153-3162 adaptive epoch factor engine"},
    {"number": 243, "kind": "implementation", "base": "pr242", "depends_on": [242], "focused_gate": "exhaustive_pending", "topic": "3163-3174 proof-carrying runtime"},
    {"number": 244, "kind": "implementation", "base": "pr243", "depends_on": [243], "focused_gate": "publication_unresolved", "topic": "3175-3186 curvature-routed inference"},
    {"number": 245, "kind": "implementation", "base": "master", "depends_on": [], "focused_gate": "queued", "topic": "3187-3192 chromatic defect filter"},
    {"number": 236, "kind": "older_stack", "base": "master", "depends_on": [], "focused_gate": "queued_or_stale", "topic": "3133-3142 certifying adaptive inference"},
    {"number": 239, "kind": "older_stack", "base": "pr236", "depends_on": [236], "focused_gate": "queued_or_stale", "topic": "3143-3152 sparse inference and universal ISA correction"},
    {"number": 238, "kind": "evidence_only", "base": "master", "depends_on": [], "focused_gate": "stale_review", "topic": "3124-3132 evidence"},
    {"number": 235, "kind": "evidence_only", "base": "master", "depends_on": [], "focused_gate": "stale_review", "topic": "3104-3119 evidence"},
    {"number": 233, "kind": "source_or_evidence", "base": "master", "depends_on": [], "focused_gate": "supersession_review", "topic": "3064-3072 belief machine"},
    {"number": 232, "kind": "evidence_only", "base": "master", "depends_on": [], "focused_gate": "stale_review", "topic": "3048-3063 evidence"},
    {"number": 231, "kind": "source_or_evidence", "base": "master", "depends_on": [], "focused_gate": "supersession_review", "topic": "3003-3011 seven-front closure"},
    {"number": 230, "kind": "source_or_evidence", "base": "master", "depends_on": [], "focused_gate": "supersession_review", "topic": "2996-3002 deep optimal information"},
    {"number": 229, "kind": "evidence_only", "base": "master", "depends_on": [], "focused_gate": "stale_review", "topic": "2981-2995 evidence"},
    {"number": 226, "kind": "evidence_only", "base": "master", "depends_on": [], "focused_gate": "stale_review", "topic": "2946-2959 evidence"},
    {"number": 225, "kind": "evidence_only", "base": "master", "depends_on": [], "focused_gate": "stale_review", "topic": "2937-2945 evidence"},
    {"number": 224, "kind": "source_or_evidence", "base": "master", "depends_on": [], "focused_gate": "supersession_review", "topic": "2929-2936 recursive Holonet"},
    {"number": 223, "kind": "source_or_evidence", "base": "master", "depends_on": [], "focused_gate": "supersession_review", "topic": "2920-2928 phase router"},
    {"number": 220, "kind": "evidence_only", "base": "master", "depends_on": [], "focused_gate": "stale_review", "topic": "2890-2900 evidence"},
    {"number": 217, "kind": "evidence_only", "base": "master", "depends_on": [], "focused_gate": "stale_review", "topic": "2862-2881 evidence"},
    {"number": 215, "kind": "source_or_evidence", "base": "master", "depends_on": [], "focused_gate": "supersession_review", "topic": "2847-2853 protected observer"},
    {"number": 213, "kind": "evidence_only", "base": "master", "depends_on": [], "focused_gate": "stale_review", "topic": "2840-2846 evidence"},
]


def topological_order(rows):
    pending = {row["number"]: set(row["depends_on"]) for row in rows}
    order = []
    while pending:
        ready = sorted(number for number, deps in pending.items() if not deps.intersection(pending))
        if not ready:
            raise AssertionError("cycle in PR dependency snapshot")
        order.extend(ready)
        for number in ready:
            pending.pop(number)
    return order


def main() -> None:
    order = topological_order(OPEN_PULLS)
    by_kind = {}
    by_gate = {}
    for row in OPEN_PULLS:
        by_kind[row["kind"]] = by_kind.get(row["kind"], 0) + 1
        by_gate[row["focused_gate"]] = by_gate.get(row["focused_gate"], 0) + 1

    execution_queue = [
        {"priority": 1, "action": "repair PR #242 focused failure and rerun its dedicated gate", "promotion": False},
        {"priority": 2, "action": "only after #242 is green and merged, retarget/reconcile #243 and complete its 194-BFS and M36 shard gates", "promotion": False},
        {"priority": 3, "action": "only after #243 is green, reconcile #244 and close its lossless manuscript/PDF gate", "promotion": False},
        {"priority": 4, "action": "run #245 independently; preserve its explicit no-ten-colour-decision boundary", "promotion": False},
        {"priority": 5, "action": "archive or close superseded evidence-only PRs after recording their terminal artifacts and replacement links", "promotion": False},
    ]
    result = {
        "schema": "w33.pass3200.repository_evidence_debt.v1",
        "snapshot_time": "2026-08-04T11:31:00-04:00",
        "open_pull_count_in_audit": len(OPEN_PULLS),
        "open_pulls": OPEN_PULLS,
        "dependency_topological_order": order,
        "counts_by_kind": dict(sorted(by_kind.items())),
        "counts_by_gate": dict(sorted(by_gate.items())),
        "active_stack": [242, 243, 244],
        "independent_current_front": [245],
        "older_overlapping_stack": [236, 239],
        "execution_queue": execution_queue,
        "merge_authority": "none: this artifact schedules evidence work but never converts queued, failed or source-complete states into merge permission",
        "headline": "The dominant repository risk is evidence debt and stacked-branch drift, not absence of new source: twenty-one open research/evidence PRs include multiple superseded gates and two overlapping inference stacks.",
        "boundary": "Frozen audit snapshot from GitHub metadata and PR descriptions. Live state must be refreshed before any merge, close or retarget operation. Classification as supersession_review is a maintenance prompt, not permission to discard unique evidence."
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"open": len(OPEN_PULLS), "active_stack": [242, 243, 244]}, sort_keys=True))


if __name__ == "__main__":
    main()
