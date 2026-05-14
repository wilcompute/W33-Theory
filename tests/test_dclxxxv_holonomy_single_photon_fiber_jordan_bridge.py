from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxxv_holonomy_single_photon_fiber_jordan_bridge import build_bridge


def test_dclxxxv_summary_counts_match_expected_runtime_shell() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["field_order"] == 3
    assert summary["pauli_frame_size"] == 81
    assert summary["projective_frame_size"] == 40
    assert summary["zero_state_count"] == 1
    assert summary["fixed_frame_state_count"] == 26
    assert summary["mobile_frame_state_count"] == 54
    assert summary["mobile_packet_count"] == 9
    assert summary["mobile_projective_fiber_size"] == 3
    assert summary["mobile_frame_packet_size"] == 6


def test_dclxxxv_frame_decomposition_is_exactly_one_plus_twenty_six_plus_fifty_four() -> None:
    payload = build_bridge()
    summary = payload["summary"]
    assert 1 + summary["fixed_frame_state_count"] + summary["mobile_frame_state_count"] == 81


def test_dclxxxv_local_three_cycle_reduces_to_exact_jordan_block() -> None:
    payload = build_bridge()
    local = payload["local_fiber_dynamics"]

    assert local["sample_projective_action"] == [1, 2, 0]
    assert local["quotient_in_jordan_basis"] == [[1, 1], [0, 1]]
    assert local["reduced_nilpotent_increment"] == [[0, 1], [0, 0]]


def test_dclxxxv_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())