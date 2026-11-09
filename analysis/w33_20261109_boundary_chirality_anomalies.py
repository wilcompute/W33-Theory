#!/usr/bin/env python3
"""Native W33 chiral-index boundary test and explicit anomaly constraints.

A single deleted incidence vertex makes a rectangular 39x40 kernel and an
index of -1 for elementary dimension-counting reasons. That index persists
under arbitrary complex edge disorder, but is imposed by removing a site,
not predicted by the closed W33 geometry. Standard Model anomaly checks
are on EXTERNALLY SUPPLIED representation assignments.
"""
import json,sys
from pathlib import Path
import numpy as np
import sympy as sp
from w33_20261109_five_fronts import geometry

def incidence():
    _,lines,rows=geometry()
    B=np.zeros((40,40),dtype=int)
    for i,nn in enumerate(rows):
        for j in nn:B[i,j]=1
    assert int(B.sum())==160
    return B

def ranks_boundary(B):
    intact=int(sp.Matrix(B).rank())
    reduced_rank=[int(sp.Matrix(np.delete(B,i,axis=0)).rank()) for i in range(40)]
    assert intact==25
    assert all(x==25 for x in reduced_rank)
    return {"closed_incidence_rank_over_Q":intact,
            "all_single_point_deleted_boundary_ranks":reduced_rank,
            "closed_plus_zero_modes":40-intact,
            "closed_minus_zero_modes":40-intact,
            "deleted_plus_zero_modes":39-25,
            "deleted_minus_zero_modes":40-25,
            "deleted_index":-1,
            "closed_index":0}

def random_disorder_test(B):
    rng=np.random.default_rng(20261109213)
    per_state=[]
    for seed in range(8):
        phases=rng.uniform(0,2*np.pi,size=B.shape)
        C=B.astype(complex)*np.exp(1j*phases)
        sing=np.linalg.svd(C,compute_uv=False)
        boundary=np.delete(C,0,axis=0)
        sv=np.linalg.svd(boundary,compute_uv=False)
        rankC=np.linalg.matrix_rank(C,tol=1e-8)
        rankBd=np.linalg.matrix_rank(boundary,tol=1e-8)
        assert rankC==40 and rankBd==39
        # Net index: plus kernel=0, minus kernel=1 for rectangular 39x40.
        u,s,vh=np.linalg.svd(boundary,full_matrices=True)
        vec=vh[-1,:].conj()
        assert np.linalg.norm(boundary@vec)<2e-12
        ipr=float(sum(abs(vec)**4))
        per_state.append({"trial":seed,"closed_min_singular":float(min(sing)),
                          "open_min_nonzero_singular":float(min(sv)),
                          "open_index":-1,
                          "boundary_zero_mode_inverse_participation_ratio":ipr,
                          "boundary_zero_mode_support_estimate":1/ipr})
    # Pure U1 vertex/line phases (not independent edge holonomy) cannot
    # change the singular spectra or zero-mode counts.
    phi=rng.uniform(0,2*np.pi,39)
    psi=rng.uniform(0,2*np.pi,40)
    base=np.delete(C,0,axis=0)
    gauged=np.exp(1j*phi)[:,None]*base*np.exp(-1j*psi)[None,:]
    maxerr=float(np.max(abs(np.linalg.svd(gauged,compute_uv=False)-np.linalg.svd(base,compute_uv=False))))
    assert maxerr<1e-12
    return {"independent_edge_holonomy_controls":per_state,
            "vertex_phase_gauge_covariance_singular_error":maxerr,
            "boundary_index_is_site_imbalance":True,
            "limitation":"Stable -1 index is forced by the imposed rectangular matrix, not by an intrinsic W33 topological invariant. An unpaired null state in a finite charged system does not imply anomaly cancellation, a Weyl cone, locality of a 3+1D theory, or emergent chiral matter."}

def anomaly_gate():
    # Five *left-handed* Weyl representation multiplets per Standard Model
    # generation. conjugated u_R, d_R, e_R supply negative/positive Y as below.
    R=sp.Rational
    rep=[
      {"name":"Q_L","mult":6,"Y":R(1,6),"su3_fund":2,"su2_doublet":3},
      {"name":"u_R_conjugate","mult":3,"Y":R(-2,3),"su3_fund":1,"su2_doublet":0},
      {"name":"d_R_conjugate","mult":3,"Y":R(1,3),"su3_fund":1,"su2_doublet":0},
      {"name":"L_L","mult":2,"Y":R(-1,2),"su3_fund":0,"su2_doublet":1},
      {"name":"e_R_conjugate","mult":1,"Y":R(1),"su3_fund":0,"su2_doublet":0}]
    su3=R(1,2)*sum(x["su3_fund"]*x["Y"] for x in rep)
    su2=R(1,2)*sum(x["su2_doublet"]*x["Y"] for x in rep)
    cubic=sum(x["mult"]*x["Y"]**3 for x in rep)
    grav=sum(x["mult"]*x["Y"] for x in rep)
    doublets=sum(x["su2_doublet"] for x in rep)
    assert su3==su2==cubic==grav==0 and doublets%2==0
    return {"SU3_sq_U1":str(su3),"SU2_sq_U1":str(su2),
            "U1_cubed":str(cubic),"gravitational_U1":str(grav),
            "SU2_left_doublet_count":doublets,
            "Witten_global_SU2_even_doublets":doublets%2==0,
            "status":"PASS_EXACT_IF_STANDARD_MODEL_REPS_SUPPLIED",
            "warning":"This only checks established Standard Model hypercharges input by hand. No W33 construction derives these representations, their observed masses/couplings or their chiral realization."}

def main(path=None):
    B=incidence()
    out={"status":"PASS_W33_BOUNDARY_INDEX_VERSUS_NATIVE_AND_INPUT_ANOMALIES",
         "rational_rank":ranks_boundary(B),
         "complex_disorder":random_disorder_test(B),
         "anomaly_gate":anomaly_gate(),
         "scope":"A stringent negative test: an index can be created by an externally imposed boundary imbalance and survives edge phases, but no evidence that W33 predicts a stable anomaly-free chiral fermion sector."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS chiral boundary anomaly",json.dumps({
       "closed":out["rational_rank"]["closed_index"],
       "cut":out["rational_rank"]["deleted_index"],
       "trials":len(out["complex_disorder"]["independent_edge_holonomy_controls"]),
       "cubic_anomaly":out["anomaly_gate"]["U1_cubed"]}))
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
