import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/'data'/name).read_text())

def test_root_derivative_packet():
    d=load('PART_W33_PASS5090_5094_5097_ROOT_DERIVATIVE_GEOMETRY.json')
    assert d['5090']['q3_anchor']['support']==81
    assert d['5090']['q3_anchor']['active_charts']==108
    assert d['5094']['distance_shells']==[1,8,32,40]
    assert d['5095']['q3']==[9,9,9,9,27,81]
    assert d['5097']['graph_automorphism_group_order']==324

def test_q4_local_rigidity():
    d=load('PART_W33_PASS5091_Q4_LOCAL_MINIMUM_CUT_RIGIDITY.json')
    assert d['seed_count']==16
    assert d['sat_chamber_stars']==8
    assert d['unsat_seeds']==8
    assert 'heavier 2|3' in d['consequence']

def test_sqrt17_integral_bridge():
    d=load('PART_W33_PASS5092_SQRT17_INTEGRAL_ORDER_BRIDGE.json')
    assert d['det_P']==1
    assert d['maximal_order_discriminant']==17
    assert d['q3_suborder_index']==4
    assert d['q3_suborder_discriminant']==272

def test_v24_smith_floor_exchange():
    d=load('PART_W33_PASS5093_V24_SMITH_FLOOR_EXCHANGE_RIGIDITY.json')
    assert d['smith_floor']['inverse_denominator']==780
    assert d['one_row_exchange']['full_rank_candidates']==3289
    assert d['one_row_exchange']['D780_neighbors']==8
    assert d['one_row_exchange']['neighbors'][0]['condition_2']>d['smith_floor']['condition_2']
