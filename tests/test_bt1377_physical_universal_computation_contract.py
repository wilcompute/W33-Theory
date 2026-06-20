#!/usr/bin/env python3
"""Regression tests for BT1377."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1377_physical_universal_computation_contract() -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "analysis/bt1377_physical_universal_computation_contract.py"),
        ],
        cwd=ROOT,
        check=True,
    )
    data = json.loads(
        (ROOT / "data/bt1377_physical_universal_computation_contract.json").read_text(
            encoding="utf-8"
        )
    )

    assert data["verified"] is True
    assert data["deterministic_kernel"]["runtime_order"] == 51840
    assert data["deterministic_kernel"]["runtime_frames"] == 720
    assert data["deterministic_kernel"]["universal_without_port"] is False
    assert data["universal_port"]["required"] is True
    assert "Hesse-SIC/T" in data["universal_port"]["port_options"][0]
    assert "Fibonacci" in data["universal_port"]["port_options"][1]

    assert data["checks"]["eight_tick_word_has_three_axis_and_five_switch_ops"] is True
    assert data["checks"]["packet_rows_are_single_bit_q6_edges"] is True
    assert data["checks"]["central_c3_scheduler_is_concrete"] is True
    assert data["checks"]["phase_correction_frontier_is_radius3_strict"] is True
    assert data["checks"]["deterministic_kernel_declines_universal_overclaim"] is True

    layers = [row["layer"] for row in data["physical_pipeline"]]
    assert layers == [
        "encode_route_digit",
        "emit_optical_word",
        "address_packet",
        "synchronize_phase",
        "schedule_generation",
        "run_clifford_supercycle",
        "non_clifford_port",
    ]


def test_bt1377_docs_index_card_present() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())
    assert "BT1377: physical universal-computation contract" in text
    assert "BT1377_physical_universal_computation_contract.md" in text
    assert "physical Clifford machine + explicit non-Clifford port" in normalized_text
    assert "51840" in text


if __name__ == "__main__":
    test_bt1377_physical_universal_computation_contract()
    test_bt1377_docs_index_card_present()
    print("BT1377 focused tests passed")
