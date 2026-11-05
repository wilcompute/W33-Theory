"""Regenerate November 5 five-front TOE falsifiers + Petersen control.

Independent relative to JSON certificates: import each producer and run
its numerical checks, then validate cross-report invariants. Does not
claim TOE or real hardware. Quantum memory and detector loopholes remain
trusted-instrument dependent; Lorentzian principal-branch failure is
a NEGATIVE result.
"""
import importlib.util,sys,collections,math
from pathlib import Path
import numpy as np,pytest
ROOT=Path(__file__).resolve().parents[1]
for x in (ROOT,ROOT/"analysis"):
 if str(x) not in sys.path:sys.path.insert(0,str(x))
def run(name):
 p=ROOT/"analysis"/(name+".py")
 spec=importlib.util.spec_from_file_location(name,p)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 return m.main()
@pytest.fixture(scope="module")
def a5():return run("toe_20261105_a5_tetrad_orbits_bhattacharyya")
@pytest.fixture(scope="module")
def petersen():return run("toe_20261105_petersen_tetrad_duad_spread_certificate")
@pytest.fixture(scope="module")
def gauge():return run("toe_20261105_two_connected_c4_gauge_matter_gauss")
@pytest.fixture(scope="module")
def decoder():return run("toe_20261105_readout_decoder_error_exponents_hardware_guard")
@pytest.fixture(scope="module")
def memory():return run("toe_20261105_quantum_memory_interventions_and_dimension_bound")
@pytest.fixture(scope="module")
def regge():return run("toe_20261105_nine_simplex_regge_action_hessian_lorentz_diagnostic")

def test_actual_native_a5_orbits_partition_40_tetrads(a5):
 assert a5["native_A5_order"]==60
 assert a5["A5_tetrad_orbit_sizes"]==[10,30]
 assert len(a5["bad_basis_indices"])==10
 assert len(a5["good_basis_indices"])==30
 assert sorted(a5["bad_basis_indices"]+a5["good_basis_indices"])==list(range(40))

def test_two_bad_basis_settings_15_complete_30_partial(a5):
 r=collections.Counter(x["distinct_440root_probability_classes"] for x in a5["two_bad_tetrad_pair_classification"])
 assert r=={440:15,249:30}
 assert a5["two_distinct_bad_tetrad_pairs_checked"]==45
 assert a5["native_10_collision_tetrads_all_exponent_zero"]

def test_full_40_witting_worstpair_beats_su4_mutual_information_best(a5):
 x=a5["full_Witting40_POVM_closest_pair_Bhattacharyya"]["worst_pair_Bhattacharyya_error_exponent"]
 y=a5["optimized_single_4outcome_basis_closest_pair_Bhattacharyya"]["worst_pair_Bhattacharyya_error_exponent"]
 assert x>0.0008
 assert 0<y<0.000003
 assert x/y>300

def test_petersen_duads_and_spread_are_native_equivariant(petersen):
 assert petersen["bad_contexts_form_ray_partition_of_40_points"]
 assert petersen["Witting_line_spread_size"]==10
 assert petersen["decoder_graph_is_petersen_KG_5_2"]
 assert petersen["decoder_graph_regular_degree"]==3
 assert petersen["decoder_graph_girth"]==5
 assert petersen["decoder_full_identifiability_pair_graph_edges"]==15
 assert petersen["native_A5_tetrad_action_equals_even_permutations_on_five_duad_slots"]
 assert petersen["native_A5_five_slot_permutation_count"]==60
 assert len(petersen["duad_labels_for_bad_tetrad"])==10

def test_decoder_440_uniform_root_label_maxerror_union_certificate(decoder):
 assert decoder["labels"]==440
 assert decoder["exact_prior_Fano_necessary_detected_photon_lower_bound_at_epsilon_point_one"]==694
 w=decoder["decoder_models"]["Witting_40"]
 u=decoder["decoder_models"]["optimized_4outcome_basis"]
 assert w["exact_union_bound_sufficient_detected_photons_for_max_5pct_ML_error"]==11238
 assert u["exact_union_bound_sufficient_detected_photons_for_max_5pct_ML_error"]==4093456
 assert w["exact_union_bound_sufficient_detected_photons_for_max_5pct_ML_error"]<u["exact_union_bound_sufficient_detected_photons_for_max_5pct_ML_error"]
 assert w["exact_union_bound_sufficient_incident_photons_eta085"]>11238
 assert w["sufficient_detected_photons_with_background"]>11238

def test_adversarial_givens_six_gate_TV_bound(decoder):
 assert abs(decoder["ideal_full_Witting_min_pair_TV"]-.0306071208)<2e-8
 delta=decoder["sufficient_max_per_gate_absolute_phase_and_mixing_error_radians_for_nonoverlap"]
 assert 0.0016<delta<0.0018
 scans=decoder["static_calibration_bound_scan"]
 assert scans[0]["worst_pair_codeword_separation_certified_by_this_bound"]
 assert not scans[-1]["worst_pair_codeword_separation_certified_by_this_bound"]

def test_gauge_connected_2C4_one_charge_projected_dimension(gauge):
 assert gauge["vertex_count"]==8 and gauge["edge_count"]==9
 assert gauge["raw_hilbert_dimension"]==4096
 assert gauge["one_particle_background_neutral_gauss_subspace_dimension"]==32
 assert gauge["Gauss_orbit_size"]==128
 assert gauge["all_dressed_hopping_and_flux_and_electric_terms_preserve_physical_sector"]
 assert gauge["bare_hopping_across_link_breaks_local_Gauss_law"]

def test_connected_gauge_flux_sector_energies(gauge):
 e=gauge["two_flux_sector_hopping_spectra"]
 assert len(e)==4
 assert e["1,1"]["ground_kinetic_energy"]<e["1,-1"]["ground_kinetic_energy"]<e["-1,-1"]["ground_kinetic_energy"]
 assert abs(e["1,-1"]["ground_kinetic_energy"]+math.sqrt(5))<1e-10
 assert abs(e["-1,-1"]["ground_kinetic_energy"]+2)<1e-10
 assert gauge["connected_120_loop_scaffold_cycle_rank"]==120
 assert int(gauge["one_charge_physical_hilbert_dimension_for_120_loops_decimal"])==480*(1<<120)
 assert gauge["full_E8_root_graph_and_interlayer_links_not_implemented"]

def test_trusted_quantum_memory_7_interventions_and_dephased_classical_controls(memory):
 assert len(memory["middle_instruments"])==7
 for t in memory["middle_instruments"]:
  assert abs(t["quantum_memory_recovered_singlet_fraction"]-1)<1e-10
  assert abs(t["dephased_classical_memory_singlet_fraction"]-1/3)<1e-10
 assert memory["arbitrary_classical_memory_dephasing_Haar_bases"]==32
 assert abs(memory["recovered_fidelity_classical_E_any_test_basis_max"]-1/3)<1e-10

def test_minimum_quantum_memory_schmidt_dimension(memory):
 assert [x["Schmidt_rank_m"] for x in memory["Schmidt_number_m_singlet_fraction_upper_bounds"]]==[1,2,3]
 assert np.allclose([x["max_singlet_fidelity_m_over_three"] for x in memory["Schmidt_number_m_singlet_fraction_upper_bounds"]],[1/3,2/3,1])
 assert memory["trusted_perfect_identity_recovery_requires_quantum_bottleneck_dimension_at_least3"]
 assert memory["p_equal_point6_eta085_Binomial_exact_rule"]["n"]>0

def test_boundary_complete_euclidean_9_simplex_Regge_action(regge):
 assert regge["four_simplices"]==9 and regge["interior_vertices"]==2
 assert regge["interior_hinges"]==20 and regge["boundary_hinges"]==10
 assert regge["interior_squared_edge_variables"]==10
 assert abs(regge["Euclidean_boundary_complete_S_flat"]-regge["Euclidean_S_flat_known_outer_value"])<1e-9
 assert regge["Euclidean_flat_internal_vertex_Jacobian_rank"]==8

def test_eight_flat_hessian_near_nulls_two_curvature_normals(regge):
 eig=np.sort(np.abs(np.array(regge["Euclidean_flat_Hessian_eigenvalues"])))
 assert max(eig[:8])<.001
 assert min(eig[8:])>40
 assert regge["Euclidean_flat_Hessian_times_J_norm"]<.01
 for x in regge["off_flat_normal_curvature_and_Hessian"]:
  assert x["Schlafli_FD_gradient_residual"]<1e-5
 assert regge["off_flat_normal_curvature_and_Hessian"][-1]["maximum_hinge_deficit"]>.01

def test_complex_lorentz_branch_fail_control_not_claimed_GR(regge):
 assert regge["Lorentzian_principal_branch_relative_flat_action_gradient_norm"]>1
 assert not regge["Lorentzian_action_physically_verified"]
 assert not regge["ADM_Hamiltonian_momentum_constraint_closure_derived"]
