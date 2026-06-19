#!/usr/bin/env python3
"""BT1307 - Holonet latency classes.

BT1304 and BT1305 gave load and service capacity.  BT1307 extracts the
deterministic latency classes already present in the full 540-chart atlas.

The surprise is a dual utilization law:

    route-word compute utilization = 3240 / (540 * 8) = 3/4,
    mirror-bus transport utilization = 540 / 2160 = 1/4.

So the same full-atlas burst is compute-dense and transport-sparse.  The
unused 1/4 of the word is local instruction slack; the unused 3/4 of the bus is
global routing headroom.
"""
from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1307_holonet_latency_classes.json"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def frac(num: int, den: int) -> str:
    value = Fraction(num, den)
    return f"{value.numerator}/{value.denominator}"


def build_payload() -> dict[str, Any]:
    bt1301 = load_json("data/bt1301_full_chart_atlas_isa_compiler.json")
    bt1304 = load_json("data/bt1304_holonet_contention_model.json")
    bt1305 = load_json("data/bt1305_mirror_bus_queueing_law.json")
    bt1306 = load_json("data/bt1306_physical_timing_model.json")

    routes = bt1301["atlas_routes"]
    word_ticks = bt1306["durations"]["word"]["tau_units"]
    completion_ticks = []
    idle_ticks = []
    for route in routes:
        completion = max(route["active_ticks"]) + 1
        completion_ticks.append(completion)
        idle_ticks.append(word_ticks - completion)

    completion_hist = Counter(completion_ticks)
    idle_hist = Counter(idle_ticks)
    total_active = sum(completion_ticks)
    total_reserved = len(routes) * word_ticks
    total_idle = total_reserved - total_active

    latency_classes = [
        {
            "completion_tick_tau": tick,
            "route_count": completion_hist[tick],
            "idle_ticks_after_completion": word_ticks - tick,
            "class_fraction": frac(completion_hist[tick], len(routes)),
        }
        for tick in sorted(completion_hist)
    ]

    checks = {
        "bt1301_verified": bt1301["verified"] is True,
        "bt1304_verified": bt1304["verified"] is True,
        "bt1305_verified": bt1305["verified"] is True,
        "bt1306_verified": bt1306["verified"] is True,
        "completion_ticks_equal_active_tick_counts": all(
            max(route["active_ticks"]) + 1 == route["active_tick_count"]
            for route in routes
        ),
        "latency_classes_are_4_through_8": dict(sorted(completion_hist.items()))
        == {4: 108, 5: 108, 6: 108, 7: 108, 8: 108},
        "idle_classes_are_0_through_4": dict(sorted(idle_hist.items()))
        == {0: 108, 1: 108, 2: 108, 3: 108, 4: 108},
        "mean_completion_is_six_ticks": mean(completion_ticks) == 6,
        "compute_utilization_is_three_quarters": frac(total_active, total_reserved)
        == "3/4",
        "instruction_slack_is_one_quarter": frac(total_idle, total_reserved) == "1/4",
        "mirror_transport_utilization_is_one_quarter": bt1304["contention_summary"][
            "mirror_bus_utilization"
        ]
        == "540/2160 = 1/4",
        "compute_plus_transport_utilizations_sum_to_one": Fraction(
            total_active, total_reserved
        )
        + Fraction(540, 2160)
        == 1,
        "q_packet_queue_mode_matches_compute_utilization": next(
            row for row in bt1305["traffic_modes"] if row["packets_per_chart"] == 3
        )["utilization"]
        == "3/4",
    }

    payload = {
        "theorem": "BT1307 holonet latency classes",
        "verified": all(checks.values()),
        "checks": checks,
        "latency_classes": latency_classes,
        "latency_summary": {
            "routes": len(routes),
            "word_ticks_tau": word_ticks,
            "min_completion_tau": min(completion_ticks),
            "max_completion_tau": max(completion_ticks),
            "mean_completion_tau": mean(completion_ticks),
            "total_active_ticks": total_active,
            "total_reserved_ticks": total_reserved,
            "total_idle_ticks": total_idle,
            "compute_utilization": frac(total_active, total_reserved),
            "instruction_slack": frac(total_idle, total_reserved),
            "mirror_transport_utilization": "1/4",
            "dual_utilization_identity": "3/4 compute + 1/4 mirror = 1",
        },
        "architecture_reading": (
            "The atlas burst completes in five equally populated latency "
            "classes, 4..8 tau, with mean 6 tau. Across all 540 routes, the "
            "8-tick word is 3/4 active and 1/4 idle. This is exactly dual to "
            "the BT1304 mirror-bus reading: the same burst uses only 1/4 of "
            "the transport bus. The holonet therefore keeps local compute "
            "dense while reserving global bus headroom."
        ),
        "honesty_boundary": (
            "BT1307 is deterministic schedule latency in tick units. It does "
            "not model analog propagation delay, switch settling time, loss, "
            "or detector jitter."
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
        raise SystemExit(f"BT1307 failed checks: {failed}")


if __name__ == "__main__":
    main()
