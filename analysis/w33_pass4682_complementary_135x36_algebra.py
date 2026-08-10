#!/usr/bin/env python3
"""Pass 4682 — close the joint algebra of the complementary 135x36 incidences.

Q is the Pass4663 deck-blind 135_4-36_15 incidence and M is the existing
135_8-36_30 code-minimum/spread incidence.  Reconstruct both from W33 and prove
that they span the same rational 36-space but have radically different integral
structure.  Their sum loses exactly the +3 eigenspace of the 36-object
SRG(36,15,6,6).
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,nullspace2,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4682_COMPLEMENTARY_135X36_ALGEBRA_REGEN.json'

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def rankp(M,p):
    A=np.asarray(M,dtype=np.int64).copy()%p;r=0
    for c in range(A.shape[1]):
        q=np.flatnonzero(A[r:,c])
        if len(q)==0:continue
        rr=r+int(q[0]);A[[r,rr]]=A[[rr,r]]
        inv=pow(int(A[r,c]),-1,p);A[r]=(A[r]*inv)%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-int(A[i,c])*A[r])%p
        r+=1
        if r==A.shape[0]:break
    return r

def smith(M):
    D=smith_normal_form(sp.Matrix(M.tolist()),domain=ZZ);z=[]
    for i in range(min(D.shape)):
        a=abs(int(D[i,i]));
        if a:z.append(a)
    return {str(k):int(v) for k,v in sorted(Counter(z).items())}

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8);apartments=sorted(tuple(map(int,a)) for a in apartments)
    j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]]);rep=lambda x:min(int(x),int(x)^j)
    def fib(ap):
        x=0
        for i in ap:x^=cols[i]
        return rep(x)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments});sing=sorted(set().union(*(set(L) for L in selected)));sidx={x:i for i,x in enumerate(sing)}
    N=np.zeros((135,270),dtype=np.uint8)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    B=nullspace2(N.T);bm=[]
    for b in B:
        m=0
        for i,z in enumerate(b):
            if int(z):m|=1<<i
        bm.append(m)
    words=[0]
    for b in bm:words += [x^b for x in words]
    minimum=sorted(w for w in words if w.bit_count()==30);assert len(minimum)==36

    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    def actv(x,g):return rep(pmask(rep(x),g))
    def actw(w,g):
        z=0
        for i in range(135):
            if (w>>i)&1:z|=1<<sidx[actv(sing[i],g)]
        return z
    byp=defaultdict(list)
    for li,L in enumerate(lines):
        for p in L:byp[p].append(li)
    spreads=[]
    def rec(chosen,used):
        if len(used)==40:spreads.append(frozenset(chosen));return
        p=next(x for x in range(40) if x not in used)
        for li in byp[p]:
            S=set(lines[li])
            if not(S&used):rec(chosen+[li],used|S)
    rec([],set());spreads=sorted(set(spreads),key=lambda S:tuple(sorted(S)));sI={S:i for i,S in enumerate(spreads)}
    def actS(S,g):return frozenset(g[i] for i in S)
    mI={w:i for i,w in enumerate(minimum)};w0=minimum[0];H=[g for g in G if actw(w0,g)==w0];fixed=[S for S in spreads if all(actS(S,g)==S for g in H)];assert len(fixed)==1;S0=fixed[0]
    tr={}
    for g in G:
        a=mI[actw(w0,g)];b=sI[actS(S0,g)]
        if a in tr:assert tr[a]==b
        tr[a]=b
    M=np.zeros((135,36),dtype=np.int64)
    for a,w in enumerate(minimum):
        b=tr[a]
        for i in range(135):
            if (w>>i)&1:M[i,b]=1

    ap0=apartments[0];K=[g for g in G if tuple(sorted(g[i] for i in ap0))==ap0];assert len(K)==16
    special=[]
    for S in spreads:
        if sum(actS(S,g)==S for g in K)==8:special.append(S)
    assert len(special)==4
    aI={a:i for i,a in enumerate(apartments)};seen={}
    for g in G:
        a=tuple(sorted(g[i] for i in ap0));ai=aI[a];U=frozenset(sI[actS(S,g)] for S in special)
        if ai in seen:assert seen[ai]==U
        seen[ai]=U
    Z=np.zeros((1620,36),dtype=np.uint8)
    for ai,U in seen.items():
        for s in U:Z[ai,s]=1
    byfib=defaultdict(set)
    for ai,a in enumerate(apartments):byfib[fib(a)].add(bytes(Z[ai]))
    Q=np.vstack([np.frombuffer(next(iter(byfib[x])),dtype=np.uint8) for x in sing]).astype(np.int64)
    assert set(map(int,Q.sum(1)))=={4} and set(map(int,Q.sum(0)))=={15}
    assert np.max((Q*M).sum(1))==0

    # 36-side exact association algebra.
    A36=np.zeros((36,36),dtype=np.int64)
    for a,b in itertools.combinations(range(36),2):
        if len(spreads[a]&spreads[b])==4:A36[a,b]=A36[b,a]=1
    I=np.eye(36,dtype=np.int64);J=np.ones((36,36),dtype=np.int64)
    assert np.array_equal(Q.T@Q,15*I+3*A36)
    assert np.array_equal(M.T@M,24*I+6*J)
    assert np.array_equal(Q.T@M,6*(J-I-A36)) and np.array_equal(Q.T@M,M.T@Q)
    S=Q+M
    assert np.array_equal(S.T@S,9*(3*I+2*J-A36))

    ranks={}
    for name,X in [('Q4',Q),('M8',M),('sum12',S)]:
        ranks[name]={'Q':int(sp.Matrix(X.tolist()).rank()),'F2':rankp(X,2),'F3':rankp(X,3),'F5':rankp(X,5),'smith':smith(X)}
    assert ranks['Q4']=={'Q':36,'F2':29,'F3':36,'F5':36,'smith':{'1':29,'2':6,'4':1}}
    assert ranks['M8']=={'Q':36,'F2':15,'F3':36,'F5':36,'smith':{'1':15,'2':14,'4':6,'8':1}}
    assert ranks['sum12']=={'Q':21,'F2':21,'F3':14,'F5':21,'smith':{'1':14,'3':7}}
    assert sp.Matrix(np.concatenate([Q,M],axis=1).tolist()).rank()==36

    # 135-side four-dimensional commutative Gram algebra.
    R44=Q@Q.T;R88=M@M.T;R48=Q@M.T
    assert np.array_equal(R48,R48.T)
    assert np.array_equal(R88,2*R44+R48)
    eig={
      'QQt':{'60':1,'24':15,'6':20,'0':99},
      'MMt':{'240':1,'24':35,'0':99},
      'QMt':{'120':1,'-24':15,'12':20,'0':99}}
    for X,key in [(R44,'QQt'),(R88,'MMt'),(R48,'QMt')]:
        got=Counter(str(int(round(v))) for v in np.linalg.eigvalsh(X.astype(float)))
        assert got==Counter({k:v for k,v in eig[key].items()})

    out={'pass':4682,'incidences':{'Q':'135_4-36_15 Pass4663','M':'135_8-36_30 code minima','rowwise_intersection':0,'same_rational_column_space_dimension':36},
      'column_gram':{'QtQ':'15 I + 3 A36','MtM':'24 I + 6 J','QtM':'6 (J-I-A36)','sum_gram':'9 (3 I + 2 J - A36)','A36':'SRG(36,15,6,6)','sum_kernel':'+3 eigenspace of A36, dimension 15'},
      'rank_smith':ranks,
      'row_gram_algebra':{'dimension':4,'relation':'M M^T = 2 Q Q^T + Q M^T','joint_multiplicities':[1,15,20,99],'eigenvalues':eig},
      'theorem':'The complementary 4- and 8-spread incidences are two integral lattices in the same rational 36-space. Their 36-side products close in the rank-3 spread algebra, while their sum annihilates exactly the 15-dimensional +3 spread eigenspace and has Smith profile 1^14 3^7.',
      'boundary':'Exact integral/rational incidence algebra only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
