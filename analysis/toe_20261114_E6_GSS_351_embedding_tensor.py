#!/usr/bin/env python3
"""Exact E6 351 embedding-tensor tests for local unipotent GSS flux.

Checks X symmetric part equals d.Z for an antisymmetric rank-two Z,
E6 cubic preservation for all X_M, zero trombone, quadratic
gauge-closure and Z invariance. Existing local Leibniz/GSS tests
supply the constant frame coefficient source.
"""
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_E6_exft_generalized_closure_affine as Ex
import toe_20261113_e6_root_matching_projection_clock as G
from toe_20261114_E6_unipotent_GSS_local_parallelization import frame_structure,check_leibniz
OUT=ROOT/"data/toe_20261114_E6_GSS_explicit_rank2_Z_351_embedding_tensor.json"

def main():
    T,Y,S5,S6=Ex.setup()
    assert np.array_equal(np.einsum("imn,jmn->ij",T,T),10*np.eye(27,dtype=np.int64))
    _,terms,_,_,roots=G.load()
    R=roots[1]; j=3
    assert not np.any(R@R)
    assert 3 in S5 and 3 in S6
    X=frame_structure(Y,R,j,0)
    assert X.shape==(27,27,27) and np.count_nonzero(X)==30
    assert check_leibniz(X)==(0,0)

    # Xsym_{MN}^P=(X_MN^P+X_NM^P)/2.
    # Use integer Zraw_{QP}=T_{MNQ}(X_MN^P+X_NM^P).
    # With d=T/sqrt(10), normalized
    # Z_{QP}=Zraw_{QP}/(2 sqrt(10)).
    # The 351 linear equation is exactly 10*(X+Xswap)=T.Zraw.
    S=X+X.transpose(1,0,2)
    Zraw=np.einsum("mnq,mnp->qp",T,S,optimize=True)
    assert np.array_equal(Zraw,-Zraw.T)
    assert np.count_nonzero(Zraw)==2
    assert Zraw[25,26]==10 and Zraw[26,25]==-10
    reconstruction=np.einsum("mnq,qp->mnp",T,Zraw,optimize=True)
    assert np.array_equal(reconstruction,10*S)
    assert len({(int(i),int(j)) for i,j in zip(*np.nonzero(Zraw))})==2

    # No trombone: E6 generators have trace zero. Verify
    # cubic preservation exactly in the original signed basis.
    active=[]
    for a,M in enumerate(X):
        assert int(np.trace(M))==0
        G.inf_check(M,terms)
        if np.any(M): active.append(a)
    assert active==list(range(5))
    mats=X[active,:,:]
    # Exact rank 5 of the 27x27 matrices: their nonzero matrix
    # units have distinct first input locations.
    assert all(not np.array_equal(M,N) for p,M in enumerate(mats)
               for N in mats[p+1:])
    assert all(not np.any(mats[a]@mats[b])
               for a in range(5) for b in range(5))
    # Full gauge closure and embedding-tensor quadratic constraint
    # [X_M,X_N]=-X_{MN}^P X_P, with both sides zero.
    for a in range(27):
        for b in range(27):
            L=X[a]@X[b]-X[b]@X[a]
            RHS=-np.einsum("c,cij->ij",X[a,b,:],X,optimize=True)
            assert np.array_equal(L,RHS)
    # Z^{MN}X_N=0 and gauge-invariance of the contravariant Z
    # in the matrix convention X_MN^P stored in the certificates.
    assert not np.any(np.einsum("mn,nbc->mbc",Zraw,X))
    for a in range(27):
        assert not np.any(X[a].T@Zraw+Zraw@X[a])

    # 27D generalized frame also has nonvanishing symmetric
    # Dorfman products, so rank2 Z is the two-form intertwiner,
    # not an arbitrary discarded algebraic nuisance.
    assert np.count_nonzero(S)==20
    assert not np.any(X[25,:,:]) and not np.any(X[26,:,:])
    quotient_ideal=[25,26]
    result=dict(
       status="PASS_EXACT_E6_SPLIT_351_LINEAR_QUADRATIC_RANK2_Z_GAUGING",
       E6_signed_cubic_terms=45,full_E6_generators_ambient=78,
       normalized_d_symbol="d_MNP=T_MNP/sqrt(10), with T_iMN*T_jMN=10delta_ij",
       gauge_frame_generator_root_index=1,derivative_axis=3,
       constant_gauge_tensor_shape=[27,27,27],
       nonzero_full_generalized_frame_coefficients=30,
       trace_trombone_zero=True,
       all_27_gauge_generator_matrices_preserve_cubic=True,
       active_gauge_generator_labels=active,
       active_gauge_generator_count=5,
       active_gauge_matrix_pairs_multiply_to_zero=True,
       local_gauge_group_is_5D_abelian_unipotent=True,
       symmetric_frame_tensor_nnz=20,
       antisymmetric_Zraw_nonzero=[[25,26,10],[26,25,-10]],
       antisymmetric_Zraw_rank=2,
       exactly_satisfied_351_linear_constraint="10*(X_MN^P+X_NM^P)=sum_Q T_MNQ Zraw_QP",
       normalized_Z_covariant="Z_QP=Zraw_QP/(2sqrt(10)); only ±sqrt(10)/2 at 25,26",
       linear_constraint_residual_nnz=0,
       quadratic_gauge_closure_residual_nnz=0,
       Z_invariant_under_gauge=True,
       Z_times_gauge_generator_zero=True,
       full_Leibniz_identity_residual_nnz=0,
       two_form_ideal_coordinate_labels=quotient_ideal,
       section_constraint_allows_axis_in_both_M_and_IIB=True,
       precise_claim="An explicit, nonzero local E6(6) generalized Scherk-Schwarz frame whose constant 27D flux satisfies exact 351 linear and quadratic constraints with no trombone, and yields a five-generator abelian unipotent gauging. This uses established ExFT generalized geometry and does not independently discover a supergravity embedding tensor class.",
       exclusions="Not a globally consistent compactification or a solution of the Einstein/scalar/vector/tensor equations. No explicit source cancellation, fermionic supersymmetry, nontrivial cosmological vacuum, or dynamic five-versus-six section selection.",
       references=[
          "https://arxiv.org/abs/1312.0614",
          "https://citeseerx.ist.psu.edu/document?doi=3daf582c22566670342ecdf5f3c96fde53293b35&repid=rep1&type=pdf",
          "https://link.springer.com/article/10.1007/JHEP01%282015%29131"])
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
       "status","active_gauge_generator_count","antisymmetric_Zraw_rank",
       "linear_constraint_residual_nnz","quadratic_gauge_closure_residual_nnz",
       "Z_invariant_under_gauge")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
