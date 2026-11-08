"""Five-front native dimensional reduction, Pfaffian, local speed, photonic scaling, S7."""
from __future__ import annotations
import importlib.util, math, os
from pathlib import Path
import numpy as np
import pytest
SRCROOT=Path(__file__).resolve().parents[1]
ROOT=Path(os.environ.get("W33_REPO_ROOT",str(SRCROOT)))
SPEC=importlib.util.spec_from_file_location("five_bridges",
          SRCROOT/"analysis/w33_20261108_five_boundary_bridges.py")
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():return M.produce(ROOT)

def test_native_four_spatial_metric_reused_not_fitted(cert):
    x=cert["gauge_reduction"]
    assert x["native_matrix_M"]==[[10,5,-6,0],[5,10,0,-6],[-6,0,12,-6],[0,-6,-6,12]]
    assert x["native_metric_determinant"]==2916
    assert x["inverse_kinetic_M44"]=="5/27"
    assert x["Schur_scalar_metric"]=="27/5"

def test_compact_zero_mode_has_two_transverse_and_one_scalar(cert):
    x=cert["gauge_reduction"]
    assert x["three_space_zero_mode_assumption"].startswith("k4=0")
    assert x["two_transverse_3D_modes_plus_one_scalar"]
    assert x["unlifted_physical_transverse_modes"]==3
    assert x["scalar_mass_gap_squared"]=="1/27"
    assert len(x["exact_three_momenta"])==3
    assert all(y["scalar_extra_gap_omega2"]=="1/27" for y in x["exact_three_momenta"])

def test_Wilson_effective_mass_not_full_4d_gauge_invariant(cert):
    x=cert["gauge_reduction"]
    assert x["nonzero_k4_breaks_full_4D_gauge_symmetry"]
    assert "NOT a local gauge-invariant full 4D mass" in x["supplied_Wilson_mass_term"]
    assert "do not derive why" in x["critical_limit"]

def test_native_e6_1620_signed_entries_rank78(cert):
    x=cert["native_E6_augmented_pfaffian"]
    assert x["records"]==1620 and x["native_skew_rank"]==78
    assert x["three_spurion_full_rank"]==81
    assert x["augmented_skew_dimension"]==84

def test_e6_augmented_pfaffian_square_identity_native(cert):
    x=cert["native_E6_augmented_pfaffian"]
    assert "corank AT LEAST THREE" in x["identity"]
    assert x["native_relative_determinant_phase_error"]<1e-7
    assert x["native_log_modulus_error"]<1e-7

def test_wrong_unrestricted_pfaffian_claim_caught_exactly(cert):
    x=cert["native_E6_augmented_pfaffian"]
    assert x["corank_one_three_column_adversarial_counterexample"]=={
         "det_mass":105,"augmented_pfaffian_squared":49}
    assert "NOT true" in x["identity"]

def test_E6_scalar_phase_rotates_twice_and_is_not_strong_CP(cert):
    x=cert["native_E6_augmented_pfaffian"]
    assert x["augmented_pfaffian_rephasing_error"]<1e-7
    assert x["mass_determinant_double_rephasing_error"]<1e-7
    assert x["one_spurion_rephasing_theta"]==pytest.approx(math.pi/9,abs=1e-15)
    assert "does NOT force its phase to vanish" in x["cp_boundary"]

def test_general_strict_null_local_quadratic_speed_limit(cert):
    x=cert["null_local_quantum_speed"]
    assert "non-translation-invariant" in x["theorem"]
    assert x["target_flat_amplitude"]==pytest.approx(5**-1.5)
    assert x["minimum_dimensionless_time_energy"]==pytest.approx(math.sqrt(2)*5**(-.75))
    assert x["synthetic_H_null_hopping_pairs"]==12

def test_nonnull_25_50_and_100_millisecond_controls(cert):
    x=cert["null_local_quantum_speed"]
    assert [z["normalized_time_tH"] for z in x["tested_times"]]==[.05,.1,.25]
    assert all(z["actual_nonnull_transition_amplitude"]<=z["rigorous_Taylor_bound"]+1e-12 for z in x["tested_times"])

def test_speed_limit_not_flat_mixing_no_go(cert):
    x=cert["null_local_quantum_speed"]
    assert "not a universal no-flat-mixing" in x["boundary"]

def test_single_photon_nonclifford_adaptive_branch_classically_tracked(cert):
    x=cert["one_photon_photonic_scaling"]
    assert x["modes"]==27 and x["logical_qutrits"]==3
    assert x["measured_first_address_probabilities"]==pytest.approx([1/3]*3,abs=1e-12)
    assert x["conditional_feedforward_state_norm"]==pytest.approx(1,abs=1e-12)
    assert "ninth-root" in x["unitary"]

def test_one_photon_exponential_mode_lower_bound(cert):
    x=cert["one_photon_photonic_scaling"]
    assert x["modes_needed_for_n_logical_qutrits"]=={
       "3":27,"5":243,"10":59049,"15":14348907,"20":3486784401}
    assert x["example_n20_orthogonal_modes"]==3486784401
    assert "already identified" in x["complexity_boundary"]

def test_polynomial_classical_sampling_model_is_restricted(cert):
    x=cert["one_photon_photonic_scaling"]
    assert "O(N^2)" in x["dense_gate_cost_arithmetic"]
    assert "polynomial(N,gate count)" in x["optical_boundary"]
    assert "different task" in x["optical_boundary"]

def test_s7_preregistered_prediction_has_unchanged_hash(cert):
    x=cert["cosmology_prereg_and_PPD"]
    assert len(x["S7_frozen_hash_sha256"])==64
    assert x["new_release_holdout_scored"] is False
    assert x["S7_prediction"].startswith("CPL/fading")

def test_s7_tomography_signs_and_pair_counts(cert):
    b=cert["cosmology_prereg_and_PPD"]["S7_tomographic_signed_ratios"]
    assert b["des_pairs"]["count"]==10
    assert b["kids_pairs"]["count"]==21
    assert b["des_pairs"]["minimum_low_z_relative_tilt"]<-.04
    assert b["kids_pairs"]["minimum_low_z_relative_tilt"]<-.03

def test_KLT_samples_are_in_progress_and_failures_visible(cert):
    x=cert["cosmology_prereg_and_PPD"]
    assert x["KLT_preliminary_PPD_rows"]["bao"]["klt25_infl1"]["accepted"]==18
    assert x["KLT_preliminary_PPD_rows"]["sn"]["klt25_infl1"]["accepted"]==12
    assert x["KLT_preliminary_PPD_rows"]["sn"]["klt25_infl1"]["solver_failed"]==12
    assert x["KLT_failures_not_physical_exclusion"]
    assert "IN_PROGRESS" in x["KLT_PPD_class"]

def test_no_cosmology_calibrated_detection_claim(cert):
    x=cert["cosmology_prereg_and_PPD"]
    assert "do not justify a calibrated" in x["statistical_boundary"]
    assert "only verifies" in x["provenance"]

def test_all_five_distinct_boundaries(cert):
    assert set(cert)>={"gauge_reduction","native_E6_augmented_pfaffian",
       "null_local_quantum_speed","one_photon_photonic_scaling",
       "cosmology_prereg_and_PPD","scope"}
    assert "not experimentally confirmed" in cert["scope"]
