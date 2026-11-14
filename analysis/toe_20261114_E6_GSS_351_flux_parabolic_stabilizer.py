#!/usr/bin/env python3
"""Exact E6(6) stabilizer of rank-two 351 GSS embedding tensor.

A 52D algebra (SL5+SL2) semisimple Levi plus a 25D two-step
negative-grade radical stabilizes the flux. The extra GL1 in the
53D opposite parabolic rescales X by weight -10, rather than
preserving a fixed nonzero flux.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import sys,json
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as G
import toe_20261113_E6_exft_generalized_closure_affine as Ex
from toe_20261114_E6_unipotent_GSS_local_parallelization import frame_structure
from toe_20261114_E6_exact_IIB_Levi_signed_tensor_intertwiner import rank_mod
OUT=ROOT/"data/toe_20261114_E6_351_flux_52D_parabolic_stabilizer.json"

def action(M,X):
    return (np.einsum("cd,abd->abc",M,X,optimize=True)
           -np.einsum("da,dbc->abc",M,X,optimize=True)
           -np.einsum("db,adc->abc",M,X,optimize=True))

def main():
    cert,terms,_,_,roots=G.load()
    T,Y,_,_=Ex.setup()
    X=frame_structure(Y,roots[1],3,0)
    assert int(np.count_nonzero(X))==30
    grading=[4]*5+[1]*8+[-2]*4+[1]*2+[-2]*2  # replace below
    groups={"V":tuple(range(5)),"W":(5,6,7,8,9,10,11,12,17,18),
            "Z":(13,14,15,16,19,20,21,22,23,24),"S":(25,26)}
    weight={"V":4,"W":1,"Z":-2,"S":-5}
    w={i:weight[k] for k,part in groups.items() for i in part}
    D=np.diag([w[i] for i in range(27)]).astype(np.int64)
    assert np.array_equal(action(D,X),-10*X)

    bygrade={}
    for i,R in enumerate(roots):
        nz=np.argwhere(R)
        g={int(w[int(a)]-w[int(b)]) for a,b in nz}
        assert len(g)==1
        g=g.pop()
        bygrade.setdefault(g,[]).append((i,R))
    assert {k:len(v) for k,v in bygrade.items()}=={-6:5,-3:20,0:22,3:20,6:5}
    fixing=[];moving=[]
    for grade,items in bygrade.items():
        for i,R in items:
            residue=action(R,X)
            if grade<=0:
                assert not np.any(residue)
                fixing.append((i,R))
            else:
                assert np.any(residue)
                moving.append((i,R))
    assert len(fixing)==47 and len(moving)==25
    assert rank_mod([action(R,X).reshape(-1) for _,R in moving])==25

    diag=[]
    for row in cert["cubic_27"]["generators"]:
        M=np.zeros((27,27),dtype=np.int64)
        for i,j,v in row:M[int(i),int(j)]=int(v)
        if np.array_equal(M,np.diag(np.diag(M))):diag.append(M)
    assert len(diag)==6
    lam=[]
    slot=tuple(int(i) for i in np.argwhere(X!=0)[0])
    for M in diag:
        res=action(M,X)
        assert not np.any(res[X==0])
        z=int(res[slot])//int(X[slot])
        assert np.array_equal(res,z*X)
        lam.append(z)
    k=next(i for i,v in enumerate(lam) if v)
    fixCartan=[lam[k]*diag[i]-lam[i]*diag[k]
               for i in range(6) if i!=k]
    assert len(fixCartan)==5
    for H in fixCartan:
        assert not np.any(action(H,X))
    # Exactly 52-dimensional stabilizer over Q:
    # 52 manifest integral kernel matrices are independent mod101,
    # all 78 delta-images have rank 26 over F101 and hence over Q.
    allG=[R for _,R in fixing]+[R for _,R in moving]+diag
    assert len(allG)==78
    stab=[R for _,R in fixing]+fixCartan
    assert rank_mod([R.reshape(-1) for R in stab])==52
    assert rank_mod([action(M,X).reshape(-1) for M in allG])==26
    # A 53D opposite parabolic (whole Cartan and <=0-grade
    # roots) preserves the dual 5-plane. The fixed flux
    # removes ONLY the scaling Cartan.
    parabolic=[R for _,R in fixing]+diag
    assert len(parabolic)==53
    assert rank_mod([R.reshape(-1) for R in parabolic])==53
    V=set(groups["V"])
    for R in parabolic:
        assert all(not R[i,j] for i in V for j in range(27) if j not in V)
    # The -3 radical brackets span precisely the -6 sector,
    # and -6 commutes with all of the nilpotent radical.
    lower3=[R for _,R in bygrade[-3]]
    lower6=[R for _,R in bygrade[-6]]
    basis=np.array([R.reshape(-1) for R in lower6],dtype=np.int64)
    pivots=sp.Matrix(basis.tolist()).rref()[1]
    assert len(pivots)==5
    S=sp.Matrix(basis[:,list(pivots)].T.tolist())
    Sinv=S.inv()
    commutators=[]
    for A,B in combinations(lower3,2):
        C=A@B-B@A
        val=sp.Matrix([int(C.reshape(-1)[p]) for p in pivots])
        co=Sinv*val
        assert all(v.q==1 for v in co)
        reconstructed=sum((int(c)*L for c,L in zip(co,lower6)),
                          np.zeros((27,27),dtype=np.int64))
        assert np.array_equal(C,reconstructed)
        commutators.append(C)
    assert rank_mod([C.reshape(-1) for C in commutators])==5
    assert all(not np.any(A@B-B@A) for A in lower3 for B in lower6)
    assert all(not np.any(A@B-B@A) for A,B in combinations(lower6,2))

    # Explicit semisimple Levi: grade-zero SL5(24) + SL2(3).
    # The GL1 scale generator D has eigenweight -10 on X.
    E=roots[55];F=roots[71];H=E@F-F@E
    assert not np.any(action(E,X)) and not np.any(action(F,X))
    assert not np.any(action(H,X))
    result=dict(status="PASS_EXACT_E6_351_GSS_FLUX_52D_OPPOSITE_PARABOLIC_STABILIZER",
       E6_full_cubic_generator_count_78=78,
       rank_of_linear_E6_action_on_embedding_tensor=26,
       exact_stabilizer_dimension=52,
       grade_counts={str(g):len(v) for g,v in sorted(bygrade.items())},
       stabilizing_root_count=47,
       moving_root_count=25,
       stabilizing_Cartan_count=5,
       full_IIB_dual_five_section_opposite_parabolic_dim=53,
       fixed_flux_broken_relative_GL1_dimension=1,
       GL1_flux_relative_weight=-10,
       Levi_semisimple_type="sl5(24)+sl2(3), dimension27",
       grade_negative_nilpotent_radical_dimension=25,
       radical_degree_minus3_dimension=20,
       radical_degree_minus6_center_dimension=5,
       negative_radical_two_step_nilpotent=True,
       radical_190_minus3_pair_commutators_checked=len(commutators),
       radical_derived_algebra_exact_rank=5,
       exact_351_flux_tensor_stabilizer_as_semidirect="(sl5 + sl2) semidirect (20_{-3}+5_{-6})",
       rank_witness_primes=[101],
       fixed_dual_five_section_coordinates=list(groups["V"]),
       e6_stabilizer_scope="Computes the full infinitesimal E6(6) stabilizer of THIS rank-two 351 embedding tensor in the signed split 27 basis; not a classification of all 351 orbits.",
       physical_limitations="A parabolic stabilizer and constant local GSS flux do NOT prove global uplift, a stationary scalar potential, flux quantization, Einstein equations or dynamically preferred IIB vs M section.",
       literature="Hohm/Samtleben 1312.0614, E6 IIB GL5xSL2 grading EPJC2024 13402-4; 5D maximal gauged-supergravity embedding tensor 351")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
       "status","rank_of_linear_E6_action_on_embedding_tensor",
       "exact_stabilizer_dimension","grade_counts",
       "radical_derived_algebra_exact_rank","GL1_flux_relative_weight")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
