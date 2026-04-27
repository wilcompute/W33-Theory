from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
if str(EXPLORATION) not in sys.path:
    sys.path.insert(0, str(EXPLORATION))

from w33_h4_ordered_path_k3_witness_bridge import (  # noqa: E402
    build_h4_ordered_path_k3_witness_bridge_summary,
)


def test_h4_ordered_path_bridge_records_shared_transport_shadow() -> None:
    summary = build_h4_ordered_path_k3_witness_bridge_summary()

    assert summary["finite_ordered_path_carrier"] == {
        "path_count": 4320,
        "seed_stabilizer_size": 6,
        "completion_fibre_size": 3,
        "seed_completion_action_size": 6,
    }
    assert summary["shared_transport_shadow"] == {
        "reduced_group_order": 6,
        "unique_invariant_projective_line": [1, 2],
        "invariant_complement_count": 0,
        "is_nonsplit_extension_of_sign_by_trivial": True,
        "fiber_nilpotent_increment": [[0, 1], [0, 0]],
        "matter_extension_dimensions": [81, 162, 81],
        "matter_extension_rank": 81,
    }


def test_h4_ordered_path_bridge_records_k3_chart_target() -> None:
    summary = build_h4_ordered_path_k3_witness_bridge_summary()

    assert summary["k3_witness_chart"] == {
        "carrier_plane": "U1",
        "ordered_filtration_dimensions": [81, 162, 81],
        "canonical_mixed_plane_split": [81, 81],
        "canonical_nonzero_increment": [[0, 1], [0, 0]],
        "target_coordinate": "dC",
        "required_value": "14105",
        "primitive_c_direction": "780",
        "transport_scale": "217/12",
        "factorization": "780 * (217/12)",
    }


def test_h4_ordered_path_bridge_theorem_holds_without_erasing_the_existence_wall() -> None:
    theorem = build_h4_ordered_path_k3_witness_bridge_summary()["theorem"]
    assert all(theorem.values())