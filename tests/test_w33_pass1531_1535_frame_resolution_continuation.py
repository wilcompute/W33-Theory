from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data'/'w33_pass1531_1535_frame_resolution_continuation.json'
def load():return json.loads(CERT.read_text(encoding="utf-8"))
def test_release_status_and_boundaries():
 c=load();assert c['status']=='PASS_WITH_OPEN_RESOLUTION'
 assert c['pass1531_resolution_cnf']['status']=='FORMULATED_OPEN'
 assert c['pass1531_resolution_cnf']['variables']==4860
 assert c['pass1531_resolution_cnf']['clauses']==99909
 assert c['pass1533_cover_frontier_audit']['frozen_frontier']['certified_cover_lower_bound']==3547800
 assert 'not a global completeness theorem' in c['pass1533_cover_frontier_audit']['boundary']
def test_module_and_bridge_dimensions():
 c=load();m=c['pass1532_module_fingerprint'];b=c['pass1535_frame_harmonic_bridge']
 assert m['psp']['minus4_block_multiplicities']==[64,60,81,15,20,60,15]
 assert sorted(m['pgsp']['minus4_block_multiplicities'])==[15,15,20,60,60,64,81]
 assert b['status']=='PASS' and b['ranks']=={'P4':81,'bridge':81,'d1':39,'d2':120,'harmonic':81}
 assert all(b['checks'].values())
def test_four_packing_affine_shell():
 c=load()['pass1534_four_packing_simplex'];assert c['status']=='PASS'
 assert c['projection']['norm_squared']=='16/3'
 assert c['integral_shell']['z_norm_squared']==48
 assert c['integral_shell']['exists'] is False
