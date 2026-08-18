#!/usr/bin/env python3
"""Passes 7130--7137: execute the five q=9 frontier attacks plus three outside-box probes.

Exact finite results only.  No claim that alpha(W(3,9)) is 51 is made here.

7130 blocker-hypergraph deficiency reformulation (global, not merely local)
7131 exact PΓSp(4,9) setwise stabilizer of the recovered 51-set
7132 rank-four Gram anchor compression
7133 intrinsic four-set fingerprint / blocker-orbit refinement
7134 q=7 positive control with a frozen 33-set
7135 Frobenius-union recombination no-go via a perfect matching
7136 quadratic-character switching-class q mod 4 dichotomy
7137 fixed-line mechanism behind the unique 80 <-> 40 local swap
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS7130_7137_STRUCTURAL_ATTACK.json"

S9 = [22,24,78,80,88,95,141,144,149,177,182,189,190,191,200,213,214,230,234,258,271,276,288,331,336,364,368,376,397,403,449,450,478,480,539,561,570,580,588,622,651,655,658,741,750,753,756,780,784,801,814]
S7 = [8,76,79,86,89,90,123,132,133,139,148,149,154,165,192,200,209,211,224,257,265,283,286,296,304,336,338,357,360,372,375,387,395]
A9 = [[1,0,0,0],[1,2,3,6],[3,0,5,6],[3,0,4,7]]
A7 = [[2,2,0,6],[0,5,0,0],[0,6,2,3],[0,0,0,5]]
J9 = [[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]]
J7 = [[0,1,0,0],[6,0,0,0],[0,0,0,1],[0,0,6,0]]

# ---------------------------------------------------------------- GF(9)
ADD = [[0]*9 for _ in range(9)]
MUL = [[0]*9 for _ in range(9)]
for x in range(9):
    a,b=x%3,x//3
    for y in range(9):
        c,d=y%3,y//3
        ADD[x][y] = ((a+c)%3) + 3*((b+d)%3)
        MUL[x][y] = ((a*c + 2*b*d)%3) + 3*((a*d+b*c)%3)
NEG=[((-x%3)%3)+3*((-(x//3))%3) for x in range(9)]
INV={}
for x in range(1,9):
    for y in range(1,9):
        if MUL[x][y] == 1:
            INV[x]=y; break


def ga(a,b): return ADD[a][b]
def gm(a,b): return MUL[a][b]
def gn(a): return NEG[a]
def gd(a,b): return MUL[a][INV[b]]
def gp(a,n):
    r=1
    while n:
        if n&1: r=gm(r,a)
        a=gm(a,a); n//=2
    return r

def fr(a): return gp(a,3)
def gsum(xs):
    r=0
    for x in xs: r=ga(r,x)
    return r


def norm9(v):
    lead=next(x for x in v if x)
    z=INV[lead]
    return tuple(gm(x,z) for x in v)


def B9(u,v):
    x=ga(gm(u[0],v[1]), gn(gm(u[1],v[0])))
    return ga(x,ga(gm(u[2],v[3]),gn(gm(u[3],v[2]))))


def matmul9(A,B):
    return [[gsum(gm(A[i][k],B[k][j]) for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def matvec9(A,v): return [gsum(gm(A[i][j],v[j]) for j in range(len(v))) for i in range(len(A))]
def tr(M): return [list(x) for x in zip(*M)]


def invmat9(M):
    n=len(M)
    A=[list(M[i])+[1 if i==j else 0 for j in range(n)] for i in range(n)]
    for c in range(n):
        p=next(i for i in range(c,n) if A[i][c])
        A[c],A[p]=A[p],A[c]
        z=INV[A[c][c]]; A[c]=[gm(x,z) for x in A[c]]
        for i in range(n):
            if i==c or not A[i][c]: continue
            f=A[i][c]
            A[i]=[ga(A[i][j],gn(gm(f,A[c][j]))) for j in range(2*n)]
    return [r[n:] for r in A]


def rank9_cols(vecs):
    M=[[vecs[j][i] for j in range(len(vecs))] for i in range(4)]
    A=[r[:] for r in M]; r=0
    for c in range(len(vecs)):
        p=next((i for i in range(r,4) if A[i][c]),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]
        z=INV[A[r][c]]; A[r]=[gm(x,z) for x in A[r]]
        for i in range(4):
            if i!=r and A[i][c]:
                f=A[i][c]; A[i]=[ga(A[i][j],gn(gm(f,A[r][j]))) for j in range(len(vecs))]
        r+=1
        if r==4: break
    return r


def build9():
    pts=[]
    for v in itertools.product(range(9),repeat=4):
        if not any(v): continue
        pts.append(norm9(v))
    P=sorted(set(pts)); idx={p:i for i,p in enumerate(P)}
    adj=[set() for _ in P]
    for i in range(len(P)):
        for j in range(i+1,len(P)):
            if B9(P[i],P[j])==0:
                adj[i].add(j); adj[j].add(i)
    return P,idx,adj

# --------------------------------------------------------------- prime q=7

def normp(v,p):
    lead=next(x for x in v if x%p); z=pow(lead,-1,p)
    return tuple(x*z%p for x in v)

def Bp(u,v,p): return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%p

def buildp(p):
    P=sorted(set(normp(v,p) for v in itertools.product(range(p),repeat=4) if any(v)))
    idx={x:i for i,x in enumerate(P)}; adj=[set() for _ in P]
    for i in range(len(P)):
        for j in range(i+1,len(P)):
            if Bp(P[i],P[j],p)==0: adj[i].add(j); adj[j].add(i)
    return P,idx,adj

def matmul_p(A,B,p): return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%p for j in range(len(B[0]))] for i in range(len(A))]
def matvec_p(A,v,p): return [sum(A[i][j]*v[j] for j in range(len(v)))%p for i in range(len(A))]

# ---------------------------------------------------- matching-product invariant
# For four projective points (v,a,b,c), the three perfect-matching products
# [B(v,a)B(b,c), B(v,b)B(c,a), B(v,c)B(a,b)] scale together under independent
# representative rescaling.  Permuting a,b,c permutes the coordinates projectively.

def canon3_9(t):
    out=[]
    for perm in set(itertools.permutations(range(3))):
        u=tuple(t[i] for i in perm)
        for sigma in (0,1):
            w=tuple(fr(x) if sigma else x for x in u)
            if not any(w): out.append((0,0,0)); continue
            z=INV[next(x for x in w if x)]
            out.append(tuple(gm(x,z) for x in w))
    return min(out)

def canon3_p(t,p):
    out=[]
    for perm in set(itertools.permutations(range(3))):
        u=tuple(t[i]%p for i in perm)
        if not any(u): out.append((0,0,0)); continue
        z=pow(next(x for x in u if x),-1,p)
        out.append(tuple(x*z%p for x in u))
    return min(out)


def table9():
    reps={}; T=np.zeros((9,9,9),dtype=np.int16)
    for x in range(9):
      for y in range(9):
       for z in range(9):
        c=canon3_9((x,y,z)); reps.setdefault(c,len(reps)); T[x,y,z]=reps[c]
    return reps,T

def tablep(p):
    reps={}; T=np.zeros((p,p,p),dtype=np.int16)
    for x in range(p):
      for y in range(p):
       for z in range(p):
        c=canon3_p((x,y,z),p); reps.setdefault(c,len(reps)); T[x,y,z]=reps[c]
    return reps,T


def inside_fps(BM,T,mul,nclasses):
    n=len(BM); ans=[]
    for i in range(n):
        cnt=[0]*nclasses; oth=[j for j in range(n) if j!=i]
        for a,b,c in itertools.combinations(oth,3):
            x=mul(BM[i][a],BM[b][c]); y=mul(BM[i][b],BM[c][a]); z=mul(BM[i][c],BM[a][b])
            cnt[int(T[x,y,z])]+=1
        ans.append(tuple(cnt))
    return ans


def edge_fps(BM,T,mul,nclasses):
    n=len(BM); out={}
    for i in range(n):
      for j in range(i+1,n):
        cnt=[0]*nclasses; oth=[x for x in range(n) if x not in (i,j)]
        for k,l in itertools.combinations(oth,2):
            x=mul(BM[i][j],BM[k][l]); y=mul(BM[i][k],BM[l][j]); z=mul(BM[i][l],BM[j][k])
            cnt[int(T[x,y,z])]+=1
        out[(i,j)]=tuple(cnt)
    return out


def groups(vals):
    d=defaultdict(list)
    for i,x in enumerate(vals): d[x].append(i)
    return list(d.values())


def blocker_data(adj,S):
    S=set(S); outside=[v for v in range(len(adj)) if v not in S]
    bl={v:frozenset(adj[v]&S) for v in outside}
    return outside,bl,Counter(map(len,bl.values()))


def rank_mod(M,p):
    A=(np.array(M,dtype=int)%p).tolist(); m=len(A); n=len(A[0]); r=0
    for c in range(n):
        k=next((i for i in range(r,m) if A[i][c]%p),None)
        if k is None: continue
        A[r],A[k]=A[k],A[r]; z=pow(A[r][c]%p,-1,p)
        A[r]=[x*z%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]%p:
                f=A[i][c]%p; A[i]=[(A[i][j]-f*A[r][j])%p for j in range(n)]
        r+=1
    return r


def det_mod(M,p):
    A=(np.array(M,dtype=int)%p).tolist(); n=len(A); d=1
    for c in range(n):
        k=next((i for i in range(c,n) if A[i][c]%p),None)
        if k is None: return 0
        if k!=c: A[c],A[k]=A[k],A[c]; d=(-d)%p
        z=A[c][c]%p; d=d*z%p; inv=pow(z,-1,p)
        for i in range(c+1,n):
            if A[i][c]%p:
                f=A[i][c]*inv%p
                A[i]=[(A[i][j]-f*A[c][j])%p for j in range(n)]
    return d%p


def max_bip_matching(left,right,edges):
    nbr={u:[] for u in left}
    for u,v in edges: nbr[u].append(v)
    mt={}
    def aug(u,seen):
        for v in nbr[u]:
            if v in seen: continue
            seen.add(v)
            if v not in mt or aug(mt[v],seen): mt[v]=u; return True
        return False
    return sum(aug(u,set()) for u in left)


def main():
    P9,I9,adj9=build9(); assert len(P9)==820 and {len(x) for x in adj9}=={90}
    W9=[P9[i] for i in S9]; assert not any(b in adj9[a] for a,b in itertools.combinations(S9,2))
    out9,bl9,h9=blocker_data(adj9,S9)
    assert dict(sorted(h9.items()))=={1:1,2:22,3:50,4:102,5:156,6:120,7:142,8:107,9:53,10:16}
    assert sum(k*v for k,v in h9.items())==4590
    assert sum(comb(k,2)*v for k,v in h9.items())==12750

    # 7130: global deficiency equivalence and exact model dimensions.
    out_edges=sum(1 for u in out9 for v in adj9[u] if v in set(out9) and u<v)
    incid=sum(len(bl9[v]) for v in out9)
    assert out_edges==32310 and incid==4590

    # 7131/7133: intrinsic four-set fingerprints recover an exact C2 stabilizer.
    reps9,T9=table9(); assert len(reps9)==16
    BM9=[[B9(W9[i],W9[j]) for j in range(51)] for i in range(51)]
    vin9=inside_fps(BM9,T9,gm,len(reps9)); vg9=groups(vin9)
    assert Counter(map(len,vg9))==Counter({2:25,1:1})
    pi={}
    for g in vg9:
        if len(g)==1: pi[g[0]]=g[0]
        else: pi[g[0]]=g[1]; pi[g[1]]=g[0]
    assert [S9[i] for i in range(51) if pi[i]==i]==[80]
    ef9=edge_fps(BM9,T9,gm,len(reps9)); assert Counter(Counter(ef9.values()).values())==Counter({2:625,1:25})
    pcs=[g for g in vg9 if len(g)==2]
    def ec(a,b): return ef9[(a,b) if a<b else (b,a)]
    assert all(ec(a,b)!=ec(a,bp) for u,(a,ap) in enumerate(pcs) for b,bp in pcs[u+1:])

    assert matmul9(A9,A9)==[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    assert matmul9(tr(A9),matmul9(J9,A9))==[[gm(2,x) for x in r] for r in J9]
    g9={v:I9[norm9(matvec9(A9,P9[v]))] for v in range(820)}
    assert set(g9[x] for x in S9)==set(S9)
    assert all(g9[S9[i]]==S9[pi[i]] for i in range(51))

    # Exclude extra Frobenius-semilinear maps with the same two allowed point permutations.
    frame=(0,1,2,5,6)
    def candidate_count(target,sigma):
        dom=[W9[i] for i in frame]; img=[W9[target[i]] for i in frame]
        bd=[tuple(fr(x) for x in v) if sigma else v for v in dom[:4]]
        fifth=tuple(fr(x) for x in dom[4]) if sigma else dom[4]
        Bdom=[[bd[j][i] for j in range(4)] for i in range(4)]
        Bimg=[[img[j][i] for j in range(4)] for i in range(4)]
        c=matvec9(invmat9(Bdom),fifth); d=matvec9(invmat9(Bimg),img[4])
        lam=[gd(d[i],c[i]) for i in range(4)]
        Wlam=[[gm(img[j][i],lam[j]) for j in range(4)] for i in range(4)]
        A=matmul9(Wlam,invmat9(Bdom)); n=0
        for i,v in enumerate(W9):
            vv=tuple(fr(x) for x in v) if sigma else v
            if norm9(matvec9(A,vv))==W9[target[i]]: n+=1
        return n
    ident={i:i for i in range(51)}
    sem_counts={"id_linear":candidate_count(ident,0),"id_frobenius":candidate_count(ident,1),
                "pi_linear":candidate_count(pi,0),"pi_frobenius":candidate_count(pi,1)}
    assert sem_counts=={"id_linear":51,"id_frobenius":6,"pi_linear":51,"pi_frobenius":6}

    fixed9=[v for v in range(820) if g9[v]==v]; assert len(fixed9)==20
    eig9={1:[],2:[]}
    for v in fixed9:
        av=matvec9(A9,P9[v]); j=next(i for i,x in enumerate(P9[v]) if x); lam=gd(av[j],P9[v][j]); eig9[lam].append(v)
    assert {k:len(v) for k,v in eig9.items()}=={1:10,2:10}
    assert 80 in eig9[2] and 40 in eig9[2]
    assert all(B9(P9[a],P9[b])==0 for L in eig9.values() for a,b in itertools.combinations(L,2))

    orb9=defaultdict(lambda:{"fixed":0,"pairs":0,"vertices":0}); seen=set()
    for v in out9:
        if v in seen: continue
        w=g9[v]; b=len(bl9[v]); seen|={v,w}
        if w==v: orb9[b]["fixed"]+=1; orb9[b]["vertices"]+=1
        else: orb9[b]["pairs"]+=1; orb9[b]["vertices"]+=2

    # Projectively/semilinearly invariant outside fingerprints recover exactly those C2 orbits.
    triples=np.array(list(itertools.combinations(range(51),3)),dtype=np.int16); aa,bb,cc=triples.T
    bc=np.array([BM9[int(b)][int(c)] for b,c in zip(bb,cc)],dtype=np.int16)
    ca=np.array([BM9[int(c)][int(a)] for c,a in zip(cc,aa)],dtype=np.int16)
    ab=np.array([BM9[int(a)][int(b)] for a,b in zip(aa,bb)],dtype=np.int16)
    pair=np.array([[B9(P9[v],P9[s]) for s in S9] for v in out9],dtype=np.int16)
    fps=[]
    M=np.array(MUL,dtype=np.int16)
    for rp in pair:
        ids=T9[M[rp[aa],bc],M[rp[bb],ca],M[rp[cc],ab]]
        fps.append(tuple(np.bincount(ids,minlength=16).tolist()))
    fpg=defaultdict(list)
    for v,f in zip(out9,fps): fpg[f].append(v)
    assert Counter(map(len,fpg.values()))==Counter({2:375,1:19})
    assert all(set(g)==({g[0]} if g9[g[0]]==g[0] else {g[0],g9[g[0]]}) for g in fpg.values())

    # 7132: rank-four Gram anchor compression.
    anchors=(0,1,2,5); G=[[BM9[i][j] for j in anchors] for i in anchors]; Gi=invmat9(G)
    R=[[BM9[i][j] for j in anchors] for i in range(51)]
    def rec(i,j):
        z=gsum(gm(R[i][a],gm(Gi[a][b],R[j][b])) for a in range(4) for b in range(4))
        return gn(z)
    assert all(rec(i,j)==BM9[i][j] for i in range(51) for j in range(51))

    # 7135: exact Frobenius-union recombination no-go.
    SF={I9[norm9(tuple(fr(x) for x in P9[s]))] for s in S9}; inter=set(S9)&SF
    L=sorted(set(S9)-SF); Rf=sorted(SF-set(S9)); E=[(u,v) for u in L for v in (adj9[u]&set(Rf))]
    mm=max_bip_matching(L,Rf,E); assert (len(inter),len(L),len(Rf),len(E),mm)==(4,47,47,301,47)
    alpha_union=len(set(S9)|SF)-mm; assert alpha_union==51

    # 7134: q=7 positive control.
    P7,I7,adj7=buildp(7); assert len(P7)==400 and {len(x) for x in adj7}=={56}
    W7=[P7[i] for i in S7]; assert not any(b in adj7[a] for a,b in itertools.combinations(S7,2))
    out7,bl7,h7=blocker_data(adj7,S7); assert dict(sorted(h7.items()))=={2:17,3:56,4:77,5:74,6:65,7:46,8:32}
    assert sum(k*v for k,v in h7.items())==1848 and sum(comb(k,2)*v for k,v in h7.items())==4224
    reps7,T7=tablep(7); BM7=[[Bp(W7[i],W7[j],7) for j in range(33)] for i in range(33)]
    mul7=lambda a,b:(a*b)%7
    vi7=inside_fps(BM7,T7,mul7,len(reps7)); vg7=groups(vi7); assert Counter(map(len,vg7))==Counter({2:16,1:1})
    pi7={}
    for g in vg7:
        if len(g)==1: pi7[g[0]]=g[0]
        else: pi7[g[0]]=g[1]; pi7[g[1]]=g[0]
    ef7=edge_fps(BM7,T7,mul7,len(reps7)); pcs7=[g for g in vg7 if len(g)==2]
    e7=lambda a,b:ef7[(a,b) if a<b else (b,a)]
    assert all(e7(a,b)!=e7(a,bp) for u,(a,ap) in enumerate(pcs7) for b,bp in pcs7[u+1:])
    assert matmul_p(tr(A7),matmul_p(J7,A7,7),7)==[[3*x%7 for x in r] for r in J7]
    assert matmul_p(A7,A7,7)==[[4,0,0,0],[0,4,0,0],[0,0,4,0],[0,0,0,4]]
    g7={v:I7[normp(matvec_p(A7,P7[v],7),7)] for v in range(400)}
    assert set(g7[s] for s in S7)==set(S7) and [s for s in S7 if g7[s]==s]==[89]
    assert len([v for v in range(400) if g7[v]==v])==16

    orb7=defaultdict(lambda:{"fixed":0,"pairs":0,"vertices":0}); seen=set()
    for v in out7:
        if v in seen: continue
        w=g7[v]; b=len(bl7[v]); seen|={v,w}
        if w==v: orb7[b]["fixed"]+=1; orb7[b]["vertices"]+=1
        else: orb7[b]["pairs"]+=1; orb7[b]["vertices"]+=2

    # 7136: quadratic-character switching classes.
    sq9={gm(x,x) for x in range(1,9)}; chi9=lambda x:0 if x==0 else (1 if x in sq9 else -1)
    Q9=np.array([[0 if i==j else chi9(BM9[i][j]) for j in range(51)] for i in range(51)],dtype=int)
    sq7={x*x%7 for x in range(1,7)}; chi7=lambda x:0 if x==0 else (1 if x in sq7 else -1)
    Q7=np.array([[0 if i==j else chi7(BM7[i][j]) for j in range(33)] for i in range(33)],dtype=int)
    assert np.array_equal(Q9,Q9.T) and np.array_equal(Q7,-Q7.T)
    assert rank_mod(Q9,5)==51 and det_mod(Q9,5)==3
    assert rank_mod(Q7,3)==32  # odd skew matrix has rank <=32, so rank_Q=32 exactly.

    sp9=9**4*(9**2-1)*(9**4-1); pgamma9=2*sp9
    sp7=7**4*(7**2-1)*(7**4-1)
    cert={
      "schema":"w33.pass7130_7137.structural_attack.v1","status":"PASS",
      "pass_7130_blocker_deficiency":{
        "theorem":"For fixed independent S and outside independent T, replacing B(T)=union_{v in T}(N(v) cap S) by T gives an independent set. Therefore a larger independent set exists anywhere iff some outside independent T has |B(T)|-|T|<0.",
        "q9_model":{"outside_x":769,"witness_y":51,"binary_variables":820,"outside_edge_constraints":out_edges,"blocker_implications":incid},
        "proved_radius":"Pass7125 already proves deficiency >=0 for |T|<=8; the unrestricted MILP remains unresolved and no alpha=51 claim is made."},
      "pass_7131_stabilizer":{
        "order":2,"isomorphism":"C2","generator_matrix_GF9":A9,"generator_square":"I","similitude_multiplier":2,
        "inside_orbits":"1 + 25*2","unique_fixed_witness_point":80,"semilinear_frame_match_counts":sem_counts,
        "P_Gamma_Sp_order":pgamma9,"orbit_size":pgamma9//2},
      "pass_7132_gram_compression":{
        "anchor_witness_positions":list(anchors),"anchor_graph_indices":[S9[i] for i in anchors],"G":G,"G_inverse":Gi,
        "identity":"A_ij = - r_i G^{-1} r_j^T with r_i=(A_i,a) on four anchors","verified_entries":51*51,
        "target_52_variable_reduction":"after choosing a nonsingular four-anchor principal block, 48 four-entry rows plus the six anchor pairings determine all 1326 off-diagonal Gram entries: 198 field variables before further gauge reduction."},
      "pass_7133_blocker_orbits":{
        "intrinsic_fourset_types":16,"outside_fingerprint_classes":394,"outside_fingerprint_class_sizes":{"1":19,"2":375},
        "fingerprints_equal_C2_orbits":True,"blocker_orbits":{str(k):v for k,v in sorted(orb9.items())}},
      "pass_7134_q7_control":{
        "stored_size":33,"published_status":"Cimrakova et al. report 33 as the exhaustive W(7) maximum; publication provenance is recorded in the report, not proved by this certificate.",
        "blocker_histogram":{str(k):v for k,v in sorted(h7.items())},"zero_blockers":0,"one_blockers":0,
        "stabilizer_order":2,"inside_orbits":"1 + 16*2","unique_fixed_witness_point":89,"blocker_orbits":{str(k):v for k,v in sorted(orb7.items())},
        "PGSp_order":sp7,"orbit_size_under_PGSp":sp7//2},
      "pass_7135_frobenius_union":{
        "intersection":4,"symmetric_difference":94,"cross_graph_sides":[47,47],"cross_edges":301,"perfect_matching":47,
        "alpha_of_union":51,"proof":"The 4 common points are isolated in the union graph; the remaining 94-vertex graph is bipartite. Konig gives alpha=94-47+4=51 from the perfect matching."},
      "pass_7136_quadratic_character":{
        "q9":{"q_mod_4":1,"minus_one_square":True,"matrix_symmetry":"symmetric","size":51,"rank_over_Q":51,"certificate":"rank mod 5 = 51; det mod 5 = 3"},
        "q7":{"q_mod_4":3,"minus_one_square":False,"matrix_symmetry":"skew-symmetric","size":33,"rank_over_Q":32,"certificate":"rank mod 3 = 32; odd skew size forces rank <=32"},
        "boundary":"This is an algebraic q mod 4 resonance in quadratic-character switching classes, not a derivation of physical chirality."},
      "pass_7137_fixed_lines":{
        "q9_fixed_projective_points":20,"eigenspace_lines":{"lambda_1":eig9[1],"lambda_minus1":eig9[2]},
        "each_line_size":10,"each_line_totally_isotropic":True,"swap_fixed_pair":[80,40],
        "mechanism":"The C2 generator has multiplier -1 and two 2D eigenspaces. Each eigenspace is totally isotropic, so the projective fixed locus is two generator lines. Both 80 and 40 are fixed and lie on the same fixed line; the two-state local swap chooses which fixed point from that line is used."},
      "boundary":"Exact finite symplectic geometry only. q=9 optimality is still open; no physics inference is made."
    }
    OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(cert,indent=2,sort_keys=True))

if __name__=="__main__": main()
