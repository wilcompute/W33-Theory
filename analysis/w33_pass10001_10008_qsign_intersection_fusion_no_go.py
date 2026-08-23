#!/usr/bin/env python3
"""Pass10001-10008: test the coarsest common fusion of the Q-/Q+ 7,371 two-space schemes.

Pass9909-9916 proved the full natural coherent configurations are nonisomorphic.
The next possibility is a common COARSE fusion.  The most canonical fusion
for Grassmannian two-spaces forgets orthogonal subtype and remembers only
intersection dimension: self / meet in a projective point / disjoint.

Both Q-(5,3) and Q+(5,3) nondegenerate candidate sets have the SAME valencies
1, 320, 7050 for this fusion.  That tempting match still fails: the point-
intersection graphs have different exact spectra.

If B is the 7371 x 364 incidence matrix between nondegenerate two-spaces and
projective points of PG(5,3), then for distinct rows (BB^T)_{UV}=1 exactly when
U,V meet in one projective point, while the diagonal is 4.  Thus A=BB^T-4I.
The nonzero spectrum of BB^T equals that of M=B^T B.  We certify the small
364 x 364 integer matrix M by an exact annihilating polynomial and recover
multiplicities from exact traces.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
from collections import Counter
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10001_10008_QSIGN_INTERSECTION_FUSION_NO_GO.json'
P=3


def rref(A):
    A=np.array(A,dtype=np.int64)%P;m,n=A.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]),None)
        if q is None:continue
        if q!=r:A[[r,q]]=A[[q,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,P))%P
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
        r+=1
        if r==m:break
    return A,r

def rank(A):return rref(A)[1]

def canon(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            u=pow(x,-1,P);return tuple(u*y%P for y in v)
    raise ValueError

def points():return sorted({canon(v) for v in itertools.product(range(P),repeat=6) if any(v)})

def two_spaces(pts):
    S=set()
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            R,r=rref([pts[i],pts[j]])
            if r==2:S.add(tuple(tuple(int(x) for x in row) for row in R[:2]))
    S=sorted(S);assert len(S)==11011;return S

def kind(U,C):
    X=np.array(U,dtype=np.int64).T%P;G=X.T@C@X%P
    if rank(G)<2:return 'degenerate'
    for z in ((1,0),(0,1),(1,1),(1,2)):
        q=np.array(z,dtype=np.int64)
        if int(q@G@q)%P==0:return 'hyperbolic'
    return 'anisotropic'

def incidence(good,pts):
    idx={p:i for i,p in enumerate(pts)}
    B=np.zeros((len(good),len(pts)),dtype=np.int64)
    coeff=((1,0),(0,1),(1,1),(1,2))
    for r,U in enumerate(good):
        R=np.array(U,dtype=np.int64)
        for a,b in coeff:
            p=canon((a*R[0]+b*R[1])%P)
            B[r,idx[p]]=1
    assert np.all(B.sum(axis=1)==4)
    return B

def exact_spectrum_small(M,eigs):
    n=M.shape[0]
    I=np.eye(n,dtype=np.int64)
    # Exact annihilating polynomial product(M-lambda I)=0. Values fit int64 here.
    Z=I.copy()
    for lam in eigs:Z=Z@(M-lam*I)
    assert not np.any(Z)
    powers=[np.eye(n,dtype=np.int64)]
    for _ in range(1,len(eigs)):powers.append(powers[-1]@M)
    traces=[int(np.trace(X)) for X in powers]
    V=sp.Matrix([[sp.Integer(lam)**k for lam in eigs] for k in range(len(eigs))])
    mult=list(V.inv()*sp.Matrix(traces))
    mult=[int(x) for x in mult]
    assert sum(mult)==n and all(x>=0 for x in mult)
    return dict(zip(eigs,mult)),traces

def analyze(C,eigs):
    pts=points();S=two_spaces(pts)
    good=[U for U in S if kind(U,C)!='degenerate'];assert len(good)==7371
    B=incidence(good,pts)
    pdeg=B.sum(axis=0)
    deg=B@pdeg-4
    assert np.all(deg==320)
    M=B.T@B
    spec,tr=exact_spectrum_small(M,eigs)
    assert spec.get(0)==1
    rankB=363
    Aspec={lam-4:m for lam,m in spec.items() if lam!=0}
    Aspec[-4]=len(good)-rankB
    assert sum(Aspec.values())==7371
    return {'fusion_valencies':{'self':1,'meet_in_point':320,'disjoint':7050},
            'BtB_spectrum':{str(k):v for k,v in sorted(spec.items())},
            'intersection_graph_spectrum':{str(k):v for k,v in sorted(Aspec.items())},
            'BtB_traces':tr,'rank_B':rankB}

def main():
    Cm=np.eye(6,dtype=np.int64)%P
    Cp=np.diag([1,1,1,1,1,2]).astype(np.int64)%P
    minus=analyze(Cm,[0,72,84,90,324])
    plus=analyze(Cp,[0,72,78,90,324])
    assert minus['fusion_valencies']==plus['fusion_valencies']
    assert minus['intersection_graph_spectrum']!=plus['intersection_graph_spectrum']
    assert minus['BtB_spectrum']=={'0':1,'72':160,'84':90,'90':112,'324':1}
    assert plus['BtB_spectrum']=={'0':1,'72':130,'78':90,'90':142,'324':1}
    out={'schema':'w33.pass10001_10008.qsign_intersection_fusion_no_go.v1','status':'PASS','passes':'10001-10008',
         'Qminus':minus,'Qplus':plus,
         'theorem':('The coarsest canonical intersection-dimension fusion has identical valencies (1,320,7050) on the Q- and Q+ 7,371 candidate sets, but the point-intersection graphs are spectrally distinct. Q- has spectrum 320^1,86^112,80^90,68^160,(-4)^7008; Q+ has 320^1,86^142,74^90,68^130,(-4)^7008. Hence even this natural fusion is not an isomorphism.'),
         'consequence':'The only automatic common intersection-only fusion left is the trivial complete-graph fusion self/nonself; any useful weld must use a less symmetric external relation or additional controller data.',
         'boundary':'Exact exhaustive finite enumeration. Spectra are certified by exact integer annihilating polynomials for B^T B and exact trace/multiplicity recovery; no floating-point eigenvalue claim is used.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','valency':320,'minus':minus['intersection_graph_spectrum'],'plus':plus['intersection_graph_spectrum']}))
    return 0
if __name__=='__main__':raise SystemExit(main())
