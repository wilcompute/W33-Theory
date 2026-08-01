#!/usr/bin/env python3
"""Pass 1836: reconstruct the 720 nonlinear signatures and verify/solve sum t_i=12*1."""
from __future__ import annotations
import argparse, itertools, json, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass1801_1805_common import build_geometry
WITNESS=[15,47,67,80,117,128,259,399,514]
PATTERNS=[('T128',(0,2,4)),('T120',(0,3,3)),('T104',(1,2,3)),('T96',(2,2,2))]
def build():
 d=build_geometry();octets=d['octets'];A=np.zeros((45,45),dtype=np.int8)
 for i in range(45):
  si=set(octets[i][0])|set(octets[i][1])
  for j in range(i+1,45):
   sj=set(octets[j][0])|set(octets[j][1])
   if len(si&sj)==2:A[i,j]=A[j,i]=1
 assert np.all(A.sum(1)==32)
 sig=[];labels=[];anchors=[];values=[]
 for a in range(45):
  non=[j for j in range(45) if j!=a and not A[a,j]]
  remaining=set(non);cells=[]
  while remaining:
   seed=min(remaining);stack=[seed];remaining.remove(seed);cell=[]
   while stack:
    u=stack.pop();cell.append(u)
    for v in list(remaining):
     if not A[u,v]:remaining.remove(v);stack.append(v)
   cells.append(sorted(cell))
  cells=sorted(cells);assert list(map(len,cells))==[4,4,4]
  for name,pat in PATTERNS:
   for vals in sorted(set(itertools.permutations(pat))):
    t=np.ones(45,dtype=np.int8);t[a]=4
    for c,v in zip(cells,vals):t[c]=v
    assert int(t.sum())==60 and np.all(A@t+4*t==48)
    sig.append(t);labels.append(name);anchors.append(a);values.append(vals)
 S=np.array(sig,dtype=np.int16);assert S.shape==(720,45) and len({tuple(x) for x in S})==720
 return A,S,labels,anchors,values
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--solve',action='store_true');args=ap.parse_args()
 A,S,labels,anchors,values=build();x=np.zeros(720,dtype=int);x[WITNESS]=1
 assert x.sum()==9 and np.array_equal(x@S,np.full(45,12))
 result={'status':'PASS','witness_indices':WITNESS,'class_multiset':dict(__import__('collections').Counter(labels[i] for i in WITNESS)),'target_verified':True}
 if args.solve:
  from scipy.optimize import Bounds,LinearConstraint,milp
  C=np.vstack([S.T,np.ones((1,720),dtype=np.int16)]);b=np.r_[np.full(45,12),9]
  r=milp(c=np.zeros(720),integrality=np.ones(720),bounds=Bounds(0,9),constraints=LinearConstraint(C,b,b),options={'mip_rel_gap':0})
  assert r.x is not None;z=np.rint(r.x).astype(int);assert np.array_equal(z@S,np.full(45,12)) and z.sum()==9
  result['solver_status']=r.message;result['solver_witness']=np.flatnonzero(z).astype(int).tolist()
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
