"""Regression: actual 25packet A5 spectral graph map vs Witting POVM darkness,
reciprocal class1 8D Hermitian observable embedding, true U4 A5 lift,
loss-aware Fisher, and 440 E8 root-derived positive density states."""
import importlib.util,sys,math
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
for x in (ROOT,ROOT/"analysis"):
    if str(x) not in sys.path:sys.path.insert(0,str(x))
def load(key,file):
    sp=importlib.util.spec_from_file_location(key,ROOT/"analysis"/file)
    m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
    return m
@pytest.fixture(scope="module")
def bridge():
    return load("physical_a5bridge","toe_20261104_witting_operator_dark_spectral_A5_duality.py").main()
@pytest.fixture(scope="module")
def wigner():
    return load("physical_a5wigner","toe_20261104_witting_A5_unitary_lift_and_fisher.py").main()
@pytest.fixture(scope="module")
def codebook():
    return load("physical_e8book","toe_20261104_two_e8_root_to_witting_density_codebook.py").main()

def test_witting_physical_operator_gram_and_kernel(bridge):
    assert bridge["Witting_projector_Gram_rank"]==16
    assert bridge["Witting_projector_Gram_spectrum"]=={"10":1,"2":15,"0":24}
    assert bridge["W33_graph_adjacency_spectrum"]=={"12":1,"2":24,"-4":15}
    assert bridge["linear_Witting_ray_to_Hermitian_map_kernel_is_W33_eigenvalue2_dim24"]

def test_prior_graph25_spectral_embedding_operator_rank_one(bridge):
    assert bridge["class0_graph_spectral_25_real_amplitudes_to_ququart_operator_rank"]==1
    assert bridge["class0_embedded_8dim_E8_A4plusA4_kernel_is_Witting_operator_dark"]
    assert bridge["spectral_25_projection_nonnegative_orthogonal_map_impossible"]
    p=bridge["spectral_25_projector_entry_values"]
    assert abs(p["diagonal"]-5/8)<1e-12
    assert abs(p["orthogonal_ray_pair"]-1/8)<1e-12
    assert abs(p["nonorthogonal_distinct_ray_pair"]+1/24)<1e-12

def test_reciprocal_A5_classes_on_traceless_sector(bridge):
    a,b=bridge["A5_classes"]
    assert a["A5_class_index"]==0 and b["A5_class_index"]==1
    assert [a["traceless_operator_intertwiner_rank"],b["traceless_operator_intertwiner_rank"]]==[4,8]
    assert a["previous_25dim_graph_spectral_12plus2_isometry"]
    assert not b["previous_25dim_graph_spectral_12plus2_isometry"]
    assert a["target_traceless_W33_eigen_minus4_irreps"]["4"]==1
    assert b["target_traceless_W33_eigen_minus4_irreps"]["4"]==2
    assert a["independent_seed_rank_trials"]==[4]*3
    assert b["independent_seed_rank_trials"]==[8]*3

def test_actual_8d_hermitian_map_unit_hilbert_schmidt(bridge):
    b=bridge["A5_classes"][1]
    W=np.array(b["explicit_W33_40x8_observable_coefficient_map"])
    X=np.array(b["explicit_8_Hermitian_ququart_observables_real"])+1j*np.array(
       b["explicit_8_Hermitian_ququart_observables_imag"])
    assert W.shape==(40,8) and X.shape==(8,4,4)
    assert np.max(abs(W.T@W-np.eye(8)))<1e-10
    assert np.max(abs(X-X.conj().transpose(0,2,1)))<1e-10
    assert np.max(abs(np.trace(X,axis1=1,axis2=2)))<1e-10
    assert np.max(abs(np.einsum("iab,jba->ij",X,X)-2*np.eye(8)))<1e-10

def test_eight_plus_eight_physical_density_controls(bridge):
    b=bridge["A5_classes"][1]
    assert b["example_16_density_matrices_eight_plus_eight_psd_verified"]
    assert len(b["example_density_eigenvalue_and_40POVM_distinguishability"])==8
    for p in b["example_density_eigenvalue_and_40POVM_distinguishability"]:
        assert p["min_eigen_plus"]>0 and p["min_eigen_minus"]>0
        assert p["total_variation_between_plus_minus"]>0

def test_both_native_A5_classes_have_real_U4_lifts(wigner):
    assert len(wigner["group_records"])==2
    for x in wigner["group_records"]:
        assert x["unitary_vs_antiunitary_triple_Bargmann_invariant_census"]=={"unitary":60}
        assert sorted(x["generator_orders"])==[3,5]
        assert len(x["verified_Witting_projective_unitary_generators"])==2
        for g in x["verified_Witting_projective_unitary_generators"]:
            U=np.array(g["U4_real"])+1j*np.array(g["U4_imag"])
            assert abs(np.linalg.det(U))>1-1e-10
            assert np.max(abs(U.conj().T@U-np.eye(4)))<1e-10
            assert g["maximum_40ray_projector_conjugation_residual"]<1e-10

def test_class1_8d_embedding_physically_covariant_not_just_graph(wigner):
    assert wigner["class1_E8_A4plusA4_8real_params_acts_by_physical_projective_unitary_A5"]
    assert wigner["group_records"][1]["class1_reye_8dim_operator_embedding_physically_A5_covariant"]
    assert not wigner["group_records"][0]["class1_reye_8dim_operator_embedding_physically_A5_covariant"]

def test_fisher_eight_real_coordinates_isotropic(wigner):
    assert abs(wigner["at_maximally_mixed_ququart_8parameter_Fisher_per_detected_photon"]-8/5)<1e-10
    f=np.array(wigner["Fisher_matrix_8params"])
    assert np.max(abs(f-8*np.eye(8)/5))<1e-10

def test_loss_efficiency_nuisance_fisher_orthogonal(wigner):
    eta=wigner["independent_erasure_eta"]
    ff=np.array(wigner["with_erasure_41outcome_Fisher_eight_density_params_and_eta"])
    assert ff.shape==(9,9)
    assert np.max(abs(ff[:8,:8]-eta*1.6*np.eye(8)))<1e-10
    assert np.max(abs(ff[8,:8]))<1e-10
    assert abs(ff[8,8]-1/(eta*(1-eta)))<1e-10

def test_multinomial_fisher_CRLB_control(wigner):
    var=wigner["CRLB_variance_per_density_coordinate_at_theta0"]
    assert abs(var-5/(8*10000*.85))<1e-12
    values=np.array(wigner["Monte_Carlo_variance_eight_coordinates"])
    assert values.shape==(8,)
    assert np.max(abs(values/var-1))<.2

def test_440_unique_E8_roots_mixed_density_positive(codebook):
    assert codebook["E8_plus_root_count"]==240
    assert codebook["E8_minus_root_count"]==240
    assert codebook["shared_roots_count"]==40
    assert codebook["two_sheet_unique_roots_count"]==440
    assert codebook["all_440_hermitian_ququart_states_psd"]
    assert codebook["all_440_density_matrices_distinct"]
    assert codebook["actual_minimum_density_eigenvalue"]>.15
    assert abs(codebook["uniform_density_purity"]-.27)<1e-10

def test_exact_E8_metric_survives_ququart_HS_overlap(codebook):
    assert codebook["maximum_density_Hilbert_Schmidt_Gram_residual"]<1e-10
    assert codebook["cross_sheet_noninteger_root_innerproduct_pairs"]==40000
    assert len(codebook["all_440_exact_root_coordinates_scaled_by5"])==440
    assert len(codebook["eight_real_parameters_for_440_states"])==440
    R=np.array(codebook["all_440_exact_root_coordinates_scaled_by5"])
    assert R.shape==(440,10)
    assert np.max(abs(np.sum(R*R,axis=1)-50))==0

def test_all_440_distinct_Witting_POVM_distributions(codebook):
    assert codebook["Witting_40outcome_POVM_tomographic_rank_on_8D_codebook"]==8
    assert codebook["Witting_POVM_440_state_min_pair_total_variation"]>.03
    assert codebook["Witting_POVM_440_state_max_pair_total_variation"]<1
    assert codebook["Witting_40outcome_probability_minimum"]>0

def test_uniform_positivity_ball_covers_entire_440_root_shell(codebook):
    assert abs(codebook["universal_PSD_8parameter_ball_radius"]-1/math.sqrt(24))<1e-12
    assert codebook["uniform_real_coordinate_encoding_epsilon"]<codebook["universal_PSD_8parameter_ball_radius"]
    assert codebook["actual_minimum_density_eigenvalue"]>codebook["universal_lower_eigenvalue_bound"]-1e-10

def test_root_codebook_information_is_not_440_orthogonal_states(codebook):
    assert abs(codebook["uniform_440root_label_entropy_bits"]-math.log2(440))<1e-12
    assert abs(codebook["Holevo_single_ququart_upper_bound_accessible_bits_per_copy"]-2)<1e-12
    assert abs(codebook["uniform_440root_label_Witting_POVM_information_bits_per_detected_photon"]-.011617757280846361)<1e-10
    assert codebook["Fano_necessary_detected_photon_count"]==694
    assert codebook["Fano_necessary_incident_photon_count_if_survival_85percent"]==816
    assert codebook["Fano_target_max_classification_error"]==.05
