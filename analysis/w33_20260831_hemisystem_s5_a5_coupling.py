#!/usr/bin/env python3
"""Exact 40x45 coupling ceilings for the hemisystem S5>A5 embedding.

The existing subgroup-breaking ladder uses the S5 stabilizer of a sentinel
five-circuit and proves exact rank ceilings 30 (S5) and 34 (its A5).
The 432 W33 two-ovoids reveal a second, nonconjugate S5 class: the stabilizer
of an unoriented complement-pair, with its index-2 A5 preserving one oriented
half.

This audit computes the permutation-character decompositions on the native
40 W33 points and 45 sentinel minima for this second embedding, using the
actual subgroup conjugacy classes. It then derives the exact equivariant rank
ceiling sum d_lambda min(m40,m45) and independently searches the full orbital
coupling space for a finite-field rank witness attaining that ceiling.

v2 repair: A5 has two split order-5 conjugacy classes.  A permutation character
is rational and, more concretely, a 5-cycle and its square have identical fixed
points.  We therefore verify equality of the two order-5 fixed counts and use
the rational fused character formulas.  This avoids attaching an arbitrary
5A/5B label to the two Galois-conjugate 3-dimensional characters.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import w33_20260829_216_clifford_torsor_nogo as geom
import w33_20260829_pg34_subgroup_zero_split as rankbase

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_HEMISYSTEM_S5_A5_COUPLING.json'
T0=frozenset([0,1,2,3,5,7,8,9,15,16,17,20,24,26,27,28,33,34,36,39])
ALL=frozenset(range(40))
P=1000003


def invperm(p):
    q=[0]*len(p)
    for i,j in enumerate(p): q[j]=i
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
    G=geom.closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen]); assert len(G)==25920
    def im(p,T): return frozenset(p[x] for x in T)
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
    srows=[]; f40S={}; f45S={}; countsS={}
    for C in clsS:
        sig=(geom.porder(next(iter(C))[0]),len(C)); ct=key_to_ct[sig]
        countsS[ct]=len(C); f40S[ct]=fixed_counts(C,0); f45S[ct]=fixed_counts(C,1)
        srows.append({'cycleType':ct,'order':sig[0],'classSize':sig[1],'fixed40':f40S[ct],'fixed45':f45S[ct]})
    def multS(f):
        out={}
        for name,(d,ch) in charsS.items():
            num=sum(countsS[ct]*f[ct]*ch[ct] for ct in countsS); assert num%120==0; out[name]=num//120
        return out
    m40S,m45S=multS(f40S),multS(f45S)
    ceilS=sum(charsS[n][0]*min(m40S[n],m45S[n]) for n in charsS)
    assert sum(charsS[n][0]*m40S[n] for n in charsS)==40
    assert sum(charsS[n][0]*m45S[n] for n in charsS)==45

    # A5 classes: 1A, 2A, 3A, and two split order-5 classes of size12.
    # We retain the split classes in the certificate but use rational fused
    # formulas.  For a permutation action, g and g^2 have the same fixed set
    # whenever |g|=5, so both split class values must coincide.
    clsA=conjugacy_classes(A5)
    sigA=[(geom.porder(next(iter(C))[0]),len(C)) for C in clsA]
    assert sorted(sigA)==[(1,1),(2,15),(3,20),(5,12),(5,12)]
    arows=[]; classdata=[]; five_rows=[]
    for C in clsA:
        order=geom.porder(next(iter(C))[0]); size=len(C)
        row={'order':order,'classSize':size,'fixed40':fixed_counts(C,0),'fixed45':fixed_counts(C,1)}
        if order==5:
            five_rows.append(row)
        classdata.append(row)
    assert len(five_rows)==2
    assert five_rows[0]['fixed40']==five_rows[1]['fixed40']
    assert five_rows[0]['fixed45']==five_rows[1]['fixed45']
    for j,row in enumerate(sorted(five_rows,key=lambda r:(r['fixed40'],r['fixed45']))): row['class']=f'5split{j+1}'
    for row in classdata:
        if row['order']==1: row['class']='1A'
        elif row['order']==2: row['class']='2A'
        elif row['order']==3: row['class']='3A'
        elif 'class' not in row:
            # assign by object equality with the split rows' numerical data;
            # when both rows have identical character data the names are only bookkeeping.
            row['class']='5split'
    arows=classdata

    def fixed_by_order(side):
        out={}
        for C in clsA:
            o=geom.porder(next(iter(C))[0]); v=fixed_counts(C,side)
            if o in out: assert out[o]==v
            else: out[o]=v
        return out
    f40A=fixed_by_order(0); f45A=fixed_by_order(1)
    assert set(f40A)==set(f45A)=={1,2,3,5}

    # Rational fused A5 character multiplicities.  The two Galois-conjugate
    # 3-dimensional irreps occur equally in every rational permutation module.
    def multA(f):
        f1,f2,f3,f5=f[1],f[2],f[3],f[5]
        nums={
          '1': f1 + 15*f2 + 20*f3 + 24*f5,
          '3a': 3*f1 - 15*f2 + 12*f5,
          '3b': 3*f1 - 15*f2 + 12*f5,
          '4': 4*f1 + 20*f3 - 24*f5,
          '5': 5*f1 + 15*f2 - 20*f3,
        }
        assert all(v%60==0 for v in nums.values())
        return {k:v//60 for k,v in nums.items()}
    dimsA={'1':1,'3a':3,'3b':3,'4':4,'5':5}
    m40A,m45A=multA(f40A),multA(f45A)
    ceilA=sum(dimsA[n]*min(m40A[n],m45A[n]) for n in dimsA)
    assert sum(dimsA[n]*m40A[n] for n in dimsA)==40
    assert sum(dimsA[n]*m45A[n] for n in dimsA)==45

    # Independent exact modular witnesses in the full orbital coupling spaces.
    bestS=(0,None,None,None); bestA=(0,None,None,None)
    for seed in range(1,65):
        r,n,sizes=sha_rank(S5,seed)
        if r>bestS[0]: bestS=(r,seed,n,sizes)
        if r==ceilS: break
    for seed in range(1,65):
        r,n,sizes=sha_rank(A5,seed)
        if r>bestA[0]: bestA=(r,seed,n,sizes)
        if r==ceilA: break
    assert bestS[0]==ceilS and bestA[0]==ceilA

    out={
      'schema':'w33.20260831.hemisystem-s5-a5-coupling.v2','status':'PASS',
      'repair':'A5 split 5-cycle classes are retained explicitly, while rational fused formulas correctly enforce equal 3a/3b multiplicity for permutation characters.',
      'hemisystemS5':{'order':120,'classes':sorted(srows,key=lambda r:(r['order'],r['classSize'])),
        'left40':m40S,'right45':m45S,'exactMaximumEquivariantRank':ceilS,
        'minimumChiralZeroModes':85-2*ceilS,'crossPairOrbits':bestS[2],
        'rankWitness':bestS[0],'witnessSeed':bestS[1]},
      'orientedHemisystemA5':{'order':60,'classes':sorted(arows,key=lambda r:(r['order'],r['classSize'],r['fixed40'],r['fixed45'])),
        'fixedCharacterByOrder40':f40A,'fixedCharacterByOrder45':f45A,
        'left40':m40A,'right45':m45A,'exactMaximumEquivariantRank':ceilA,
        'minimumChiralZeroModes':85-2*ceilA,'crossPairOrbits':bestA[2],
        'rankWitness':bestA[0],'witnessSeed':bestA[1]},
      'comparisonToCircuitChain':{'circuitS5Rank':30,'circuitA5Rank':34,
        'hemisystemS5Rank':ceilS,'hemisystemA5Rank':ceilA},
      'theorem':'The exact 40x45 equivariant coupling ceiling depends on the conjugacy class of the subgroup embedding, not only its abstract isomorphism type. The nonconjugate hemisystem S5>A5 chain has the certified rank ceilings recorded here, independently attained by full-orbital finite-field witnesses.',
      'boundary':'This is a finite representation-theoretic coupling theorem. Maximum symmetry-allowed rank is not a claim that a local physical perturbation realizes a generic orbital coupling.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','S5':{'rank':ceilS,'zero':85-2*ceilS,'left':m40S,'right':m45S,'orbits':bestS[2]},
      'A5':{'rank':ceilA,'zero':85-2*ceilA,'left':m40A,'right':m45A,'orbits':bestA[2]},
      'circuit':[30,34]},sort_keys=True))

if __name__=='__main__': main()
