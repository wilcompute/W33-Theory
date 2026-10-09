"""Five additional independent W33/TOE research regression controls."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_spectral_linear_SOS_obstruction_exact_graph_identity():
    import w33_20261009_linear_current_scalar_SOS_obstruction as x
    d=x.certificate()
    assert d['bilinear_symbol_gram_rank']==160
    assert d['exact_min_eigenvalue']==5120000
    assert d['weighted_scalar_sum_impossible']
    assert d['exact_Gram_spectrum']['5120000']==81
def test_heterotic_raw_catalog_and_selection_boundary():
    d=json.loads((ROOT/'data/w33_20261009_heterotic_coupling_catalog_probe.json').read_text())
    assert d['status']=='PASS' and d['candidate_count']==11
    assert d['field_metadata_coverage']['w']['required_fields_present']==[]
    assert len(d['field_metadata_coverage']['sp']['required_fields_present'])==17
    assert d['by_catalog']['dbd']['parsed_C_lines']==170
    assert d['by_catalog']['mu']['parsed_C_lines']==51
    assert d['by_catalog']['dbd']['matching_count']==0
    assert d['by_catalog']['mu']['matching_count']==0
def test_actual_current_curvature_quantum_second_moment():
    import w33_20261009_isotropic_curvature_fluctuations as x
    d=x.certificate()
    assert d['actual_current_pairs']==480
    assert d['pair_type_variance_counts']=={
        "('line', '41/20')":240,"('point', '41/20')":240}
def test_factorial_optical_controls_and_confound():
    import w33_20261009_factorial_optical_gate_control as x
    d=x.certificate()
    assert d['trials_each']==96
    assert d['no_gate_interaction_rejections']<=6
    assert d['true_quartic_signal_rejections']>=60
    assert d['gate_times_sign_detector_artifact_rejections']>=50
def test_rank_three_quotient_has_unimodular_witness():
    import w33_20261009_triple_point_integral_3D_quotient as x
    d=x.certificate()
    assert d['subgroup_order']==27
    assert d['H_fixed_cycle_covector_rank']==3
    assert d['cycle_basis_rank']==81
    assert abs(d['nonzero_minor_determinant'])==1
    assert len(d['period_matrix_3_by_81'])==3
