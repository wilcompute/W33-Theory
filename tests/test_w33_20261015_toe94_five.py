"""TOE94 all five continued investigations: exact algebra, homology and devices."""
import json,math
from functools import lru_cache
from pathlib import Path
import pytest
from scipy.stats import binom
from analysis import w33_20261015_toe94_exact_central as E
from analysis import w33_20261015_toe94_face_obstruction as F
from analysis import w33_20261015_toe94_qkd_finite_iid as Q
from analysis import w33_20261015_toe94_mzi_drift as M
from analysis import w33_20261015_toe94_polar_guard as P
ROOT=Path(__file__).resolve().parents[1]
@lru_cache(None)
def doc(k):
    return {'exact':E.certificate,'face':F.evaluate,'qkd':Q.certificate,
            'drift':M.certificate,'polar':P.certificate}[k]()

def test_exact_Qzeta12_representation_central_obstruction():
    x=doc('exact')
    assert x['coefficient_field']=='Q(sqrt(3),i)=Q(zeta_12)'
    assert x['exact_lifted_commutator']=='-I4'
    assert x['exact_matrix_product_XY_plus_YX']=='zero 4x4 over Q(zeta12)'
    assert x['linearization_impossible_on_projective_25920_group']
    assert x['max_rational_reconstruction_residual']==0.

def test_face_F2_obstruction_selected_83_rank_code():
    x=doc('face')
    assert x['target_face_image_rank_over_F3']==83
    assert x['source_affine_vertex_count']==27
    assert x['source_affine_edge_count']==108
    assert x['source_face_census']=={
      'triangles':{'count':36,'bounds_mod3':18,'nonbounding_mod3':18},
      'chordless_squares':{'count':324,'bounds_mod3':0,'nonbounding_mod3':324}}
    assert x['first_failing_face']['face_type']=='triangles'
    assert x['first_failing_face']['cokernel_residual_edges']

def test_exact_polar_tetrad_and_event_inventory():
    x=doc('polar')
    assert x['space_decomposition']=={'affine':27,'polar_guard':13}
    assert x['polar_H27_orbit_sizes']==[1,3,3,3,3]
    assert x['tetrad_count_by_polar_membership']=={'1':36,'4':4}
    assert x['directed_detector_event_types']=={
      'affine->affine':216,'affine->polar':108,
      'polar->affine':108,'polar->polar':48}
    assert x['typed_accepted_affine_affine_events']==216
    assert x['typed_erasure_detector_events']==264

def test_polar_typed_erasure_admission_not_qkd_postselection():
    x=doc('polar')
    assert x['maximally_mixed_single_ray_polar_erasure_probability']==13/40
    assert x['directed_event_admission_fraction']==.45
    assert x['all_polar_tetrad_setting_fraction']==.1

def test_finite_iid_CP_virtual_phase_upper_interval():
    assert Q.N_TEST==4096
    for k in (0,1,4,15,40):
        ub=Q.phase_upper(k)
        assert k/4096<=ub<=1
        assert binom.cdf(k,4096,ub)==pytest.approx(.001,rel=1e-6,abs=1e-8)

def test_toeplitz_exact_two_universal_collision_sanity():
    assert Q.check_universal_small()==28

def test_QKD_Hamming_correctness_and_abort_models():
    x=doc('qkd')
    assert x['toeplitz_exact_small_pair_collision_checks']==28
    assert x['test_sample_count']==4096
    assert x['raw_key_pairs']==196
    assert len(x['trials'])==20
    assert x['accepted_trials']==20
    assert x['released_key_bits_total_over_20_synthetic_trials']==1828
    assert all(t['matched_extracted_key_when_accepted'] for t in x['trials'])

def test_MZI_two_arm_drift_calibrated_operator_spectral_bound():
    x=doc('drift')
    rows=x['rows']
    assert [z['phase_drift_max_radians'] for z in rows]==[0,.001,.002,.005,.01]
    assert rows[0]['trusted_no_background_separable_upper']==.4
    assert rows[-1]['trusted_no_background_separable_upper']==pytest.approx(.406217696786,abs=1e-8)
    assert all(z['violation_after_calibrated_adversarial_click_bound'] for z in rows)
    assert all(rows[i]['max_joint_operator_spectral_deviation']<rows[i+1]['max_joint_operator_spectral_deviation'] for i in range(4))

@pytest.mark.parametrize('key,filename',[
  ('exact','w33_20261015_toe94_exact_central.json'),
  ('face','w33_20261015_toe94_face_obstruction.json'),
  ('qkd','w33_20261015_toe94_qkd_finite_iid.json'),
  ('drift','w33_20261015_toe94_mzi_drift.json'),
  ('polar','w33_20261015_toe94_polar_guard.json')])
def test_frozen_result_certificates(key,filename):
    assert doc(key)==json.loads((ROOT/'data'/filename).read_text(encoding='utf8'))
