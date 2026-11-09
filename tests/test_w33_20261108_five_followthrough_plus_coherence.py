"""Regression contract: five W33 physical followthrough gates and frame coherence."""
from __future__ import annotations
import importlib.util
import math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("w33_5plus_coherence",
 ROOT/"analysis/w33_20261108_five_followthrough_plus_coherence.py")
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():
    return M.produce(ROOT)

def test_frame_potential_exact_orbit_minimum_count(cert):
    c=cert["frame"]["cases"]
    assert [r["degenerate_minima"] for r in c]==[4,20,56,220]
    assert all(r["degenerate_minima"]==r["GL2_orbit_size"] for r in c)

def test_frame_potential_radial_hessian_is_positive(cert):
    c=cert["frame"]["cases"]
    assert all(r["quartic_local_radial_mass_squared"]==2 for r in c)
    assert all(r["collective_radial_mass_squared"]>2 for r in c)

def test_frame_cannot_have_unique_symmetry_respecting_vacuum(cert):
    c=cert["frame"]
    assert c["selected_frames_are_PGL2_equivalent"] is True
    assert "every G-translated frame" in c["no_unique_symmetry_invariant_minimum_theorem"]
    assert "Elitzur" in c["caveat"]

def test_gauge_matter_native_selected_lattice_dimensions(cert):
    c=cert["Maxwell"]
    assert (c["vertices"],c["edges"],c["oriented_square_plaquettes"])==(27,81,81)
    assert c["vertex_gradient_rank"]==26

def test_full_nonlinear_U1_action_invariant(cert):
    assert cert["Maxwell"]["nonlinear_gauge_action_difference"]<1e-10

def test_gauge_Ward_and_Gauss(cert):
    c=cert["Maxwell"]
    assert c["finite_difference_gauge_Ward_residual"]<1e-7
    assert c["neutral_Gauss_constraint_residual"]<1e-10

def test_discrete_charge_continuity(cert):
    assert cert["Maxwell"]["discrete_charge_continuity_residual"]<1e-10

def test_no_false_qed_or_fine_structure_constant(cert):
    assert "Not a derivation of charge" in cert["Maxwell"]["proof_boundary"] or "Not a derivation" in cert["Maxwell"]["proof_boundary"]

def test_clock_noise_has_48_independent_trials(cert):
    c=cert["clock"]
    assert c["total_trials"]==48
    assert len(c["perturbations"])==6
    assert all(r["trials"]==8 for r in c["perturbations"])

def test_clock_error_levels_monotonic_with_sigma(cert):
    for kind in ("onsite_detuning","null_edge_coupling"):
        rows=[r for r in cert["clock"]["perturbations"] if r["type"]==kind]
        assert len(rows)==3
        assert rows[0]["mean_probability_error"]<rows[1]["mean_probability_error"]<rows[2]["mean_probability_error"]

def test_clock_noise_all_realistic_nonzero_and_bounded(cert):
    for r in cert["clock"]["perturbations"]:
        assert 0<r["worst_probability_error"]<2*r["worst_operator_norm"]+1e-10
        assert r["worst_TV"]>=r["mean_probability_error"]

def test_uniform_global_detuning_only_adds_phase(cert):
    assert cert["clock"]["uniform_common_onsite_shift_probability_error_less_than_1e_minus_12"] is True

def test_native_E6_cubic_triad_torus_dimension(cert):
    c=cert["E6"]
    assert (c["ordered_signed_records"],c["unordered_signed_E6_triples"])==(1620,45)
    assert c["e6_triad_incidence_rank"]==21
    assert c["e6_torus_nullspace_dimension"]==6

def test_native_E6_torus_and_external_SL3_transform_covariance(cert):
    c=cert["E6"]
    assert c["Cartan_torus_finite_rescaling_invariance_relative_error"]<1e-10
    assert c["external_SL3_complex_finite_invariance_relative_error"]<1e-10

def test_E6_all_generator_covariance_not_assumed(cert):
    c=cert["E6"]
    assert c["full_E6_covariance_certified"] is False
    assert c["candidate_VEV_cubic_interaction_physically_allowed_certified"] is False
    assert "other 72" in c["actual_conclusion"]

def test_old_shear_claims_remain_withdrawn(cert):
    c=cert["cosmology"]
    assert c["safety"].startswith("Old S7/S8")
    assert c["future_independent_shear_likelihood_executed"] is False

def test_s9_preregistry_is_not_observation(cert):
    c=cert["cosmology"]
    assert c["S9_preregistration_exists"] is True
    assert c["S9_preregistration_not_future_data"] is True

def test_halofit_corrected_control_six_cells(cert):
    rows=cert["cosmology"]["corrected_control_rows"]
    assert len(rows)==6
    assert all(abs(r["corrected_scf_over_Lambda"]-1)<3e-6 for r in rows)

def test_source_only_dark_energy_and_flavour_coupling_boundary(cert):
    c=cert["cosmology"]
    assert c["A4_flavour_modulus_clock_violation_factor_min"]>1e6
    assert "not observational validation" in c["source_crosscheck"]

def test_four_frame_coherence_has_all_physical_points(cert):
    c=cert["sixth"]
    assert c["frames"]==4 and c["point_count"]==27
    assert len(c["points"])==27
    assert c["all_channel_intensities"]==1/27

def test_q0_q1_q2_exact_purity_census(cert):
    c=cert["sixth"]["exact_purity_class_census"]
    assert c=={"0":{"0.25":8,"1.0":1},"1":{"0.25":6},"2":{"0.375":12}}

def test_frame_mixture_classical_information_invisible_to_intensity(cert):
    c=cert["sixth"]["representative_density_checks"]
    assert all(v["intensity_deviation"]<1e-12 for v in c.values())
    assert sorted(v["Tr_rho_squared"] for v in c.values())==pytest.approx([.25,.375,1.0])

def test_frame_eigenvalue_census_is_exact_character_multiplicity(cert):
    for r in cert["sixth"]["points"]:
        vals=r["rho_nonzero_eigenvalues"]
        assert abs(sum(vals)-1)<1e-13
        assert abs(sum(x*x for x in vals)-r["purity"])<1e-13
        assert all(int(round(z*4)) in (1,2,4) for z in vals)

def test_evidence_layers_are_separate(cert):
    assert set(cert)>={"frame","Maxwell","clock","E6","cosmology","sixth"}
    assert "No TOE" in cert["scientific_boundary"]


def test_reference_frame_inverse_echo_separates_hidden_frame_mixture(cert):
    e=cert["sixth"]["frame_matched_inverse_echo_probabilities"]
    assert e=={"origin":1,"q0_nonzero":.25,
               "q2_singleton_reference":.25,"q2_duplicated_reference":.5}


def test_charged_matter_links_reuse_native_null_graph_not_replacement(cert):
    c=cert["Maxwell"]
    assert c["original_native_graph_edges"]==108
    assert c["selected_81_edges_native_subset_verified"] is True
