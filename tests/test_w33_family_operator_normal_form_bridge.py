from __future__ import annotations

from exploration.w33_family_operator_normal_form_bridge import build_summary


def test_family_operator_normal_form_bridge() -> None:
    summary = build_summary()
    theorem = summary["family_operator_normal_form_theorem"]
    operators = summary["exact_family_operator_normal_forms"]

    assert theorem["the_live_ckm_family_operator_is_exactly_a_single_quark_axis_idempotent_in_the_family_cartan_subalgebra"] is True
    assert theorem["the_paper_real_family_operator_is_the_same_idempotent_with_a_weaker_exact_scalar"] is True
    assert theorem["the_promoted_neutrino_doublet_operator_is_exactly_29I_minus_deltaR_and_so_lives_in_the_same_cartan_subalgebra"] is True
    assert theorem["all_current_real_family_operators_therefore_live_in_span_I_R_while_triality_phase_structure_lives_in_the_complementary_JK_sector"] is True

    assert operators["live_ckm_family_operator"]["scalar_exact"] == "-1973/4000"
    assert operators["paper_real_family_operator"]["scalar_exact"] == "-559/124320"
