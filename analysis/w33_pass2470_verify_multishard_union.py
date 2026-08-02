#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'data/w33_pass2470_multishard_u6_union_engine.json'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d=json.loads(CERT.read_text());assert d['sha256_without_hash_field']==digest(d)
 for ns,x in d['runs'].items():
  n=int(ns);assert x['records']==n*math.comb(237,3);assert x['unique_representatives']==math.comb(238,4)-math.comb(238-n,4)
  hist={str(k):math.comb(n,k)*math.comb(238-n,4-k) for k in range(1,min(4,n)+1)};assert x['representative_shard_multiplicity_histogram']==hist
  assert x['unique_representatives']==x['collision_marked_union_representatives']+x['collision_unmarked_union_representatives']
 assert all(d['checks'].values());print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
