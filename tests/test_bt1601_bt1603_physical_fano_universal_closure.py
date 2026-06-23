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


def test_bt1601_compiles_single_photon_transaction_automaton():
    run_tool(
        "bt1600_full_witting_transaction_cycle.py",
        "bt1600_full_witting_transaction_cycle.json",
    )
    result = run_tool(
        "bt1601_single_photon_transaction_automaton.py",
        "bt1601_single_photon_transaction_automaton.json",
    )

    assert result["verified"] is True
    assert result["counts"]["frames"] == 1600
    assert result["counts"]["ticks"] == 115200
    assert result["histograms"]["rail"] == {
        "ACCEPTED_CONTROL": 520,
        "CONTEXTUAL_FUEL": 1080,
    }
    assert result["histograms"]["detector_slot"] == {
        "0": 400,
        "1": 400,
        "2": 400,
        "3": 400,
    }
    assert result["counts"]["loss_placeholders"] == 1600
    assert result["counts"]["dark_reference_placeholders"] == 1600


def test_bt1602_welds_fano_168_bins_to_witting_body():
    run_tool(
        "bt1601_single_photon_transaction_automaton.py",
        "bt1601_single_photon_transaction_automaton.json",
    )
    result = run_tool(
        "bt1602_fano_witting_detector_bin_synthesis.py",
        "bt1602_fano_witting_detector_bin_synthesis.json",
    )

    assert result["verified"] is True
    assert result["counts"]["active_detector_bins"] == 168
    assert result["counts"]["fuel_bins"] == 120
    assert result["counts"]["compatible_control_bins"] == 48
    assert result["counts"]["same_ray_anchor_bins"] == 40
    assert result["histograms"]["total_bin_usage_profile"] == {"9": 80, "10": 88}
    assert result["checks"]["source_shell_profile_is_27_12_1"] is True


def test_bt1603_closes_universal_computation_abi_theorem():
    run_tool(
        "bt1602_fano_witting_detector_bin_synthesis.py",
        "bt1602_fano_witting_detector_bin_synthesis.json",
    )
    result = run_tool(
        "bt1603_universal_computation_proof_closure.py",
        "bt1603_universal_computation_proof_closure.json",
    )

    assert result["verified"] is True
    assert result["closure_summary"]["frames"] == 1600
    assert result["closure_summary"]["ticks"] == 115200
    assert result["closure_summary"]["active_detector_bins"] == 168
    assert result["closure_summary"]["css_rows"] == 72
    assert result["closure_summary"]["css_logical_dimension"] == 81
    assert [step["step"] for step in result["proof_steps"]] == [
        "finite_program_carrier",
        "clifford_transport",
        "contextual_fuel",
        "non_clifford_injection",
        "detector_bus",
        "qec_syndrome_handoff",
    ]


def test_bt1601_bt1603_publication_anchors():
    run_tool(
        "bt1586_operator_oam_full_appendix_splicer.py",
        "bt1586_operator_oam_full_appendix_splicer.json",
        "--apply",
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT1601_BT1603_holonet_insert.tex").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )

    assert "BT1601_BT1603_holonet_insert.tex" in paper
    assert "168=7\\cdot24" in insert
    assert "Physical Fano Universal Closure" in docs
    assert "test_bt1601_bt1603_physical_fano_universal_closure.py" in focused
