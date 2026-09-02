#!/usr/bin/env python3
"""Exact PGSp outer action on the St81^3 and St64^3 obstruction routers.

The 1080 completion-chart x W33-line carrier contains multiplicity-three copies
of the two building Steinbergs, and BT796 realizes the corresponding
End_G-blocks as M3(Q).  The global PGSp/PSp outer involution fixes the 81- and
64-dimensional irreducible characters individually, so it must act *inside*
each M3 multiplicity algebra.

This script computes that action exactly.  It induces the explicit multiplier
minus-one similitude s=diag(1,2,1,2) on the 27 charts and 40 W33 lines, hence on
all 1080 obstruction states and all 59 PSp orbitals.  It then:
  * verifies the induced map is an involutive algebra automorphism;
  * fixes the central St81^3 and St64^3 isotypic idempotents;
  * uses exact matrix units for both M3 blocks;
  * solves the induced automorphism as J M J^{-1} over Q, unique projectively;
  * records J^2, characteristic data, and its action on the three primitive
    channel projectors;
  * checks the K3,3-selected 81 projector separately.

This decides whether the multiplicity-three labels are globally canonical,
outer-paired, or only gauge choices.  It is finite representation theory, not a
particle-generation claim.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp

import w33_20260901_packet48_bt796_crossid as shell
import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
import w33_20260901_double_steinberg_64_81 as dual
from w33_20260901_steinberg_frame_common import build as build_frame, proportional_scalar
from w33_20260831_c5_wedderburn_kernel import center_equations, generic_center, mulvec
from w33_20260902_building_bt796_path_algebra import make_matrix_units

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260902_PGSP_OUTER_M3_ROUTER.json'


def norm(v):
    i=next(k for k,x in enumerate(v) if x%3); z=pow(v[i]%3,-1,3)
    return tuple((z*x)%3 for x in v)


def main():
    F=build_frame(); rel,reps,T,diag=F['rel'],F['reps'],F['T'],F['diag']
    E81=F['E']; frame81=list(F['frame']); Q81=F['Qvec']

    Zc=center_equations(T).nullspace(); one=sp.zeros(59,1); one[diag]=1
    z,_L,_cp,factors,_coeff=generic_center(Zc,T)
    records,idempotents=obs.central_records(z,factors,T,one,diag)
    i64=next(i for i,r in enumerate(records) if r['complexIrrepDegree']==64)
    E64=idempotents[i64]
    split64_label,split64_vals,frame64,_left64=dual.split_three_copies(E64,rel,reps,T,64,diag)

    units81,connect81=make_matrix_units(frame81,E81,T,rel,reps)
    units64,connect64=make_matrix_units(frame64,E64,T,rel,reps)

    D=shell.build(); pts,wlines,supports,charts=D['pts'],D['wlines'],D['supports'],D['charts']
    idx={v:i for i,v in enumerate(pts)}
    outer40=tuple(idx[norm((v[0],2*v[1],v[2],2*v[3]))] for v in pts)
    assert tuple(outer40[outer40[i]] for i in range(40))==tuple(range(40))
    li={frozenset(L):i for i,L in enumerate(wlines)}
    outerL=tuple(li[frozenset(outer40[x] for x in L)] for L in wlines)
    si={S:i for i,S in enumerate(supports)}
    outer45=tuple(si[frozenset(outer40[x] for x in S)] for S in supports)
    ci={frozenset(C):i for i,C in enumerate(charts)}
    outer27=tuple(ci[frozenset(outer45[x] for x in C)] for C in charts)
    outer1080=tuple(outer27[y//40]*40+outerL[y%40] for y in range(1080))
    assert tuple(outer1080[outer1080[y]] for y in range(1080))==tuple(range(1080))

    # It normalizes the four generator action; the conjugates must occur in the
    # exact 25920-element obstruction action group.
    acts=F['acts']
    # Orbital permutation under simultaneous outer action on ordered pairs.
    operm=[]
    for seed in reps:
        a,b=divmod(int(seed),1080)
        operm.append(int(rel[outer1080[a],outer1080[b]]))
    assert sorted(operm)==list(range(59))
    assert all(operm[operm[r]]==r for r in range(59))

    def alpha(v): return sp.Matrix([v[operm[r]] for r in range(59)])
    assert alpha(E81)==E81 and alpha(E64)==E64
    zero=sp.zeros(59,1)
    # Check multiplication on a spanning set of each M3 block.
    for units in (units81,units64):
        for a,b in itertools.product(units.values(),repeat=2):
            assert alpha(mulvec(a,b,T))==mulvec(alpha(a),alpha(b),T)

    order=[(i,j) for i in range(3) for j in range(3)]
    def solve_block(name,degree,E,frame,units,connectors):
        B=sp.Matrix.hstack(*[units[k] for k in order]); assert B.rank()==9
        images={}; mats={}
        for k in order:
            v=alpha(units[k]); sol,_=B.gauss_jordan_solve(v); assert B*sol==v
            M=sp.Matrix(3,3,[sp.factor(sol[q]) for q in range(9)])
            images[k]=[str(sp.factor(x)) for x in sol]
            mats[k]=M
        # Solve J e_ij = alpha(e_ij) J for a projective conjugator J.
        vars=sp.symbols('j0:9'); J=sp.Matrix(3,3,vars); eq=[]
        for i,j in order:
            Eij=sp.zeros(3,3); Eij[i,j]=1
            eq.extend(list(J*Eij-mats[(i,j)]*J))
        Msys,_rhs=sp.linear_eq_to_matrix(eq,vars)
        ns=Msys.nullspace(); assert len(ns)==1
        J=sp.Matrix(3,3,list(ns[0]))
        q=next(x for x in J if x!=0); J=sp.simplify(J/q)
        assert J.det()!=0
        for i,j in order:
            Eij=sp.zeros(3,3); Eij[i,j]=1
            assert sp.simplify(J*Eij*J.inv()-mats[(i,j)])==sp.zeros(3,3)
        J2=sp.simplify(J*J); lam=proportional_scalar(J2,sp.eye(3)); assert lam is not None and lam!=0
        eig={str(sp.factor(k)):int(v) for k,v in J.eigenvals().items()}
        # Exact action on the deterministic primitive projector frame.
        frame_action=[]
        for i,P in enumerate(frame):
            AP=alpha(P); exact=next((j for j,Q in enumerate(frame) if AP==Q),None)
            sol,_=B.gauss_jordan_solve(AP); MM=sp.Matrix(3,3,[sp.factor(sol[q]) for q in range(9)])
            frame_action.append({'source':i,'exactFrameTarget':exact,
                                 'matrix':[[str(sp.factor(MM[r,c])) for c in range(3)] for r in range(3)]})
        return {'name':name,'degree':degree,'centralIsotypicFixed':alpha(E)==E,
                'connectors':connectors,
                'projectiveConjugatorJ':[[str(sp.factor(J[r,c])) for c in range(3)] for r in range(3)],
                'J2Scalar':str(sp.factor(lam)),'traceJ':str(sp.factor(sp.trace(J))),
                'detJ':str(sp.factor(J.det())),'eigenvalues':eig,
                'frameAction':frame_action,
                'allNineMatrixUnitsMappedInsideSameBlock':True}

    R81=solve_block('St81^3',81,E81,frame81,units81,connect81)
    R64=solve_block('St64^3',64,E64,frame64,units64,connect64)
    qfixed=alpha(Q81)==Q81
    qframe=next((i for i,P in enumerate(frame81) if Q81==P),None)

    out={'schema':'w33.20260902.pgsp-outer-m3-router.v1','status':'PASS',
         'outer':{'matrixMod3':'diag(1,2,1,2)','obstructionInvolution':True,'orbitalInvolution':True},
         'St81':R81,'St64':R64,
         'K33Selected81':{'outerFixed':qfixed,'equalsDeterministicFrameIndex':qframe},
         'theorem':('The explicit PGSp/PSp outer involution acts internally on each multiplicity-three Steinberg router as an exact projective inner automorphism of M3(Q). The recorded 3x3 conjugators determine which primitive channels are fixed, exchanged, or mixed; the two degree sectors remain separate.'),
         'boundary':('This is exact finite representation theory on the obstruction/router carriers. A distinguished multiplicity line or plane is a canonical algebraic subspace, not by itself a particle generation, flavour, or physical field.')}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','J81':R81['projectiveConjugatorJ'],'eig81':R81['eigenvalues'],
                      'J64':R64['projectiveConjugatorJ'],'eig64':R64['eigenvalues'],
                      'K33fixed':qfixed},sort_keys=True))

if __name__=='__main__': main()
