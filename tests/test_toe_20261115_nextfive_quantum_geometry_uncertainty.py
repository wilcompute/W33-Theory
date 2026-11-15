"""Independent scoped end-to-end 2026-11-15 next-five-and-more regressions.

Five requested fronts: 4copy physical CP map, genus6 geometry, D9,
F8 mixed-state control, photonic witness-specific calibration.
Prior 2026-11-15 producers are imported read-only as existing input.
"""
import importlib.util,json,math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
def load(rel,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/"analysis"/rel)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

@pytest.fixture(scope="module")
def fourcopy():
    return load("toe_20261115_symmetric_fourcopy_W33_E6_heralded.py","sym4").run()

@pytest.fixture(scope="module")
def genus():
    return load("toe_20261115_genus6_plane_optimization.py","genus")

@pytest.fixture(scope="module")
def rational():
    return load("toe_20261115_genus6_exact_rational_crossings.py","rat").run()

@pytest.fixture(scope="module")
def d9():
    return load("toe_20261115_D9_product_oneform_KK_decomposition.py","d9").run()

@pytest.fixture(scope="module")
def f8():
    return load("toe_20261115_F8_mixed_purity_stabilizer_falsifier.py","f8").run()

@pytest.fixture(scope="module")
def photon():
    return load("toe_20261115_direct_witness_contrast_calibration.py","photon").run()

def test_4copy_exact_symmetry_and_Gram(fourcopy):
    assert fourcopy["all_40_symplectic_transvections_covariant"]
    assert fourcopy["rank_output"]==27
    assert fourcopy["exact_Gram_diagonal_adjacent_nonadjacent"]==[1440,24,60]
    assert fourcopy["exact_Gram_eigenvalues_mult"]=={
       "uniform_1":2640,"schlafli_20":1344,"schlafli_dark_6":1560}

def test_4copy_heralded_CP_contraction(fourcopy):
    assert fourcopy["K_contraction_verified"]
    assert fourcopy["kraus_normalization_lambda_max"]==2640
    assert fourcopy["symmetric_fourcopy_Hilbert_dimension"]==math.comb(43,4)
    assert 0<fourcopy["uniform_superposition_4copy_success_probability"]<1
    assert fourcopy["rank_output"]==27

def test_four_point_multiplicity_and_no_double_count(fourcopy):
    assert fourcopy["nonedge_point_pairs_per_octet"]==12
    assert fourcopy["disjoint_octet_pairs"]==270
    assert fourcopy["point_pair_decompositions"]==38880
    assert fourcopy["distinct_unordered_fourpoint_inputs"]==22680
    assert fourcopy["quartet_pair_decomposition_multiplicity"]=={1:6480,2:16200}
    assert fourcopy["quartet_distinct_E6_output_labels"]=={1:6480,2:16200}

def test_Haar_and_random_phase_selection_penalty(fourcopy):
    assert fourcopy["Haar_random_pure_40_mode_state_4copy_mean_success"]==pytest.approx(
      (27*1440)/(2640*math.comb(43,4)))
    assert fourcopy["fixed_uniform_magnitudes_random_independent_phases_mean_success"]==pytest.approx(
      24*(27*1440)/(2640*40**4))
    assert fourcopy["coherent_uniform_to_Haar_success_ratio"]>1600
    assert fourcopy["coherent_uniform_to_random_phase_success_ratio"]==pytest.approx(1440)

def test_no_onecopy_POVM_with_required_success_law(fourcopy):
    assert fourcopy["no_singlecopy_POVM_can_reproduce_success_law"]
    assert "zero diagonal" in fourcopy["no_singlecopy_POVM_proof"]

def test_genus6_exact_geometry_and_saved_candidate(genus,rational):
    saved=json.loads((ROOT/"data"/"toe_20261115_genus6_12plane_optimized_necessary.json").read_text())
    v,_=genus.score(__import__("numpy").array(saved["parameters"]).ravel())
    assert v==saved["best_total_face_self_crossings"]==8
    assert rational["exact_total_proper_crossings"]==8
    assert sum(rational["exact_proper_crossings_each_face"])==8
    assert len(rational["exact_proper_crossings_each_face"])==12
    assert rational["nonadjacent_segment_orientation_zero_tests"]==0
    assert rational["failure_of_local_face_simplicity"]

def test_genus6_nonrealizability_NOT_proved(rational):
    assert "neither genus-6 dual nonrealizability" in rational["limits"]

def test_D9_scalar_and_oneform_Hodge_counts(d9):
    assert d9["scalar_harmonic_count"]==6561
    assert d9["exact_oneform_count_in_window"]==6560
    assert d9["coexact_oneform_count_in_window"]==19360
    assert d9["total_oneform_count_in_window"]==25920
    assert d9["six_Killing_oneforms_inside_coexact_modes"]==6

def test_D9_kinematics_is_not_full_mixed_mass(d9):
    assert d9["independent_coexact_polarizations_l1l2"]=={
      "0,0":0,"a>0,0":1,"0,b>0":1,"a>0,b>0":3}
    assert "NOT the dynamically mixed" in d9["model_scope"]
    assert len(d9["mode_table"])==81

def test_F8_explicit_uncovered_stabilizer_subspace(f8):
    assert f8["best_isotropic_dimension"]==5
    assert f8["all_nonzero_subspace_labels_uncovered"]
    assert len(f8["all_labels_in_span"])==32
    assert len(set(f8["all_labels_in_span"]))==32
    assert f8["covered_nonidentity_labels"]==567
    assert f8["state_purity_Tr_rho_squared"]==.5
    assert f8["covered_Pauli_expectation_square_sum"]==0

def test_F8_matrix_verified_logical_qubit_purity_law(f8):
    assert f8["covered_Pauli_counts_in_three_logical_cosets"]==[3,3,3]
    assert f8["maximally_mixed_stabilizer_code_rank"]==2
    assert "cx*rx^2+cy*ry^2+cz*rz^2" in f8["exact_purity_dependent_objective_in_this_code"]
    assert "(2*purity-1)" in f8["minimal_C_at_fixed_purity_in_code"]
    assert "pure-state" in f8["exact_pure_vs_mixed_scope"]

def test_photonic_model_free_16_rail_contrast_calibration(photon):
    assert photon["accepted_rail_preparations_each"]==52642
    assert photon["accepted_total_calibration"]==1137384
    assert photon["accepted_total_rail_calibration"]==842272
    assert photon["accepted_parity_calibrations_each"]==147556
    assert photon["joint_99pct_corrected_fidelity_lower"]>.9
    assert "Does NOT assume circulant" in photon["assumptions"]

def test_photonic_one_rail_anomaly_detected(photon):
    assert photon["single_corrupted_rail_analytic_contrast_anomaly"]>.5
    assert photon["rail_specific_anomaly_detectable_without_circulant_assumption"]
    assert sum(photon["joint_failure_split"].values())==pytest.approx(.01)

def test_preserved_temporary_data_and_existing_repo_inputs():
    assert (ROOT/"analysis"/"w33_pass1536_frame_dual_k44_code.py").exists()
    assert (ROOT/"analysis"/"w33_genus_six_execution.py").exists()

def test_json_fixtures_reproducible(fourcopy,d9,f8,photon,rational):
    fixtures={
      "toe_20261115_full_equivariant_fourcopy_quantum_channel.json":("rank_output",27),
      "toe_20261115_D9_S2S2_Hodge_vector_KK_pre_mix.json":("coexact_oneform_count_in_window",19360),
      "toe_20261115_F8_mixed_uncovered_stabilizer.json":("best_isotropic_dimension",5),
      "toe_20261115_direct_witness_contrast_calibration.json":("accepted_total_calibration",1137384),
      "toe_20261115_genus6_12plane_exact_rational_crossings.json":("exact_total_proper_crossings",8)}
    for fname,(k,v) in fixtures.items():
        assert json.loads((ROOT/"data"/fname).read_text())[k]==v
