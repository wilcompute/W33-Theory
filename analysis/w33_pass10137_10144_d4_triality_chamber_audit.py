#!/usr/bin/env python3
"""Pass10137-10144: audit the proposed D4-triality / BT-chamber dictionary.

The parallel packet attributed the pairing of six chamber layers to the Galois
involution tau of L/K and then identified an order-3 D4 triality with a cycle of
those pairs.  The first step is false:

    tau(t) = -t/(1+t) = unit * t,

so tau preserves every t-adic ideal and every filtration degree.  The three
opposite pairs come instead from HERMITIAN SELF-DUALITY of the six-step flag.

At the level of chamber TYPES, reversal r=(1 6)(2 5)(3 4) has centralizer

    C_{S6}(r) = C2 wr S3 = C2^3 : S3, order 48.

Its quotient S3 permutes the three dual pairs, so there is an exact abstract
TRIALITY SLOT: an order-3 element may cycle the three pairs.  Identifying that
chosen S3 with the outer automorphism S3 of D4 requires additional root/lattice
data and is not canonical from the chamber alone.

A useful guard against another count match: this order-48 chamber-pair group is
NOT isomorphic to the projective U2(3) order-48 group acting on the chamber-
selected W33.  Their element-order distributions differ.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10137_10144_D4_TRIALITY_CHAMBER_AUDIT.json'
P=3

def comp(p,q): return tuple(p[q[i]] for i in range(len(p)))
def pinv(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def porder(p):
    I=tuple(range(len(p)));x=I
    for k in range(1,100):
        x=comp(p,x)
        if x==I:return k
    raise RuntimeError

def mat_rank(M):
    A=np.array(M,dtype=np.int64)%P;m,n=A.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,P))%P
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
        r+=1
    return r

def mkey(M):return tuple(int(x) for x in (np.array(M,dtype=np.int64)%P).ravel())
def proj_key(M):
    a=mkey(M);b=mkey((-np.array(M,dtype=np.int64))%P);return min(a,b)
def proj_order(M):
    I=np.eye(4,dtype=np.int64)%P;X=np.eye(4,dtype=np.int64)%P
    for k in range(1,100):
        X=X@M%P
        if np.array_equal(X,I) or np.array_equal(X,(-I)%P):return k
    raise RuntimeError

def main():
    # Exact centralizer of self-dual reversal on six chamber types.
    r=(5,4,3,2,1,0)
    S6=list(itertools.permutations(range(6)))
    C=[p for p in S6 if comp(p,r)==comp(r,p)]
    assert len(C)==48
    cdist=Counter(porder(p) for p in C)
    assert cdist==Counter({2:19,4:12,3:8,6:8,1:1})
    pairs=[frozenset((0,5)),frozenset((1,4)),frozenset((2,3))]
    pidx={x:i for i,x in enumerate(pairs)}
    induced=[]
    for p in C:
        induced.append(tuple(pidx[frozenset(p[i] for i in pair)] for pair in pairs))
    image=set(induced);assert len(image)==6
    kernel=sum(x==(0,1,2) for x in induced);assert kernel==8

    # Recompute the projective U2(3) order-48 W33 centralizer distribution.
    J=np.array([[0,1],[2,0]],dtype=np.int64)%P
    K=np.block([[J,np.zeros((2,2),dtype=np.int64)],[np.zeros((2,2),dtype=np.int64),J]])%P
    R=np.block([[np.zeros((2,2),dtype=np.int64),2*np.eye(2,dtype=np.int64)],
                [np.eye(2,dtype=np.int64),np.zeros((2,2),dtype=np.int64)]])%P
    group=[]
    for vals in itertools.product(range(P),repeat=8):
        A=np.array(vals[:4],dtype=np.int64).reshape(2,2)%P
        B=np.array(vals[4:],dtype=np.int64).reshape(2,2)%P
        X=np.block([[A,2*B],[B,A]])%P
        if mat_rank(X)==4 and np.array_equal(X.T@K@X%P,K):group.append(X)
    assert len(group)==96 and all(np.array_equal(X@R%P,R@X%P) for X in group)
    reps={}
    for X in group:reps.setdefault(proj_key(X),X)
    assert len(reps)==48
    udist=Counter(proj_order(X) for X in reps.values())
    assert udist==Counter({4:24,3:8,6:8,2:7,1:1})
    assert cdist!=udist

    out={
      'schema':'w33.pass10137_10144.d4_triality_chamber_audit.v1','status':'PASS','passes':'10137-10144',
      'galois_correction':{'tau_t':'-t/(1+t)=unit*t','effect':'tau preserves every t^j O_L and its filtration degree','consequence':'Galois conjugation does NOT pair j with 5-j and supplies no layer-cycling C3.'},
      'self_dual_pair_group':{'reversal':'(1 6)(2 5)(3 4)','centralizer_in_S6_order':48,'structure':'C2 wr S3 = C2^3:S3','pair_permutation_image':'S3','kernel_order':8,'element_order_distribution':dict(sorted(cdist.items()))},
      'triality_slot':{'exact_statement':'The quotient S3 permuting the three self-dual layer pairs has the same abstract group as Out(D4)=S3.','not_yet_proved':'No canonical root-theoretic intertwiner identifies the chamber-pair S3 with D4 triality.'},
      'order48_no_count_match':{'chamber_pair_group_distribution':dict(sorted(cdist.items())),'projective_U2_3_W33_distribution':dict(sorted(udist.items())),'isomorphic':False,'reason':'different numbers of involutions/order-4 elements'},
      'theorem':'The three BT layer pairs come from Hermitian self-duality, not Galois conjugation. Their exact chamber-type symmetry is C2 wr S3 of order 48 with an S3 quotient, giving a legitimate abstract D4-triality slot. But this S3 is not canonically identified with D4 triality, and the order-48 pair group is not the projective U2(3) W33 group.',
      'boundary':'Finite permutation/matrix computations are exhaustive. The D4 connection is retained only as an abstract S3-intertwiner target until an explicit D4 root/lattice map is constructed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','pair_group':48,'pair_quotient':'S3','same_as_U2proj':False}))
    return 0
if __name__=='__main__':raise SystemExit(main())
