import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str, *args: str) -> dict:
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / script), *args], check=True, cwd=ROOT
    )
    return json.loads((ROOT / "data" / data).read_text(encoding="utf-8"))


def test_bt1589_lg_radial_covariance_survives_recenter_tax():
    result = run_tool(
        "bt1589_lg_oam_radial_covariance_simulator.py",
        "bt1589_lg_oam_radial_covariance_simulator.json",
    )
    assert result["verified"] is True
    assert result["counts"]["radial_type_rows"] == 45
    assert result["counts"]["expanded_word_cases"] == 1080
    assert result["counts"]["expanded_ticks"] == 77760
    assert result["class_eta_max"] == {
        "centered_frame": 0.1,
        "mixed_shift_phase": 0.18296,
        "oam_shift_only": 0.168,
        "phase_shift_only": 0.117,
    }
    assert result["worst_case"]["recenter_class"] == "mixed_shift_phase"
    assert result["worst_case"]["witness_gate"] == "F3"
    assert result["checks"]["all_commutators_zero"] is True


def test_bt1590_full_witness_lane_sheet_balances_physical_lanes():
    run_tool(
        "bt1589_lg_oam_radial_covariance_simulator.py",
        "bt1589_lg_oam_radial_covariance_simulator.json",
    )
    result = run_tool(
        "bt1590_full_witness_lane_sheet_compiler.py",
        "bt1590_full_witness_lane_sheet_compiler.json",
    )
    assert result["verified"] is True
    assert result["counts"]["segments"] == 1080
    assert result["counts"]["total_ticks"] == 77760
    assert set(result["lane_counts"].values()) == {12960}
    assert result["detector_slot_counts"] == {
        "0": 19440,
        "1": 19440,
        "2": 19440,
        "3": 19440,
    }
    assert result["action_level_tick_counts"] == {
        "native_d4_square_pulse": 25920,
        "s4_analyzer_relabel": 51840,
    }
    assert "segments" not in result
    assert len(result["segment_samples"]) == 30


def test_bt1591_oam_mdnn_frontend_keeps_claim_firewall():
    run_tool(
        "bt1589_lg_oam_radial_covariance_simulator.py",
        "bt1589_lg_oam_radial_covariance_simulator.json",
    )
    run_tool(
        "bt1590_full_witness_lane_sheet_compiler.py",
        "bt1590_full_witness_lane_sheet_compiler.json",
    )
    result = run_tool(
        "bt1591_oam_mdnn_frontend_firewall.py",
        "bt1591_oam_mdnn_frontend_firewall.json",
    )
    assert result["verified"] is True
    assert result["exact_numbers"]["finite_action_addresses"] == 216
    assert result["exact_numbers"]["witness_ticks"] == 77760
    assert result["external_source_used"] == "oam_multiplexing_natphot_2026"
    assert len(result["frontend_layers"]) == 6
    assert sum(not row["allowed"] for row in result["claim_firewall"]) == 3


def test_bt1589_bt1591_publication_anchors():
    run_tool(
        "bt1586_operator_oam_full_appendix_splicer.py",
        "bt1586_operator_oam_full_appendix_splicer.json",
        "--apply",
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT1589_BT1591_holonet_insert.tex").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )

    assert "BT1589_BT1591_holonet_insert.tex" in paper
    assert "0.18296 < 0.20" in insert
    assert "OAM Radial Lane Front-End" in docs
    assert "test_bt1589_bt1591_oam_radial_lane_frontend.py" in focused
