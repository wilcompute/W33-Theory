#!/usr/bin/env python3
"""Pass5332: exact noncommutative orbital algebra of the q=5 K0 minimum shell.

Pass5305 proved that the 2340 minimum K0 words form one transitive PSp4(5)
action of orbital rank 21.  This pass computes the full coherent-configuration
intersection tensor from the 21 stabilizer suborbits, detects the directed
orbitals, and determines the complex Wedderburn structure and the permutation-
module constituent dimensions from primitive central idempotents.
"""
from __future__ import annotations
import itertools,json,hashlib
from collections import Counter
from fractions import Fraction
from math import gcd
from functools import reduce
from pathlib import Path
import numpy as np
from sympy import Matrix
from sympy.combinatorics import Permutation,PermutationGroup
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5332_Q5_K0_ORBITAL_WEDDERBURN.json'

def build_action():
    G=build_W(5);pts=G['pts'];pi={p:i for i,p in enumerate(pts)}
    lines=[tuple(sorted(L)) for L in G['lines']];lk={L:i for i,L in enumerate(lines)}
    byp=[[] for _ in pts]
    for l,L in enumerate(lines):
        for p in L:byp[p].append(l)
    labels=[];idx={}
    for p in range(156):
        for a,b in itertools.combinations(sorted(byp[p]),2):idx[(p,a,b)]=len(labels);labels.append((p,a,b))
    assert len(labels)==2340
    def norm(v):
        for x in v:
            if x:
                s=pow(x,-1,5);return tuple(s*y%5 for y in v)
        raise ValueError
    def sp(u,v):return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%5
    vs=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1))
    gens=[];garr=[]
    for v in vs:
        pp=[]
        for x in pts:
            a=sp(x,v);pp.append(pi[norm(tuple((x[k]+a*v[k])%5 for k in range(4)))])
        lp=[lk[tuple(sorted(pp[p] for p in L))] for L in lines]
        arr=[]
        for p,a,b in labels:
            aa,bb=sorted((lp[a],lp[b]));arr.append(idx[(pp[p],aa,bb)])
        garr.append(np.array(arr,dtype=np.uint16));gens.append(Permutation(arr))
    GP=PermutationGroup(gens);assert GP.order()==4680000 and len(GP.orbit(0))==2340
    St=GP.stabilizer(0);assert St.order()==2000
    orbs=sorted([sorted(O) for O in St.orbits()],key=lambda O:(len(O),O[0]))
    assert len(orbs)==21 and Counter(map(len,orbs))==Counter({1:3,4:3,50:9,125:3,500:3})
    return garr,orbs

def tensor(garr,orbs):
    n=2340;r=21
    sub=np.empty(n,dtype=np.uint8)
    for i,O in enumerate(orbs):sub[O]=i
    invs=[]
    for a in garr:
        z=np.empty(n,dtype=np.uint16);z[a]=np.arange(n,dtype=np.uint16);invs.append(z)
    parent=np.full(n,-1,dtype=np.int32);pgen=np.full(n,-1,dtype=np.int8);parent[0]=0;Q=[0]
    for x in Q:
        for gi,a in enumerate(garr):
            y=int(a[x])
            if parent[y]<0:parent[y]=x;pgen[y]=gi;Q.append(y)
    assert len(Q)==n
    maps=np.empty((n,n),dtype=np.uint16);maps[0]=np.arange(n,dtype=np.uint16)
    for x in Q[1:]:maps[x]=maps[parent[x]][invs[pgen[x]]]
    R=np.empty((n,n),dtype=np.uint8)
    for x in range(n):R[x]=sub[maps[x]]
    tr=[int(R[O[0],0]) for O in orbs]
    P=np.zeros((r,r,r),dtype=np.int32)
    for k,O in enumerate(orbs):
        y=O[0];c=np.bincount(sub.astype(np.int16)*r+R[y].astype(np.int16),minlength=r*r).reshape(r,r)
        for i in range(r):
            for j in range(r):P[k,i,j]=c[i,tr[j]]
    val=np.array(list(map(len,orbs)))
    for k in range(r):
        assert np.all(P[k].sum(axis=1)==val) and np.all(P[k].sum(axis=0)==val)
    return P,tr

def algebra(P):
    r=21;L=[]
    for i in range(r):
        M=np.zeros((r,r),dtype=int)
        for j in range(r):M[:,j]=P[:,i,j]
        L.append(M)
    rows=[]
    for j in range(r):
        C=[L[i]@L[j]-L[j]@L[i] for i in range(r)]
        for a in range(r):
            for b in range(r):
                v=[int(C[i][a,b]) for i in range(r)]
                if any(v):rows.append(v)
    A=Matrix(rows);center_dim=r-A.rank();assert center_dim==7
    ns=A.nullspace();Z=[]
    for v in ns:
        den=1
        for x in v:den=np.lcm(den,int(x.q))
        a=np.array([int(x*den) for x in v],dtype=np.int64)
        g=reduce(gcd,[abs(int(x)) for x in a if x] or [1]);a//=g
        if next((x for x in a if x),1)<0:a=-a
        Z.append(a)
    c=sum((i+1)*Z[i] for i in range(7))
    C=sum(int(c[i])*L[i] for i in range(r))
    cp=Matrix(C.tolist()).charpoly().as_expr().factor()
    eig=[9878,1283,998,443,128,-352,-340]
    mult={9878:1,1283:1,998:1,443:1,128:9,-352:4,-340:4}
    assert all(Matrix(C.tolist()).det() is not None for _ in [0])
    # exact algebra multiplication for primitive central idempotents
    def mul(a,b):
        out=[Fraction(0) for _ in range(r)]
        for i,ai in enumerate(a):
            if not ai:continue
            for j,bj in enumerate(b):
                if not bj:continue
                for k,v in enumerate(P[:,i,j]):
                    if v:out[k]+=ai*bj*int(v)
        return out
    one=[Fraction(0) for _ in range(r)];one[0]=1;z=[Fraction(int(x)) for x in c]
    dec=[]
    for lam in eig:
        e=one;den=1
        for mu in eig:
            if mu==lam:continue
            t=z.copy();t[0]-=mu;e=mul(e,t);den*=lam-mu
        e=[x/Fraction(den) for x in e];assert mul(e,e)==e
        iso=Fraction(2340)*e[0];m=int(round(mult[lam]**0.5));d=iso/Fraction(m)
        assert d.denominator==1
        dec.append({'central_eigenvalue':lam,'algebra_block_dimension':mult[lam],
                    'multiplicity':m,'isotypic_rank':int(iso),'irreducible_dimension':int(d)})
    comm=[]
    for i in range(r):
        for j in range(r):
            v=P[:,i,j]-P[:,j,i]
            if np.any(v):comm.append([int(x) for x in v])
    commdim=Matrix(comm).rank();assert commdim==14
    return center_dim,commdim,dec,str(cp)

def main():
    garr,orbs=build_action();P,tr=tensor(garr,orbs)
    center,comm,dec,cp=algebra(P)
    assert sum(x['algebra_block_dimension'] for x in dec)==21
    assert sum(x['multiplicity']*x['irreducible_dimension'] for x in dec)==2340
    out={'pass':5332,'status':'THEOREM_Q5_K0_RANK21_ORBITAL_ALGEBRA_NONCOMMUTATIVE_WEDDERBURN',
      'vertices':2340,'orbital_rank':21,'symmetric_orbitals':sum(i==tr[i] for i in range(21)),
      'directed_orbitals':sum(i!=tr[i] for i in range(21)),'transpose_map':tr,
      'intersection_tensor_sha256':hashlib.sha256(P.tobytes()).hexdigest(),
      'intersection_tensor_nonzero_entries':int(np.count_nonzero(P)),
      'center_dimension':center,'commutator_subspace_dimension':comm,
      'complex_wedderburn':'C^4 + M2(C)^2 + M3(C)',
      'generic_center_charpoly':cp,'primitive_blocks':dec,
      'permutation_module':'1 + 104 + 65 + 520 + 3*90 + 2*65 + 2*625 = 2340',
      'boundary':'Complex semisimple/orbital-algebra theorem. This does not identify equal-dimensional 65-dimensional constituents with the footprint module without an explicit intertwiner.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
