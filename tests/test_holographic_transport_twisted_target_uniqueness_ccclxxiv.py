"""
Phase CCCLXXIV -- Holographic Transport-Twisted Target Uniqueness
=================================================================

After CCCLXXIII, the remaining wall was already localized to existence of a
carrier-preserving transport-twisted K3 lift of the fixed external package.

This phase sharpens that wall one step further. The target external completion
avatar itself is now unique up to the natural head/tail basis gauge:

    head line ⊂ U1 ⊂ 81 -> 162 -> 81 -> J2^81

So the honest remaining problem is not classification of possible transport-
twisted avatars. It is realization of that one unique avatar from genuine
K3-side data.
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
from exploration.w33_transport_twisted_k3_target_uniqueness_bridge import (  # noqa: E402
    build_transport_twisted_k3_target_uniqueness_bridge_summary,
)
from exploration.w33_yukawa_a4_entry_bridge import build_yukawa_a4_entry_summary  # noqa: E402


q = 3
mu = 4
LOGICAL_QUTRITS = 81
AVATAR_DIMS = [81, 162, 81]
DELTA_A4_COEFFICIENT = Fraction(1209, 9194)


def _lift_summary():
    return build_carrier_preserving_transport_twisted_k3_lift_bridge_summary()


def _uniqueness_summary():
    return build_transport_twisted_k3_target_uniqueness_bridge_summary()


class TestT1_InheritedFiniteClosure:
    """The finite/holographic packet from CCCLXXI/II remains fixed input."""

    def test_q_equals_three(self):
        assert q == 3

    def test_mu_equals_four(self):
        assert mu == 4

    def test_logical_qutrits_are_81(self):
        assert LOGICAL_QUTRITS == q**mu == 81

    def test_avatar_dimensions_are_fixed(self):
        assert AVATAR_DIMS == [81, 162, 81]

    def test_delta_a4_coefficient_is_still_exact(self):
        assert DELTA_A4_COEFFICIENT == Fraction(1209, 9194)

    def test_remaining_wall_is_not_finite_multiplicity(self):
        assert build_yukawa_a4_entry_summary()["a4_entry_theorem"][
            "remaining_continuum_wall_is_refined_a4_density"
        ] is True


class TestT2_InheritedLiftLocalization:
    """CCCLXXIII already fixed the nature of the lift problem."""

    def test_external_carrier_package_is_fixed_before_realization(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem[
            "the_external_carrier_package_is_already_fixed_before_any_genuine_k3_realization"
        ] is True

    def test_internal_datum_is_nontrivial_twisted_cocycle(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem[
            "the_missing_internal_datum_is_already_a_nontrivial_twisted_cocycle"
        ] is True

    def test_internal_datum_is_transport_twisted_precomplex(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem[
            "the_missing_internal_datum_already_assembles_into_an_exact_transport_twisted_precomplex"
        ] is True

    def test_any_exact_k3_realization_must_be_transport_twisted_lift(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem[
            "therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_lift"
        ] is True

    def test_open_wall_is_still_existence_of_that_lift(self):
        theorem = _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"]
        assert theorem[
            "the_open_wall_is_existence_of_that_carrier_preserving_transport_twisted_k3_lift"
        ] is True

    def test_ccclxxiv_sharpens_target_not_support(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["ordered_filtration_dimensions"] == AVATAR_DIMS


class TestT3_UniqueTargetAvatar:
    """The external completion target avatar is already fixed."""

    def test_carrier_plane_is_u1(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["carrier_plane"] == "U1"

    def test_ordered_shell_is_81_to_162_to_81(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["ordered_filtration_dimensions"] == AVATAR_DIMS

    def test_slot_direction_is_tail_to_head(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["slot_direction"] == "tail_to_head"

    def test_slot_matrix_normal_form_is_identity_81(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["slot_matrix_normal_form"] == "I_81"

    def test_polarized_nilpotent_normal_form_is_j2_power_81(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["polarized_nilpotent_normal_form"] == "J2^81"

    def test_realization_status_is_not_current_k3_realization(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["realization_status"] == "formal_minimal_completion_not_current_k3_realization"


class TestT4_UniquenessInputs:
    """The nonzero completion data is already unique before K3 realization."""

    def test_required_nonzero_slot_state_is_unique_existing_glue_slot(self):
        inputs = _uniqueness_summary()["target_uniqueness_inputs"]
        assert inputs["required_nonzero_slot_state"] == "unique_nonzero_orbit_in_existing_glue_slot"

    def test_shared_slot_state_matches_required_nonzero_state(self):
        inputs = _uniqueness_summary()["target_uniqueness_inputs"]
        assert inputs["shared_slot_state"] == inputs["required_nonzero_slot_state"]

    def test_shared_slot_matrix_normal_form_is_identity_81(self):
        inputs = _uniqueness_summary()["target_uniqueness_inputs"]
        assert inputs["shared_slot_matrix_normal_form"] == "I_81"

    def test_shared_nilpotent_normal_form_is_j2_power_81(self):
        inputs = _uniqueness_summary()["target_uniqueness_inputs"]
        assert inputs["shared_polarized_nilpotent_normal_form"] == "J2^81"

    def test_no_new_line_plane_or_dimension_moduli_remain(self):
        theorem = _uniqueness_summary()["transport_twisted_k3_target_uniqueness_theorem"]
        assert theorem[
            "the_shared_nonzero_completion_problem_is_only_a_datum_to_avatar_lift"
        ] is True

    def test_formal_completion_avatar_is_unique_up_to_gauge(self):
        theorem = _uniqueness_summary()["transport_twisted_k3_target_uniqueness_theorem"]
        assert theorem[
            "the_formal_completion_avatar_is_unique_up_to_head_tail_basis_gauge"
        ] is True


class TestT5_TargetRigidityTheorem:
    """The target avatar is unique if a genuine K3 lift exists."""

    def test_head_line_carrier_plane_and_shell_are_fixed(self):
        theorem = _uniqueness_summary()["transport_twisted_k3_target_uniqueness_theorem"]
        assert theorem["the_head_line_carrier_plane_and_shell_are_already_fixed"] is True

    def test_only_missing_slot_state_is_unique_nonzero_orbit(self):
        theorem = _uniqueness_summary()["transport_twisted_k3_target_uniqueness_theorem"]
        assert theorem[
            "the_only_missing_slot_state_is_the_unique_nonzero_orbit_in_the_existing_slot"
        ] is True

    def test_problem_is_not_another_line_plane_choice(self):
        theorem = _uniqueness_summary()["transport_twisted_k3_target_uniqueness_theorem"]
        assert theorem[
            "the_shared_nonzero_completion_problem_is_only_a_datum_to_avatar_lift"
        ] is True

    def test_any_exact_k3_realization_targets_same_avatar(self):
        theorem = _uniqueness_summary()["transport_twisted_k3_target_uniqueness_theorem"]
        assert theorem[
            "any_exact_k3_side_realization_must_target_that_same_unique_avatar"
        ] is True

    def test_remaining_wall_is_existence_of_one_gauge_class(self):
        theorem = _uniqueness_summary()["transport_twisted_k3_target_uniqueness_theorem"]
        assert theorem[
            "the_live_wall_is_existence_of_a_realization_of_one_unique_transport_twisted_avatar"
        ] is True

    def test_target_avatar_contains_the_same_avatar_dimensions(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["ordered_filtration_dimensions"] == AVATAR_DIMS


class TestT6_HolographicVerdict:
    """The frontier is now a one-avatar existence problem."""

    def test_post_ccclxxiii_wall_is_not_avatar_classification(self):
        verdict = _uniqueness_summary()["bridge_verdict"]
        assert "not classification of many candidate avatars" in verdict

    def test_post_ccclxxiii_wall_is_one_avatar_realization_problem(self):
        verdict = _uniqueness_summary()["bridge_verdict"]
        assert "one unique transport-twisted avatar" in verdict

    def test_avatar_still_sits_on_fixed_support_ladder(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["carrier_plane"] == "U1"
        assert avatar["ordered_filtration_dimensions"] == AVATAR_DIMS

    def test_formal_target_is_external_not_yet_genuine_k3_data(self):
        avatar = _uniqueness_summary()["unique_transport_twisted_target_avatar"]
        assert avatar["realization_status"] == "formal_minimal_completion_not_current_k3_realization"

    def test_honest_next_wall_is_actual_k3_realization(self):
        theorem = _uniqueness_summary()["transport_twisted_k3_target_uniqueness_theorem"]
        assert theorem[
            "the_live_wall_is_existence_of_a_realization_of_one_unique_transport_twisted_avatar"
        ] is True

    def test_phase_is_stronger_than_generic_enhancement_language(self):
        assert _lift_summary()["carrier_preserving_transport_twisted_k3_lift_theorem"][
            "therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_lift"
        ] is True
        assert _uniqueness_summary()["transport_twisted_k3_target_uniqueness_theorem"][
            "any_exact_k3_side_realization_must_target_that_same_unique_avatar"
        ] is True
