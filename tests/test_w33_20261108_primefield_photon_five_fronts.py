"""Regressions for native five-front prime-field, E6, clock, optical, and cosmology tests."""
from __future__ import annotations
import importlib.util
import math
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("primefield_five",ROOT/"analysis/w33_20261108_primefield_photon_five_fronts.py")
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():
    return M.produce(ROOT)

def test_native_prime3_four_direction_full_spectrum(cert):
    g=cert["prime_Maxwell"]
    assert g["q3_triangle_plus_square_spectral_multiplicities"]=={"3":4,"6":12,"9":40,"12":26}
    assert g["q3_gradient_modes"]==26
    assert g["q3_square_only_boundary_rank"]==78
    assert g["q3_square_only_harmonic_modes"]==4

def test_prime_family_transverse_branch_count(cert):
    for case in cert["prime_Maxwell"]["natural_full_null_direction_family"]:
        p=case["p"]
        assert case["edge_directions"]==p+1
        assert case["nonzero_momentum_transverse_branch_count"]==p
        assert case["physical_nonzero_k_modes"]==p*(p**3-1)

def test_nonuniform_primefield_continuum_ratio(cert):
    cases=cert["prime_Maxwell"]["natural_full_null_direction_family"]
    assert len(cases)==6
    assert cases[-1]["p"]==31
    assert cases[-1]["lateral_over_soft"]>48
    assert cases[-1]["lateral_over_soft"]>cases[-2]["lateral_over_soft"]

def test_gaussian_sum_bound_is_reproduced(cert):
    for case in cert["prime_Maxwell"]["natural_full_null_direction_family"]:
        p=case["p"]
        assert abs(case["local_square_Bloch_lateral_axis"]-2*p)<1e-9
        assert case["local_square_Bloch_quadratic_axis"]>=case["quadratic_Gauss_lower_bound"]-1e-9

def test_e6_native_symmetric_spurion_full_rank(cert):
    x=cert["E6"]
    assert x["native_signed_records"]==1620
    assert (x["native_rank_before"],x["native_rank_after"])==(78,81)

def test_e6_gauge_quotient_still_flat(cert):
    x=cert["E6"]
    assert x["real_dimensions"]==477
    assert x["upper_bound_E6_gauge_orbit_dimension"]==78
    assert x["lower_bound_unlifted_flat_moduli_after_E6_quotient"]==399
    assert x["conditional_lower_bound_if_extra_U3_flavor_is_gauged"]==390

def test_e6_potential_does_not_pin_spurion_phase(cert):
    x=cert["E6"]
    assert x["determinant_ratio_phase_error"]<1e-8
    assert x["determinant_log_magnitude_invariance_error"]<1e-8
    assert math.isclose(x["potential_invariant_phase_rotation_of_first_spurion"],math.pi/7)

def test_exact_flat_chirp_each_prime(cert):
    for x in cert["quantum_clock"]["data"]:
        assert x["max_flat_error"]<1e-12
        assert math.isclose(x["flat_probability"],x["p"]**-3)
        assert x["off_null_hopping_count"]>0

def test_q5_chirp_principal_log_needs_off_null_links(cert):
    x=next(x for x in cert["quantum_clock"]["data"] if x["p"]==5)
    assert x["principal_log_off_null_energy_fraction"]>.7
    assert x["minimum_relative_offdiagonal_Frobenius_distance_for_fixed_principal_H"]>.84

def test_no_false_general_local_generator_exclusion(cert):
    assert "NOT excluded" in cert["quantum_clock"]["scope"]

def test_single_photon_csum_is_exact_passive_permutation(cert):
    p=cert["photonic"]
    assert p["mode_count"]==27
    assert p["permutation_cycle_lengths"]=={"1":9,"3":6}
    assert p["minimum_arbitrary_rail_swap_count"]==12
    assert p["intra_particle_qutrit_nonseparability_Schmidt_rank"]==3

def test_ninth_root_intensity_blindness_and_phase_interferometry(cert):
    p=cert["photonic"]
    assert p["ninth_root_phase_required_nontrivial_rails"]==18
    assert p["intensity_blindness_to_direct_ninth_root_phase"] is True
    assert p["max_phase_sensitive_readout_difference"]>.05
    assert math.isclose(sum(p["Fourier_control_basis_readout_distribution_after"]),1)

def test_single_photon_exponential_mode_budget(cert):
    b=cert["photonic"]["rail_requirement_by_logical_qutrit_count"]
    assert b["3"]==27 and b["10"]==59049
    assert "independent photons" in cert["photonic"]["physical_distinction"].lower()

def test_corrected_halofit_control_and_matched_fluid(cert):
    x=cert["cosmology"]
    assert len(x["lambda_control_cells"])==6
    assert all(abs(v["patched_scf_to_Lambda"]-1)<3e-6 for v in x["lambda_control_cells"])
    assert x["matched_fluid_max_deviation"]["exp_neg"]["patched"]<.001

def test_patched_shear_reversal_is_recorded_not_claimed_as_detection(cert):
    x=cert["cosmology"]
    assert set(x["fixed_background_pairwise_chi2"])=={"DES_Y3","KiDS_Legacy"}
    for v in x["fixed_background_pairwise_chi2"].values():
        assert v["original_CPL_minus_fading"]>2.5
        assert -1<v["patched_CPL_minus_fading"]<0
    assert x["heldout_likelihood_recomputed"] is False
    assert x["S7_S8_original_shear_claims_withdrawn"] is True

def test_all_five_fronts_and_scientific_boundaries(cert):
    assert {"prime_Maxwell","E6","quantum_clock","photonic","cosmology"}<=set(cert)
    assert "No predictive TOE" in cert["evidence_boundary"]


def test_two_patched_nonlinear_prescriptions_are_distinct_and_close(cert):
    c=cert["cosmology"]["two_nonlinear_prescriptions_at_z001_k1"]
    assert 0<c["HMcode_fading_over_CPL_minus_one"]<.03
    assert 0<c["Halofit_fading_over_CPL_minus_one"]<.03
    assert c["HMcode_fading_over_CPL_minus_one"]>c["Halofit_fading_over_CPL_minus_one"]
    assert c["HMcode_scalar_LCDM_control_relative_error"]<.004
    assert "neither is calibrated" in c["physical_scope"]


def test_finite_lorentz_2plus1_is_not_automatically_3plus1_photon():
    g=M.prime_bloch_maxwell()
    assert g["reference_Maxwell_polarizations_in_2plus1_spacetime"]==1
    assert g["reference_Maxwell_polarizations_in_3plus1_spacetime"]==2
    assert "derive a 3+1 spacetime" in g["missing_dimension_bridge"]
