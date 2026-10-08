"""Oct 8 independent Z2 physical followthrough and exact CSS/cocycle controls."""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_twenty_apartment_binary_CSS_F20 as css
import w33_20261008_twenty_apartment_X_cosystole as milp
import w33_20261008_binary_CSS_exhaustive_distance as exact
import w33_20261008_twenty_apartment_logical_SWAP as swap
import w33_20261008_twenty_apartment_exact_gauge_partition as gauge
import w33_20261008_F20_binary_proton_hexality_no_go as proton
import w33_20261008_photonic_coherent_fabrication_guard as photon
def j(file):return json.loads((ROOT/"data"/file).read_text())

def test_binary_code_chain_ranks_and_commutation():
 x=css.analyze()
 assert (x["n"],x["rank_HX"],x["rank_HZ"],x["k"])==(60,39,19,2)
 assert x["all_HX_HZ_commutators_zero"]
 assert x["F20_mod2_H1_representation_image_hist"]=={"(2, 1)":10,"(1, 2)":10}
 assert x["F20_invariant_binary_H1_dimension"]==1
 assert x["nontrivial_Z_shortest_length"]==8

def test_exact_X_distance_frozen_full_mitm():
 x=exact.main()
 assert x["all_X_cocycles_weight_below_six_are_stabilizer_or_zero"]
 assert x["X_weight6_witness_nonzero_logical_pairing"]!=0
 assert x["distance_X_exact"]==6
 assert x["distance_Z_exact"]==8
 assert x["overall_css_distance_exact"]==6

def test_milp_independent_support_and_gap():
 x=j("w33_20261008_twenty_apartment_X_cosystole.json")
 assert x["exact_X_minimum_proven"]
 assert x["minimal_X_weight"]==6
 assert all(row["MILP_status"]==0 and row["MIP_gap"]==0 for row in x["logical_operators"])

def test_permutation_only_logical_swap():
 x=swap.main()
 assert x["logical_SWAP_implemented_by_edge_permutation"]
 assert x["all_vertex_X_and_face_Z_stabilizers_preserved"]
 assert x["F20_logical_action_by_element_order"]=={"1":"identity","2":"identity","4":"SWAP","5":"identity"}
 assert len(x["physical_wire_permutation_witness"]["edge_permutation"])==60
 assert x["physical_wire_permutation_witness"]["logical_X_image"]==[2,1]
 assert x["physical_wire_permutation_witness"]["logical_Z_image"]==[2,1]
 assert x["not_an_entangling_gate"]

def test_exact_wilson_partition_Z2_Z3():
 x=gauge.main()
 assert x["Z2_reduced_state_count"]==4*2**19
 assert x["Z3_reduced_state_count"]==9*3**19
 assert x["Z2_lowest_positive_action"]==4
 assert x["Z3_lowest_positive_action"]==3
 assert x["beta_infinity_GSD_Z2"]==4 and x["beta_infinity_GSD_Z3"]==9
 assert x["finite_CW_no_refinement_or_GR_limit_derived"]
 assert x["Z2_exact_face_weight_enumerator"]["1"]==0
 assert x["Z2_exact_face_weight_enumerator"]["2"]==190
 assert x["Z3_exact_face_weight_enumerator"]["2"]==380

def test_F20_binary_vs_ternary_fixed_classes():
 b=j("w33_20261008_twenty_apartment_binary_CSS_F20.json")
 t=j("w33_20261008_F20_torus_mod3_equivariance.json")
 assert b["F20_invariant_binary_H1_classes"]==[0,3]
 assert t["F20"]["dim_H1_F3_invariant_under_group"]==0
 assert t["F20_invariant_H2_F3_dimension"]==1

def test_single_nonR_Z2_proton_hexality_no_go():
 x=proton.main()
 assert x["all_possible_nonR_Z2_assignments"]==256
 assert x["allowing_all_five_standard_Yukawa_mu_constraints"]==8
 assert x["maximum_dangerous_operators_simultaneously_vetoed_by_these_Z2"]==4
 assert not x["single_nonR_Z2_can_veto_all_5"]
 table={r["operator"]:r for r in x["supplied_P6_charge_operator_table"]}
 assert table["QQQL"]["P6_mod2"]==0
 assert table["UcUcDcEc"]["P6_mod2"]==0
 assert all(table[p]["P6_mod6"]!=0 for p in x["dangerous_operators"])
 assert not x["physical_P6_constructed"]

def test_photonic_coherent_error_guard():
 x=photon.main()
 assert x["selected_scenarios"]["gate0_det0"]=={"stages":72,"launches":2538}
 assert x["selected_scenarios"]["gate0.0001_det0.005"]=={"stages":72,"launches":4098}
 assert x["selected_scenarios"]["gate0.0005_det0.01"]=={"stages":36,"launches":34729}
 assert not x["experimental_realization"]
 assert all(v["separation_lower_bound"]>=0 for v in x["bounded_error_designs"])

def test_research_old_Z2_parity_obstruction_not_overwritten():
 x=j("w33_20261008_F20_binary_proton_hexality_no_go.json")
 assert "Pass10967" in x["UV_prior_art"]
 assert "Pass10974" in x["UV_prior_art"]
 assert "non-R Z2" in x["limitations"]

def test_sparse_explicit_tetraquadric_candidate_not_falsely_certified():
 x=j("w33_20261008_tetraquadric_sparse_good_reduction.json")
 assert x["Z2xZ2_invariant"]
 assert x["all_48_ambient_fixed_points_avoided_over_Q"]
 assert x["fixed_point_audit"]["fixed_points_checked"]==48
 assert set(x["fixed_point_audit"]["nonzero_values"])=={"-1","-16","-32","3","64","80"}
 assert x["nonunit_chart"]["chart_bits"]==[0,0,0,0]
 assert not x["complex_smoothness_proven"]
 assert not x["smooth_free_quotient_constructed"]
