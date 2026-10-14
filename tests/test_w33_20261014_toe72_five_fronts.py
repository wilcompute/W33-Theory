"""TOE72: five source-regenerating finite mathematical/physics front tests."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe72_hessian_multiray import certificate as disorder
from w33_20261014_toe72_gauge_gram_bound import certificate as gauge
from w33_20261014_toe72_cover_orbit_escape import certificate as pairing
from w33_20261014_toe72_w33_squared_index import certificate as topology
from w33_20261014_toe72_exact_interacting_octagon import certificate as interacting

def test_native_hessian_eigen_axis_and_six_global_numerical_MILPs():
    c=disorder()
    assert c["status"]=="PASS_TOE72_FULL_HESSIAN_AND_MULTIRAY_MILP_PROBES"
    assert c["exact_antisymmetric_rayleigh_coefficients"]==[0,0,72,46,34,0,0,0,-12]
    assert len(c["six_independent_full_160_edge_MILP_directions"])==6
    assert all(float(z["floating_minimum"])>0 for z in
        c["six_independent_full_160_edge_MILP_directions"])
    assert float(c["fixed_adversary_rational_epsilon_matrices"][-1]["smallest_numeric_eigenvalue"])<0
    assert "NOT" in c["scope"]

def test_rigorous_integer_two_loop_Gram_and_Q_row_bound():
    c=gauge()
    assert c["status"]=="PASS_TOE72_INTEGER_INTERFACE_AND_GERSHGORIN"
    assert c["Q_omitted_diagonal_minus_allowed_rowsum_min_exact_units_2000"]==28330
    assert c["exact_KKT_max_abs_row_sum_integer"]==12822
    assert abs(c["rigorous_K_norm_squared_upper"]-2.0034375)<1e-14
    assert abs(c["rigorous_Q_spectral_lower"]-14.165)<1e-14
    assert .922<c["conditional_full_rotor_gap_lower"]<.924
    assert "conditional" in c["mathematical_scope"].lower()

def test_seven_distinct_full_group_ground_cover_orbits():
    c=pairing()
    assert c["status"]=="PASS_TOE72_SEVEN_DISTINCT_COVER_ORBITS"
    assert c["number_of_proved_distinct_full_PGSp_orbits"]==7
    assert c["number_of_proved_ground_cover_states_lower"]==362880
    assert c["second_order_links_remaining_inside_initial_orbit"]==0
    assert c["second_order_links_leaving_initial_orbit_per_state"]==6
    assert len(c["neighbor_orbit_classification"])==6
    assert all(not z["intersects_original_orbit"] for z in
        c["neighbor_orbit_classification"])

def test_w33_squared_closed_spin_4d_with_graph_lagrangian_index_obstruction():
    c=topology()
    assert c["status"]=="PASS_TOE72_W33_TIMES_W33_LAGRANGIAN_INDEX_NO_GO"
    assert c["external_torus_required"] is False
    assert c["betti_integral_torsion_free"]==[1,324,26246,324,1]
    assert c["euler_characteristic"]==25600
    assert c["graph_inherited_mixed_H2_subspace_rank"]==6561
    assert c["all_graph_inherited_mixed_c1_classes_have_index_zero"]
    assert c["non_native_dual_meridian_twisted_spin_Dirac_index"]==1

def test_exact_native_octagon_N4_ED_vs_full_exchange_HF():
    c=interacting()
    assert c["status"]=="PASS_TOE72_EXACT_NATIVE_INTERACTION_VS_HF"
    assert c["native_octagon_id"]==111
    assert c["fixed_particle_many_body_dimension"]==70
    assert len(c["runs"])==6
    assert all(abs(z["exact_staggered_mean"])<1e-9 for z in c["runs"])
    assert all(z["many_body_ground_energy"]<=z["HF_variational_energy"] for z in c["runs"])
    assert c["runs"][-1]["exact_fixed_N_first_gap"]<.13
    assert c["runs"][-1]["HF_one_particle_hole_gap"]>15
