import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_analysis() -> dict:
    subprocess.run(
        [sys.executable, str(ROOT / "analysis" / "bt1697_holonet_typed_packet_abi.py")],
        check=True,
        cwd=ROOT,
    )
    return json.loads(
        (ROOT / "data" / "bt1697_holonet_typed_packet_abi.json").read_text(
            encoding="utf-8"
        )
    )


def test_bt1697_verifies_typed_packet_abi():
    result = run_analysis()

    assert result["verified"] is True
    checks = result["checks"]
    assert checks["frame_is_48_body_plus_24_epilogue"] is True
    assert checks["body_is_16_q6_edges_times_3_pulses"] is True
    assert checks["epilogue_is_3_hesse_words_times_8_ticks"] is True
    assert checks["full_hesse_grid_is_3_by_3"] is True
    assert checks["selected_hesse_branch_is_one_route_branch"] is True


def test_bt1697_unifies_admission_port_ledger_and_magic_boundaries():
    result = run_analysis()
    checks = result["checks"]

    assert checks["witting_logical_rom_splits_40_squared"] is True
    assert checks["accepted_witting_rate_is_13_over_40"] is True
    assert checks["physical_witting_rom_is_40_tetrads_times_4_by_4"] is True
    assert checks["dual_port_is_168_active_plus_24_guard"] is True
    assert checks["css_ledger_is_216_plus_24"] is True
    assert checks["magic_guard_is_two_D4_quartics"] is True
    assert checks["magic_orients_to_full_tomotope_bus"] is True


def test_bt1697_promotes_global_runtime_packet_schema():
    result = run_analysis()

    fields = {row["field"]: row["size"] for row in result["field_schema"]}
    assert fields["pauli_frame"] == 9
    assert fields["chart_word"] == 8
    assert fields["q6_body_edge"] == 16
    assert fields["tomotope_flag"] == 192
    assert fields["steinberg_syndrome_row"] == 216
    assert fields["css_edge_row"] == 240
    assert fields["mirror_slot"] == 2160
    assert fields["clifford_supercycle"] == 51840
    assert result["checks"]["global_mirror_bus_is_45_times_48"] is True
    assert result["checks"]["runtime_supercycle_is_24_times_2160"] is True


def test_bt1697_publication_anchors():
    run_analysis()
    note = (ROOT / "analysis" / "BT1697_holonet_typed_packet_abi.md").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")

    assert "BT1697" in note
    assert "Holonet Typed Packet ABI" in docs
    assert "test_bt1697_holonet_typed_packet_abi.py" in focused
    assert "BT1697 typed packet ABI" in paper
