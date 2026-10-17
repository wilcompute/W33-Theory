from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def J(name): return json.loads((ROOT/'data'/name).read_text())

def test_5150_exterior_parity():
    x=J('PART_W33_PASS5150_THETA_EXTERIOR_PARITY.json')
    assert [r['active_theta_checks'] for r in x['chamber_star_anchors']]==[32,324,1536,5000]

def test_5151_curvature():
    x=J('PART_W33_PASS5151_THETA_CURVATURE_SECOND_MOMENT.json')
    q=x['q2_exhaustive'];assert (q['nonzero_words'],q['curvature_zero_words'],q['curvature_zero_weight'],q['minimum_positive_defect'])==(65535,45,16,64)
    assert x['star_anchors']['5']['second_moment']==180000

def test_5152_centered_rayleigh():
    x=J('PART_W33_PASS5152_CENTERED_THETA_RAYLEIGH_WEIGHT.json')
    assert [r['rho'] for r in x['chamber_star_anchors']]==['116/37','144/19','1636/139','460/29']

def test_5153_q4_smith():
    x=J('PART_W33_PASS5153_Q4_ROOT_COSET_SMITH.json')
    assert x['smith_nonzero']=={'1':180,'2':4}
    assert (x['rank_Q'],x['rank_F2'],x['rank_F3'])==(184,180,184)
    assert x['cokernel']=='Z^72 direct_sum (Z/2)^4'

def test_5154_markov():
    x=J('PART_W33_PASS5154_THETA_TWO_STEP_MARKOV_CURVATURE.json')
    assert [r['minimum_P2'] for r in x['anchors']]==['3/8','5/16','7/24','9/32']

def test_5155_hidden_defect():
    x=J('PART_W33_PASS5155_NATIVE_AUGMENTATION_DEFECT.json')
    assert [r['rank_drop'] for r in x['rows']]==[0,1,4,8,10]
    assert [r['minimum_hidden_beyond_one_explicit_relation'] for r in x['rows']]==[0,0,3,7,9]

def test_5156_root_stats():
    x=J('PART_W33_PASS5156_ROOT_VOLUME_DEPTH_CALCULUS.json')
    assert [(r['N_positive_roots'],r['height_sum']) for r in x['rows']]==[(3,4),(4,7),(6,16)]

def test_5157_cheeger_blindness():
    x=J('PART_W33_PASS5157_THETA_CHEEGER_BLINDNESS.json')
    assert [(r['theta_degree'],r['inside_degree'],r['outside_degree']) for r in x['anchors']]==[(8,4,4),(16,8,8),(24,12,12),(32,16,16)]

def test_consolidated_collision_reconciliation():
    x=J('PART_W33_PASS5150_5157_CONSOLIDATED.json')
    assert x['status']=='EXECUTED_RESULTS_FROZEN_COLLISION_RECONCILED'
    assert 'renumbered to 5150-5157' in x['collision_reconciliation']
