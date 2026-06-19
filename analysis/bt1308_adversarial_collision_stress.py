#!/usr/bin/env python3
"""BT1308 - Adversarial collision stress for the mirror bus.

BT1305 says service capacity is local: four packets per chart per mirror epoch.
BT1308 stresses that law with adversarial traffic.  The main result is a
negative design rule:

    global utilization is not enough.

An all-to-one burst has the same global packet count as the balanced atlas
burst, 540 packets = 1/4 of the bus, but needs 135 epochs because one chart is
overloaded.  A one-chart hot spot with only four extra packets already creates
backlog despite global utilization still barely above 1/4.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1308_adversarial_collision_stress.json"
CHARTS = 540
SERVICE = 4
BUS = 2160


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def frac(num: int, den: int) -> str:
    value = Fraction(num, den)
    return f"{value.numerator}/{value.denominator}"


def case_stats(name: str, counts: list[int], reading: str) -> dict[str, Any]:
    total = sum(counts)
    max_count = max(counts)
    backlog = sum(max(0, count - SERVICE) for count in counts)
    conflicts = sum(max(0, count - 1) for count in counts)
    hot_charts = sum(1 for count in counts if count > SERVICE)
    return {
        "case": name,
        "total_packets": total,
        "global_utilization": frac(total, BUS),
        "max_packets_on_one_chart": max_count,
        "epochs_needed": math.ceil(max_count / SERVICE),
        "output_conflicts": conflicts,
        "backlog_after_one_epoch": backlog,
        "hot_charts_over_capacity": hot_charts,
        "multiplicity_histogram": dict(sorted(Counter(counts).items())),
        "stable_after_one_epoch": backlog == 0,
        "architecture_reading": reading,
    }


def build_payload() -> dict[str, Any]:
    bt1304 = load_json("data/bt1304_holonet_contention_model.json")
    bt1305 = load_json("data/bt1305_mirror_bus_queueing_law.json")

    balanced = [1] * CHARTS
    q_per_chart = [3] * CHARTS
    saturated = [4] * CHARTS
    first_global_overflow = [5] * CHARTS
    single_hot_boundary = [1] * CHARTS
    single_hot_boundary[0] = 5
    all_to_one = [0] * CHARTS
    all_to_one[0] = CHARTS

    cases = [
        case_stats(
            "balanced_atlas",
            balanced,
            "BT1304 baseline: one packet per chart, zero output contention.",
        ),
        case_stats(
            "q_per_chart",
            q_per_chart,
            "Ternary load: three packets per chart uses 3/4 of the bus and queues nowhere.",
        ),
        case_stats(
            "saturated_q_plus_1",
            saturated,
            "Four packets per chart saturates the local mirror service without backlog.",
        ),
        case_stats(
            "first_global_overflow",
            first_global_overflow,
            "Five packets per chart creates one full-atlas backlog after one epoch.",
        ),
        case_stats(
            "single_hot_chart_boundary",
            single_hot_boundary,
            "Four extra packets aimed at one chart create backlog although global utilization is near 1/4.",
        ),
        case_stats(
            "all_to_one_collapse",
            all_to_one,
            "Same packet count as the balanced atlas, but address entropy collapses to one chart.",
        ),
    ]
    by_case = {row["case"]: row for row in cases}

    checks = {
        "bt1304_verified": bt1304["verified"] is True,
        "bt1305_verified": bt1305["verified"] is True,
        "balanced_matches_bt1304": by_case["balanced_atlas"]["output_conflicts"] == 0
        and by_case["balanced_atlas"]["global_utilization"] == "1/4",
        "q_per_chart_has_no_backlog": by_case["q_per_chart"]["stable_after_one_epoch"]
        is True
        and by_case["q_per_chart"]["global_utilization"] == "3/4",
        "q_plus_1_saturates_without_backlog": by_case["saturated_q_plus_1"][
            "stable_after_one_epoch"
        ]
        is True
        and by_case["saturated_q_plus_1"]["global_utilization"] == "1/1",
        "five_per_chart_backlogs_one_atlas": by_case["first_global_overflow"][
            "backlog_after_one_epoch"
        ]
        == CHARTS,
        "single_hot_chart_backlogs_below_one_third_global_utilization": by_case[
            "single_hot_chart_boundary"
        ]["backlog_after_one_epoch"]
        == 1
        and Fraction(544, BUS) < Fraction(1, 3),
        "all_to_one_same_global_utilization_as_balanced": by_case[
            "all_to_one_collapse"
        ]["global_utilization"]
        == by_case["balanced_atlas"]["global_utilization"],
        "all_to_one_needs_135_epochs": by_case["all_to_one_collapse"]["epochs_needed"]
        == 135,
        "global_average_does_not_determine_latency": by_case["balanced_atlas"][
            "global_utilization"
        ]
        == by_case["all_to_one_collapse"]["global_utilization"]
        and by_case["balanced_atlas"]["epochs_needed"]
        != by_case["all_to_one_collapse"]["epochs_needed"],
    }

    payload = {
        "theorem": "BT1308 adversarial collision stress",
        "verified": all(checks.values()),
        "checks": checks,
        "stress_cases": cases,
        "design_rule": {
            "local_service_capacity": "4 packets per chart per mirror epoch",
            "global_average_warning": (
                "Two traffic patterns can have identical global utilization "
                "and radically different latency if their chart multiplicity "
                "profiles differ."
            ),
            "routing_requirement": (
                "The holonet must preserve chart-entropy/load spreading; "
                "otherwise a 1/4-full bus can still queue for 135 epochs."
            ),
        },
        "architecture_reading": (
            "BT1308 turns the queue law into a network design constraint. The "
            "balanced atlas is not merely pretty symmetry; it is the condition "
            "that keeps the mirror bus low-latency. Local chart multiplicity, "
            "not global packet count, controls queueing."
        ),
        "honesty_boundary": (
            "BT1308 is worst-case deterministic traffic accounting. It does "
            "not model stochastic arrivals, analog loss, or adaptive online "
            "routing beyond the fixed mirror service law."
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
        raise SystemExit(f"BT1308 failed checks: {failed}")


if __name__ == "__main__":
    main()
