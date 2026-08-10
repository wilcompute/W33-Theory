import base64,json,sys,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from analysis import bt3556_3569_radius_amplitude_code_fault_c5 as packet
CACHE=None
EXPECTED='39a20ba02e9e28b77414e5e1236d2f58f9fb457a6ed2a610bab03fe74a9dadb3'

def generated():
    global CACHE
    if CACHE is None:CACHE=packet.certificate()
    return CACHE

def frozen_fallback():
    parts=sorted((ROOT/'bootstrap/pass3556_3569').glob('results.legacy.*.zlib.b64'))
    assert len(parts)==2
    saved=json.loads(zlib.decompress(base64.b64decode(''.join(p.read_text(encoding="utf-8").strip() for p in parts))))
    assert saved['schema']=='w33.pass3542_3555.radius_amplitude_code_fault_c5.v1'
    saved['schema']='w33.pass3556_3569.radius_amplitude_code_fault_c5.v1'
    saved['semantic_sha256']=packet.semantic_hash(saved)
    return saved

def test_exact_packet_matches_renamespaced_frozen_fallback():
    data=generated();saved=frozen_fallback()
    assert data==saved
    assert data['status']=='PASS_7_FRONTS'
    assert data['semantic_sha256']==EXPECTED
    assert data['sections']['relation_plane_radius']['new_circuit_weight']==263
    assert data['sections']['relation_plane_radius']['rank_three_heavy_pilot']['triples_exhausted']==41664
    assert data['sections']['compound_fault_distance']['new_twenty_one_bit_minimum_distance']==3
    assert data['sections']['rank20_subgroup_atlas']['atlas']['C5']['isomorphic']

def test_boundaries_remain_fail_closed():
    data=generated()
    assert data['live_boundaries']['covering_radius']=='open in [389,435]'
    assert data['live_boundaries']['chromatic_number']=='open in {10,11}'
    assert 'open' in data['live_boundaries']['amplitude']
