import base64, json, zlib
from pathlib import Path
from analysis import bt3500_3513_multicircuit_rm_biplane_a5 as packet
ROOT=Path(__file__).resolve().parents[1]

def frozen():
    path=ROOT/'data/PART_BT3500_BT3513_MULTICIRCUIT_RM_BIPLANE_A5_results.json'
    if path.exists(): return json.loads(path.read_text())
    parts=sorted((ROOT/'bootstrap/pass3500_3513').glob('results.*.zlib.b64'))
    return json.loads(zlib.decompress(base64.b64decode(''.join(p.read_text().strip() for p in parts))))

def test_exact_packet_matches_frozen_certificate():
    generated=packet.build(); saved=frozen()
    assert generated['status']=='PASS_7_FRONTS'
    assert generated['semantic_sha256']==saved['semantic_sha256']
    assert generated['checks']==saved['checks']
    assert generated['sections']['multi_circuit_radius']['live_interval']==[389,435]
    assert generated['sections']['equivariant_code_frontier']['witnesses']['8']['parameters']=='[16,5,8]'
    assert generated['sections']['compound_biplane_locator']['minimum_extra_bits']==3

def test_claim_boundaries_remain_open():
    data=packet.build()
    assert data['boundaries']['covering_radius']=='open in [389,435]'
    assert data['boundaries']['chromatic_number']=='open in {10,11}'
    assert 'open' in data['boundaries']['amplitude']
