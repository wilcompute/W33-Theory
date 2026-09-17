#!/usr/bin/env python3
"""Exact stopping distance of the 165-point / 297-line GQ(4,8) decoder.

The local Suzuki carrier is already certified as the point graph of GQ(4,8),
SRG(165,36,3,9).  A point-erasure peeling decoder has one equation per GQ line:
a line-sum measurement can recover a point whenever that line contains exactly
one erased point.  A stopping set S therefore meets every GQ line in either 0
or at least 2 points.

Two ingredients give the exact minimum.

1) If S is a stopping set, every p in S has at least one partner on each of the
   nine GQ lines through p.  Distinct lines through p meet only in p, so the
   induced point graph on S has minimum degree at least 9, hence average degree
   at least 9.
2) The point graph has eigenvalues 36,3,-9.  For |S|=m the indicator-vector
   Rayleigh bound using the largest nontrivial eigenvalue 3 gives

      2 e(S) <= 36 m^2/165 + 3(m-m^2/165) = 3m + m^2/5.

   Combining 2e(S)>=9m gives m>=30.

A concrete 30-point witness is constructed in the classical Hermitian model
H(4,4) of GQ(4,8).  It meets the 297 lines in 162 empty lines and 135 secants,
so it is a stopping set and the lower bound is sharp.

Therefore d_stop=30: any <=29 erased point encodings are peel-decodable from
surviving point values plus all 297 line-sum measurements.  A 30-erasure
stopping pattern exists, so 29 is the exact worst-case peeling guarantee.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_suzuki_gq48_stopping_distance.json'

# GF(4)=F2[a]/(a^2+a+1), encoded 0,1,a,a+1 as 0,1,2,3.
def mul(x,y):
    p=0
    for i in range(2):
        if (x>>i)&1:
            for j in range(2):
                if (y>>j)&1:p^=1<<(i+j)
    if p&4:p^=4^2^1
    return p

def sq(x):return mul(x,x)
def inv(x):
    if not x:raise ZeroDivisionError
    return sq(x)
def canon(v):
    for x in v:
        if x:
            a=inv(x);return tuple(mul(a,z) for z in v)
    raise ValueError
def herm(u,v):
    s=0
    for x,y in zip(u,v):s^=mul(x,sq(y))
    return s

def build():
    P=sorted({canon(v) for v in itertools.product(range(4),repeat=5) if any(v) and herm(v,v)==0})
    pi={p:i for i,p in enumerate(P)};lines=set()
    for i,u in enumerate(P):
        for v in P[i+1:]:
            if herm(u,v):continue
            z=set()
            for a,b in itertools.product(range(4),repeat=2):
                if not(a or b):continue
                z.add(canon(tuple(mul(a,u[k])^mul(b,v[k]) for k in range(5))))
            if len(z)==5:lines.add(tuple(sorted(pi[x] for x in z)))
    return P,sorted(lines)

WITNESS=[
(0,0,0,1,1),(0,0,0,1,2),(0,0,0,1,3),
(0,1,0,0,1),(0,1,0,0,2),(0,1,0,0,3),
(0,1,0,1,0),(0,1,0,2,0),(0,1,0,3,0),
(0,1,1,1,2),(0,1,1,2,1),(0,1,1,3,3),
(0,1,2,1,2),(0,1,2,2,1),(0,1,2,3,3),
(0,1,3,1,2),(0,1,3,2,1),(0,1,3,3,3),
(1,0,1,0,0),(1,0,2,0,0),(1,0,3,0,0),
(1,1,0,1,2),(1,1,0,2,1),(1,1,0,3,3),
(1,2,0,1,1),(1,2,0,2,3),(1,2,0,3,2),
(1,3,0,1,3),(1,3,0,2,2),(1,3,0,3,1)]

def main(write=True):
    parent=json.loads((ROOT/'data'/'w33_suzuki_local_165_gq48_spectral_bridge.json').read_text())
    assert parent['status']=='PASS' and parent['construction']['srg']==[165,36,3,9]
    P,L=build();assert len(P)==165 and len(L)==297
    deg=Counter(x for z in L for x in z);assert set(deg.values())=={9}
    A=np.zeros((165,165),dtype=np.int64)
    for z in L:
        for a,b in itertools.combinations(z,2):A[a,b]=A[b,a]=1
    assert set(A.sum(1))=={36}
    # SRG common-neighbor counts.
    la=set();mu=set()
    for i,j in itertools.combinations(range(165),2):
        c=int(np.logical_and(A[i],A[j]).sum())
        (la if A[i,j] else mu).add(c)
    assert la=={3} and mu=={9}
    pi={p:i for i,p in enumerate(P)};S={pi[p] for p in WITNESS};assert len(S)==30
    census=Counter(len(S.intersection(z)) for z in L);assert census==Counter({0:162,2:135})
    d=A[np.ix_(sorted(S),sorted(S))].sum(1);assert set(map(int,d))=={9}
    # Spectral lower bound: 9m <= 3m + m^2/5 -> m>=30.
    m=30
    upper=3*m+m*m//5;lower=9*m;assert upper==lower==270
    out={
      'schema':'w33.suzuki_gq48_stopping_distance.v1','status':'PASS',
      'headline':'The 165-point/297-line GQ(4,8) peeling decoder has exact stopping distance 30. The SRG upper-eigenvalue bound forces every stopping set to have at least 30 points, and an explicit 30-point Hermitian-model witness meets the 297 lines as 162 empty + 135 secants.',
      'incidence':{'points':165,'lines':297,'points_per_line':5,'lines_per_point':9,'point_graph_srg':[165,36,3,9],'point_graph_spectrum':{'36':1,'3':120,'-9':44}},
      'lower_bound':{'stopping_implies_min_induced_degree':9,'rayleigh_upper':'2e(S) <= 3m + m^2/5','stopping_lower':'2e(S) >= 9m','consequence':'m>=30'},
      'witness':{'size':30,'GF4_coordinates':[list(x) for x in WITNESS],'line_intersection_census':{'0':162,'2':135},'induced_degree':9},
      'decoder_consequence':{'stopping_distance':30,'all_point_erasure_patterns_up_to':29,'decoder':'iterative peeling using surviving point values and all 297 line-sum measurements','sharp':True},
      'boundary':'Stopping distance controls the local peeling decoder. A size-30 stopping set may still be recoverable by a different global linear solver; that stronger question is not claimed here.',
      'checks':{'classical_GQ48_165_297':True,'srg_165_36_3_9':True,'spectral_lower_bound_30':True,'explicit_size30_stopping_set':True,'line_census_162_135':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
