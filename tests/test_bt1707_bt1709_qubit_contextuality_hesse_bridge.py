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


def test_bt1707_contextuality_ladder_is_symplectic_and_timed():
    result = run_script(
        "bt1707_qubit_contextuality_ladder.py",
        "bt1707_qubit_contextuality_ladder.json",
    )

    assert result["verified"] is True
    assert result["checks"]["symplectic_point_counts_match"] is True
    assert result["checks"]["symplectic_line_counts_match"] is True
    assert result["checks"]["three_qubit_degree_is_hexagon_line_count"] is True
    assert result["checks"]["split_cayley_aut_is_readout_times_packet_clock"] is True
    q3 = {row["qubits"]: row for row in result["ladder"]}[3]
    assert q3["hexagon_automorphism_order"] == 12096
    assert q3["reported_degree"] == 63


def test_bt1708_hexagon_tomotope_bus_matches_48_interface():
    result = run_script(
        "bt1708_hexagon_tomotope_contextual_bus.py",
        "bt1708_hexagon_tomotope_contextual_bus.json",
    )

    assert result["verified"] is True
    assert result["checks"]["q2025_domain_is_balanced_48"] is True
    assert result["checks"]["tomotope_middle_is_48_blocks"] is True
    assert result["checks"]["holonet_body_is_same_48_interface"] is True
    assert result["q2025_domain"]["incidences"] == 48
    assert result["split_cayley"]["automorphism_order"] == 168 * 72


def test_bt1709_binary_to_hesse_crossover_is_ag23():
    result = run_script(
        "bt1709_binary_to_hesse_qutrit_crossover.py",
        "bt1709_binary_to_hesse_qutrit_crossover.json",
    )

    assert result["verified"] is True
    assert result["checks"]["ring_order_splits_units_and_zero_divisors"] is True
    assert result["checks"]["all_pauli_factorizations_sum_to_doily"] is True
    assert result["checks"]["holonet_hesse_is_ag23_grid"] is True
    assert result["checks"]["pg23_closure_is_phi3"] is True
    assert result["marcelis_bridge"]["ag23_points"] == 9
    assert result["marcelis_bridge"]["pg23_points"] == 13


def test_bt1707_bt1709_publication_anchors():
    run_script(
        "bt1709_binary_to_hesse_qutrit_crossover.py",
        "bt1709_binary_to_hesse_qutrit_crossover.json",
    )
    note = (
        ROOT / "analysis" / "BT1707_BT1709_qubit_contextuality_hesse_bridge.md"
    ).read_text(encoding="utf-8")
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")

    assert "BT1707-BT1709" in note
    assert "Qubit Contextuality Hesse Bridge" in docs
    assert "test_bt1707_bt1709_qubit_contextuality_hesse_bridge.py" in focused
    assert "BT1707--BT1709 contextuality and Hesse crossover" in paper
