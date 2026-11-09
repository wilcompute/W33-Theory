"""Adversarial native W33 five-front regression after CLASS/Halofit Pass12632."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("w33_falsifiers",ROOT/"analysis/w33_20261108_five_physical_falsifiers.py")
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():
    return M.produce(ROOT)

def test_native_squares_have_correct_count_and_rank(cert):
    s=cert["maxwell"]
    assert s["additional_translation_squares"]==162
    assert s["square_unique_count"]==162
    assert (s["triangle_boundary_rank"],s["completed_boundary_rank"])==(36,82)
    assert (s["modular_rank_prime"],s["modular_rank_witness"])==(101,82)
    assert s["exact_integer_annihilator"]=="K(K-3I)(K-6I)(K-9I)(K-12I)=0"
    assert (s["gradient_rank"],s["completed_harmonic_dimension"])==(26,0)

def test_complete_local_curvature_is_gapped_not_photons(cert):
    s=cert["maxwell"]
    assert s["magnetic_spectrum"]=={0:26,3:4,6:12,9:40,12:26}
    assert s["physical_gap_in_equal_stiffness_units"]==3
    assert "No two gapless" in s["warning"]

def test_native_e6_rank_and_invariant_stiefel_vacua(cert):
    e=cert["e6"]
    assert e["real_scalar_components"]==486
    assert e["normal_Gram_constraints"]==9
    assert e["vacuum_flat_real_dimension"]==477
    assert (e["native_mass_rank_before"],e["native_mass_rank_after"])==(78,81)

def test_e6_radial_stable_but_tangential_flat(cert):
    e=cert["e6"]
    assert abs(e["normal_quadratic_numerical_coefficient"]-e["expected_normal_coefficient"])<.005
    assert e["tangent_quadratic_numerical_coefficient"]<1e-6
    assert e["stable_radial_hessian_eigenvalue_for_lambda_v2_one"]==8

def test_e6_mass_rank_does_not_solve_strong_cp(cert):
    e=cert["e6"]
    assert e["mass_det_factorization_log_error"]<1e-6
    assert abs(e["mass_det_phase_radians"])>.01
    assert "477 flat" in e["missing_physics"]

def test_q5_complex_null_supported_hermitian_optimization(cert):
    c=cert["clock"]
    assert c["hilbert_dimension"]==125
    assert c["conjugate_hopping_pairs"]==12
    assert c["independent_real_hopping_parameters"]==24
    assert c["best_24_parameter_MSE"]<=c["initial_six_real_parameter_MSE"]+1e-10
    assert c["best_24_parameter_MSE"]>0

def test_q5_no_false_global_no_go_claim(cert):
    c=cert["clock"]
    assert "not a proof" in c["proof_boundary"]
    assert len(c["best_coefficients"])==24

def test_magic_three_feedforward_corrections_are_clifford(cert):
    p=cert["photonic"]
    assert len(p["correction_outcomes"])==3
    assert all(x["correction_is_qutrit_diagonal_Clifford"] for x in p["correction_outcomes"])
    assert abs(sum(x["probability"] for x in p["correction_outcomes"])-1)<1e-13

def test_729_intensities_cannot_certify_t9(cert):
    p=cert["photonic"]
    assert p["ideal_channel_intensity_values"]==729
    assert p["ideal_27_mode_tritters"]==27
    assert p["input_magic_phase_729_intensity_max_change"]<1e-13
    assert "TWO-qutrit" in p["hardware_boundary"]

def test_halofit_bug_prepatch_and_lambda_control_after_patch(cert):
    c=cert["cosmology"]
    assert len(c["original_and_patched_controls"])==6
    assert min(x["original_scalar_to_lambda_ratio"] for x in c["original_and_patched_controls"])<.43
    assert all(x["patched_relative_error"]<3e-6 for x in c["original_and_patched_controls"])

def test_shear_results_explicitly_withdrawn(cert):
    c=cert["cosmology"]
    assert c["fail_closed"] is True
    assert c["status"].startswith("WITHDRAWN")
    assert any("S8_hybrid" in s for s in c["failed_previous_model_assessment"])
    assert "DOES NOT independently rerun" in c["correctness_statement"]

def test_separate_evidence_classes(cert):
    assert set(cert)>=set(["maxwell","e6","clock","photonic","cosmology"])
    assert "no physical TOE" in cert["scientific_boundary"]


def test_stale_s8_and_cosmology_reports_have_visible_retractions():
    files=[
      "analysis/PASS20261108_S8_SHAPLEY_INTERACTION.md",
      "analysis/NOTE_DARK_ENERGY_EVIDENCE_20261108.md",
      "analysis/PASS20261108_FIVE_GATE_EXTENSIONS.md",
      "analysis/PASS20261108_FIVE_PHYSICS_GATES.md",
    ]
    for path in files:
        head=(ROOT/path).read_text(encoding="utf-8")[:1000]
        assert "PASS12632" in head
        assert "WITHDRAWN" in head or "WITHDRAWAL" in head


def test_latest_patched_fixed_background_shear_reverses_old_ranking(cert):
    rows=cert["cosmology"]["corrected_fixed_background_shear"]
    assert set(rows)=={"DES_Y3","KiDS_Legacy"}
    for row in rows.values():
        assert row["prepatch_CPL_minus_fading_chi2"]>2.5
        assert -1<row["patched_CPL_minus_fading_chi2"]<0
        assert row["original_positive_ordering_reversed"]
        assert "not held-out" in row["evidence_layer"]
