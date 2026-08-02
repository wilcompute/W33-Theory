#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=[
 ('2430','data/w33_pass2430_labelled_tomotope_group_obstruction.json','56393ccb883c323bb27a46adc051a4e4a1a36cf2d76d631d7a7fb5d5f0d65114'),
 ('2431','data/w33_pass2431_u6_singleton_identifiability.json','cdbb0265764cf07d8e00c489878594cc35e23f765838d28eaad9a1bc9145c2ed'),
 ('2432','data/w33_pass2432_signature_pair_obstruction.json','b839e081cc67a1aab685e1c783ffa4a810185c68e80107e755d26441004e315e'),
 ('2433','data/w33_pass2433_exact_commutative_fusion_lattice.json','c5f306ae722f663cb5af4f17c6d6743c637b9326918a3cfc0437b1afcd61bf1f'),
 ('2434','data/w33_pass2434_c5_split_hom.json','ef00ff26d513a80bb2fa8cbf88598a139ee90630598c89406f11368db1ed12d3')]
AGG='03d119b901433d5c9d14501d929c310c86e1523e52cf2f7926fb7c7efb29b725'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d={}
 for p,f,h in FILES:
  z=json.loads((ROOT/f).read_text());assert z['sha256_without_hash_field']==h==digest(z);d[p]=z
 assert hashlib.sha256(''.join(h for _,_,h in FILES).encode()).hexdigest()==AGG
 assert d['2430']['comparison']['wd4plus_matches']==0 and d['2430']['orbit_exchange_extension_search']['full_relation_preserving_extensions']==20
 assert d['2431']['exact_second_moment_sum_m2_n_m']==3697497150640 and d['2431']['nonidentifiability_witness']['distribution_A']['n1']!=d['2431']['nonidentifiability_witness']['distribution_B']['n1']
 assert d['2432']['exact_pair_test']['fiber_counts']==[11664,288] and d['2432']['exact_pair_test']['disjoint_pairs']==0
 assert d['2433']['exhaustive_search']['binary_symmetric_seeds_tested']==65535 and d['2433']['finest_commutative_fusion']['rank']==9
 assert d['2434']['restriction']['Hom_C5_E8_to_coexact90_dimension']==144
 p16=json.loads((ROOT/'data/w33_pass2416_nine_signature_cover_fibers.json').read_text());assert p16['selected_fiber_counts']==d['2432']['selected_signature_fibers']['counts']
 for f in ('w33_paper.tex','photonic_holonet.tex'):
  text=(ROOT/f).read_text();assert 'analysis/BT2435_five_frontiers_insert' in text
 print(json.dumps({'status':'PASS','checks':21,'aggregate_sha256':AGG,'certificates':{p:h for p,_,h in FILES}},sort_keys=True))
if __name__=='__main__':main()
