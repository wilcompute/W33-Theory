#!/usr/bin/env python3
"""Exact integer-affine E6(6) generalized Lie derivative closure
on representative maximal M6 and IIB5 coordinate sections.

For density-weight 1/3 generalized vectors,
 L_X V^M = X^K d_K V^M - V^K d_K X^M
           + Y^{MK}{}_{NL} d_K X^L V^N,
 Y^{MK}{}_{NL}=10 d^{MKR} d_{NLR}=sum_R t^{MKR} t_{NLR},
 where t has 270 signed ±1 ordered cubic entries.

For affine X,V, each L_X V is affine, so the exact closure identity
2[L_X,L_Z]V = L_{L_X Z - L_Z X} V
is checked coefficient-by-coefficient using integer arithmetic.

Also verifies trivial affine gauge parameters and one explicit
off-section constraint-breaking counterexample. Independent of prior
assistant's uncommitted local calculations.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
from itertools import combinations,permutations
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import networkx as nx
OUT=ROOT/"data/toe_20261113_E6_ExFT_affine_generalized_diffeomorphism_closure.json"

def setup():
    _,terms,_,_,_=R.load()
    T=np.zeros((27,27,27),dtype=np.int64)
    for w,s in terms.items():
        for perm in permutations(w):T[perm]=s
    assert np.count_nonzero(T)==270
    assert np.array_equal(np.einsum("imn,jmn->ij",T,T),10*np.eye(27,dtype=np.int64))
    Y=np.einsum("mkr,nlr->mknl",T,T,optimize=True)
    assert Y.shape==(27,27,27,27)
    G=nx.Graph();G.add_nodes_from(range(27))
    for w in terms:G.add_edges_from(combinations(w,2))
    sects=sorted(tuple(sorted(c)) for c in nx.find_cliques(nx.complement(G)))
    S5=next(z for z in sects if len(z)==5)
    S6=next(z for z in sects if len(z)==6)
    for s in (S5,S6):
        assert all(not T[a,b,:].any() for a in s for b in s)
    return T,Y,S5,S6

def calc(X,V,Y):
    """Affine generalized derivative, X=(constant, jacobian)."""
    a,A=X;b,B=V
    # Y[m,k,n,l] A[l,k] b[n], returns output m.
    # Instead of 4D einsum repeatedly, precompute 27x27 action
    # of the gradient of X: Z[m,n]=Y[m,k,n,l] A[l,k].
    Z=np.einsum("mknl,lk->mn",Y,A,optimize=True)
    return (B@a-A@b+Z@b, B@A-A@B+Z@B)

def add(X,V,sign=1):
    return (X[0]+sign*V[0],X[1]+sign*V[1])

def res(X):
    return max(int(np.max(np.abs(z))) for z in X)

def random_affine(rng,S,nonzero=13):
    a=np.zeros(27,dtype=np.int64)
    A=np.zeros((27,27),dtype=np.int64)
    out=rng.choice(27,size=7,replace=False)
    a[out]=rng.integers(-2,3,len(out))
    for _ in range(nonzero):
        A[int(rng.integers(0,27)),int(rng.choice(S))] += int(rng.choice([-2,-1,1,2]))
    return (a,A)

def check_closure(X,Z,V,Y):
    XZ=calc(X,Z,Y);ZX=calc(Z,X,Y)
    comm=add(calc(X,calc(Z,V,Y),Y),calc(Z,calc(X,V,Y),Y),-1)
    rhs=calc(add(XZ,ZX,-1),V,Y)
    two_comm=(2*comm[0],2*comm[1])
    gap=add(two_comm,rhs,-1)
    return res(gap), gap

def trivial_param_from_grad(T,S):
    # A trivial parameter is U^M=t^{MNK} d_N chi_K,
    # with chi_K(Y)=q_K Y_s (affine scalar; q_K arbitrary).
    # Normalization sqrt(10) ignored because the Lie derivative
    # is linear in U, hence scalar multiple of a trivial parameter.
    q=np.arange(1,28,dtype=np.int64)%5-2
    U=np.zeros(27,dtype=np.int64)
    for k in S:
        U+=T[:,k,:]@q
    # U only has support in the derivative-annihilator:
    assert all(U[int(k)]==0 for k in S)
    return (U,np.zeros((27,27),dtype=np.int64))

def find_negative_control(rng,Y,T):
    # Explicit strongly violating section containing one edge of a term.
    for i in range(27):
        for j in range(i+1,27):
            if not np.any(T[i,j,:]):continue
            for _ in range(200):
                x=random_affine(rng,(i,j),5)
                z=random_affine(rng,(i,j),5)
                v=random_affine(rng,(i,j),5)
                r,g=check_closure(x,z,v,Y)
                if r:
                    return {"violating_coordinate_pair":[i,j],
                            "section_constraint_nonzero_components":np.flatnonzero(T[i,j,:]).tolist(),
                            "closure_residual_max_integer":r,
                            "explicit_affine_counterexample":{
                              "X_const":x[0].tolist(),"X_jacobian_sparse":np.argwhere(x[1]).tolist(),
                              "X_jacobian_values":[int(x[1][a,b]) for a,b in np.argwhere(x[1])],
                              "Z_const":z[0].tolist(),"Z_jacobian_sparse":np.argwhere(z[1]).tolist(),
                              "Z_jacobian_values":[int(z[1][a,b]) for a,b in np.argwhere(z[1])],
                              "V_const":v[0].tolist(),"V_jacobian_sparse":np.argwhere(v[1]).tolist(),
                              "V_jacobian_values":[int(v[1][a,b]) for a,b in np.argwhere(v[1])],
                              "closure_residual_const_nonzero":{str(i):int(t) for i,t in enumerate(g[0]) if t},
                              "closure_residual_jacobian_nonzero":{f"{a},{b}":int(g[1][a,b]) for a,b in np.argwhere(g[1])}
                             }}
    raise AssertionError("No counterexample found; incorrect generalized Lie coefficient or insufficient probes.")

def main():
    T,Y,S5,S6=setup()
    rng=np.random.default_rng(2026111307)
    records={}
    for S in (S5,S6):
        trials=32
        violations=0
        triv=trivial_param_from_grad(T,S)
        for _ in range(trials):
            X=random_affine(rng,S)
            Z=random_affine(rng,S)
            V=random_affine(rng,S)
            gap,_=check_closure(X,Z,V,Y)
            assert gap==0,(S,gap)
            assert res(calc(triv,V,Y))==0
        records[str(len(S))]={
          "section_indices":list(S),
          "exact_affine_closure_trials":trials,
          "exact_integer_closure_residual_max":violations,
          "trivial_d_gradient_parameters_act_as_zero":True,
          "section_tensor_zero_for_all_pair_derivatives":True}
    off=find_negative_control(rng,Y,T)
    assert off["closure_residual_max_integer"]>0
    result={
       "status":"PASS_E6_EXFT_AFFINE_GENERALIZED_LIE_CLOSURE_BOTH_SECTIONS_OFFSECTION_COUNTEREXAMPLE",
       "Y_tensor":"Y^{MK}{}_{NL}=10d^{MKR}d_{NLR}=sum_R t^{MKR}t_{NLR}",
       "generalized_Lie_vector_weight":"1/3",
       "closure_identity":"2[L_X,L_Z]V = L_{L_X Z-L_Z X} V for all affine test coefficients",
       "section_cases":records,
       "bad_pair_control":off,
       "scope":"Tests exact affine generalized-vector fields with random integer coefficients, not a proof for all polynomial/smooth fields, and no physical action, gauge curvature or full tensor hierarchy. The closure formula is the published E6(6) exceptional-field-theory operation, not discovered from scratch.",
       "reference":"Hohm Samtleben 2014 PRD89 066016 generalized Lie derivative and E bracket."
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ["status","section_cases"]}|{"bad_pair":off["violating_coordinate_pair"],"bad_residual":off["closure_residual_max_integer"]},indent=2),flush=True)
    return result
if __name__=="__main__":main()
