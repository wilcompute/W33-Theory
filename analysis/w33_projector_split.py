#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; P=3

def cn(v):
 v=tuple(int(x)%P for x in v)
 if v==(0,0,0,0): raise ValueError
 for x in v:
  if x: return tuple(((1 if x==1 else 2)*y)%P for y in v)
def sp(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P
def ec(A): return Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
def W():
 pts=[]; seen=set()
 for raw in product(range(P),repeat=4):
  if raw==(0,0,0,0): continue
  z=cn(raw)
  if z not in seen: seen.add(z); pts.append(z)
 A=np.zeros((40,40),dtype=int)
 for i,j in combinations(range(40),2):
  if sp(pts[i],pts[j])==0: A[i,j]=A[j,i]=1
 return A
def main():
 A=W(); I=np.eye(40,dtype=int); J=np.ones((40,40),dtype=int)
 Gf=8*I+J+2*A
 Gc=272*I+16*J+20*A
 P15=8*I+J-4*A
 P25=16*I+4*A-J
 R=Gc-26*Gf+18*J
 checks={
  'A_spectrum':ec(A)==Counter({12:1,2:24,-4:15}),
  'P15_scaled_idempotent':np.array_equal(P15@P15,24*P15),
  'P25_scaled_idempotent':np.array_equal(P25@P25,24*P25),
  'orthogonal_scaled':np.array_equal(P15@P25,np.zeros((40,40),dtype=int)),
  'sum_scaled':np.array_equal(P15+P25,24*I),
  'residual_formula':np.array_equal(R,8*P15),
 }
 out={'all_checks_passed':all(checks.values()),'summary':{'A_spectrum':dict(ec(A)),'flat_frame_spectrum':dict(ec(Gf)),'curved_frame_spectrum':dict(ec(Gc)),'residual_spectrum':dict(ec(R)),'rank_25_projector_scaled_trace':int(np.trace(P25)//24),'rank_15_projector_scaled_trace':int(np.trace(P15)//24)},'checks':checks,'identities':{'rank15_projector':'E15=(8I+J-4A)/24','rank25_projector':'E25=(16I+4A-J)/24','frame_residual':'Gc-26Gf+18J=192E15'},'meaning':'The flat-visible frame and the curved/full frame give an exact algebraic split of the W33 point space into ranks 25 and 15.'}
 path=ROOT/'data'/'w33_projector_split.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if out['all_checks_passed'] else 1
if __name__=='__main__': raise SystemExit(main())
