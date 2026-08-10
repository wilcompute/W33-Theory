from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(n):
 p=next((ROOT/'data').glob(f'w33_pass{n}_*.json'))
 return json.loads(p.read_text(encoding="utf-8"))

def test_pass553_core_geometry():
 p=load(553); assert p['status']=='PASS'
 assert p['automorphisms']['order']==120
 assert p['automorphisms']['component_image_order']==10

def test_pass554_memory_automaton():
 p=load(554); assert p['status']=='PASS'
 assert [x['distinct_charpolys'] for x in p['layers']]==[13,26,96,336,921]
 assert [x['minimal_markov_states'] for x in p['minimal_future_automaton']['layers']]==[41,122,365,1081,921]

def test_pass555_fibre_catalog():
 p=load(555); assert p['status']=='PASS'
 assert p['catalog_custody']['fibre_count']==98 and len(p['type_counts'])==5
 assert p['five_cube_result']['count']==3

def test_pass556_control_plane():
 p=load(556); assert p['status']=='PASS'
 assert p['quartic_readout']['target_level_size']==80
 assert p['odd_switch_test']['same_quartic_invariant']
 assert p['odd_switch_test']['A_product_mod5']!=p['odd_switch_test']['B_product_mod5']

def test_pass557_formal_support():
 p=load(557); assert p['status']=='PASS'
 assert p['formalized']['periods_first7']==[312,1560,1560,7800,7800,39000,39000]

def test_combined_release():
 p=json.loads((ROOT/'data'/'w33_pass553_557_intrinsic_automaton_formal_control_release.json').read_text(encoding="utf-8"))
 assert p['status']=='PASS'
 assert p['owner_check_total']==56
 assert all(p['release_checks'].values())
