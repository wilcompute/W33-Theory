#!/usr/bin/env python3
"""BT1314 - Deterministic traffic stability stress test.

BT1308 showed an adversarial hot spot can defeat global utilization averages.
BT1314 asks the stochastic-looking question deterministically: under a fixed
LCG traffic source, how often does raw per-chart service create local backlog,
and does the BT1310 entropy router remove it for admitted bursts?
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1314_deterministic_traffic_stability.json"
CHARTS = 540
SERVICE = 4
CAPACITY = CHARTS * SERVICE
TRIALS = 60
SEED = 1314


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def lcg_stream(seed: int):
    state = seed
    while True:
        state = (1103515245 * state + 12345) % (2**31)
        yield state


def generate_requests(packets: int, seed: int) -> list[int]:
    stream = lcg_stream(seed)
    return [next(stream) % CHARTS for _ in range(packets)]


def raw_service(requests: list[int]) -> dict[str, Any]:
    loads = Counter(requests)
    max_load = max(loads.values()) if loads else 0
    backlog = sum(max(0, load - SERVICE) for load in loads.values())
    hot_charts = sum(1 for load in loads.values() if load > SERVICE)
    return {
        "max_chart_load": max_load,
        "hot_charts": hot_charts,
        "backlog_after_one_epoch": backlog,
        "epochs_needed": math.ceil(max_load / SERVICE) if max_load else 0,
    }


def routed_service(requests: list[int]) -> dict[str, Any]:
    loads = [0] * CHARTS
    rejected = 0
    for requested in requests:
        placed = None
        for offset in range(CHARTS):
            chart = (requested + offset) % CHARTS
            if loads[chart] < SERVICE:
                placed = chart
                break
        if placed is None:
            rejected += 1
            continue
        loads[placed] += 1
    max_load = max(loads) if loads else 0
    return {
        "accepted": len(requests) - rejected,
        "rejected": rejected,
        "max_chart_load": max_load,
        "backlog_after_one_epoch": sum(max(0, load - SERVICE) for load in loads),
        "epochs_needed": math.ceil(max_load / SERVICE) if max_load else 0,
        "nonempty_charts": sum(1 for load in loads if load),
    }


def aggregate(rows: list[dict[str, Any]], keys: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {"trials": len(rows)}
    for key in keys:
        values = [row[key] for row in rows]
        out[f"{key}_min"] = min(values)
        out[f"{key}_max"] = max(values)
        out[f"{key}_mean"] = mean(values)
    return out


def build_case(name: str, packets: int, base_seed: int) -> dict[str, Any]:
    raw_rows = []
    routed_rows = []
    for trial in range(TRIALS):
        requests = generate_requests(packets, base_seed + 7919 * trial)
        raw_rows.append(raw_service(requests))
        routed_rows.append(routed_service(requests))
    return {
        "case": name,
        "packets_per_epoch": packets,
        "global_utilization": f"{min(packets, CAPACITY)}/{CAPACITY}",
        "raw": aggregate(
            raw_rows, ["max_chart_load", "hot_charts", "backlog_after_one_epoch"]
        ),
        "routed": aggregate(
            routed_rows,
            ["accepted", "rejected", "max_chart_load", "backlog_after_one_epoch"],
        ),
        "sample_raw": raw_rows[:5],
        "sample_routed": routed_rows[:5],
    }


def build_payload() -> dict[str, Any]:
    bt1310 = load_json("data/bt1310_entropy_preserving_router.json")
    cases = {
        "one_packet_per_chart_randomized": 540,
        "q_packets_per_chart_randomized": 1620,
        "saturated_randomized": 2160,
        "overflow_randomized": 2700,
    }
    rows = {
        name: build_case(name, packets, SEED + idx * 104729)
        for idx, (name, packets) in enumerate(cases.items())
    }

    checks = {
        "bt1310_verified": bt1310["verified"] is True,
        "raw_540_random_traffic_has_backlog": rows["one_packet_per_chart_randomized"][
            "raw"
        ]["backlog_after_one_epoch_mean"]
        > 0,
        "raw_1620_random_traffic_has_backlog": rows["q_packets_per_chart_randomized"][
            "raw"
        ]["backlog_after_one_epoch_mean"]
        > 0,
        "raw_2160_random_traffic_has_backlog": rows["saturated_randomized"]["raw"][
            "backlog_after_one_epoch_mean"
        ]
        > 0,
        "routed_admitted_cases_have_no_backlog": all(
            rows[name]["routed"]["backlog_after_one_epoch_max"] == 0
            and rows[name]["routed"]["rejected_max"] == 0
            for name in [
                "one_packet_per_chart_randomized",
                "q_packets_per_chart_randomized",
                "saturated_randomized",
            ]
        ),
        "routed_admitted_cases_need_one_epoch": all(
            rows[name]["routed"]["max_chart_load_max"] <= SERVICE
            for name in [
                "one_packet_per_chart_randomized",
                "q_packets_per_chart_randomized",
                "saturated_randomized",
            ]
        ),
        "overflow_rejects_exact_capacity_excess": rows["overflow_randomized"]["routed"][
            "accepted_min"
        ]
        == CAPACITY
        and rows["overflow_randomized"]["routed"]["accepted_max"] == CAPACITY
        and rows["overflow_randomized"]["routed"]["rejected_min"] == 540
        and rows["overflow_randomized"]["routed"]["rejected_max"] == 540,
        "trial_count_is_substrate_multiple": TRIALS == CHARTS // 9,
    }

    payload = {
        "theorem": "BT1314 deterministic traffic stability",
        "verified": all(checks.values()),
        "checks": checks,
        "traffic_source": {
            "kind": "LCG modulo 540",
            "seed": SEED,
            "trials": TRIALS,
            "note": (
                "The source is deterministic, offline, and reproducible. It is "
                "used as a pseudo-random stress distribution, not as a model of "
                "real optical traffic statistics."
            ),
        },
        "cases": rows,
        "architecture_reading": (
            "BT1314 shows why the entropy router is an architectural layer, "
            "not cosmetic symmetry. Raw randomized arrivals produce local hot "
            "charts and backlog even when global utilization is only one "
            "quarter. The BT1310 router removes all backlog for every admitted "
            "burst up to 2160 packets and turns overflow into exact admission "
            "control."
        ),
        "honesty_boundary": (
            "This is a deterministic stress harness. It does not estimate a "
            "real deployment distribution, optical jitter, packet loss, or QoS "
            "fairness policy."
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
        raise SystemExit(f"BT1314 failed checks: {failed}")


if __name__ == "__main__":
    main()
