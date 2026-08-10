import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
sys.path.insert(0,str(ROOT/'analysis'))

def load(name):return json.loads((DATA/name).read_text(encoding="utf-8"))

def test_release_check_total():
    files=['w33_pass1074_schur_extension_formal_certificate.json','w33_pass1075_gsp43_character_fingerprint.json','w33_pass1076_spread_frame_incidence_algebra.json','w33_pass1077_g32_g25_invariant_restriction.json','w33_pass1078_photonic_hardware_backend.json']
    ds=[load(f) for f in files]
    assert all(d['status']=='PASS' for d in ds)
    assert sum(d['check_count'] for d in ds)==50
    assert all(all(d['checks'].values()) for d in ds)

def test_schur_extension_certificate():
    d=load('w33_pass1074_schur_extension_formal_certificate.json')
    assert d['orders']=={'base':25920,'extension':51840,'kernel':2}
    assert d['cocycle_identity_checks']==648000
    assert len(d['shortest_detected_minusI_word'])==10

def test_gsp_character_fingerprint():
    d=load('w33_pass1075_gsp43_character_fingerprint.json')
    assert d['identification']['group']=='GSp(4,3)'
    assert d['number_of_conjugacy_classes']==38
    assert d['permutation_character_inner_products']=={'full_point_action_rank':3,'full_spread_action_rank':3,'full_frame_action_rank':22,'inner_point_action_rank':3,'inner_spread_action_rank':3,'inner_frame_action_rank':32}

def test_incidence_algebra_boundary():
    d=load('w33_pass1076_spread_frame_incidence_algebra.json')
    assert d['incidence']=={'shape':[36,540],'row_degree':45,'column_degree':3,'total':1620}
    assert d['squared_singular_values']=={'27.0':20,'63.0':15,'135.0':1}
    assert d['coarse_relation_algebra_closed'] is False

def test_invariant_restriction_non_surjective():
    d=load('w33_pass1077_g32_g25_invariant_restriction.json')
    assert d['structural_decision']['restriction_surjective'] is False
    assert d['reflection_arrangement_restriction']['slice_hyperplane_factor_count']==1
    assert d['reflection_arrangement_restriction']['G25_hyperplanes']==12
    assert d['reflection_arrangement_restriction']['G32_hyperplanes']==40
    for f in d['G32_basic_restrictions_mod43'].values():
        for label,c in zip(f['basis'],f['coefficients_mod43']):
            if c: assert int(label.split('v9^')[1].split('*')[0])%2==0

def test_hardware_backend_fail_closed():
    d=load('w33_pass1078_photonic_hardware_backend.json')
    assert d['resources']['elementary_operations']==6480
    assert d['resources']['detector_channels']==4
    assert d['synthetic_fixtures']['positive']['decision']=='contextual_positive'
    assert d['synthetic_fixtures']['negative']['decision']=='noncontextual_negative'
    assert d['synthetic_fixtures']['bad_calibration']['decision']=='inconclusive_no_claim'

def test_lean_and_hardware_wiring():
    lean=(ROOT/'formal/W33/Pass1074SchurCocycleExtension.lean').read_text(encoding="utf-8")
    assert 'structure NormalizedCocycle' in lean
    assert 'theorem extensionMul_assoc' in lean
    assert 'theorem kernel_central' in lean
    assert 'theorem section_mul_iff' in lean
    assert 'W33.Pass1063.signedLiftFourRowObstruction' in lean
    for p in ['w33_pass1078_mesh_manifest.json','w33_pass1078_macro_schedule.json','w33_pass1078_blinded_index.json','w33_pass1078_real_data_fixture.csv']:
        assert (ROOT/'hardware'/p).exists()
