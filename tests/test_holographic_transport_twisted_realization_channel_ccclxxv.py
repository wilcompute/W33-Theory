"""
Phase CCCLXXV -- Holographic Transport-Twisted Realization Channel
==================================================================

CCCLXXIV reduced the live K3 wall to existence of one unique transport-twisted
target avatar. The next exact question is therefore not “which avatar?” but
“where can a genuine realization live inside that fixed avatar?”

The promoted transport stack already answers this sharply:

- the transport Bose-Mesner / heat selector canonically fixes one protected
  flat ``81``-dimensional matter copy;
- the exact coupled curved transport package hits only the complementary
  ``81`` copy;
- the internal nilpotent transport operator has image = kernel = the
  invariant/head ``81`` channel; and
- the unique target avatar already fixes the tail-to-head activation slot on
  the shell ``81 -> 162 -> 81``.

So the honest remaining wall is now one realization-channel problem. Any
genuine K3-side transport-twisted lift must preserve the protected head ``81``
and activate only the complementary curvature-sensitive tail ``81`` into that
head.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "exploration"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from exploration.w33_transport_spectral_selector_bridge import (  # noqa: E402
    build_transport_spectral_selector_summary,
)
from exploration.w33_transport_matter_curved_harmonic_bridge import (  # noqa: E402
    build_transport_matter_curved_harmonic_summary,
)
from exploration.w33_transport_polarized_line_shadow_bridge import (  # noqa: E402
    build_transport_polarized_line_shadow_bridge_summary,
)
from exploration.w33_transport_twisted_k3_realization_channel_bridge import (  # noqa: E402
    build_transport_twisted_k3_realization_channel_bridge_summary,
)
from exploration.w33_transport_twisted_k3_target_uniqueness_bridge import (  # noqa: E402
    build_transport_twisted_k3_target_uniqueness_bridge_summary,
)


q = 3
mu = 4
LOGICAL_QUTRITS = 81
AVATAR_DIMS = [81, 162, 81]
G = Fraction(1, 960)


def _selector_summary():
    return build_transport_spectral_selector_summary()


def _matter_summary():
    return build_transport_matter_curved_harmonic_summary()


def _polarized_summary():
    return build_transport_polarized_line_shadow_bridge_summary()


def _uniqueness_summary():
    return build_transport_twisted_k3_target_uniqueness_bridge_summary()


def _channel_summary():
    return build_transport_twisted_k3_realization_channel_bridge_summary()


class TestT1_HolographicInputStillLocked:
    """The same finite holographic packet remains the input."""

    def test_q_equals_three(self):
        assert q == 3

    def test_mu_equals_four(self):
        assert mu == 4

    def test_logical_qutrits_are_81(self):
        assert LOGICAL_QUTRITS == q**mu == 81

    def test_inverse_gravity_is_960(self):
        assert Fraction(1, G) == 960

    def test_avatar_dimensions_remain_fixed(self):
        assert AVATAR_DIMS == [81, 162, 81]

    def test_target_uniqueness_is_the_previous_frontier(self):
        theorem = _uniqueness_summary()["transport_twisted_k3_target_uniqueness_theorem"]
        assert theorem[
            "the_live_wall_is_existence_of_a_realization_of_one_unique_transport_twisted_avatar"
        ] is True


class TestT2_ProtectedSelectorChannel:
    """One 81-copy is now canonically protected by spectral data."""

    def test_w33_mod3_kernel_is_unique(self):
        base = _selector_summary()["w33_base_selector"]
        assert base["kernel_dimension_mod_3"] == 1

    def test_w33_all_ones_spans_mod3_kernel(self):
        base = _selector_summary()["w33_base_selector"]
        assert base["all_ones_spans_mod_3_kernel"] is True

    def test_transport_projector_is_exact_trivial_selector(self):
        transport = _selector_summary()["transport_selector"]
        assert transport["projector_rank"] == 1
        assert transport["projector_idempotent"] is True

    def test_tensor_selector_rank_is_81(self):
        dynamic = _selector_summary()["dynamic_selection_bridge"]
        assert dynamic["protected_flat_selector_rank_after_tensoring"] == LOGICAL_QUTRITS

    def test_selector_matches_protected_flat_matter_dimension(self):
        dynamic = _selector_summary()["dynamic_selection_bridge"]
        assert dynamic["matches_protected_flat_matter_dimension"] is True

    def test_selector_lifts_to_243_and_1944(self):
        lifts = _selector_summary()["dynamic_selection_bridge"][
            "protected_flat_curved_harmonic_lifts"
        ]
        assert lifts["CP2_9"] == 243
        assert lifts["K3_16"] == 1944


class TestT3_ExactProtectedVsCurvedSplit:
    """The other 81-copy is exactly the curvature-sensitive complement."""

    def test_protected_flat_h0_is_exactly_one_81_copy(self):
        coupled = _matter_summary()["matter_coupled_precomplex"]
        assert coupled["protected_flat_h0_dimension"] == LOGICAL_QUTRITS

    def test_protected_flat_sector_is_exactly_one_81_copy(self):
        coupled = _matter_summary()["matter_coupled_precomplex"]
        assert coupled["protected_flat_sector_is_exactly_one_81_copy"] is True

    def test_curvature_hits_only_the_other_81_copy(self):
        coupled = _matter_summary()["matter_coupled_precomplex"]
        assert coupled["curvature_hits_only_the_other_81_copy"] is True

    def test_internal_head_type_is_invariant(self):
        polarization = _polarized_summary()["internal_transport_polarization"]
        assert polarization["head_type"] == "invariant"

    def test_internal_tail_type_is_sign(self):
        polarization = _polarized_summary()["internal_transport_polarization"]
        assert polarization["tail_type"] == "sign"

    def test_polarized_shell_stays_81_to_162_to_81(self):
        polarization = _polarized_summary()["internal_transport_polarization"]
        assert polarization["ordered_filtration_dimensions"] == AVATAR_DIMS


class TestT4_UniqueAvatarNowHasOneChannel:
    """The fixed avatar already determines the only admissible activation channel."""

    def test_unique_avatar_carrier_plane_is_u1(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["carrier_plane"] == "U1"

    def test_unique_avatar_slot_direction_is_tail_to_head(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["slot_direction"] == "tail_to_head"

    def test_unique_avatar_slot_normal_form_is_i81(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["slot_matrix_normal_form"] == "I_81"

    def test_unique_avatar_nilpotent_normal_form_is_j2_power_81(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["polarized_nilpotent_normal_form"] == "J2^81"

    def test_minimal_realization_channel_source_is_tail_81(self):
        channel = _channel_summary()["minimal_realization_channel"]
        assert channel["source_channel"] == "curvature_sensitive_sign_tail_81"

    def test_minimal_realization_channel_target_is_head_81(self):
        channel = _channel_summary()["minimal_realization_channel"]
        assert channel["target_channel"] == "protected_flat_invariant_head_81"


class TestT5_RealizationChannelTheorem:
    """Any genuine K3-side realization must use one fixed tail-to-head channel."""

    def test_transport_selector_fixes_one_protected_head_81(self):
        theorem = _channel_summary()["transport_twisted_k3_realization_channel_theorem"]
        assert theorem[
            "the_transport_spectral_selector_canonically_fixes_one_protected_flat_head_81_copy"
        ] is True

    def test_complementary_81_is_curvature_sensitive_tail(self):
        theorem = _channel_summary()["transport_twisted_k3_realization_channel_theorem"]
        assert theorem[
            "the_complementary_81_copy_is_exactly_the_curvature_sensitive_tail_channel"
        ] is True

    def test_internal_nilpotent_image_kernel_is_head_81(self):
        theorem = _channel_summary()["transport_twisted_k3_realization_channel_theorem"]
        assert theorem[
            "the_internal_transport_nilpotent_has_image_and_kernel_equal_to_the_protected_invariant_head_81"
        ] is True

    def test_unique_avatar_uses_tail_to_head_activation_on_fixed_split(self):
        theorem = _channel_summary()["transport_twisted_k3_realization_channel_theorem"]
        assert theorem[
            "the_unique_transport_twisted_target_avatar_uses_tail_to_head_activation_on_that_fixed_head_tail_split"
        ] is True

    def test_any_genuine_realization_preserves_protected_head_81(self):
        theorem = _channel_summary()["transport_twisted_k3_realization_channel_theorem"]
        assert theorem[
            "therefore_any_genuine_k3_side_realization_must_preserve_the_protected_head_81"
        ] is True

    def test_any_nonzero_twist_can_only_activate_curvature_sensitive_tail_81(self):
        theorem = _channel_summary()["transport_twisted_k3_realization_channel_theorem"]
        assert theorem[
            "and_any_nonzero_transport_twist_can_only_activate_the_complementary_curvature_sensitive_tail_81"
        ] is True


class TestT6_HolographicFrontierNowMeansOneChannel:
    """The remaining wall is existence of one realization channel, not more classification."""

    def test_live_wall_is_one_tail_to_head_realization_channel(self):
        theorem = _channel_summary()["transport_twisted_k3_realization_channel_theorem"]
        assert theorem[
            "the_live_wall_is_existence_of_one_tail_to_head_realization_channel_on_the_unique_avatar"
        ] is True

    def test_protected_head_channel_has_exact_243_1944_lifts(self):
        protected = _channel_summary()["canonical_protected_head_channel"]
        assert protected["curved_harmonic_lifts"] == {"CP2_9": 243, "K3_16": 1944}

    def test_curvature_sensitive_tail_channel_is_marked_as_curved(self):
        tail = _channel_summary()["canonical_curvature_sensitive_tail_channel"]
        assert tail["curvature_sensitive"] is True

    def test_minimal_channel_keeps_exact_avatar_dimensions(self):
        channel = _channel_summary()["minimal_realization_channel"]
        assert channel["ordered_filtration_dimensions"] == AVATAR_DIMS

    def test_bridge_verdict_mentions_protected_head_81(self):
        verdict = _channel_summary()["bridge_verdict"]
        assert "preserve the protected head 81" in verdict

    def test_bridge_verdict_mentions_one_tail_to_head_realization_channel(self):
        verdict = _channel_summary()["bridge_verdict"]
        assert "one tail-to-head realization channel" in verdict
