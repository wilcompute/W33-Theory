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


def test_bt1598_compiles_accepted_witting_pairs_to_control_rail():
    run_tool(
        "bt1597_universal_transaction_object.py",
        "bt1597_universal_transaction_object.json",
    )
    result = run_tool(
        "bt1598_witting_accepted_control_rail.py",
        "bt1598_witting_accepted_control_rail.json",
    )

    assert result["verified"] is True
    assert result["counts"]["control_frames"] == 520
    assert result["counts"]["ticks"] == 37440
    assert result["counts"]["tomotope_blocks_used"] == 40
    assert result["counts"]["tomotope_blocks_slack"] == 8
    assert set(result["histograms"]["basis"].values()) == {13}
    assert result["histograms"]["detector_slot"] == {
        "0": 130,
        "1": 130,
        "2": 130,
        "3": 130,
    }


def test_bt1599_welds_same_ray_surplus_to_phase_sheets():
    run_tool(
        "bt1598_witting_accepted_control_rail.py",
        "bt1598_witting_accepted_control_rail.json",
    )
    result = run_tool(
        "bt1599_same_ray_phase_sheet_weld.py",
        "bt1599_same_ray_phase_sheet_weld.json",
    )

    assert result["verified"] is True
    assert result["counts"]["surplus_contexts"] == 120
    assert result["counts"]["selector_sheets"] == 120
    assert result["histograms"]["phase"] == {"0": 40, "1": 40, "2": 40}
    assert set(result["histograms"]["ray"].values()) == {3}
    assert result["checks"]["matches_bt1365_identity"] is True


def test_bt1600_compiles_complete_1600_frame_witting_cycle():
    run_tool(
        "bt1599_same_ray_phase_sheet_weld.py",
        "bt1599_same_ray_phase_sheet_weld.json",
    )
    result = run_tool(
        "bt1600_full_witting_transaction_cycle.py",
        "bt1600_full_witting_transaction_cycle.json",
    )

    assert result["verified"] is True
    assert result["counts"] == {
        "accepted_control_frames": 520,
        "contextual_fuel_frames": 1080,
        "frames": 1600,
        "same_ray_phase_sidecar_records": 120,
        "ticks": 115200,
    }
    assert result["rail_histogram"] == {
        "ACCEPTED_CONTROL": 520,
        "CONTEXTUAL_FUEL": 1080,
    }
    assert result["checks"]["each_source_has_13_control_27_fuel"] is True


def test_bt1598_bt1600_publication_anchors():
    run_tool(
        "bt1586_operator_oam_full_appendix_splicer.py",
        "bt1586_operator_oam_full_appendix_splicer.json",
        "--apply",
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT1598_BT1600_holonet_insert.tex").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )

    assert "BT1598_BT1600_holonet_insert.tex" in paper
    assert "1600\\cdot72=115200" in insert
    assert "Full Witting Transaction Cycle" in docs
    assert "test_bt1598_bt1600_full_witting_cycle.py" in focused
