#!/usr/bin/env python3
"""Exact Wedderburn analysis of the 216/540 circuit permutation modules.

Targets closed here:
  (2) determine the complex Wedderburn block sizes of the 10-orbital C5
      commutant directly from its orbital multiplication table, and locate the
      seven symmetric spectral sectors inside that algebra;
  (4) decompose the 324-dimensional kernel of M as a PSp(4,3)-module without
      importing an external character table.  We compute the 32-orbital C6
      commutant, choose a generic central element, transport its action through
      the equivariant embedding M^T, and subtract left multiplicities from
      right multiplicities factor by factor.

For a generic central element z of A=direct_sum M_{m_i}(C), left multiplication
on A has characteristic polynomial product f_j(x)^(m_j^2), where irreducible
f_j groups Galois-conjugate central scalars.  Thus the exact rational orbital
algebra already determines the complex multiplicities.
"""
from __future__ import annotations

import itertools, json, math
from collections import Counter, deque
from pathlib import Path
import numpy as np
import sympy as sp

import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260830_sentinel_six_circuit_orbit import six_circuits
from w33_20260831_all5_frontier_audit import orbit_ids, lagrange_projector_numerators

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_C5_WEDDERBURN_KERNEL.json'
x=sp.Symbol('x')


def orbital_mult(rel: np.ndarray, reps: list[int]) -> np.ndarray:
    n=rel.shape[0]; r=len(reps)
    T=np.zeros((r,r,r),dtype=np.int64)
    for k,seed in enumerate(reps):
        a,b=divmod(seed,n)
        C=Counter((int(rel[a,z]),int(rel[z,b])) for z in range(n))
        for (i,j),v in C.items(): T[i,j,k]=v
    return T


def center_equations(T: np.ndarray) -> sp.Matrix:
    r=T.shape[0]
    rows=[]
    for j in range(r):
        for k in range(r):
            rows.append([int(T[i,j,k]-T[j,i,k]) for i in range(r)])
    return sp.Matrix(rows)


def mulvec(a: sp.Matrix, b: sp.Matrix, T: np.ndarray) -> sp.Matrix:
    r=T.shape[0]
    out=[sp.Rational(0) for _ in range(r)]
    for i in range(r):
        ai=a[i]
        if not ai: continue
        for j in range(r):
            bj=b[j]
            if not bj: continue
            q=ai*bj
            for k in np.flatnonzero(T[i,j]):
                out[int(k)] += q*int(T[i,j,int(k)])
    return sp.Matrix(out)


def left_mult(v: sp.Matrix, T: np.ndarray) -> sp.Matrix:
    r=T.shape[0]
    M=sp.zeros(r,r)
    for j in range(r):
        ej=sp.zeros(r,1); ej[j]=1
        M[:,j]=mulvec(v,ej,T)
    return M


def factor_key(f: sp.Poly) -> str:
    return str(sp.Poly(f,x,domain=sp.QQ).monic().as_expr())


def generic_center(center_basis: list[sp.Matrix], T: np.ndarray):
    r=T.shape[0]; zdim=len(center_basis)
    attempts=[]
    attempts.append([i+1 for i in range(zdim)])
    attempts.append([(i+1)**2+1 for i in range(zdim)])
    attempts.append([2**i for i in range(zdim)])
    attempts.append([2,3,5,7,11,13,17,19,23,29,31,37][:zdim])
    for coeff in attempts:
        z=sp.zeros(r,1)
        for c,b in zip(coeff,center_basis): z += c*b
        L=left_mult(z,T)
        cp=sp.Poly(L.charpoly(x).as_expr(),x,domain=sp.QQ)
        fac=sp.factor_list(cp)[1]
        simple_count=sum(sp.degree(f,x) for f,e in fac)
        square_exponents=all(math.isqrt(int(e))**2==int(e) for f,e in fac)
        if simple_count==zdim and square_exponents:
            return z,L,cp,[(sp.Poly(f,x,domain=sp.QQ),int(e)) for f,e in fac],coeff
    raise AssertionError('failed to find separating generic central element')


def poly_eval(poly: sp.Poly, z: sp.Matrix, T: np.ndarray, identity: sp.Matrix) -> sp.Matrix:
    out=sp.zeros(len(z),1)
    for c in poly.all_coeffs():
        out=mulvec(out,z,T)+sp.Rational(c)*identity
    return out


def factor_records(z: sp.Matrix, factors, T: np.ndarray, identity: sp.Matrix,
                   diag_id: int, carrier_n: int):
    minimal=sp.Poly(1,x,domain=sp.QQ)
    for f,e in factors: minimal *= f
    rows=[]
    for f,e in factors:
        Mi=minimal.exquo(f)
        inv=sp.Poly(sp.invert(Mi,f),x,domain=sp.QQ)
        ep=sp.rem(Mi*inv,minimal)
        ev=poly_eval(sp.Poly(ep,x,domain=sp.QQ),z,T,identity)
        assert mulvec(ev,ev,T)==ev
        tr=sp.Rational(carrier_n)*ev[diag_id]
        assert tr.q==1
        degree=int(sp.degree(f,x)); mult=math.isqrt(e)
        carrier=int(tr)
        assert carrier%(degree*mult)==0
        irrep_degree=carrier//(degree*mult)
        rows.append({
            'factor':factor_key(f),'factorDegree':degree,'regularExponent':e,
            'permutationMultiplicity':mult,'carrierDimension':carrier,
            'complexIrrepDegree':irrep_degree,
            '_idempotent':ev,
        })
    return rows


def main():
    pts,idx,_lines,N=base.geometry(); supports,masks=base.supports_from_N(N)
    c5=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C: w^=masks[i]
        if w==0: c5.append(C)
    c6=six_circuits(masks)
    assert len(c5)==216 and len(c6)==540
    i5={C:i for i,C in enumerate(c5)}; i6={C:i for i,C in enumerate(c6)}

    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for q in pts:
                zz=alpha*base.form(q,v)%3
                y=base.norm(tuple((q[k]+zz*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[tuple(si[frozenset(p[q] for q in S)] for S in supports) for p in gens40]
    gg=[gens45[i] for i in (18,62,77,10)]
    act5=[tuple(i5[tuple(sorted(g[q] for q in C))] for C in c5) for g in gg]
    act6=[tuple(i6[tuple(sorted(g[q] for q in C))] for C in c6) for g in gg]

    rel55,reps55,sizes55=orbit_ids(act5,act5,216,216)
    rel66,reps66,sizes66=orbit_ids(act6,act6,540,540)
    assert len(reps55)==10 and len(reps66)==32
    T55=orbital_mult(rel55,reps55); T66=orbital_mult(rel66,reps66)
    E55=center_equations(T55); E66=center_equations(T66)
    Z55=E55.nullspace(); Z66=E66.nullspace()
    id55=int(rel55[0,0]); id66=int(rel66[0,0])
    e55=sp.zeros(10,1); e55[id55]=1
    e66=sp.zeros(32,1); e66[id66]=1

    z55,L55,cp55,fac55,coeff55=generic_center(Z55,T55)
    left_factors=factor_records(z55,fac55,T55,e55,id55,216)
    left_blocks=[]
    for r in left_factors:
        left_blocks += [r['permutationMultiplicity']]*r['factorDegree']
    assert sum(m*m for m in left_blocks)==10

    # Rebuild the bicolour incidence and seven symmetric projectors.
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
    sectors=[(-58,15),(-22,15),(-18,81),(8,20),(14,60),(62,24),(170,1)]
    projectors=lagrange_projector_numerators(Csep,[s for s,d in sectors])

    sector_rows=[]; pvecs=[]
    for lam,d in sectors:
        Qs,Ds=projectors[lam]
        pv=sp.Matrix([sp.Rational(int(Qs[divmod(seed55,216)[0],divmod(seed55,216)[1]]),Ds) for seed55 in reps55])
        assert mulvec(pv,pv,T55)==pv
        central=bool(E55*pv==sp.zeros(E55.rows,1))
        zp=[mulvec(zb,pv,T55) for zb in Z55]
        zrank=sp.Matrix.hstack(*zp).rank()
        sector_rows.append({'separatorEigenvalue':lam,'dimension':d,'centralProjector':central,
                            'centerRestrictionDimension':int(zrank)})
        pvecs.append(pv)

    central_pairs=[]
    for i in range(7):
        for j in range(i+1,7):
            if E55*(pvecs[i]+pvecs[j])==sp.zeros(E55.rows,1):
                central_pairs.append([sectors[i][0],sectors[j][0]])

    split_details=[]
    for i,row in enumerate(sector_rows):
        if row['centerRestrictionDimension']<=1: continue
        p=pvecs[i]; zp=mulvec(z55,p,T55); z2p=mulvec(z55,zp,T55)
        B=sp.Matrix.hstack(p,zp)
        assert B.rank()==2
        sol=sp.linsolve((B,z2p))
        vals=list(next(iter(sol)))
        bcoef,acoef=vals[0],vals[1]
        pol=sp.Poly(x**2-acoef*x-bcoef,x,domain=sp.QQ)
        fl=sp.factor_list(pol)[1]
        irreducible=(len(fl)==1 and sp.degree(fl[0][0],x)==2)
        split_details.append({'separatorEigenvalue':sectors[i][0],'dimension':sectors[i][1],
                              'centralMinimalPolynomial':str(pol.as_expr()),
                              'irreducibleQuadraticOverQ':bool(irreducible),
                              'complexCarrierDimensions':([sectors[i][1]//2,sectors[i][1]//2] if irreducible else None)})

    # Right C6 commutant and a generic central element.
    z66,L66,cp66,fac66,coeff66=generic_center(Z66,T66)
    right_factors=factor_records(z66,fac66,T66,e66,id66,540)
    right_blocks=[]
    for r in right_factors: right_blocks += [r['permutationMultiplicity']]*r['factorDegree']
    assert sum(m*m for m in right_blocks)==32

    # Transport z66 through the equivariant image M^T.  For a right orbital R_j,
    # H_j=M R_j M^T is constant on each left orbital; compute those constants
    # from only 20x20 pairs at each left representative.
    nzrows=[np.flatnonzero(M[a]) for a in range(216)]
    sandwich=np.zeros((32,10),dtype=np.int64)
    for j in range(32):
        for k,seed55 in enumerate(reps55):
            a,b=divmod(seed55,216); cnt=0
            for u in nzrows[a]:
                cnt += int(np.sum(rel66[int(u),nzrows[b]]==j))
            sandwich[j,k]=cnt

    G=M@M.T
    gvec=sp.Matrix([int(G[divmod(s,216)[0],divmod(s,216)[1]]) for s in reps55])
    Lg=left_mult(gvec,T55)
    ginv=Lg.inv()*e55
    assert mulvec(gvec,ginv,T55)==e55
    hvec=sp.Matrix([sum(z66[j]*int(sandwich[j,k]) for j in range(32)) for k in range(10)])
    tvec=mulvec(ginv,hvec,T55)
    assert E55*tvec==sp.zeros(E55.rows,1)
    Lt=left_mult(tvec,T55)
    cpt=sp.Poly(Lt.charpoly(x).as_expr(),x,domain=sp.QQ)
    fact=sp.factor_list(cpt)[1]
    left_restr={factor_key(sp.Poly(f,x,domain=sp.QQ)):int(e) for f,e in fact}

    kernel_rows=[]
    for rr in right_factors:
        key=rr['factor']; er=rr['regularExponent']; nr=rr['permutationMultiplicity']
        el=left_restr.get(key,0)
        if el:
            ml=math.isqrt(el); assert ml*ml==el
        else: ml=0
        kk=nr-ml
        assert kk>=0
        kr={k:v for k,v in rr.items() if not k.startswith('_')}
        kr.update({'leftMultiplicity':ml,'kernelMultiplicity':kk,
                   'kernelCarrierDimension':rr['factorDegree']*rr['complexIrrepDegree']*kk})
        kernel_rows.append(kr)

    kernel_dim=sum(r['kernelCarrierDimension'] for r in kernel_rows)
    kernel_norm=sum(r['factorDegree']*r['kernelMultiplicity']**2 for r in kernel_rows)
    assert kernel_dim==324 and kernel_norm==8

    # Strip internal idempotents from output records.
    left_out=[{k:v for k,v in r.items() if not k.startswith('_')} for r in left_factors]
    right_out=[{k:v for k,v in r.items() if not k.startswith('_')} for r in right_factors]

    out={
      'schema':'w33.20260831.c5-wedderburn-kernel.v1','status':'PASS',
      'leftC5Commutant':{
        'orbitalRank':10,'centerDimension':len(Z55),'genericCenterCoefficients':coeff55,
        'complexWedderburnBlockSizes':sorted(left_blocks,reverse=True),'factorRecords':left_out,
        'sectorPlacement':sector_rows,'centralSectorPairs':central_pairs,'splitSectorDetails':split_details,
      },
      'rightC6Commutant':{
        'orbitalRank':32,'centerDimension':len(Z66),'genericCenterCoefficients':coeff66,
        'complexWedderburnBlockSizes':sorted(right_blocks,reverse=True),'factorRecords':right_out,
      },
      'kernel324':{
        'dimension':kernel_dim,'characterNorm':kernel_norm,'factorwiseDecomposition':kernel_rows,
        'proof':'generic right-center action transported through M^T; multiplicities subtract exactly factor by factor'
      },
      'boundary':'Irreducibles are identified intrinsically by exact central minimal-polynomial factors and degrees; no external character-table naming is imposed.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','leftCenter':len(Z55),'leftBlocks':sorted(left_blocks,reverse=True),
                      'sectors':sector_rows,'pairs':central_pairs,'split':split_details,
                      'rightCenter':len(Z66),'rightBlocks':sorted(right_blocks,reverse=True),
                      'kernelNorm':kernel_norm,'kernel':[{k:r[k] for k in ('factor','factorDegree','complexIrrepDegree','permutationMultiplicity','leftMultiplicity','kernelMultiplicity','kernelCarrierDimension')} for r in kernel_rows if r['kernelMultiplicity']]},sort_keys=True))

if __name__=='__main__': main()
