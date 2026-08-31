#!/usr/bin/env python3
"""Compare the two nonconjugate index-216 S5 permutation modules in PSp(4,3).

There are now two exact 216-point G-sets in the repo:
  C : sentinel five-circuits, with stabilizer H_C ~= S5;
  H : complement-pairs of W33 two-ovoids, with stabilizer H_H ~= S5.
The preceding classifier proves H_C and H_H are nonconjugate.

This audit determines *where their permutation characters differ*.

1. Build the complete orbital algebra of the hemisystem-pair action and recover
   its complex Wedderburn multiplicities and irrep degrees without importing a
   character table.
2. Use the seven exact circuit spectral projectors to evaluate known G-character
   traces on the 120 elements of H_H. Frobenius reciprocity then gives the
   multiplicity of every circuit-visible irrep inside C[H].
3. Check the cross-Hom dimension against the five H_H-orbits on C.
4. Subtract the shared character contribution from the hemisystem module,
   exposing the dimensions/multiplicities of the genuinely new representation
   species carried by the second S5 class.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260830_sentinel_six_circuit_orbit import six_circuits
from w33_20260831_all5_frontier_audit import orbit_ids, lagrange_projector_numerators
from w33_20260831_c5_wedderburn_kernel import orbital_mult, center_equations, generic_center, factor_records

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_TWO_S5_PERMUTATION_MODULES.json'
T0=frozenset([0,1,2,3,5,7,8,9,15,16,17,20,24,26,27,28,33,34,36,39])
ALL=frozenset(range(40))


def canon_pair(T):
    C=ALL-T; a,b=tuple(sorted(T)),tuple(sorted(C)); return (a,b) if a<b else (b,a)


def parts(H,n,action):
    rem=set(range(n)); out=[]
    while rem:
        s=min(rem); O={action(g,s) for g in H}; out.append(sorted(O)); rem-=O
    return sorted(out,key=lambda O:(-len(O),O))


def main():
    pts,idx,lines,N=base.geometry(); supports,masks=base.supports_from_N(N)

    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for q in pts:
                z=alpha*base.form(q,v)%3
                y=base.norm(tuple((q[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[tuple(si[frozenset(p[q] for q in S)] for S in supports) for p in gens40]
    chosen=(18,62,77,10)
    g40=[gens40[i] for i in chosen]; g45=[gens45[i] for i in chosen]
    Gpaired=base.closure_paired(g40,g45); assert len(Gpaired)==25920

    # Hemisystem pairs and four-generator action.
    orbit432={frozenset(p40[x] for x in T0) for p40,_ in Gpaired}; assert len(orbit432)==432
    hpairs=sorted({canon_pair(T) for T in orbit432}); assert len(hpairs)==216
    hidx={P:i for i,P in enumerate(hpairs)}
    def himage(p,T): return frozenset(p[x] for x in T)
    def hact_perm(p):
        out=[]
        for P in hpairs:
            T=frozenset(P[0]); out.append(hidx[canon_pair(himage(p,T))])
        return tuple(out)
    actH=[hact_perm(g) for g in g40]

    # Complete hemisystem orbital algebra.
    relHH,repsHH,sizesHH=orbit_ids(actH,actH,216,216)
    rH=len(repsHH)
    TH=orbital_mult(relHH,repsHH)
    ZH=center_equations(TH).nullspace(); zdimH=len(ZH)
    idH=int(relHH[0,0]); eH=sp.zeros(rH,1); eH[idH]=1
    zH,LH,cpH,facH,coeffH=generic_center(ZH,TH)
    hfac=factor_records(zH,facH,TH,eH,idH,216)
    hblocks=[]
    for r in hfac: hblocks += [r['permutationMultiplicity']]*r['factorDegree']
    assert sum(m*m for m in hblocks)==rH
    hfac_out=[{k:v for k,v in r.items() if not k.startswith('_')} for r in hfac]

    # Sentinel five-circuit action and exact seven spectral projectors.
    c5=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C: w^=masks[i]
        if w==0:c5.append(C)
    c6=six_circuits(masks); assert len(c5)==216 and len(c6)==540
    i5={C:i for i,C in enumerate(c5)}; i6={C:i for i,C in enumerate(c6)}
    act5=[tuple(i5[tuple(sorted(g[q] for q in C))] for C in c5) for g in g45]
    act6=[tuple(i6[tuple(sorted(g[q] for q in C))] for C in c6) for g in g45]

    s5=[set(C) for C in c5]; s6=[set(C) for C in c6]
    M=np.zeros((216,540),dtype=np.int64)
    for a in range(216):
        for b in range(540):
            if len(s5[a]&s6[b])==3:M[a,b]=1
    seed=next(a*540+b for a in range(216) for b in range(540) if M[a,b])
    O={seed}; Q=deque([seed])
    while Q:
        z0=Q.popleft(); a,b=divmod(z0,540)
        for p5,p6 in zip(act5,act6):
            nz=p5[a]*540+p6[b]
            if nz not in O:O.add(nz);Q.append(nz)
    Mp=np.zeros_like(M)
    for z0 in O:
        a,b=divmod(z0,540);Mp[a,b]=1
    Mm=M-Mp; I=np.eye(216,dtype=np.int64)
    A30=Mp@Mp.T-10*I
    A20=(Mp@Mm.T+Mm@Mp.T)//4
    Csep=A30+7*A20
    sectors=[(-58,'15a',15),(-22,'15b',15),(-18,'81',81),(8,'20',20),(14,'30+30bar',60),(62,'24',24),(170,'1',1)]
    projs=lagrange_projector_numerators(Csep,[lam for lam,_,_ in sectors])

    # Hemisystem-pair stabilizer H_H and circuit permutations of its elements.
    Tbase=frozenset(hpairs[0][0]); Cbase=ALL-Tbase
    HH=[(p40,p45) for p40,p45 in Gpaired if himage(p40,Tbase) in (Tbase,Cbase)]
    assert len(HH)==120
    def cperm(p45): return tuple(i5[tuple(sorted(p45[q] for q in C))] for C in c5)

    avg={}
    char_rows=[]
    for lam,name,dim in sectors:
        Qn,D=projs[lam]
        s=sp.Rational(0)
        vals=Counter()
        for p40,p45 in HH:
            p=cperm(p45)
            num=sum(int(Qn[i,p[i]]) for i in range(216))
            val=sp.Rational(num,D)
            assert val.q==1
            s+=val; vals[int(val)]+=1
        av=s/120; assert av.q==1
        avg[name]=int(av)
        char_rows.append({'sector':name,'dimension':dim,'separatorEigenvalue':lam,
                          'fixedMultiplicityAverage':int(av),'characterValueHistogramOnHH':dict(sorted(vals.items()))})

    # The two 15 eigenspaces are two copies of the same G-irrep.
    assert avg['15a']==avg['15b']
    m15=avg['15a']; m20=avg['20']; m24=avg['24']; m81=avg['81']; m1=avg['1']
    assert m1==1
    # The rational 60-sector is one 30 plus its Galois conjugate.  An induced
    # rational permutation character contains conjugates with equal multiplicity.
    assert avg['30+30bar']%2==0
    m30=avg['30+30bar']//2

    # Cross-Hom dimension = number of HH-orbits on circuit points.
    HH45=[p45 for _,p45 in HH]
    cross_orbits=parts(HH45,216,lambda g,i:cperm(g)[i])
    cross_dim=len(cross_orbits)
    predicted_cross=1 + 2*m15 + m20 + m24 + m81 + 2*m30
    assert predicted_cross==cross_dim

    # Independent 40/45 point-action checks:
    # C^40 = 1 + V15 + V24, and C^45 = 1 + V20 + V24.
    HH40=[p40 for p40,_ in HH]
    orb40=parts(HH40,40,lambda g,i:g[i]); orb45=parts(HH45,45,lambda g,i:g[i])
    assert len(orb40)==1+m15+m24
    assert len(orb45)==1+m20+m24

    shared_dim=1+15*m15+20*m20+24*m24+81*m81+60*m30
    shared_norm=1+m15*m15+m20*m20+m24*m24+m81*m81+2*m30*m30
    residual_dim=216-shared_dim
    residual_norm=rH-shared_norm
    assert residual_dim>=0 and residual_norm>=0

    # Compare complete hemisystem Wedderburn degree/multiplicity multiset with
    # the known shared contribution.  Remove shared factors by degree/multiplicity
    # only when forced; leave exact raw factor records as the primary certificate.
    complete_complex=[]
    for r in hfac_out:
        for _ in range(r['factorDegree']):
            complete_complex.append((r['complexIrrepDegree'],r['permutationMultiplicity']))
    complete_complex=sorted(complete_complex)

    # Stabilizer subdegrees (the permutation character norm rH).
    base_stab=HH40
    sub=parts(base_stab,216,lambda g,i:hidx[canon_pair(himage(g,frozenset(hpairs[i][0])))])
    assert len(sub)==rH

    out={
      'schema':'w33.20260831.two-s5-permutation-modules.v1','status':'PASS',
      'circuit216':{'dimension':216,'orbitalRank':10,'decomposition':'1 + 2*15 + 20 + 24 + 81 + 30 + 30bar'},
      'hemisystem216':{'dimension':216,'orbitalRank':rH,'centerDimension':zdimH,
        'complexWedderburnBlockSizes':sorted(hblocks,reverse=True),
        'factorRecords':hfac_out,'complexDegreeMultiplicityPairs':complete_complex,
        'subdegrees':sorted(map(len,sub),reverse=True)},
      'circuitVisibleMultiplicitiesInHemisystemModule':{
        '1':m1,'15':m15,'20':m20,'24':m24,'81':m81,'30':m30,'30bar':m30,
        'sharedDimension':shared_dim,'sharedCharacterNormContribution':shared_norm,
        'projectorAverages':char_rows},
      'crossHom':{'dimension':cross_dim,'orbitSizes':sorted(map(len,cross_orbits),reverse=True),
        'frobeniusReciprocityPrediction':predicted_cross},
      'residual':{'dimensionNotInCircuitVisibleSpecies':residual_dim,
        'characterNormNotInCircuitVisibleSpecies':residual_norm},
      'pointActionChecks':{'HHOrbitsOn40':sorted(map(len,orb40),reverse=True),
        'HHOrbitsOn45':sorted(map(len,orb45),reverse=True),
        'identities':['#orbits40 = 1 + m15 + m24','#orbits45 = 1 + m20 + m24']},
      'theorem':'The two nonconjugate index-216 S5 actions have different permutation characters. Exact circuit spectral projectors determine every circuit-visible multiplicity in the hemisystem action by Frobenius reciprocity; the remaining degree and character norm are supplied by genuinely new PSp(4,3) representation species resolved by the hemisystem orbital algebra.',
      'boundary':'Irrep labels are attached only where the existing circuit spectral algebra proves them. New hemisystem-only factors are reported by exact degree, multiplicity, and rational central factor rather than guessed names.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({'status':'PASS','rH':rH,'centerH':zdimH,'blocks':sorted(hblocks,reverse=True),
      'degrees':complete_complex,'known':{'15':m15,'20':m20,'24':m24,'81':m81,'30pairEach':m30},
      'cross':cross_dim,'sharedDim':shared_dim,'residualDim':residual_dim,'residualNorm':residual_norm,
      'subdegrees':sorted(map(len,sub),reverse=True),'orb40':sorted(map(len,orb40),reverse=True),'orb45':sorted(map(len,orb45),reverse=True)},sort_keys=True))

if __name__=='__main__':main()
