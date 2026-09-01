#!/usr/bin/env python3
"""Resolve the full multiplicity geometry of the three-copy Steinberg block.

The central Steinberg isotypic component is St_81 tensor Q^3, so its commutant
is M3(Q).  The prior certificate produced three orthogonal primitive projectors
P,R,S and a fourth natural K3,3-selected primitive Q.  Here we go beyond
projector overlaps: find deterministic symmetric orbital connectors from P to
R and P to S, normalize them, and verify all nine rational matrix-unit laws

    e_ij e_kl = delta_jk e_il.

This gives an explicit Q-rational coordinate system on the entire Steinberg
multiplicity algebra.  We then express the geometric K3,3 projector Q and the
older {-4,0,+4} orbital spectral frame in those coordinates.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from w33_20260901_steinberg_frame_common import build, proportional_scalar
from w33_20260831_c5_wedderburn_kernel import mulvec

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_STEINBERG_M3_MATRIX_UNITS.json'


def main():
    F=build(); T=F['T']; E=F['E']; rel=F['rel']; reps=F['reps']; left=F['left_matrix']
    P,R,S=F['frame']; Q=F['Qvec']; frame=[P,R,S]
    zero=sp.zeros(59,1)

    # Orbital transpose involution.
    tr=[]
    for seed in reps:
        a,b=divmod(seed,1080);tr.append(int(rel[b,a]))
    assert all(tr[tr[j]]==j for j in range(59))

    def sym_orb(j):
        v=sp.zeros(59,1);v[j]=1
        if tr[j]!=j:v[tr[j]]+=1
        return mulvec(E,v,T)

    def sandwich(A,B,C):return mulvec(A,mulvec(B,C,T),T)

    # Deterministically find the first symmetric orbital connector between two
    # primitive frame lines.  Normalize asymmetric matrix units rationally;
    # no sqrt(2) or arbitrary orthonormal basis is introduced.
    def connector(i,j):
        Pi,Pj=frame[i],frame[j]
        for k in range(59):
            B=sym_orb(k)
            if B==zero:continue
            X=sandwich(Pi,B,Pj);Y=sandwich(Pj,B,Pi)
            if X==zero or Y==zero:continue
            XY=mulvec(X,Y,T);YX=mulvec(Y,X,T)
            a=proportional_scalar(XY,Pi);b=proportional_scalar(YX,Pj)
            if a is not None and b is not None and a==b and a!=0:
                return k,tr[k],X,Y,sp.factor(a)
        raise AssertionError((i,j))

    k12,kt12,X12,Y21,a12=connector(0,1)
    k13,kt13,X13,Y31,a13=connector(0,2)

    units={}
    units[(0,0)]=P;units[(1,1)]=R;units[(2,2)]=S
    units[(0,1)]=X12;units[(1,0)]=Y21/a12
    units[(0,2)]=X13;units[(2,0)]=Y31/a13
    units[(1,2)]=mulvec(units[(1,0)],units[(0,2)],T)
    units[(2,1)]=mulvec(units[(2,0)],units[(0,1)],T)

    # Verify all 81 matrix-unit products exactly in the 59-orbital algebra.
    for i in range(3):
        for j in range(3):
            assert units[(i,j)]!=zero
            for k in range(3):
                for l in range(3):
                    got=mulvec(units[(i,j)],units[(k,l)],T)
                    want=units[(i,l)] if j==k else zero
                    assert got==want,(i,j,k,l)

    basis=[units[(i,j)] for i in range(3) for j in range(3)]
    B=sp.Matrix.hstack(*basis);assert B.rank()==9
    def coords(v):
        sol,_params=B.gauss_jordan_solve(v)
        assert B*sol==v
        return [[str(sp.factor(sol[3*i+j])) for j in range(3)] for i in range(3)]

    qcoords=coords(Q)

    # Express the older deterministic symmetric orbital whose multiplicity
    # spectrum is {-4,0,+4}; its three primitive spectral projectors give an
    # independent orthogonal frame in the same explicit M3(Q).
    oldB=sym_orb(11); assert tr[11]==25
    oldM=left(oldB)
    assert sp.factor(oldM.charpoly().as_expr())==sp.Symbol('lambda')**3*(sp.Symbol('lambda')-4)**3*(sp.Symbol('lambda')+4)**3
    oldproj=[]
    for lam in (-4,0,4):
        v=E;den=sp.Rational(1)
        for mu in (-4,0,4):
            if mu==lam:continue
            v=mulvec(v,oldB-mu*E,T);den*=lam-mu
        v/=den
        assert mulvec(v,v,T)==v and 1080*v[F['diag']]==81
        oldproj.append({'eigenvalue':lam,'matrixUnitCoordinates':coords(v)})

    # Coordinate multiplication itself must now reproduce the Q projector law.
    Qm=sp.Matrix([[sp.Rational(x) for x in row] for row in qcoords])
    assert Qm*Qm==Qm and Qm.rank()==1

    out={
      'schema':'w33.20260901.steinberg-m3-matrix-units.v1','status':'PASS',
      'block':'End_PSp(St_81^3) ~= M3(Q)',
      'primitiveDiagonalFrame':['P_intrinsic_20x15','R_K33_complement_component','S_K33_dark'],
      'connectors':{
        'P_to_R':{'orbital':k12,'transposeOrbital':kt12,'normalizationProduct':str(a12)},
        'P_to_S':{'orbital':k13,'transposeOrbital':kt13,'normalizationProduct':str(a13)}},
      'allNineRationalMatrixUnitLawsVerified':True,
      'K33PrimitiveQCoordinates':qcoords,
      'K33QCoordinateRank':int(Qm.rank()),
      'olderOrbital11_25PrimitiveFrame':oldproj,
      'theorem':(
        'The entire rational Steinberg multiplicity commutant is now explicit, not merely its central or primitive idempotents. '
        'P,R,S and deterministic symmetric orbital connectors generate nine rational matrix units satisfying the full M3(Q) multiplication table. '
        'The K3,3 projector Q and the older orbital spectral frame are expressed in this common coordinate algebra.'),
      'boundary':(
        'These 3x3 coordinates live in multiplicity space for three isomorphic finite-group representations. '
        'They are not a physical generation matrix, CKM/PMNS matrix, Hamiltonian, or experimentally measured mixing matrix.')}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','connectors':[k12,k13],'a':[str(a12),str(a13)],
                      'Qcoords':qcoords},sort_keys=True))

if __name__=='__main__':main()
