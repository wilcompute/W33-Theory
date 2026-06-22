#!/usr/bin/env python3
"""Regression tests for BT1413-BT1415."""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(relpath: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / relpath)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def test_bt1413_q4_plaquette_compiler_runs_true() -> None:
    out = run_tool("tools/bt1413_q4_plaquette_tomotope_face_compiler.py")
    assert out == {
        "bt": 1413,
        "q4_plaquettes": 24,
        "tomotope_flags": 192,
        "verified": True,
    }

    data = load_json("data/bt1413_q4_plaquette_tomotope_face_compiler.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["compiler_summary"] == {
        "antipodal_middle_blocks": 48,
        "formula": "24 plaquettes * 4 edge incidences / 2 antipodal lifts * 4 residues = 192 flags",
        "q4_face_edge_lifts": 96,
        "q4_plaquettes": 24,
        "q6_edges": 192,
        "tomotope_flags": 192,
    }
    assert [row["tomotope_flags"] for row in data["sheet_summaries"]] == [
        64,
        64,
        64,
    ]
    assert all(row["tomotope_face_labels_hit"] == 16 for row in data["sheet_summaries"])
    assert len(data["middle_blocks"]) == 48
    assert len(data["flag_rows"]) == 192
    assert [row["tomotope_flag"] for row in data["flag_rows"]] == list(range(192))
    assert len({row["q6_edge_index"] for row in data["flag_rows"]}) == 192


def test_bt1414_dual_port_active_guard_split() -> None:
    out = run_tool("tools/bt1414_csaszar_szilassi_dual_physical_port.py")
    assert out == {
        "active_slots": 168,
        "bt": 1414,
        "guard_slots": 24,
        "verified": True,
    }

    data = load_json("data/bt1414_csaszar_szilassi_dual_physical_port.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["port_summary"]["identity"] == (
        "21 edges * 2 orientations * 4 residues + 24 guard flags = 192"
    )
    assert len(data["shared_edge_channels"]) == 21
    assert len(data["active_slot_rows"]) == 168
    assert len(data["guard_band_rows"]) == 24
    assert data["axis_summary"] == {
        "crossed_axis_channel": 19,
        "crossed_axis_edge": [4, 6],
        "csaszar_fixed_vertex": 6,
        "szilassi_fixed_face": 4,
    }
    assert Counter(row["edge_channel"] for row in data["active_slot_rows"]) == {
        idx: 8 for idx in range(21)
    }
    assert [row["tomotope_flag"] for row in data["guard_band_rows"]] == list(
        range(168, 192)
    )


def test_bt1415_even_projection_fills_css_ledger() -> None:
    out = run_tool("tools/bt1415_even_projection_steinberg_syndrome_layer.py")
    assert out == {
        "bt": 1415,
        "css_edge_ledger_rows": 240,
        "verified": True,
    }

    data = load_json("data/bt1415_even_projection_steinberg_syndrome_layer.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["syndrome_summary"] == {
        "css_edge_ledger_rows": 240,
        "even_q4_clock_states": 8,
        "field_boundary": "binary Q4 clock syndrome front-end over F2; Steinberg/CSS memory remains over F3",
        "identity": "27 central cycles * 8 even Q4 states + 24 plaquette guards = 240 CSS edge rows",
        "parity_syndrome_rows": 216,
        "q4_plaquette_guard_rows": 24,
        "steinberg_central_cycles": 27,
    }
    assert data["single_bit_error_profile"]["all_single_bit_errors_detected"] is True
    assert data["single_bit_error_profile"]["tested_edges"] == 32
    assert data["single_bit_error_profile"]["unique_odd_error_words"] == 8
    assert [row["css_edge_index"] for row in data["guard_rows"]] == list(
        range(216, 240)
    )
    assert (
        data["external_literature_audit"]["status"]
        == "heuristic_only_not_a_validation_source"
    )
    assert "Moebius-ball" in data["boundary"]


def test_bt1413_bt1415_publication_anchors() -> None:
    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )
    runner = (ROOT / "tools" / "bt1389_run_runtime_frontier_release_lock.sh").read_text(
        encoding="utf-8"
    )
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )

    assert "BT1413&ndash;BT1415: Q4 face compiler, dual port, syndrome ledger" in docs
    assert "BT1413_BT1415_toroidal_q4_dual_port_syndrome.md" in docs
    assert "BT1413 Q4 plaquette-tomotope compiler" in holonet
    assert "BT1414 Csaszar-Szilassi dual port" in holonet
    assert "BT1415 even-projection Steinberg/CSS syndrome ledger" in holonet
    assert "Golden Quartic Polynomial and Moebius-Ball Electron" in holonet
    assert "bt1413_q4_plaquette_tomotope_face_compiler.py" in runner
    assert "test_bt1413_bt1415_toroidal_q4_dual_port_syndrome.py" in runner
    assert "test_bt1413_bt1415_toroidal_q4_dual_port_syndrome.py" in focused


if __name__ == "__main__":
    test_bt1413_q4_plaquette_compiler_runs_true()
    test_bt1414_dual_port_active_guard_split()
    test_bt1415_even_projection_fills_css_ledger()
    test_bt1413_bt1415_publication_anchors()
    print("BT1413-BT1415 focused tests passed")
