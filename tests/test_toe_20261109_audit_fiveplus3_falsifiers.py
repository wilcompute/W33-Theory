"""Regression gates for 43-commit audit + five strengthened fronts + three controls."""
from __future__ import annotations
import importlib.util,math
from fractions import Fraction
from pathlib import Path
import pytest
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("eight_new_gates",ROOT/"analysis/toe_20261109_audit_fiveplus3_falsifiers.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
@pytest.fixture(scope="module")
def cert():return M.produce()

def test_audit_all_intervening_commits_and_bytes(cert):
    a=cert["audit"]
    assert a["commits"]==43 and a["revisions"]==190
    assert a["final_changed_files"]==112 and a["bytes_read"]>=21_000_000

def test_potts_four_equal_global_vacua(cert):
    f=cert["frame"]
    assert f["exactly_degenerate_zero_energy_vacua"]==4
    assert f["first_nonzero_interface_energy"]==3
    assert f["all_configs"]==4**8

def test_potts_partition_enumeration_exact(cert):
    d=cert["frame"]["exact_energy_histogram"]
    assert sum(d.values())==65536 and d["0"]==4 and d["3"]==96

def test_potts_finite_volume_no_spontaneous_selection(cert):
    c=cert["frame"]
    assert "Finite volume has no spontaneous breaking" in c["caveat"]
    assert c["finite_volume_symmetric_mean_occupancy_per_frame"]==2

def test_potts_low_temp_increases_order(cert):
    r=cert["frame"]["beta_energy_sweeps"]
    assert [x["beta_J"] for x in r]==[.7,1.5,2.5]
    assert r[0]["expectation_largest_frame_fraction"]<r[1]["expectation_largest_frame_fraction"]<r[2]["expectation_largest_frame_fraction"]

def test_exact_magnetic_rational_compensation(cert):
    m=cert["magnetic"]
    assert m["critical_positive_short_weight"]=="5775/29857"
    assert m["supplied_short_weight"]=="1/16"
    assert m["determinant_lemma_verified_at_five_rational_alphas"] is True

def test_native_magnetic_sylvester_positive(cert):
    m=cert["magnetic"]
    assert len(m["positive_H_sylvester_leading_minors"])==6
    assert all(Fraction(z)>0 for z in m["positive_H_sylvester_leading_minors"])
    assert m["commutator_area_unimodular_determinant"] in (-1,1)

def test_magnetic_4plus1_not_physical_3plus1(cert):
    m=cert["magnetic"]
    assert m["source_spatial_deck_rank"]==4
    assert m["source_transverse_branches_per_nonzero_momentum"]==3
    assert m["observed_three_spatial_Maxwell_transverse_branches"]==2
    assert m["dimensionality_gap_explicit"]

def test_optical_inverse_echo_minimum_sample_search(cert):
    a=cert["optics"]
    assert a["minimum_accepted_heralded_events"]==17
    assert a["accept_frame_lock_if_echo_returns_at_least"]==12
    assert a["exact_false_positive_probability"]<=.001
    assert a["exact_minimum_power"]>=.99

def test_echo_previous_sample_is_infeasible(cert):
    a=cert["optics"];n=a["minimum_accepted_heralded_events"]-1
    for k in range(n+1):
        assert not (binom.sf(k-1,n,.30)<=.001 and binom.sf(k-1,n,.90)>=.99)

def test_echo_measurement_not_declared_real(cert):
    assert cert["optics"]["need_independent_loss_reference"] is True
    assert "not a demonstrated" in cert["optics"]["caveat"]

def test_e6_full_stabilizer_supersedes_partial_check(cert):
    e=cert["E6"]
    assert e["exact_e6_infinitesimal_generators"]==78
    assert e["E6_plus_SL3_infinitesimal_generators"]==86
    assert e["perturbative_family_anomaly_net"]==0

def test_e6_89_remaining_is_not_SM_mass_spectrum(cert):
    e=cert["E6"]
    assert e["canonical_untwisted_SM_minimum_duals"]==2
    assert e["signed_matter_repaired_sextic_uneaten_chiral_modes"]==89
    assert e["decomposition_after_SO10_branch"]=={"chiral_16s":3,"vectorlike_10s":3,"extra_1s_outside_each_16":11}

def test_e6_model_does_not_solve_masses(cert):
    assert "89 remaining massless fields" in cert["E6"]["open_gates"]

def test_cosmology_exact_heldout_score_arithmetic(cert):
    for x in cert["cosmology"]["three_models"]:
        assert abs(x["linear_expansion_elpd"]+x["DES_heldout_elpd"]+x["KiDS_heldout_elpd"]-x["all_heldout_elpd_total"])<1e-12

def test_cosmology_fading_cpl_gap_is_small(cert):
    assert 0<cert["cosmology"]["fading_minus_CPL_combined_elpd"]<.5
    assert cert["cosmology"]["best_model_claim_not_significant"]

def test_S9_is_only_future_preregistration(cert):
    c=cert["cosmology"]
    assert len(c["S9_preregistered_content_sha256"])==64
    assert c["S9_future_releases_observed_here"] is False

def test_frame_p3_reproduces_exact_purity_census(cert):
    p3=cert["prime_frames"]["tested"][0]
    assert p3["frames"]==4 and p3["points"]==27
    assert p3["exact_purity_census_by_Q"]=={"0":{"16/16":1,"4/16":8},"1":{"4/16":6},"2":{"6/16":12}}

def test_frame_p5_has_20_ensemble_members(cert):
    p=cert["prime_frames"]["tested"][1]
    assert p["frames"]==20 and p["points"]==125
    assert p["all_frame_and_mixture_output_intensities"]=="1/125"

def test_frame_p7_counterexample_same_determinant_different_purity(cert):
    p=cert["prime_frames"]["tested"][2]
    ex=next(v for v in p["counterexample_same_Q_different_purity"] if v["Q"]==6)
    assert ex["first_purity"]=="82/3136"
    assert ex["second_purity"]=="90/3136"
    assert ex["first_input"]==[2,0,3] and ex["second_input"]==[0,1,0]

def test_nonzero_Q_p7_coherence_not_a_determinant_only_law(cert):
    p=cert["prime_frames"]["tested"][2]
    assert all(p["Q_residue_classes_with_nonuniform_purity"][str(q)]>=3 for q in range(1,7))
    assert "chosen representatives" in cert["prime_frames"]["normalization_warning"]

def test_fermion_doubling_corner_count_and_orientation(cert):
    f=cert["lattice_fermions"]
    assert f["corner_Dirac_zeros_without_Wilson"]==8
    assert sum(f["Weyl_orientation_signs"].values())==8
    assert sorted(f["Weyl_orientation_signs"].values())==[4,4]

def test_Wilson_gaps_and_chiral_sacrifice(cert):
    f=cert["lattice_fermions"]
    assert f["Wilson_gap_by_pi_axis_count"]=={"0":0,"1":2,"2":4,"3":6}
    assert f["one_Dirac_cone_remains_after_Wilson"]
    assert f["original_chiral_symmetry_broken_by_Wilson_term"]

def test_antiunitary_cannot_be_global_unknown_state_unitary(cert):
    x=cert["triality"]
    assert x["two_basis_state_linear_extension_fidelity_to_conjugation"]<1e-14
    assert x["cannot_infer_physical_CP_from_combinatorial_reflection"]

def test_all_eight_fronts_have_scope_limits(cert):
    assert {"audit","frame","magnetic","optics","E6","cosmology","prime_frames","lattice_fermions","triality"}<=set(cert)
    assert "No new measured data" in cert["claim_boundary"]


def test_parallel_kramers_e7_late_commits_are_fail_closed(cert):
    x=cert["triality"]
    assert x["native_double_six_kramers_reflections"]==36
    assert x["native_each_fixed_points"]==0
    assert x["native_each_fixed_lines"]==10
    assert x["E7_60480_candidate_canonical_scalene_triple_passes"] is True
    assert x["E7_A7_singular_planes_only_two_not_three"] is True
