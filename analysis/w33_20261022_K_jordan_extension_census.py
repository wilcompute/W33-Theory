#!/usr/bin/env python3
"""Exact modular dual-quotient Jordan census for p=2,3,5,7.

The observed K decomposition is conjectural in all prime characteristics.
Q is the separately certified CSS logical quotient and is not identified
with a split direct summand of K.
"""
from itertools import product
import json
from pathlib import Path
import numpy as np

J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=np.int64)


def norm(v,p):
    v=[int(a)%p for a in v]
    t=next(a for a in v if a)
    return tuple(a*pow(t,-1,p)%p for a in v)


def rank_reduced(matrix,p):
    a=np.array(matrix,dtype=np.int64,copy=True)%p
    r=0
    for col in range(a.shape[1]):
        if r==a.shape[0]:break
        candidates=np.flatnonzero(a[r:,col])
        if not len(candidates):continue
        k=r+int(candidates[0])
        a[[k,r]]=a[[r,k]]
        a[r]=(a[r]*pow(int(a[r,col]),-1,p))%p
        factors=a[:,col].copy()
        factors[r]=0
        a=(a-factors[:,None]*a[r])%p
        r+=1
    return a[:r]


def sample(p):
    pts=sorted({norm(v,p) for v in product(range(p),repeat=4) if any(v)})
    x=np.asarray(pts,dtype=np.int64)
    n=len(pts)
    B=((x@J@x.T)%p!=0).astype(np.int64)
    C=rank_reduced(B,p)
    lk={z:i for i,z in enumerate(pts)}
    w=x[0]
    perm=[lk[norm(v+(int(v@J@w)%p)*w,p)] for v in x]
    T=np.zeros((n,n),dtype=np.int64)
    T[np.arange(n),perm]=1
    delta=(T-np.eye(n,dtype=np.int64))%p
    power=np.eye(n,dtype=np.int64)
    ranks=[n-len(C)]
    for k in range(1,p+1):
        power=power@delta%p
        ranks.append(len(rank_reduced(np.vstack((C,power)),p))-len(C))
    blocks={j:int(ranks[j-1]-2*ranks[j]+ranks[j+1]) for j in range(1,p)}
    blocks[p]=int(ranks[p-1])
    predict={1:(p*p+p+4)//2}
    predict.update({j:j for j in range(2,p)})
    predict[p]=p*(p+1)//2
    if p==2:
        # At p=2 the size-p and size-2 expressions are the same.
        predict={1:5,2:3}
    assert blocks==predict, (p,blocks,predict)
    return {"p":p,"physical_n":n,"stabilizer_dim":len(C),
            "K_dimension":n-len(C),"rank_powers_K":ranks,
            "Jordan_K":{str(j):v for j,v in blocks.items()},
            "uniform_K_conjecture_matches":True}


def run():
    return {"schema":"w33.K_jordan_extension_census.v1",
            "result_status":"FINITE_CERTIFIED_P2_P3_P5_P7_GENERAL_FORMULA_CONJECTURAL",
            "module":"K=C^perp is dual to M/C under coordinate dot product",
            "conjectural_formula":"K: J1^((p^2+p+4)/2) + sum_(j=2)^(p-1) Jj^j + Jp^(p(p+1)/2)",
            "proof_boundary":"An extension class calculation for arbitrary p is still missing. K is not generally C direct-sum Q as cyclic modules.",
            "samples":[sample(p) for p in [2,3,5,7]]}


if __name__=="__main__":
    import sys
    s=json.dumps(run(),indent=2)+"\n"
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(s,encoding="utf-8")
    else:print(s,end="")
