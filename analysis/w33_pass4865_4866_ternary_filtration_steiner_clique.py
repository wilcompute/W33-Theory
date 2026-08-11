#!/usr/bin/env python3
"""Passes 4865–4866 — ternary Levi radical filtration and Steiner clique obstruction.

4865:
  * reconstruct H1 of the GQ(4,2) Levi graph over F3;
  * reconstruct the 54D span of oriented K3,3 witnesses;
  * use the canonical edge dot product to find the 29D radical;
  * classify the radical submodule lattice by an exhaustive split-element eigenvector scan;
  * certify simple factors 14,5,10,25, two nonsplit extensions, and the canonical
    nondegenerate 25 ⊥ 10 quotient.

4866:
  * reconstruct the 36-double-six SRG(36,20,10,12);
  * characterize the 120 Steiner triangles as graph-theoretic maximal triangles;
  * compute the full clique-complex boundary ranks in characteristics 2 and 3;
  * prove the one-dimensional even-triangle H2 defect is characteristic-2-only;
  * identify H2(F3) with the 120 Steiner-coordinate permutation module and prove
    there is no PSp-equivariant linear map to/from the Pass4864 adjoint 10-space.

The group action is generated directly from the 36 orthogonal transvections of
Q^-(5,2), avoiding any graph-isomorphism enumeration.
"""
from __future__ import annotations
import itertools, json, math
from collections import Counter, deque
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT65=ROOT/"data/PART_W33_PASS4865_TERNARY_LEVI_RADICAL_FILTRATION.json"
OUT66=ROOT/"data/PART_W33_PASS4866_STEINER_CLIQUE_HOMOLOGY_OBSTRUCTION.json"

def Q6(v):
    a,c,d,e,f,g=v
    return (a*c+d*e+f+f*g+g)&1

def add2(a,b): return tuple(x^y for x,y in zip(a,b))
def polar(a,b): return Q6(add2(a,b))^Q6(a)^Q6(b)
def comp(p,q): return tuple(p[q[i]] for i in range(len(q)))

def closure(gens,n=27):
    I=tuple(range(n)); S={I}; D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S: S.add(z);D.append(z)
    return S

def porder(p):
    seen=[False]*len(p); o=1
    for i in range(len(p)):
        if seen[i]: continue
        j=i; l=0
        while not seen[j]:
            seen[j]=True;l+=1;j=p[j]
        o=math.lcm(o,l)
    return o

def rref(M,p=3):
    A=np.array(M,dtype=int)%p; r=0; piv=[]
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None: continue
        A[[r,q]]=A[[q,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c);r+=1
        if r==A.shape[0]: break
    return A,piv

def rank(M,p=3): return len(rref(M,p)[1])

def rank_fast(M,p=3):
    A=np.array(M,dtype=np.int8)%p; m,n=A.shape; r=0
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if len(nz)==0: continue
        q=r+int(nz[0]); A[[r,q]]=A[[q,r]]
        if p==3 and A[r,c]==2: A[r]=(2*A[r])%3
        inds=np.flatnonzero(A[:,c]); inds=inds[inds!=r]
        if len(inds):
            fac=A[inds,c].copy()
            A[inds]=(A[inds]-fac[:,None]*A[r])%p
        r+=1
        if r==m: break
    return r

def null(M,p=3):
    R,piv=rref(M,p); free=[c for c in range(R.shape[1]) if c not in piv]; out=[]
    for f in free:
        x=np.zeros(R.shape[1],dtype=int);x[f]=1
        for i,c in enumerate(piv): x[c]=(-R[i,f])%p
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

def rowbasis(M,p=3):
    R,piv=rref(M,p); return R[:len(piv)]

class Span3:
    def __init__(self,n): self.n=n; self.rows={}
    def add(self,x):
        x=np.array(x,dtype=np.int8)%3
        for p in sorted(self.rows):
            if x[p]: x=(x-x[p]*self.rows[p])%3
        nz=np.flatnonzero(x)
        if len(nz)==0:return False
        p=int(nz[0])
        if x[p]==2:x=(2*x)%3
        for q in list(self.rows):
            if self.rows[q][p]:self.rows[q]=(self.rows[q]-self.rows[q][p]*x)%3
        self.rows[p]=x;return True
    def basis(self):return np.array([self.rows[p] for p in sorted(self.rows)],dtype=int)
    def dim(self):return len(self.rows)

def cyclic(v,mats):
    sp=Span3(len(v)); D=deque()
    if sp.add(v):D.append(np.array(v,dtype=int)%3)
    while D:
        x=D.popleft()
        for A in mats:
            y=(x@A)%3
            if sp.add(y):D.append(y)
    return sp.basis()

def keyspace(B):return tuple(map(tuple,rowbasis(B,3).tolist()))

def projvecs(E):
    E=np.array(E,dtype=int);d=len(E)
    for n in range(1,3**d):
        x=n;c=[]
        for _ in range(d):c.append(x%3);x//=3
        if next((z for z in c if z),None)!=1:continue
        yield (np.array(c,dtype=int)@E)%3

def wordmat(mats,w):
    R=np.eye(mats[0].shape[0],dtype=int)
    for i in w:R=(R@mats[i])%3
    return R

def extend_basis(S,M):
    T=rowbasis(S,3)
    for b in rowbasis(M,3):
        if rank(np.vstack([T,b]),3)>len(T):T=np.vstack([T,b])
        if len(T)==rank(M,3):break
    return T

def sub_action(B,mats):
    B=rowbasis(B,3);_,pc=rref(B,3)
    out=[]
    for A in mats:
        R=np.zeros((len(B),len(B)),dtype=int)
        for i,b in enumerate(B):
            y=(b@A)%3;c=y[pc]%3
            assert np.array_equal((c@B)%3,y)
            R[i]=c
        out.append(R)
    return B,out

def quotient_actions(S,M,mats):
    S=rowbasis(S,3);T=extend_basis(S,M);s=len(S);_,pc=rref(T,3);Ti=invm(T[:,pc],3);out=[]
    for A in mats:
        R=np.zeros((len(T),len(T)),dtype=int)
        for i,b in enumerate(T):R[i]=((b@A)%3)[pc]@Ti%3
        assert not np.any(R[:s,s:])
        out.append(R[s:,s:])
    return T,out

def split_irred(acts,w):
    n=acts[0].shape[0];W=wordmat(acts,w);prof=Counter();tested=0
    for lam in (1,2):
        E=null((W-lam*np.eye(n,dtype=int)).T,3)
        for v in projvecs(E):
            prof[len(cyclic(v,acts))]+=1;tested+=1
    return tested,dict(prof)

def split_ranks(acts,s):
    n=acts[0].shape[0];q=n-s;unk=q*s;rows=[];rhs=[]
    for R in acts:
        A=R[:s,:s];C=R[s:,:s];D=R[s:,s:]
        assert not np.any(R[:s,s:])
        for i in range(q):
            for j in range(s):
                z=np.zeros(unk,dtype=np.int8)
                for k in range(q):z[k*s+j]=(z[k*s+j]+D[i,k])%3
                for l in range(s):z[i*s+l]=(z[i*s+l]-A[l,j])%3
                rows.append(z);rhs.append(C[i,j])
    M=np.array(rows,dtype=np.int8);b=np.array(rhs,dtype=np.int8)
    return unk,rank_fast(M,3),rank_fast(np.c_[M,b],3)

def hom_dim(As,Bs):
    m=As[0].shape[0];n=Bs[0].shape[0];rows=[]
    for A,B in zip(As,Bs):
        for i in range(m):
            nz=np.flatnonzero(A[i])
            for j in range(n):
                z=np.zeros(m*n,dtype=np.int8)
                for k in nz:z[k*n+j]=(z[k*n+j]+A[i,k])%3
                for l in range(n):
                    if B[l,j]:z[i*n+l]=(z[i*n+l]-B[l,j])%3
                rows.append(z)
    M=np.array(rows,dtype=np.int8)
    return m*n-rank_fast(M,3)

def boundary_rank(simplices,lower_index,p):
    if p==2:
        piv={}
        for s in simplices:
            bits=0
            for i in range(len(s)):bits^=1<<lower_index[tuple(s[:i]+s[i+1:])]
            while bits:
                q=bits.bit_length()-1
                if q in piv:bits^=piv[q]
                else:piv[q]=bits;break
        return len(piv)
    sp=Span3(max(lower_index.values())+1)
    for s in simplices:
        v=np.zeros(sp.n,dtype=np.int8)
        for i in range(len(s)):
            v[lower_index[tuple(s[:i]+s[i+1:])]]=1 if i%2==0 else 2
        sp.add(v)
    return sp.dim()

def main():
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0];nons=[v for v in vecs if Q6(v)==1]
    assert (len(sing),len(nons))==(27,36)
    si={v:i for i,v in enumerate(sing)}
    trans=[]
    for v in nons:
        p=[]
        for x in sing:
            y=add2(x,v) if polar(x,v) else x
            p.append(si[y])
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
    assert len(S)==25920 and len(gp)>=5

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
    def fullmat(g):
        pg=[pl[frozenset(g[L] for L in T)] for T in point_lines]
        ep=[lei[(pg[p],g[L])] for p,L in ledges]
        R=np.zeros((64,64),dtype=int)
        for i,v in enumerate(B64):
            w=np.zeros(135,dtype=int)
            for j,x in enumerate(v):
                if x:w[ep[j]]=x
            R[i]=co(w)
        assert not np.any(R[:54,54:])
        return R%3
    RP=[fullmat(g) for g in gp];RF=[fullmat(g) for g in gf]

    Gram=B64@B64.T%3
    Rad=null(Gram,3);assert Rad.shape==(29,64) and rank(Rad[:,54:],3)==0
    R29=rowbasis(Rad[:,:54],3);assert len(R29)==29 and rank(Gram[:54,:54],3)==25
    T54=R29.copy()
    for e in np.eye(54,dtype=int):
        if rank(np.vstack([T54,e]),3)>len(T54):T54=np.vstack([T54,e])
        if len(T54)==54:break
    T64=np.zeros((64,64),dtype=int);T64[:54,:54]=T54;T64[54:,54:]=np.eye(10,dtype=int)
    Ti=invm(T64,3)
    RPT=[T64@A@Ti%3 for A in RP];RFT=[T64@A@Ti%3 for A in RF]
    Gm=T64@Gram@T64.T%3
    assert not np.any(Gm[:29,:]) and rank(Gm[29:,29:],3)==35 and rank(Gm[29:54,29:54],3)==25

    Rmods=[A[:29,:29] for A in RPT]
    w=[4,2,1]
    pp=tuple(range(27))
    for i in w:pp=comp(pp,gp[i])
    assert porder(pp)==6
    A6=wordmat(Rmods,w)
    spaces={}
    for lam in (1,2):
        E=null((A6-lam*np.eye(29,dtype=int)).T,3)
        for v in projvecs(E):
            B=cyclic(v,Rmods);spaces[keyspace(B)]=len(B)
    assert Counter(spaces.values())==Counter({14:1,19:1,24:1,29:1})
    bd={d:np.array(k,dtype=int) for k,d in spaces.items()}
    S14,M19,M24,R29b=bd[14],bd[19],bd[24],bd[29]
    inter=lambda A,B:len(A)+len(B)-rank(np.vstack([A,B]),3)
    assert inter(S14,M19)==inter(S14,M24)==inter(M19,M24)==14
    assert rank(np.vstack([M19,M24]),3)==29
    assert all(rank(np.vstack([B,(b@A)%3]),3)==len(B)
               for B in (S14,M19,M24,R29b) for A in [x[:29,:29] for x in RFT] for b in B)

    _,A14=sub_action(S14,Rmods)
    _,A5=quotient_actions(S14,M19,Rmods)
    _,A10=quotient_actions(S14,M24,Rmods)
    _,A10b=quotient_actions(M19,R29b,Rmods)
    _,A5b=quotient_actions(M24,R29b,Rmods)
    A25=[A[29:54,29:54] for A in RPT]
    irr={}
    for name,acts in (("14",A14),("19_over_14",A5),("24_over_14",A10),
                      ("29_over_19",A10b),("29_over_24",A5b),("54_over_29",A25)):
        tested,prof=split_irred(acts,w)
        assert prof=={acts[0].shape[0]:tested}
        irr[name]={"tested":tested,"all_cyclic_spans":acts[0].shape[0]}

    s64P=split_ranks(RPT,54);s64F=split_ranks(RFT,54)
    KP=[A[:54,:54] for A in RPT];KF=[A[:54,:54] for A in RFT]
    s54P=split_ranks(KP,29);s54F=split_ranks(KF,29)
    assert s64P[1:]==(540,541) and s64F[1:]==(540,541)
    assert s54P[1:]==(725,726) and s54F[1:]==(725,726)

    G35=Gm[29:,29:]
    O10=rowbasis(null(G35[:,:25].T,3),3)
    assert O10.shape==(10,35) and rank(O10@G35@O10.T,3)==10 and not np.any(O10@G35[:,:25]%3)
    W35P=[A[29:,29:] for A in RPT];W35F=[A[29:,29:] for A in RFT]
    _,O10P=sub_action(O10,W35P);_,O10F=sub_action(O10,W35F)
    Q10P=[A[54:,54:] for A in RPT];Q10F=[A[54:,54:] for A in RFT]
    assert hom_dim(O10P,Q10P)==hom_dim(Q10P,O10P)==1
    assert hom_dim(O10F,Q10F)==hom_dim(Q10F,O10F)==1

    out65={
      "pass":4865,"ambient_Levi_H1_dimension_F3":64,"K33_generated_submodule_dimension":54,
      "canonical_edge_pairing":{"ambient_rank":35,"ambient_radical_dimension":29,
        "K33_restriction_rank":25,"K33_radical_dimension":29,
        "ambient_radical_contained_in_K33_submodule":True},
      "PSp_submodule_lattice":{"radical_dimension":29,"proper_nonzero_submodule_dimensions":[14,19,24],
        "diamond":{"intersection_19_24":14,"sum_19_24":29,"14_in_19":True,"14_in_24":True},
        "composition_factor_dimensions_radical":[14,5,10],
        "composition_factor_dimensions_K33":[14,5,10,25],
        "composition_factor_dimensions_H1":[14,5,10,25,10],
        "irreducibility_certificates":irr},
      "PGSp_invariance":{"radical":True,"submodule_14":True,"submodule_19":True,"submodule_24":True},
      "extensions":{"0_to_54_to_64_to_10":{
          "PSp":{"unknowns":s64P[0],"coefficient_rank":s64P[1],"augmented_rank":s64P[2],"splits":False},
          "PGSp":{"unknowns":s64F[0],"coefficient_rank":s64F[1],"augmented_rank":s64F[2],"splits":False}},
        "0_to_29_to_54_to_25":{
          "PSp":{"unknowns":s54P[0],"coefficient_rank":s54P[1],"augmented_rank":s54P[2],"splits":False},
          "PGSp":{"unknowns":s54F[0],"coefficient_rank":s54F[1],"augmented_rank":s54F[2],"splits":False}}},
      "nondegenerate_quotient":{"H1_over_radical_dimension":35,"K33_over_radical_dimension":25,
        "orthogonal_complement_dimension":10,"orthogonal_complement_nondegenerate":True,
        "PSp_Hom_to_original_adjoint10_dimension":1,"PGSp_Hom_to_original_adjoint10_dimension":1,
        "orthogonal_decomposition":"H1/rad = (K33/rad)_25 orthogonal-sum Q10"},
      "ATLAS_crosscheck":"U4(2)=S4(3)=PSp(4,3) lists all faithful characteristic-3 irreducibles in dimensions 5,10,14,25,81; the repo-derived nontrivial irreducible factors 5,10,14,25 match these classes.",
      "theorem":"The canonical F3 edge pairing on Levi H1 has a 29-dimensional radical contained in the 54-dimensional oriented-K3,3 submodule. That radical has the exact PSp/PGSp-invariant diamond 14 < {19,24} < 29, with simple factors 14,5,10; the quotient 54/29 is irreducible 25. Both 29->54->25 and 54->64->10 are nonsplit for PSp and PGSp. After quotienting the pairing radical, H1/rad is nondegenerate and decomposes canonically as 25 orthogonal-sum 10, with the 10-space explicitly isomorphic to the previously certified adjoint quotient.",
      "boundary":"Finite characteristic-three module and bilinear-form theorem. ATLAS labels are external cross-checks; no continuum field or particle interpretation follows."}
    OUT65.write_text(json.dumps(out65,indent=2,sort_keys=True)+"\n")

    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6];assert len(C6)==72
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        H=G.subgraph(A|B)
        if len(A|B)==12 and H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda S:tuple(sorted(S)));assert len(DS)==36
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    assert H36.number_of_edges()==360 and set(dict(H36.degree()).values())=={20}
    E=sorted(tuple(sorted(e)) for e in H36.edges());ei={e:i for i,e in enumerate(E)}
    tri=[]
    for a,b,c in itertools.combinations(range(36),3):
        if H36.has_edge(a,b) and H36.has_edge(a,c) and H36.has_edge(b,c):tri.append((a,b,c))
    tri=sorted(tri);assert len(tri)==1200
    odd=[t for t in tri if len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0];oddset=set(odd);even=[t for t in tri if t not in oddset]
    assert (len(even),len(odd))==(1080,120)
    maxc=[tuple(sorted(c)) for c in nx.find_cliques(H36)]
    K5=sorted(c for c in maxc if len(c)==5);K3m=sorted(c for c in maxc if len(c)==3)
    assert (len(K5),len(K3m))==(216,120) and set(K3m)==oddset
    K4=sorted(set(tuple(sorted(s)) for C in K5 for s in itertools.combinations(C,4)));assert len(K4)==1080
    assert all(sum(tuple(sorted(f)) in oddset for f in itertools.combinations(C,3))==0 for C in K4)
    for t in even:
        cn=set(range(36))
        for v in t:cn&=set(H36.neighbors(v))
        assert len(cn)==4 and sum(set(t).issubset(C) for C in K5)==2
    for t in odd:
        cn=set(range(36))
        for v in t:cn&=set(H36.neighbors(v))
        assert len(cn)==0
    ti={t:i for i,t in enumerate(tri)};k4i={c:i for i,c in enumerate(K4)}
    vindex={(i,):i for i in range(36)}
    ranks={}
    for p in (2,3):
        ranks[p]=[boundary_rank(E,vindex,p),boundary_rank(tri,ei,p),boundary_rank(K4,ti,p),boundary_rank(K5,k4i,p)]
        assert ranks[p]==[35,325,755,216]
    er2,er3=boundary_rank(even,ei,2),boundary_rank(even,ei,3)
    or2,or3=boundary_rank(odd,ei,2),boundary_rank(odd,ei,3)
    assert (er2,er3,or2,or3)==(324,325,120,120)
    betti=[1,360-35-325,1200-325-755,1080-755-216,216-216]
    assert betti==[1,0,120,109,0]

    di={S:i for i,S in enumerate(DS)};oti={t:i for i,t in enumerate(odd)};P120=[]
    for g in gp:
        dp=[di[frozenset(g[x] for x in S)] for S in DS]
        op=[oti[tuple(sorted(dp[i] for i in t))] for t in odd]
        P=np.zeros((120,120),dtype=np.int8)
        for i,j in enumerate(op):P[i,j]=1
        P120.append(P)
    assert hom_dim(P120,Q10P)==0 and hom_dim(Q10P,P120)==0

    out66={
      "pass":4866,"double_six_graph":"SRG(36,20,10,12)",
      "clique_complex":{"f_vector":[36,360,1200,1080,216],"maximal_cliques":{"K5":216,"K3":120},"maximum_clique_size":5},
      "Steiner_graph_only_characterization":{"Steiner_triangles":120,"even_triangles":1080,
        "Steiner_triangles_equal_maximal_K3":True,"Steiner_triangle_common_neighbor_count":0,
        "even_triangle_common_neighbor_count":4,"even_triangle_K5_containment_count":2,
        "every_K4_has_only_even_triangle_faces":True},
      "boundary_ranks":{"F2":{"d1":35,"d2":325,"d3":755,"d4":216},
                        "F3":{"d1":35,"d2":325,"d3":755,"d4":216}},
      "clique_homology":{"F2_betti":betti,"F3_betti":betti},
      "even_triangle_boundary_span":{"F2_rank":er2,"F3_rank":er3,
        "odd_Steiner_triangle_boundary_rank_F2":or2,"odd_Steiner_triangle_boundary_rank_F3":or3,
        "F2_even_supported_H2_dimension":1080-er2-755,
        "F3_even_supported_H2_dimension":1080-er3-755,
        "F3_restriction_H2_to_120_Steiner_coordinates":"isomorphism",
        "F2_restriction_H2_to_120_Steiner_coordinates_rank":119},
      "adjoint_linear_bridge_obstruction":{"H2_F3_identified_with":"120-dimensional permutation module on maximal/Steiner triangles",
        "target":"Pass4864 adjoint Q10 ~= sp4(F3)","Hom_PSp_H2_to_Q10_dimension":0,
        "Hom_PSp_Q10_to_H2_dimension":0,"nonzero_equivariant_linear_bridge_exists":False},
      "theorem":"The 120 Steiner triangles are intrinsically the maximal triangles of the 36-double-six graph: every other triangle extends through exactly four common neighbors and lies in two K5 cliques. The clique complex has f=(36,360,1200,1080,216) and Betti numbers (1,0,120,109,0) over both F2 and F3. The 1080 non-Steiner triangles span only 324 boundary dimensions over F2 but all 325 over F3; equivalently the even-supported H2 defect is one-dimensional only in characteristic 2. Over F3, H2 is canonically the 120-dimensional permutation module on Steiner triangles, and exact common-generator Hom calculations give Hom_PSp(H2,Q10)=Hom_PSp(Q10,H2)=0. Thus there is no linear PSp-equivariant Steiner-H2/adjoint bridge; any bridge must be nonlinear, characteristic-changing, or use extra structure.",
      "boundary":"Finite graph/clique-homology and modular-representation theorem. No physical phase or gauge field follows from the obstruction."}
    OUT66.write_text(json.dumps(out66,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"4865":out65,"4866":out66},indent=2,sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
