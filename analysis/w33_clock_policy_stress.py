#!/usr/bin/env python3
"""Stress-test active-tick vs frame-clock-native Holonet compilation policies.

The exact MILP certificate is practical for the current demo packet DAG.  For
larger wrapped workloads this script scales the same wrapper reports and compares
the deterministic active packer against the clock-native packer.  The goal is not
to overclaim optimality; it is to test whether the architectural tradeoff remains:
fewest active ticks can still be a worse elapsed frame-clock program than a
schedule compiled directly on the SRG(36,15,6,6) clock graph.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from w33_line_context_compiler import build_compilation
from w33_spread_contextual_microkernel_bridge import (
    DEFAULT_INPUTS,
    load_json,
    normalize_path,
)
from w33_uor_runtime_model import ROOT

DEFAULT_OUTPUT = ROOT / "data" / "w33_clock_policy_stress.json"
DEFAULT_CERTIFIED = ROOT / "data" / "w33_line_context_compiler.json"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_certified_anchor(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    report = json.loads(path.read_text(encoding="utf-8"))
    active = report["active_schedule"]
    native = report["clock_native_schedule"]
    selected = report["optimizer"].get("selected_policy_schedule", {})
    return {
        "source": str(path.relative_to(ROOT)),
        "status": report["status"],
        "optimality": report["optimizer"]["optimality_status"],
        "exact_backend": report["optimizer"]["exact_backend"]["status"],
        "selected_policy": selected.get("policy"),
        "packet_count": report["input"]["packet_count"],
        "job_count": report["lowering"]["job_count"],
        "active_ticks": active["tick_count"],
        "active_clock_slots": active["clock_embedding"]["clock_slot_count"],
        "active_connectors": active["clock_embedding"]["connector_slot_count"],
        "clock_native_ticks": native["tick_count"],
        "clock_native_clock_slots": native["clock_slot_count"],
        "clock_native_connectors": native["connector_slot_count"],
        "active_tick_delta": native["tick_count"] - active["tick_count"],
        "clock_slot_savings": active["clock_embedding"]["clock_slot_count"]
        - native["clock_slot_count"],
        "certified_tradeoff": (
            report["optimizer"]["optimality_status"] == "optimal_certified"
            and native["tick_count"] >= active["tick_count"]
            and native["clock_slot_count"]
            < active["clock_embedding"]["clock_slot_count"]
            and native["connector_slot_count"] == 0
        ),
    }


def multiply_reports(
    reports: list[dict[str, Any]], multiplier: int
) -> list[dict[str, Any]]:
    expanded = []
    for copy_index in range(multiplier):
        for report in reports:
            cloned = copy.deepcopy(report)
            cloned["stress_copy"] = copy_index
            expanded.append(cloned)
    return expanded


def summarize_compilation(multiplier: int, report: dict[str, Any]) -> dict[str, Any]:
    active = report["active_schedule"]
    native = report["clock_native_schedule"]
    active_clock = active["clock_embedding"]
    return {
        "multiplier": multiplier,
        "packet_count": report["input"]["packet_count"],
        "job_count": report["lowering"]["job_count"],
        "active_policy": {
            "ticks": active["tick_count"],
            "clock_slots": active_clock["clock_slot_count"],
            "connectors": active_clock["connector_slot_count"],
            "schedule_hash": active["schedule_hash"],
        },
        "clock_native_policy": {
            "ticks": native["tick_count"],
            "clock_slots": native["clock_slot_count"],
            "connectors": native["connector_slot_count"],
            "schedule_hash": native["schedule_hash"],
        },
        "deltas": {
            "clock_native_minus_active_ticks": native["tick_count"]
            - active["tick_count"],
            "clock_slot_savings": active_clock["clock_slot_count"]
            - native["clock_slot_count"],
            "connector_savings": active_clock["connector_slot_count"]
            - native["connector_slot_count"],
        },
        "checks": {
            "active_verified": active["verification"]["ok"],
            "clock_native_verified": native["verification"]["ok"],
            "clock_native_connector_free": native["connector_slot_count"] == 0,
            "clock_native_saves_clock_slots": native["clock_slot_count"]
            < active_clock["clock_slot_count"],
        },
        "boundary": (
            "Scaled rows use deterministic schedulers with exact verification, not a global MILP optimum. "
            "Use the certified anchor row for the one-copy optimality claim."
        ),
    }


def build_report(
    inputs: list[Path], multipliers: list[int], certified: Path
) -> dict[str, Any]:
    base_reports = [load_json(path) for path in inputs]
    rows = []
    for multiplier in multipliers:
        compilation = build_compilation(
            multiply_reports(base_reports, multiplier),
            exact_backend="off",
            exact_time_limit_s=1.0,
            optimize_policy="clock-slots",
        )
        rows.append(summarize_compilation(multiplier, compilation))

    checks = {
        "stress_rows_executed": len(rows) == len(multipliers),
        "all_scaled_schedules_verify": all(
            row["checks"]["active_verified"] and row["checks"]["clock_native_verified"]
            for row in rows
        ),
        "all_clock_native_connector_free": all(
            row["checks"]["clock_native_connector_free"] for row in rows
        ),
        "all_clock_native_save_clock_slots": all(
            row["checks"]["clock_native_saves_clock_slots"] for row in rows
        ),
    }
    anchor = load_certified_anchor(certified)
    checks["certified_one_copy_tradeoff_loaded"] = bool(
        anchor and anchor["certified_tradeoff"]
    )

    return {
        "schema": "w33.clock_policy_stress.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "inputs": [str(path.relative_to(ROOT)) for path in inputs],
        "multipliers": multipliers,
        "certified_anchor": anchor,
        "scaled_policy_rows": rows,
        "theorem_checks": checks,
        "interpretation": (
            "The exact demo row proves the 14-active-tick optimum, while the scaled rows test the same policy "
            "choice on larger wrapper DAGs. Across these deterministic stress cases, compiling on the clock "
            "graph removes connector frames and reduces elapsed SRG(36,15,6,6) slots even when it is not the "
            "fewest-active-tick program."
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
        default=parse_multipliers("1,2,3,4,5,6"),
        help="comma-separated workload repetition factors",
    )
    parser.add_argument(
        "--certified",
        default=str(DEFAULT_CERTIFIED),
        help="existing exact compiler JSON used as the one-copy certified anchor",
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
    anchor = report.get("certified_anchor")
    if anchor:
        print(
            "certified anchor: "
            f"{anchor['active_ticks']} active ticks -> {anchor['active_clock_slots']} clock slots; "
            f"native {anchor['clock_native_ticks']} ticks -> {anchor['clock_native_clock_slots']} slots"
        )
    for row in report["scaled_policy_rows"]:
        print(
            f"x{row['multiplier']}: "
            f"active {row['active_policy']['ticks']}t/{row['active_policy']['clock_slots']}s; "
            f"native {row['clock_native_policy']['ticks']}t/{row['clock_native_policy']['clock_slots']}s; "
            f"save {row['deltas']['clock_slot_savings']} slots"
        )
    print(f"wrote: {display_path(output)}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
