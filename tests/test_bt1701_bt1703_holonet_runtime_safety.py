import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(script_name: str, data_name: str) -> dict:
    subprocess.run(
        [sys.executable, str(ROOT / "analysis" / script_name)],
        cwd=ROOT,
        check=True,
    )
    return json.loads((ROOT / "data" / data_name).read_text(encoding="utf-8"))


def test_bt1701_generates_packet_trace_html_svg():
    result = run_script(
        "bt1701_holonet_packet_trace_visualizer.py",
        "bt1701_holonet_packet_trace_visualizer.json",
    )

    html_path = ROOT / result["html_output"]
    html_text = html_path.read_text(encoding="utf-8")
    assert result["verified"] is True
    assert result["checks"]["has_72_tick_cells"] is True
    assert result["checks"]["svg_contains_72_rectangles"] is True
    assert "BT1701 Holonet Packet Trace" in html_text
    assert "<svg" in html_text
    assert len(result["tick_cells"]) == 72


def test_bt1702_scheduler_is_collision_free_with_boundary():
    result = run_script(
        "bt1702_holonet_scheduler_collision_audit.py",
        "bt1702_holonet_scheduler_collision_audit.json",
    )

    assert result["verified"] is True
    assert result["checks"]["extended_keys_are_collision_free"] is True
    assert result["checks"]["timesliced_shared_bus_is_collision_free"] is True
    assert result["checks"]["shared_physical_bus_reuse_is_explicit"] is True
    for row in result["depth_audits"]:
        assert row["extended_collision_count"] == 0
        assert row["timesliced_collision_count"] == 0
        assert row["extended_keys"] == row["expected_keys"]


def test_bt1703_symbolic_faults_have_finite_exits():
    result = run_script(
        "bt1703_holonet_fault_propagation_simulator.py",
        "bt1703_holonet_fault_propagation_simulator.json",
    )

    assert result["verified"] is True
    assert result["histograms"]["fault_type"] == {
        "DARK_CLICK": 8,
        "LOSS": 72,
        "PARITY": 24,
    }
    assert result["checks"]["all_faults_classified"] is True
    assert result["checks"]["parity_faults_enter_css_handoff"] is True
    assert result["checks"]["dark_faults_terminate_locally"] is True
    assert result["checks"]["no_unhandled_exit"] is True


def test_bt1701_bt1703_publication_anchors():
    run_script(
        "bt1703_holonet_fault_propagation_simulator.py",
        "bt1703_holonet_fault_propagation_simulator.json",
    )
    note = (ROOT / "analysis" / "BT1701_BT1703_holonet_runtime_safety.md").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")

    assert "BT1701-BT1703" in note
    assert "Holonet Runtime Safety" in docs
    assert "test_bt1701_bt1703_holonet_runtime_safety.py" in focused
    assert "BT1701--BT1703 runtime safety layer" in paper
