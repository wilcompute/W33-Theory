#!/usr/bin/env python3
"""Fail-closed aggregate verifier for Passes 1882--1886."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={
 1882:ROOT/'data/w33_pass1882_decoder_chart_to_global_obstruction.json',
 1883:ROOT/'data/w33_pass1883_full_primal_weight_enumerator.json',
 1884:ROOT/'data/w33_pass1884_two_adic_maximal_order.json',
 1885:ROOT/'data/w33_pass1885_exceptional_s6_carrier_intertwiners.json',
 1886:ROOT/'data/w33_pass1886_geometric_c4_clock_model.json'}
EXPECTED={1882:'c026478da359015c9bdf06a8eb90f5e38c8bde741de65ed38d645418332f2c29',1883:'03d8f7d55536636c8f006bf96618def01f03ac7ae4f59ea915bbba64b016574c',1884:'bc2834982c084141d8966980daa8a21e17be86e4f56df47e628eaee79dda8fb2',1885:'2e33f590eb0f1abb142be927bcdf39827935eea404be3c3e3a62a893c4218a64',1886:'e7dbc3c634826fef76db5926d923c6cc4345697e0f4e2bd3f4050a77bf55cd34'}

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 d={p:json.loads(path.read_text()) for p,path in FILES.items()}
 for p in d:
  assert d[p]['sha256_without_hash_field']==EXPECTED[p]==digest(d[p]),p
  assert all(d[p]['checks'].values()),p
 assert d[1882]['weight5']['corrected_status']=='upper_bound_only'
 assert d[1882]['weight5']['disjoint_weight10_collision_edges_invisible_to_every_coordinate_chart']==2207943360
 assert d[1882]['weight6']['exact_equal_syndrome_collision_edges']==1724138884380
 p=d[1883]['primal_weight_enumerator'];assert [p[str(w)] for w in (12,14,16)]==[891792940,54326090880,3770230198995]
 assert all(d[1883]['shell_designs'][str(w)]['exact_design_strength']==1 for w in (12,14,16))
 assert d[1884]['maximal_order_index']==2**35
 assert d[1884]['conductor']['in_maximal_order']=='1024 Z x 1024 Z x 512 Z[i] x 256 Z[zeta_8]'
 assert d[1885]['separator_V9_multiplicities']=={'15':0,'24':1,'30':0,'81':0,'90':1}
 assert d[1885]['explicit_maps']['ranks']=={'N24':9,'N90':9}
 assert d[1886]['outer_automorphism_fixed_subgroup_structure']=='C4'
 assert d[1886]['orbit_sizes']==[4,4,4,2,1]
 n=sum(len(d[p]['checks']) for p in d);assert n==42
 out={'status':'PASS_WITH_CORRECTION_AND_PROOF_BOUNDARY','n_verified':n,'n_checks':n,'certificates':EXPECTED,'aggregate_sha256':'4a9611b3cd9463307efd12678be2792fd63da77b750e1dd4755bf9bad6fc8f1c'}
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main()
# CI trigger after namespace and manuscript finalization.
