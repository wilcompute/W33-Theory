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


def test_bt1592_synthetic_lab_tomography_harness_accepts_fixture_csv():
    run_tool(
        "bt1589_lg_oam_radial_covariance_simulator.py",
        "bt1589_lg_oam_radial_covariance_simulator.json",
    )
    run_tool(
        "bt1590_full_witness_lane_sheet_compiler.py",
        "bt1590_full_witness_lane_sheet_compiler.json",
    )
    run_tool(
        "bt1591_oam_mdnn_frontend_firewall.py",
        "bt1591_oam_mdnn_frontend_firewall.json",
    )
    result = run_tool(
        "bt1592_synthetic_lab_tomography_harness.py",
        "bt1592_synthetic_lab_tomography_harness.json",
    )

    assert result["verified"] is True
    assert len(result["sector_confusion_matrix"]) == 9
    assert result["acceptance_thresholds"]["sector_min_diagonal"] == 0.9
    assert result["acceptance_thresholds"]["sector_max_off_diagonal"] == 0.02
    assert result["csv_ingest"]["rows"] == 91
    assert result["csv_ingest"]["kind_counts"] == {
        "lane_replay": 6,
        "radial_eta": 4,
        "sector_diagonal": 9,
        "sector_off_diagonal": 72,
    }
    assert result["csv_ingest"]["all_rows_pass"] is True


def test_bt1593_lg_mode_alphabet_uses_nine_modes_plus_word_selector():
    run_tool(
        "bt1592_synthetic_lab_tomography_harness.py",
        "bt1592_synthetic_lab_tomography_harness.json",
    )
    result = run_tool(
        "bt1593_lg_mode_alphabet_selector.py",
        "bt1593_lg_mode_alphabet_selector.json",
    )

    assert result["verified"] is True
    assert result["counts"]["lg_modes"] == 9
    assert result["counts"]["word_selectors"] == 24
    assert result["counts"]["finite_addresses"] == 216
    assert [row["lg_oam_charge_ell"] for row in result["lg_mode_alphabet"]] == [
        -4,
        -1,
        2,
        -3,
        -2,
        0,
        1,
        3,
        4,
    ]
    assert sorted(row["address"] for row in result["address_rows"]) == list(range(216))
    assert result["counts"]["native_d4_addresses"] == 72
    assert result["counts"]["s4_relabel_addresses"] == 144


def test_bt1594_hesse_t_port_overlays_without_tick_inflation():
    run_tool(
        "bt1593_lg_mode_alphabet_selector.py",
        "bt1593_lg_mode_alphabet_selector.json",
    )
    result = run_tool(
        "bt1594_hesse_t_universality_witness_loop.py",
        "bt1594_hesse_t_universality_witness_loop.json",
    )

    assert result["verified"] is True
    assert result["overlay_identity"]["witness_segments"] == 1080
    assert result["overlay_identity"]["ticks_per_witness_segment"] == 72
    assert result["overlay_identity"]["hesse_ticks_per_segment"] == 72
    assert result["overlay_identity"]["total_ticks"] == 77760
    assert set(result["hesse_outcome_counts"].values()) == {1080}
    assert result["t_frame_bit_counts"] == {"0": 5400, "1": 4320}
    assert result["checks"]["no_tick_inflation"] is True


def test_bt1592_bt1594_publication_anchors():
    run_tool(
        "bt1586_operator_oam_full_appendix_splicer.py",
        "bt1586_operator_oam_full_appendix_splicer.json",
        "--apply",
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT1592_BT1594_holonet_insert.tex").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )

    assert "BT1592_BT1594_holonet_insert.tex" in paper
    assert "1080\\ {\\rm segments}\\times72\\ {\\rm ticks}" in insert
    assert "Lab/Mode/Hesse Witness Loop" in docs
    assert "test_bt1592_bt1594_lab_mode_hesse_loop.py" in focused
