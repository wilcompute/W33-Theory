import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]

SCRIPTS=[
    "w33_20260924_history_bigcell_q43_compactification.py",
    "w33_20260924_history_cycle81_character_bridge.py",
    "w33_20260924_history_h27_35_46_decomposition.py",
    "w33_20260924_temporal_maslov_mu12.py",
    "w33_20260924_spectral_clock_fixed9_group_probe.py",
    "w33_20260924_fixed9_chiral_null_fourplusfour.py",
    "w33_20260924_history_pointline_cospectral_firewall.py",
    "w33_20260924_history_invariant_cycle_orientation.py",
    "w33_20260924_null_history_spectral_clock.py",
    "w33_20260924_temporal_universal_cover.py",
    "w33_20260924_history_to_global_h1_intertwiner.py",
    "w33_20260924_relative_levi_35_46_split.py",
    "w33_20260924_hermitian_3p1_spread_bridge.py",
    "w33_20260924_temporal_hesse_4a2_a8_bridge.py",
    "w33_20260924_null_hesse_4a2_s4_intertwiner.py",
    "w33_20260924_page_wootters_diagonal_weld.py",
    "w33_20260924_positive_null_counter_cover.py",
    "w33_20260924_four_a2_history_quotient.py",
    "w33_20260924_temporal_a8_e8_process_bracket.py",
    "w33_20260924_temporal_su9_e8_compiler.py",
]


@pytest.mark.parametrize("name",SCRIPTS)
def test_producers_replay(name):
    subprocess.run(
        [sys.executable,str(ROOT/"analysis"/name)],
        cwd=ROOT,check=True,capture_output=True,text=True,timeout=45,
    )


def load(name):
    return json.loads((ROOT/"data"/name).read_text(encoding="utf-8"))
def test_big_cell_is_q43_and_spectrum_is_exact():
    x=load("w33_20260924_history_bigcell_q43_compactification.json")
    assert x["status"]=="PASS_27_HISTORY_BIG_CELL_COMPACTS_TO_Q43_LINE_CARRIER"
    assert x["lagrangian_grassmannian"]["big_cell_disjoint_from_bell"]==27
    assert x["lagrangian_grassmannian"]["boundary_meeting_bell"]==13
    assert x["null_history_graph"]["cycle_rank"]==82
    assert x["null_history_graph"]["adjacency_spectrum"]=={
        "-4":6,"-1":8,"2":12,"8":1
    }
    assert x["null_history_graph"]["laplacian_spectrum"]=={
        "0":1,"6":12,"9":8,"12":6
    }


def test_reduced_history_cycles_are_global_h1_characterwise():
    x=load("w33_20260924_history_cycle81_character_bridge.json")
    assert x["status"]=="PASS_CHARACTER_AUDIT"
    assert x["history_null_graph"]["cycle_space_dimension"]==82
    assert x["history_null_graph"]["trivial_multiplicity"]==1
    assert x["history_null_graph"]["reduced_dimension"]==81
    assert x["comparison"]["characters_identical"] is True
    assert x["comparison"]["character_equal_elements"]==648
def test_temporal_35_plus_46_and_point_line_firewall():
    x=load("w33_20260924_history_h27_35_46_decomposition.json")
    assert x["status"]=="PASS_HISTORY_35_46_SPLIT_WITH_POINT_LINE_FIREWALL"
    assert x["history_graph"]["triangles"]==36
    assert x["history_graph"]["filled_clique_b1"]==46
    assert x["H27_firewall"]["isomorphic_to_history_null_graph"] is False
    assert x["bell_stabilizer_character_split"]["identity"]=="81=(36-1)+46=35+46"

    y=load("w33_20260924_history_pointline_cospectral_firewall.json")
    assert y["separator"]["complete_induced_four_vertex_profiles_equal"] is True
    assert y["separator"]["independent_triad_common_neighbor_hist_history"]=={
        "0":405,"1":216,"2":324
    }
    assert y["separator"]["independent_triad_common_neighbor_hist_point_H27"]=={
        "0":225,"1":648,"3":72
    }


def test_weil_mu12_and_fixed_clock_chirality():
    x=load("w33_20260924_temporal_maslov_mu12.json")
    assert x["status"]=="PASS_HISTORY_QUADRATICS_GENERATE_THE_CLIFFORD_MU12_FIELD"
    assert x["quadratic_history_atlas"]["phase_exponent_histogram_mu12"]=={
        "0":13,"3":4,"6":6,"9":4
    }
    q=load("w33_20260924_spectral_clock_fixed9_group_probe.json")
    assert q["clock"]["phase_dimensions"]=={"1":9,"omega":12,"omega2":6}
    assert q["bell_stabilizer_action"]["fixed9_action_kernel_order"]==1
    assert q["bell_stabilizer_action"]["fixed9_action_image_order"]==648
    assert q["projective_qutrit_clifford_test"]["image_order_matches_216"] is False

    y=load("w33_20260924_fixed9_chiral_null_fourplusfour.json")
    assert y["status"]=="PASS_FIXED9_IS_VACUUM_PLUS_TWO_ORIENTED_NULL_FOURS"
    assert y["PSp_order648"]["orbit_sizes"]==[4,4]
    assert y["PSp_order648"]["orbit_weil_phases"]==[["-i"],["i"]]
    assert y["PGSp_order1296"]["orbit_sizes"]==[8]


def test_explicit_orientation_cycle_is_outer_odd():
    x=load("w33_20260924_history_invariant_cycle_orientation.json")
    assert x["status"]=="PASS_EXPLICIT_UNIQUE_HISTORY_ORIENTATION_CYCLE"
    assert x["invariant_cycle"]["support_size"]==108
    assert x["invariant_cycle"]["vertex_boundary_zero"] is True
    assert x["PGSp_outer_action"]["inner_half_preserves_orientation"] is True
    assert x["PGSp_outer_action"]["outer_coset_flips_orientation"] is True
    assert x["PGSp_outer_action"]["sign_histogram"]=={"-1":648,"1":648}


def test_universal_cover_is_unbounded_history():
    x=load("w33_20260924_temporal_universal_cover.json")
    assert x["status"]=="PASS_NULL_HISTORY_UNIVERSAL_COVER_UNBOUNDED_PATH_TIME"
    assert x["fundamental_group"]["rank"]==82
    assert x["base_graph"]["integral_first_homology"]=="Z^82"
    assert x["universal_cover"]["graph"]=="infinite 8-regular tree"


def test_explicit_history46_injects_into_global_h1():
    x=load("w33_20260924_history_to_global_h1_intertwiner.json")
    assert x["status"]=="PASS_EXPLICIT_TEMPORAL_CYCLES_TO_GLOBAL_W33_H1_INTERTWINER"
    assert x["construction"]["Bell_stabilizer_equivariant_all_648"] is True
    assert x["homology"]["filled_history_H1_dimension"]==46
    assert x["homology"]["kernel_is_exactly_history_triangle_boundary_space"] is True
    for row in x["homology"]["induced_rank_mod_primes"].values():
        assert row["induced_history_rank"]==46
        assert row["triangle_image_extra_rank"]==0


def test_relative_levi_sector_is_the_reduced_triangle35():
    x=load("w33_20260924_relative_levi_35_46_split.json")
    assert x["status"]=="PASS_GLOBAL_H1_SPLITS_AS_HISTORY46_PLUS_BELL_BOUNDARY35"
    assert x["topology"]["full_W33_Levi"]["b1"]==81
    assert x["topology"]["temporal_core_Levi"]["b1"]==46
    assert x["topology"]["boundary_extension"]["relative_b1"]==35
    assert x["representation"]["relative35_equals_reduced_signed_triangle35_all_elements"] is True
    assert x["representation"]["elements_checked"]==648


def test_null_clock_fixed9_is_not_projective_qutrit_clifford():
    x=load("w33_20260924_null_history_spectral_clock.json")
    assert x["status"]=="PASS_ORDER3_NULL_HISTORY_CLOCK_WITH_QUTRIT_MODULE_NOGO"
    assert x["clock"]["fixed_dimension"]==9
    assert x["qutrit_operator_intertwiner_test"]["equivariant_identification_under_these_actions"] is False


def test_hermitian_3p1_nulls_are_exactly_w33_spreads():
    x=load("w33_20260924_hermitian_3p1_spread_bridge.json")
    assert x["status"]=="PASS_HERMITIAN_3P1_ELLIPTIC_SECTION_SPREAD_WITH_J_NOGO"
    assert x["hermitian_space"]["affine_norm_counts"]=={"0":21,"1":30,"2":30}
    assert x["hermitian_space"]["projective_norm_counts"]=={"0":10,"1":15,"2":15}
    assert x["q43_embedding"]["hyperplane_section_census"]=={
        "elliptic_10":36,"tangent_13":40,"hyperbolic_16":45
    }
    assert x["spread_bridge"]["section_spreads_equal_all_W33_spreads"] is True
    assert x["complex_structure_nogo"]["candidate_space_size"]==729
    assert x["complex_structure_nogo"]["solutions"]==0


def test_hesse_12_plus_72_refines_e8_as_4a2():
    x=load("w33_20260924_temporal_hesse_4a2_a8_bridge.json")
    assert x["status"]=="PASS_HESSE_12_IS_4A2_INSIDE_TEMPORAL_A8_E8"
    assert x["history_plane"]["AGL_orbits"]=={
        "Hesse_lines":12,"noncollinear_triangles":72
    }
    assert x["Hesse_4A2"]["root_count"]==24
    assert x["Hesse_4A2"]["rank"]==8
    assert x["Hesse_4A2"]["components"]==4
    assert x["Hesse_4A2"]["reflection_closed"] is True
    assert x["root_partition"]["identity"]=="240 = 72 + 24 + 144"


def test_null_hesse_and_4a2_share_the_same_s4_carrier():
    x=load("w33_20260924_null_hesse_4a2_s4_intertwiner.json")
    assert x["status"]=="PASS_NULL_DIRECTIONS_HESSE_STRIATIONS_4A2_SHARE_EXACT_S4"
    assert x["carrier"]["size"]==4
    assert x["action"]["image_order"]==24
    assert x["action"]["permutations_identical_objectwise"] is True
    assert x["action"]["temporal_line_parabolic"]["kernel_order_on_P1"]==27
    assert x["action"]["Hesse_AGL23"]["kernel_order_on_P1"]==18


def test_page_wootters_phase_matching_is_the_diagonal_weld():
    x=load("w33_20260924_page_wootters_diagonal_weld.json")
    assert x["status"]=="PASS_PAGE_WOOTTERS_PHASE_MATCHING_IS_THE_DIAGONAL_E8_WELD"
    assert x["page_wootters"]["forward_equals_plus_zero_set"] is True
    assert x["page_wootters"]["reverse_equals_minus_zero_set"] is True
    assert x["page_wootters"]["invariant_dimension_each"]==3
    assert x["existing_E8_switch_reinterpreted"]["all_16_entries_match_rule"] is True
    assert x["existing_E8_switch_reinterpreted"]["pure_axis_pair_dimension"]==24
    assert x["existing_E8_switch_reinterpreted"]["any_correlated_graph_side_dimension"]==248


def test_positive_null_counters_quotient_to_27_histories():
    x=load("w33_20260924_positive_null_counter_cover.json")
    assert x["status"]=="PASS_27_HISTORIES_ARE_FOUR_NULL_COUNTERS_MOD_COMMON_WINDING"
    assert x["finite_quotient"]["rank"]==3
    assert x["finite_quotient"]["image_size"]==27
    assert x["finite_quotient"]["kernel_description"]=="span_F3{(1,1,1,1)}"
    assert x["integer_cover"]["fundamental_winding_matrix"]==[[3,0],[0,3]]
    assert x["integer_cover"]["positive_loop_upstairs"] is False


def test_four_a2_components_quotient_equivariantly_to_history27():
    x=load("w33_20260924_four_a2_history_quotient.json")
    assert x["status"]=="PASS_HISTORY_27_IS_RELATIVE_MODE_OF_FOUR_HESSE_A2_COMPONENTS"
    assert x["linear_map"]["rank"]==3
    assert x["linear_map"]["image_size"]==27
    assert x["linear_map"]["kernel"]=="span{(1,1,1,1)}"
    assert x["representation"]["order"]==24
    assert x["representation"]["all_24_elements_verified"] is True


def test_temporal_a8_e8_process_bracket_counts():
    x=load("w33_20260924_temporal_a8_e8_process_bracket.json")
    assert x["status"]=="PASS_NINE_HISTORY_CELLS_COMPILE_THE_A8_E8_ROOT_SUPPORT_BRACKETS"
    assert x["basis"]["root_total"]==240
    assert x["exact_counts"]["sl9_Lambda3_nonzero"]==1512
    assert x["exact_counts"]["Lambda3_Lambda3_nonzero_unordered_pairs"]==840
    assert x["exact_counts"]["Lambda3_Lambda6_root_contractions"]==1512
    assert x["exact_counts"]["Lambda3_Lambda6_opposite_Cartan_pairs"]==84
    assert x["Hesse_process"]["same_parallel_class_nonzero_pairs"]==12
    assert x["Hesse_process"]["different_direction_zero_pairs"]==54


def test_nine_history_compiler_reaches_w33_sl9_and_e8_support():
    x=load("w33_20260924_temporal_su9_e8_compiler.json")
    assert x["status"]=="PASS_NINE_QUTRIT_HISTORY_AMPLITUDES_COMPILE_W33_SL9_AND_E8_SUPPORT"
    assert x["two_sided_Weyl"]["operators"]==81
    assert x["two_sided_Weyl"]["nonidentity_traceless"]==80
    assert x["two_sided_Weyl"]["nonidentity_span_rank"]==80
    assert x["two_sided_Weyl"]["same_space_as_standard_sl9_basis"] is True
    assert x["W33_projectivization"]["projective_inverse_pairs"]==40
    assert x["W33_projectivization"]["srg_parameters"]==[40,12,2,4]
    assert x["E8_A8_completion"]["identity"]=="248=80+84+84"
