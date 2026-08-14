from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def J(name):
    return json.loads((ROOT/'data'/name).read_text())

def test_pass5142_exterior_parity():
    x=J('PART_W33_PASS5142_THETA_EXTERIOR_PARITY.json')
    assert x['status']=='THEOREM_ALL_Q_THETA_EXTERIOR_PARITY_CONSERVATION'
    assert [r['active_theta_checks'] for r in x['chamber_star_anchors']]==[32,324,1536,5000]
    assert [r['b2'] for r in x['chamber_star_anchors']]==[32,324,1536,5000]

def test_pass5143_curvature():
    x=J('PART_W33_PASS5143_THETA_CURVATURE_SECOND_MOMENT.json')
    assert x['q2_exhaustive']['nonzero_words']==65535
    assert x['q2_exhaustive']['curvature_zero_words']==45
    assert x['q2_exhaustive']['curvature_zero_weight']==16
    assert x['q2_exhaustive']['minimum_positive_defect']==64
    assert x['star_anchors']['5']['second_moment']==180000

def test_pass5144_centered_rayleigh():
    x=J('PART_W33_PASS5144_CENTERED_THETA_RAYLEIGH_WEIGHT.json')
    assert x['status']=='THEOREM_CENTERED_THETA_RAYLEIGH_WEIGHT_INVERSION'
    assert [r['rho'] for r in x['chamber_star_anchors']]==['116/37','144/19','1636/139','460/29']

def test_pass5145_q4_smith():
    x=J('PART_W33_PASS5145_Q4_ROOT_COSET_SMITH.json')
    assert x['smith_nonzero']=={'1':180,'2':4}
    assert (x['rank_Q'],x['rank_F2'],x['rank_F3'])==(184,180,184)
    assert x['cokernel']=='Z^72 direct_sum (Z/2)^4'

def test_pass5146_two_step_markov():
    x=J('PART_W33_PASS5146_THETA_TWO_STEP_MARKOV_CURVATURE.json')
    assert x['status']=='THEOREM_THETA_TWO_STEP_MARKOV_CURVATURE'
    assert [r['minimum_P2'] for r in x['anchors']]==['3/8','5/16','7/24','9/32']

def test_pass5147_augmentation_hidden_defect():
    x=J('PART_W33_PASS5147_NATIVE_AUGMENTATION_DEFECT.json')
    assert [r['rank_drop'] for r in x['rows']]==[0,1,4,8,10]
    assert [r['minimum_hidden_beyond_one_explicit_relation'] for r in x['rows']]==[0,0,3,7,9]

def test_pass5148_root_stats():
    x=J('PART_W33_PASS5148_ROOT_VOLUME_DEPTH_CALCULUS.json')
    assert [(r['N_positive_roots'],r['height_sum']) for r in x['rows']]==[(3,4),(4,7),(6,16)]

def test_pass5149_cheeger_blindness():
    x=J('PART_W33_PASS5149_THETA_CHEEGER_BLINDNESS.json')
    assert x['statement'].endswith('independent of its Hamming weight.')
    assert [(r['theta_degree'],r['inside_degree'],r['outside_degree']) for r in x['anchors']]==[(8,4,4),(16,8,8),(24,12,12),(32,16,16)]

def test_consolidated_collision_firewall():
    x=J('PART_W33_PASS5142_5149_CONSOLIDATED.json')
    assert x['status']=='EXECUTED_RESULTS_FROZEN_COLLISION_RECONCILED'
    assert 'already owned' in x['collision_reconciliation']
