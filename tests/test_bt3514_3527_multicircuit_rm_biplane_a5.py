import base64, json, zlib
from pathlib import Path
from analysis import bt3514_3527_multicircuit_rm_biplane_a5 as packet
ROOT=Path(__file__).resolve().parents[1]
GENERATED=None

def generated():
    global GENERATED
    if GENERATED is None:
        GENERATED=packet.build()
    return GENERATED

def frozen():
    path=ROOT/'data/PART_BT3514_BT3527_MULTICIRCUIT_RM_BIPLANE_A5_results.json'
    if path.exists(): return json.loads(path.read_text())
    parts=sorted((ROOT/'bootstrap/pass3514_3527').glob('results.*.zlib.b64'))
    return json.loads(zlib.decompress(base64.b64decode(''.join(p.read_text().strip() for p in parts))))

def test_exact_packet_matches_frozen_certificate():
    data=generated(); saved=frozen()
    assert data['status']=='PASS_7_FRONTS'
    assert data['semantic_sha256']==saved['semantic_sha256']
    assert data['checks']==saved['checks']
    assert data['sections']['multi_circuit_radius']['live_interval']==[389,435]
    assert data['sections']['equivariant_code_frontier']['witnesses']['8']['parameters']=='[16,5,8]'
    assert data['sections']['compound_biplane_locator']['minimum_extra_bits']==3

def test_claim_boundaries_remain_open():
    data=generated()
    assert data['boundaries']['covering_radius']=='open in [389,435]'
    assert data['boundaries']['chromatic_number']=='open in {10,11}'
    assert 'open' in data['boundaries']['amplitude']
