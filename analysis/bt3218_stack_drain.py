#!/usr/bin/env python3
"""Pass 3218: exact non-promoting PR/evidence dependency scheduler.

The scheduler consumes a frozen connector snapshot, validates the dependency DAG,
and emits necessary preconditions and next actions. It never merges, retargets,
closes, approves, or promotes a workflow. Live metadata must be refreshed before
any mutation.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/PART_BT3218_STACK_SNAPSHOT.json"
OUT = ROOT / "data/PART_BT3218_STACK_DRAIN_RESULTS.json"
GREEN = {"success", "green", "completed_success"}


def topo(rows):
    pending = {r["number"]: set(r.get("depends_on", [])) for r in rows}
    order = []
    while pending:
        ready = sorted(n for n, deps in pending.items() if not deps.intersection(pending))
        if not ready:
            raise AssertionError("dependency cycle")
        # Consume one smallest ready item at a time. This keeps a numbered dependency
        # chain contiguous without changing the partial order or hiding parallel lanes.
        number = ready[0]
        order.append(number)
        pending.pop(number)
    return order


def main():
    snap = json.loads(SOURCE.read_text())
    rows = snap["pulls"]
    by = {r["number"]: r for r in rows}
    assert len(by) == len(rows)
    for row in rows:
        assert all(d in by for d in row.get("depends_on", []))

    order = topo(rows)
    actions = []
    for number in order:
        row = by[number]
        deps = [by[d] for d in row.get("depends_on", [])]
        deps_merged = all(d.get("merged") for d in deps)
        focused = row.get("focused_status", "unknown")
        ready = (
            row["state"] == "open"
            and row.get("mergeable") is True
            and deps_merged
            and focused in GREEN
        )
        if row.get("merged"):
            action = "record terminal merge artifact and retain explicit evidence boundary"
        elif not deps_merged:
            action = "blocked: complete and merge dependencies " + ",".join(
                "#" + str(d["number"]) for d in deps if not d.get("merged")
            )
        elif focused in {"queued", "pending", "unobserved", "unknown"}:
            action = (
                "observe dedicated focused workflow; do not infer success from source, "
                "mergeability, or unrelated checks"
            )
        elif focused == "action_required":
            action = (
                "human approval is required before the workflow can run; approval is not "
                "evidence of success"
            )
        elif focused not in GREEN:
            action = "repair or rerun the focused gate and inspect terminal artifacts"
        elif row.get("mergeable") is not True:
            action = "reconcile newest master and re-run the focused gate on the reconciled head"
        else:
            action = "eligible for explicit human merge review; scheduler itself grants no authority"
        actions.append(
            {
                "number": number,
                "dependencies_merged": deps_merged,
                "focused_run": row.get("focused_run"),
                "focused_status": focused,
                "mergeable_snapshot": row.get("mergeable"),
                "ready_for_human_merge_review": ready,
                "next_action": action,
            }
        )

    assert not any(x["ready_for_human_merge_review"] for x in actions)
    result = {
        "schema": "w33.pass3218.stack_drain.v1",
        "snapshot_time": snap["captured_at"],
        "master_commit": snap["master_commit"],
        "topological_order": order,
        "actions": actions,
        "active_chain": [242, 243, 244],
        "independent_gate": [246],
        "recently_merged": [247],
        "ready_count": 0,
        "exact_next_sequence": [
            "Observe corrected PR #242 run 30940467641. Mergeability alone is insufficient; require terminal integration idempotence, three PDFs and persisted evidence on head 41e34c85.",
            "Only after #242 is green and merged, retarget or reconcile #243; approve its action-required workflow, inspect readable materialization, and run its focused gate.",
            "Only after #243 is green and merged, reconcile #244, repair its failed focused lane, and rerun on the reconciled head.",
            "Independently inspect the terminal failure in #246 run 30931074919, apply the narrow repair, reconcile current master, and require a green rerun.",
            "Retain #247 as merged source with PDF and physical boundaries until its dedicated evidence is terminal.",
        ],
        "merge_authority": "none",
        "boundary": (
            "This is a frozen scheduling certificate, not live GitHub state and not "
            "permission to mutate any pull request. Mergeability is not merge readiness."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"order": order, "ready": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
