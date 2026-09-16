#!/usr/bin/env python3
"""Identify the ten-dimensional cubic tritangent H1 with the Sp4(F3) adjoint.

Pass7364 gives the mod-3 complex C2=F3^36 --N--> C1=F3^45 --R--> C0=F3^27
with RN=0 and dim H1=10.  Pass4863/4864 independently identifies a different
10D ternary obstruction module with Lambda^2(F3^5)=so5(F3)=sp4(F3).
This file puts the two constructions on the SAME PSp(4,3) generators and solves
the simultaneous Hom equations.  The Hom space is one-dimensional and its
nonzero map has rank ten, proving the cubic holonomy H1 itself is the adjoint.

Consequence for the current magic search: a linear mod-3 tritangent holonomy
lives in the finite symplectic adjoint/controller module.  That is important
Clifford-side structure, but is not by itself a certified non-Clifford gate.
"""
from __future__ import annotations
import importlib.util,itertools,json
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_e6_cubic_h1_is_sp4_adjoint.json'

def load(name):
 p=ROOT/'analysis'/(name+'.py');s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
base_mod=load('w33_pass4992_4999_common')

def rref(M,p=3):
 A=np.asarray(M,dtype=np.int64).copy()%p;r=0;piv=[]
 for c in range(A.shape[1]):
  z=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
  if z is None:continue
  A[[r,z]]=A[[z,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for i in range(A.shape[0]):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  piv.append(c);r+=1
 return A,piv
def rank(M,p=3):return len(rref(M,p)[1])
def null(M,p=3):
 R,piv=rref(M,p);free=[c for c in range(R.shape[1]) if c not in piv];out=[]
 for f in free:
  x=np.zeros(R.shape[1],dtype=np.int64);x[f]=1
  for i,c in enumerate(piv):x[c]=(-R[i,f])%p
  out.append(x)
 return np.asarray(out,dtype=np.int64)
def invm(A,p=3):
 A=np.asarray(A,dtype=np.int64)%p;n=len(A);X=np.c_[A,np.eye(n,dtype=np.int64)]
 for c in range(n):
  z=next(i for i in range(c,n) if X[i,c]);X[[c,z]]=X[[z,c]];X[c]=X[c]*pow(int(X[c,c]),-1,p)%p
  for i in range(n):
   if i!=c and X[i,c]:X[i]=(X[i]-X[i,c]*X[c])%p
 return X[:,n:]%p

def canon(v):
 v=np.asarray(v,dtype=np.int64)%3;k=next(i for i,x in enumerate(v) if x);return tuple((v*pow(int(v[k]),-1,3))%3)

def main(write=True):
 b=base_mod.build_base();grp=base_mod.build_group(b);T=b['tritangents'];DS=b['DS'];di=b['di'];gp=grp['gp'];DP=grp['DPp']
 R=np.zeros((27,45),dtype=np.int64)
 for j,t in enumerate(T):R[list(t),j]=1
 N=1-np.asarray(b['M'],dtype=np.int64)
 assert rank(R,3)==21 and rank(N,3)==14 and not np.any((R@N)%3)
 Z=null(R,3);assert Z.shape==(24,45)
 # Boundary rows first, then a complement in ker R.
 BB=[]
 for v in N.T:
  if rank(np.asarray(BB+[v.tolist()]),3)>len(BB):BB.append(v.tolist())
 assert len(BB)==14
 B24=np.asarray(BB,dtype=np.int64)
 for v in Z:
  if rank(np.vstack([B24,v]),3)>len(B24):B24=np.vstack([B24,v])
  if len(B24)==24:break
 assert B24.shape==(24,45)
 _,pc=rref(B24,3);Pi=invm(B24[:,pc],3)
 co=lambda v:(np.asarray(v,dtype=np.int64)[pc]@Pi)%3
 ti={frozenset(t):i for i,t in enumerate(T)}
 def tperm(g):return tuple(ti[frozenset(g[x] for x in t)] for t in T)
 TP=[tperm(g) for g in gp]
 HA=[]
 for p in TP:
  M=np.zeros((24,24),dtype=np.int64)
  for i,v in enumerate(B24):
   w=np.zeros(45,dtype=np.int64)
   for j,x in enumerate(v):w[p[j]]=x
   M[i]=co(w)
  assert not np.any(M[:14,14:]);HA.append(M[14:,14:]%3)

 # Independent O5(3) natural model on the 36 norm-2 rays; transport the same
 # cubic generators through the double-six graph and take exterior square.
 proj=[]
 for v in itertools.product(range(3),repeat=5):
  if not any(v):continue
  if canon(v)==tuple(v):proj.append(tuple(v))
 n2=[v for v in proj if sum(x*x for x in v)%3==2];assert len(n2)==36
 O=nx.Graph();O.add_nodes_from(range(36));dot=lambda x,y:sum(a*c for a,c in zip(x,y))%3
 for i,j in itertools.combinations(range(36),2):
  if dot(n2[i],n2[j]):O.add_edge(i,j)
 iso=next(nx.algorithms.isomorphism.GraphMatcher(b['H36'],O).isomorphisms_iter())
 OP=[]
 for p in DP:
  q=[0]*36
  for i in range(36):q[iso[i]]=iso[p[i]]
  OP.append(tuple(q))
 bind=next(I for I in itertools.combinations(range(36),5) if rank(np.asarray([n2[i] for i in I]),3)==5)
 V=np.asarray([n2[i] for i in bind],dtype=np.int64);Vi=invm(V,3)
 def lift(p):
  tar=[np.asarray(n2[p[i]]) for i in bind]
  for tail in itertools.product((1,2),repeat=4):
   W=np.asarray([(s*t)%3 for s,t in zip((1,)+tail,tar)]);X=Vi@W%3
   if all(canon(np.asarray(v)@X)==n2[p[i]] for i,v in enumerate(n2)):
    assert np.array_equal(X@X.T%3,np.eye(5,dtype=np.int64));return X
  raise AssertionError
 TF=[lift(p) for p in OP];pairs=list(itertools.combinations(range(5),2))
 def wedge(A):
  W=np.zeros((10,10),dtype=np.int64)
  for r,(i,j) in enumerate(pairs):
   for c,(k,l) in enumerate(pairs):W[r,c]=(A[i,k]*A[j,l]-A[i,l]*A[j,k])%3
  return W
 WA=[wedge(A) for A in TF]
 # Solve A_H X = X A_wedge for X in M_10(F3).
 rows=[]
 for A,W in zip(HA,WA):
  for i in range(10):
   for j in range(10):
    q=np.zeros(100,dtype=np.int64)
    for k in range(10):q[k*10+j]=(q[k*10+j]+A[i,k])%3;q[i*10+k]=(q[i*10+k]-W[k,j])%3
    rows.append(q)
 Hom=null(np.asarray(rows),3);assert Hom.shape==(1,100)
 X=Hom[0].reshape(10,10)%3;assert rank(X,3)==10
 out={'schema':'w33.e6_cubic_h1_is_sp4_adjoint.v1','status':'PASS',
 'headline':'The ten-dimensional mod-3 H1 of the integral 27-line -> 45-tritangent -> 36-double-six cubic complex is PSp(4,3)-equivariantly isomorphic to Lambda^2(F3^5)=so5(F3)=sp4(F3). On common exact generators the Hom space has dimension one and its nonzero intertwiner has rank ten.',
 'cubic_complex':{'R_shape':[27,45],'N_shape':[45,36],'rank_F3_R':21,'rank_F3_N':14,'ker_R':24,'H1':10},
 'intertwiner':{'Hom_dimension_F3':1,'rank':10,'matrix_mod3':X.tolist()},
 'target_module':'Lambda^2(F3^5) ~= so5(F3) ~= sp4(F3), the adjoint PSp(4,3) module',
 'repo_bridge':'This identifies Pass7364 H1 with the same adjoint isomorphism class constructed independently in Pass4858 and explicitly realized as O5(3) adjoint in Pass4863/4864.',
 'magic_boundary':'Linear tritangent holonomy in this H1 is finite symplectic-adjoint/Clifford-side data. A nonzero H1 coordinate may encode global contextual transport, but H1 membership alone is not a non-Clifford gate or magic-state witness.',
 'checks':{'RN_zero_mod3':True,'H1_dim10':True,'common_PSp_generators':True,'Hom_dim1':True,'intertwiner_rank10':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
