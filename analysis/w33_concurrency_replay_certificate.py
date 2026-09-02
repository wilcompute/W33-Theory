#!/usr/bin/env python3
"""Deterministic concurrency certificate for the W33 async component runtime.

The async schedule recorder previously committed SEND/RECV/PUMP ordering while
wait-for deadlock detection lived beside it.  This module closes that gap by
committing, in one replayable transcript:

* the pre-resolution wait-for graph root,
* the detected SCC/deadlock cycle,
* deterministic victim selection,
* the scoped cancellation event and post-cancel graph root,
* the subsequent async wake schedule root.

Equal input plus equal cancellation policy plus equal wake schedule replays to
one exact concurrency root.  Changing either the victim or wake ordering changes
that identity.  All state is carrier-neutral; private fibre coordinates never
enter the transcript.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from w33_async_deadlock_detector import CancelCapability, WaitForGraph
from w33_async_schedule_replay import run_schedule


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def graph_snapshot(graph: WaitForGraph) -> dict[str, Any]:
    return {
        "owners": dict(sorted(graph.owners.items())),
        "waits": {k: sorted(v) for k, v in sorted(graph.waits.items())},
        "edges": {k: sorted(v) for k, v in sorted(graph.edges().items())},
        "cancelled": sorted(graph.cancelled),
    }


def build_deadlock() -> WaitForGraph:
    graph = WaitForGraph()
    for task, resource in (
        ("component-A", "future-A"),
        ("component-B", "stream-B"),
        ("component-C", "mailbox-C"),
    ):
        graph.own(task, resource)
    graph.wait("component-A", "stream-B")
    graph.wait("component-B", "mailbox-C")
    graph.wait("component-C", "future-A")
    return graph


def run_concurrency(
    priorities: dict[str, int],
    wake_schedule: list[str],
) -> dict[str, Any]:
    graph = build_deadlock()
    before = graph_snapshot(graph)
    cycles = graph.deadlocks()
    if len(cycles) != 1:
        raise RuntimeError("demo topology must contain exactly one deadlock SCC")
    cycle = cycles[0]
    victim = graph.choose_victim(cycle, priorities)

    root_cap = CancelCapability(frozenset(cycle), frozenset({"cancel", "derive"}))
    victim_cap = root_cap.derive({victim}, {"cancel"})
    cancellation_record = graph.cancel(victim, victim_cap)
    after = graph_snapshot(graph)

    wait_for_root = digest(before)
    post_cancel_root = digest(after)
    cancellation_event = {
        "schema": "w33.typed-cancellation-event.v1",
        "cycle": list(cycle),
        "victim": victim,
        "priorities": dict(sorted(priorities.items())),
        "wait_for_root": wait_for_root,
        "post_cancel_root": post_cancel_root,
        "cancellation_record": cancellation_record,
        "authority": {
            "tasks": sorted(victim_cap.tasks),
            "rights": sorted(victim_cap.rights),
        },
    }
    cancellation_root = digest(cancellation_event)

    async_run = run_schedule(wake_schedule)
    transcript = {
        "schema": "w33.concurrency-transcript.v1",
        "wait_for_root": wait_for_root,
        "cancellation_root": cancellation_root,
        "post_cancel_root": post_cancel_root,
        "async_schedule_root": async_run["schedule_root"],
        "deadlocks_after_resolution": [list(x) for x in graph.deadlocks()],
        "final_async_state": async_run["final"],
    }
    return {
        "wait_for_root": wait_for_root,
        "cancellation_event": cancellation_event,
        "cancellation_root": cancellation_root,
        "post_cancel_root": post_cancel_root,
        "async_schedule_root": async_run["schedule_root"],
        "concurrency_root": digest(transcript),
        "transcript": transcript,
    }


def verify() -> dict[str, Any]:
    priorities = {"component-A": 10, "component-B": 1, "component-C": 5}
    schedule = ["send:first", "send:second", "recv:first", "pump", "recv:second"]
    a = run_concurrency(priorities, schedule)
    b = run_concurrency(priorities, schedule)

    different_victim = run_concurrency(
        {"component-A": 1, "component-B": 10, "component-C": 5}, schedule
    )
    different_wake = run_concurrency(
        priorities,
        ["send:first", "send:second", "pump", "recv:first", "recv:second"],
    )

    serialized = json.dumps(a, sort_keys=True)
    checks = {
        "exact_replay_has_same_wait_graph": a["wait_for_root"] == b["wait_for_root"],
        "exact_replay_has_same_cancellation": a["cancellation_root"] == b["cancellation_root"],
        "exact_replay_has_same_wake_schedule": a["async_schedule_root"] == b["async_schedule_root"],
        "exact_replay_has_same_concurrency_root": a["concurrency_root"] == b["concurrency_root"],
        "deadlock_is_resolved": a["transcript"]["deadlocks_after_resolution"] == [],
        "different_victim_changes_certificate": different_victim["cancellation_root"] != a["cancellation_root"] and different_victim["concurrency_root"] != a["concurrency_root"],
        "different_wake_order_changes_certificate": different_wake["async_schedule_root"] != a["async_schedule_root"] and different_wake["concurrency_root"] != a["concurrency_root"],
        "transcript_is_carrier_neutral": "private_tag6" not in serialized and "state216" not in serialized,
    }
    return {
        "schema": "w33.concurrency-replay-certificate.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "wait_for_root": a["wait_for_root"],
        "cancellation_root": a["cancellation_root"],
        "async_schedule_root": a["async_schedule_root"],
        "concurrency_root": a["concurrency_root"],
        "checks": checks,
        "interpretation": "Deadlock state, the authorized cycle-breaking decision, and host wake ordering are one content-addressed replay object rather than separate scheduler side effects.",
        "honesty_boundary": "This proves deterministic software replay for the recorded control-plane decisions; it is not distributed consensus or a physical real-time scheduling theorem.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
