#!/usr/bin/env python3
"""Fail-closed verifier for Passes 2309--2314."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AGG=ROOT/'data/w33_pass2309_2314_six_frontiers.json'
EXPECTED='cac7fad2fbe255a89c4314d9f35b86fc814f2e091333407b300908a64fe276c0'
FILES={
'2309':'data/w33_pass2309_signature_capacity_feasibility.json',
'2310':'data/w33_pass2310_quadratic_hom_orbit_seed_compression.json',
'2311':'data/w33_pass2311_regular_spread_rank_three_obstruction.json',
'2312':'data/w33_pass2312_kantor_q9_symplectic_spread.json',
'2313':'data/w33_pass2313_theorem_hardware_contract.json',
'2314':'data/w33_pass2314_triangle_controller_bifurcation.json'}
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 a=json.loads(AGG.read_text());assert a['sha256_without_hash_field']==EXPECTED==digest(a)
 total=0
 for p,path in FILES.items():
  d=json.loads((ROOT/path).read_text());assert d['sha256_without_hash_field']==a['certificates'][p]==digest(d)
  assert all(d['checks'].values());total+=len(d['checks'])
 assert total==a['n_checks']==a['n_verified']==45
 c=a['critical_values'];assert c['signature_capacity_per_coordinate']==12
 assert c['quadratic_basis_maps']==50 and c['quadratic_unique_orbit_seeds']==24
 assert c['rank_three_possible_odd_q_under_formula']==[3,5]
 assert c['q9_regular_kantor_intersection']==28 and c['hardware_phase_transitions']==1152
 assert c['fano_triangle']==[2,3,7] and c['quadratic_triangle']==[2,3,2]
 print(json.dumps({'status':a['status'],'certificate':EXPECTED,'checks':total},sort_keys=True))
if __name__=='__main__':main()
