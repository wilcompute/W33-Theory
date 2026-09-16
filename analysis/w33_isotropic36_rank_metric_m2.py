#!/usr/bin/env python3
"""Rank-metric structure inside the Suzuki isotropic-36 affine matrix chart.

The parent certificate identifies the 81 projective lines disjoint from the
missing line in PG(3,3) with graph lines Gamma_A for all A in M_2(F3).
For graph lines, Gamma_A and Gamma_B meet iff A-B is singular.  Therefore the
complementary 'disjoint-channel' relation is exactly rank(A-B)=2.

This verifier enumerates all 81 matrices and all 130 two-dimensional F3-linear
subspaces of M2(F3).  The invertible-difference graph is SRG(81,48,27,30), with
spectrum 48^1,3^48,(-6)^32.  Exactly 18 two-planes C have every nonzero member
invertible: [2x2,2,2]_3 MRD subspaces.  Each of their 9 affine cosets A+C is a
9-set with pairwise invertible differences.  The corresponding nine graph lines
are pairwise disjoint; adjoining the deleted PG(1,3) line yields a 10-line spread
of PG(3,3).  The 18 directions give 162 distinct affine-linear spread frames.

These spreads live in the totally isotropic ambient four-space of the 12D
Suzuki module.  They are projective line spreads, NOT the 36 spreads of a
nondegenerate W(3,3); the ambient symplectic restriction here is zero.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_isotropic36_rank_metric_m2.json'
P=3

def rref_key(rows):
 A=np.array(rows,dtype=np.int64)%P;r=0
 for c in range(A.shape[1]):
  q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
  if q is None:continue
  A[[r,q]]=A[[q,r]];A[r]=A[r]*pow(int(A[r,c]),-1,P)%P
  for i in range(A.shape[0]):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
  r+=1
 A=A[[i for i in range(A.shape[0]) if np.any(A[i])]]
 return tuple(tuple(map(int,x)) for x in A)

def mrank(v):
 a,b,c,d=map(int,v);det=(a*d-b*c)%3
 if det:return 2
 return 0 if not any(v) else 1

def span(B):
 return {tuple((x*np.array(B[0])+y*np.array(B[1]))%3) for x in range(3) for y in range(3)}

def main(write=True):
 parent=json.loads((ROOT/'data'/'w33_suzuki_isotropic36_affine_matrix_chart.json').read_text());assert parent['status']=='PASS' and parent['lines']['contained']==81
 V=[tuple(v) for v in itertools.product(range(3),repeat=4)]
 ranks=Counter(mrank(v) for v in V);assert ranks==Counter({2:48,1:32,0:1})
 # rank-distance graph
 A=np.zeros((81,81),dtype=bool)
 for i,j in itertools.combinations(range(81),2):
  if mrank(tuple((np.array(V[i])-np.array(V[j]))%3))==2:A[i,j]=A[j,i]=True
 assert set(map(int,A.sum(1)))=={48}
 la=set();mu=set()
 for i,j in itertools.combinations(range(81),2):
  z=int(np.logical_and(A[i],A[j]).sum());(la if A[i,j] else mu).add(z)
 assert la=={27} and mu=={30}
 # all projective 2-subspaces of F3^4
 subs={}
 nz=V[1:]
 for a,b in itertools.combinations(nz,2):
  k=rref_key([a,b])
  if len(k)==2:subs[k]=span(k)
 assert len(subs)==130
 mrd=[(k,S) for k,S in subs.items() if all(mrank(v)==2 for v in S if any(v))]
 assert len(mrd)==18
 I=(1,0,0,1);assert sum(I in S for _,S in mrd)==3
 # affine cosets; a coset is stored as its sorted 9 matrix labels.
 cosets=set()
 for _,C in mrd:
  unseen=set(V)
  while unseen:
   a=min(unseen);D=frozenset(tuple((np.array(a)+np.array(c))%3) for c in C)
   assert len(D)==9
   assert all(mrank(tuple((np.array(x)-np.array(y))%3))==2 for x,y in itertools.combinations(D,2))
   cosets.add(tuple(sorted(D)));unseen-=D
 assert len(cosets)==162
 # eigenvalue multiplicities are forced by SRG parameters / trace.
 spectrum={'48':1,'3':48,'-6':32}
 out={
  'schema':'w33.isotropic36_rank_metric_m2.v1','status':'PASS',
  'headline':'The 81 graph lines in the Suzuki PG(3,3)-minus-line chart carry the M2(F3) rank metric. Invertible difference gives SRG(81,48,27,30) with spectrum 48^1+3^48+(-6)^32. Exactly 18 two-dimensional MRD subspaces exist; their 9 affine cosets give 162 distinct 9-line parallel frames, each closing with the deleted line to a 10-line projective spread.',
  'matrix_space':{'size':81,'rank_census':{'0':1,'1':32,'2':48}},
  'rank_metric_graph':{'srg':[81,48,27,30],'edges':1944,'spectrum':spectrum,'adjacency':'rank(A-B)=2 iff graph lines Gamma_A,Gamma_B are disjoint'},
  'two_planes':{'total':130,'MRD_every_nonzero_invertible':18,'MRD_containing_identity':3},
  'affine_frames':{'cosets_per_MRD_direction':9,'distinct_cosets':162,'matrices_per_coset':9,'geometry':'9 pairwise-disjoint graph lines + deleted line = 10-line spread of PG(3,3)'},
  'computation_reading':'M2(F3) is a four-trit address space. Rank distance becomes a directly geometric collision/disjointness test, and the 18 MRD directions provide maximal affine channel codes. This is a finite coding/compiler structure, not yet a physical gate set.',
  'boundary':'These 162 are projective line spreads inside a totally isotropic PG(3,3) chart. They must not be conflated with the 36 symplectic W33 spreads/double-sixes, whose underlying 4-space is nondegenerate.',
  'checks':{'parent_81_lines':True,'rank_census':True,'SRG_81_48_27_30':True,'130_two_planes':True,'18_MRD':True,'162_affine_frames':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
