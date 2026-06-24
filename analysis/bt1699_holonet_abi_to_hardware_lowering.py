#!/usr/bin/env python3
"""BT1699 - lower the typed Holonet ABI onto physical hardware rows.

BT1698 proves the local packet is a deterministic 72-tick state machine.
BT1699 lowers those ticks onto the existing single-photon hardware envelope:
source switch, delay/program, analyzer/OAM body, detector/Hesse handoff, and
dark-reference closeout.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from bt1698_holonet_packet_state_machine import build_certificate as build_state_machine

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1699_holonet_abi_to_hardware_lowering.json"

FRAME_WINDOWS = {
    "source_switch": (0, 7),
    "program_delay": (8, 31),
    "analyzer_or_fuel_body": (32, 47),
    "detector_or_hesse_handoff": (48, 63),
    "dark_reference": (64, 71),
}

STAGE_PRIMITIVES = {
    "source_switch": "single-photon source/select switch",
    "program_delay": "11-bit time-bin program and delay line",
    "analyzer_or_fuel_body": "Q6/tomotope analyzer or OAM fuel body",
    "detector_or_hesse_handoff": "detector, mirror, and Hesse handoff",
    "dark_reference": "dark-reference closeout placeholder",
}


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def hardware_stage(tick: int) -> str:
    for stage, (start, end) in FRAME_WINDOWS.items():
        if start <= tick <= end:
            return stage
    raise ValueError(f"tick outside hardware frame: {tick}")


def slot_class(tomotope_flag: int | None) -> str | None:
    if tomotope_flag is None:
        return None
    if 0 <= tomotope_flag < 168:
        return "ACTIVE_DUAL_TOROIDAL_PORT"
    if 168 <= tomotope_flag < 192:
        return "Q4_CSS_D4_GUARD_BAND"
    return "OUT_OF_RANGE"


def build_lowering_rows(trace: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in trace:
        tick = int(row["tick"])
        stage = hardware_stage(tick)
        flag = row.get("tomotope_flag")
        rows.append(
            {
                "tick": tick,
                "logical_region": row["region"],
                "logical_op": row["op"],
                "hardware_stage": stage,
                "primitive": STAGE_PRIMITIVES[stage],
                "tomotope_flag": flag,
                "slot_class": slot_class(flag),
                "loss_placeholder": f"L_FRAME_TICK_{tick:02d}",
                "dark_reference_placeholder": (
                    f"DARK_TICK_{tick:02d}" if stage == "dark_reference" else None
                ),
                "detector_window": stage
                in {"detector_or_hesse_handoff", "dark_reference"},
            }
        )
    return rows


def build_guard_weld(
    port: dict[str, Any], syndrome: dict[str, Any], magic: dict[str, Any]
) -> list[dict[str, Any]]:
    rows = []
    for port_row, css_row, magic_row in zip(
        port["guard_band_rows"], syndrome["guard_rows"], magic["resource_apertures"]
    ):
        rows.append(
            {
                "guard_slot": port_row["guard_slot"],
                "tomotope_flag": port_row["tomotope_flag"],
                "q4_plaquette": port_row["q4_plaquette"],
                "css_edge_index": css_row["css_edge_index"],
                "magic_resource_aperture": magic_row["resource_aperture"],
                "quartic_atom": magic_row["atom"],
                "quartic_branch": magic_row["quartic_branch"],
                "qutrit_phase": magic_row["qutrit_phase"],
            }
        )
    return rows


def build_certificate() -> dict[str, Any]:
    state = build_state_machine()
    bt1697 = load_json("data/bt1697_holonet_typed_packet_abi.json")
    automaton = load_json("data/bt1601_single_photon_transaction_automaton.json")
    envelope = load_json("data/bt1649_time_bin_qudit_envelope.json")
    guard_shell = load_json("data/bt1650_guard_page_calibration_closure.json")
    compiler = load_json("data/bt1653_time_bin_hardware_compiler.json")
    port = load_json("data/bt1414_csaszar_szilassi_dual_physical_port.json")
    syndrome = load_json("data/bt1415_even_projection_steinberg_syndrome_layer.json")
    magic = load_json("data/bt1418_d4_quartic_magic_injection_frontier.json")

    lowering_rows = build_lowering_rows(state["trace"])
    stage_histogram = Counter(row["hardware_stage"] for row in lowering_rows)
    guard_weld = build_guard_weld(port, syndrome, magic)
    body_flags = [
        row["tomotope_flag"]
        for row in lowering_rows
        if row["logical_region"] == "tomotope_body"
    ]
    guard_flags = [row["tomotope_flag"] for row in guard_weld]

    frame_windows_cover = []
    for stage, (start, end) in FRAME_WINDOWS.items():
        frame_windows_cover.extend(range(start, end + 1))

    checks = {
        "bt1697_verified": bt1697["verified"] is True,
        "bt1698_verified": state["verified"] is True,
        "physical_sources_verified": all(
            item["verified"]
            for item in (
                automaton,
                envelope,
                guard_shell,
                compiler,
                port,
                syndrome,
                magic,
            )
        ),
        "frame_windows_partition_72_ticks": sorted(frame_windows_cover)
        == list(range(72)),
        "lowering_has_one_row_per_tick": len(lowering_rows) == 72
        and [row["tick"] for row in lowering_rows] == list(range(72)),
        "stage_histogram_matches_physical_template": dict(stage_histogram)
        == {
            "source_switch": 8,
            "program_delay": 24,
            "analyzer_or_fuel_body": 16,
            "detector_or_hesse_handoff": 16,
            "dark_reference": 8,
        },
        "all_ticks_have_loss_placeholders": all(
            row["loss_placeholder"] for row in lowering_rows
        ),
        "dark_reference_is_last_eight_ticks": [
            row["tick"] for row in lowering_rows if row["dark_reference_placeholder"]
        ]
        == list(range(64, 72)),
        "body_flags_lower_to_port_or_guard": all(
            slot_class(flag) in {"ACTIVE_DUAL_TOROIDAL_PORT", "Q4_CSS_D4_GUARD_BAND"}
            for flag in body_flags
        ),
        "guard_weld_has_24_rows": len(guard_weld) == 24,
        "guard_weld_aligns_port_css_magic_flags": all(
            row["tomotope_flag"] == 168 + index
            and row["css_edge_index"] == 216 + index
            and row["magic_resource_aperture"] == index
            and row["q4_plaquette"] == index
            for index, row in enumerate(guard_weld)
        ),
        "single_photon_cycle_is_1600_frames_115200_ticks": automaton["counts"]["frames"]
        == 1600
        and automaton["counts"]["ticks"] == 1600 * 72 == 115200,
        "time_bin_envelope_is_1600_plus_448": envelope["counts"]["envelope_bins"]
        == 2048
        and envelope["counts"]["active_frames"] == 1600
        and envelope["counts"]["guard_bins"] == 448,
        "guard_shell_spends_448_as_168_168_112": guard_shell["counts"][
            "dark_reference_guards"
        ]
        == 168
        and guard_shell["counts"]["loss_probe_guards"] == 168
        and guard_shell["counts"]["parity_overflow_guards"] == 112,
        "hardware_compiler_keeps_10_components_and_11_delay_stages": compiler[
            "component_count"
        ]
        == 10
        and len(compiler["delay_stages_tau"]) == 11,
    }

    return {
        "theorem": "BT1699 Holonet ABI-to-Hardware Lowering",
        "verified": all(checks.values()),
        "breakthrough": (
            "The typed packet ABI lowers onto the existing single-photon hardware "
            "envelope without changing tick order: each of the 72 logical ticks "
            "has one physical stage, one symbolic loss hook, and the last eight "
            "ticks are the dark-reference closeout."
        ),
        "frame_windows": FRAME_WINDOWS,
        "stage_primitives": STAGE_PRIMITIVES,
        "stage_histogram": dict(sorted(stage_histogram.items())),
        "lowering_rows": lowering_rows,
        "guard_weld": guard_weld,
        "cycle_totals": {
            "frames": 1600,
            "ticks": 115200,
            "dark_reference_guards": 168,
            "loss_probe_guards": 168,
            "parity_overflow_guards": 112,
            "time_bin_envelope": 2048,
        },
        "source_certificates": [
            "data/bt1697_holonet_typed_packet_abi.json",
            "data/bt1698_holonet_packet_state_machine.json",
            "data/bt1601_single_photon_transaction_automaton.json",
            "data/bt1649_time_bin_qudit_envelope.json",
            "data/bt1650_guard_page_calibration_closure.json",
            "data/bt1653_time_bin_hardware_compiler.json",
            "data/bt1414_csaszar_szilassi_dual_physical_port.json",
            "data/bt1415_even_projection_steinberg_syndrome_layer.json",
            "data/bt1418_d4_quartic_magic_injection_frontier.json",
        ],
        "claim_boundary": [
            "This is a typed lowering certificate, not a calibrated optical chip.",
            "Loss, dark counts, delay, jitter, and detector efficiency remain symbolic placeholders.",
            "The guard weld proves interface equality of 24 rows; it does not claim the four 24-count layers are physically identical.",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(f"  stage histogram: {cert['stage_histogram']}")
    print(
        "  cycle: "
        f"{cert['cycle_totals']['frames']} frames, {cert['cycle_totals']['ticks']} ticks"
    )
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
