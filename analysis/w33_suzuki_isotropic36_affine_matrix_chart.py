#!/usr/bin/env python3
r"""Resolve the special 36-point totally-isotropic Suzuki section.

A 4-dimensional totally isotropic subspace of the 12-dimensional 2.Suz module
meets the 32760-point tight set in 36 of its 40 projective points.  The four
missing points are one complete projective line.  Hence the section is exactly
PG(3,3) \ PG(1,3), not the 36-element W33 spread carrier.

The complement has a useful affine/matrix chart: after choosing a complementary
2-space, its 36 points split as 4 quotient directions times 9 lifts, and its 81
fully-contained projective lines are the graphs of all 3^4 linear maps
F3^2 -> F3^2, i.e. M_2(F3).  This is a new bridge to the 81-element two-qutrit
Pauli displacement register, but no physical identification is asserted.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_suzuki_isotropic36_affine_matrix_chart.json'
P=3
J=np.array([
[0,0,0,0,0,0,1,2,2,2,1,2],[0,0,0,0,0,0,2,2,1,2,1,1],
[0,0,0,0,0,2,0,2,1,2,0,1],[0,0,0,0,2,0,2,0,0,1,2,1],
[0,0,0,1,0,0,0,1,2,0,2,0],[0,0,1,0,0,0,1,0,2,0,1,0],
[2,1,0,1,0,2,0,0,1,0,0,2],[1,1,1,0,2,0,0,0,0,2,2,0],
[1,2,2,0,1,1,2,0,0,0,0,2],[1,1,1,2,0,0,0,1,0,0,1,0],
[2,2,0,1,1,2,0,1,0,2,0,0],[1,2,2,2,0,0,1,0,1,0,0,0]],dtype=np.int64)
T_SEED=np.array([1,1,0,1,0,2,1,0,1,0,0,1],dtype=np.int64)
B36=np.array([
[1,0,0,0,0,1,2,2,1,1,1,1],
[0,1,0,0,0,0,2,1,2,0,1,1],
[0,0,1,0,0,1,0,1,0,0,1,2],
[0,0,0,1,1,0,1,2,1,0,2,2]],dtype=np.int64)

def parse(path):
 t=path.read_text().split();return np.array([[int(c) for c in r] for r in t[4:]],dtype=np.int64)%P

def rankp(M):
 A=np.array(M,dtype=np.int64)%P;r=0
 for c in range(A.shape[1]):
  q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
  if q is None:continue
  A[[r,q]]=A[[q,r]];A[r]=A[r]*pow(int(A[r,c]),-1,P)%P
  for i in range(A.shape[0]):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
  r+=1
 return r

def rref(M):
 A=np.array(M,dtype=np.int64)%P;r=0
 for c in range(A.shape[1]):
  q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
  if q is None:continue
  A[[r,q]]=A[[q,r]];A[r]=A[r]*pow(int(A[r,c]),-1,P)%P
  for i in range(A.shape[0]):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
  r+=1
 return A[[i for i in range(A.shape[0]) if np.any(A[i])]]

def canon(v):
 a=np.array(v,dtype=np.int64)%P;i=next(i for i,x in enumerate(a) if x);return tuple(map(int,a*pow(int(a[i]),-1,P)%P))

def orbit(seed,gens):
 s=canon(seed);S={s};Q=deque([np.array(s,dtype=np.int64)])
 while Q:
  v=Q.popleft()
  for g in gens:
   w=canon(v@g%P)
   if w not in S:S.add(w);Q.append(np.array(w,dtype=np.int64))
 return S

def invp(M):
 n=len(M);A=np.hstack([np.array(M,dtype=np.int64)%P,np.eye(n,dtype=np.int64)])
 r=0
 for c in range(n):
  q=next(i for i in range(r,n) if A[i,c]);A[[r,q]]=A[[q,r]]
  A[r]=A[r]*pow(int(A[r,c]),-1,P)%P
  for i in range(n):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
  r+=1
 return A[:,n:]%P

def main(write=True):
 A=parse(ROOT/'data/atlas/2SuzG1-f3r12B0.m1');B=parse(ROOT/'data/atlas/2SuzG1-f3r12B0.m2')
 assert np.all((B36@J@B36.T)%P==0)
 T=orbit(T_SEED,[A,B]);assert len(T)==32760
 coeff=sorted({canon(v) for v in itertools.product(range(P),repeat=4) if any(v)})
 image={c:canon(np.array(c,dtype=np.int64)@B36%P) for c in coeff}
 inside={c for c in coeff if image[c] in T};missing=set(coeff)-inside
 assert len(inside)==36 and len(missing)==4
 L=rref(np.array(list(missing),dtype=np.int64));assert L.shape==(2,4)
 Lpts={canon(np.array(c,dtype=np.int64)@L%P) for c in itertools.product(range(P),repeat=2) if any(c)}
 assert Lpts==missing
 # All 130 projective lines of PG(3,3); classify by missing-line intersection.
 lines=set()
 for a,b in itertools.combinations(coeff,2):
  if rankp(np.array([a,b]))<2:continue
  Q=frozenset(canon((x*np.array(a)+y*np.array(b))%P) for x in range(P) for y in range(P) if x or y)
  if len(Q)==4:lines.add(Q)
 assert len(lines)==130
 hist=Counter(len(set(Q)&missing) for Q in lines);assert hist==Counter({0:81,1:48,4:1})
 # Extend the missing 2-space to a basis and read quotient projective directions.
 ext=[x.copy() for x in L]
 for e in np.eye(4,dtype=np.int64):
  if rankp(np.array(ext+[e]))>len(ext):ext.append(e)
  if len(ext)==4:break
 E=np.array(ext,dtype=np.int64);Ei=invp(E)
 classes=Counter()
 for c in inside:
  z=np.array(c,dtype=np.int64)@Ei%P;q=canon(z[2:])
  classes[q]+=1
 assert len(classes)==4 and set(classes.values())=={9}
 out={
  'schema':'w33.suzuki_isotropic36_affine_matrix_chart.v1','status':'PASS',
  'headline':'A totally isotropic four-space meets the Suzuki 32760-set in exactly PG(3,3) minus one projective line: 36 points. The section has 81 fully contained projective lines, exactly the lines disjoint from the missing line. Choosing a complementary 2-space identifies those 81 lines with graphs of all linear maps F3^2 -> F3^2, i.e. M_2(F3).',
  'basis_12d':B36.tolist(),'symplectic_rank':0,'section':{'PG3_points':40,'tight_points':36,'missing_points':4,'missing_span_dimension':2,'missing_object':'PG(1,3)'},
  'projective_line_census_by_missing_line_intersection':{'0':81,'1':48,'4':1},
  'affine_chart':{'quotient_projective_directions':4,'lifts_per_direction':9,'factorization':'36=4*9','contained_lines':81,'matrix_model':'End(F3^2)=M_2(F3), |M_2(F3)|=3^4=81'},
  'spread_boundary':'This 36-point isotropic section is not identified with the 36 W33 spreads. The latter are a different PSp(4,3)-set already proved equivariantly equivalent to the 36 E6 cubic double-sixes in Pass 4964.',
  'computational_reading':'The 81 contained lines give an exact finite M_2(F3) chart, numerically and algebraically the same 3^4 register size as two-qutrit Pauli displacement labels. A quantum-computational identification requires an explicit operator map and is not asserted here.',
  'checks':{'isotropic':True,'intersection_36':True,'missing_is_one_line':True,'line_census_81_48_1':True,'quotient_4_times_9':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
