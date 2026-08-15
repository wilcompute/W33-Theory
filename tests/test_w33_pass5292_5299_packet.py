import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R=json.loads((ROOT/'data/PART_W33_PASS5292_5299_RESULTS.json').read_text())

def test_q9_moment_distance():
    p=R['5292']
    assert p['dual16_orbit_size']==13_450_050
    assert p['coordinate_replication']==64_800
    assert p['maximum_pair_codegree']==810
    assert 1+p['coordinate_replication']//p['maximum_pair_codegree']==81
    assert p['footprint_code']=='[3321,369,81]_2'

def test_allodd_rank_anchors_and_equivalence():
    p=R['5293'];assert p['rank_equality_anchors']=={'q3':15,'q5':65,'q7':175,'q9':369,'q11':671}
    assert p['q11']['rank_F2']==11*(11*11+1)//2
    assert 'iff' in p['equivalence']

def test_hoffman_triples_all_40():
    p=R['5294'];assert p['cover_stabilizer_order']==576
    assert sum(x['orbit_size'] for x in p['triple_orbits'])==286
    assert {x['minimum'] for x in p['triple_orbits']}=={40}

def test_fiber_and_shell():
    assert R['5296']['image_order']==60
    assert R['5296']['PG3_2_line_orbit_sizes']==[5,10,10,10]
    p=R['5298'];assert p['minimum_words']==2340 and p['GF2_span_rank']==p['K0_dimension']==560
    assert sum(p['fixed_word_distance_distribution'].values())==2339

def test_relation_count_q5():
    p=R['5299'];assert 'g-1' in p['relation_dimension']
    assert '624 local dimensions - 64 relations = 560-dimensional K0'==p['q5']
