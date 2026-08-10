import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n):return json.loads((ROOT/'data'/n).read_text(encoding="utf-8"))
def test_pass596_connection_family():
 p=load('w33_pass596_connection_universality.json');assert p['status']=='PASS';assert p['wilson_values']==[-168,-84,56,112];assert all(r['holonomy_order']==120 for r in p['records'])
def test_pass597_twisted_torsion():
 p=load('w33_pass597_twisted_singer_torsion.json');assert p['status']=='PASS';assert p['five_primary_smith']['elementary_divisors']=={'5':9,'25':3};assert p['cyclotomic_DVR_bridge']['lambda_valuation_after_scalar_extension']==60
def test_pass598_outer_automorphism():
 p=load('w33_pass598_s6_outer_automorphism.json');assert p['status']=='PASS';assert p['outer_action']['image_order']==720;assert p['outer_action']['transposition_image_cycle_type']==[2,2,2]
def test_pass599_deep_anchor_no_go():
 p=load('w33_pass599_600cell_singer_axis_transport.json');assert p['status']=='PASS';assert p['six_axis_transport']['geometric_A5_order']==60;assert p['deep_anchor_test']['globally_fixed_axes']==[]
def test_pass600_photonic_compiler():
 p=load('w33_pass600_photonic_wilson_compiler.json');assert p['status']=='PASS';assert [r['switch_count'] for r in p['compiled_classes']]==[0,2,3,4];assert len(p['falsifier']['decision_table'])==4
