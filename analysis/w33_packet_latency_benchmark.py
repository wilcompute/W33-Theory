#!/usr/bin/env python3
"""Packet-level latency benchmark for Holonet active vs clock-native policies.

Compiler slot counts tell us how long a complete program takes.  This benchmark
looks inside the schedule: for every packet, it finds the last hop-line job in
that packet and records when the packet completes under the active-tick schedule
and under the clock-native schedule, both in active ticks and elapsed frame-clock
slots.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from statistics import mean
from typing import Any

from w33_line_context_compiler import build_compilation
from w33_spread_contextual_microkernel_bridge import (
    DEFAULT_INPUTS,
    load_json,
    normalize_path,
)
from w33_uor_runtime_model import ROOT

DEFAULT_OUTPUT = ROOT / "data" / "w33_packet_latency_benchmark.json"
DEFAULT_CERTIFIED = ROOT / "data" / "w33_line_context_compiler.json"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_packet_id(job_id: str) -> str:
    return job_id.rsplit(":h", 1)[0]


def source_tick_to_clock_slot(embedding: dict[str, Any]) -> dict[int, int]:
    mapping = {}
    for slot_index, slot in enumerate(embedding["expanded_clock_walk"]):
        if slot["kind"] == "active":
            mapping[int(slot["source_tick"])] = slot_index
    return mapping


def tick_maps(ticks: list[dict[str, Any]]) -> dict[str, int]:
    job_tick = {}
    for tick in ticks:
        for job_id in tick["jobs"]:
            job_tick[job_id] = int(tick["tick"])
    return job_tick


def packet_completion_rows(schedule: dict[str, Any]) -> list[dict[str, Any]]:
    active = schedule["active_schedule"]
    native = schedule["clock_native_schedule"]
    active_job_tick = tick_maps(active["ticks"])
    native_job_tick = tick_maps(native["ticks"])
    active_clock_for_tick = source_tick_to_clock_slot(active["clock_embedding"])
    native_clock_for_tick = source_tick_to_clock_slot(native["clock_embedding"])
    packet_jobs: dict[str, list[str]] = {}
    for job in schedule["lowering"]["jobs"]:
        packet_jobs.setdefault(parse_packet_id(job["job_id"]), []).append(job["job_id"])

    rows = []
    for packet_id in sorted(packet_jobs):
        jobs = packet_jobs[packet_id]
        active_tick = max(active_job_tick[job_id] for job_id in jobs)
        native_tick = max(native_job_tick[job_id] for job_id in jobs)
        active_clock = max(
            active_clock_for_tick[active_job_tick[job_id]] for job_id in jobs
        )
        native_clock = max(
            native_clock_for_tick[native_job_tick[job_id]] for job_id in jobs
        )
        rows.append(
            {
                "packet_id": packet_id,
                "hop_job_count": len(jobs),
                "active_completion_tick": active_tick + 1,
                "active_completion_clock_slot": active_clock + 1,
                "clock_native_completion_tick": native_tick + 1,
                "clock_native_completion_clock_slot": native_clock + 1,
                "clock_slot_delta_native_minus_active": (native_clock + 1)
                - (active_clock + 1),
                "native_clock_faster": native_clock < active_clock,
            }
        )
    return rows


def percentile(values: list[int | float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * q)))
    return float(ordered[index])


def policy_summary(rows: list[dict[str, Any]], prefix: str) -> dict[str, Any]:
    ticks = [row[f"{prefix}_completion_tick"] for row in rows]
    slots = [row[f"{prefix}_completion_clock_slot"] for row in rows]
    return {
        "mean_completion_tick": mean(ticks) if ticks else 0,
        "p50_completion_tick": percentile(ticks, 0.5),
        "max_completion_tick": max(ticks, default=0),
        "mean_completion_clock_slot": mean(slots) if slots else 0,
        "p50_completion_clock_slot": percentile(slots, 0.5),
        "p90_completion_clock_slot": percentile(slots, 0.9),
        "max_completion_clock_slot": max(slots, default=0),
    }


def summarize_schedule(
    label: str, multiplier: int, schedule: dict[str, Any], source: str
) -> dict[str, Any]:
    rows = packet_completion_rows(schedule)
    native_faster = sum(1 for row in rows if row["native_clock_faster"])
    deltas = [row["clock_slot_delta_native_minus_active"] for row in rows]
    return {
        "label": label,
        "source": source,
        "multiplier": multiplier,
        "status": schedule["status"],
        "packet_count": len(rows),
        "job_count": schedule["lowering"]["job_count"],
        "compiler_optimality": schedule["optimizer"]["optimality_status"],
        "active_policy": {
            "total_ticks": schedule["active_schedule"]["tick_count"],
            "total_clock_slots": schedule["active_schedule"]["clock_embedding"][
                "clock_slot_count"
            ],
            "total_connectors": schedule["active_schedule"]["clock_embedding"][
                "connector_slot_count"
            ],
            **policy_summary(rows, "active"),
        },
        "clock_native_policy": {
            "total_ticks": schedule["clock_native_schedule"]["tick_count"],
            "total_clock_slots": schedule["clock_native_schedule"]["clock_slot_count"],
            "total_connectors": schedule["clock_native_schedule"][
                "connector_slot_count"
            ],
            **policy_summary(rows, "clock_native"),
        },
        "packet_delta_summary": {
            "native_faster_packet_count": native_faster,
            "native_not_slower_packet_count": sum(1 for delta in deltas if delta <= 0),
            "min_native_minus_active_clock_slot": min(deltas, default=0),
            "mean_native_minus_active_clock_slot": mean(deltas) if deltas else 0,
            "max_native_minus_active_clock_slot": max(deltas, default=0),
        },
        "packet_rows": rows,
    }


def multiply_reports(
    reports: list[dict[str, Any]], multiplier: int
) -> list[dict[str, Any]]:
    expanded = []
    for copy_index in range(multiplier):
        for report in reports:
            cloned = copy.deepcopy(report)
            cloned["latency_benchmark_copy"] = copy_index
            expanded.append(cloned)
    return expanded


def load_anchor(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def build_report(
    inputs: list[Path], multipliers: list[int], certified: Path
) -> dict[str, Any]:
    base_reports = [load_json(path) for path in inputs]
    rows = []
    anchor = load_anchor(certified)
    if anchor:
        rows.append(
            summarize_schedule("certified_one_copy", 1, anchor, display_path(certified))
        )

    for multiplier in multipliers:
        schedule = build_compilation(
            multiply_reports(base_reports, multiplier),
            exact_backend="off",
            exact_time_limit_s=1.0,
            optimize_policy="clock-slots",
        )
        rows.append(
            summarize_schedule(
                f"deterministic_{multiplier}x", multiplier, schedule, "rebuilt"
            )
        )

    checks = {
        "rows_present": bool(rows),
        "all_rows_pass": all(row["status"] == "PASS" for row in rows),
        "all_native_total_clock_lte_active": all(
            row["clock_native_policy"]["total_clock_slots"]
            <= row["active_policy"]["total_clock_slots"]
            for row in rows
        ),
        "some_packets_finish_earlier_native": any(
            row["packet_delta_summary"]["native_faster_packet_count"] > 0
            for row in rows
        ),
        "all_native_connector_free": all(
            row["clock_native_policy"]["total_connectors"] == 0 for row in rows
        ),
    }
    return {
        "schema": "w33.packet_latency_benchmark.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "inputs": [display_path(path) for path in inputs],
        "multipliers": multipliers,
        "benchmark_rows": rows,
        "theorem_checks": checks,
        "interpretation": (
            "This is packet-completion latency over the Holonet control-plane DAG. It measures completion "
            "in active ticks and in elapsed SRG(36,15,6,6) frame-clock slots. It does not benchmark child "
            "process arithmetic."
        ),
    }


def parse_multipliers(raw: str) -> list[int]:
    values = [int(part.strip()) for part in raw.split(",") if part.strip()]
    if not values or any(value < 1 for value in values):
        raise argparse.ArgumentTypeError("multipliers must be positive integers")
    return values


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUTPUT), help="output JSON")
    parser.add_argument(
        "--multipliers",
        type=parse_multipliers,
        default=parse_multipliers("1,2,3,4"),
        help="comma-separated deterministic workload repetition factors",
    )
    parser.add_argument(
        "--certified", default=str(DEFAULT_CERTIFIED), help="certified compiler JSON"
    )
    parser.add_argument("inputs", nargs="*", help="Holonet wrapper reports")
    args = parser.parse_args(argv)

    inputs = (
        [normalize_path(path) for path in args.inputs]
        if args.inputs
        else DEFAULT_INPUTS
    )
    certified = normalize_path(args.certified)
    report = build_report(inputs, args.multipliers, certified)
    output = normalize_path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"status: {report['status']}")
    for row in report["benchmark_rows"]:
        print(
            f"{row['label']}: packets={row['packet_count']} "
            f"active={row['active_policy']['total_ticks']}t/{row['active_policy']['total_clock_slots']}s "
            f"native={row['clock_native_policy']['total_ticks']}t/{row['clock_native_policy']['total_clock_slots']}s "
            f"faster_packets={row['packet_delta_summary']['native_faster_packet_count']}"
        )
    print(f"wrote: {display_path(output)}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
