"""TOE75 reproducibility tests for all five independent research fronts."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe75_structural import disorder,spectral_minmax,quantum_orbits,squared_graph_dirac
from w33_20261014_toe75_continuous_interacting import certificate as interacting

def test_exact_global_160_link_disorder_bracket_and_realizable_witness():
    c=disorder()
    assert c["status"]=="PASS_TOE75_RATIONAL_ALL_EDGES_LOWER_AND_REALIZABLE_UPPER"
    assert c["entire_amplitude_box_edges"]==160
    assert c["verified_global_unique_three_pi_free_energy_at_epsilon"]=="1/7"
    assert len(c["realizable_17_edge_witness_indices"])==17
    assert int(c["exact_witness_negative_numerator"])<0
    assert int(c["exact_witness_positive_numerator"])>0
    assert "Does not prove" in c["scope"]

def test_unbounded_rotor_two_ordered_levels_variational_no_gap_claim():
    c=spectral_minmax()
    assert c["status"]=="PASS_TOE75_UNCONDITIONAL_ORDERED_SECOND_EIGENVALUE_UPPER"
    assert c["finite_P_dimension"]==22638
    assert c["off_diagonal_direct_coupling_exactly_zero"]
    assert c["spectral_gap_certified"] is False

def test_exact_20_extra_cover_neighbor_full_group_membership():
    c=quantum_orbits()
    assert c["status"]=="PASS_TOE75_20_NEIGHBOR_FULL_ORBIT_MEMBERSHIP"
    assert c["candidate_distinct_neighbors_outside_seven_SEEDS"]==20
    assert len(c["seven_legacy_full_group_orbit_sizes"])==7
    assert c["seven_legacy_full_group_orbit_sizes"]==[51840]*7
    assert c["candidate_neighbors_outside_all_seven_orbits"]>=0
    assert c["not_yet_classified_candidate_remainder"]>=0

def test_actual_squared_native_graph_sparse_cell_complex():
    c=squared_graph_dirac()
    assert c["status"]=="PASS_TOE75_NATIVE_LEVI_SQUARED_LOCAL_CELLULAR_DIRAC"
    assert c["product_cells_by_dimension"]==[6400,25600,25600]
    assert c["exact_d1_d0_nonzero_entries"]==0
    assert c["product_Z_betti_numbers"]==[1,162,6561]
    assert c["Euler_Dirac_index"]==6400
    assert c["closed_W33_squared_4D_surface_spin_Dirac_index"]==0
    assert "ONLY a 2D" in c["obstruction"]

def test_continuous_interacting_static_U1_local_minima_and_finite_temp():
    c=interacting()
    assert c["status"]=="PASS_TOE75_CONTINUOUS_INTERACTING_U1_FINITE_T_CONTROLS"
    assert c["full_fixed_N_manybody_dimension"]==462
    assert len(c["interaction_scans"])==4
    assert c["theta_graph_three_nontrivial_Z2_sectors_exactly_isospectral"]
    assert all(len(r["beta_resolved_2D_local_best_minus_Z2_free_energy_advantage"])==4 for r in c["interaction_scans"])
    for r in c["interaction_scans"]:
        assert len(r["two_dimensional_multistart_runs"])==4
        assert len(r["beta_resolved_boundary_optimized_minus_Z2_free_energy_advantage"])==4
        assert r["best_local_two_dimensional_energy"]<=r["one_dimensional_continuous_min_energy"]+1e-7

from w33_20261014_toe75_exact_120_flux import certificate as theta120

def test_exact_native_theta_all_torus_free_120_degree_global_minimum():
    c=theta120()
    assert c["status"]=="PASS_TOE75_EXACT_GLOBAL_120_DEGREE_FLUX"
    assert c["single_particle_bipartition"]==[5,6]
    assert c["global_minimum_phase_pairs_pi_units"]==[[2/3,4/3],[4/3,2/3]]
    assert len(c["eight_direct_manybody_spectral_cross_checks"])==8
    assert 0.02069<c["global_120_advantage_below_best_Z2"]<0.02070
    assert "ONLY" in c["scope"]

from w33_20261014_toe75_cover_orbit_expansion import certificate as expanded_orbits

def test_all_twenty_extra_ground_cover_candidates_full_group_orbits():
    c=expanded_orbits()
    assert c["status"]=="PASS_TOE75_COMPLETE_ORBIT_CLASSIFICATION_OF_20_NEW_NEIGHBORS"
    assert c["number_of_new_candidates"]==20
    assert c["unclassified_candidates_from_initial_20"]==0
    assert c["proved_total_distinct_cover_orbits_at_least"]>=8
    assert c["proved_total_distinct_20_cycle_cover_states_at_least"]>=414720
