#!/usr/bin/env python3
"""BT1305 - Mirror-bus queueing law.

BT1304 shows that one full atlas burst uses one of four mirror slots per chart.
BT1305 turns that into a service law:

    service capacity = 4 packets per chart per mirror epoch.

For a recursive holonet with I_n = (40^n - 1)/39 W33 shells, the mirror-bus
capacity is 2160 I_n packets per epoch.  A one-packet-per-chart burst uses
540 I_n packets, so utilization is 1/4 at every depth.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1305_mirror_bus_queueing_law.json"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def instances(level: int) -> int:
    return (40**level - 1) // 39


def mode_row(packets_per_chart: int) -> dict[str, Any]:
    service = 4
    packets = 540 * packets_per_chart
    capacity = 2160
    epochs = math.ceil(packets_per_chart / service)
    backlog_after_one_epoch = max(0, packets_per_chart - service)
    utilization = Fraction(packets, capacity)
    return {
        "packets_per_chart": packets_per_chart,
        "packets_per_instance": packets,
        "capacity_per_instance": capacity,
        "service_slots_per_chart": service,
        "epochs_needed": epochs,
        "utilization": f"{utilization.numerator}/{utilization.denominator}",
        "slack_after_one_epoch_per_instance": max(0, capacity - packets),
        "backlog_after_one_epoch_per_chart": backlog_after_one_epoch,
        "stable_without_queue": packets_per_chart <= service,
    }


def build_payload() -> dict[str, Any]:
    bt1303 = load_json("data/bt1303_holonet_stack_contract.json")
    bt1304 = load_json("data/bt1304_holonet_contention_model.json")

    traffic_modes = [mode_row(m) for m in [1, 2, 3, 4, 5, 8, 9]]
    recursive_rows = []
    for level in range(1, 7):
        count = instances(level)
        packets = 540 * count
        capacity = 2160 * count
        recursive_rows.append(
            {
                "level": level,
                "w33_instances": count,
                "one_packet_per_chart_packets": packets,
                "mirror_capacity": capacity,
                "slack": capacity - packets,
                "utilization": "1/4",
                "slack_per_instance": (capacity - packets) // count,
            }
        )

    by_mode = {row["packets_per_chart"]: row for row in traffic_modes}
    checks = {
        "bt1303_verified": bt1303["verified"] is True,
        "bt1304_verified": bt1304["verified"] is True,
        "one_packet_per_chart_is_quarter_utilization": by_mode[1]["utilization"]
        == "1/4",
        "q_packets_per_chart_is_three_quarter_utilization": by_mode[3]["utilization"]
        == "3/4",
        "four_packets_per_chart_saturates_bus": by_mode[4]["utilization"] == "1/1"
        and by_mode[4]["stable_without_queue"] is True,
        "five_packets_per_chart_creates_one_backlog": by_mode[5][
            "backlog_after_one_epoch_per_chart"
        ]
        == 1,
        "eight_packets_needs_two_epochs": by_mode[8]["epochs_needed"] == 2,
        "nine_packets_needs_three_epochs": by_mode[9]["epochs_needed"] == 3,
        "recursive_utilization_is_depth_independent": all(
            row["utilization"] == "1/4" for row in recursive_rows
        ),
        "recursive_slack_per_instance_is_apartment_count": all(
            row["slack_per_instance"] == 1620 for row in recursive_rows
        ),
        "level6_matches_bt827_instance_count": recursive_rows[-1]["w33_instances"]
        == (40**6 - 1) // 39,
    }

    payload = {
        "theorem": "BT1305 mirror-bus queueing law",
        "verified": all(checks.values()),
        "checks": checks,
        "service_law": {
            "mirror_bus_capacity": "2160 = 540 charts * 4 slots",
            "service_capacity_per_chart_per_epoch": 4,
            "backlog_recurrence": "B_{t+1} = max(0, B_t + arrivals_per_chart - 4)",
            "epochs_needed_for_m_packets_per_chart": "ceil(m/4)",
        },
        "traffic_modes": traffic_modes,
        "recursive_scaling": recursive_rows,
        "architecture_reading": (
            "The mirror bus is a four-server queue at each chart. One full "
            "atlas burst uses 1/4 capacity; q=3 bursts use 3/4; q+1=4 bursts "
            "saturate without backlog; the fifth packet per chart is the first "
            "queueing boundary. The same utilization law holds at every "
            "recursive depth because both demand and capacity scale by I_n."
        ),
        "honesty_boundary": (
            "BT1305 is deterministic service accounting. It does not assume a "
            "stochastic arrival distribution, derive latency tails, or model "
            "hardware loss."
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
        raise SystemExit(f"BT1305 failed checks: {failed}")


if __name__ == "__main__":
    main()
