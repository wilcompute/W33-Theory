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


def test_bt1704_replay_is_deterministic():
    result = run_script(
        "bt1704_holonet_packet_replay_runner.py",
        "bt1704_holonet_packet_replay_runner.json",
    )

    assert result["verified"] is True
    assert len(result["event_log"]) == 72
    assert result["checks"]["replay_is_deterministic"] is True
    assert result["checks"]["final_hesse_word_done"] is True
    assert result["final_state"]["cursor"] == "HESSE_WORD:5:DONE"
    assert result["final_state"]["x_correction"] == "X^1"
    assert result["final_state"]["z_correction"] == "Z^2"


def test_bt1705_shared_bus_time_division_is_fair_and_bounded():
    result = run_script(
        "bt1705_holonet_shared_bus_time_division_simulator.py",
        "bt1705_holonet_shared_bus_time_division_simulator.json",
    )

    assert result["verified"] is True
    assert result["checks"]["all_profiles_collision_free"] is True
    assert result["checks"]["all_packets_served_once"] is True
    assert result["checks"]["jain_fairness_is_one"] is True
    profiles = {row["profile"]: row for row in result["profiles"]}
    assert profiles["depth1_burst"]["max_queue_depth"] == 40
    assert profiles["depth2_wavefront"]["max_queue_depth"] == 1561
    assert profiles["depth2_sequential"]["max_wait_slices"] == 0


def test_bt1706_retry_economics_are_parameterized_and_guarded():
    result = run_script(
        "bt1706_holonet_retry_economics.py",
        "bt1706_holonet_retry_economics.json",
    )

    assert result["verified"] is True
    assert result["checks"]["all_profiles_within_guard_budget"] is True
    assert result["checks"]["guard_limit_reaches_unit_pressure"] is True
    assert result["checks"]["css_load_comes_only_from_parity_faults"] is True
    profiles = {row["profile"]: row for row in result["profiles"]}
    assert (
        profiles["nominal_low"]["expected_retry_or_reprogram_per_packet"]["fraction"]
        == "2/3125"
    )
    assert (
        profiles["guard_budget_limit"]["guard_budget_pressure"]["LOSS"]["fraction"]
        == "1/1"
    )


def test_bt1704_bt1706_publication_anchors():
    run_script(
        "bt1706_holonet_retry_economics.py",
        "bt1706_holonet_retry_economics.json",
    )
    note = (
        ROOT / "analysis" / "BT1704_BT1706_holonet_replay_scheduling_economics.md"
    ).read_text(encoding="utf-8")
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")

    assert "BT1704-BT1706" in note
    assert "Holonet Replay Economics" in docs
    assert "test_bt1704_bt1706_holonet_replay_scheduling_economics.py" in focused
    assert "BT1704--BT1706 replay and retry economics" in paper
