#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
FILES={1939:'w33_pass1939_u6_supershard.json',1940:'w33_pass1940_split_macwilliams.json',1941:'w33_pass1941_gaussian_solver_transport.json',1942:'w33_pass1942_integral_phase_order.json',1943:'w33_pass1943_hodge_eisenstein_carrier_separator.json'}
EXPECTED={1939:'0c47affe22e578d5886e84db4981dac9f230093bb0661606b94ac72247737ca1',1940:'5590688669ec4567d35d12ed1e9f27ecdfab2a3af0a0355b523b8f19285a896f',1941:'0b5940750dc83e1932956bb3e771438dc4a8e319fd1e2c5ba57e0c352c82fc96',1942:'c585873e71a79461cff5d684ef0553c60a4e0abd6c3fa2bf8b9c13b03de27433',1943:'0bdfcf35965f2b704c1d61bb70b973df83d843dab8d3d3afd4b958f233e7fa28'}
AGG='970cb200b3e2b960424ec084da72c075f42d14bbf189f281634562d1a4103971'
def chash(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d={p:json.loads((DATA/f).read_text()) for p,f in FILES.items()};checks=[]
 def add(n,x):checks.append((n,bool(x)))
 for p,x in d.items():add(f'{p}_hash',x['sha256_without_hash_field']==EXPECTED[p]==chash(x));add(f'{p}_checks',all(x['checks'].values()))
 add('1939_records',d[1939]['combined_supershard']['records']==58282126);add('1939_cross_edges',d[1939]['cross_shard_effect']['collision_edges_newly_visible']==5389182)
 add('1940_bins',d[1940]['full_transform']['nonzero_bins']==39081);add('1940_words',d[1940]['full_transform']['words']==2**195);add('1940_weight4',sum(z[3] for z in d[1940]['split_shells_through_12']['4'])==540)
 add('1941_odd_kernel',d[1941]['oriented_lift']['odd_subspace_dimension']==135);add('1942_order',d[1942]['associative_order']['integral_order']=='M3(Z)');add('1942_infinite',d[1942]['unit_group_behavior']['generated_group']=='infinite')
 add('1943_signature',d[1943]['energy_invariant']=={'definition':'epsilon(A)=tr(A^T L1 A)/tr(A^T A)','A24':10,'A90':4})
 agg=json.loads((DATA/'w33_pass1939_1943_five_frontiers.json').read_text());add('aggregate_hash',agg['sha256_without_hash_field']==AGG==chash(agg));add('aggregate_checks',agg['n_checks']==agg['n_verified']==40)
 failed=[n for n,x in checks if not x]
 if failed:raise AssertionError(failed)
 print(f'PASS {len(checks)}/{len(checks)}')
if __name__=='__main__':main()
