#!/usr/bin/env python3
"""Finite W33 dark-mass effective Hamiltonian and robust 15-edge gap design.

First-order near-flat perturbations project into the 15x15 dark-dark
matrix, hence the 30 chiral zero states pair into 15 positive/negative
mass eigenvalues. Optimization checks possible 15-link supports with
fixed pi phases; it does NOT derive a gauge vacuum or physical masses.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from sympy import Matrix
from w33_20261109_flux_dark_mode_fragility import build
from w33_20261109_minimal_15_flux_lift import find_support

def gap(B,selected):
    A=B.copy().astype(float)
    for i,j in selected:A[i,j]=-1
    sig=np.linalg.svd(A,compute_uv=False)
    return float(sig[-1]),sig

def projected_masses(B,selected):
    u,s,v=np.linalg.svd(B,full_matrices=True)
    assert sum(s<1e-9)==15
    E=np.zeros_like(B)
    for i,j in selected:E[i,j]+=1
    M=u[:,25:].T@E@v.T[:,25:]
    sig=np.linalg.svd(M,compute_uv=False)
    return M,sig

def greedy(B,edges,P,R,rng):
    order=rng.permutation(len(edges))
    Qp=np.zeros((40,0));Ql=np.zeros((40,0));choice=[]
    for ix in order:
        p,l=edges[ix]
        a=P[:,p]-(Qp@(Qp.T@P[:,p]) if len(choice) else 0)
        b=R[:,l]-(Ql@(Ql.T@R[:,l]) if len(choice) else 0)
        na=np.linalg.norm(a);nb=np.linalg.norm(b)
        if na>1e-7 and nb>1e-7:
            Qp=np.column_stack((Qp,a/na))
            Ql=np.column_stack((Ql,b/nb))
            choice.append((p,l))
        if len(choice)==15:return choice
    return None

def main(path=None):
    B,edges,G=build()
    prior=json.loads((Path(__file__).resolve().parents[1]/"data/w33_20261109_minimal_15_flux_lift.json").read_text())
    initial=[(x["point"],x["line"]) for x in prior["constructed_phase_only_pi_flip_links"]]
    initial_gap,_=gap(B,initial)
    M,sm=projected_masses(B,initial)
    assert len(sm)==15 and sm.min()>1e-10
    diff=B.copy().astype(float)
    for p,l in initial:diff[p,l]=-1
    assert np.linalg.matrix_rank(diff)==40
    asymptotic=[]
    for t in (0.02,0.01,0.005,0.002):
        T=B.astype(complex)
        for p,l in initial:T[p,l]=np.exp(1j*t)
        actual=np.linalg.svd(T,compute_uv=False)[25:]
        predicted=abs(np.expm1(1j*t))*sm
        asymptotic.append({"theta":t,
            "relative_15_mass_spectrum_error":float(np.linalg.norm(actual-predicted)/np.linalg.norm(predicted)),
            "minimum_exact_gap":float(actual[-1]),
            "minimum_first_order_gap":float(predicted[-1])})
    assert asymptotic[-1]["relative_15_mass_spectrum_error"]<.01

    AP=B@B.T-4*np.eye(40)
    AL=B.T@B-4*np.eye(40)
    P=(8*np.eye(40)-4*AP+np.ones((40,40)))/24
    R=(8*np.eye(40)-4*AL+np.ones((40,40)))/24
    rng=np.random.default_rng(2026110921)
    tested=0;valid=0
    best=initial.copy();bestgap=initial_gap
    random_gaps=[]
    for trial in range(500):
        choice=greedy(B,edges,P,R,rng)
        tested+=1
        if choice is None:continue
        valid+=1
        g,_=gap(B,choice)
        random_gaps.append(g)
        if g>bestgap+1e-12:
            bestgap=g;best=choice
    # local swaps retain exactly 15 modified edges: reject rank-deficient
    moves=0;accepted=0
    for step in range(2400):
        q=int(rng.integers(0,15));cand=edges[int(rng.integers(0,len(edges)))]
        if cand in best:continue
        proposal=best.copy();proposal[q]=cand
        g,_=gap(B,proposal);moves+=1
        if g>bestgap+1e-9:
            bestgap=g;best=proposal;accepted+=1
    assert bestgap>=initial_gap
    mat=B.astype(int)
    for p,l in best:mat[p,l]=-1
    det=Matrix(mat.tolist()).det(method="domain-ge")
    assert det!=0 and np.linalg.matrix_rank(mat)==40
    m2,s2=projected_masses(B,best)
    # First-order min gap is positive iff selected endpoints form a
    # common dark-gram basis; no need for a global optimiser theorem.
    assert s2[-1]>1e-10
    out={"status":"PASS_W33_15_DARK_MASSES_GAP_DESIGN",
         "native_chiral_zero_modes":30,
         "dark_effective_mass_matrix_dimension":[15,15],
         "dark_effective_mass_singular_spectrum_initial":[float(s) for s in sm],
         "first_order_minimal_mass_slope_initial":float(sm[-1]),
         "first_order_mass_formula":"low singular masses = |exp(i theta)-1| singular_values(U_dark† E_selected V_dark) + O(theta²), where E_selected is the rank-15 selected-edge indicator",
         "near_zero_phase_comparison":asymptotic,
         "initial_15_edge_minimum_singular_gap_pi":initial_gap,
         "stochastic_gap_search":{"random_starts_attempted":tested,
               "found_valid_matroid_bases":valid,
               "random_start_min_gap":float(min(random_gaps)),
               "random_start_median_gap":float(np.median(random_gaps)),
               "random_start_max_gap":float(max(random_gaps)),
               "hill_swaps_tested":moves,
               "hill_accepted_improvements":accepted},
         "best_15_edge_minimum_singular_gap_pi":bestgap,
         "gap_improvement_ratio":bestgap/initial_gap,
         "best_15_edges":[{"point":p,"line":l} for p,l in best],
         "best_exact_signed_integer_determinant":str(det),
         "best_first_order_minimal_mass_slope":float(s2[-1]),
         "best_production_still_uses_only_15_phase_flips":True,
         "honesty":"Stochastic search is not a global optimum or a dynamical flux law. The first-order mass matrix is an effective *spectral perturbation* on a finite one-body Hamiltonian, not standard-model fermion masses, topological protection or a Weyl index. Changing 15 links breaks full PSp symmetry."}
    if path:Path(path).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("W33_MASS_GAP",json.dumps({"initial":initial_gap,"best":bestgap,
             "improvement":bestgap/initial_gap,"bestdet":str(det),
             "mass_slope":float(sm[-1]),"valid":valid,"accepted":accepted}))
    return out

if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
