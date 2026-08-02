#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'data/w33_pass2412_proof_producing_nine_colour_search.json'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d=json.loads(CERT.read_text());assert d['sha256_without_hash_field']==digest(d);assert all(d['checks'].values());assert d['exact_cover_enumeration']['covers']==394200;assert d['literal_all_different_search']['status']=='UNKNOWN';print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
