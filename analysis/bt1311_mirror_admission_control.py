#!/usr/bin/env python3
"""BT1311 - Mirror admission-control law.

BT1310 can route any admitted burst up to 2160 packets into one mirror epoch.
BT1311 turns that into a frame-level admission controller.

The law is simple:

    admitted_per_epoch = min(backlog + arrivals, 2160)
    spill = max(0, backlog + arrivals - 2160)

This is the executable boundary between "route now" and "defer to the next
mirror epoch".
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1311_mirror_admission_control.json"
CAPACITY = 2160


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def frac(num: int, den: int) -> str:
    value = Fraction(num, den)
    return f"{value.numerator}/{value.denominator}"


def admit(total_packets: int) -> dict[str, Any]:
    admitted = min(total_packets, CAPACITY)
    spill = max(0, total_packets - CAPACITY)
    return {
        "arrival_packets": total_packets,
        "admitted_epoch_0": admitted,
        "spill_after_epoch_0": spill,
        "epochs_needed": math.ceil(total_packets / CAPACITY) if total_packets else 0,
        "first_epoch_utilization": frac(admitted, CAPACITY),
        "final_epoch_packets": total_packets % CAPACITY
        or (CAPACITY if total_packets else 0),
    }


def parallel_admit(total_packets: int, instances: int) -> dict[str, Any]:
    capacity = CAPACITY * instances
    admitted = min(total_packets, capacity)
    spill = max(0, total_packets - capacity)
    return {
        "arrival_packets": total_packets,
        "w33_instances": instances,
        "parallel_capacity": capacity,
        "admitted_epoch_0": admitted,
        "spill_after_epoch_0": spill,
        "epochs_needed": math.ceil(total_packets / capacity) if total_packets else 0,
        "first_epoch_utilization": frac(admitted, capacity),
    }


def build_payload() -> dict[str, Any]:
    bt1310 = load_json("data/bt1310_entropy_preserving_router.json")

    level6_instances = 105025641
    arrivals = {
        "balanced_atlas": 540,
        "q_per_chart": 1620,
        "saturated": 2160,
        "first_overflow": 2700,
        "double_epoch": 4320,
        "double_plus_one": 4321,
        "level6_one_packet_per_chart_serialized": level6_instances * 540,
    }
    admission_cases = {name: admit(count) for name, count in arrivals.items()}
    parallel_cases = {
        "level6_one_packet_per_chart_parallel": parallel_admit(
            level6_instances * 540, level6_instances
        )
    }

    checks = {
        "bt1310_verified": bt1310["verified"] is True,
        "balanced_admits_one_quarter": admission_cases["balanced_atlas"][
            "first_epoch_utilization"
        ]
        == "1/4",
        "q_per_chart_admits_three_quarters": admission_cases["q_per_chart"][
            "first_epoch_utilization"
        ]
        == "3/4",
        "saturated_admits_full_epoch": admission_cases["saturated"][
            "first_epoch_utilization"
        ]
        == "1/1",
        "first_overflow_spills_one_atlas": admission_cases["first_overflow"][
            "spill_after_epoch_0"
        ]
        == 540,
        "double_epoch_has_no_final_spill": admission_cases["double_epoch"][
            "epochs_needed"
        ]
        == 2
        and admission_cases["double_epoch"]["final_epoch_packets"] == CAPACITY,
        "double_plus_one_needs_third_epoch": admission_cases["double_plus_one"][
            "epochs_needed"
        ]
        == 3
        and admission_cases["double_plus_one"]["final_epoch_packets"] == 1,
        "level6_serialization_cost_is_exact": admission_cases[
            "level6_one_packet_per_chart_serialized"
        ]["arrival_packets"]
        == level6_instances * 540
        and admission_cases["level6_one_packet_per_chart_serialized"]["epochs_needed"]
        == level6_instances // 4 + 1,
        "level6_parallel_shell_admits_in_one_epoch": parallel_cases[
            "level6_one_packet_per_chart_parallel"
        ]["epochs_needed"]
        == 1
        and parallel_cases["level6_one_packet_per_chart_parallel"][
            "first_epoch_utilization"
        ]
        == "1/4",
    }

    payload = {
        "theorem": "BT1311 mirror admission-control law",
        "verified": all(checks.values()),
        "checks": checks,
        "admission_law": {
            "capacity_per_instance_per_epoch": CAPACITY,
            "admitted_per_epoch": "min(backlog + arrivals, 2160)",
            "spill": "max(0, backlog + arrivals - 2160)",
            "epochs_needed": "ceil(total_packets / 2160)",
            "parallel_scaling_note": (
                "A recursive holonet does not have to serialize all instances "
                "through one bus. With I_n instances, capacity is 2160 I_n."
            ),
        },
        "admission_cases": admission_cases,
        "parallel_admission_cases": parallel_cases,
        "architecture_reading": (
            "BT1311 separates local admission from global serialization. One "
            "W33 instance admits at most 2160 packets per mirror epoch; a "
            "recursive shell admits 2160 times its W33 instance count in "
            "parallel. The controller therefore rejects or defers overflow "
            "without changing the BT1310 in-epoch router."
        ),
        "honesty_boundary": (
            "BT1311 is deterministic admission arithmetic. It does not model "
            "random arrivals, QoS policy, physical buffering, or packet loss."
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
        raise SystemExit(f"BT1311 failed checks: {failed}")


if __name__ == "__main__":
    main()
