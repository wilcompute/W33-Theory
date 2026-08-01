#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={1902:ROOT/'data/w33_pass1902_u6_component_reduction.json',1903:ROOT/'data/w33_pass1903_mixed_separator_tensor_reduction.json',1904:ROOT/'data/w33_pass1904_gaussian_v9_lattice.json',1905:ROOT/'data/w33_pass1905_phase_subgroup_poset.json',1906:ROOT/'data/w33_pass1906_c4_twisted_ihara.json'}
EXPECTED={1902:'e87f04873830013a8d096382c46ec5b893c30371d2667588fbdb811d899a182c',1903:'84ce30a07f908c37049667fb62c91910f8e78fec66edbd13a973511de65981d4',1904:'59e15d48db8e98360272fca4590baf15d34c2df059a9917721def6592679a9f0',1905:'9e5e9c5db2490c6a6b44e6c34378da013354eb4c8dbbf5d7d08a8522e8997652',1906:'75265b602abbd6c5f32fced554a0e4d3e879054eed50401ea10a44ce9d174be6'}
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d={p:json.loads(f.read_text()) for p,f in FILES.items()}
 for p,x in d.items():assert x['sha256_without_hash_field']==EXPECTED[p]==digest(x) and all(x['checks'].values())
 assert d[1902]['equal_syndrome_collision_edges_total']==1724138884380 and d[1902]['weight12_disjoint_edges_invisible_to_every_coordinate_chart']==412008338280
 assert d[1903]['coordinate_factors']=={'residual_triples':20,'pair_factors':180,'phase_triples':40}
 assert d[1904]['minimum_hermitian_norm']==24 and d[1904]['minimal_vectors']==60 and d[1904]['unitary_automorphism_group_order']==2880
 assert next(r for r in d[1905]['rows'] if r['subgroup']=='PSp(4,3)')['canonical_90_up_to_sign'] is True
 assert d[1906]['character_dimensions']==[26,20,24,20] and d[1906]['primitive_unoriented_reduced_cycles']['24']==703650
 n=sum(len(x['checks']) for x in d.values());assert n==33
 out={'status':'PASS_WITH_U6_MIXED_AND_FULL_SUBGROUP_BOUNDARIES','n_verified':n,'n_checks':n,'certificates':EXPECTED};out['aggregate_sha256']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest();print(json.dumps(out,indent=2));return out
if __name__=='__main__':main()
