import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / "tools" / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / "data" / data).read_text(encoding="utf-8"))


def test_bt1492_canonical_fano_s4_d4_fiber():
    result = run_tool(
        "bt1492_canonical_fano_s4_d4_fiber.py",
        "bt1492_canonical_fano_s4_d4_fiber.json",
    )
    assert result["verified"] is True
    assert result["groups"]["point_stabilizer_s4"]["order"] == 24
    assert result["groups"]["flag_stabilizer_d4"]["order"] == 8
    assert result["checks"]["point_stabilizer_splits_as_three_flag_cosets"] is True
    assert result["checks"]["point_stabilizer_acts_as_full_s4_on_branch_lines"] is True
    assert result["checks"]["flag_stabilizer_acts_as_d4_on_branch_lines"] is True
    assert result["checks"]["bt1490_shared_fiber_is_canonical_coset_count"] is True


def test_bt1493_row_action_physical_pulse_compiler():
    run_tool(
        "bt1492_canonical_fano_s4_d4_fiber.py",
        "bt1492_canonical_fano_s4_d4_fiber.json",
    )
    result = run_tool(
        "bt1493_row_action_physical_pulse_compiler.py",
        "bt1493_row_action_physical_pulse_compiler.json",
    )
    assert result["verified"] is True
    assert result["counts"]["compiled_actions"] == 24
    assert result["counts"]["compiled_row_pulses"] == 24 * 72
    assert result["counts"]["native_d4_row_pulses"] == 8 * 72
    assert result["counts"]["s4_analyzer_relabel_row_pulses"] == 16 * 72
    assert result["checks"]["row_slots_use_first_six_hesse_lanes"] is True
    assert result["checks"]["mirror_residue_equals_detector_slot"] is True
    assert result["checks"]["target_branch_follows_branch_perm"] is True


def test_bt1494_photonic_qec_release_lock_repair():
    result = run_tool(
        "bt1494_photonic_qec_release_lock_repair.py",
        "bt1494_photonic_qec_release_lock_repair.json",
    )
    assert result["verified"] is True
    assert result["missing_after"] == []
    assert result["checks"]["ccccvi_current"] is True
    assert result["checks"]["ccccxviii_current"] is True
    assert result["checks"]["ccccxxvi_current"] is True
    assert result["checks"]["dcmii_anchors_present"] is True
    for artifact in result["required_artifacts"]:
        assert (ROOT / artifact).exists()


def test_bt1492_bt1494_publication_anchors():
    analysis = (
        ROOT / "analysis" / "BT1492_BT1494_row_pulse_release_lock.md"
    ).read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT1492_BT1494_holonet_insert.tex").read_text(
        encoding="utf-8"
    )
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    main_tex = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")

    assert "point stabilizer of the Fano plane" in analysis
    assert "BT1493 compiles those row symmetries" in insert
    assert "test_bt1492_bt1494_canonical_pulse_release_lock.py" in focused
    assert "Canonical Fano/Pulse Lock" in docs
    assert r"\input{analysis/BT1492_BT1494_holonet_insert}" in main_tex
