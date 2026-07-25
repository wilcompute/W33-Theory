from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n):
 p=json.loads((ROOT/'data'/n).read_text());assert p['status']=='PASS';assert all(p['checks'].values());return p
def test_pass976_vendor_atlas():
 p=load('w33_pass976_vendor_atlas_matrices.json');assert len(p['files'])==6;assert all((ROOT/z['file']).exists() for z in p['files']);assert all(hashlib.sha256((ROOT/z['file']).read_bytes()).hexdigest()==z['expected_sha256'] for z in p['files'])
def test_pass977_h27_normalizer():
 p=load('w33_pass977_h27_normalizer_loewy_action.json');g=p['groups'];assert g['ambient_image_order']==25920;assert g['H27_order']==27;assert g['normalizer_order']==g['kernel_order']*g['normalizer_quotient_image_order'];assert p['loewy_action']['layer_dimensions']==[1,2,4,2,1]
def test_pass978_dynamic_bounds():
 p=load('w33_pass978_adaptive_game_dynamic_bounds.json');b=p['certified_value_bracket'];assert b['lower']==540.5675691787816;assert b['upper']==925.3967239366389;assert p['periodic_policy_upper_bound']['probe_counts_per_cycle']=={'reference_interferometer':2,'dark_afterpulse_monitor':1,'joint_pair_pilot':1,'shadow_science_sentinel':1}
def test_pass979_exact_mdd():
 p=load('w33_pass979_exact_phase_mdd_minimizer.json');assert p['search']['orders_scanned']==5040;assert p['minimal_MDD']['internal_nodes']==156;assert p['minimal_MDD']['total_states']==178;assert len(p['search']['optimal_orders_names'])==2
 for name,key in [('w33_phase_mdd.h','c'),('w33_phase_mdd.sv','sv'),('w33_phase_mdd_nodes.mem','nodes'),('w33_phase_mdd_children.mem','children')]:assert hashlib.sha256((ROOT/'hardware'/name).read_bytes()).hexdigest()==p['hardware']['hashes'][key]
def test_pass980_order_rigidity():
 p=load('w33_pass980_phase_automaton_order_rigidity.json');r=p['order_rigidity'];assert (r['minimum'],r['minimum_multiplicity'])==(156,2);assert (r['second_minimum'],r['second_minimum_multiplicity'])==(157,5);assert r['distinct_size_classes']==500;assert r['optimality_gap']==1
