from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
if str(EXPLORATION) not in sys.path:
    sys.path.insert(0, str(EXPLORATION))

from w33_transport_twisted_k3_target_uniqueness_bridge import (  # noqa: E402
    build_transport_twisted_k3_target_uniqueness_bridge_summary,
)


def test_transport_twisted_k3_target_avatar_is_unique() -> None:
    summary = build_transport_twisted_k3_target_uniqueness_bridge_summary()
    avatar = summary["unique_transport_twisted_target_avatar"]
    theorem = summary["transport_twisted_k3_target_uniqueness_theorem"]

    assert avatar["carrier_plane"] == "U1"
    assert avatar["ordered_filtration_dimensions"] == [81, 162, 81]
    assert avatar["slot_direction"] == "tail_to_head"
    assert avatar["slot_matrix_normal_form"] == "I_81"
    assert avatar["polarized_nilpotent_normal_form"] == "J2^81"

    assert theorem["the_head_line_carrier_plane_and_shell_are_already_fixed"] is True
    assert (
        theorem[
            "the_only_missing_slot_state_is_the_unique_nonzero_orbit_in_the_existing_slot"
        ]
        is True
    )
    assert (
        theorem["the_formal_completion_avatar_is_unique_up_to_head_tail_basis_gauge"]
        is True
    )
    assert (
        theorem["any_exact_k3_side_realization_must_target_that_same_unique_avatar"]
        is True
    )
    assert (
        theorem[
            "the_live_wall_is_existence_of_a_realization_of_one_unique_transport_twisted_avatar"
        ]
        is True
    )
