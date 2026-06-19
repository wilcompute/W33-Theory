#!/usr/bin/env python3
"""BT1309 - Photonic pulse budget for the holonet ISA.

BT1306 mapped the 8-tick word to symbolic hardware.  BT1309 counts the control
windows and active pulses implied by the verified full-atlas schedule.

There are two complementary ratios:

    scheduled windows per word: 3 qutrit-axis + 5 delay-hop = 8,
    active full-atlas pulses: 1620 qutrit-axis + 1620 delay-hop.

The schedule reserves a 3:5 hardware word, but the balanced atlas activates the
two physical control families equally.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1309_photonic_pulse_budget.json"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def scheduled_window_counts(words: int) -> dict[str, int]:
    return {
        "words": words,
        "qutrit_axis_windows": 3 * words,
        "delay_hop_windows": 5 * words,
        "total_windows": 8 * words,
    }


def build_payload() -> dict[str, Any]:
    bt1301 = load_json("data/bt1301_full_chart_atlas_isa_compiler.json")
    bt1306 = load_json("data/bt1306_physical_timing_model.json")
    physical_stack = load_json("data/w33_holonet_physical_stack.json")

    routes = bt1301["atlas_routes"]
    active_qutrit_axis = sum(len(route["xor_axes"]) for route in routes)
    active_delay_hops = sum(route["apartment_hops"] for route in routes)
    active_total = active_qutrit_axis + active_delay_hops
    reserved_total = len(routes) * 8
    idle_total = reserved_total - active_total
    hop_hist = Counter(route["apartment_hops"] for route in routes)

    hierarchy = {
        "word": scheduled_window_counts(1),
        "tomotope_body": scheduled_window_counts(6),
        "parity_epilogue": scheduled_window_counts(3),
        "microframe": scheduled_window_counts(9),
        "mirror_epoch": scheduled_window_counts(270),
        "clifford_supercycle": scheduled_window_counts(6480),
    }
    parity_hardware = Counter(
        "qutrit_axis" if window["tick"] < 3 else "delay_hop"
        for window in bt1306["parity_windows"]
    )

    checks = {
        "bt1301_verified": bt1301["verified"] is True,
        "bt1306_verified": bt1306["verified"] is True,
        "physical_stack_has_single_photon_demo": "single self-entangled photon"
        in physical_stack["what_it_is"],
        "scheduled_word_is_three_plus_five": hierarchy["word"]["qutrit_axis_windows"]
        == 3
        and hierarchy["word"]["delay_hop_windows"] == 5,
        "microframe_has_27_plus_45_windows": hierarchy["microframe"][
            "qutrit_axis_windows"
        ]
        == 27
        and hierarchy["microframe"]["delay_hop_windows"] == 45,
        "mirror_epoch_has_2160_windows": hierarchy["mirror_epoch"]["total_windows"]
        == 2160,
        "supercycle_has_51840_windows": hierarchy["clifford_supercycle"][
            "total_windows"
        ]
        == 51840,
        "full_atlas_active_qutrit_axis_is_1620": active_qutrit_axis == 1620,
        "full_atlas_active_delay_hops_is_1620": active_delay_hops == 1620,
        "full_atlas_active_families_balance": active_qutrit_axis == active_delay_hops,
        "full_atlas_active_total_is_3240": active_total == 3240,
        "full_atlas_idle_total_is_1080": idle_total == 1080,
        "apartment_hops_have_mean_q": sum(
            hop * count for hop, count in hop_hist.items()
        )
        // sum(hop_hist.values())
        == 3,
        "parity_lanes_are_one_axis_plus_five_delay": dict(parity_hardware)
        == {"qutrit_axis": 1, "delay_hop": 5},
    }

    payload = {
        "theorem": "BT1309 photonic pulse budget",
        "verified": all(checks.values()),
        "checks": checks,
        "scheduled_window_hierarchy": hierarchy,
        "full_atlas_active_budget": {
            "routes": len(routes),
            "active_qutrit_axis_pulses": active_qutrit_axis,
            "active_delay_hop_pulses": active_delay_hops,
            "active_total_pulses": active_total,
            "reserved_total_windows": reserved_total,
            "idle_windows": idle_total,
            "active_family_ratio": "1620:1620 = 1:1",
            "apartment_hop_histogram": dict(sorted(hop_hist.items())),
        },
        "physical_control_families": {
            "qutrit_axis": "tritter/EOM phase-address pulse on ticks 0..2",
            "delay_hop": "delay-line switch pulse on ticks 3..7",
            "parity_lane_family_count": dict(parity_hardware),
            "hardware_boundary": (
                "Counts are symbolic control windows/pulses. They are not a "
                "clock speed, optical loss budget, or detector timing budget."
            ),
        },
        "architecture_reading": (
            "The holonet reserves a 3:5 word because a route digit has three "
            "ternary qutrit axes and five apartment-hop slots. The full atlas "
            "then activates those physical families in exact balance: 1620 "
            "qutrit-axis pulses and 1620 delay-hop pulses. The mean apartment "
            "hop count is q=3, so the network control load self-balances "
            "against the qutrit-axis load."
        ),
        "honesty_boundary": (
            "BT1309 is a symbolic pulse-count budget derived from verified "
            "routing data and the existing build sheet. It does not choose "
            "photonic component bandwidths, losses, jitter tolerances, or "
            "GKP thresholds."
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
        raise SystemExit(f"BT1309 failed checks: {failed}")


if __name__ == "__main__":
    main()
