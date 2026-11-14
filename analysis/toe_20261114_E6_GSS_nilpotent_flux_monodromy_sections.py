#!/usr/bin/env python3
"""Audit Lie algebra, monodromy and sections of exact local E6 GSS flux.

The root1 unipotent 27x27 frame U(y)=I+yR has 30 nonzero constant
generalized structure coefficients. This checks whether those
coefficients define an antisymmetric Lie algebra, computes its
center/derived algebra over Q, and tabulates coordinate sections
fixed by its integral unipotent monodromy. The local frame still does
NOT solve the ExFT action or provide a dynamical section selector.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import json,sys
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as G
import toe_20261113_E6_exft_generalized_closure_affine as Ex
from toe_20261114_E6_unipotent_GSS_local_parallelization import frame_structure,check_leibniz
OUT=ROOT/"data/toe_20261114_E6_GSS_nilpotent_flux_monodromy_section_audit.json"

def exact_rank(rows):
    pivots={}
    for vals in rows:
        z={k:Fraction(int(v)) for k,v in enumerate(vals) if v}
        while z:
            k=min(z)
            if k not in pivots:
                a=z[k]
                pivots[k]={j:v/a for j,v in z.items()}
                break
            a=z[k]
            for j,v in pivots[k].items():
                z[j]=z.get(j,Fraction(0))-a*v
                if not z[j]:z.pop(j,None)
    return len(pivots)

def main():
    T,Y,_,_=Ex.setup()
    _,terms,_,_,roots=G.load()
    root=roots[1]
    j=3
    assert not root[j,:].any() and not root[:,j].any()
    assert not (root@root).any()
    X=frame_structure(Y,root,j,0)
    assert np.count_nonzero(X)==30
    # ExFT's generalized Dorfman product is a LEIBNIZ algebra,
    # not an ordinary antisymmetric Lie bracket. The nonzero
    # symmetric-product ideal is precisely the tensor-hierarchy
    # obstruction that must be quotiented before Lie reduction.
    sym=X+np.transpose(X,(1,0,2))
    assert np.count_nonzero(sym)==20
    sym_ideal_rank=exact_rank(sym.reshape(-1,27))
    assert sym_ideal_rank==2
    jac=check_leibniz(X)
    assert jac==(0,0)
    nested=np.einsum("abc,cde->abde",X,X,optimize=True)
    assert not np.any(nested)
    sym_left=np.einsum("abc,cde->abde",sym,X,optimize=True)
    sym_right=np.einsum("abc,dce->abde",sym,X,optimize=True)
    assert not np.any(sym_left) and not np.any(sym_right)
    derived=exact_rank(X.reshape(-1,27))
    leftann=27-exact_rank(X.reshape(27,-1))
    rightann=27-exact_rank(np.transpose(X,(1,0,2)).reshape(27,-1))
    assert (derived,leftann,rightann)==(12,22,12)
    assert set(int(k) for k in np.nonzero(sym)[2])=={25,26}
    assert not X[25:,:,:].any() and not X[:,25:,:].any()
    # The 25D quotient by the 2D symmetric/trivial ideal is an
    # ordinary two-step nilpotent Lie algebra. Its noncentral
    # five generators give 10 independent wedge brackets, with
    # another 10 independent abelian central spectators.
    quotient=np.array(X[:25,:25,:25],copy=True)
    assert np.array_equal(quotient,-np.transpose(quotient,(1,0,2)))
    assert not quotient[5:,:,:].any() and not quotient[:,5:,:].any()
    quot_derived=exact_rank(quotient.reshape(-1,25))
    quot_center=25-exact_rank(quotient.reshape(25,-1))
    wedge_brackets=[quotient[a,b,:] for a in range(5) for b in range(a+1,5)]
    assert (quot_derived,quot_center,exact_rank(wedge_brackets))==(10,20,10)
    # A fully EXPLICIT wedge pairing, rather than merely agreeing
    # with an IIB-style dimension count.
    wedge_map=[]
    for a in range(5):
        for b in range(a+1,5):
            outputs=np.flatnonzero(quotient[a,b,:])
            assert len(outputs)==1
            c=int(outputs[0]);sign=int(quotient[a,b,c])
            assert abs(sign)==1
            wedge_map.append(dict(pair=[a,b],derived_coordinate=c,sign=sign))
    wedge_indices=sorted({entry["derived_coordinate"] for entry in wedge_map})
    assert len(wedge_indices)==10
    spectator=sorted(set(range(25))-set(range(5))-set(wedge_indices))
    assert len(spectator)==10
    assert set(wedge_indices).isdisjoint(spectator)
    # The standard IIB generalized tangent decomposes as
    # T5 (5) + T5* tensor SL2 (10) + Lambda^3 T5* (10)
    # + Lambda^5 T5* tensor SL2 (2). Our wedge map is a
    # concrete Lambda^2 T5 -> 10D derived-space isomorphism,
    # dualizable to Lambda^3 T5* after choosing a volume form.
    # No equivariant GL5 x SL2 intertwiner is claimed yet.
    support_out=sorted(set(int(c) for c in np.nonzero(X)[2]))
    assert all(not X[c,:,:].any() for c in support_out)
    support_in=sorted(set(int(i) for i in np.concatenate(
                      (np.nonzero(X)[0],np.nonzero(X)[1]))))
    U=np.eye(27,dtype=np.int64)+root
    Uinv=np.eye(27,dtype=np.int64)-root
    assert np.array_equal(U@Uinv,np.eye(27,dtype=np.int64))
    assert np.array_equal((np.eye(27,dtype=np.int64)+2*root),
                          U@U)
    # Original root is exactly an infinitesimal cubic stabilizer.
    G.inf_check(root,terms)
    H=nx.Graph();H.add_nodes_from(range(27))
    for tri in terms:
        for a in tri:
            for b in tri:
                if a<b:H.add_edge(a,b)
    maxsets=[tuple(sorted(S)) for S in nx.find_cliques(nx.complement(H))]
    assert Counter(map(len,maxsets))=={5:216,6:72}
    result_counts={}
    compatible={}
    for n in (5,6):
        sets=[S for S in maxsets if len(S)==n]
        primal=[];dual=[]
        for S in sets:
            ss=set(S)
            # Column support means U stabilizes the primal S.
            col=all(all((not root[r,k]) or r in ss
                  for r in range(27)) for k in S)
            # Row support means U^-T stabilizes the dual S.
            row=all(all((not root[k,c]) or c in ss
                  for c in range(27)) for k in S)
            if col:primal.append(S)
            if row:dual.append(S)
        if n==5: assert (0,1,2,3,4) in primal
        if n==6: assert (0,1,2,3,5,9) in primal
        result_counts[str(n)]=dict(primal=len(primal),dual=len(dual),
                                   primal_contain_base_j=sum(j in S for S in primal),
                                   dual_contain_base_j=sum(j in S for S in dual))
        compatible[str(n)]=dict(primal_example=list(min(primal)) if primal else None,
                                  dual_example=list(min(dual)) if dual else None)
    result=dict(status="PASS_E6_GSS_TWO_STEP_LEIBNIZ_FREE5_LIE_QUOTIENT_MONODROMY",
         generator_root_index=1,base_coordinate=j,
         U_of_y="I+yR",R_squared_zero=True,
         integral_monodromy_U_one="I+R",inverse_monodromy="I-R",
         monodromy_infinite_order=True,
         cubic_preserved_by_all_U_y=True,
         constant_generalized_structure_coefficient_nnz=30,
         symmetric_Dorfman_product_nnz=20,
         ordinary_antisymmetric_Lie_bracket=False,
         exact_Leibniz_residual_zero=True,
         symmetric_ideal_two_sided_annihilator=True,
         two_step_nilpotent_Leibniz=True,
         full_product_image_rational_dim=derived,
         symmetric_trivial_ideal_rational_dim=sym_ideal_rank,
         left_annihilator_dim=leftann,
         right_annihilator_dim=rightann,
         lie_quotient_dim=25,
         lie_quotient_derived_dim=quot_derived,
         lie_quotient_center_dim=quot_center,
         lie_quotient_is_free_two_step_on_five_plus_10_central=True,
         explicit_wedge2_five_to_derived_ten_dictionary=wedge_map,
         candidate_IIB_5_10_10_2_partition={
             "five_section_generators":list(range(5)),
             "ten_central_spectator_candidates":spectator,
             "ten_wedge2_derived_coordinates":wedge_indices,
             "two_symmetric_ideal_coordinates":[25,26]},
         IIB_intertwiner_to_GL5_times_SL2_not_yet_constructed=True,
         distinct_nonzero_structure_output_coordinate_indices=support_out,
         structure_input_coordinate_indices=support_in,
         fixed_max_coordinate_sections_by_monodromy=result_counts,
         fixed_section_examples=compatible,
         interpretation="Exact local 27D two-step nilpotent algebra of generalized frame flux, with integer cubic-preserving unipotent monodromy. This meets two local prerequisites for a GSS reduction, not full global consistency.",
         exclusions="This algebra can be a standard twisted/duality frame rather than a new physics result. No full embedding tensor projection, fermion equations, source/tadpole consistency, global generalized manifold, or dynamical section selection proved.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in (
        "status","full_product_image_rational_dim",
        "symmetric_trivial_ideal_rational_dim",
        "lie_quotient_derived_dim","lie_quotient_center_dim",
        "fixed_max_coordinate_sections_by_monodromy",
        "fixed_section_examples")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
