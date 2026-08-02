#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'data/w33_pass2411_global_u6_collision_ledger.json';MAC=ROOT/'data/w33_pass1940_split_macwilliams.json'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d=json.loads(CERT.read_text());assert d['sha256_without_hash_field']==digest(d);m=json.loads(MAC.read_text());A={int(k):v for k,v in m['ordinary_low_weights'].items() if int(k) in (4,6,8,10,12)}
 C={w:A[w]*math.comb(w,w//2)*math.comb(240-w,6-w//2)//2 for w in A};assert sum(C.values())==d['global_equal_syndrome_collision_edges']==1724138884380
 I={w:C[w]*(6-w//2)//240 for w in C};X={w:C[w]*w//240 for w in C};assert sum(I.values())==d['fixed_coordinate_chart']['internal_collision_edges'];assert sum(X.values())==d['fixed_coordinate_chart']['crossing_partner_incidences'];assert all(d['checks'].values())
 print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
