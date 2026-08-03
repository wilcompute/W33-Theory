from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE=ROOT/'analysis/bt2757_qutrit_cx_w33_lagrangian_unipotent.py'

def load():
 spec=importlib.util.spec_from_file_location('bt2757_cx',MODULE);assert spec and spec.loader
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def test_exact_cx_certificate():
 c=load().build_certificate();assert c['all_checks_pass'];assert c['matrix_order']==3
 assert c['rank_of_M_minus_I']==2 and c['jordan_type']=='2+2'
 assert c['generator_closure']=={'generators':['F_p','F_f','S_p','S_f','CX_p_to_f'],'order':51840,'group':'Sp(4,3)'}
 assert c['unipotent_class_resolution']['classes']==[
  {'line_cycle_profile':{'1':1,'3':13},'element_count':240,'centralizer_order':216,'conjugacy_class_size':240},
  {'line_cycle_profile':{'1':7,'3':11},'element_count':480,'centralizer_order':108,'conjugacy_class_size':480}]

def test_induced_w33_cycle_profiles():
 w=load().build_certificate()['w33']
 assert w['point_cycle_profile']=={'1':4,'3':12}
 assert w['line_cycle_profile']=={'1':7,'3':11}
 assert w['flag_cycle_profile']=={'1':10,'3':50}
 assert w['edge_cycle_profile']=={'1':6,'3':78}
 assert w['fixed_line_structure']=={'fixed_lines':7,'axis_plus_external':'1 + 6','external_pencils_on_axis':[3,3],'fixed_edges':6,'fixed_edges_are_axis_K4':True}

def test_scope_firewall_present():
 c=load().build_certificate();assert 'physical' in c['scope']['not_proved']
