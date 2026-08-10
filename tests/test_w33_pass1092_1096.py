import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'
def load(n):return json.loads((D/n).read_text(encoding="utf-8"))
def test_release_total():
 ds=[load(f'w33_pass{p}_{n}.json') for p,n in [(1092,'u42dot2_character_identification'),(1093,'dual_hesse_firewall_fiber_equivalence'),(1094,'e8_root_sheet_bridge'),(1095,'vendor_controller_adapter'),(1096,'formal_character_hesse_e8_lock')]]
 assert all(x['status']=='PASS' and all(x['checks'].values()) for x in ds)
 assert sum(x['check_count'] for x in ds)==75
def test_character_and_clifford():
 d=load('w33_pass1092_u42dot2_character_identification.json')
 assert d['group']['class_count']==25 and d['documented_vector_matches_component']=='15a'
 assert d['restriction_U42dot2_to_U42']['60b']=={'30a':1,'30b':1}
 assert d['induction_U42_to_U42dot2']['81']=={'81_minus':1,'81_plus':1}
def test_hesse_fibers():
 d=load('w33_pass1093_dual_hesse_firewall_fiber_equivalence.json')
 assert d['group_reading']['order']==216 and len(d['explicit_equivariant_mapping'])==9
 assert {tuple(x['firewall_fiber_u']) for x in d['explicit_equivariant_mapping']}=={(a,b) for a in range(3) for b in range(3)}
def test_e8_obstruction():
 d=load('w33_pass1094_e8_root_sheet_bridge.json')
 assert d['decision']['equivariant_bridge_exists'] is False
 for carrier in d['constituent_inner_products'].values(): assert carrier['81_plus']==carrier['81_minus']==0
def test_vendor_adapter():
 d=load('w33_pass1095_vendor_controller_adapter.json')
 assert d['checks']['dry_run_never_opens_socket'] and d['checks']['unarmed_acquisition_fails_closed']
 assert d['receipt']['physical_hardware_connected'] is False
def test_formal_lock():
 d=load('w33_pass1096_formal_character_hesse_e8_lock.json');s=(ROOT/'formal/W33/Pass1096CharacterHesseE8Lock.lean').read_text(encoding="utf-8")
 assert d['status']=='PASS' and s.count('no_81')==4 and 'minus_is_sign_twist' in s
def test_gap_companion_and_hardware_receipt():
 assert 'CharacterTable("U4(2).2")' in (ROOT/'analysis/w33_pass1092_u42dot2_character_match.g').read_text(encoding="utf-8")
 assert (ROOT/'hardware/w33_pass1095_vendor_adapter_receipt.json').exists()
