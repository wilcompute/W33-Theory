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


def test_bt1648_fano_charge_conservation_law():
    result = run_tool(
        "bt1648_fano_charge_conservation.py",
        "bt1648_fano_charge_conservation.json",
    )

    assert result["verified"] is True
    assert result["counts"]["active_detector_bins"] == 168
    assert result["histograms"]["class"] == {
        "COMPATIBLE_RESERVE_BIN": 48,
        "SAME_ANCHORED_FUEL_BIN": 40,
        "UNANCHORED_FUEL_BIN": 80,
    }
    assert result["histograms"]["usage"] == {"9": 80, "10": 88}
    assert result["checks"]["five_gate_lines_have_16_low_8_anchor_bins"] is True
    assert result["checks"]["two_reserve_lines_are_24_compatible_bins_each"] is True


def test_bt1649_time_bin_qudit_envelope():
    run_tool(
        "bt1648_fano_charge_conservation.py",
        "bt1648_fano_charge_conservation.json",
    )
    result = run_tool(
        "bt1649_time_bin_qudit_envelope.py",
        "bt1649_time_bin_qudit_envelope.json",
    )

    assert result["verified"] is True
    assert result["counts"]["time_bin_bits"] == 11
    assert result["counts"]["envelope_bins"] == 2048
    assert result["counts"]["active_frames"] == 1600
    assert result["counts"]["guard_bins"] == 448
    assert result["histograms"]["guard_role"] == {
        "DARK_REFERENCE": 168,
        "LOSS_PROBE": 168,
        "PARITY_OVERFLOW": 112,
    }


def test_bt1650_guard_page_calibration_closure():
    run_tool(
        "bt1649_time_bin_qudit_envelope.py",
        "bt1649_time_bin_qudit_envelope.json",
    )
    result = run_tool(
        "bt1650_guard_page_calibration_closure.py",
        "bt1650_guard_page_calibration_closure.json",
    )

    assert result["verified"] is True
    assert result["counts"]["guard_rows"] == 448
    assert result["counts"]["dark_reference_guards"] == 168
    assert result["counts"]["loss_probe_guards"] == 168
    assert result["counts"]["parity_overflow_guards"] == 112
    assert result["counts"]["detector_bins_covered_by_dark"] == 168
    assert result["counts"]["detector_bins_covered_by_loss"] == 168
    assert result["checks"]["guard_roles_map_to_retry_fault_modes"] is True


def test_bt1648_bt1650_publication_anchors():
    run_tool(
        "bt1586_operator_oam_full_appendix_splicer.py",
        "bt1586_operator_oam_full_appendix_splicer.json",
        "--apply",
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT1648_BT1650_holonet_insert.tex").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )

    assert "BT1648_BT1650_holonet_insert.tex" in paper
    assert "2048-1600=448=7\\cdot64" in insert
    assert "Fano Time-Bin Guard Closure" in docs
    assert "test_bt1648_bt1650_fano_timebin_guard_closure.py" in focused
