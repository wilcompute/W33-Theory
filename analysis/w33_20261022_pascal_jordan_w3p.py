#!/usr/bin/env python3
"""Pascal-Jordan theorem for W(3,p) in defining characteristic.

B=J-I-A is the noncollinearity matrix and B_xy=<x,y>^(p-1).
For every prime p, rank_Fp(B)=C(p+2,3) and B^2=0.
Uses independent exact modular elimination for p=2,3,5,7.
The rank is classical (Chandler–Sin–Xiang 2010), not newly discovered.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np

def normalize(v,p):
    a=next(x for x in v if x)
    inv=pow(a,-1,p)
    return tuple((x*inv)%p for x in v)

def symplectic(a,b,p):
    return (a[0]*b[2]-a[2]*b[0]+a[1]*b[3]-a[3]*b[1])%p

def geometry(p):
    points=sorted({normalize(v,p) for v in itertools.product(range(p),repeat=4) if any(v)})
    n=(p+1)*(p*p+1)
    assert len(points)==n
    A=np.zeros((n,n),dtype=np.int64)
    for i in range(n):
        for j in range(i+1,n):
            if not symplectic(points[i],points[j],p):
                A[i,j]=A[j,i]=1
    return points,A

def modular_rank(matrix,p):
    M=np.asarray(matrix,dtype=np.int64).copy()%p
    rows,cols=M.shape;rank=0
    for col in range(cols):
        where=np.flatnonzero(M[rank:,col])
        if not len(where):continue
        rr=rank+int(where[0])
        M[[rank,rr]]=M[[rr,rank]]
        M[rank]=(M[rank]*pow(int(M[rank,col]),-1,p))%p
        for i in range(rank+1,rows):
            if M[i,col]:M[i]=(M[i]-M[i,col]*M[rank])%p
        rank+=1
        if rank==rows:break
    return rank

def one_prime(p):
    assert p in (2,3,5,7)
    pts,A=geometry(p)
    n=len(pts)
    I=np.eye(n,dtype=np.int64);J=np.ones((n,n),dtype=np.int64)
    B=(J-I-A)%p
    # Independent polynomial formula, exact on projective points.
    for i,x in enumerate(pts):
        assert all(B[i,j]==pow(symplectic(x,y,p),p-1,p)
                   for j,y in enumerate(pts))
    assert not np.any((B@B)%p)
    assert np.array_equal(((A+I)@(A+I))%p,J%p)
    assert np.array_equal((A+I)%p,(J-B)%p)
    assert not np.any((B@J)%p)
    assert not np.any((J@B)%p)
    d=math.comb(p+2,3)
    br=modular_rank(B,p)
    ar=modular_rank(A+I,p)
    assert br==d and ar==d+1
    assert modular_rank(A,p)==n-1
    singles=(n-1)-2*d
    assert singles>=0
    return {"p":p,"vertices":n,"rank_B":br,"rank_A_plus_I":ar,
            "Jordan_size2_minus1":d,"Jordan_size1_minus1":singles,
            "zero_eigenvalue_dimension":1,
            "Pascal_binomial":f"C({p+2},3)",
            "B_squared_zero":True}

def certificate():
    cases=[one_prime(p) for p in (2,3,5,7)]
    assert [r["Jordan_size2_minus1"] for r in cases]==[4,10,35,84]
    return {
        "status":"PASS_EXACT_MODULAR","classical_RH_proved":False,
        "theorem":"For W(3,p), p prime, B=J-I-A is square-zero over Fp, rank(B)=C(p+2,3).",
        "proof":"B_xy=<x,y>^(p-1). Such (p-1)th powers of all linear forms span homogeneous degree-(p-1) polynomials on Fp^4 (multinomial coefficients nonzero mod p). Their evaluation on projective points is injective (degree<p). SRG relations give B²=0.",
        "Jordan":"The nonconstant adjacency module has C(p+2,3) blocks J_2(-1), and (p+1)(p²+1)-1-2*C(p+2,3) blocks J_1(-1).",
        "phi_extension_boundary":"Extending Fp to Fp² via phi does not remove the square-zero Jordan blocks: rank and nonsemisimplicity are unchanged under scalar extension.",
        "prior_art":"p-ranks of W(3,q) studied by Chandler, Sin, Xi (2010), and earlier symplectic incidence literature. New only as a repo cross-track Pascal/phinary interpretation.",
        "cases":cases
    }
if __name__=="__main__":
    r=certificate()
    out=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_pascal_jordan_w3p.json"
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print([(x["p"],x["Jordan_size2_minus1"]) for x in r["cases"]])
