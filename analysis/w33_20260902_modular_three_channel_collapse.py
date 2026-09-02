#!/usr/bin/env python3
"""Do the three characteristic-zero Steinberg router copies survive mod p?

The obstruction carrier has three rational copies of St81 and three rational
copies of St64.  Their primitive projectors require denominators divisible by
the defining primes, so semisimple characteristic-zero multiplicity need not
survive reduction modulo 3 (W33) or modulo 2 (GQ(4,2)).

We reconstruct the six *integral numerator* chain maps used by the exact
building-injection certificate and reduce those numerators modulo small primes.
For each degree and prime we record individual image ranks, combined rank, and
pairwise intersection dimensions.  In particular:

  * p=3 tests whether the three W33 81 channels collapse/glue in the same
    characteristic in which the [[240,81,3]]_3 CSS logical module is the
    modular Steinberg;
  * p=2 tests the native characteristic of the GQ(4,2) 64-dimensional
    building Steinberg.

No claim is assumed in advance: full 3d rank means the three images remain
independent; rank d means complete modular collapse to one image; intermediate
rank detects partial gluing.
"""
from __future__ import annotations

import itertools
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260901_packet48_bt796_crossid as shell
import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
import w33_20260901_double_steinberg_64_81 as dual
from w33_20260901_steinberg_frame_common import build as build_frame
from w33_20260831_c5_wedderburn_kernel import center_equations, generic_center, mulvec
from w33_20260901_building_chain_injections import integer_cycle_basis, rank_mod, lcm_den

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260902_MODULAR_THREE_CHANNEL_COLLAPSE.json'
PRIMES=(2,3,5,7,1000003)


def projector_integer(P,rel):
    den=lcm_den(P); coeff=np.array([int(den*q) for q in P],dtype=np.int64)
    return coeff[np.asarray(rel,dtype=np.int64)],den


def main():
    D=shell.build(); pts,wlines,supports,charts,G=D['pts'],D['wlines'],D['supports'],D['charts'],D['G']
    F=build_frame(); acts,rel,reps,T,diag=F['acts'],F['rel'],F['reps'],F['T'],F['diag']
    frame81=list(F['frame'])
    Zc=center_equations(T).nullspace(); one=sp.zeros(59,1); one[diag]=1
    z,_L,_cp,factors,_coeff=generic_center(Zc,T)
    records,idempotents=obs.central_records(z,factors,T,one,diag)
    i64=next(i for i,r in enumerate(records) if r['complexIrrepDegree']==64)
    E64=idempotents[i64]
    split64_label,split64_vals,frame64,_left64=dual.split_three_copies(E64,rel,reps,T,64,diag)

    li={frozenset(L):i for i,L in enumerate(wlines)}
    @lru_cache(maxsize=None)
    def line_perm(gi):
        p=G[gi][0]; return tuple(li[frozenset(p[x] for x in L)] for L in wlines)
    def target_one(gi,y):
        c,ell=divmod(y,40); return G[gi][2][c]*40+line_perm(gi)[ell]

    # Match the deterministic four generators.
    gen_indices=[]
    for a in acts:
        hit=next(gi for gi in range(len(G)) if all(target_one(gi,y)==a[y] for y in (0,1,39,40,217,1079)))
        assert all(target_one(hit,y)==a[y] for y in range(1080)); gen_indices.append(hit)

    wch=[(p,ell) for ell,L in enumerate(wlines) for p in L]
    fch=[(packet,c) for c,C in enumerate(charts) for packet in C]
    wi={x:i for i,x in enumerate(wch)}; fi={x:i for i,x in enumerate(fch)}
    def wsrc_one(gi,s):
        p,ell=wch[s]; return wi[(G[gi][0][p],line_perm(gi)[ell])]
    def fsrc_one(gi,s):
        p,c=fch[s]; return fi[(G[gi][1][p],G[gi][2][c])]
    Z81,d81=integer_cycle_basis(40,40,wch); Z64,d64=integer_cycle_basis(45,27,fch)
    assert d81==d64==1 and Z81.shape==(160,81) and Z64.shape==(135,64)

    def source_orbits(source_n,source_one):
        transport=[None]*source_n; H=[]
        for gi in range(len(G)):
            s=source_one(gi,0)
            if transport[s] is None: transport[s]=gi
            if s==0:H.append(gi)
        unseen=set(range(1080)); OO=[]
        while unseen:
            y=min(unseen); O={target_one(gi,y) for gi in H}; unseen-=O; OO.append(tuple(sorted(O)))
        OO.sort(key=lambda O:(len(O),O[0])); return transport,OO
    def columns(transport,O):
        return [tuple(sorted(target_one(transport[s],y) for y in O)) for s in range(len(transport))]
    def selfgram(cols):
        row=np.zeros(1080,dtype=np.int64)
        for C in cols:
            if 0 in C: row[list(C)]+=1
        oval=[None]*59
        for y,v in enumerate(row.tolist()):
            r=int(rel[0,y])
            if oval[r] is None: oval[r]=v
            else: assert oval[r]==v
        return sp.Matrix(oval)

    def materialize(degree,source_n,source_one,cycle,frame):
        transport,OO=source_orbits(source_n,source_one); zero=sp.zeros(59,1); ys=[]; meta=[]
        for k,P in enumerate(frame):
            chosen=None
            for oi,O in enumerate(OO):
                C=columns(transport,O); V=selfgram(C)
                if mulvec(P,mulvec(V,P,T),T)!=zero:
                    chosen=(oi,O,C); break
            assert chosen is not None
            oi,O,C=chosen; Pnum,Pden=projector_integer(P,rel)
            A=np.zeros((1080,source_n),dtype=np.int64)
            for s,col in enumerate(C): A[:,s]=Pnum[:,list(col)].sum(axis=1)
            Y=A@cycle; ys.append(Y); meta.append({'primitive':k,'sourceOrbit':oi,'projectorDenominator':int(Pden)})
        perprime={}
        for p in PRIMES:
            indiv=[rank_mod(Y,p) for Y in ys]
            combined=rank_mod(np.concatenate(ys,axis=1),p)
            pair={}
            for i,j in itertools.combinations(range(3),2):
                rij=rank_mod(np.concatenate([ys[i],ys[j]],axis=1),p)
                pair[f'{i}{j}']=int(indiv[i]+indiv[j]-rij)
            reading=('FULLY_INDEPENDENT' if combined==3*degree else
                     ('COMPLETE_COLLAPSE' if combined==degree and all(r==degree for r in indiv) else
                      ('PARTIAL_GLUE' if combined<3*degree else 'OTHER')))
            perprime[str(p)]={'individualRanks':indiv,'combinedRank':combined,
                              'pairwiseIntersectionDimensions':pair,'reading':reading}
        return {'degree':degree,'maps':meta,'primeReductions':perprime}

    R81=materialize(81,160,wsrc_one,Z81,frame81)
    R64=materialize(64,135,fsrc_one,Z64,frame64)
    native81=R81['primeReductions']['3']; native64=R64['primeReductions']['2']
    out={'schema':'w33.20260902.modular-three-channel-collapse.v1','status':'PASS',
         'St81':R81,'St64':R64,
         'nativeCharacteristicSummary':{'St81_mod3':native81,'St64_mod2':native64},
         'theorem':('The integral numerator forms of all six characteristic-zero building injections have been reduced modulo 2,3,5,7 and a good large prime. Their exact ranks determine whether the three rational multiplicity channels remain independent, partially glue, or collapse in modular characteristic.'),
         'boundary':('Reduction of an integral numerator when the rational projector denominator is divisible by p is a legitimate equivariant modular map, but it is not the reduction of the rational idempotent itself. The certificate therefore describes modular images of the integral chain maps, not a semisimple modular projector decomposition.')}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','81mod3':native81,'64mod2':native64},sort_keys=True))

if __name__=='__main__': main()
