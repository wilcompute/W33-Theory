from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxxvii_holonomy_selector_bundle_bridge import build_bridge


def test_dclxxxvii_summary_matches_uniform_bundle_counts() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["affine_fiber_count"] == 9
    assert summary["ordered_adjacent_pair_count"] == 60
    assert summary["global_qutrit_fiber_count"] == 540
    assert summary["global_branch_count"] == 1620


def test_dclxxxvii_every_local_fiber_has_same_three_cycle_and_jordan_quotient() -> None:
    payload = build_bridge()
    local_bundle = payload["local_bundle"]

    assert local_bundle["reference_action"] == [1, 2, 0]
    assert all(action == [1, 2, 0] for action in local_bundle["fiber_actions"])
    assert all(matrix == local_bundle["reference_quotient_matrix_mod3"] for matrix in local_bundle["fiber_quotient_matrices"])
    assert local_bundle["quotient_in_jordan_basis"] == [[1, 1], [0, 1]]
    assert local_bundle["nilpotent_increment"] == [[0, 1], [0, 0]]


def test_dclxxxvii_global_bundle_is_540_times_3_equals_1620() -> None:
    payload = build_bridge()
    global_bundle = payload["global_bundle"]
    assert global_bundle["global_qutrit_fiber_count"] * global_bundle["branches_per_fiber"] == global_bundle["global_branch_count"] == 1620


def test_dclxxxvii_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())