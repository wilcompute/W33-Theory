#!/usr/bin/env python3
"""Exact discrete universality certificate for 4 fixed Witting optical gates.

Generators R5(omega), R26(omega), R33(omega), R36(-1). The commutant
of their adjoint action on sl4 has dimension one (over Q(omega)), as
certified by modular rank 224 of 225 equations in six split prime fields.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import toe_20261122_witting_minimal_lie_control as base

OUT=Path(__file__).resolve().parents[1]/"data/toe_20261122_discrete_witting_dense_su4.json"
FIXED=(5,26,33)
PI_GATE=36
PRIMES=(7,13,19,31,37,43)

def projector(j,p):
    v,vc=base.all_witting_rays(p)[j]
    return np.array(base.outer(v,vc,p),dtype=np.int64).reshape(4,4)*pow(3,-1,p)%p

def reflect(j,p):
    w=base.primitive_cube_root(p)
    P=projector(j,p);I=np.eye(4,dtype=np.int64)
    U=(I+(w-1)*P)%p
    Ui=(I+((w*w)%p-1)*P)%p
    assert np.array_equal(U@Ui%p,I)
    return U,Ui

def pi_phase(j,p):
    P=projector(j,p);I=np.eye(4,dtype=np.int64)
    U=(I-2*P)%p
    assert np.array_equal(U@U%p,I)
    return U,U

def sl4_basis():
    out=[]
    for i in range(4):
        for j in range(4):
            if i!=j:
                E=np.zeros((4,4),dtype=np.int64)
                E[i,j]=1;out.append(E)
    for i in range(3):
        E=np.zeros((4,4),dtype=np.int64)
        E[i,i]=1;E[3,3]=-1;out.append(E)
    assert len(out)==15
    return out

def sl4_coords(X):
    return [int(X[i,j]) for i in range(4) for j in range(4) if i!=j]+[int(X[i,i]) for i in range(3)]

def adjoint(U,Ui,p):
    return np.array([sl4_coords(U@X@Ui%p) for X in sl4_basis()],dtype=np.int64).T%p

def commutant_equations(A,p):
    n=A.shape[0]
    M=np.zeros((n*n,n*n),dtype=np.int64)
    for r in range(n):
        for c in range(n):
            for k in range(n):
                M[r*n+c,r*n+k]+=A[k,c]
                M[r*n+c,k*n+c]-=A[r,k]
    return M%p

def rank_mod(matrix,p):
    A=np.array(matrix,dtype=np.int64,copy=True)%p
    m,n=A.shape;rank=0
    for j in range(n):
        if rank>=m:break
        nz=np.flatnonzero(A[rank:,j])
        if len(nz)==0:continue
        k=rank+int(nz[0]);A[[k,rank]]=A[[rank,k]]
        A[rank]=A[rank]*pow(int(A[rank,j]),-1,p)%p
        rows=np.flatnonzero(A[rank+1:,j])+rank+1
        if len(rows):
            A[rows]=(A[rows]-A[rows,j:j+1]*A[rank:rank+1])%p
        rank+=1
    return rank

def verify():
    certificates=[]
    for p in PRIMES:
        gates=[reflect(j,p) for j in FIXED]+[pi_phase(PI_GATE,p)]
        ads=[adjoint(U,Ui,p) for U,Ui in gates]
        systems=[];ranks=[]
        for A in ads:
            systems.append(commutant_equations(A,p))
            ranks.append(rank_mod(np.vstack(systems),p))
        assert ranks==[126,200,221,224],(p,ranks)
        w=base.primitive_cube_root(p)
        P=projector(26,p);Q=projector(36,p)
        assert int(np.trace(P@Q)%p)==pow(3,-1,p)
        tr=int(np.trace(gates[3][0]@gates[1][0])%p)
        assert tr==((5+w)*pow(3,-1,p))%p
        certificates.append(dict(prime=p,omega=w,commutant_equation_ranks=ranks,
            commutant_dimension=225-ranks[-1],trace_mod_p=tr))
    return dict(status="PASS_EXACT_ADJOINT_IRREDUCIBILITY_AND_DENSITY",
        fixed_order3_rays=list(FIXED),fixed_order2_ray=PI_GATE,
        product_trace="(5+omega)/3; omega^2+omega+1=0",
        infinite_order_reason="Trace not algebraic integer in Z[omega]; finite-order matrix has integral trace.",
        adjoint_rep="Ad on sl4(C), dimension 15",
        equations_unknowns=225,commutant_over_complex_dimension=1,
        finite_field_certificates=certificates,
        proof="Infinite subgroup has nonzero Lie algebra in closure. Determinants belong to mu6 so identity component is inside SU4. Its Lie algebra complexification is a nonzero invariant subspace of sl4(C). A finite-dimensional unitary adjoint representation is completely reducible; scalar commutant forces irreducibility. Therefore identity component is SU4.",
        determinant_group="mu6",
        full_closure="{U in U(4):det(U) in mu6}",
        limitation="Dense single-photon four-mode gate alphabet; not exact finite-depth synthesis, photonic entanglement, hardware efficiency or TOE.")

def main():
    d=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS exact discrete Witting SU4 density and mu6 determinant")
if __name__=="__main__":main()
