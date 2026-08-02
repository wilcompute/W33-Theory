#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'data/w33_pass2474_f20_lifted_normalizer_hom.json'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d=json.loads(CERT.read_text());assert d['sha256_without_hash_field']==digest(d);assert d['sylow5_normalizer']['order_spectrum']=={'1':1,'2':1,'4':10,'5':4,'8':20,'10':4};assert d['lifted_normalizer_action']['Hom_5colon8_dimension']==0;assert all(d['checks'].values());print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
