"""Focused regression for the GAP-owned Pass 382 logic-switch controller."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")
PHASE_WORD = ["LOAD_FLAG", "FLIP_Q6_AXIS", "LATCH_VERTEX"]


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 382")
def test_pass382_constructs_the_reversible_logic_switch_controller() -> None:
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass382_reversible_logic_switch_controller.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass382 status=PASS" in result.stdout
    assert "states=48 tick_order=48 phase_orbits=16 phase_faults=16" in result.stdout

    certificate = json.loads(
        (ROOT / "data" / "w33_pass382_reversible_logic_switch_controller.json").read_text(
            encoding="utf-8"
        )
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 15 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["state_space"] == {
        "label": "Z/16 edge-step index x Z/3 phase",
        "states": 48,
        "edge_steps": 16,
        "phase_trits": 3,
        "phase_word": PHASE_WORD,
    }
    assert certificate["transition_semantics"] == {
        "tick": "T(edge,0)=(edge,1); T(edge,1)=(edge,2); T(edge,2)=(edge+1 mod 16,0)",
        "inverse": "T^-1(edge,0)=(edge-1 mod 16,2); T^-1(edge,1)=(edge,0); T^-1(edge,2)=(edge,1)",
        "phase_clock": "P(edge,phase)=(edge,phase+1 mod 3)",
        "tick_order": 48,
        "phase_clock_order": 3,
    }


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 382")
def test_pass382_transition_table_and_fault_syndromes_are_exact() -> None:
    subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass382_reversible_logic_switch_controller.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    certificate = json.loads(
        (ROOT / "data" / "w33_pass382_reversible_logic_switch_controller.json").read_text(
            encoding="utf-8"
        )
    )
    table = certificate["transition_table"]
    assert len(table) == 48
    assert [row["state"] for row in table] == [
        [edge, phase] for edge in range(16) for phase in range(3)
    ]
    assert [row["operation"] for row in table] == PHASE_WORD * 16
    assert table[0] == {
        "state": [0, 0],
        "operation": "LOAD_FLAG",
        "next_state": [0, 1],
        "previous_state": [15, 2],
        "phase_clock_next": [0, 1],
        "latch_advances_edge": False,
        "frame_wrap": False,
    }
    assert table[2]["next_state"] == [1, 0]
    assert [row["latch_advances_edge"] for row in table].count(True) == 16
    assert [row["frame_wrap"] for row in table].count(True) == 1
    assert table[-1]["next_state"] == [0, 0]

    assert certificate["fault_injection"] == {
        "phase_clock_substitution": {
            "map": "P replaces T",
            "mismatched_expected_ticks": 16,
            "mismatching_phases": [2],
            "orbit_sizes": [3],
            "syndrome_pairs": [[0, 32], [45, 16]],
        },
        "stutter": {
            "map": "identity replaces T",
            "mismatched_expected_ticks": 48,
            "orbit_sizes": [1],
            "syndrome_pairs": [[47, 48]],
        },
        "double_tick": {
            "map": "T^2 replaces T",
            "mismatched_expected_ticks": 48,
            "orbit_sizes": [24],
            "syndrome_pairs": [[1, 48]],
        },
    }


def test_pass382_scope_stays_an_abstract_controller_model() -> None:
    synthesis = (ROOT / "PASS382_REVERSIBLE_LOGIC_SWITCH_CONTROLLER.md").read_text(
        encoding="utf-8"
    )
    assert "does not bind a header" in synthesis
    assert "not a Q6 path closure" in synthesis
    assert "does not identify a physical oscillator" in synthesis
