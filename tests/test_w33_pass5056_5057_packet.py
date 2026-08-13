from __future__ import annotations
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(name): return json.loads((R/'data'/name).read_text())
def test_q4_anchor():
 d=load('PART_W33_PASS5056_Q4_THETA_APARTMENT_CODE.json')
 assert d['status']=='PASS' and d['q']==4
 assert d['geometry']['points']==85 and d['geometry']['lines']==85 and d['geometry']['chambers_flags']==425
 assert d['apartments']==13600 and d['apartment_cycle_rank_f2']==256
 assert d['theta_checks']==54400 and d['theta_check_rank_f2']==13344 and d['theta_checks_per_apartment']==12
 assert d['theta_checks_span_full_dual'] and d['distance_milp']['objective']==256 and d['distance_milp']['mip_gap']==0.0
 assert d['code']==[13600,256,256]
def test_local_cutspace():
 d=load('PART_W33_PASS5057_LOCAL_THETA_CUTSPACE.json')
 q4=next(x for x in d['checked_local_q'] if x['q']==4)
 assert q4['theta_relation_rank']==6 and q4['theta_kernel_dimension']==4 and q4['nonzero_cut_weights']==[4,6]
 w=d['q4_chamber_star'];assert w['support_weight']==256 and w['active_opposite_point_charts']==128 and w['active_opposite_line_charts']==128
 assert all(x['minimum_nonzero_local_weight']==x['q'] for x in d['checked_local_q'])
def test_family_continuity():
 old=load('PART_W33_PASS5051_Q_FAMILY_THETA_CODE.json');new=load('PART_W33_PASS5056_Q4_THETA_APARTMENT_CODE.json')
 assert old['q2']['code']==[90,16,16] and old['q3']['code']==[1620,81,81] and new['code']==[13600,256,256]
 assert [old['q2']['checks_per_apartment'],old['q3']['checks_per_apartment'],new['theta_checks_per_apartment']]==[4,8,12]
