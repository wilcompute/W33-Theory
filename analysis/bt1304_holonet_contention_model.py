#!/usr/bin/env python3
"""BT1304 - Holonet contention model.

BT1301 compiles one ingress packet for each of the 540 charts.  BT1304 reads
that atlas burst as a network load model.

The important distinction is:

    shared micro-op ticks are broadcast control load,
    repeated target charts are output-port contention.

In the BT1301 full-atlas burst, every target chart is unique, so output-port
contention is zero.  The mirror bus has four local slots per chart, so one
packet per chart uses exactly one quarter of the 2160-slot bus.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1304_holonet_contention_model.json"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def choose2(n: int) -> int:
    return n * (n - 1) // 2


def build_payload() -> dict[str, Any]:
    bt1301 = load_json("data/bt1301_full_chart_atlas_isa_compiler.json")
    bt1302 = load_json("data/bt1302_parity_epilogue_reroute_protocol.json")
    bt1303 = load_json("data/bt1303_holonet_stack_contract.json")

    routes = bt1301["atlas_routes"]
    target_hist = Counter(route["target_chart"] for route in routes)
    phase_hist = Counter(route["target_chart"] % 4 for route in routes)
    active_tick_hist = Counter(route["active_tick_count"] for route in routes)
    tick_load = Counter()
    for route in routes:
        for tick in route["active_ticks"]:
            tick_load[tick] += 1

    parity_pair_distribution = bt1302["protocol"]["base_pair_distribution"]
    same_parity_pairs = sum(
        choose2(count) for count in parity_pair_distribution.values()
    )
    same_phase_pairs = sum(choose2(count) for count in phase_hist.values())
    same_tick_pairs = {tick: choose2(tick_load[tick]) for tick in range(8)}
    output_port_conflicts = sum(max(0, count - 1) for count in target_hist.values())

    mirror_bus_slots = 2160
    atlas_packets = len(routes)
    checks = {
        "bt1301_verified": bt1301["verified"] is True,
        "bt1302_verified": bt1302["verified"] is True,
        "bt1303_verified": bt1303["verified"] is True,
        "atlas_has_540_packets": atlas_packets == 540,
        "target_charts_are_unique": len(target_hist) == 540
        and max(target_hist.values()) == 1,
        "output_port_contention_is_zero": output_port_conflicts == 0,
        "mirror_phase_hist_is_uniform": dict(sorted(phase_hist.items()))
        == {0: 135, 1: 135, 2: 135, 3: 135},
        "active_tick_hist_is_bt1301_balanced": dict(sorted(active_tick_hist.items()))
        == {4: 108, 5: 108, 6: 108, 7: 108, 8: 108},
        "tick_load_is_prefix_staircase": dict(sorted(tick_load.items()))
        == {0: 540, 1: 540, 2: 540, 3: 540, 4: 432, 5: 324, 6: 216, 7: 108},
        "full_atlas_uses_one_quarter_mirror_bus": atlas_packets * 4 == mirror_bus_slots,
        "one_packet_per_chart_fits_four_slot_local_bus": max(target_hist.values()) <= 4,
        "six_parity_lanes_all_loaded": len(parity_pair_distribution) == 6
        and sum(parity_pair_distribution.values()) == 540,
    }

    payload = {
        "theorem": "BT1304 holonet contention model",
        "verified": all(checks.values()),
        "checks": checks,
        "contention_summary": {
            "atlas_packets": atlas_packets,
            "target_chart_count": len(target_hist),
            "output_port_conflicts": output_port_conflicts,
            "mirror_bus_slots": mirror_bus_slots,
            "mirror_bus_utilization": "540/2160 = 1/4",
            "mirror_phase_histogram": dict(sorted(phase_hist.items())),
            "active_tick_histogram": dict(sorted(active_tick_hist.items())),
            "tick_load": dict(sorted(tick_load.items())),
            "same_phase_pair_count": same_phase_pairs,
            "same_parity_pair_count": same_parity_pairs,
            "same_tick_pair_counts": same_tick_pairs,
            "parity_pair_distribution": parity_pair_distribution,
        },
        "architecture_reading": (
            "A full one-packet-per-chart atlas burst is output-conflict-free: "
            "all 540 target charts are distinct. Shared ticks are broadcast "
            "control load, not port contention. The burst occupies one of four "
            "local mirror-bus slots per chart, so the 2160-slot bus is at 1/4 "
            "utilization with 3/4 headroom."
        ),
        "honesty_boundary": (
            "BT1304 is a deterministic load/contention accounting model. It "
            "does not yet simulate analog pulse crosstalk, queueing over time, "
            "or simultaneous packets targeting the same chart beyond the "
            "four-slot service capacity."
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
        raise SystemExit(f"BT1304 failed checks: {failed}")


if __name__ == "__main__":
    main()
