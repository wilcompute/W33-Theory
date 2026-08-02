#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=[
 ('data/w33_pass2550_global_u6_lower_shadow_singleton_orbits.json','ad12a5f1a781ca0f53a6263fd180404c53b734332c5ce349375d6e2c90835f6b'),
 ('data/w33_pass2551_complete_cover_link_k8_refutation.json','6a5fa12b0febe764648239af6c8e81bc02293527b17232653f010da0c0c91226'),
 ('data/w33_pass2552_radius5_signature_trade_closure.json','187d40e521ee0094bc0ece7dcd5eef0d0e208fec564a553589707bd72bec336f'),
 ('data/w33_pass2553_rank9_octet_a4_v4_decoder.json','fcc12fd84edf8d3a651bca0cee8f6d48fce9b174170e9e6118aa5bfef2e41b96'),
 ('data/w33_pass2554_5colon8_nonlinear_covariants.json','17a884c8e11152c843d400ec94e33ef33f30b1ea489892ab8689a02d1b500e19'),
 ('data/w33_pass2555_syndrome_triangle_geometry.json','ee116fe729b3f8a5dde0c29b2752def1dc3c31e04ce62e3d8ae178743fa46516'),
 ('data/w33_pass2556_frame_graph_chromatic_spectral_gap.json','075534d40ef7b74020637481da1827582fd85c9875427c40c5bb0fdc197dafe1'),
]
AGG='f99df88f81eeb1bbeefeb35e4c1f27b7dd75a57600a301faf75243a2f1048743'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 hs=[];checks=0;data=[]
 for path,expected in FILES:
  d=json.loads((ROOT/path).read_text());got=digest(d)
  assert got==expected==d['sha256_without_hash_field'],(path,got,expected)
  assert all(d.get('checks',{}).values()),path
  hs.append(got);data.append(d);checks+=2+len(d.get('checks',{}))
 assert hashlib.sha256(json.dumps(hs,separators=(',',':')).encode()).hexdigest()==AGG;checks+=1
 d0,d1,d2,d3,d4,d5,d6=data
 assert d0['certified_global_singleton_lower_bound']==3265920
 assert d1['chromatic_consequence']['proved_lower_bound']==10 and not d1['link_search']['any_k8']
 assert d2['exact_lift']['sat_tuples']==0
 assert d3['block_model']['quotient']=='A4/V4 = C3'
 assert d4['equivariant_self_map_dimensions']['3']==4
 assert d5['gram_identity']=='H H^T = 16 I + A_45'
 assert d6['chromatic']['explicit_upper_bound']==14
 checks+=7
 print(json.dumps({'status':'PASS','checks':checks,'aggregate_sha256':AGG},sort_keys=True))
 return checks
if __name__=='__main__':main()
