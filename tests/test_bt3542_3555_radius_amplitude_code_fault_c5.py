import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from analysis import bt3542_3555_radius_amplitude_code_fault_c5 as packet
CACHE=None

def generated():
    global CACHE
    if CACHE is None:CACHE=packet.certificate()
    return CACHE

def frozen():
    return json.loads((ROOT/'data/PART_BT3542_BT3555_RADIUS_AMPLITUDE_CODE_FAULT_C5_results.json').read_text())

def test_exact_packet_matches_frozen_certificate():
    data=generated();saved=frozen()
    assert data['status']=='PASS_7_FRONTS'
    assert data['semantic_sha256']==saved['semantic_sha256']
    assert data['checks']==saved['checks']
    assert data['sections']['relation_plane_radius']['new_circuit_weight']==263
    assert data['sections']['relation_plane_radius']['rank_three_heavy_pilot']['triples_exhausted']==41664
    assert data['sections']['compound_fault_distance']['new_twenty_one_bit_minimum_distance']==3
    assert data['sections']['rank20_subgroup_atlas']['atlas']['C5']['isomorphic']

def test_boundaries_remain_fail_closed():
    data=generated()
    assert data['live_boundaries']['covering_radius']=='open in [389,435]'
    assert data['live_boundaries']['chromatic_number']=='open in {10,11}'
    assert 'open' in data['live_boundaries']['amplitude']
