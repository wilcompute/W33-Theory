#!/usr/bin/env python3
"""Pass4871 — recover the adjoint Lie bracket from Levi incidence alone.

Reconstruct the Pass4858 ten-dimensional quotient Q10 from the GQ(4,2) Levi
cycle space. Using only its exact PSp/PGSp generator matrices, solve
Hom_G(Lambda^2 Q10,Q10). The unique nonzero map is then checked directly for
Jacobi, center, derived algebra, and full-group equivariance.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/PART_W33_PASS4871_INTRINSIC_LEVI_ADJOINT_BRACKET.json"

def Q6(v):
    a,c,d,e,f,g=v;return (a*c+d*e+f+f*g+g)&1
def add2(a,b):return tuple(x^y for x,y in zip(a,b))
def polar(a,b):return Q6(add2(a,b))^Q6(a)^Q6(b)
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def closure(gens,n=27):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S
def rref(M,p=3):
    A=np.array(M,dtype=int)%p;r=0;piv=[]
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c);r+=1
        if r==A.shape[0]:break
    return A,piv
def rank(M,p=3):return len(rref(M,p)[1])
def null(M,p=3):
    R,piv=rref(M,p);free=[c for c in range(R.shape[1]) if c not in piv];out=[]
    for f in free:
        x=np.zeros(R.shape[1],dtype=int);x[f]=1
        for i,c in enumerate(piv):x[c]=(-R[i,f])%p
        out.append(x)
    return np.array(out,dtype=int)
def invm(A,p=3):
    A=np.array(A,dtype=int)%p;n=A.shape[0];X=np.c_[A,np.eye(n,dtype=int)]
    for c in range(n):
        q=next(i for i in range(c,n) if X[i,c]);X[[c,q]]=X[[q,c]]
        X[c]=(X[c]*pow(int(X[c,c]),-1,p))%p
        for i in range(n):
            if i!=c and X[i,c]:X[i]=(X[i]-X[i,c]*X[c])%p
    return X[:,n:]%p

def wedge(R):
    P=list(itertools.combinations(range(10),2));W=np.zeros((45,45),dtype=int)
    for a,(i,j) in enumerate(P):
        for b,(k,l) in enumerate(P):W[a,b]=(R[i,k]*R[j,l]-R[i,l]*R[j,k])%3
    return W

def hom_null(As,Bs):
    m=As[0].shape[0];n=Bs[0].shape[0];rows=[]
    for A,B in zip(As,Bs):
        for i in range(m):
            nz=np.flatnonzero(A[i])
            for j in range(n):
                z=np.zeros(m*n,dtype=int)
                for k in nz:z[k*n+j]=(z[k*n+j]+A[i,k])%3
                for l in range(n):
                    if B[l,j]:z[i*n+l]=(z[i*n+l]-B[l,j])%3
                rows.append(z)
    return null(np.array(rows,dtype=int),3)

def main()->int:
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0];nons=[v for v in vecs if Q6(v)==1];si={v:i for i,v in enumerate(sing)}
    trans=[]
    for v in nons:
        p=[]
        for x in sing:p.append(si[add2(x,v) if polar(x,v) else x])
        trans.append(tuple(p))
    gf=[];S={tuple(range(27))}
    for g in trans:
        T=closure(gf+[g])
        if len(T)>len(S):gf.append(g);S=T
        if len(S)==51840:break
    assert len(S)==51840
    gp=[];S={tuple(range(27))}
    for g in [comp(trans[0],t) for t in trans[1:]]:
        T=closure(gp+[g])
        if len(T)>len(S):gp.append(g);S=T
        if len(S)==25920:break
    assert len(S)==25920

    qp=[sum(bit<<i for i,bit in enumerate(v)) for v in sing]
    pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(lines[i])&set(lines[j]):G.add_edge(i,j)
    ledges=sorted((p,L) for L,S in enumerate(lines) for p in S);lei={e:i for i,e in enumerate(ledges)}
    D=np.zeros((72,135),dtype=int)
    for e,(p,L) in enumerate(ledges):D[p,e]=1;D[45+L,e]=-1
    HB=null(D,3);assert HB.shape==(64,135)
    KV=[]
    for S6 in itertools.combinations(range(27),6):
        H=G.subgraph(S6)
        if H.number_of_edges()!=9 or set(dict(H.degree()).values())!={3} or not nx.is_bipartite(H):continue
        A,B=nx.algorithms.bipartite.sets(H)
        if len(A)!=3 or len(B)!=3:continue
        v=np.zeros(135,dtype=int)
        for a in A:
            for b in B:
                if G.has_edge(a,b):
                    p=next(iter(set(lines[a])&set(lines[b])))
                    v[lei[(p,a)]]=1;v[lei[(p,b)]]=2
        KV.append(v)
    KV=np.array(KV);assert KV.shape==(360,135) and rank(KV,3)==54
    sel=[]
    for v in KV:
        if rank(np.array(sel+[v.tolist()]),3)>len(sel):sel.append(v.tolist())
        if len(sel)==54:break
    B64=np.array(sel,dtype=int)
    for v in HB:
        if rank(np.vstack([B64,v]),3)>len(B64):B64=np.vstack([B64,v])
        if len(B64)==64:break
    _,pc=rref(B64,3);Pi=invm(B64[:,pc],3)
    co=lambda v:(np.array(v,dtype=int)[pc]@Pi)%3
    point_lines=[frozenset(L for L,S in enumerate(lines) if p in S) for p in range(45)]
    pl={T:i for i,T in enumerate(point_lines)}
    def qmat(g):
        pg=[pl[frozenset(g[L] for L in T)] for T in point_lines]
        ep=[lei[(pg[p],g[L])] for p,L in ledges]
        R=np.zeros((64,64),dtype=int)
        for i,v in enumerate(B64):
            w=np.zeros(135,dtype=int)
            for j,x in enumerate(v):
                if x:w[ep[j]]=x
            R[i]=co(w)
        assert not np.any(R[:54,54:])
        return R[54:,54:]%3
    QP=[qmat(g) for g in gp];QF=[qmat(g) for g in gf]

    HP=hom_null([wedge(A) for A in QP],QP)
    HF=hom_null([wedge(A) for A in QF],QF)
    assert HP.shape==(1,450) and HF.shape==(1,450)
    assert rank(np.vstack([HP[0],HF[0]]),3)==1
    X=HP[0].reshape(45,10)%3;assert rank(X,3)==10

    pairs=list(itertools.combinations(range(10),2));pi={p:i for i,p in enumerate(pairs)}
    def bb(i,j):
        if i==j:return np.zeros(10,dtype=int)
        if i<j:return X[pi[(i,j)]].copy()
        return (-X[pi[(j,i)]])%3
    def br(a,b):
        z=np.zeros(10,dtype=int)
        for i,ai in enumerate(a):
            if ai:
                for j,bj in enumerate(b):
                    if bj:z=(z+ai*bj*bb(i,j))%3
        return z
    E=np.eye(10,dtype=int)
    for i,j,k in itertools.product(range(10),repeat=3):
        assert not np.any((br(E[i],br(E[j],E[k]))+br(E[j],br(E[k],E[i]))+br(E[k],br(E[i],E[j])))%3)
    center_rows=[]
    for j in range(10):
        M=np.zeros((10,10),dtype=int)
        for i in range(10):M[i]=bb(i,j)
        center_rows.append(M.T)
    center_dim=10-rank(np.vstack(center_rows),3)
    assert center_dim==0 and rank(X,3)==10

    out={
      "pass":4871,
      "source":"Levi H1 / oriented-K3,3 span over F3; no O5 coordinates used",
      "module_dimension":10,
      "equivariant_alternating_products":{"PSp_Hom_Lambda2Q_to_Q_dimension":1,
        "PGSp_Hom_Lambda2Q_to_Q_dimension":1,"same_line_up_to_scalar":True,
        "unique_nonzero_map_rank":10},
      "Lie_checks":{"Jacobi_all_1000_basis_triples":True,"center_dimension":center_dim,
        "derived_dimension":rank(X,3),"perfect":True},
      "comparison":"Pass4864's O5/Lambda2 construction is now an independent cross-certificate: the bracket is already forced up to F3^* scalar by the incidence-derived module action.",
      "theorem":"The ten-dimensional ternary Levi quotient carries a unique nonzero PSp- and PGSp-equivariant alternating product Lambda^2 Q10 -> Q10 up to scalar. That product is surjective, centerless, perfect, and satisfies Jacobi. Therefore the finite Lie algebra structure Q10 ~= sp4(F3) is intrinsic to the Levi incidence action; O5(3) coordinates are not needed to define the bracket.",
      "boundary":"Finite characteristic-three Lie-algebra theorem. Uniqueness up to nonzero F3 scalar does not select a continuum normalization or physical gauge coupling."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
