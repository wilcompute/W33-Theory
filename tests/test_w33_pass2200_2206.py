import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def test_all_q_regular_spread_certificate():
 m=load('p2201','analysis/w33_pass2201_all_q_regular_spread_scheme.py')
 assert m.build()==json.loads((ROOT/'data/w33_pass2201_2202_all_q_regular_spread_scheme.json').read_text(encoding="utf-8"))

def test_ree_tits_nonregular_certificate():
 m=load('p2203','analysis/w33_pass2203_ree_tits_nonregular_control.py')
 d=m.build();assert d==json.loads((ROOT/'data/w33_pass2203_ree_tits_nonregular_control.json').read_text(encoding="utf-8"))
 assert d['intersection_values_outside_regular_scheme']==[19,37,46,55]

def test_controller_and_quadratic_correction():
 m=load('p2204','analysis/w33_pass2200_2204_2205_quadratic_controller_audit.py')
 d=m.build();assert d==json.loads((ROOT/'data/w33_pass2200_2204_2205_quadratic_controller_audit.json').read_text(encoding="utf-8"))
 assert d['controller']['image']=='D24=C12:C2 of order 24'
 assert d['quadratic_Hom_correction']['corrected_actual_signed_edge_targets']['Lambda2_90']['24']==0

def test_rtl_reference():
 m=load('p2206','analysis/w33_pass2206_verify_rtl.py')
 d=m.build(ROOT/'rtl/w33_pass2773_spread_mixer36_synth.sv')
 assert d==json.loads((ROOT/'data/w33_pass2206_rtl_reference.json').read_text(encoding="utf-8"))
 assert d['checks']['A2_equals_9I_plus_6J']
 assert d['source']=='rtl/w33_pass2773_spread_mixer36_synth.sv'
