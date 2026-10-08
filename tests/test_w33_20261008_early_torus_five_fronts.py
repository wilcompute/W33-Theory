"""Regression for early-March torus recovery and October C5/F20 continuation."""
import json,sys,math
from pathlib import Path
from scipy.stats import binom
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
import w33_20261008_early_torus_singer_quotient as singer
import w33_20261008_F20_torus_mod3_equivariance as f20
import w33_20261008_torus_Z3_lattice_gauge as gauge
import w33_20261008_photon_binomial_launch_cert as launch
import w33_20261008_tetraquadric_free_Bertini_existence as bertini
D=R/"data"
def saved(name):return json.loads((D/name).read_text())

def test_singer_five_sheet_quotient_and_topology():
 x=saved("w33_20261008_early_torus_singer_quotient.json")
 assert x["singer_C5_free_cell_action"]
 assert x["original_CW_cells"]==[40,60,20]
 assert x["C5_quotient_cells"]==[8,12,4]
 assert x["C5_quotient_euler"]==0
 assert x["quotient_smith_d1"]==[1]*7
 assert x["quotient_smith_d2"]==[1]*3
 assert x["quotient_integral_betti"]==[1,2,1]
 assert x["quotient_pi1_post_elimination_generators"]==2
 assert x["quotient_pi1_post_elimination_relators"]==[[5,-3,-5,3]]
 assert x["quotient_tietze_eliminations"]==3

def test_singer_quotient_not_cube_but_C8_with_alternating_parallel_matching():
 x=saved("w33_20261008_early_torus_singer_quotient.json")
 assert not x["C5_quotient_1_skeleton_is_three_cube_Q3"]
 assert x["C5_quotient_simple_underlying_graph_is_C8"]
 assert x["C5_quotient_double_edges_form_perfect_matching_on_C8"]
 assert x["C5_quotient_simple_graph_edges"]==8
 assert x["C5_quotient_parallel_edge_multiplicity_histogram"]=={"1":4,"2":4}
 assert all(len(set(f))==8 for f in x["C5_quotient_C8_face_vertex_walks"])
 assert x["C5_quotient_octagon_edge_face_multiplicities"]=={"4":8}
 assert x["quotient_is_Csaszar_or_Szilassi"] is False

def test_F20_c1_vs_c2_invariant_mod3_cohomology_firewall():
 x=f20.compute()
 assert x["C5"]["dim_H1_F3_invariant_under_group"]==2
 assert x["F20"]["dim_H1_F3_invariant_under_group"]==0
 assert x["F20"]["vertex_orbit_sizes"]==[20,20]
 assert x["F20"]["edge_orbit_sizes"]==[20,20,20]
 # Corrects previous prose guessing 10+10: actual three orbits 5,5,10
 assert x["F20"]["face_orbit_sizes"]==[5,5,10]
 assert x["H2_Z_orientation_character_element_histogram"]=={1:20}
 assert x["F20_invariant_H2_F3_dimension"]==1
 assert x["F20_H1_no_order_three_character_if_zero"]

def test_Z3_gauge_complex_and_topological_flux():
 x=gauge.compute()
 assert x["CW_vertices_edges_faces"]==[40,60,20]
 assert x["gauge_effective_rank"]==39
 assert x["face_curvature_coboundary_rank_mod3"]==19
 assert x["flat_link_cochain_kernel_dim"]==41
 assert x["flat_connection_gauge_equivalence_sector_dimension"]==2
 assert x["flat_Z3_gauge_classes"]==9
 assert x["H2_nonexact_flux_classes"]==3
 assert x["exact_curvature_code_parameters_F3"]==[20,19,2]
 assert x["nonzero_exact_curvature_minimum_classical_action"]==3
 assert x["F20_invariant_flat_Z3_characters"]==1
 assert sum(v!=0 for v in x["example_two_plaquette_exact_flux"])==2
 assert sum(v!=0 for v in x["example_nonexact_unit_face_flux"])==1

def test_binomial_photon_true_joint_confidence():
 x=launch.build()
 assert x["winners"]["dark0_eps0"]=={"stages":72,"minimum_95pct_joint_launch_budget":2538,"required_successful_detections":1182}
 assert x["winners"]["dark0.05_eps0.01"]["minimum_95pct_joint_launch_budget"]==3396
 assert x["winners"]["dark0.1_eps0.02"]["minimum_95pct_joint_launch_budget"]==4780
 assert x["winners"]["dark0.2_eps0.05"]["minimum_95pct_joint_launch_budget"]==18933
 for row in x["rows"]:
  N=row["exact_minimal_launches_for_collection_probability_at_least_0.975"]
  n=row["successful_detections_for_conditional_error_at_most_0.025"]
  p=row["per_launch_success_probability"]
  assert binom.sf(n-1,N,p)>=.975
  assert binom.sf(n-1,N-1,p)<.975
 assert x["not_physically_calibrated"] is True

def test_Klein_four_21_basis_basepoint_free_algebraic_case_split():
 x=bertini.build()
 assert x["invariant_basis_dim"]==21
 assert x["invariant_basis_by_number_of_linear_xiyi_factors"]=={"0":8,"2":12,"4":1}
 assert x["boundary_support_patterns_verified"]==80
 assert x["interior_potential_base_locus_sign_patterns_dispatched"]==8
 for c in x["explicit_interior_two_ones_section_witnesses"]:
  a,b=c["remaining_quadratic_indices"]
  assert c["t_signs"][a]*c["t_signs"][b]==1
  assert len(c["nonvanishing_two_ones_section_positions"])==2
 assert x["invariant_linear_system_basepoint_free_over_C"] is True
 assert x["generic_invariant_member_avoids_all_48_fixed_points"] is True
 assert x["generic_Klein_four_free_smooth_tetraquadric_exists"] is True
 assert not x["explicit_previous_integer_coefficient_polynomial_smoothness_proven"]

def test_prior_march_torus_may_csaszar_not_reidentified():
 x=saved("w33_20261008_early_torus_singer_quotient.json")
 assert "2026-03-09" in x["context"]["earliest_external_torus_refinement_commit"]
 assert "2026-05-18" in x["context"]["Csaszar_Szilassi_edge_parser"]
 assert not x["quotient_is_Csaszar_or_Szilassi"]
