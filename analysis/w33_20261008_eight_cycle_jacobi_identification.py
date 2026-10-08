#!/usr/bin/env python3
"""Exact rational identification of the W33 Levi C8 current algebra.

All calculations are over Q, with finite-dimensional explicit matrices.
The Jacobi algebra identified here is NOT the Hamiltonian-constraint algebra
of a Lorentzian gravitational theory.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261008_eight_cycle_jacobi_identification.json"


def rational_generators():
    gens=[]
    for i in range(8):
        j=(i+1)%8
        u=sp.zeros(8,1);v=sp.zeros(8,1)
        u[i]=u[j]=1;v[i]=1;v[j]=-1
        gens.append(u*v.T)
    return gens


def rational_lie_basis():
    gens=rational_generators()
    echelons=[]; pivots=[]; found=[]
    def reduce(mat):
        v=list(mat)
        for pivot,row in zip(pivots,echelons):
            if v[pivot]:
                m=v[pivot]
                v=[a-m*b for a,b in zip(v,row)]
        return v
    def add(mat):
        v=reduce(mat)
        for k,t in enumerate(v):
            if t:
                v=[x/t for x in v]
                idx=sum(p<k for p in pivots)
                pivots.insert(idx,k)
                echelons.insert(idx,v)
                return True
        return False
    for g in gens:
        if add(g): found.append(g)
    for m in found:
        for g in gens:
            v=m*g-g*m
            if add(v): found.append(v)
    assert len(found)==34
    basis=[sp.Matrix(8,8,row) for row in echelons]
    return gens,basis


def identify():
    gens,basis=rational_lie_basis()
    u=sp.ones(8,1)
    s=sp.Matrix([1,-1,1,-1,1,-1,1,-1])
    assert all(x*u==sp.zeros(8,1) and s.T*x==sp.zeros(1,8) for x in basis)
    # Build an exact adapted basis of 1 + 6 + 1 dimensions:
    # u spans the common kernel, 6 columns supplement u in ker(s.T),
    # last column is transverse to ker(s.T).
    cols=[u]
    for j in range(6):
        e=sp.zeros(8,1)
        e[j]=1;e[7]=s[j]
        cols.append(e)
    e=sp.zeros(8,1);e[7]=1
    cols.append(e)
    T=sp.Matrix.hstack(*cols)
    assert T.det()!=0
    Ti=T.inv()
    transforms=[Ti*x*T for x in basis]
    assert all(x[:,0]==sp.zeros(8,1) and x[7,:]==sp.zeros(1,8) for x in transforms)
    A=[x[1:7,1:7] for x in transforms]
    L=sp.Matrix.hstack(*[sp.Matrix(list(x)) for x in A])
    image_dim=L.rank()
    assert image_dim==21
    # All invariant antisymmetric forms J on six-dim quotient:
    skew=[]
    for i in range(6):
        for j in range(i+1,6):
            e=sp.zeros(6,6);e[i,j]=1;e[j,i]=-1
            skew.append(e)
    C=sp.Matrix.vstack(*[
        sp.Matrix.hstack(*[
            sp.Matrix(list(x.T*j+j*x)) for j in skew
        ]) for x in A
    ])
    form_kernel=C.nullspace()
    assert len(form_kernel)==1
    J=sum((c*j for c,j in zip(form_kernel[0],skew)),sp.zeros(6))
    assert J.det()!=0
    assert all(x.T*J+J*x==sp.zeros(6) for x in A)
    # dim(sp6) = 6(6+1)/2 = 21. Since image dimension=21,
    # image IS all sp(6,Q;J), not merely a subalgebra.
    assert image_dim==6*7//2
    ker=L.nullspace()
    assert len(ker)==13
    radical=[sum((v[i]*transforms[i] for i in range(34)),sp.zeros(8)) for v in ker]
    assert all(x[1:7,1:7]==sp.zeros(6) for x in radical)
    # The linear map radical -> (row R_1x6, col v_6x1, center z)
    # is an isomorphism onto the full 13-d Heisenberg matrices.
    rvz=sp.Matrix.hstack(*[
        sp.Matrix(list(x[0,1:7])) .col_join(x[1:7,7]).col_join(sp.Matrix([x[0,7]]))
        for x in radical])
    assert rvz.shape==(13,13) and rvz.det()!=0
    # Every radical commutator has only the central (0,7) entry:
    rb=[x*y-y*x for x in radical for y in radical]
    assert all(all(m[i,j]==0 for i in range(8) for j in range(8) if (i,j)!=(0,7)) for m in rb)
    assert any(m[0,7]!=0 for m in rb)
    z=sp.zeros(8);z[0,7]=1
    assert all(z*x==x*z for x in transforms)
    # show full algebra = sp6 acting by derivations on Heisenberg13,
    # and exact split follows characteristic-zero Levi theorem.
    # Center original matrix = T z T^-1, scale to primitive integral.
    center=T*z*Ti
    central_scaled=sp.lcm([sp.denom(q) for q in center])*center
    return {
       "dimension_over_Q":34,
       "adapted_basis_determinant":str(T.det()),
       "six_dimensional_symplectic_representation_image_dim":image_dim,
       "invariant_skew_form_kernel_dim":len(form_kernel),
       "J_six_by_six":[[str(J[i,j]) for j in range(6)] for i in range(6)],
       "J_nondegenerate_det":str(J.det()),
       "radical_kernel_dim":len(radical),
       "radical_to_heisenberg_13_det":str(rvz.det()),
       "radical_commutator_dim":1,
       "central_matrix_rational":[[str(center[i,j]) for j in range(8)] for i in range(8)],
       "structure_over_Q":"sp(6,Q) semidirect Heisenberg_13(Q), via rational Levi splitting",
       "precise_gravity_boundary":"finite graph-current Lie algebra, no Dirac hypersurface constraints or spacetime limit"
    }


if __name__=="__main__":
    out=identify()
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps(out,indent=2,sort_keys=True))
    print("JACOBI_IDENTIFICATION_EXACT_PASS")
