from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def J(name):
    return json.loads((ROOT/'data'/name).read_text())

def test_pass5142_half_regular():
    x=J('PART_W33_PASS5142_THETA_HALF_REGULAR_SUPPORT.json')
    assert x['status']=='THEOREM_ALL_Q_THETA_HALF_REGULAR_SUPPORT'
    assert [x['anchors'][str(q)]['half_degree'] for q in (2,3,4,5)]==[4,8,12,16]
    assert [x['anchors'][str(q)]['theta_degree'] for q in (2,3,4,5)]==[8,16,24,32]

def test_pass5143_curvature():
    x=J('PART_W33_PASS5143_THETA_CURVATURE_SECOND_MOMENT.json')
    assert x['q2_exhaustive']['nonzero_words']==65535
    assert x['q2_exhaustive']['curvature_zero_words']==45
    assert x['q2_exhaustive']['curvature_zero_weight']==16
    assert x['q2_exhaustive']['minimum_positive_defect']==64
    assert x['star_anchors']['5']['second_moment']==180000

def test_pass5144_q7_kills_cube_guess():
    x=J('PART_W33_PASS5144_Q7_ROOT_COSET_NATIVE_RANK.json')
    assert x['ranks']=={'2':1183,'3':1183,'5':1183,'7':1173,'11':1183}
    assert x['native_rank_drop']==10 and x['guess_at_q7']==27 and x['guess_falsified']

def test_pass5145_q4_smith():
    x=J('PART_W33_PASS5145_Q4_ROOT_COSET_SMITH.json')
    assert x['smith_nonzero']=={'1':180,'2':4}
    assert (x['rank_Q'],x['rank_F2'],x['rank_F3'])==(184,180,184)
    assert x['cokernel']=='Z^72 direct_sum (Z/2)^4'

def test_pass5146_jennings():
    x=J('PART_W33_PASS5146_RANK2_JENNINGS_ROOT_HEIGHT.json')
    rows={r['type']:r for r in x['rows']}
    assert rows['A2']['height_sum']==4 and rows['A2']['group_order']==125
    assert rows['C2']['height_sum']==7 and rows['C2']['group_order']==625
    assert rows['G2']['height_sum']==16 and rows['G2']['group_order']==117649
    assert x['small_characteristic_C2_p3_layers']==[1,2,4,5,7,8,9,9,9,8,7,5,4,2,1]

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
