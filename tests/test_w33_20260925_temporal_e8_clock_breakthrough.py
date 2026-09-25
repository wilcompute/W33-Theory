import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


def test_hesse_clock_has_both_exceptional_gradings():
    x = load("w33_20260925_hesse_clock_e8_gradings.json")
    assert x["status"] == "PASS_HESSE_CLOCK_GENERATES_CONTACT_AND_CUBIC_E8_GRADINGS"
    assert x["single_tick_contact_grading"]["Lie_dimensions"] == [1, 56, 134, 56, 1]
    assert x["oriented_three_tick_grading"]["Lie_dimensions"] == [2, 27, 54, 82, 54, 27, 2]
    assert x["oriented_three_tick_grading"]["positive_nilpotent_growth"] == [54, 81, 83]
    assert x["oriented_three_tick_grading"]["all_24_clock_choices_verified"] is True


def test_signed_cubic_closes_the_clock_ladder():
    x = load("w33_20260925_cubic_clock_bracket_ladder.json")
    assert x["status"] == "PASS_SIGNED_E6_CUBIC_GENERATES_EXACT_54_81_83_CLOCK_LADDER"
    assert x["graded_model"]["growth_vector"] == [54, 81, 83]
    assert x["graded_model"]["dim_g2"] == 27
    assert x["graded_model"]["dim_g3"] == 2
    assert x["graded_model"]["same_temporal_ray_bracket_is_zero"] is True
    assert x["graded_model"]["two_temporal_rays_generate_all_g2"] is True
    assert x["cubic_tick"]["jacobi_basis_checks"] == 360

def test_frozen_ce2_grading_is_exact_integer_clock_shadow():
    x = load("w33_20260925_e8_parabolic_cubic_clock_lift.json")
    assert x["status"] == (
        "PASS_CE2_Z3_IS_MOD3_SHADOW_OF_EXACT_E8_THREE_STEP_CUBIC_CLOCK_GRADING"
    )
    assert x["bracket_growth"]["growth_vector"] == [54, 81, 83]
    assert x["grading"]["mod3_dimensions"] == {"g0": 86, "g1": 81, "g2": 81}
    assert x["grading"]["structure_constant_terms_checked"] == 8347
    assert x["cubic_clock"]["canonical_E6_triads"] == 45
    assert x["cubic_clock"]["nested_support_equals_canonical_45_E6_cubic_triads"]
    assert x["cubic_clock"]["coefficient_identity_checked_on_all_45_triads"]
