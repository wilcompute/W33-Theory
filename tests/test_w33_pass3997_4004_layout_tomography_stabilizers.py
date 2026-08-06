import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def test_layout_tomography_certificate():
 p=load('data/PART_3997_4004_LAYOUT_TOMOGRAPHY_EDGE_MEMORY.json')
 assert p['semantic_sha256']=='ed4eddab150575ec2a719bc55974ac24e0b1852b1a3bec4a08204bc9114f4960'
 assert p['layout_competition']['direct_40_mode']['perfect_matching_layers']==12
 assert p['layout_competition']['incidence_80_mode']['perfect_matching_layers']==4
 assert p['bonkers_edge_carrier_memory']['dark_cycle_dimension']==201
 assert all(3.8<x<4.2 for x in p['wigner_smith_tomography']['successive_error_ratios'])
def test_stabilizer_certificate():
 p=load('data/PART_4001_CODE_STABILIZER_IDENTIFICATION.json')
 assert p['semantic_sha256']=='2bb684e7fcbfc8ca00e233c4955fc7a985c8aada6791c932599db10b4287598c'
 assert [x['stabilizer_order'] for x in p['records']]==[96,192,384]
 assert p['records'][0]['identified_group']=='S4 x V4'
 assert p['records'][2]['identified_group'].endswith('W(B4)')
