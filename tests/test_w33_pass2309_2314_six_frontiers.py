from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))
def test_aggregate():
 d=load('w33_pass2309_2314_six_frontiers.json')
 assert d['n_checks']==d['n_verified']==45
 assert d['critical_values']['signature_capacity_per_coordinate']==12
 assert d['critical_values']['q9_regular_kantor_intersection']==28
 assert d['critical_values']['fano_triangle']==[2,3,7]
 assert d['critical_values']['quadratic_triangle']==[2,3,2]
def test_signature_boundary():
 d=load('w33_pass2309_signature_capacity_feasibility.json')
 assert d['capacity_solution']['coordinate_sum']==[12]*45
 assert len(d['capacity_solution']['selected_signature_indices'])==9
 assert 'remain open' in d['boundary']
def test_quadratic_compiler():
 d=load('w33_pass2310_quadratic_hom_orbit_seed_compression.json')
 assert d['counts']['basis_maps']==50 and d['counts']['unique_signed_orbit_seeds']==24
 assert d['storage']['exact_cache_compression_factor']=='281/135'
def test_spread_boundaries():
 r=load('w33_pass2311_regular_spread_rank_three_obstruction.json')
 k=load('w33_pass2312_kantor_q9_symplectic_spread.json')
 assert r['divisibility']['sample_table'][2]['remainder']==700
 assert k['intersection']['common_lines']==28
def test_hardware_and_controller():
 h=load('w33_pass2313_theorem_hardware_contract.json')
 c=load('w33_pass2314_triangle_controller_bifurcation.json')
 assert h['spread_mixer']['identity']=='A^2=9I+6J'
 assert h['phase_controller']['exhaustive_transition_count']==1152
 assert c['fork']['arithmetic_triangle_signature']==[2,3,7]
 assert c['fork']['quadratic_triangle_signature']==[2,3,2]
