"""Regression gates for exact W33 finite null-frame construction and physical bounds."""
from __future__ import annotations
import importlib.util
import math
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location(
    "w33_selected_null_frame",ROOT/"analysis/w33_20261108_null_frame_selection_five_fronts.py")
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():
    return M.produce(ROOT)

def test_all_three_selected_directions_are_isotropic():
    for p in (3,5,7,11,17):
        coords,physical=M.null_coordinate_basis(p)
        assert len(coords)==p**3 and len(set(map(tuple,physical)))==p**3
        assert all(M.detq(x,p)==0 for x in M.DIRECTIONS)

def test_unitary_fourth_roots_and_exact_hermitian_logarithms():
    for p in (3,5,7):
        F,h=M.dft_and_log(p)
        import numpy as np
        from scipy.linalg import expm
        assert np.max(np.abs(expm(-1j*h)-F))<2e-12
        assert np.max(np.abs(h-h.conj().T))<2e-12

def test_p3_exact_flat_and_null_supported(cert):
    c=cert["clock"]["tested_cases"][0]
    assert c["p"]==3 and c["modes"]==27
    assert c["actual_undirected_null_hopping_edges"]==81
    assert c["max_flat_probability_error"]<1e-12
    assert c["maximal_forbidden_nonnull_hopping_magnitude"]<1e-12

def test_p5_exact_flat_overcomes_translation_invariant_search_only(cert):
    c=cert["clock"]["tested_cases"][1]
    assert c["p"]==5 and c["modes"]==125
    assert c["actual_undirected_null_hopping_edges"]==750
    assert c["max_flat_probability_error"]<1e-12
    assert c["maximal_forbidden_nonnull_hopping_magnitude"]<1e-12
    assert c["translation_shift_commutator_Frobenius"]>.1

def test_p7_exact_flat_null_supported(cert):
    c=cert["clock"]["tested_cases"][2]
    assert c["p"]==7 and c["modes"]==343
    assert c["actual_undirected_null_hopping_edges"]==3087
    assert c["max_flat_probability_error"]<1e-12
    assert c["maximal_forbidden_nonnull_hopping_magnitude"]<1e-12

def test_one_static_hamiltonian_not_switching_required(cert):
    c=cert["clock"]
    assert c["first_pulse_count_is_one"] is True
    assert c["commuting_directional_generators"]==3
    assert c["earlier_affine_no_go_not_contradicted"] is True

def test_projective_frame_symmetry_breaking_exact_gl2_group(cert):
    cases=cert["clock"]["frame_symmetry_orbit_checks"]
    assert [(x["p"],x["GL2_orbit_size"]) for x in cases]==[(3,4),(5,20),(7,56)]
    for x in cases:
        assert x["setwise_frame_stabilizer_order"]==6*(x["p"]-1)
        assert x["GL2_orbit_size"]==math.comb(x["p"]+1,3)

def test_maxwell_exact_two_transverse_branches(cert):
    for c in cert["Maxwell"]["cases"]:
        p=c["p"]
        assert c["transverse_modes_per_nonzero_momentum"]==2
        assert c["uniform_Wilson_holonomy_modes"]==3
        assert c["total_gauge_inequivalent_real_edge_modes"]==2*(p**3-1)+3

def test_maxwell_positive_lattice_dispersion_continuum(cert):
    cases=cert["Maxwell"]["cases"]
    assert cases[-1]["p"]==31
    assert cases[-1]["relative_dispersion_error"]<.004
    assert all(cases[i+1]["relative_dispersion_error"]<cases[i]["relative_dispersion_error"]
               for i in range(len(cases)-1))

def test_time_and_three_axes_are_assumed_not_emergent(cert):
    m=cert["Maxwell"]
    assert "ADDED independent" in M.framed_spatial_maxwell()["fixed_physical_setup"] or "added continuous time" in m["fixed_physical_setup"]
    assert "DOES NOT derive 3+1" in m["material_limitation"]

def test_e6_native_cubic_and_81_rank(cert):
    e=cert["E6"]
    assert e["source_cubic_signed_records"]==1620
    assert e["original_81_state_alternating_mass_rank"]==78
    assert e["completed_mass_rank"]==81

def test_e6_native_cubic_regular_level_set_two_real_constraints(cert):
    e=cert["E6"]
    assert e["two_real_component_cubic_Jacobian_nondegeneracy_witness"]>1e-7
    assert e["quartic_plus_complex_cubic_regular_level_set_dimension"]==475
    assert e["conditional_remaining_gauge_inequivalent_moduli_lower_bound"]==397

def test_e6_cubic_phase_preserving_relative_moduli(cert):
    e=cert["E6"]
    assert e["continuous_relative_spurion_phase_preserves_Gram_and_cubic"]
    assert e["phase_unpinned_in_quartic_only_mass_determinant_error"]<1e-8
    assert "only if invariance" in e["conditional_invariant"]

def test_photonic_27_mode_reck_upper_bound(cert):
    p=cert["photonic"]
    assert p["physical_modes"]==27
    assert p["p_mode_DFT_blocks_total"]==27
    assert p["max_two_mode_couplers_in_naive_DFT_triangular_synthesis"]==81

def test_photonic_echo_phase_not_invisible(cert):
    p=cert["photonic"]
    assert math.isclose(p["single_address_phase_echo_return_probability"],7/9)
    assert math.isclose(p["phase_error_echo_radians"],math.pi/3)

def test_photonic_common_mode_loss_only_affects_survival(cert):
    p=cert["photonic"]
    assert p["differential_transmission_average_survival"]<1
    assert 0<p["differential_transmission_conditional_total_variation"]<.01
    assert p["common_mode_transmission_conditional_total_variation"]<1e-15

def test_cosmology_six_patch_cells_reproduced(cert):
    c=cert["cosmology"]
    assert len(c["Lambda_control_cells"])==6
    assert all(abs(v["patched_scf_Lambda_ratio"]-1)<3e-6 for v in c["Lambda_control_cells"])

def test_cosmology_hmcode_halofit_distinct_models_not_detection(cert):
    c=cert["cosmology"]
    assert len(c["patched_two_prescription_fading_CPL_ratio_cells"])==6
    assert "no independent raw shear chains" in c["provenance"]

def test_cosmology_old_s7_s8_invalid_and_no_new_heldout(cert):
    c=cert["cosmology"]
    assert c["S7_S8_prepatch_shear_results_withdrawn"] is True
    assert c["independent_corrected_heldout_DES_KiDS_likelihood_executed"] is False
    for x in c["fixed_background_shear_model_comparison"].values():
        assert x["original_CPL_minus_fading_chi2"]>2.5
        assert -1<x["corrected_fixed_background_delta_chi2"]<0

def test_flavour_modulus_visible_sequestering_conditional(cert):
    c=cert["cosmology"]
    assert c["maximum_visible_rolling_flavour_admixture_under_proxy"]<6e-7
    assert c["sequestering_ratio_visible_over_dark_upper_bound"]<5.1e-5

def test_five_research_fronts_not_claimed_to_be_physical_toe(cert):
    assert {"clock","Maxwell","E6","photonic","cosmology"}<=set(cert)
    assert "No quantum gravitation" in cert["conclusion_boundary"]
    assert "conditional" in cert["E6"]["evidence_boundary"]


def test_new_81_hops_are_exact_subset_of_original_native_108_edges(cert):
    c=cert["clock"]["tested_cases"][0]
    assert c["native_27_graph_edge_count"]==108
    assert c["selected_hops_are_subset_of_native_27_graph"] is True
    assert c["actual_undirected_null_hopping_edges"]==81
