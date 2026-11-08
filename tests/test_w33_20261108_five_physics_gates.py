"""Five adversarial physics gates: finite Maxwell, null-local clock, E6, magic, cosmology."""
from __future__ import annotations
import importlib.util,math,json
from pathlib import Path
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("five_gates",ROOT/"analysis/w33_20261108_five_physics_gates.py")
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():return M.produce(ROOT)

def test_finite_maxwell_hodge_sums_to_all_edges(cert):
    x=cert["gauge"]
    assert (x["vertices"],x["edges"],x["triangles"])==(27,108,36)
    assert x["orthogonal_chain_dimensions"]=={"gradient_gauge":26,"harmonic":46,"coexact":36}
    assert sum(x["orthogonal_chain_dimensions"].values())==108

def test_gauge_action_invariance_and_curvature_eigenvalues(cert):
    x=cert["gauge"]
    assert x["magnetic_curvature_operator_eigenvalue_multiplicity"]=={"zero":72,"three":36}
    assert x["gauge_shift_action_error"]<1e-10
    assert x["H1_zero_curvature_residual"]<1e-9

def test_momentum_fiber_census_and_no_naive_photon_dispersion(cert):
    x=cert["gauge"]
    assert x["momentum_fibers_coexact_harmonic_gradient"]=={
        "(4, 0, 0)":1,"(2, 1, 1)":12,"(1, 2, 1)":8,"(0, 3, 1)":6}
    assert x["no_two_dispersing_photons_from_this_unmodified_action"] is True
    assert "not a complete" in x["physical_limit"]

def test_q5_exact_locality_stability_deficit(cert):
    d=cert["local_hamiltonian"]
    assert d["q5_unitary_amplitude_deficit"]==pytest.approx(1/(5*np.sqrt(5))-2/25,abs=1e-15)
    assert d["q5_unitary_probability_deficit"]==pytest.approx(1/125-4/625,abs=1e-15)
    assert "Duhamel" in d["exact_theorem"]

def test_local_6_direction_numerical_control_is_not_global(cert):
    d=cert["local_hamiltonian"]
    assert d["q5_6_null_direction_hopping_orbits"]==6
    assert d["q5_6_parameter_BFGS_seed_count"]==8
    assert d["q5_local_anisotropic_best_mean_squared_probability_error"]>0
    assert d["q5_local_anisotropic_best_max_probability_error"]>0
    assert len(d["q5_local_anisotropic_best_couplings"])==6
    assert "NOT a no-go" in d["scope"]

def test_native_e6_uses_1620_signed_records_not_toy(cert):
    d=cert["E6_three_scalar_spurions"]
    assert d["signed_native_tensor_records"]==1620
    assert d["native_dimension"]==81 and d["native_rank"]==78
    assert d["rank_with_three_repetitions_of_one_scalar"]==[78,79]

def test_three_gauge_covariant_form_spurions_lift_all_null_modes(cert):
    d=cert["E6_three_scalar_spurions"]
    assert d["rank_with_three_independent_extra_scalar_directions"]==[78,79,80,81]
    assert "Xi_a^dagger" in d["spurion_form"]
    assert "no F/D-flat vacuum" in d["scope"]

def test_no_spurious_strong_cp_success(cert):
    d=cert["E6_three_scalar_spurions"]
    assert math.isfinite(d["generic_complex_mass_determinant_phase_radians"])
    assert "NOT the physical" in d["cp_warning"]

def test_cubic_third_root_is_pauli_but_ninth_root_is_magic(cert):
    d=cert["photonic_nonclifford"]
    assert d["T9_is_identity"]
    assert d["T_is_nonclifford"]
    assert d["best_pauli_normalizer_overlap"]==pytest.approx(1/math.sqrt(3),abs=1e-12)
    assert "NOT a magic gate" in d["third_root_cubic_phase_is_only_Pauli"]

def test_wigner_signed_normalized_negativity(cert):
    d=cert["photonic_nonclifford"]
    w=list(d["injected_state_qutrit_discrete_wigner"].values())
    assert len(w)==9 and sum(w)==pytest.approx(1,abs=1e-12)
    assert sum(x<0 for x in w)==3
    assert d["wigner_minimum"]==pytest.approx(-0.0977094712857574,abs=1e-12)
    assert d["wigner_L1"]==pytest.approx(1.5862568277145446,abs=1e-12)
    assert d["log_wigner_negativity_mana"]==pytest.approx(math.log(d["wigner_L1"]),abs=1e-12)

def test_synthetic_phase_noise_calibration_analytic(cert):
    d=cert["photonic_nonclifford"]
    s=d["synthetic_independent_rail_phase_noise_sigma_rad"]
    want=1/27+(26/27)*math.exp(-s*s)
    assert d["synthetic_samples"]==4000
    assert d["analytic_expected_process_fidelity"]==pytest.approx(want,abs=1e-12)
    assert abs(d["synthetic_mean_process_fidelity"]-want)<.001

def test_kids_des_heldout_both_disfavor_cpl_vs_lcdm(cert):
    d=cert["cosmology"]
    assert d["fading_exceeds_LCDM_in_both_individual_shear_holdouts"] is False
    for name,rows in d["survey_heldout_elpd_vs_LCDM"].items():
        assert rows["CPL"]<rows["free_neg"]<rows["LCDM"]
    assert d["survey_heldout_elpd_vs_LCDM"]["kids_dovekie"]["CPL"]==pytest.approx(-3.0431257334722517)

def test_combined_model_score_is_only_arithmetic_sum(cert):
    d=cert["cosmology"]
    for x in d["combined_Dovekie_decomposition"].values():
        assert x["combined_gain"]==pytest.approx(x["oos_bao_sn_heldout_gain"]+x["des_shear_gain"]+x["kids_shear_gain"])
    assert d["fading_minus_CPL_combined"]==pytest.approx(4.405079640030536,abs=1e-9)

def test_small_f_root_solver_failure_is_not_physics_no_go(cert):
    d=cert["cosmology"]
    assert len(d["klt_root_bracketing_failures"])>=5
    assert d["solver_error_is_proof_of_no_physical_solution"] is False
    assert d["klt_control_absolute_chi2_difference"]<.001

def test_cosmology_cannot_claim_calibrated_significance(cert):
    d=cert["cosmology"]
    assert d["uncertainty_calibration_available_in_committed_aggregates"] is False
    assert any("overlapping" in x for x in d["caveats"])
    assert any("discrete anomaly" in x for x in d["caveats"])
    assert "No rerun from raw" in d["physical_limit"]

def test_all_five_distinct_evidence_fronts_present(cert):
    assert set(cert)>={"gauge","local_hamiltonian","E6_three_scalar_spurions",
                         "photonic_nonclifford","cosmology","scope"}
    assert "no complete TOE" in cert["scope"]
