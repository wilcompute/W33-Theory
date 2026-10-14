"""TOE76 six-front independent reproducibility: hopping, gauge, cover,
spin/Dirac, persistent currents, and Ihara/Ramanujan graph-RH bridge."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe76_four_fronts import (
 two_edge_robustness,multiple_eigenlevel_bounds,quotient_27_orbits,spin_index_integrality)
from w33_20261014_toe76_flux_currents import certificate as currents
from w33_20261014_toe76_theta_twisted_ihara import certificate as ihara

def test_all_160_native_pairs_exact_two_link_endpoint_hessians():
    c=two_edge_robustness()
    assert c["status"]=="PASS_TOE76_EXACT_TWO_EDGE_CORNER_CENSUS"
    assert c["unordered_edge_pairs"]==12720
    assert c["integer_corner_Hessian_matrices_checked"]==50880
    assert c["winding_octagons"]==238
    assert c["bad_Hessian_corners"]==951
    assert c["two_edge_non_PSD_corners"]>=0
    assert c["all_two_edge_boxes_PSD"]==(c["two_edge_non_PSD_corners"]==0)
    assert c["bad_single_edge_PSD_endpoints"]>=0
    assert c["single_edge_endpoints_checked"]==320
    assert c["bad_single_edge_endpoint_Hessians"]>=0
    assert c["all_two_edge_boxes_strictly_positive_Hessian"]==(c["bad_Hessian_corners"]==0)

def test_eight_unconditionally_ordered_electric_rotor_variational_uppers():
    c=multiple_eigenlevel_bounds()
    assert c["status"]=="PASS_TOE76_EIGHT_ORDERED_ROTOR_MINMAX_UPPERS"
    assert c["finite_P_dimension"]==22638
    assert c["integer_low_energy_uncoupled_basis_count"]==8
    assert len(c["ordered_eigenvalues_E0_through_E7_upper_bounds_rational"])==8
    assert not c["positive_spectral_gap_proven"]

def test_27_orbit_exact_regular_symmetry_transported_matching_subgraph():
    c=quotient_27_orbits()
    assert c["status"]=="PASS_TOE76_27_ORBIT_SEED_TRANSITION_GRAPH"
    assert c["distinct_orbit_seed_count"]==27
    assert c["every_orbit_seed_connected"]
    assert len(c["seed_graph_adjacency_matrix"])==27
    assert c["compressed_regular_equivariant_matching_edges"]==51840*c["exact_directly_witnessed_seed_graph_edges"]
    assert c["exact_seed_graph_cycle_rank"]==c["exact_directly_witnessed_seed_graph_edges"]-26

def test_integral_spin_index_dual_curvature_and_graph_only_zero():
    c=spin_index_integrality()
    assert c["status"]=="PASS_TOE76_W33_SQUARED_INTEGRAL_SPIN_INDEX_CROSSCHECK"
    assert c["untwisted_index"]==0
    assert c["graph_inherited_only_index_zero"]
    assert len(c["sampled_integer_flux_pairs"])==49
    assert c["mixed_dual_flux_index_formula"]=="index(D_L^+)=-a*b"

def test_interacting_theta_persistent_current_and_hessian_controls():
    c=currents()
    assert c["status"]=="PASS_TOE76_FLUX_CURRENTS_STIFFNESS_AND_GENERIC_CONTROL"
    assert c["S3_arm_relabelings"]==6
    assert len(c["observables"])==4
    for z in c["observables"]:
        assert max(abs(x) for x in z["ground_state"]["numerical_current_grad"])<2e-4
        assert len(z["beta_2"]["Hessian_eigenvalues"])==2
    assert all(x>0 for x in c["observables"][0]["ground_state"]["Hessian_eigenvalues"])

def test_twisted_theta_exact_Ihara_Bass_Hashimoto_and_ramanujan_scope():
    c=ihara()
    assert c["status"]=="PASS_TOE76_NATIVE_THETA_TWISTED_IHARA_RAMANUJAN_BRIDGE"
    assert c["theta_vertices_edges"]==[11,12]
    assert c["primitive_undirected_girth_eight_cycles"]==3
    assert c["zeta_inverse_exact"]=="(1-u^8)*(1+(4-s^2)*u^8+4*u^16)"
    assert c["120_degree_inverse_twisted_zeta"]=="(1-u^8)*(1+2*u^8)^2"
    assert c["tempered_twisted_dipole_condition"]=="s^2<=8; nontrivial roots x=u^8 satisfy |x|=1/2"
    assert len(c["independent_hashimoto_bass_transfer_checks"])==6
    assert all(z["max_independent_24x24_hashimoto_vs_11x11_Bass_vs_3x3_transfer_error"]<2e-8
               for z in c["independent_hashimoto_bass_transfer_checks"])
    assert "IRREGULAR" in c["precise_interpretation"]

from w33_20261014_toe76_levi_ihara_hierarchy import certificate as rh_hierarchy

def test_full_40_80_11_graph_RH_ramanujan_hierarchy_and_320_hashimoto():
    c=rh_hierarchy()
    assert c["status"]=="PASS_TOE76_COMPLETE_GRAPH_RH_THREE_LEVEL_HIERARCHY"
    assert c["native_Levi_graph"]["critical_Ihara_pole_modulus"]=="3^(-1/2)"
    assert c["native_Levi_graph"]["undirected_primitive_octagons"]==1620
    assert c["native_Levi_graph"]["direct_320_by_320_native_nonbacktracking_traces_1_to_8"]["8"]==25920
    assert c["native_theta_patch"]["theta_octagons_as_fraction_of_all_Levi_octagons"]=="1/540"
    assert c["collinearity_graph"]["critical_Ihara_pole_modulus"]=="11^(-1/2)"
    assert c["native_theta_patch"]["is_irregular"]
