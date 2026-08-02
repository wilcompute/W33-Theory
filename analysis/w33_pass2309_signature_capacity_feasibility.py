#!/usr/bin/env python3
"""Pass 2309: verify a nine-signature capacity witness in the complete 720 set."""
from __future__ import annotations
import base64,gzip,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/w33_pass1825_signatures720.json.gz.b64'
OUT=ROOT/'data/w33_pass2309_signature_capacity_feasibility.json'
EXPECTED='53b88deb3f0d7d322abf3d49a56a6838dfa84e68ac626a65d8562ad806006776'
IDS=[8,147,194,324,432,485,512,598,703]
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load():
 obj=json.loads(gzip.decompress(base64.b64decode(SRC.read_text().strip())))
 if isinstance(obj,list):rows=obj
 else:
  rows=next(obj[k] for k in ('signatures','vectors','data','rows') if k in obj)
 rows=sorted(tuple(map(int,r)) for r in rows)
 assert len(rows)==720 and len(set(rows))==720 and {len(r) for r in rows}=={45}
 return rows
def main():
 rows=load();chosen=[rows[i] for i in IDS];total=[sum(v[j] for v in chosen) for j in range(45)]
 frozen=json.loads(OUT.read_text());assert frozen['sha256_without_hash_field']==EXPECTED==digest(frozen)
 assert hashlib.sha256(json.dumps([list(x) for x in rows],separators=(',',':')).encode()).hexdigest()==frozen['reconstruction']['signature_set_sha256']
 assert total==[12]*45 and frozen['capacity_solution']['selected_signature_indices']==IDS
 assert frozen['capacity_solution']['selected_signatures']==[list(x) for x in chosen]
 assert all(frozen['checks'].values())
 print(json.dumps({'status':frozen['status'],'certificate':EXPECTED,'selected':IDS,'coordinate_sum':12},sort_keys=True))
if __name__=='__main__':main()
