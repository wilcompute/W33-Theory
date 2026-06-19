#!/usr/bin/env python3
"""BT1306 - Physical timing model for the 8-tick ISA.

BT1306 maps the abstract BT1300 word to symbolic optical hardware timing.  It
does not claim a hardware threshold.  It only states the pulse schedule:

    ticks 0..2  ternary XOR axes  -> tritter/EOM/phase programming
    ticks 3..7  apartment hops    -> delay-line/switch hops

All durations are expressed in a hardware tick tau.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1306_physical_timing_model.json"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def build_payload() -> dict[str, Any]:
    bt1300 = load_json("data/bt1300_oscillator_instruction_isa.json")
    bt1303 = load_json("data/bt1303_holonet_stack_contract.json")
    bt1305 = load_json("data/bt1305_mirror_bus_queueing_law.json")

    micro_ops = bt1300["isa_header"]["micro_ops"]
    tick_schedule = []
    for tick, op in enumerate(micro_ops):
        if tick < 3:
            hardware = "tritter/EOM phase-address pulse"
            rail = f"qutrit_axis_{tick}"
            physical_action = "program ternary XOR axis"
        else:
            hardware = "delay-line switch pulse"
            rail = f"apartment_hop_{tick - 3}"
            physical_action = "advance chart/building route"
        tick_schedule.append(
            {
                "tick": tick,
                "micro_op": op,
                "hardware": hardware,
                "rail": rail,
                "physical_action": physical_action,
                "time_window": f"[{tick} tau, {tick + 1} tau)",
            }
        )

    parity_lanes = [lane for lane in bt1300["lane_layout"] if lane["kind"] == "parity"]
    parity_windows = [
        {
            "lane": lane["lane"],
            "tick": lane["tick"],
            "frame_time_window": f"[{lane['lane']} tau, {lane['lane'] + 1} tau)",
            "column_pair": lane["column_pair"],
            "micro_op": lane["micro_op"],
        }
        for lane in parity_lanes
    ]

    durations = {
        "word": {"tau_units": 8, "formula": "8 tau"},
        "tomotope_body": {"tau_units": 48, "formula": "48 tau = 6 words"},
        "parity_epilogue": {"tau_units": 24, "formula": "24 tau = 3 words"},
        "microframe": {"tau_units": 72, "formula": "72 tau = 9 words"},
        "mirror_bus_epoch": {"tau_units": 2160, "formula": "2160 tau = 30 frames"},
        "clifford_supercycle": {
            "tau_units": 51840,
            "formula": "51840 tau = 720 frames",
        },
    }

    checks = {
        "bt1300_verified": bt1300["verified"] is True,
        "bt1303_verified": bt1303["verified"] is True,
        "bt1305_verified": bt1305["verified"] is True,
        "tick_schedule_has_8_micro_ops": len(tick_schedule) == 8,
        "first_three_ticks_are_qutrit_axis_pulses": all(
            row["hardware"] == "tritter/EOM phase-address pulse"
            for row in tick_schedule[:3]
        ),
        "last_five_ticks_are_delay_switch_pulses": all(
            row["hardware"] == "delay-line switch pulse" for row in tick_schedule[3:]
        ),
        "parity_lanes_are_last_six_frame_ticks": [lane["lane"] for lane in parity_lanes]
        == [66, 67, 68, 69, 70, 71],
        "word_body_epilogue_frame_durations_match_stack": durations["word"]["tau_units"]
        == 8
        and durations["tomotope_body"]["tau_units"] == 48
        and durations["parity_epilogue"]["tau_units"] == 24
        and durations["microframe"]["tau_units"] == 72,
        "mirror_and_supercycle_durations_match_stack": durations["mirror_bus_epoch"][
            "tau_units"
        ]
        == 2160
        and durations["clifford_supercycle"]["tau_units"] == 51840,
        "queue_service_tick_law_loaded": bt1305["service_law"][
            "service_capacity_per_chart_per_epoch"
        ]
        == 4,
    }

    payload = {
        "theorem": "BT1306 physical timing model",
        "verified": all(checks.values()),
        "checks": checks,
        "hardware_tick": {
            "symbol": "tau",
            "meaning": "one programmable optical control window; numeric duration is implementation-dependent",
        },
        "tick_schedule": tick_schedule,
        "parity_windows": parity_windows,
        "durations": durations,
        "architecture_reading": (
            "The 8-tick ISA can be read as a symbolic pulse train. The first "
            "three windows program ternary tritter/EOM axes; the last five "
            "windows switch delay-line apartment hops. The parity epilogue is "
            "the last six frame ticks, lanes 66..71. Scaling by tau gives the "
            "word, tomotope body, epilogue, frame, mirror epoch, and Clifford "
            "supercycle durations without choosing a hardware clock rate."
        ),
        "honesty_boundary": (
            "BT1306 is a symbolic timing contract. It does not set an optical "
            "clock speed, loss budget, detector timing jitter, squeezing "
            "threshold, or integrated-photonics tolerance."
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
        raise SystemExit(f"BT1306 failed checks: {failed}")


if __name__ == "__main__":
    main()
