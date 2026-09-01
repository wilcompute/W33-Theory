#!/usr/bin/env python3
"""Complete the 1080 obstruction-carrier Wedderburn decomposition and split St^3.

The 2026-09-01 product theorem identifies the depth-three obstruction carrier
with the diagonal PSp(4,3)-set 27 completion charts x 40 W33 lines.  The first
representation audit proved transitivity, stabilizer order 24, orbital rank 59,
and Steinberg multiplicity three, but left a 692-dimensional ordinary
character residual unlabeled.

This witness closes that residual from the exact 59-dimensional orbital
algebra, without importing an external character table.  A generic central
element separates all 15 rational central factors.  The three quadratic
factors have discriminants that are -3 times rational squares, so all complex
Galois pairs live over Q(sqrt(-3)).

It then goes one step further.  Inside the 243-dimensional Steinberg isotypic
block, the symmetric orbital operator indexed by the deterministic pair
(11,25) has multiplicity-space spectrum {+4,0,-4}.  Its three spectral
idempotents are rational, pairwise orthogonal, rank 81, and sum to the central
Steinberg projector.  Thus the three abstract Steinberg copies are materialized
as explicit commutant projectors.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260831_all5_frontier_audit import orbit_ids
from w33_20260831_c5_wedderburn_kernel import (
    orbital_mult, center_equations, generic_center, mulvec, factor_key,
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_OBSTRUCTION_WEDDERBURN_STEINBERG.json'
x=sp.Symbol('x')


def build_action():
    pts,idx,lines,N=base.geometry(); supports,_=base.supports_from_N(N)
    adj=[set() for _ in range(45)]
    for i,j in itertools.combinations(range(45),2):
        if supports[i].isdisjoint(supports[j]):
            adj[i].add(j);adj[j].add(i)
    charts=[C for C in itertools.combinations(range(45),5)
            if all(v in adj[u] for u,v in itertools.combinations(C,2))]
    assert len(charts)==27
    cidx={frozenset(C):i for i,C in enumerate(charts)}
    lidx={frozenset(L):i for i,L in enumerate(lines)}

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
    gens45=[tuple(si[frozenset(p[q] for q in S)] for S in supports)
            for p in gens40]
    acts=[]
    for gi in (18,62,77,10):
        p40,p45=gens40[gi],gens45[gi]
        pl=tuple(lidx[frozenset(p40[q] for q in L)] for L in lines)
        pc=tuple(cidx[frozenset(p45[q] for q in C)] for C in charts)
        acts.append(tuple(pc[c]*40+pl[l] for c in range(27) for l in range(40)))
    return acts,charts,lines


def central_records(z,factors,T,identity,diag_id):
    """Fast exact CRT idempotents: precompute powers of z only once."""
    minimal=sp.Poly(1,x,domain=sp.QQ)
    for f,_e in factors:minimal*=f
    d=int(minimal.degree())
    powers=[identity]
    for _ in range(1,d):powers.append(mulvec(powers[-1],z,T))
    records=[];idempotents=[]
    for f,e in factors:
        Mi=minimal.exquo(f)
        inv=sp.Poly(sp.invert(Mi,f),x,domain=sp.QQ)
        ep=sp.Poly(sp.rem(Mi*inv,minimal),x,domain=sp.QQ)
        p=sp.zeros(len(z),1)
        for k in range(d):
            if ep.nth(k):p+=ep.nth(k)*powers[k]
        tr=sp.Rational(1080)*p[diag_id]
        fd=int(sp.degree(f,x)); mult=math.isqrt(int(e)); carrier=int(tr)
        assert tr.q==1 and mult*mult==e and carrier%(fd*mult)==0
        records.append({
            'factor':factor_key(f),'factorDegree':fd,'regularExponent':int(e),
            'permutationMultiplicity':mult,'carrierDimension':carrier,
            'complexIrrepDegree':carrier//(fd*mult),
        })
        idempotents.append(p)
    assert sum(idempotents,sp.zeros(len(z),1))==identity
    return records,idempotents


def main():
    acts,charts,lines=build_action()
    rel,reps,sizes=orbit_ids(acts,acts,1080,1080)
    assert len(reps)==59
    assert sorted(sizes)==sorted([1080]+[3240]+[4320]*2+[6480]*2+[12960]*18+[25920]*35)
    T=orbital_mult(rel,reps)
    Z=center_equations(T).nullspace(); assert len(Z)==15
    diag=int(rel[0,0]); one=sp.zeros(59,1);one[diag]=1
    z,_L,_cp,factors,coeff=generic_center(Z,T)
    records,idempotents=central_records(z,factors,T,one,diag)
    assert sum(r['carrierDimension'] for r in records)==1080
    assert sum(r['factorDegree']*r['permutationMultiplicity']**2 for r in records)==59

    profile=sorted((r['complexIrrepDegree'],r['factorDegree'],r['permutationMultiplicity'])
                   for r in records)
    expected=sorted([
        (1,1,1),(6,1,1),(30,1,1),(15,1,2),(24,1,2),(20,1,3),
        (60,1,3),(64,1,3),(81,1,3),(45,2,1),(40,2,1),(30,2,2),
    ])
    assert profile==expected

    # All three quadratic factors are Eisenstein: discriminant = -3*square.
    quadratic=[]
    for f,e in factors:
        if sp.degree(f,x)!=2:continue
        p=sp.Poly(f,x,domain=sp.QQ); a,b,c=p.nth(2),p.nth(1),p.nth(0)
        D=sp.factor(b*b-4*a*c)
        q=sp.factor(-D/3)
        assert sp.sqrt(q).is_rational
        rec=next(r for r in records if r['factor']==factor_key(p))
        quadratic.append({'irrepDegree':rec['complexIrrepDegree'],
                          'multiplicityEach':rec['permutationMultiplicity'],
                          'discriminant':str(D),'minusDiscriminantOver3Square':str(q)})
    assert {r['irrepDegree'] for r in quadratic}=={30,40,45}

    # Materialize the three primitive Steinberg projectors.
    si=next(i for i,r in enumerate(records) if r['complexIrrepDegree']==81)
    e=idempotents[si]; assert 1080*e[diag]==243
    cols=[]
    for j in range(59):
        q=sp.zeros(59,1);q[j]=1;cols.append(mulvec(e,q,T))
    B=sp.Matrix.hstack(*cols);_r,piv=B.rref();piv=list(piv);assert len(piv)==9
    U=sp.Matrix.hstack(*[cols[j] for j in piv])
    _rr,rowp=U.T.rref();rowp=list(rowp);assert len(rowp)==9
    Uinv=U[rowp,:].inv()
    coord=lambda v:Uinv*v[rowp,:]

    tr=[]
    for seed in reps:
        a,b=divmod(seed,1080);tr.append(int(rel[b,a]))
    chosen=None
    for j in range(59):
        q=sp.zeros(59,1);q[j]=1
        if tr[j]!=j:q[tr[j]]+=1
        b=mulvec(e,q,T)
        if b==sp.zeros(59,1):continue
        M=sp.zeros(9,9)
        for k in range(9):M[:,k]=coord(mulvec(b,U[:,k],T))
        fac=sp.factor_list(sp.Poly(M.charpoly(x).as_expr(),x,domain=sp.QQ))[1]
        if len(fac)==3 and all(sp.degree(f,x)==1 and int(ex)==3 for f,ex in fac):
            vals=[]
            for f,_ex in fac:
                p=sp.Poly(f,x,domain=sp.QQ);vals.append(-p.nth(0)/p.nth(1))
            if set(vals)=={sp.Rational(-4),sp.Rational(0),sp.Rational(4)}:
                chosen=(j,tr[j],b,vals);break
    assert chosen is not None and chosen[0:2]==(11,25)
    j,jt,b,vals=chosen
    primitive=[]
    for lam in vals:
        p=e;den=sp.Rational(1)
        for mu in vals:
            if mu==lam:continue
            p=mulvec(p,b-mu*e,T);den*=lam-mu
        p/=den
        assert mulvec(p,p,T)==p and 1080*p[diag]==81
        primitive.append((lam,p))
    assert sum((p for _lam,p in primitive),sp.zeros(59,1))==e
    for a in range(3):
        for c in range(3):
            if a!=c:assert mulvec(primitive[a][1],primitive[c][1],T)==sp.zeros(59,1)

    reps_decoded={str(k):{'from':list(divmod(reps[k],1080))[0],
                          'to':list(divmod(reps[k],1080))[1]}
                  for k in (j,jt)}
    out={
      'schema':'w33.20260901.obstruction-wedderburn-steinberg.v1','status':'PASS',
      'carrier':{'degree':1080,'orbitalRank':59,'centerDimension':15,
                 'genericCenterCoefficients':coeff},
      'fullRationalCentralFactors':records,
      'complexDecompositionReading':[
        '1','6','2*15','3*20','2*24','30_rational',
        '2*30_Eisenstein + 2*30bar_Eisenstein',
        '40 + 40bar','45 + 45bar','3*60','3*64','3*81_Steinberg'],
      'quadraticGaloisPairs':quadratic,
      'commonQuadraticField':'Q(sqrt(-3))',
      'steinberg':{
        'centralIsotypicRank':243,'multiplicity':3,
        'splittingOrbital':j,'transposeOrbital':jt,
        'representatives':reps_decoded,'multiplicitySpaceSpectrum':['4','0','-4'],
        'projectorFormulas':{
          '+4':'B(B+4E)/32','0':'E-B^2/16','-4':'B(B-4E)/32'},
        'primitiveRanks':[81,81,81],
        'primitiveOrbitalCoefficients':{
          str(lam):[[i,str(sp.factor(p[i]))] for i in range(59) if p[i]]
          for lam,p in primitive},
      },
      'theorem':'The degree-1080 obstruction permutation module is completely decomposed by its exact orbital algebra. Its only non-rational central factors are three conjugate pairs of degrees 30, 40 and 45, all over Q(sqrt(-3)). The Steinberg isotypic block is 3*81 and admits three explicit rational primitive commutant projectors of rank 81.',
      'boundary':'The primitive projectors split multiplicity space canonically only relative to the deterministic orbital ordering and the chosen symmetric orbital B. They are exact G-equivariant projectors, not new physical channels.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','degree':1080,'rank':59,'center':15,
      'field':'Q(sqrt(-3))','steinbergPrimitiveRanks':[81,81,81]},sort_keys=True))

if __name__=='__main__':main()
