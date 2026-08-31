#!/usr/bin/env python3
"""Exact 40x45 coupling ceilings for the hemisystem S5>A5 embedding.

The existing subgroup-breaking ladder uses the S5 stabilizer of a sentinel
five-circuit and proves exact rank ceilings 30 (S5) and 34 (its A5).
The 432 W33 two-ovoids reveal a second, nonconjugate S5 class: the stabilizer
of an unoriented complement-pair, with its index-2 A5 preserving one oriented
half.

This audit computes the permutation-character decompositions on the native
40 W33 points and 45 sentinel minima for this second embedding, using the
actual subgroup conjugacy classes.  It then derives the exact equivariant rank
ceiling sum d_lambda min(m40,m45) and independently searches the full orbital
coupling space for a finite-field rank witness attaining that ceiling.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from collections import Counter

import sympy as sp

import w33_20260829_216_clifford_torsor_nogo as geom
import w33_20260829_pg34_subgroup_zero_split as rankbase

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_HEMISYSTEM_S5_A5_COUPLING.json'
T0=frozenset([0,1,2,3,5,7,8,9,15,16,17,20,24,26,27,28,33,34,36,39])
ALL=frozenset(range(40))
P=1000003


def invperm(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)


def cp(a,b): return (geom.compose(a[0],b[0]),geom.compose(a[1],b[1]))
def ip(a): return (invperm(a[0]),invperm(a[1]))


def conjugacy_classes(H):
    Hset=set(H); rem=set(H); out=[]
    while rem:
        g=next(iter(rem)); C={cp(cp(h,g),ip(h)) for h in H}
        assert C<=Hset
        out.append(C); rem-=C
    return sorted(out,key=lambda C:(geom.porder(next(iter(C))[0]),len(C)))


def fixed_counts(C,side):
    vals={sum(g[side][i]==i for i in range(len(g[side]))) for g in C}
    assert len(vals)==1
    return vals.pop()


def sha_rank(H,seed=1):
    idx,sizes=rankbase.cross_orbit_index(H); norb=1+max(idx.values())
    coeff=[]
    for k in range(norb):
        h=hashlib.sha256(f'w33-hemi-coupling:{seed}:{k}'.encode()).digest()
        coeff.append(1+int.from_bytes(h,'big')%(P-1))
    M=[[coeff[idx[(i,j)]] for j in range(45)] for i in range(40)]
    return rankbase.rank_mod(M),norb,sizes


def main():
    pts,idxp,lines,N=geom.geometry(); supports,masks=geom.supports_from_N(N)
    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*geom.form(x,v)%3
                y=geom.norm(tuple((x[k]+z*v[k])%3 for k in range(4)))
                p.append(idxp[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[tuple(si[frozenset(p[x] for x in S)] for S in supports) for p in gens40]
    chosen=(18,62,77,10)
    G=geom.closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen]);assert len(G)==25920
    def im(p,T):return frozenset(p[x] for x in T)
    S5=[g for g in G if im(g[0],T0) in (T0,ALL-T0)]
    A5=[g for g in S5 if im(g[0],T0)==T0]
    assert len(S5)==120 and len(A5)==60

    # S5 actual conjugacy classes mapped by (order,class size), which uniquely
    # identifies all seven S5 cycle types including the two order-2 classes.
    clsS=conjugacy_classes(S5)
    sigS=[(geom.porder(next(iter(C))[0]),len(C)) for C in clsS]
    expected={(1,1),(2,10),(2,15),(3,20),(4,30),(5,24),(6,20)}
    assert set(sigS)==expected
    key_to_ct={(1,1):'11111',(2,10):'2111',(2,15):'221',(3,20):'311',(6,20):'32',(4,30):'41',(5,24):'5'}
    charsS={
      '5':(1,{'11111':1,'2111':1,'221':1,'311':1,'32':1,'41':1,'5':1}),
      '41':(4,{'11111':4,'2111':2,'221':0,'311':1,'32':-1,'41':0,'5':-1}),
      '32':(5,{'11111':5,'2111':1,'221':1,'311':-1,'32':1,'41':-1,'5':0}),
      '311':(6,{'11111':6,'2111':0,'221':-2,'311':0,'32':0,'41':0,'5':1}),
      '221':(5,{'11111':5,'2111':-1,'221':1,'311':-1,'32':-1,'41':1,'5':0}),
      '2111':(4,{'11111':4,'2111':-2,'221':0,'311':1,'32':1,'41':0,'5':-1}),
      '11111':(1,{'11111':1,'2111':-1,'221':1,'311':1,'32':-1,'41':-1,'5':1})}
    srows=[]
    f40S={};f45S={};countsS={}
    for C in clsS:
        sig=(geom.porder(next(iter(C))[0]),len(C));ct=key_to_ct[sig]
        countsS[ct]=len(C);f40S[ct]=fixed_counts(C,0);f45S[ct]=fixed_counts(C,1)
        srows.append({'cycleType':ct,'order':sig[0],'classSize':sig[1],'fixed40':f40S[ct],'fixed45':f45S[ct]})
    def multS(f):
        out={}
        for name,(d,ch) in charsS.items():
            num=sum(countsS[ct]*f[ct]*ch[ct] for ct in countsS);assert num%120==0;out[name]=num//120
        return out
    m40S,m45S=multS(f40S),multS(f45S)
    ceilS=sum(charsS[n][0]*min(m40S[n],m45S[n]) for n in charsS)
    assert sum(charsS[n][0]*m40S[n] for n in charsS)==40
    assert sum(charsS[n][0]*m45S[n] for n in charsS)==45

    # A5 classes: 1A,2A,3A and two order-5 classes of size12.  Label the two
    # order-5 classes arbitrarily but consistently; swapping them exchanges 3a,3b.
    clsA=conjugacy_classes(A5);sigA=[(geom.porder(next(iter(C))[0]),len(C)) for C in clsA]
    assert sorted(sigA)==[(1,1),(2,15),(3,20),(5,12),(5,12)]
    five=[C for C in clsA if geom.porder(next(iter(C))[0])==5]
    other={ (1,1):'1A',(2,15):'2A',(3,20):'3A' }
    label={id(five[0]):'5A',id(five[1]):'5B'}
    sqrt5=sp.sqrt(5);phi=(1+sqrt5)/2;phib=(1-sqrt5)/2
    charsA={
      '1':(1,{'1A':1,'2A':1,'3A':1,'5A':1,'5B':1}),
      '3a':(3,{'1A':3,'2A':-1,'3A':0,'5A':phi,'5B':phib}),
      '3b':(3,{'1A':3,'2A':-1,'3A':0,'5A':phib,'5B':phi}),
      '4':(4,{'1A':4,'2A':0,'3A':1,'5A':-1,'5B':-1}),
      '5':(5,{'1A':5,'2A':1,'3A':-1,'5A':0,'5B':0})}
    countsA={};f40A={};f45A={};arows=[]
    fi=0
    for C in clsA:
        sig=(geom.porder(next(iter(C))[0]),len(C))
        if sig[0]==5:
            ct='5A' if C is five[0] else '5B'
        else:ct=other[sig]
        countsA[ct]=len(C);f40A[ct]=fixed_counts(C,0);f45A[ct]=fixed_counts(C,1)
        arows.append({'class':ct,'order':sig[0],'classSize':sig[1],'fixed40':f40A[ct],'fixed45':f45A[ct]})
    def multA(f):
        out={}
        for name,(d,ch) in charsA.items():
            val=sp.simplify(sum(countsA[ct]*f[ct]*ch[ct] for ct in countsA)/60)
            assert val.is_Integer
            out[name]=int(val)
        return out
    m40A,m45A=multA(f40A),multA(f45A)
    ceilA=sum(charsA[n][0]*min(m40A[n],m45A[n]) for n in charsA)
    assert sum(charsA[n][0]*m40A[n] for n in charsA)==40
    assert sum(charsA[n][0]*m45A[n] for n in charsA)==45

    # Independent exact modular witnesses in the full orbital coupling spaces.
    bestS=(0,None,None,None);bestA=(0,None,None,None)
    for seed in range(1,65):
        r,n,sizes=sha_rank(S5,seed)
        if r>bestS[0]:bestS=(r,seed,n,sizes)
        if r==ceilS:break
    for seed in range(1,65):
        r,n,sizes=sha_rank(A5,seed)
        if r>bestA[0]:bestA=(r,seed,n,sizes)
        if r==ceilA:break
    assert bestS[0]==ceilS and bestA[0]==ceilA

    out={
      'schema':'w33.20260831.hemisystem-s5-a5-coupling.v1','status':'PASS',
      'hemisystemS5':{'order':120,'classes':sorted(srows,key=lambda r:(r['order'],r['classSize'])),
        'left40':m40S,'right45':m45S,'exactMaximumEquivariantRank':ceilS,
        'minimumChiralZeroModes':85-2*ceilS,'crossPairOrbits':bestS[2],
        'rankWitness':bestS[0],'witnessSeed':bestS[1]},
      'orientedHemisystemA5':{'order':60,'classes':sorted(arows,key=lambda r:(r['order'],r['classSize'],r['class'])),
        'left40':m40A,'right45':m45A,'exactMaximumEquivariantRank':ceilA,
        'minimumChiralZeroModes':85-2*ceilA,'crossPairOrbits':bestA[2],
        'rankWitness':bestA[0],'witnessSeed':bestA[1]},
      'comparisonToCircuitChain':{'circuitS5Rank':30,'circuitA5Rank':34,
        'hemisystemS5Rank':ceilS,'hemisystemA5Rank':ceilA},
      'theorem':'The exact 40x45 equivariant coupling ceiling depends on the conjugacy class of the subgroup embedding, not only its abstract isomorphism type. The nonconjugate hemisystem S5>A5 chain has the certified rank ceilings recorded here, independently attained by full-orbital finite-field witnesses.',
      'boundary':'This is a finite representation-theoretic coupling theorem. Maximum symmetry-allowed rank is not a claim that a local physical perturbation realizes a generic orbital coupling.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({'status':'PASS','S5':{'rank':ceilS,'zero':85-2*ceilS,'left':m40S,'right':m45S,'orbits':bestS[2]},
      'A5':{'rank':ceilA,'zero':85-2*ceilA,'left':m40A,'right':m45A,'orbits':bestA[2]},
      'circuit':[30,34]},sort_keys=True))

if __name__=='__main__':main()
