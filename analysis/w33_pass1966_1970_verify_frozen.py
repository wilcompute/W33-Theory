#!/usr/bin/env python3
"""Fail-closed verifier for Passes 1966--1970."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={1966:ROOT/'data/w33_pass1966_combined_spread_signature_geometry.json',1967:ROOT/'data/w33_pass1967_forty_generator_scaling.json',1968:ROOT/'data/w33_pass1968_internal_mu6_structural_role.json',1969:ROOT/'data/w33_pass1969_backward_constraint_audit.json',1970:ROOT/'data/w33_pass1970_spread_obstruction_referee_draft.json'}
EXPECTED={1966:'e7ccf82c72ca62601a3301b105b83547ba868f43443ca04a27d2b8d4ef2bf85c',1967:'0e262c3ea8a33b813c3cd45f54643a2129e6e319efd6b511f50a4cce3bc1ee28',1968:'52ac1546c8d3547e7a4a1895ccb2c6d82be3c7e4cfb3672bc78cdc48ef087a7d',1969:'450387a032d23659524b34201032e5302bbe002705a40825ce466e284f8b6ac7',1970:'60752096f72d1352652d712275586c64089bbbbc7f42545fb38615f2f5183410'}
AGG='022ebdfa6cbd3a5ce9dfb87bc261cc57239ac226754c4a82fdfdc7ac84e2723a'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d={p:json.loads(f.read_text()) for p,f in FILES.items()}
 for p,z in d.items():
  assert z['sha256_without_hash_field']==EXPECTED[p]==digest(z),p
  assert all(z['checks'].values()),p
 assert d[1966]['exact_nonvacuity_witness']['survivors_after_40_cuts']==807
 assert d[1966]['model']['constraints_with_40_cuts']==3073
 assert d[1967]['linear_independence']['ranks']['40']==40
 assert d[1967]['orbit_scaling']['milestones']['8']==3244
 assert d[1968]['centralizer']['unique_odd_sylow']=='C3=<mu6^2>'
 assert d[1968]['chirality_normalizer']['generated_finite_group']=='C6 semidirect C2 = D12'
 assert d[1968]['sector_action']['nontrivial_power_common_fixed_space_dimension']==150
 assert d[1969]['exact_replays']['plus8_pair']=={'after':81,'before':81,'constraint':'x<=y+8 over x,y in 0..8'}
 assert d[1969]['exact_replays']['spread_cap_counterexample']['certified_attained']==13
 assert d[1969]['status']=='PASS_WITH_TWO_LEGACY_REPLAYS_UNLOCATED'
 assert d[1970]['draft_structure']['open_problems']==5
 assert d[1970]['artifact']['path']=='analysis/W33_SPREAD_OBSTRUCTION_REFEREE_DRAFT.tex'
 n=sum(len(z['checks']) for z in d.values());assert n==35
 a=json.loads((ROOT/'data/w33_pass1966_1970_five_frontiers.json').read_text())
 assert a['sha256_without_hash_field']==AGG==digest(a)
 assert a['certificates']=={str(k):v for k,v in EXPECTED.items()}
 assert a['n_checks']==a['n_verified']==n
 out={'status':a['status'],'n_checks':n,'n_verified':n,'certificates':EXPECTED,'aggregate_sha256':AGG}
 print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=='__main__':main()
