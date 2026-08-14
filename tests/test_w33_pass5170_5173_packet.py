from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/'data'/name).read_text())

def test_pass5170_leader29_wall():
    d=load('PART_W33_PASS5170_Q5_LEADER29_DISTANCE3_INJECTION.json')
    assert d['status']=='THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_29'
    assert d['leader_size_closed']==28 and d['adjacent_pair_cap']==48
    assert d['dense_profile_census']['N1=49']['all_rejected']
    assert d['dense_profile_census']['N1=50']['all_rejected']
    assert d['critical_branch']['integer_weight_lower_bound']==651

def test_pass5171_leader30_wall():
    d=load('PART_W33_PASS5171_Q5_LEADER30_P4_DELSARTE_COUPLING.json')
    assert d['status']=='THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_30'
    assert d['leader_size_closed']==29
    assert d['conditioned_branches']['leaf_free_(0,8,14)']['integer_weight_lower_bound']==715
    assert d['conditioned_branches']['three_leaf_(3,5,15)']['integer_weight_lower_bound']==630

def test_pass5172_incidence_bridge():
    d=load('PART_W33_PASS5172_ALLQ_INCIDENCE_N2_SPECTRAL_BRIDGE.json')
    assert d['status']=='THEOREM_ALL_Q_LEVI_INCIDENCE_N2_SPECTRAL_BRIDGE'
    assert d['exact_identity']=='N2 = x^T N y - (m+2 N1)'
    assert max(x[2] for x in d['q5_m30_N1_51_split_bounds'])==140
    assert max(x[2] for x in d['q5_m30_N1_52_split_bounds'])==141

def test_pass5173_leader31_wall():
    d=load('PART_W33_PASS5173_Q5_LEADER31_SHARP_P5_EXTENSION.json')
    assert d['status']=='THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_31'
    assert d['leader_size_closed']==30
    assert d['pair_only_N1_le_40_lower']==776
    assert d['generic_uniform_bounds']['N1=50']==827
    assert d['dense_N1_51']['uniform_lower_bound']==794
    assert d['dense_N1_52']['uniform_lower_bound']==760

def test_shared_manuscript_insert_and_public_card():
    manifest=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
    assert r'\input{analysis/PASS5170_5173_q5_geodesic_incidence_insert}' in manifest
    insert=(ROOT/'analysis/PASS5170_5173_q5_geodesic_incidence_insert.tex').read_text()
    assert 'leader at least $31$' in insert
    card=(ROOT/'analysis/PASS5170_5173_index_insert.html').read_text()
    assert 'leader ≥31' in card
