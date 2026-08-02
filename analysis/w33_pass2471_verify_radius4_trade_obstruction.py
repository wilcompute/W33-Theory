#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'data/w33_pass2471_radius4_signature_trade_obstruction.json'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d=json.loads(CERT.read_text());assert d['sha256_without_hash_field']==digest(d);t=d['trade_search'];assert (t['pair_trade_tuples'],t['triple_trade_tuples'],t['quad_trade_tuples'])==(0,3,11)
 assert len(d['candidate_results'])==14 and all(r['zero_pairs'] and r['minimum_pair_count']==0 for r in d['candidate_results']);assert d['exact_fiber_reconstruction']['unique_signature_fibers']==43;assert all(d['checks'].values())
 print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
