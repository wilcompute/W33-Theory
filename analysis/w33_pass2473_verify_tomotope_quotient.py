#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'data/w33_pass2473_tomotope_rank_colour_quotient_obstruction.json'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d=json.loads(CERT.read_text());assert d['sha256_without_hash_field']==digest(d);assert len(d['archived_rank_colour_unions'])==15;assert all(d['checks'].values());print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
