#!/usr/bin/env python3
"""BT1310 - Entropy-preserving mirror router.

BT1308 proved that global utilization does not determine latency: 540 packets
can take either one epoch or 135 epochs depending on chart multiplicity.

BT1310 adds the missing deterministic router.  For each requested chart, place
the packet in the first cyclic chart with remaining local mirror capacity.  The
rule preserves already-balanced traffic, but spreads hot spots so any admitted
burst of at most 2160 packets has max chart load <= 4.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1310_entropy_preserving_router.json"
CHARTS = 540
SERVICE = 4
CAPACITY = CHARTS * SERVICE


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def requests_from_counts(counts: list[int]) -> list[int]:
    requests: list[int] = []
    for chart, count in enumerate(counts):
        requests.extend([chart] * count)
    return requests


def spread_route(requests: list[int]) -> dict[str, Any]:
    loads = [0] * CHARTS
    assignments = []
    rejected = 0
    displacements = []
    for packet_id, requested in enumerate(requests):
        placed = None
        for offset in range(CHARTS):
            candidate = (requested + offset) % CHARTS
            if loads[candidate] < SERVICE:
                placed = candidate
                break
        if placed is None:
            rejected += 1
            continue
        loads[placed] += 1
        displacements.append((placed - requested) % CHARTS)
        assignments.append(
            {
                "packet_id": packet_id,
                "requested_chart": requested,
                "assigned_chart": placed,
                "cyclic_displacement": (placed - requested) % CHARTS,
            }
        )
    max_load = max(loads) if loads else 0
    return {
        "accepted": len(assignments),
        "rejected": rejected,
        "max_chart_load": max_load,
        "epochs_needed": math.ceil(max_load / SERVICE) if max_load else 0,
        "nonempty_charts": sum(1 for load in loads if load),
        "load_histogram": dict(sorted(Counter(loads).items())),
        "max_displacement": max(displacements) if displacements else 0,
        "mean_displacement": mean(displacements) if displacements else 0,
        "zero_displacement_packets": sum(1 for d in displacements if d == 0),
        "assignments_sample": assignments[:16],
    }


def stress_counts() -> dict[str, list[int]]:
    balanced = [1] * CHARTS
    q_per_chart = [3] * CHARTS
    saturated = [4] * CHARTS
    single_hot = [1] * CHARTS
    single_hot[0] = 5
    all_to_one = [0] * CHARTS
    all_to_one[0] = CHARTS
    over_capacity = [5] * CHARTS
    return {
        "balanced_atlas": balanced,
        "q_per_chart": q_per_chart,
        "saturated_q_plus_1": saturated,
        "single_hot_chart_boundary": single_hot,
        "all_to_one_collapse": all_to_one,
        "over_capacity_five_per_chart": over_capacity,
    }


def build_payload() -> dict[str, Any]:
    bt1308 = load_json("data/bt1308_adversarial_collision_stress.json")

    routed_cases = {}
    for name, counts in stress_counts().items():
        routed_cases[name] = spread_route(requests_from_counts(counts))

    checks = {
        "bt1308_verified": bt1308["verified"] is True,
        "balanced_traffic_unchanged": routed_cases["balanced_atlas"][
            "zero_displacement_packets"
        ]
        == CHARTS
        and routed_cases["balanced_atlas"]["max_chart_load"] == 1,
        "q_per_chart_traffic_unchanged": routed_cases["q_per_chart"][
            "zero_displacement_packets"
        ]
        == 3 * CHARTS
        and routed_cases["q_per_chart"]["max_chart_load"] == 3,
        "saturated_traffic_unchanged": routed_cases["saturated_q_plus_1"][
            "zero_displacement_packets"
        ]
        == CAPACITY
        and routed_cases["saturated_q_plus_1"]["max_chart_load"] == SERVICE,
        "single_hot_boundary_admitted_in_one_epoch": routed_cases[
            "single_hot_chart_boundary"
        ]["epochs_needed"]
        == 1
        and routed_cases["single_hot_chart_boundary"]["rejected"] == 0,
        "all_to_one_540_packets_repaired_to_one_epoch": routed_cases[
            "all_to_one_collapse"
        ]["epochs_needed"]
        == 1
        and routed_cases["all_to_one_collapse"]["nonempty_charts"] == 135,
        "admitted_cases_never_exceed_service": all(
            routed_cases[name]["max_chart_load"] <= SERVICE
            for name in [
                "balanced_atlas",
                "q_per_chart",
                "saturated_q_plus_1",
                "single_hot_chart_boundary",
                "all_to_one_collapse",
            ]
        ),
        "over_capacity_rejects_exactly_one_per_chart": routed_cases[
            "over_capacity_five_per_chart"
        ]["accepted"]
        == CAPACITY
        and routed_cases["over_capacity_five_per_chart"]["rejected"] == CHARTS,
        "router_capacity_is_2160": CAPACITY == 2160,
    }

    payload = {
        "theorem": "BT1310 entropy-preserving mirror router",
        "verified": all(checks.values()),
        "checks": checks,
        "router": {
            "charts": CHARTS,
            "service_slots_per_chart": SERVICE,
            "capacity": CAPACITY,
            "rule": (
                "For each requested chart c, assign the packet to the first "
                "cyclic chart c+d with load below 4. Reject only when all "
                "2160 local slots are occupied."
            ),
        },
        "routed_cases": routed_cases,
        "architecture_reading": (
            "BT1310 repairs the BT1308 all-to-one failure without disturbing "
            "balanced traffic. The router preserves chart entropy when it is "
            "already present, and injects entropy only when a hot spot would "
            "exceed local four-slot mirror service."
        ),
        "honesty_boundary": (
            "BT1310 is deterministic slot routing. It does not model online "
            "arrival races, analog switching time, packet loss, or adaptive "
            "path choice inside the optical fabric."
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
        raise SystemExit(f"BT1310 failed checks: {failed}")


if __name__ == "__main__":
    main()
