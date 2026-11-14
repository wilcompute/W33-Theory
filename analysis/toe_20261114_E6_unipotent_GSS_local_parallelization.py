#!/usr/bin/env python3
"""Exact local E6 unipotent generalized Scherk-Schwarz frame experiment.

Construct a cubic-preserving nilpotent root R (R²=0) from the committed
78-generator E6 matrix basis, and one strong-constraint coordinate y_j
shared by M6 and IIB5 sections. Build E_A^M(y)=delta_A^M+y R_A^M.
Use the PUBLISHED weight-1/3 generalized Lie derivative Y tensor to
compute the full frame flux coefficients X_AB^C(y).

If constant nonzero, this is a LOCAL generalized Leibniz
parallelization witness, a necessary starting condition for a
generalized Scherk-Schwarz reduction. It is NOT by itself a global
consistent truncation, full embedding tensor, gauge potential, field
equations, or selected physical branch.
"""
from pathlib import Path
from itertools import combinations
import json,sys,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as G
import toe_20261113_E6_exft_generalized_closure_affine as Ex
OUT=ROOT/"data/toe_20261114_E6_unipotent_GSS_local_parallelization.json"

def frame_structure(Y,R,j,y):
    I=np.eye(27,dtype=np.int64)
    U=I+int(y)*R
    Uinv=I-int(y)*R
    assert np.array_equal(U@Uinv,I)
    assert round(np.linalg.det(U))==1
    # For weight 1/3:
    # L_{E_A} E_B^M=E_A^j R_B^M-E_B^j R_A^M
    #     +Y^{Mj}{}_{NL} R_A^L E_B^N.
    V=np.einsum("a,bm->abm",U[:,j],R)-np.einsum("b,am->abm",U[:,j],R)
    V+=np.einsum("mnl,al,bn->abm",Y[:,j,:,:],R,U,optimize=True)
    return np.einsum("abm,mc->abc",V,Uinv,optimize=True)

def check_leibniz(X):
    # A circ (B circ C) = (A circ B) circ C + B circ (A circ C)
    terms=(np.einsum("bcd,ade->abce",X,X,optimize=True)
       -np.einsum("abd,dce->abce",X,X,optimize=True)
       -np.einsum("acd,bde->abce",X,X,optimize=True))
    return int(np.max(np.abs(terms))),int(np.count_nonzero(terms))

def main():
    T,Y,S5,S6=Ex.setup()
    _,signed,_,_,roots=G.load()
    assert len(roots)==72
    common=(0,1,2,3)
    fixed5=(0,1,2,3,4)
    fixed6=(0,1,2,3,5,9)
    for S in (fixed5,fixed6):
        assert all(not T[a,b,:].any() for a in S for b in S)
    checked=0;nonconstant=0;allzero=0;candidate=None
    for root_index,R in enumerate(roots):
        assert np.array_equal(R@R,np.zeros((27,27),dtype=np.int64))
        for j in common:
            if np.any(R[:,j]) or np.any(R[j,:]):continue
            checked+=1
            x0=frame_structure(Y,R,j,0)
            if not np.any(x0):
                allzero+=1
                continue
            # X(y) is polynomial degree at most 3 by U,I-yR and
            # Lie derivative. Four distinct matching samples prove
            # identity, and y=-1 is an independent negative control.
            vals=[frame_structure(Y,R,j,y) for y in (1,2,3,-1)]
            if any(not np.array_equal(x0,x) for x in vals):
                nonconstant+=1
                continue
            # Cross-check raw generalized Lie expression with the
            # repo's affine Ex.calc in the constant frame y=0.
            a=np.zeros(27,dtype=np.int64)
            A=np.zeros((27,27),dtype=np.int64)
            B=np.zeros((27,27),dtype=np.int64)
            for p in (0,1,9,13,26):
                for q in (2,4,6,15,21):
                    a[:]=0;A[:]=0;B[:]=0
                    a[p]=1;A[:,j]=R[p,:];b=np.eye(27,dtype=np.int64)[q]
                    B[:,j]=R[q,:]
                    calc=Ex.calc((a,A),(b,B),Y)[0]
                    assert np.array_equal(calc,x0[p,q,:])
            gap,nnz=check_leibniz(x0)
            assert gap==0,(root_index,j,gap,nnz)
            # Integral E6 cubic preserved by finite U(y) for
            # independent integer state vectors, not merely root
            # generator incidence.
            rng=np.random.default_rng(20261114)
            for y in (1,-2,3):
                U=np.eye(27,dtype=np.int64)+y*R
                for trial in range(8):
                    v=rng.integers(-2,3,27)
                    def N(z):
                        return sum(int(s)*int(z[i])*int(z[k])*int(z[l])
                           for (i,k,l),s in signed.items())
                    assert N(U@v)==N(v)
            candidate=dict(root_index=root_index,coordinate_index=j,
                 root_sparse=[[int(a),int(b),int(R[a,b])]
                    for a,b in zip(*np.nonzero(R))],
                 nonzero_flux_components=int(np.count_nonzero(x0)),
                 X_tensor_sha256=hashlib.sha256(x0.tobytes()).hexdigest(),
                 trace_X_AB_B=[
                     int(sum(x0[a,b,b] for b in range(27)))
                     for a in range(27)],
                 flux_sample=[[int(a),int(b),int(c),int(x0[a,b,c])]
                     for a,b,c in zip(*np.nonzero(x0))][:50],
                 complete_integer_leibniz_identity=True,
                 all_sampled_polynomial_coefficients_constant=True,
                 exact_R_squared_zero=True,
                 simultaneous_shared_four_M_IIB_single_coordinate=True,
                 unit_determinant_twist=True)
            break
        if candidate is not None:break
    result=dict(status="PASS_NONZERO_LOCAL_E6_GENERALIZED_FRAME_FLUX" if candidate else "NO_NONZERO_CONSTANT_ROOT_TWIST_WITNESS_FOUND",
         total_root_generators=72,candidate_untouched_common4_root_axis_pairs_checked=checked,
         nonconstant_candidates=nonconstant,zero_flux_candidates=allzero,
         candidate=candidate,
         exact_section_support="single y_j, automatically satisfies E6 strong constraint and lies in both M6 and IIB5 representative maximal sections",
         global_limitations="A constant nonzero generalized frame Leibniz bracket is a local necessary condition. Full generalized Scherk-Schwarz uplift needs exact embedding tensor representation/linear constraints, density/trombone, integrated monodromy/flux quantization, all fields and Einstein equations. No dynamic selection of either branch follows.",
         reference="Hohm and Samtleben JHEP01(2015)131; published ExFT generalized Lie derivative")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in (
      "status","candidate_untouched_common4_root_axis_pairs_checked",
      "nonconstant_candidates","zero_flux_candidates",
      "candidate")},indent=2),flush=True)
    return result

if __name__=="__main__":main()
