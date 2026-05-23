#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; P=3

def canon(v):
 v=tuple(int(x)%P for x in v)
 if v==(0,0,0,0): raise ValueError
 for x in v:
  if x: return tuple(((1 if x==1 else 2)*y)%P for y in v)
def sp(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P
def spec(A): return Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
def build():
 pts=[]; seen=set()
 for raw in product(range(P), repeat=4):
  if raw==(0,0,0,0): continue
  z=canon(raw)
  if z not in seen: seen.add(z); pts.append(z)
 A=np.zeros((40,40),dtype=np.int8)
 for i,j in combinations(range(40),2):
  if sp(pts[i],pts[j])==0: A[i,j]=A[j,i]=1
 return A
def main():
 W=build(); centers={}
 for t in combinations(range(40),3):
  if all(W[a,b]==0 for a,b in combinations(t,2)):
   centers[t]=tuple(x for x in range(40) if all(W[x,a] for a in t))
 curved=[]
 for t,c in centers.items():
  if len(c)==1: curved.append(tuple(sorted((c[0],)+t)))
 M=np.zeros((40,len(curved)),dtype=np.int8)
 for j,B in enumerate(curved):
  for p in B: M[p,j]=1
 G=M@M.T
 by=defaultdict(Counter)
 for i,j in combinations(range(40),2): by[int(W[i,j])][int(G[i,j])]+=1
 expected=272*np.eye(40,dtype=int)+16*np.ones((40,40),dtype=int)+20*W
 ok=(len(curved)==2880 and len(set(curved))==2880 and Counter(M.sum(0))==Counter({4:2880}) and Counter(M.sum(1))==Counter({288:40}) and by[1]==Counter({36:240}) and by[0]==Counter({16:540}) and np.array_equal(G,expected) and spec(G)==Counter({1152:1,312:24,192:15}))
 out={'all_checks_passed':ok,'summary':{'curved_centered_blocks':len(curved),'block_size_distribution':dict(Counter(M.sum(0))),'point_degree_distribution':dict(Counter(M.sum(1))),'point_pair_coincidence_by_w33_adjacency':{str(k):dict(v) for k,v in by.items()},'point_gram_spectrum':dict(spec(G))},'identity':'M_curved M_curved^T = 272 I_40 + 16 J_40 + 20 A_W33','meaning':'The full curved sector forms a point-frame preserving all W33 eigenspaces: constant, 24-dimensional eigenvalue-2 sector, and 15-dimensional eigenvalue-minus-4 sector.  This is the spectral companion to the flat 45-sector, which kills the minus-4 sector.'}
 path=ROOT/'data'/'w33_curved_sector_point_frame.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
