#!/usr/bin/env python3
"""Replayable Holonet OS scheduler over W(3,3) spread epochs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "w33_uor_spread_scheduler.json"
DEFAULT_OUTPUT = ROOT / "data" / "holonet_os_scheduler_trace.json"


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def build_trace(schedule: dict[str, Any]) -> dict[str, Any]:
    assignments = schedule["assignments"]
    queue = list(assignments)
    ticks = []
    for epoch in sorted(
        {
            row["assigned_epoch"]
            for row in assignments
            if row["assigned_epoch"] is not None
        }
    ):
        before = len(queue)
        dispatch = [row for row in queue if row["assigned_epoch"] == epoch]
        queue = [row for row in queue if row["assigned_epoch"] != epoch]
        used_sites: set[str] = set()
        conflict = False
        for row in dispatch:
            sites = set(row["sites"])
            if used_sites & sites:
                conflict = True
            used_sites.update(sites)
        ticks.append(
            {
                "tick": len(ticks),
                "spread_epoch": epoch,
                "queue_before": before,
                "dispatch_count": len(dispatch),
                "queue_after": len(queue),
                "used_site_count": len(used_sites),
                "conflict_free": not conflict,
                "packets": [
                    {
                        "packet_id": row["packet_id"],
                        "report_index": row["report_index"],
                        "sites": row["sites"],
                        "hops": row["hops"],
                    }
                    for row in dispatch
                ],
            }
        )

    replay_hash = hashlib.sha256(canonical_bytes(ticks)).hexdigest()
    return {
        "schema": "w33.holonet.os_scheduler_trace.v1",
        "status": (
            "PASS"
            if not queue and all(tick["conflict_free"] for tick in ticks)
            else "FAIL"
        ),
        "source_scheduler_status": schedule["status"],
        "packet_count": schedule["packet_count"],
        "spread_count": schedule["spread_count"],
        "tick_count": len(ticks),
        "all_packets_dispatched": not queue,
        "all_ticks_conflict_free": all(tick["conflict_free"] for tick in ticks),
        "max_dispatch_per_tick": max(
            (tick["dispatch_count"] for tick in ticks), default=0
        ),
        "replay_hash": replay_hash,
        "ticks": ticks,
        "boundary": (
            "This is the OS-level dispatch trace over spread epochs. It schedules "
            "Holonet control packets, not child-process CPU arithmetic."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", default=str(DEFAULT_INPUT), help="spread scheduler JSON"
    )
    parser.add_argument(
        "--out", default=str(DEFAULT_OUTPUT), help="OS trace output JSON"
    )
    args = parser.parse_args(argv)

    source = Path(args.input)
    if not source.is_absolute():
        source = ROOT / source
    trace = build_trace(json.loads(source.read_text(encoding="utf-8")))
    output = Path(args.out)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(trace, indent=2), encoding="utf-8")

    print(f"status: {trace['status']}")
    print(f"ticks: {trace['tick_count']}")
    print(f"packets: {trace['packet_count']}")
    print(f"replay: {trace['replay_hash'][:24]}...")
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0 if trace["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
