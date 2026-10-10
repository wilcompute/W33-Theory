"""Round34 reproducibility and honest no-go boundaries."""
from pathlib import Path
import sys,json,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261010_toe34_verified_cat_multiround_circuit as cat
import w33_20261010_toe34_p13_breakout_voltage as p13
import w33_20261010_toe34_p13_local_exact_repair as fix
import w33_20261010_toe34_spin_sl29_exact_clifford as spin
import w33_20261010_toe34_weighted_cover_dimensional_scaling as dim
import w33_20261010_toe34_c8_specific_cavity_transmon_tradeoff as c8
def frozen(name,res):
 expected=json.loads((ROOT/'data'/f'w33_20261010_toe34_{name}.json').read_text(encoding='utf-8'))
 assert res==expected
def test_full_verified_GHZ_multiround_Pauli_noise_and_time_decoder():
 r=cat.run(60);frozen('verified_cat_multiround_circuit',r)
 assert [x['logical_failures']['raw'] for x in r['outcomes']]==[0,44,58]
 assert [x['logical_failures']['joint'] for x in r['outcomes']]==[0,6,20]
 assert all(x['logical_failures']['joint']<=x['logical_failures']['raw'] for x in r['outcomes'])
def test_weighted_p13_nearmiss_is_NOT_a_cover():
 r=json.loads((ROOT/'data/w33_20261010_toe34_p13_breakout_voltage.json').read_text())
 assert r['prime']==13 and r['best_zero_holonomy_8cycles']==2
 assert not r['proven_feasible'] and not r['proven_infeasible']
 from w33_20261009_toe26_css_matching_family import wilson
 import numpy as np
 e,D,C=wilson()
 assert int(np.count_nonzero((C.astype(int)@np.asarray(r['best_voltages']))%13==0))==2
def test_exact_local_repair_neighborhood_or_grounded_yes():
 r=json.loads((ROOT/'data/w33_20261010_toe34_p13_local_exact_repair.json').read_text())
 assert r['source_prior_best_zero_cycles']==2
 assert len(r['search_neighborhoods'])>=1
 assert all(x['solver_status'] in ('OPTIMAL','FEASIBLE','INFEASIBLE','UNKNOWN') for x in r['search_neighborhoods'])
 if r['valid_p13_certificate_found']:
  from w33_20261009_toe26_css_matching_family import wilson
  import numpy as np
  e,D,C=wilson()
  assert not np.any((C.astype(int)@np.asarray(r['p13_voltages']))%13==0)
def test_exact_clifford_spinorial_SL29_double_cover_720():
 r=spin.run();frozen('spin_sl29_exact_clifford',r)
 assert r['exact_group_order']==720
 assert r['base_projective_group_order']==360
 assert r['central_negative_identity_present']
 assert r['scalar_centre_elements']=={'1':1,'-1':1}
def test_weighted_1_17_83_cover_no_decade_dimension():
 r=dim.run();frozen('weighted_cover_dimensional_scaling',r)
 assert [x['n'] for x in r['scenarios']]==[80,1360,1360,1360,6640]
 assert not any(x['has_3D_decade'] or x['has_4D_decade'] for x in r['scenarios'])
def test_specific_tunable_cavity_hardware_Kerr_survival_tradeoff():
 r=c8.run();frozen('c8_specific_cavity_transmon_tradeoff',r)
 assert math.isclose(r['minimum_r_to_reach_160MHz_Kerr'],.8)
 assert r['survival_requisite_effective_T1_us']>173
 assert all(x['largest_inherited_Kerr_MHz_at_survival_limit']<160 for x in r['parameter_grid'])
