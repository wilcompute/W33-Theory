#!/usr/bin/env python3
"""BT1302 - Parity epilogue reroute protocol.

BT1300 identified six F3 parity lanes in the local-lift epilogue.  BT1301
showed that every chart has five all-XOR ingress choices.  BT1302 turns the
six parity lanes into an active recovery table:

    for each chart and each failed column-pair syndrome,
    choose an ingress route whose own column-pair carrier avoids that syndrome.

The result is a 540 x 6 = 3240-entry reroute table.  Every chart has a safe
choice for every syndrome, and every chosen reroute still fits one BT1300
8-tick word.
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any

from bt1301_full_chart_atlas_isa_compiler import (
    CHART_COUNT,
    candidate_palette_for_chart,
    chosen_route_for_chart,
    slim_route,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1302_parity_epilogue_reroute_protocol.json"

COLUMN_PAIRS = tuple(combinations(range(4), 2))


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def pair_label(pair: tuple[int, int]) -> str:
    return f"{pair[0]}_{pair[1]}"


def parity_pair_for_route(row: dict[str, Any]) -> tuple[int, int]:
    # Local column: which of the five all-XOR ingress digits 7,15,23,31,39.
    # Global column: chart residue in the 4-column CSS sheet.
    local_column = (row["target_digit"] // 8) % 4
    global_column = row["target_chart"] % 4
    if local_column == global_column:
        global_column = (global_column + 1) % 4
    return tuple(sorted((local_column, global_column)))


def choose_recovery(chart: int, failed_pair: tuple[int, int]) -> dict[str, Any]:
    base = chosen_route_for_chart(chart)
    base_pair = parity_pair_for_route(base)
    if base_pair != failed_pair:
        chosen = base
        changed = False
    else:
        alternatives = [
            row
            for row in candidate_palette_for_chart(chart)
            if parity_pair_for_route(row) != failed_pair
        ]
        alternatives.sort(
            key=lambda row: (
                row["reversible_moves"],
                parity_pair_for_route(row),
                row["target_digit"],
                row["depth"],
            )
        )
        chosen = alternatives[0]
        changed = True
    chosen_pair = parity_pair_for_route(chosen)
    return {
        "chart": chart,
        "failed_pair": list(failed_pair),
        "failed_lane": pair_label(failed_pair),
        "base_pair": list(base_pair),
        "chosen_pair": list(chosen_pair),
        "changed_route": changed,
        "recovery_route": slim_route(chosen),
        "avoids_failed_pair": chosen_pair != failed_pair,
    }


def build_payload() -> dict[str, Any]:
    bt1300 = load_json("data/bt1300_oscillator_instruction_isa.json")
    bt1301 = load_json("data/bt1301_full_chart_atlas_isa_compiler.json")

    parity_lanes = [lane for lane in bt1300["lane_layout"] if lane["kind"] == "parity"]
    parity_pairs = [tuple(lane["column_pair"]) for lane in parity_lanes]

    recovery_table = [
        choose_recovery(chart, failed_pair)
        for chart in range(CHART_COUNT)
        for failed_pair in COLUMN_PAIRS
    ]
    changed = [row for row in recovery_table if row["changed_route"]]
    by_failed_lane = Counter(row["failed_lane"] for row in recovery_table)
    changed_by_failed_lane = Counter(row["failed_lane"] for row in changed)
    base_pair_distribution = Counter(
        pair_label(parity_pair_for_route(chosen_route_for_chart(chart)))
        for chart in range(CHART_COUNT)
    )
    max_recovery_ticks = max(
        row["recovery_route"]["active_tick_count"] for row in recovery_table
    )

    checks = {
        "bt1300_isa_verified": bt1300["verified"] is True,
        "bt1301_atlas_verified": bt1301["verified"] is True,
        "six_parity_lanes_match_column_pairs": tuple(parity_pairs) == COLUMN_PAIRS,
        "recovery_table_has_540_by_6_entries": len(recovery_table)
        == CHART_COUNT * len(COLUMN_PAIRS),
        "each_failed_lane_has_540_actions": all(
            by_failed_lane[pair_label(pair)] == CHART_COUNT for pair in COLUMN_PAIRS
        ),
        "every_action_avoids_failed_pair": all(
            row["avoids_failed_pair"] for row in recovery_table
        ),
        "every_recovery_fits_one_word": max_recovery_ticks <= 8,
        "only_failed_base_pair_forces_route_change": all(
            row["changed_route"]
            == (tuple(row["base_pair"]) == tuple(row["failed_pair"]))
            for row in recovery_table
        ),
        "one_changed_action_per_chart": len(changed) == CHART_COUNT,
        "all_six_lanes_have_live_changes": all(
            changed_by_failed_lane[pair_label(pair)] > 0 for pair in COLUMN_PAIRS
        ),
        "changed_routes_remain_nontrivial": all(
            row["recovery_route"]["source_chart"]
            != row["recovery_route"]["target_chart"]
            for row in changed
        ),
    }

    payload = {
        "theorem": "BT1302 parity epilogue reroute protocol",
        "verified": all(checks.values()),
        "checks": checks,
        "protocol": {
            "parity_lanes": [
                {
                    "lane": lane["lane"],
                    "column_pair": lane["column_pair"],
                    "coordinate": lane["coordinate"],
                }
                for lane in parity_lanes
            ],
            "recovery_actions": len(recovery_table),
            "changed_actions": len(changed),
            "base_pair_distribution": dict(sorted(base_pair_distribution.items())),
            "changed_by_failed_lane": dict(sorted(changed_by_failed_lane.items())),
            "max_recovery_active_ticks": max_recovery_ticks,
            "rule": (
                "If the packet's column-pair carrier is not the failed syndrome, "
                "keep the route. If it is the failed syndrome, switch to the "
                "lowest-cost all-XOR candidate for the same chart whose carrier "
                "uses a different column pair."
            ),
        },
        "recovery_table": recovery_table,
        "architecture_reading": (
            "The final six parity lanes of the BT1300 epilogue are active route "
            "controls. Each column-pair syndrome selects a safe ingress for every "
            "one of the 540 charts. The common case keeps the packet; the single "
            "matching failed pair per chart switches to another all-XOR candidate "
            "while staying inside one 8-tick word."
        ),
        "honesty_boundary": (
            "BT1302 is a deterministic syndrome-to-reroute table for the atlas "
            "ingress layer. It does not yet simulate stochastic noise, repeated "
            "faults, or congestion across multiple simultaneous packets."
        ),
    }
    return payload


def main() -> None:
    payload = build_payload()
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "theorem": payload["theorem"],
                "verified": payload["verified"],
                "checks_passed": sum(payload["checks"].values()),
                "checks_total": len(payload["checks"]),
                "out": str(OUT.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not payload["verified"]:
        failed = [name for name, passed in payload["checks"].items() if not passed]
        raise SystemExit(f"BT1302 failed checks: {failed}")


if __name__ == "__main__":
    main()
