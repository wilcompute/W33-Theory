#!/usr/bin/env python3
"""Pass7733-7740: the Leech dual-40 code is the one-line augmentation of the
common quadratic code underneath all 234 W33 symplectic overlays.

Pass7653 gives the canonical Leech point/hyperplane PG(3,3) interface.
Pass7717 gives its ternary incidence code [40,11,13]_3.
Pass5744-5751 independently gave the polarity-independent quadratic code
[40,10,18]_3 and 234 W33 overlays sharing that code.

For every nondegenerate alternating polarity on PG(3,3), let A be W33 adjacency,
N=I+A its closed-neighbourhood/polar-incidence matrix, and Q=J-I-A the
noncollinearity matrix. Over F3 the SRG identity gives N^2=J. Consequently
row(Q)=row(N) intersect 1^perp, and row(N)=<1> orthogonal-sum row(Q).
This script verifies the identity simultaneously for all 234 labelled polarities.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7733_7740_LEECH_QUADRATIC_CODE_WELD.json'

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError

def rref(M,p=3):
    X=np.asarray(M,dtype=np.int64).copy()%p;m,n=X.shape;r=0
    for c in range(n):
        z=next((i for i in range(r,m) if X[i,c]),None)
        if z is None:continue
        X[[r,z]]=X[[z,r]];X[r]=(X[r]*pow(int(X[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and X[i,c]:X[i]=(X[i]-int(X[i,c])*X[r])%p
        r+=1
        if r==m:break
    return X[:r].astype(np.int8)

def rank4(M):return len(rref(M,3))==4

def main():
    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});n=40
    I=np.eye(n,dtype=np.int8);J=np.ones((n,n),dtype=np.int8)
    commonN=commonQ=None;count=0
    for a,b,c,d,e,f in itertools.product(range(3),repeat=6):
        M=np.array([[0,a,b,c],[-a,0,d,e],[-b,-d,0,f],[-c,-e,-f,0]],dtype=np.int8)%3
        if not rank4(M):continue
        vals=[a,b,c,d,e,f];first=next(x for x in vals if x)
        if first==2:continue # one representative of {M,-M}
        A=np.zeros((n,n),dtype=np.int8)
        for x in range(n):
          u=np.asarray(P[x],dtype=np.int8)
          for y in range(x+1,n):
            if int(u@M@np.asarray(P[y],dtype=np.int8))%3==0:A[x,y]=A[y,x]=1
        assert set(map(int,A.sum(1)))=={12}
        N=(I+A)%3;Q=(J-I-A)%3
        assert np.array_equal((N.astype(int)@N.astype(int))%3,J%3)
        RN,RQ=rref(N),rref(Q);assert RN.shape==(11,40) and RQ.shape==(10,40)
        assert np.max((RQ.astype(int)@RQ.astype(int).T)%3)==0
        assert all(int(row.sum())%3==0 for row in RQ)
        if commonN is None:commonN,commonQ=RN,RQ
        else:
            assert np.array_equal(RN,commonN) and np.array_equal(RQ,commonQ)
        count+=1
    assert count==234
    one=np.ones(40,dtype=np.int8);assert np.array_equal(rref(np.vstack([commonQ,one])),commonN)
    assert np.all((commonQ.astype(int)@one.astype(int))%3==0) and int(one@one)%3==1

    weights=Counter()
    for z in range(3**10):
        q=z;c=np.zeros(10,dtype=np.int8)
        for i in range(10):c[i]=q%3;q//=3
        w=(c.astype(np.int16)@commonQ.astype(np.int16))%3
        weights[int(np.count_nonzero(w))]+=1
    expected={0:1,18:1560,24:21060,27:18800,30:16848,36:780};assert dict(sorted(weights.items()))==expected

    out={
      'schema':'w33.pass7733_7740.leech_quadratic_code_weld.v1','status':'PASS','passes':'7733-7740',
      'dependencies':['Pass7653 Leech dual PG(3,3)','Pass7717 Leech [40,11,13]_3 incidence code','Pass5744-5751 common [40,10,18]_3 quadratic code and 234 W33 overlays'],
      'universal_mod3_identity':'For every W33 polarization, N=I+A and N^2=J over F3; Q=J-N is the noncollinearity matrix.',
      'all_234_closed_neighborhood_rowspaces_equal':True,'all_234_noncollinearity_rowspaces_equal':True,
      'Leech_incidence_code':{'parameters':'[40,11,13]_3','decomposition':'<1> perp C_quad'},
      'common_quadratic_core':{'parameters':'[40,10,18]_3','self_orthogonal':True,'weight_enumerator':{str(k):v for k,v in expected.items()}},
      'canonicality_gain':'Although Pass7653 does not canonically choose one of the 234 symplectic polarities, the ternary code layer is independent of that choice. The Leech interface therefore reaches the common W33 quadratic code before a specific W33 graph is selected.',
      'theorem':'The canonical Leech dual-PG(3,3) incidence code is exactly the orthogonal one-line augmentation of the polarity-independent ternary quadratic code shared by all 234 W33 symplectic overlays: C_Leech=<1> perp C_quad.',
      'novelty_boundary':'Pass5744-5751 already owns the quadratic code, its [40,10,18]_3 parameters, and the 234-overlay invariance. Pass7733 supplies the new objectwise weld from the corrected Leech order-9 linking interface to that existing common code layer.',
      'claim_boundary':'Exact finite coding/projective-geometry theorem; no physical encoding or decoder-performance claim is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','overlays':234,'Leech':'[40,11,13]_3','core':'[40,10,18]_3','polarization_independent':True}))
if __name__=='__main__':main()
