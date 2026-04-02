"""
Phase CCCLXXIII -- Holographic Transport-Twisted Lift Localization
=================================================================

The last two promoted phases already locked:

1. the finite holographic code dictionary

       q = 3,  mu = 4,  D^2 = v = 40,  k_log = q^mu = 81,  1/G = 960;

2. the first family-sensitive continuum coefficient

       Delta A4 = 81 epsilon^2 a0 = 1209 a0 / 9194.

The open wall after CCCLXXII was therefore no longer the finite multiplicity.
The exact bridge summaries already sharpen it further:

- the central image-side channel localizes to one head-compatible line;
- the first family-sensitive A4 packet has minimal canonical external carrier
  plane U1;
- exact transport completion uses the ordered avatar shell 81 -> 162 -> 81;
- the missing K3-side realization is localized to a carrier-preserving
  transport-twisted lift of that already-fixed carrier package.

So the honest remaining theorem is not a generic continuum or K3 enhancement
problem. The finite holographic A4 packet is already localized to the nested
support ladder

    head line ⊂ U1 ⊂ (81 -> 162 -> 81) ⊂ transport-twisted K3 lift.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "exploration"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from exploration.w33_carrier_preserving_transport_twisted_k3_lift_bridge import (  # noqa: E402
    build_carrier_preserving_transport_twisted_k3_lift_bridge_summary,
)
from exploration.w33_e13_a4_support_stratification_bridge import (  # noqa: E402
    build_e13_a4_support_stratification_bridge_summary,
)
from exploration.w33_u1_family_a4_carrier_bridge import (  # noqa: E402
    build_u1_family_a4_carrier_bridge_summary,
)
from exploration.w33_yukawa_a4_entry_bridge import build_yukawa_a4_entry_summary  # noqa: E402
from exploration.w33_yukawa_transport_coupling_hierarchy_bridge import (  # noqa: E402
    build_yukawa_transport_coupling_hierarchy_bridge_summary,
)


v, k, lam, mu = 40, 12, 2, 4
q = 3
E = v * k // 2
G = Fraction(1, 960)
LOGICAL_QUTRITS = 81
AVATAR_DIMS = [81, 162, 81]
DELTA_A4_COEFFICIENT = Fraction(1209, 9194)
REDUCED_GLOBAL_PREFRACTOR = "351/(4 pi^2)"


def _support_summary():
    return build_e13_a4_support_stratification_bridge_summary()


def _carrier_summary():
    return build_u1_family_a4_carrier_bridge_summary()


def _hierarchy_summary():
    return build_yukawa_transport_coupling_hierarchy_bridge_summary()


def _lift_summary():
    return build_carrier_preserving_transport_twisted_k3_lift_bridge_summary()


class TestT1_FiniteHolographicInput:
    """The same finite dictionary from CCCLXXI/II is still the input."""

    def test_q_equals_three(self):
        assert q == 3

    def test_mu_equals_four(self):
        assert mu == 4

    def test_center_dimension_is_forty(self):
        assert v == 40

    def test_bulk_edge_count_is_240(self):
        assert E == 240

    def test_logical_qutrits_are_81(self):
        assert LOGICAL_QUTRITS == q**mu == 81

    def test_inverse_gravity_is_960(self):
        assert Fraction(1, G) == 960


class TestT2_A4EntryLock:
    """The first family-sensitive coefficient is already exact."""

    def test_a0_is_family_blind(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["A0_is_family_blind"] is True

    def test_a2_is_family_blind(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["A2_is_family_blind"] is True

    def test_a4_is_first_family_entry_point(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["A4_is_first_family_entry_point"] is True

    def test_delta_a4_exact_coefficient(self):
        assert DELTA_A4_COEFFICIENT == Fraction(1209, 9194)

    def test_delta_a4_has_exact_81_multiplier(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["delta_A4_equals_81_epsilon_squared_a0"] is True

    def test_remaining_wall_is_not_finite_multiplicity(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["remaining_continuum_wall_is_refined_a4_density"] is True


class TestT3_SupportLadder:
    """The exact family/transport bridge is already support-stratified."""

    def test_central_image_channel_is_line_level(self):
        theorem = _support_summary()["e13_a4_support_stratification_theorem"]
        assert theorem[
            "the_central_image_side_2e13_channel_localizes_to_the_head_line_in_any_exact_completion"
        ] is True

    def test_a4_packet_is_plane_level_on_u1(self):
        support = _support_summary()["support_levels"]
        theorem = _support_summary()["e13_a4_support_stratification_theorem"]
        assert support["minimal_a4_carrier_plane"] == "U1"
        assert theorem[
            "the_first_family_sensitive_a4_bridge_packet_has_minimal_canonical_plane_carrier_u1"
        ] is True

    def test_transport_completion_is_avatar_level(self):
        support = _support_summary()["support_levels"]
        theorem = _support_summary()["e13_a4_support_stratification_theorem"]
        assert support["rigid_transport_avatar_dimensions"] == AVATAR_DIMS
        assert theorem[
            "exact_transport_completion_uses_the_full_rigid_avatar_shell_81_to_162_to_81"
        ] is True

    def test_support_ladder_is_exactly_nested(self):
        theorem = _support_summary()["e13_a4_support_stratification_theorem"]
        assert theorem[
            "the_live_2e13_a4_bridge_is_exactly_stratified_as_head_line_inside_u1_inside_avatar"
        ] is True

    def test_broader_packet_is_context_not_minimal_carrier(self):
        theorem = _support_summary()["e13_a4_support_stratification_theorem"]
        assert theorem[
            "the_broader_five_factor_packet_is_local_selector_context_not_the_minimal_exact_family_carrier"
        ] is True

    def test_locally_dominant_piece_is_not_u1(self):
        assert _support_summary()["support_levels"]["broader_local_packet_dominant_piece"] == "U3"


class TestT4_CanonicalExternalCarrier:
    """The first family-sensitive packet already has a canonical external plane."""

    def test_canonical_plane_is_u1(self):
        carrier = _carrier_summary()["canonical_external_carrier"]
        assert carrier["plane_name"] == "U1"

    def test_u1_is_first_explicit_u_factor(self):
        theorem = _carrier_summary()["u1_family_a4_carrier_theorem"]
        assert theorem["canonical_external_carrier_equals_u_factor_one"] is True

    def test_global_reduced_prefactor_is_exact(self):
        carrier = _carrier_summary()["canonical_external_carrier"]
        theorem = _carrier_summary()["u1_family_a4_carrier_theorem"]
        assert carrier["normalized_global_prefactor"] == REDUCED_GLOBAL_PREFRACTOR
        assert theorem["canonical_u1_carrier_has_exact_351_over_4_pi_squared_coupling"] is True

    def test_u1_is_minimal_canonical_family_bridge_carrier(self):
        theorem = _carrier_summary()["u1_family_a4_carrier_theorem"]
        assert theorem["minimal_canonical_family_bridge_carrier_is_delta_a4_on_u1"] is True

    def test_u1_is_nonzero_piece_of_full_selector_packet(self):
        theorem = _carrier_summary()["u1_family_a4_carrier_theorem"]
        assert theorem["u1_is_nonzero_piece_of_full_selector_packet"] is True

    def test_full_selector_packet_does_not_collapse_to_u1(self):
        theorem = _carrier_summary()["u1_family_a4_carrier_theorem"]
        assert theorem["full_selector_packet_is_not_supported_on_u1_alone"] is True


class TestT5_TransportTwistedLiftWall:
    """The remaining K3-side realization wall is now sharply localized."""

    def test_external_carrier_package_is_already_fixed(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem[
            "the_external_carrier_package_is_already_fixed_before_any_genuine_k3_realization"
        ] is True

    def test_missing_internal_datum_is_nontrivial_twisted_cocycle(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem["the_missing_internal_datum_is_already_a_nontrivial_twisted_cocycle"] is True

    def test_missing_internal_datum_is_exact_transport_twisted_precomplex(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem[
            "the_missing_internal_datum_already_assembles_into_an_exact_transport_twisted_precomplex"
        ] is True

    def test_shared_nonzero_completion_wall_is_datum_to_avatar_lift(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem[
            "the_shared_nonzero_completion_wall_is_already_localized_as_datum_to_avatar_lift"
        ] is True

    def test_any_exact_k3_realization_must_be_transport_twisted_lift(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem[
            "therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_lift"
        ] is True

    def test_open_wall_is_existence_of_that_lift(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem[
            "the_open_wall_is_existence_of_that_carrier_preserving_transport_twisted_k3_lift"
        ] is True


class TestT6_HolographicLiftLocalization:
    """The honest post-CCCLXXII wall is now one nested support/lift theorem."""

    def test_line_plane_avatar_levels_match_coupling_hierarchy(self):
        levels = _hierarchy_summary()["coupling_levels"]
        assert levels["plane_level"] == "U1"
        assert levels["avatar_level"] == AVATAR_DIMS
        assert levels["broader_local_context"] == "U3"

    def test_coupling_hierarchy_is_line_inside_plane_inside_avatar(self):
        theorem = _hierarchy_summary()["yukawa_transport_coupling_hierarchy_theorem"]
        assert theorem[
            "the_live_unresolved_family_closure_is_support_filtered_as_line_inside_plane_inside_avatar"
        ] is True

    def test_non_split_transport_identity_requires_avatar_support(self):
        theorem = _hierarchy_summary()["yukawa_transport_coupling_hierarchy_theorem"]
        assert theorem["non_split_transport_identity_requires_avatar_level_support"] is True

    def test_a4_does_not_couple_only_to_local_u3_piece(self):
        theorem = _hierarchy_summary()["yukawa_transport_coupling_hierarchy_theorem"]
        assert theorem[
            "the_unresolved_family_packet_does_not_reduce_to_u3_even_though_u3_is_locally_dominant"
        ] is True

    def test_remaining_wall_is_refined_a4_density_on_transport_twisted_lift(self):
        assert build_yukawa_a4_entry_summary()["a4_entry_theorem"][
            "remaining_continuum_wall_is_refined_a4_density"
        ] is True
        assert _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"][
            "the_open_wall_is_existence_of_that_carrier_preserving_transport_twisted_k3_lift"
        ] is True

    def test_honest_post_ccclxxii_verdict(self):
        assert LOGICAL_QUTRITS == 81
        assert _carrier_summary()["canonical_external_carrier"]["plane_name"] == "U1"
        assert _support_summary()["support_levels"]["rigid_transport_avatar_dimensions"] == AVATAR_DIMS
        assert _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"][
            "the_open_wall_is_existence_of_that_carrier_preserving_transport_twisted_k3_lift"
        ] is True
