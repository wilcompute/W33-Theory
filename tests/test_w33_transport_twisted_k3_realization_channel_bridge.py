from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
if str(EXPLORATION) not in sys.path:
    sys.path.insert(0, str(EXPLORATION))

from w33_transport_twisted_k3_realization_channel_bridge import (  # noqa: E402
    build_transport_twisted_k3_realization_channel_bridge_summary,
)


def test_transport_twisted_realization_channel_is_rigid() -> None:
    summary = build_transport_twisted_k3_realization_channel_bridge_summary()
    theorem = summary["transport_twisted_k3_realization_channel_theorem"]
    channel = summary["minimal_realization_channel"]

    assert summary["canonical_protected_head_channel"]["dimension"] == 81
    assert summary["canonical_curvature_sensitive_tail_channel"]["dimension"] == 81
    assert channel["source_channel"] == "curvature_sensitive_sign_tail_81"
    assert channel["target_channel"] == "protected_flat_invariant_head_81"
    assert channel["ordered_filtration_dimensions"] == [81, 162, 81]
    assert channel["slot_direction"] == "tail_to_head"

    assert theorem[
        "the_transport_spectral_selector_canonically_fixes_one_protected_flat_head_81_copy"
    ] is True
    assert theorem[
        "the_complementary_81_copy_is_exactly_the_curvature_sensitive_tail_channel"
    ] is True
    assert theorem[
        "the_internal_transport_nilpotent_has_image_and_kernel_equal_to_the_protected_invariant_head_81"
    ] is True
    assert theorem[
        "the_unique_transport_twisted_target_avatar_uses_tail_to_head_activation_on_that_fixed_head_tail_split"
    ] is True
    assert theorem[
        "therefore_any_genuine_k3_side_realization_must_preserve_the_protected_head_81"
    ] is True
    assert theorem[
        "and_any_nonzero_transport_twist_can_only_activate_the_complementary_curvature_sensitive_tail_81"
    ] is True
    assert theorem[
        "the_live_wall_is_existence_of_one_tail_to_head_realization_channel_on_the_unique_avatar"
    ] is True
