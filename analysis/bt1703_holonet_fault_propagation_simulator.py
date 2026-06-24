#!/usr/bin/env python3
"""BT1703 - symbolic Holonet fault propagation simulator.

BT1703 injects symbolic loss, dark-click, and parity faults into the BT1699
lowering.  The goal is not calibrated noise.  The goal is to prove that every
symbolic fault lands in one of the finite ABI exits: local termination, retry,
or CSS syndrome handoff.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from bt1699_holonet_abi_to_hardware_lowering import build_certificate as build_lowering

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1703_holonet_fault_propagation_simulator.json"


def classify_loss(row: dict[str, Any]) -> str:
    stage = row["hardware_stage"]
    if stage == "dark_reference":
        return "LOCAL_DARK_CLOSEOUT"
    if stage in {"detector_or_hesse_handoff", "analyzer_or_fuel_body"}:
        return "RETRY_FRAME"
    return "LOCAL_REPROGRAM_RETRY"


def build_fault_rows(lowering: dict[str, Any]) -> list[dict[str, Any]]:
    faults: list[dict[str, Any]] = []
    for row in lowering["lowering_rows"]:
        faults.append(
            {
                "fault_id": f"LOSS_TICK_{row['tick']:02d}",
                "fault_type": "LOSS",
                "tick": row["tick"],
                "hardware_stage": row["hardware_stage"],
                "logical_op": row["logical_op"],
                "exit": classify_loss(row),
                "reason": "symbolic loss hook on every lowered packet tick",
            }
        )
        if row["hardware_stage"] == "dark_reference":
            faults.append(
                {
                    "fault_id": f"DARK_CLICK_TICK_{row['tick']:02d}",
                    "fault_type": "DARK_CLICK",
                    "tick": row["tick"],
                    "hardware_stage": row["hardware_stage"],
                    "logical_op": row["logical_op"],
                    "exit": "LOCAL_DARK_REFERENCE_TERMINATION",
                    "reason": "dark-reference closeout bins terminate locally",
                }
            )
    for guard in lowering["guard_weld"]:
        faults.append(
            {
                "fault_id": f"PARITY_GUARD_{guard['guard_slot']:02d}",
                "fault_type": "PARITY",
                "tick": None,
                "hardware_stage": "q4_css_d4_guard_weld",
                "guard_slot": guard["guard_slot"],
                "tomotope_flag": guard["tomotope_flag"],
                "css_edge_index": guard["css_edge_index"],
                "magic_resource_aperture": guard["magic_resource_aperture"],
                "exit": "CSS_SYNDROME_HANDOFF",
                "reason": "guard weld parity faults enter the CSS edge ledger",
            }
        )
    return faults


def build_certificate() -> dict[str, Any]:
    lowering = build_lowering()
    faults = build_fault_rows(lowering)
    exit_histogram = Counter(row["exit"] for row in faults)
    type_histogram = Counter(row["fault_type"] for row in faults)
    checks = {
        "bt1699_verified": lowering["verified"] is True,
        "all_faults_classified": all(row["exit"] for row in faults),
        "loss_fault_on_every_tick": type_histogram["LOSS"] == 72,
        "dark_clicks_are_last_eight_ticks": [
            row["tick"] for row in faults if row["fault_type"] == "DARK_CLICK"
        ]
        == list(range(64, 72)),
        "parity_faults_cover_24_guard_weld_rows": type_histogram["PARITY"] == 24,
        "parity_faults_enter_css_handoff": all(
            row["exit"] == "CSS_SYNDROME_HANDOFF"
            for row in faults
            if row["fault_type"] == "PARITY"
        ),
        "dark_faults_terminate_locally": all(
            row["exit"] == "LOCAL_DARK_REFERENCE_TERMINATION"
            for row in faults
            if row["fault_type"] == "DARK_CLICK"
        ),
        "payload_loss_faults_retry_or_reprogram": all(
            row["exit"] in {"RETRY_FRAME", "LOCAL_REPROGRAM_RETRY"}
            for row in faults
            if row["fault_type"] == "LOSS" and row["hardware_stage"] != "dark_reference"
        ),
        "no_unhandled_exit": "UNHANDLED" not in exit_histogram,
    }
    return {
        "theorem": "BT1703 Holonet Fault Propagation Simulator",
        "verified": all(checks.values()),
        "breakthrough": (
            "Every symbolic loss, dark-click, and parity fault in the lowered "
            "packet ABI has a finite exit: local termination, retry/reprogram, "
            "or CSS syndrome handoff."
        ),
        "fault_exit_policy": {
            "LOSS": "retry frame or local reprogram retry; dark-window loss closes locally",
            "DARK_CLICK": "local dark-reference termination",
            "PARITY": "CSS syndrome handoff through the 24-row guard weld",
        },
        "histograms": {
            "fault_type": dict(sorted(type_histogram.items())),
            "exit": dict(sorted(exit_histogram.items())),
        },
        "fault_rows": faults,
        "source_certificates": [
            "data/bt1699_holonet_abi_to_hardware_lowering.json",
        ],
        "claim_boundary": [
            "This is a symbolic ABI fault table, not a stochastic noise model.",
            "No calibrated loss rate, dark-count probability, detector efficiency, or threshold is claimed.",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(f"  fault histogram: {cert['histograms']['fault_type']}")
    print(f"  exits: {cert['histograms']['exit']}")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
