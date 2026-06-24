import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(name: str, data_name: str) -> dict:
    subprocess.run(
        [sys.executable, str(ROOT / "analysis" / name)],
        cwd=ROOT,
        check=True,
    )
    return json.loads((ROOT / "data" / data_name).read_text(encoding="utf-8"))


def test_bt1698_packet_state_machine_is_deterministic():
    result = run_script(
        "bt1698_holonet_packet_state_machine.py",
        "bt1698_holonet_packet_state_machine.json",
    )

    assert result["verified"] is True
    checks = result["checks"]
    assert checks["trace_has_72_ticks"] is True
    assert checks["ticks_are_contiguous_0_to_71"] is True
    assert checks["body_has_16_three_phase_edges"] is True
    assert checks["body_edges_chain_without_gap"] is True
    assert checks["epilogue_words_are_eight_tick_clifford_returns"] is True
    assert result["state_machine_identity"]["body_ops"] == [
        "LOAD_FLAG",
        "FLIP_Q6_AXIS",
        "LATCH_VERTEX",
    ]


def test_bt1699_lowers_abi_to_hardware_stages():
    result = run_script(
        "bt1699_holonet_abi_to_hardware_lowering.py",
        "bt1699_holonet_abi_to_hardware_lowering.json",
    )

    assert result["verified"] is True
    assert result["stage_histogram"] == {
        "analyzer_or_fuel_body": 16,
        "dark_reference": 8,
        "detector_or_hesse_handoff": 16,
        "program_delay": 24,
        "source_switch": 8,
    }
    assert result["checks"]["guard_weld_aligns_port_css_magic_flags"] is True
    assert result["checks"]["time_bin_envelope_is_1600_plus_448"] is True
    assert result["cycle_totals"]["ticks"] == 115200
    assert len(result["guard_weld"]) == 24


def test_bt1700_recursive_compiler_preserves_local_abi():
    result = run_script(
        "bt1700_recursive_holonet_packet_compiler.py",
        "bt1700_recursive_holonet_packet_compiler.json",
    )

    assert result["verified"] is True
    layers = result["layers"]
    assert [row["depth"] for row in layers] == list(range(6))
    assert layers[0]["total_ticks"] == 72
    assert layers[1]["packet_count"] == 40
    assert layers[2]["packet_count"] == 1600
    assert all(row["body_ticks"] == 2 * row["guard_ticks"] for row in layers)
    assert all(row["route_bound_8n"] == 8 * row["depth"] for row in layers)
    assert all(
        row["phase_scheduler_slots"] == 2160 * row["packet_count"] for row in layers
    )
    assert all(
        row["clifford_supercycle_slots"] == 51840 * row["packet_count"]
        for row in layers
    )


def test_bt1698_bt1700_publication_anchors():
    run_script(
        "bt1700_recursive_holonet_packet_compiler.py",
        "bt1700_recursive_holonet_packet_compiler.json",
    )
    note = (ROOT / "analysis" / "BT1698_BT1700_holonet_execution_stack.md").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")

    assert "BT1698-BT1700" in note
    assert "Holonet Execution Stack" in docs
    assert "test_bt1698_bt1700_holonet_execution_stack.py" in focused
    assert "BT1698--BT1700 execution stack" in paper
