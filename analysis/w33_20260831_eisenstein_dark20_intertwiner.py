#!/usr/bin/env python3
"""Compare the 24-sector and dark20 conjugate C3 sixes under K exactly.

Both PSp spectral sectors restrict to the W33 point stabilizer K (order 648)
with central C3 nontrivial carriers of rational dimension 12:
  24 -> 12_0 + 6_omega + 6_omega2,
  20 ->  8_0 + 6_omega + 6_omega2.

This script first computes exact Eisenstein-valued character norms and the
cross inner product of the omega sixes.  If they are isomorphic, it then
searches the K-orbital commutant on the 216 circuit states for an explicit
rational intertwiner whose restriction to the two 12-dimensional nontrivial
central carriers has full rank 12.  If the character inner product vanishes,
it certifies the corresponding no-go instead.
"""
from __future__ import annotations

import itertools, json
from collections import deque
from pathlib import Path
import numpy as np

import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260830_sentinel_six_circuit_orbit import six_circuits
from w33_20260831_all5_frontier_audit import orbit_ids, lagrange_projector_numerators, rank_mod

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_EISENSTEIN_DARK20_INTERTWINER.json'
P=1009


def epair_mul(u,v):
    a,b=u; c,d=v
    return (a*c-b*d, a*d+b*c-b*d)


def epair_conj(u):
    a,b=u
    return (a-b,-b)


def epair_add(u,v): return (u[0]+v[0],u[1]+v[1])


def omega_char_pair(c0,c1,c2):
    # (c0 + omega^2*c1 + omega*c2)/3
    assert (c0-c1)%3==0 and (c2-c1)%3==0
    return ((c0-c1)//3,(c2-c1)//3)


def main():
    pts,idx,_lines,N=base.geometry(); supports,masks=base.supports_from_N(N)
    c5=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C: w^=masks[i]
        if w==0: c5.append(C)
    c6=six_circuits(masks); i5={C:i for i,C in enumerate(c5)}; i6={C:i for i,C in enumerate(c6)}

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
    act5=[tuple(i5[tuple(sorted(g[q] for q in C))] for C in c5) for g in g45]
    act6=[tuple(i6[tuple(sorted(g[q] for q in C))] for C in c6) for g in g45]

    s5=[set(C) for C in c5]; s6=[set(C) for C in c6]
    M=np.zeros((216,540),dtype=np.int64)
    for a in range(216):
        for b in range(540):
            if len(s5[a]&s6[b])==3: M[a,b]=1
    seed=next(a*540+b for a in range(216) for b in range(540) if M[a,b])
    O={seed}; Q=deque([seed])
    while Q:
        z0=Q.popleft(); a,b=divmod(z0,540)
        for p5,p6 in zip(act5,act6):
            nz=p5[a]*540+p6[b]
            if nz not in O: O.add(nz); Q.append(nz)
    Mp=np.zeros_like(M)
    for z0 in O:
        a,b=divmod(z0,540); Mp[a,b]=1
    Mm=M-Mp
    I=np.eye(216,dtype=np.int64)
    A30=Mp@Mp.T-10*I
    A20=(Mp@Mm.T+Mm@Mp.T)//4
    Csep=A30+7*A20
    roots=[-58,-22,-18,8,14,62,170]
    projectors=lagrange_projector_numerators(Csep,roots)
    Q20,D20=projectors[8]; Q24,D24=projectors[62]
    assert int(np.trace(Q20))==20*D20 and int(np.trace(Q24))==24*D24

    Kpairs=[(p40,p45) for p40,p45 in Gpaired if p40[0]==0]; assert len(Kpairs)==648
    K45={p45 for p40,p45 in Kpairs}
    kg45=base.deterministic_generators(K45,45)
    Z=[z for z in K45 if all(base.compose(z,g)==base.compose(g,z) for g in kg45)]
    assert len(Z)==3
    e45=tuple(range(45)); z45=next(z for z in Z if z!=e45); z245=base.compose(z45,z45)

    def cperm(g): return tuple(i5[tuple(sorted(g[q] for q in C))] for C in c5)
    Kp={g:cperm(g) for g in K45}
    z=Kp[z45]; z2=Kp[z245]

    def sector_char(Qs,Ds,g):
        p=Kp[g]
        num=sum(int(Qs[i,p[i]]) for i in range(216))
        assert num%Ds==0
        return num//Ds

    sum20=(0,0); sum24=(0,0); cross=(0,0)
    for g in K45:
        vals=[]
        for Qs,Ds in ((Q20,D20),(Q24,D24)):
            c0=sector_char(Qs,Ds,g)
            c1=sector_char(Qs,Ds,base.compose(z45,g))
            c2=sector_char(Qs,Ds,base.compose(z245,g))
            vals.append(omega_char_pair(c0,c1,c2))
        w20,w24=vals
        sum20=epair_add(sum20,epair_mul(w20,epair_conj(w20)))
        sum24=epair_add(sum24,epair_mul(w24,epair_conj(w24)))
        cross=epair_add(cross,epair_mul(w20,epair_conj(w24)))
    assert sum20[1]==sum24[1]==cross[1]==0
    norm20=sum20[0]//648; norm24=sum24[0]//648; hom=cross[0]//648
    assert sum20[0]%648==sum24[0]%648==cross[0]%648==0

    # Rational nontrivial central projectors.  Denominators are irrelevant for
    # image/rank; S=2I-z-z^2 is three times the nontrivial C3 projector.
    Zm=np.zeros((216,216),dtype=np.int64); Z2m=np.zeros_like(Zm)
    for i,j in enumerate(z): Zm[j,i]=1
    for i,j in enumerate(z2): Z2m[j,i]=1
    S=2*I-Zm-Z2m
    N20=Q20@S; N24=Q24@S
    assert rank_mod(N20,P)==12 and rank_mod(N24,P)==12

    kg5=[Kp[g] for g in kg45]
    relK,repsK,sizesK=orbit_ids(kg5,kg5,216,216)
    projected=[]; best_rank=0; witness=None
    for rid,seedK in enumerate(repsK):
        Omat=(relK==rid).astype(np.int64)
        T=((N20%P)@(Omat%P))%P
        T=(T@(N24%P))%P
        rr=rank_mod(T,P)
        projected.append((rid,rr,Omat))
        if rr>best_rank:
            best_rank=rr; witness={'kind':'singleOrbital','orbitalId':rid,'seedPair':list(divmod(seedK,216)),
                                   'orbitalSize':sizesK[rid],'rankModP':rr,'coefficients':{str(rid):1}}
        if rr==12: break

    # If no single orbital gives the isomorphism, deterministic integer linear
    # combinations span Hom_K and should expose it whenever hom>0.
    if best_rank<12 and hom>0:
        mats=[(rid,O) for rid,rr,O in projected if rr>0]
        for trial in range(1,17):
            Ocombo=np.zeros((216,216),dtype=np.int64); coeff={}
            for pos,(rid,Omat) in enumerate(mats):
                c=(pos+1)**trial
                Ocombo += c*Omat; coeff[str(rid)]=c
            T=((N20%P)@(Ocombo%P))%P; T=(T@(N24%P))%P
            rr=rank_mod(T,P)
            if rr>best_rank:
                best_rank=rr; witness={'kind':'orbitalCombination','trial':trial,'rankModP':rr,'coefficients':coeff}
            if rr==12: break

    if hom==0:
        assert best_rank==0
        relation='NO_GO'
    else:
        assert norm20==norm24==1 and hom==1
        assert best_rank==12
        relation='ISOMORPHIC'

    out={
      'schema':'w33.20260831.eisenstein-dark20-intertwiner.v1','status':'PASS',
      'omegaCharacter':{'dark20Norm':norm20,'sector24Norm':norm24,'crossInnerProduct':hom,
                        'relation':relation},
      'rationalNontrivialCarriers':{'dark20Dimension':12,'sector24Dimension':12},
      'KOrbitalCommutant':{'orbitalCount':len(repsK),'bestProjectedRank':best_rank,'modulus':P,
                           'witness':witness},
      'theorem':('The two conjugate 6+6 carriers are K-isomorphic and the recorded K-orbital map is an explicit rational rank-12 intertwiner.' if relation=='ISOMORPHIC' else
                 'The omega character inner product vanishes, so there is no K-equivariant intertwiner between the two conjugate six carriers.'),
      'boundary':'This is a finite-representation intertwiner; it does not identify either six with a calibrated optical degree of freedom.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','norms':[norm20,norm24],'hom':hom,'relation':relation,
                      'Korbitals':len(repsK),'bestRank':best_rank,'witness':witness},sort_keys=True))

if __name__=='__main__': main()
