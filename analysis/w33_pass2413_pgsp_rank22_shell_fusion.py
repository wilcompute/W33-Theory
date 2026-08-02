#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,importlib.util,json
from pathlib import Path
import numpy as np,sympy as sp
ROOT=Path(__file__).resolve().parents[1];COMMON=ROOT/'analysis/w33_pass1801_1805_common.py';PACK=ROOT/'data/w33_pass1837_middle_layer_compression.json';CERT=ROOT/'data/w33_pass2413_pgsp_rank22_shell_fusion.json'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def common():
 s=importlib.util.spec_from_file_location('c',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def actions():
 D=common().build_geometry();idp=tuple(range(40));seen={idp:(tuple(range(45)),tuple(range(540)))};q=collections.deque([idp])
 while q:
  pp=q.popleft();op,fp=seen[pp]
  for gp,ge,gl,gf,go,gos in D['acts']+[D['outer']]:
   np_=compose(gp,pp)
   if np_ not in seen:seen[np_]=(tuple(go[op[i]] for i in range(45)),tuple(gf[fp[i]] for i in range(540)));q.append(np_)
 assert len(seen)==51840;pack=json.loads(PACK.read_text());F=pack['canonical_six_line_pack'];Fset={frozenset(x) for x in F};s6=[fp for pp,(op,fp) in seen.items() if {frozenset(op[i] for i in x) for x in F}==Fset];assert len(s6)==720;return [fp for op,fp in seen.values()],s6
def orbitals(group):
 rel=np.full((540,540),-1,dtype=np.int16);reps=[];sizes=[]
 for a in range(540):
  for b in range(540):
   if rel[a,b]>=0:continue
   O={(p[a],p[b]) for p in group};r=len(reps)
   for x,y in O:rel[x,y]=r
   reps.append((a,b));sizes.append(len(O))
 return rel,reps,sizes
def full():
 G,S=actions();rf,rpf,sizes=orbitals(G);rs,rps,_=orbitals(S);assert len(rpf)==22 and len(rps)==527
 mapping=[int(rf[a,b]) for a,b in rps];mh=hashlib.sha256(json.dumps(mapping,separators=(',',':')).encode()).hexdigest();val=[int(np.sum(rf[a]==k)) for k,(a,b) in enumerate(rpf)];tr=[int(rf[b,a]) for a,b in rpf]
 r=22;P=np.zeros((r,r,r),dtype=np.int64)
 for k,(a,b) in enumerate(rpf):
  for x in range(540):P[int(rf[a,x]),int(rf[x,b]),k]+=1
 rows=[]
 for j in range(r):
  for k in range(r):
   z=[int(P[i,j,k]-P[j,i,k]) for i in range(r)]
   if any(z):rows.append(z)
 return {'rank':r,'mapping_sha256':mh,'valencies':val,'transpose':tr,'center_dimension':r-sp.Matrix(rows).rank()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');a=ap.parse_args();d=json.loads(CERT.read_text());assert d['sha256_without_hash_field']==digest(d) and all(d['checks'].values())
 if a.full:
  z=full();assert z['rank']==22 and z['mapping_sha256']==d['fusion']['mapping_sha256'] and z['center_dimension']==10;assert z['valencies']==d['algebra']['orbital_valencies'] and z['transpose']==d['algebra']['transpose_map']
 print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
