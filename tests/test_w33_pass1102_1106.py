import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))
def test_release_total():
 r=load('w33_pass1102_1106_release.json');assert r['status']=='PASS';assert r['total_exact_checks']==86
def test_clifford_matrices():
 x=load('w33_pass1102_ctbllib_clifford_naming.json');assert x['status']=='PASS';assert len(x['restriction_matrix_outer_to_inner'])==10;assert x['checks']['steinberg_induction_exact']
def test_full_firewall_transport():
 x=load('w33_pass1103_hesse_firewall_cubic_transport.json');assert x['status']=='PASS';assert len(x['records'])==9;assert x['firewall_support']['deleted_internal_edges']==27;assert x['fiber_cubic_sign_distribution']=={'plus':2,'minus':7}
def test_e8_pair_carriers():
 x=load('w33_pass1104_e8_pair_carrier_census.json');assert x['first_any_steinberg']['degree']==3360;assert x['first_any_steinberg']['multiplicity_81_minus']==4;assert x['first_81_plus']['degree']==15120;assert x['first_81_plus']['multiplicity_81_plus']==1
def test_keysight_fail_closed():
 x=load('w33_pass1105_keysight_n7731a_transport.json');assert x['status']=='PASS';assert x['receipt']['processed_commands']==240;assert x['receipt']['physical_hardware_connected'] is False;assert all(x['negative_probes'].values())
def test_formal_lock_and_parallel_baseline():
 x=load('w33_pass1106_formal_clifford_firewall_carrier.json');assert x['status']=='PASS';assert x['parallel_observed_baseline']['commit'].startswith('7bd164a');src=(ROOT/'formal/W33/Pass1106CliffordFirewallCarrier.lean').read_text(encoding="utf-8");assert 'native_decide' not in src;assert 'rootLine3360_contains_four_81Minus' in src
def test_all_pass_ledgers_sum_to_release():
 names=['w33_pass1102_ctbllib_clifford_naming.json','w33_pass1103_hesse_firewall_cubic_transport.json','w33_pass1104_e8_pair_carrier_census.json','w33_pass1105_keysight_n7731a_transport.json','w33_pass1106_formal_clifford_firewall_carrier.json'];xs=[load(n) for n in names];assert all(x['status']=='PASS' for x in xs);assert sum(x['check_count'] for x in xs)==86
