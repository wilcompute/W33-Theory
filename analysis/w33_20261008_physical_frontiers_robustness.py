#!/usr/bin/env python3
"""Six independent, scope-limited TOE interface follow-ups, October 8 2026.

NO proof of quantum advantage, Einstein gravity, physical CP asymmetry,
compactification viability, physical Yukawa masses, or cosmological screening.
"""
from __future__ import annotations

import itertools, json, math, sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp
from scipy.linalg import eigh

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_six_toe_frontier_followthrough as PREV
from w33_20261008_dual_27_electrical_transport import build_graphs
from w33_20261008_five_physics_frontiers import FIELDS
OUT=ROOT/"data"/"w33_20261008_physical_frontiers_robustness.json"


def coherent_device():
    """Permutation-invariant readout statistic and norm-certified robustness."""
    gs=build_graphs()
    eig={key:(np.linalg.eigh(a)[0],np.linalg.eigh(a)[1]) for key,a in gs.items()}
    def amplitudes(key,t):
        vals,vecs=eig[key]
        return (vecs*np.exp(-1j*t*vals))@vecs.T
    def maxoff(key,t):
        p=np.abs(amplitudes(key,t))**2
        return float(np.max(p[~np.eye(27,dtype=bool)]))
    # Prespecified grid, best certified gap/t among those tested.
    best=None
    for t in np.linspace(.10,2.0,191):
        q=maxoff("point_far_H27",t)
        l=maxoff("line_transverse_null",t)
        gap=q-l
        if gap<=0:continue
        margin=gap/(4*t)
        if best is None or margin>best["guaranteed_operator_norm_epsilon"]:
            best={"time":float(t),"point_max":q,"line_max":l,
                  "probability_gap":gap,"guaranteed_operator_norm_epsilon":float(margin)}
    assert best is not None
    # Duhamel: ||exp(-it(H+E))-exp(-itH)|| <= |t| ||E||,
    # hence each transition-probability difference <= 2|t| ||E||.
    # Two devices -> observable gap margin >= Delta-4|t|epsilon.
    t=best["time"]
    rng=np.random.default_rng(20261008)
    delta=min(0.005,best["guaranteed_operator_norm_epsilon"]/15)
    trials=32
    survived=0
    observed=[]
    for _ in range(trials):
        maxima={}
        for name,a in gs.items():
            diagonal=rng.uniform(-delta,delta,27)
            raw=rng.uniform(-delta,delta,(27,27))
            raw=np.triu(raw,1)
            off=(raw+raw.T)*a
            e=off+np.diag(diagonal)
            assert np.linalg.norm(e,ord=2)<=9*delta+1e-12
            vals,v=eigh(a+e,check_finite=False)
            u=(v*np.exp(-1j*t*vals))@v.T
            maxima[name]=float(np.max((np.abs(u)**2)[~np.eye(27,dtype=bool)]))
        separation=maxima["point_far_H27"]-maxima["line_transverse_null"]
        survived+=int(separation>0)
        observed.append(separation)
    assert survived==trials
    assert best["probability_gap"]>0 and 9*delta<best["guaranteed_operator_norm_epsilon"]
    best.update({"analytic_probability_shift_bound":"2 |t| ||E||_2 per probability",
                 "two_device_gap_bound":"Delta - 4 |t| epsilon",
                 "edge_and_onsite_uniform_error_delta":float(delta),
                 "operator_norm_bound_via_max_row_sum":float(9*delta),
                 "random_seed":20261008,
                 "disorder_trials":trials,
                 "separation_survivors":survived,
                 "noisy_gap_min":float(min(observed)),
                 "noisy_gap_max":float(max(observed)),
                 "label_free_observable":"largest off-diagonal single-photon output probability",
                 "scope":"ideal 27-mode addressability and a known normalized coupling scale; no physical calibration"})
    return best


def modular_rank(vectors,p=101):
    basis=[]
    for v in vectors:
        w=[int(x)%p for x in np.asarray(v).reshape(-1)]
        for pivot,row in basis:
            if w[pivot]:
                c=w[pivot];w=[(x-c*y)%p for x,y in zip(w,row)]
        pivot=next((i for i,x in enumerate(w) if x),None)
        if pivot is not None:
            scale=pow(w[pivot],-1,p)
            basis.append((pivot,[(x*scale)%p for x in w]))
            basis.sort(key=lambda x:x[0])
    return len(basis)


def gravity_algebra():
    n=8;mod=101
    gen=[]
    for i in range(n):
        j=(i+1)%n
        x=np.zeros(n,np.int64);z=np.zeros(n,np.int64)
        x[i]=x[j]=1;z[i]=1;z[j]=-1
        gen.append(np.outer(x,z)%mod)
    closure=[]
    for g in gen:
        if modular_rank(closure+[g],mod)>len(closure):closure.append(g)
    for m in closure:
        for g in gen:
            v=(m@g-g@m)%mod
            if modular_rank(closure+[v],mod)>len(closure):
                closure.append(v)
    assert len(closure)==34
    comms=[(a@b-b@a)%mod for a in closure for b in closure]
    derived=modular_rank(comms,mod)
    # center must commute with all generators (therefore the generated algebra).
    columns=[]
    for x in closure:
        columns.append(np.concatenate([((x@g-g@x)%mod).reshape(-1) for g in gen]))
    # integer matrix rank over F_101 for the center linear system
    commutator_column_rank=modular_rank(columns,mod)
    center=34-commutator_column_rank
    assert derived<=34 and center>=0
    return {"original_generators":8,"generated_dimension_over_Q":PREV.rational_eight_cycle_closure_dimension(),
            "generated_dimension_mod_101":len(closure),
            "derived_ideal_dimension_mod_101":derived,"center_dimension_mod_101":center,
            "matrix_invariant_bound_dimension":48,
            "scope":"induced actual W33 Levi C8, not the full hypersurface deformation algebra"}


def flag_topology():
    g=PREV.levi_graph()
    l=nx.line_graph(g)
    assert g.number_of_nodes()==80 and g.number_of_edges()==160
    assert l.number_of_nodes()==160 and l.number_of_edges()==480
    beta_g=g.number_of_edges()-g.number_of_nodes()+1
    beta_l=l.number_of_edges()-l.number_of_nodes()+1
    assert (beta_g,beta_l)==(81,321)
    triangles=sum(nx.triangles(l).values())//3
    assert triangles==320
    # Every original vertex contributes a K4 (six line-graph edges,
    # four local triangles, cycle rank three).
    assert sum(math.comb(g.degree(v),3) for v in g)==320
    local_excess=sum(math.comb(g.degree(v)-1,2) for v in g)
    assert beta_l-beta_g==local_excess==240
    # For a Z2 edge field, mod gauge there are 2**beta cycles
    return {"original_levi_cycle_rank":81,
            "flag_line_graph_cycle_rank":321,
            "extra_flag_graph_cycle_rank":240,
            "flag_graph_triangles":triangles,
            "local_K4_sites":80,
            "local_K4_cycle_rank_each":3,
            "flat_Z2_connection_classes_original":str(2**81),
            "flat_Z2_connection_classes_flag_graph":str(2**321),
            "flag_ising_vacua_from_previous":2,
            "distinction":"unconstrained Z2 edge holonomies (2^beta) are NOT the 2 Ising vertex ground states",
            "320_warning":"320 local triangles equals prior count of 320 quartic chiral vacua numerically; no natural equivariant identification shown"}


def discrete_vacuum():
    prev=PREV.p6_frontier()
    q=prev["known_proton_hexality_Z6"]
    # Charges with left-chiral superfield conventions, always integral:
    u={k:int(6*FIELDS[k]["Y"]) for k in ("Q","Uc","Dc","L","Ec","Nc","Hu","Hd")}
    b={k:int(3*FIELDS[k]["BL"]) for k in u}
    candidates=[]
    for a in range(6):
        for c in range(6):
            if all((a*b[k]+c*u[k]-q[k])%6==0 for k in u):
                candidates.append([a,c])
    assert candidates==[]
    # Immediate obstruction: Q requires a+c=0 and Uc demands
    # -a-4c=1; c=-a gives 3a=1 mod6, impossible.
    assert b["Q"]==u["Q"]==1
    assert b["Uc"]==-1 and u["Uc"]==-4
    assert (3*0)%6!=1 and (3*1)%6!=1
    # More general: regardless of generation labels, Q/Uc pin a no-go.
    allowed={key:(sum(q[x] for x in PREV.OPS[key])%6==0)
             for key in PREV.OPS}
    assert allowed["weinberg"] and not allowed["QQQL"] and not allowed["UUDE"]
    return {"known_proton_hexality_assignment":q,
            "sixY":u,"threeBL":b,
            "solutions_qP6_equals_a3BL_plus_b6Y_mod6":candidates,
            "two_multiplet_modular_obstruction":"Q gives a+b=0; Uc then gives 3a=1 (mod 6), impossible",
            "consequence":"Additional discrete/continuous generator is necessary beyond only Y and B-L for this chosen P6 residue set",
            "operator_veto":allowed,
            "string_vacuum_status":"not constructed, FI/spectrum/worldsheet/anomaly sufficiency unverified"}


def physical_flavor():
    # Source-proved holomorphic quotient value C=1/2, for the published
    # residue and Serre basis. Z_i and universal e^(K/2) are NOT supplied.
    C=F(1,2)
    zrange=(F(1),F(4))
    smallest=F(1,16)
    largest=C
    assert float(smallest)==0.0625 and float(largest)==0.5
    # Covariant singular value inequality for arbitrary SPD K1,K2 with
    # mI<=K<=MI: sigma_i(Y)/M <= sigma_i(K1^-1/2 Y K2^-1/2)<=sigma_i(Y)/m.
    Y=np.array([[.5,.03j,.02],[.01,.1,.005j],[.005,.02,.01]],complex)
    s=np.linalg.svd(Y,compute_uv=False)
    rng=np.random.default_rng(314159)
    worst_lo=1.;worst_hi=0.
    for _ in range(64):
        k=[]
        for _ in range(2):
            r=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
            u,_=np.linalg.qr(r)
            d=rng.uniform(1,4,3)
            k.append((u*(d**-.5))@u.conj().T)
        sn=np.linalg.svd(k[0]@Y@k[1],compute_uv=False)
        ratio=sn/s
        assert np.all(ratio>=1/4-1e-11) and np.all(ratio<=1+1e-11)
        worst_lo=min(worst_lo,float(min(ratio)));worst_hi=max(worst_hi,float(max(ratio)))
    return {"actual_repo_C_holomorphic":"1/2",
            "assumed_positive_Z_interval":["1","4"],
            "conditional_physical_magnitude_interval_eKhalf_fixed":["1/16","1/2"],
            "normalization_span_factor":8,
            "rank_preserved_by_invertible_kinetic_matrices":True,
            "full_matrix_singular_value_bounds":"sigma_i(Y)/4 <= sigma_i(physical Y) <= sigma_i(Y) for K1,K2 eigenvalues in [1,4]",
            "seeded_random_metric_trials":64,
            "observed_min_singular_ratio":worst_lo,
            "observed_max_singular_ratio":worst_hi,
            "no_physical_prediction":"Z_i, Ricci-flat metric, HYM forms, complex structure vacuum, e^(K/2) and full holomorphic Yukawa not fixed"}


def flux_geometry():
    k=np.array([2]+[4]*7,dtype=int) # from Pass11754 U=A exp(-k dot lambda)
    # Positive sums of exponentials e^(-k_a dot lambda) have stationarity
    # condition 0=sum_a p_a k_a with p_a>0.
    # If each k_a lies in strictly positive orthant, impossible.
    supports=[k,2*k,k+1]
    assert all(np.all(v>0) for v in supports)
    assert np.all(np.sum(supports,axis=0)>0)
    # Construct independent toy 9-term positive potential in 8 variables:
    # U=sum_i exp(-lambda_i)+exp(sum_i lambda_i), stationary at 0.
    vecs=[np.eye(8,dtype=int)[i] for i in range(8)]+[-np.ones(8,dtype=int)]
    mat=np.stack(vecs)
    assert np.array_equal(mat.sum(axis=0),np.zeros(8,dtype=int))
    assert np.linalg.matrix_rank(mat)==8
    H=mat.T@mat
    eig=sorted(np.linalg.eigvalsh(H))
    assert np.allclose(eig,[1]*7+[9])
    # At least 9 exponent vectors are required for a strictly positive
    # affine dependence and full-dimensional span in R8.
    return {"actual_flat_torus_flux_exponent":k.tolist(),
            "same_orthant_positive_flows_stationary":False,
            "counterexample_model":"sum_i exp(-lambda_i) + exp(sum_i lambda_i) (supplied 9-term toy)",
            "minimal_full_dimensional_positive_balance_terms":9,
            "toy_stationary_at_origin":True,
            "toy_hessian_eigenvalues":[int(round(x)) for x in eig],
            "toy_potential_value_at_origin":9,
            "full_Einstein_solution_or_CC_screening_derived":False,
            "warning":"toy exp terms are not verified allowed E8 flux, string compactification or 4D action"}


def build():
    return {"scope":"finite / analytic necessary checks, supplied-device/noise and scalar toy models; TOE open",
            "coherent_photonic":coherent_device(),
            "gravity_lie":gravity_algebra(),
            "chiral_flag_topology":flag_topology(),
            "proton_hexality_origin":discrete_vacuum(),
            "physical_flavor":physical_flavor(),
            "flux_vacuum":flux_geometry()}


def main():
    ans=build()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(ans,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for k,v in ans.items():
        if k!="scope":print(k,json.dumps(v,sort_keys=True))
    print("PHYSICAL_FRONTIER_CHECKS_PASS")
    return ans


if __name__=="__main__":main()
