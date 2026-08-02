#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=[
'data/w33_pass2470_multishard_u6_union_engine.json',
'data/w33_pass2471_radius4_signature_trade_obstruction.json',
'data/w33_pass2472_rank9_scheme_decode.json',
'data/w33_pass2473_tomotope_rank_colour_quotient_obstruction.json',
'data/w33_pass2474_f20_lifted_normalizer_hom.json']
EXPECTED='edb352760cf624957c1f2903c8d8e8edef056ffe8b7c073ccd9d30c1d27919fa'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 hs=[];checks=0
 for p in FILES:
  d=json.loads((ROOT/p).read_text());assert d['sha256_without_hash_field']==digest(d);assert all(d['checks'].values());hs.append(d['sha256_without_hash_field']);checks+=2+len(d['checks'])
 agg=hashlib.sha256('\n'.join(hs).encode()).hexdigest();assert agg==EXPECTED
 print(json.dumps({'status':'PASS','checks':checks+1,'aggregate_sha256':agg},sort_keys=True))
if __name__=='__main__':main()
