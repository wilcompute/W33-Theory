import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_pass5284_5291_frozen_results():
    d=json.loads((ROOT/'data/PART_W33_PASS5284_5291_RESULTS.json').read_text())
    assert d['status']=='EXECUTED_WITH_HOFFMAN_SHORTENING_AND_ALLODD_EQUALITY_OPEN'
    assert d['5284']['fixed_support_kernel_dimension']==4
    assert d['5284']['complete_block_minimum_words']==2340
    assert d['5284']['apartment_weight']==1000
    assert d['5285']['coordinate_types']=={'(6,5,2)':144,'(6,6,1)':96,'(6,3,4)':48,'(6,1,6)':24}
    assert d['5286']['q7']['ambient_stabilizer']==72
    assert d['5287']['rank_F2']==369
    assert len(d['5287']['dual16_witness'])==16
    assert d['5288']['equality_anchors']=={'q3':15,'q5':65,'q7':175,'q9':369}
    assert d['5289']['projective_fiber']=='PG(3,2)'
    assert d['5290']['zero_extended_restricted_code']=='[5625,4,1000]_2'
    assert d['5291']['pairwise_distance']==1000
    assert d['strict_frontier']['q5_apartment_code']=='[73125,625,625]_2'


def test_frontier_manifest_carries_full_distance_and_postdistance():
    s=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
    assert 'PASS5262_5269_q5_full_distance_block_shell_insert' in s
    assert 'PASS5284_5291_postdistance_bundle_q9_insert' in s


def test_simplex_arithmetic():
    # Local 4D constant-weight fiber: 15 nonzero column types x5 plus 150 zero.
    assert 15*5+150==225
    assert 8*5==40
    # 25 diagonal copies.
    assert 15*125+3750==5625
    assert 8*125==1000
    assert 156*15==2340
