#!/usr/bin/env python3
"""Exact 216-circuit -> 15+20 flat-band intertwiner audit.

The 216 sentinel five-circuits form PSp(4,3)/S5.  This script asks the
representation-theoretic question left open by the Clifford-torsor no-go:
do these circuits carry explicit copies of the 20-dimensional right dark
sector and/or the 15-dimensional left dark sector of the 40x45 Hermitian
incidence coupling B?

The circuit incidence C (216 x 45) is canonical.  Its Gram operator is proved
exactly, and the stabilizer-fixed dimensions of the 15 and 20 irreducibles are
computed from orbit indicators, i.e. by Frobenius reciprocity without relying
on character-table labels.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path

from w33_20260829_216_clifford_torsor_nogo import (
    geometry,supports_from_N,closure_paired,norm,form,compose
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_CIRCUIT_DARK_INTERTWINER.json'
P=1000003

def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A): return [list(x) for x in zip(*A)]
def add(A,B,sa=1,sb=1): return [[sa*A[i][j]+sb*B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def rank_mod(A,p=P):
    M=[[x%p for x in row] for row in A];m=len(M);n=len(M[0]);r=0
    for c in range(n):
        q=next((i for i in range(r,m) if M[i][c]),None)
        if q is None: continue
        M[r],M[q]=M[q],M[r]; inv=pow(M[r][c],p-2,p);M[r]=[(x*inv)%p for x in M[r]]
        for i in range(m):
            if i==r or not M[i][c]: continue
            z=M[i][c];M[i]=[(M[i][j]-z*M[r][j])%p for j in range(n)]
        r+=1
        if r==m: break
    return r

def orbits(H,n,which):
    rem=set(range(n));out=[]
    while rem:
        s=min(rem);O={s};Q=deque([s])
        while Q:
            x=Q.popleft()
            for h in H:
                y=h[which][x]
                if y not in O:O.add(y);Q.append(y)
        out.append(tuple(sorted(O)));rem-=O
    return sorted(out,key=lambda z:(len(z),z))
def indicators(orbs,n):
    return [[int(i in O) for O in orbs] for i in range(n)]

def main():
    pts,idx,lines,N=geometry();supports,masks=supports_from_N(N)
    # 40-point collinearity graph.
    NtN=mm(tr(N),N);A40=add(NtN,eye(40),1,-4)
    # 45-point GQ(4,2): minimum supports are adjacent iff disjoint.
    A45=[[0]*45 for _ in range(45)]
    for i,j in itertools.combinations(range(45),2):
        if supports[i].isdisjoint(supports[j]):A45[i][j]=A45[j][i]=1
    assert {sum(r) for r in A40}=={12} and {sum(r) for r in A45}=={12}

    circuits=[]
    for cc in itertools.combinations(range(45),5):
        w=0
        for i in cc:w^=masks[i]
        if w==0:circuits.append(cc)
    assert len(circuits)==216
    C=[[int(m in cc) for m in range(45)] for cc in circuits]
    G=mm(tr(C),C)
    Abar=[[int(i!=j)-A45[i][j] for j in range(45)] for i in range(45)]
    assert G==add(eye(45),Abar,24,3)
    assert rank_mod(C)==45

    # Integer projectors, scalar multiples of the spectral projectors:
    # Q20=(12I-A45)(A45+3I)=54 P20; Q15=(A40-12I)(A40-2I)=96 P15.
    Q20=mm(add(eye(45),A45,12,-1),add(A45,eye(45),1,3))
    Q15=mm(add(A40,eye(40),1,-12),add(A40,eye(40),1,-2))
    assert rank_mod(Q20)==20 and rank_mod(Q15)==15

    # B is the 40x45 support-incidence coupling.
    B=[[int(p in supports[m]) for m in range(45)] for p in range(40)]
    T20=mm(Q20,tr(C)) # 45 x 216 explicit circuit -> right-dark map
    assert rank_mod(T20)==20
    assert all(x==0 for row in mm(B,T20) for x in row)
    # On P20, C^T C=12 I; integer form Q20 G Q20 = 648 Q20.
    assert mm(mm(Q20,G),Q20)==[[648*x for x in row] for row in Q20]

    # Build native PSp and circuit stabilizer H=S5.
    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*form(x,v)%3
                y=norm(tuple((x[k]+z*v[k])%3 for k in range(4)));p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)};gens45=[]
    for p in gens40:gens45.append(tuple(si[frozenset(p[x] for x in S)] for S in supports))
    chosen=(18,62,77,10)
    Gpaired=closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen]);assert len(Gpaired)==25920
    cc0=set(circuits[0])
    H=[g for g in Gpaired if {g[1][x] for x in cc0}==cc0];assert len(H)==120
    o40=orbits(H,40,0);o45=orbits(H,45,1)
    fixed15=rank_mod(mm(Q15,indicators(o40,40)))
    fixed20=rank_mod(mm(Q20,indicators(o45,45)))

    out={
      'schema':'w33.20260829.circuit-dark-intertwiner.v1','status':'PASS',
      'circuitIncidence':{'shape':[216,45],'rank':45,'gram':'C^T C = 24 I + 3 A_complement(GQ(4,2))',
        'gramEigenvalues':{'trivial':120,'dark20':12,'shared24':30}},
      'rightDark20':{'integerProjector':'Q20=(12I-A45)(A45+3I)=54 P20','rank':20,
        'explicitMap':'T20=Q20 C^T : R^216 -> ker(B) subset R^45','mapRank':20,
        'exactNormIdentity':'Q20 (C^T C) Q20 = 648 Q20'},
      'circuitStabilizer':{'order':120,'structure':'S5','orbitsOnW33Points':[len(x) for x in o40],
        'orbitsOnGQPoints':[len(x) for x in o45],
        'fixedDimensionLeft15':fixed15,'fixedDimensionRight20':fixed20},
      'frobeniusReading':'fixedDimensionLeft15/right20 are the multiplicities of those irreducibles in the 216-point circuit permutation module.',
      'boundary':'Exact finite representation/intertwiner statement. The 216 circuits are not a qutrit-Clifford torsor; this audit concerns their PSp/S5 permutation module only.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
