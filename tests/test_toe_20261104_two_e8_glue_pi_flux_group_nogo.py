"""Independent regression for icosian 2*E8: mixed glues, group no-go,
full-symmetry interlayer C4 and gauge-covariant pi flux / photonic control.

Exact finite arithmetic, finite group theory and calibrated toy models.
NO physical TOE, retrocausal photon, or W33 graph equivariant isomorphism.
"""
import importlib.util,sys,math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):
    if str(p) not in sys.path:sys.path.insert(0,str(p))
def module(name,filename):
    s=importlib.util.spec_from_file_location(name,ROOT/"analysis"/filename)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m
@pytest.fixture(scope="module")
def mismatch():
    return module("twoglue","toe_20261104_two_e8_glues_w33_symmetry_nogo.py").main()
@pytest.fixture(scope="module")
def bridge():
    return module("roots480","toe_20261104_double_e8_interlayer_c4_hamiltonian.py").main()
@pytest.fixture(scope="module")
def flux():
    return module("flux480","toe_20261104_two_e8_pi_flux_gauge_frame.py").main()
@pytest.fixture(scope="module")
def photo():
    return module("fourrail","toe_20261104_e8_c4_flux_photonic_falsifier.py").main()

def test_two_glue_root_shell_intersection_union(mismatch):
    assert mismatch["two_E8_lattice_norm2_root_counts"]==[240,240]
    assert mismatch["common_roots_of_both_E8_glues"]==40
    assert mismatch["common_roots_exactly_A4plusA4_roots"]
    assert mismatch["union_roots_across_both_glues"]==440

def test_glue_discriminant_planes_and_nonintegral_pairing(mismatch):
    assert mismatch["glue_discriminant_intersection_order"]==1
    assert mismatch["glue_discriminant_sum_order"]==25
    assert mismatch["cross_glue_vector_inner_product"]=="-12/5"
    assert mismatch["both_e8_glues_cannot_coexist_as_same_even_integral_sublattice"]
    assert mismatch["mixed_root_pair_count"]==240**2
    assert mismatch["mixed_root_pairs_noninteger_inner_product"]==40000
    assert sum(mismatch["mixed_root_inner_product_histogram"].values())==240**2

def test_no_full_H4_packet_action_into_W33_graph(mismatch):
    assert mismatch["point_grid_icosian_symmetry"]=="(A5×A5)⋊C2"
    assert mismatch["normal_base_order"]==3600
    assert mismatch["full_effective_H4_packet_group_order"]==7200
    assert mismatch["W33_graph_automorphism_group_order"]==51840
    assert mismatch["gcd_group_orders"]==1440
    assert mismatch["full_W33_graph_aut_factor5_exponent"]==1
    assert mismatch["H4_packet_group_factor5_exponent"]==2
    assert mismatch["any_full_H4_packet_group_homomorphism_to_W33_graph_aut_kills_A5xA5"]
    assert mismatch["max_image_order_of_full_H4_packet_group_in_W33_graph_aut"]==2

def test_interlayer_two_root_flip_completion_exact(bridge):
    assert bridge["intersheet_disconnected_components"]==120
    assert bridge["intersheet_each_component_is_four_cycle"]
    assert bridge["intersheet_degree_per_root"]==2
    assert bridge["intersheet_bipartite_edge_count"]==480
    assert bridge["intersheet_exact_minimal_polynomial"]=="A^3=4A"
    assert bridge["intersheet_adjacency_spectrum"]=={"-2":120,"0":240,"2":120}
    assert bridge["one_flip_matching_preserves_base_A5xA5_but_breaks_full_swap"]
    assert bridge["two_flip_completed_matching_preserves_all_five_group_generators"]

def test_combined_480_connected_root_graph_and_exact_integer_spectrum(bridge):
    assert bridge["e8_single_sheet_innerproduct1_degree"]==56
    assert bridge["e8_both_sheets_intralayer_edges"]==13440
    assert bridge["combined_graph_connected"]
    assert bridge["combined_graph_vertices"]==480
    assert bridge["combined_graph_regular_degree"]==58
    assert bridge["combined_graph_edges"]==13920
    assert bridge["combined_graph_eigenvalues"]=={
        "-6.0":84,"-2.0":308,"6.0":35,"10.0":35,
        "28.0":16,"54.0":1,"58.0":1}

def test_interlayer_240_dark_modes_protected_by_root_inversion(bridge):
    assert bridge["block_conjugacy_verified_integer"]
    assert bridge["root_inversion_commutes_with_E8_adj_exact"]
    assert bridge["full_H4_symmetric_interlayer_dark_subspace_dimension"]==240
    assert bridge["exact_two_sheet_spectrum_from_inversion_parity"]
    assert bridge["inversion_odd_subspace_T_eigenvalues"]=={"28":8,"-2":112}
    assert bridge["inversion_even_subspace_T_eigenvalues"]=={"56":1,"8":35,"-4":84}

def test_uniform_pi_flux_has_exact_full_rank_and_H4_gauge_lift(flux):
    assert flux["components"]==120
    assert flux["pi_flux_graph_exact_poly"]=="A_pi^2=2I480"
    assert flux["pi_flux_spectrum"]=={"-sqrt2":240,"sqrt2":240}
    assert flux["pi_flux_has_no_zero_eigenmodes"]
    assert flux["all_wilson_fluxes_minus_one"]
    assert flux["all_generators_gauge_covariant"]
    assert flux["full_H4_packet_generators_count"]==5
    assert flux["two_ticks_minus_identity"]

def test_strict_H4_edge_signs_force_20_zero_100_pi_and_40_dark(flux):
    assert flux["H4_interlayer_edge_orbit_sizes"]==[40,40,100,100,100,100]
    assert flux["strict_full_H4_20_common_A4_C4_forced_trivial_flux"]
    assert flux["strict_full_H4_100_noncommon_E8_glue_C4_allow_pi_flux"]
    assert not flux["strict_full_H4_signed_edge_pi_flux_possible_on_all_120_C4"]
    assert flux["strict_full_H4_partial_pi_flux_squares"]==100
    assert flux["strict_full_H4_partial_zero_flux_squares"]==20
    assert flux["strict_full_H4_partial_flux_residual_zero_modes"]==40
    assert flux["strict_full_H4_partial_pi_flux_verified_by_edge_orbit_signs"]

def test_four_rail_ideal_opposite_port_flux_contrast(photo):
    assert photo["modes_per_test_loop"]==4
    assert photo["initial_rail"]==0 and photo["opposite_output_rail"]==2
    assert abs(photo["ideal_target_interrogation_time"]-math.pi/2)<1e-12
    assert abs(photo["zero_flux_ideal_4port_probability_at_target"][2]-1)<1e-12
    assert abs(photo["pi_flux_ideal_4port_probability_at_target"][2])<1e-12
    assert photo["target_probability_contrast_ideal"]==1
    assert all(abs(z["pi_flux_opposite_probability"])<1e-11 for z in photo["ideal_time_scans"])
    assert all(abs(z["zero_flux_opposite_probability"]-math.sin(z["t"])**4)<1e-11
               for z in photo["ideal_time_scans"])

def test_loss_dephasing_lindblad_control_matches_analytic_survival(photo):
    rows=photo["uniform_loss_plus_markov_site_dephasing_control"]
    assert len(rows)==16
    for z in rows:
        eta=math.exp(-z["uniform_loss_rate"]*math.pi/2)
        assert abs(z["survival_probability"]-eta)<1e-11
        assert z["opposite_population_contrast_unconditional"]>0
        if z["site_dephasing_rate"]==0:
            assert abs(z["zero_flux_opposite_probability_unconditional"]-eta)<1e-10
            assert abs(z["pi_flux_opposite_probability_unconditional"])<1e-10
        assert z["exact_iid_one_sided_5sigma_binomial_error_threshold"]["trials"]>=1

def test_nonideal_four_rail_binomial_discrimination_is_exact_under_iid(photo):
    r=next(z for z in photo["uniform_loss_plus_markov_site_dephasing_control"]
            if z["uniform_loss_rate"]==.1 and z["site_dephasing_rate"]==.1)
    assert abs(r["zero_flux_opposite_probability_unconditional"]-.8024075069181063)<1e-11
    assert abs(r["pi_flux_opposite_probability_unconditional"]-.018623900471373876)<1e-11
    b=r["exact_iid_one_sided_5sigma_binomial_error_threshold"]
    assert b["trials"]==22
    assert b["decision_threshold_opposite_clicks"]==7
    assert b["false_positive_pi_as_zero"]<2.866515719e-7
    assert b["false_negative_zero_as_pi"]<2.866515719e-7

def test_phase_error_calibration_causes_pi_port_leak(photo):
    phi=photo["pi_edge_phase_calibration_error_scan"]
    assert len(phi)==6
    assert abs(phi[0]["pi_flux_opposite_leak_probability"])<1e-12
    assert all(x["pi_flux_opposite_leak_probability"]>0 for x in phi[1:])
