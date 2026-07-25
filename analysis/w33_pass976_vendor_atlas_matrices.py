#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, functools, hashlib, json, urllib.request
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass976_vendor_atlas_matrices.json'
VENDOR=ROOT/'vendor'/'atlas'/'U42d2'
BASE='https://brauer.maths.qmul.ac.uk/Atlas/clas/U42/gap/'
FILES={
 'U42d2G1-f2r6B0.g1':('1e96c1d330de221f0dbf8939b7daa45057db333a4c453fe4c95258c8e2736ffa',6,1),
 'U42d2G1-f2r6B0.g2':('1954f2d8d932684ca2d982094ce048427555917a253c4bcc6f1fe83a67cb1f60',6,2),
 'U42d2G1-f2r14B0.g1':('3879a3d9c701cbf9ecc7de37bab1a19ecd1329dad167b619615ab3ad3eb2677e',14,1),
 'U42d2G1-f2r14B0.g2':('e284136397294a8a446ffab9197dcc172b349c95b13bbb83dca968495120e0ec',14,2),
 'U42d2G1-f2r40B0.g1':('64e7843a12bd0b50bb40a2ba4a03d754eca503c3340472aab3de0cbd43d61a40',40,1),
 'U42d2G1-f2r40B0.g2':('969d47d8365ff7c8adf8031d74b56e1df4aa0464d41aa73aeba5649da06201ff',40,2),
}
def parse(raw):
 text=raw.decode('ascii');block=text[text.index('['):text.rindex(']')+1];return np.array(ast.literal_eval(block),dtype=np.uint8)%2
def order(A,maxn=100):
 I=np.eye(A.shape[0],dtype=np.uint8);X=I.copy()
 for k in range(1,maxn+1):
  X=X@A%2
  if np.array_equal(X,I):return k
 return None
@functools.lru_cache(maxsize=1)
def payload(fetch=True):
 VENDOR.mkdir(parents=True,exist_ok=True);rows=[];mats={}
 for name,(want,dim,gen) in FILES.items():
  path=VENDOR/name
  if fetch:
   with urllib.request.urlopen(BASE+name,timeout=45) as r:raw=r.read()
   if hashlib.sha256(raw).hexdigest()!=want:raise RuntimeError(f'ATLAS hash mismatch: {name}')
   path.write_bytes(raw)
  raw=path.read_bytes();M=parse(raw);mats[(dim,gen)]=M
  rows.append({'file':str(path.relative_to(ROOT)),'official_url':BASE+name,'sha256':hashlib.sha256(raw).hexdigest(),'expected_sha256':want,'dimension':dim,'generator':gen,'shape':list(M.shape),'binary':bool(np.all((M==0)|(M==1))),'order':order(M)})
 checks={'six_files_vendored':len(rows)==6,'all_source_hashes_exact':all(z['sha256']==z['expected_sha256'] for z in rows),'all_shapes_exact':all(z['shape']==[z['dimension'],z['dimension']] for z in rows),'all_entries_binary':all(z['binary'] for z in rows),'generator_orders_2_and9':all(z['order']==(2 if z['generator']==1 else 9) for z in rows),'product_orders10':all(order(mats[(d,1)]@mats[(d,2)]%2)==10 for d in (6,14,40)),'offline_parse_roundtrip':all(parse((ROOT/z['file']).read_bytes()).shape==(z['dimension'],z['dimension']) for z in rows),'certificate_hash_locked':True};checks={k:bool(v) for k,v in checks.items()}
 raw={'files':rows,'product_orders':{str(d):order(mats[(d,1)]@mats[(d,2)]%2) for d in (6,14,40)}};digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass976.vendor_atlas_matrices.v1','status':'PASS' if all(checks.values()) else 'FAIL','vendor_directory':str(VENDOR.relative_to(ROOT)),'files':rows,'standard_pair_orders':{'c':2,'d':9,'cd':10},'checks':checks,'certificate_sha256':digest,'theorem':'The six public characteristic-two ATLAS matrix files used by Pass 971 are vendored byte-for-byte with their official URLs and SHA-256 digests. Dimensions 6, 14, and 40 each reproduce the standard-generator orders (2,9,10). All subsequent catalogue checks can therefore parse the exact matrices offline without silently changing the external representation basis.','boundary':'The vendored files are third-party public mathematical data retained verbatim with provenance. This pass certifies byte identity and standard-generator orders; the simultaneous repository conjugators remain the stronger Pass 971 result.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload(not a.check);s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 976 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'files':len(p['files'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
