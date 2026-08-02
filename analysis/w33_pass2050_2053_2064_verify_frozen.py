#!/usr/bin/env python3
"""Fail-closed verifier for Passes 2050--2053 and 2064."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={
 '2050':ROOT/'data/w33_pass2050_full_group_orbit_cover_fusion.json',
 '2051':ROOT/'data/w33_pass2051_explicit_quadratic_intertwiners.json',
 '2052':ROOT/'data/w33_pass2052_integrated_geometry_hardware_prototype.json',
 '2053':ROOT/'data/w33_pass2053_exact_spread_graph_identification.json',
 '2064':ROOT/'data/w33_pass2064_regular_spread_rank3_family_q357.json'}
EXPECTED={'2050':'ee62a332676deabb198367161800e467bb8a09e3694ca1c448d9fe45d20c0663','2051':'8ab0957d202b517e7ee8104f2c180e986607074c746d5643b76f8f066f70d3dc','2052':'975e159ffaca69b2c4ad488f5b3552fe7780c3b017fc29c94194013956bd5e42','2053':'2f92d0f61995a4355167902fef4ae30da2e3ecf7758a9047ae3e9e1b1c3cd6d7','2064':'28c28d5078aa495c3022a6a6153b0e83d55a70a9160179c15cd23a4d8a25a60e'}
AGG='627bb254b3d33d35acc263c1640f8181d255a7fdf82087d06abfc2ffef4c6867'
WIT='9070764d14ea9bd25134a5b606a3743f7883c51e91730396dea9eebab6236028'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d={k:json.loads(v.read_text()) for k,v in FILES.items()}
 for k,z in d.items():
  assert z['sha256_without_hash_field']==EXPECTED[k]==digest(z),k
  assert all(z['checks'].values()),k
 assert sum(len(z['checks']) for z in d.values())==77
 assert d['2050']['full_group_fusion']['full_group_subgroup_types']==14
 assert d['2050']['canonical_first_witnesses']['full_group_schedule_orbits']==12
 assert len(d['2051']['maps'])==7 and d['2051']['maps']['SJ81_J_twist']['rank']==81
 assert d['2052']['components']['d8_orbit_scheduler']['covered_edges']==240
 assert d['2053']['identification']['name']=='NO_6^-(2) graph'
 assert d['2053']['graph']['modular_adjacency_ranks']=={'2':36,'3':15,'5':35,'7':36}
 assert [d['2064']['complete_finite_results'][q]['spreads'] for q in ('3','5','7')]==[36,300,1176]
 wit=json.loads((ROOT/'data/w33_pass2012_d8_orbit_parallel_class_witness.json').read_text())
 assert wit['sha256_without_hash_field']==WIT==digest(wit)
 assert wit['frame_count']==60 and wit['edge_multiplicity_profile']=={'1':240}
 a=json.loads((ROOT/'data/w33_pass2050_2053_2064_five_frontiers.json').read_text())
 assert a['sha256_without_hash_field']==AGG==digest(a)
 assert a['certificates']==EXPECTED and a['n_checks']==a['n_verified']==77
 out={'status':a['status'],'n_checks':77,'n_verified':77,'certificates':EXPECTED,'aggregate_sha256':AGG,'witness_sha256':WIT}
 print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=='__main__':main()
