#!/usr/bin/env python3
"""Pass9909-9916: exact orbital schemes on the 7,371 nondegenerate two-spaces.

The Q-(5,3) glue selector and Q+(5,3) Suzuki selector both contain 7,371
nondegenerate 2-spaces, but their hyperbolic/anisotropic splits differ.  This
pass goes beyond counts and computes the full stabilizer suborbits.

For a fixed nondegenerate U and another V, choose 2-column bases and form the
4-column matrix X=[U V].  Under the stabilizer of U, the complete finite
fingerprint is the Gram matrix X^T C X together with ker(X), modulo
O(C|U) on the U basis and GL(2,3) on the V basis.  Equality of fingerprints
gives a well-defined isometry U+V -> U+V' preserving U and V; Witt's extension
lemma extends it to O(C).  Hence these fingerprints are exactly the orbitals.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9909_9916_TWO_SPACE_ORBITAL_SCHEME.json'
P=3

def rref(A):
    A=np.array(A,dtype=np.int64)%P;m,n=A.shape;r=0;piv=[]
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]),None)
        if q is None:continue
        if q!=r:A[[r,q]]=A[[q,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,P))%P
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
        piv.append(c);r+=1
        if r==m:break
    return A,r,piv

def rank(A):return rref(A)[1]

def canon_point(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            u=pow(x,-1,P);return tuple(u*y%P for y in v)
    raise ValueError

def two_spaces():
    pts=sorted({canon_point(v) for v in itertools.product(range(P),repeat=6) if any(v)})
    assert len(pts)==364
    S=set()
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            R,r,_=rref([pts[i],pts[j]])
            if r==2:S.add(tuple(tuple(int(x) for x in row) for row in R[:2]))
    assert len(S)==11011
    return sorted(S)

def nullcols(A):
    R,r,piv=rref(A);n=A.shape[1];free=[c for c in range(n) if c not in piv]
    K=np.zeros((n,len(free)),dtype=np.int64)
    for j,f in enumerate(free):
        K[f,j]=1
        for i,p in enumerate(piv):K[p,j]=(-R[i,f])%P
    return K%P

def canon_kernel(K):
    if K.shape[1]==0:return b''
    R,r,_=rref(K.T)
    return R[:r].astype(np.uint8).tobytes()

def inv2(M):
    a,b,c,d=[int(x) for x in M.ravel()];det=(a*d-b*c)%P;u=pow(det,-1,P)
    return (u*np.array([[d,-b],[-c,a]],dtype=np.int64))%P

GL2=[]
for z in itertools.product(range(P),repeat=4):
    M=np.array(z,dtype=np.int64).reshape(2,2)
    if rank(M)==2:GL2.append(M)
assert len(GL2)==48
INV={M.astype(np.uint8).tobytes():inv2(M) for M in GL2}

def kind(U,C):
    B=np.array(U,dtype=np.int64).T%P;G=B.T@C@B%P
    if rank(G)<2:return 'degenerate'
    iso=False
    for z in ((1,0),(0,1),(1,1),(1,2)):
        q=np.array(z,dtype=np.int64)
        if int(q@G@q)%P==0:iso=True;break
    return 'hyperbolic' if iso else 'anisotropic'

def fingerprint(U,V,C):
    BU=np.array(U,dtype=np.int64).T%P;BV=np.array(V,dtype=np.int64).T%P
    GU=BU.T@C@BU%P
    OU=[A for A in GL2 if np.array_equal(A.T@GU@A%P,GU)]
    X=np.concatenate([BU,BV],axis=1)%P;Gram=X.T@C@X%P;rr=rank(X);Ker=nullcols(X)
    best=None
    for A in OU:
        Ai=INV[A.astype(np.uint8).tobytes()]
        for B in GL2:
            T=np.zeros((4,4),dtype=np.int64);T[:2,:2]=A;T[2:,2:]=B
            H=T.T@Gram@T%P
            if Ker.shape[1]:
                Ti=np.zeros((4,4),dtype=np.int64);Ti[:2,:2]=Ai;Ti[2:,2:]=INV[B.astype(np.uint8).tobytes()]
                kk=canon_kernel(Ti@Ker%P)
            else:kk=b''
            key=bytes([rr,Ker.shape[1]])+H.astype(np.uint8).tobytes()+kk
            if best is None or key<best:best=key
    return best

def subdegrees(spaces,C,base_kind):
    good=[U for U in spaces if kind(U,C)!='degenerate']
    U=next(U for U in good if kind(U,C)==base_kind)
    cnt=Counter(fingerprint(U,V,C) for V in good)
    return sorted(cnt.values())

def main():
    S=two_spaces()
    Cminus=np.eye(6,dtype=np.int64)%P
    Cplus=np.diag([1,1,1,1,1,2]).astype(np.int64)%P
    cm=Counter(kind(U,Cminus) for U in S);cp=Counter(kind(U,Cplus) for U in S)
    assert cm==Counter({'hyperbolic':4536,'degenerate':3640,'anisotropic':2835})
    assert cp==Counter({'hyperbolic':5265,'degenerate':3640,'anisotropic':2106})

    mh=subdegrees(S,Cminus,'hyperbolic')
    ma=subdegrees(S,Cminus,'anisotropic')
    ph=subdegrees(S,Cplus,'hyperbolic')
    pa=subdegrees(S,Cplus,'anisotropic')
    EXP_MH=[1,15,15,15,15,20,20,30,30,40,45,45,60,60,90,90,120,120,120,120,180,180,180,180,180,180,180,240,240,360,360,360,360,360,360,480,480,720,720]
    EXP_MA=[1,18,24,24,24,24,48,48,64,64,72,144,144,144,192,192,192,192,288,288,384,384,384,576,576,576,1152,1152]
    EXP_PH=[1,12,12,12,12,18,24,24,32,32,48,48,64,72,72,72,96,96,96,96,144,144,144,144,192,192,288,288,288,288,288,288,288,384,384,384,576,576,576,576]
    EXP_PA=[1,30,30,30,30,40,40,45,45,60,60,180,180,240,240,240,240,360,360,360,360,360,480,480,720,720,1440]
    assert mh==EXP_MH and ma==EXP_MA and ph==EXP_PH and pa==EXP_PA
    assert sum(mh)==sum(ma)==sum(ph)==sum(pa)==7371
    # Point stabilizer orders from orthogonal orbit-stabilizer.
    stabs={'minus_hyperbolic':5760,'minus_anisotropic':9216,'plus_hyperbolic':4608,'plus_anisotropic':11520}
    for n in mh:assert stabs['minus_hyperbolic']%n==0
    for n in ma:assert stabs['minus_anisotropic']%n==0
    for n in ph:assert stabs['plus_hyperbolic']%n==0
    for n in pa:assert stabs['plus_anisotropic']%n==0

    out={
      'schema':'w33.pass9909_9916.two_space_orbital_scheme.v1','status':'PASS','passes':'9909-9916',
      'candidate_totals':{'Qminus':dict(cm),'Qplus':dict(cp),'nondegenerate_each':7371},
      'exact_subdegrees':{
        'Qminus_hyperbolic_base':mh,'Qminus_anisotropic_base':ma,
        'Qplus_hyperbolic_base':ph,'Qplus_anisotropic_base':pa},
      'orbital_ranks':{'Qminus_hyperbolic_base':len(mh),'Qminus_anisotropic_base':len(ma),'Qplus_hyperbolic_base':len(ph),'Qplus_anisotropic_base':len(pa)},
      'stabilizer_orders':stabs,
      'classification_proof':('The canonical Gram+relation-kernel fingerprint is invariant under the base 2-space stabilizer. Equality produces an isometry between the two subspace sums carrying U to U and V to V prime; Witt extension promotes it to the ambient orthogonal group. Therefore fingerprint classes are exactly stabilizer suborbits.'),
      'theorem':('The natural derived coherent configurations on the two 7,371-element candidate sets are different. Q- has orbital ranks 39 and 28 from hyperbolic/anisotropic basepoints, while Q+ has ranks 40 and 27. Thus the common cardinality 7,371 does not extend to an isomorphism of their natural orthogonal two-space schemes.'),
      'boundary':'Exact exhaustive enumeration over all 11,011 two-spaces of F3^6 plus Witt extension. This rules out the natural orthogonal-scheme identification; it does not rule out a less symmetric external bijection.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','ranks':out['orbital_ranks']}))
    return 0
if __name__=='__main__':raise SystemExit(main())
