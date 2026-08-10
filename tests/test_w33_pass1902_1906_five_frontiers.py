from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n):return json.loads((ROOT/'data'/n).read_text(encoding="utf-8"))
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def test_frozen_certificates():
 for n in ['w33_pass1902_u6_component_reduction.json','w33_pass1903_mixed_separator_tensor_reduction.json','w33_pass1904_gaussian_v9_lattice.json','w33_pass1905_phase_subgroup_poset.json','w33_pass1906_c4_twisted_ihara.json']:
  d=load(n);assert d['sha256_without_hash_field']==digest(d);assert all(d['checks'].values())
def test_critical_values():
 d=load('w33_pass1902_u6_component_reduction.json');assert sum(d['equal_syndrome_collision_edges_by_difference_weight'].values())==1724138884380 and d['weight12_disjoint_edges_invisible_to_every_coordinate_chart']==412008338280
 d=load('w33_pass1903_mixed_separator_tensor_reduction.json');assert sum(d['coordinate_factors'].values())==240
 d=load('w33_pass1904_gaussian_v9_lattice.json');assert(d['minimum_hermitian_norm'],d['minimal_vectors'],d['unitary_automorphism_group_order'])==(24,60,2880)
 d=load('w33_pass1905_phase_subgroup_poset.json');assert next(r for r in d['rows'] if r['subgroup']=='PSp(4,3)')['canonical_90_up_to_sign']
 d=load('w33_pass1906_c4_twisted_ihara.json');assert d['character_dimensions']==[26,20,24,20] and d['primitive_unoriented_reduced_cycles']['24']==703650
