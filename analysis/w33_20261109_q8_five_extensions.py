#!/usr/bin/env python3
"""Five follow-on W33 experiments: norm SDP, Pyramid/Horodecki PPT, optical routing,
Ward identity/dimension diagnostics, DES Y6 public-data readiness.
No physical experiment or new cosmological likelihood is claimed.
"""
import itertools
import json
import math
import sys
from pathlib import Path

import cvxpy as cp
import numpy as np
import sympy as sp
from scipy.optimize import linprog

from w33_20261109_q8_correlation_five import (
    frames, hermitian_basis, frame_map, probabilities, tensor_direct,
    tensor_recovered, trace_norm, min_dual_lp, continuum_null
)
from w33_20261109_q8_tiles_ppt_exact import exact_tiles
from w33_20261109_five_fronts import geometry, gauge_geometry_and_action

ROOT = Path(__file__).resolve().parents[1]

def pyramid_state():
    h=math.sqrt(math.cos(math.pi/5))
    V=np.array([[math.cos(2*math.pi*k/5),
                 math.sin(2*math.pi*k/5),h] for k in range(5)],float)/math.sqrt(1+h*h)
    UPB=np.column_stack([np.kron(V[k],V[(2*k)%5]) for k in range(5)])
    err=float(np.max(abs(UPB.T@UPB-np.eye(5))))
    assert err<2e-14
    rho=(np.eye(9)-UPB@UPB.T)/4
    assert np.max(abs(rho@rho-rho/4))<2e-14
    pt=rho.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
    assert np.max(abs(pt-rho))<2e-14
    return rho,err

def horodecki_state(a):
    """Known 3x3 PPT-entangled family, Horodecki (1997), 0<a<1."""
    R=np.zeros((9,9),float)
    for i in (0,1,2,3,4,5,7): R[i,i]=a
    R[6,6]=R[8,8]=(1+a)/2
    for i,j in ((0,4),(0,8),(4,8)): R[i,j]=R[j,i]=a
    R[6,8]=R[8,6]=math.sqrt(1-a*a)/2
    R/=8*a+1
    assert min(np.linalg.eigvalsh(R))>-5e-14
    pt=R.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
    assert min(np.linalg.eigvalsh(pt))>-5e-14
    return R

def horodecki_symbolic_proof():
    a=sp.symbols('a',real=True,positive=True)
    d=8*a+1
    # Block decomposition of correlation T in repo's real Hermitian frame.
    # Five independent diagonal entries +/-a/d; the remaining 2x3 block:
    M=sp.Matrix([[a/d,0,0],
       [-sp.sqrt(3-3*a*a)/(3*d),sp.sqrt(3)*(a-1)/(6*d),(1-a)/(6*d)]])
    # Independently derive every symbolic T entry from the Horodecki density.
    R=sp.zeros(9)
    for j in (0,1,2,3,4,5,7):
        R[j,j]=a
    R[6,6]=R[8,8]=(1+a)/2
    for i,j in ((0,4),(0,8),(4,8)):
        R[i,j]=R[j,i]=a
    R[6,8]=R[8,6]=sp.sqrt(1-a*a)/2
    R/=d
    H=[]
    for i in range(3):
        for j in range(i+1,3):
            X=sp.zeros(3); X[i,j]=X[j,i]=1/sp.sqrt(2); H.append(X)
            Y=sp.zeros(3); Y[i,j]=-sp.I/sp.sqrt(2);Y[j,i]=sp.I/sp.sqrt(2);H.append(Y)
    H += [sp.diag(1,-1,0)/sp.sqrt(2),sp.diag(1,1,-2)/sp.sqrt(6)]
    Texact=sp.Matrix(8,8,lambda i,j:sp.simplify(sp.trace(R*sp.kronecker_product(H[i],H[j]))))
    Tclaimed=sp.zeros(8)
    for j in range(6):
        Tclaimed[j,j]=(-1 if j%2 else 1)*a/d
    for j,val in zip((2,6,7),M.row(1)):
        Tclaimed[7,j]=val
    assert all(sp.simplify(Texact[i,j]-Tclaimed[i,j])==0 for i in range(8) for j in range(8))
    K=sp.simplify(M*M.T)
    squared=sp.factor(sp.trace(K))
    determinant=sp.factor(K.det())
    nuclear_sq=(a+2)**2/(9*d*d)
    assert sp.simplify(nuclear_sq-squared-2*a*(1-a)/(3*d*d))==0
    assert sp.simplify((2*a*(1-a)/(3*d*d))**2-4*determinant)==0
    # Since 0<a<1, all the square roots above have their positive sign.
    assert sp.simplify(5*a/d+(a+2)/(3*d)-sp.Rational(2,3))==0
    return dict(exact_nuclear_norm="2/3 for every 0<a<1",
       proof="five independent |a/(8a+1)| singular values and a rank-2 2x3 block with sum (a+2)/(3*(8a+1))",
       block_frobenius_squared=str(squared),block_gram_determinant=str(determinant),
       trace_norm_witness_blind_spot=True)

def ppt_benchmarks():
    operators=np.array(hermitian_basis())
    tiles=np.array(exact_tiles()[0],dtype=float)
    pyr,ortho=pyramid_state()
    results={}
    for name,rho in (('Tiles',tiles),('Pyramids',pyr)):
        T=tensor_direct(rho,operators)
        results[name]={"purity":float(np.trace(rho@rho)),
                       "PPT_min_eigenvalue":float(min(np.linalg.eigvalsh(rho.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)))),
                       "correlation_trace_norm":trace_norm(T),
                       "witness_excess":trace_norm(T)-2/3,
                       "F8":float(np.sum(T*T))}
        assert trace_norm(T)>2/3+.02
    rows=[]
    for a in (.01,.05,.1,.2,.3,.4,.5,.6,.7,.8,.9,.99):
        t=tensor_direct(horodecki_state(a),operators)
        rows.append({"a":a,"trace_norm":trace_norm(t),
                     "difference_from_2_over_3":trace_norm(t)-2/3})
    assert max(abs(r["difference_from_2_over_3"]) for r in rows)<2e-13
    return {"pyramid_UPB_orthogonality_error":ortho,
            "two_UPB_benchmarks":results,
            "Horodecki_PPT_family_scan":rows,
            "Horodecki_all_a_exact_proof":horodecki_symbolic_proof()}

def nuclear_sdp(E,A,rho,rel=.001,N=10000000,alpha=.05):
    """Conservative relaxation, minimizes full trace norm, unlike a frozen-dual LP.
    Simulated q_j set to its expectation for design-point comparison.
    """
    eff=np.array([.63+.045*j for j in range(9)])
    lo,hi=eff*(1-rel),eff*(1+rel)
    ps=np.array([probabilities(E[:,9*b:9*(b+1)],rho) for b in range(8)])
    q=ps*eff[None,:]
    q/=q.sum(axis=1,keepdims=True)
    eps=math.sqrt(math.log(2*72/alpha)/(2*N))
    p=cp.Variable((8,9),nonneg=True)
    v=cp.Variable((8,9),nonneg=True)
    s=cp.Variable(8)
    cons=[cp.sum(p,axis=1)==1,
          cp.sum(v,axis=1)==s,
          s>=np.min(lo),s<=np.max(hi),
          v>=cp.multiply(p,lo[None,:]),
          v<=cp.multiply(p,hi[None,:]),
          v>=cp.multiply(cp.reshape(s,(8,1),order="C"),np.maximum(0,q-eps)),
          v<=cp.multiply(cp.reshape(s,(8,1),order="C"),np.minimum(1,q+eps))]
    pflat=cp.reshape(p,(72,),order="C")
    T=cp.reshape(A.T@(pflat-np.full(72,1/9)),(8,8),order="C")
    objective=cp.Minimize(cp.normNuc(T))
    problem=cp.Problem(objective,cons)
    try:
        value=problem.solve(solver="CLARABEL",tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8,max_iter=300)
    except Exception:
        value=problem.solve(solver="SCS",eps=1e-7,max_iters=50000)
    assert problem.status in ("optimal","optimal_inaccurate"),problem.status
    lp=min_dual_lp(A,q,lo,hi,eps)
    # SDP relaxed parameter space contains true p, so optimal <= true norm.
    true=trace_norm(tensor_direct(rho,np.array(hermitian_basis())))
    assert value<=true+1e-4
    assert value+1e-4>=lp["lower_bound"]
    return {"solver_status":problem.status,
            "solver":str(problem.solver_stats.solver_name),
            "solver_approx_full_min_nuclear_norm":float(value),
            "prior_lp_rigorous_dual_lower_bound":lp["lower_bound"],
            "gain_over_fixed_dual":float(value-lp["lower_bound"]),
            "true_trace_norm":true,
            "assumed_efficiency_relative_error":rel,
            "accepted_N_per_basis":N,
            "expected_conditional_frequencies_only":True,
            "95pct_simultaneous_radius":eps,
            "certifies_PPT_entanglement_numerically":bool(value>2/3+1e-4),
            "scope":"Numerical SDP is diagnostic, not a machine-certified lower bound; only LP dual plus interval proof is conservative and robust to solver numerical error"}

def optimize_tests():
    E=frames()[1][0]
    A=frame_map(E,np.array(hermitian_basis()))
    tiles=np.array(exact_tiles()[0],float)
    pyr,_=pyramid_state()
    out={}
    for name,rho in (("Tiles",tiles),("Pyramids",pyr)):
        out[name]=nuclear_sdp(E,A,rho,rel=.001,N=10000000)
    return out

def tomography_kernel_no_go():
    fam=frames()[1]
    r0=np.eye(9)/9
    r1=np.kron(np.diag([1.,0,0]),np.eye(3)/3)
    assert np.max(abs(r1-r0))>.01
    err=max(float(np.max(abs(probabilities(E,r0)-probabilities(E,r1))))
            for E in fam)
    assert err<3e-14
    return {"all_24_Choi_MUB_bases_unable_to_distinguish_these_two_states":True,
        "max_outcome_probability_difference":err,
        "global_purities":[float(np.trace(r0@r0)),float(np.trace(r1@r1))],
        "density_example":"rho0=I9/9; rho1=|0><0| tensor I3/3",
        "reason":"Every maximally entangled measurement vector has maximally mixed local reductions, so the 16 local Bloch coefficients are in the exact kernel",
        "consequence":"Do not infer pure-state entanglement entropy or source purity without independent local measurements or a trusted preparation promise"}

def optical_routing():
    desired=[3*((c-r)%3)+r for r in range(3) for c in range(3)]
    inv=sum(desired[i]>desired[j] for i in range(9) for j in range(i+1,9))
    arr=list(desired); ids=list(range(9));use=[0]*9;layers=[]
    for step in range(10):
        swaps=[]
        for j in range((step+1)%2,8,2):
            if arr[j]>arr[j+1]:
                swaps.append((j,j+1))
                use[ids[j]]+=1;use[ids[j+1]]+=1
                arr[j],arr[j+1]=arr[j+1],arr[j]
                ids[j],ids[j+1]=ids[j+1],ids[j]
        if swaps: layers.append(swaps)
        if arr==sorted(desired):break
    assert arr==list(range(9)) and len(layers)==6 and sum(map(len,layers))==inv==13
    return {"logical_permutation_input_to_output":desired,
            "minimal_adjacent_swaps_in_one_linear_rail_order":inv,
            "constructed_parallel_layers":layers,
            "parallel_layer_depth":len(layers),
            "per_logical_mode_swap_exposures":use,
            "max_rail_swap_exposures":max(use),
            "conditional_transmissions_for_t_per_swap_0p995":[round(.995**n,10) for n in use],
            "previous_unitary_two_mode_couplers":18,
            "if_all_13_SWAPS_require_2mode_components_total_upper_budget":31,
            "caution":"Crossings may implement ideal permutations geometrically; counting them as tunable 2-mode couplers is conservative hardware-specific; exposure loss assumes independent identical 0.5% intensity loss per crossing."}

def gauge_covariance():
    # Build native point-line graph and verify Ward identity in the independent code.
    facts=gauge_geometry_and_action()
    assert facts["free_U1_cycle_fluxes"]==81
    assert facts["relative_gauge_action_error"]<2e-12
    return {"native_gauge":{k:facts[k] for k in (
        "incidence_graph_vertices","incidence_edges","distinct_eight_cycles",
        "free_U1_cycle_fluxes","relative_gauge_action_error",
        "laplacian_covariance_error")},
        "continuum":continuum_null()["running_dimensions"],
        "quantitative_falsifier":"The native 80-vertex finite incidence graph has no continuum 3+1D Weyl law; any 3D/4D plateau in Levi x Z^d is determined by the externally input d.",
        "not_established":"nonperturbative Ward-identity-controlled continuum, anomaly-free chiral fermions, dynamical metric, Lorentz invariance"}

def des_release_gate():
    prereg=json.loads((ROOT/"analysis/toe_uv/prereg_noshear.json").read_text())
    assert prereg["S9_shear_no_split"]["frozen"]=="2026-11-08"
    return {"survey":"DES Year 6, 2026-11-09 readiness audit",
      "public_data_release":"https://des.ncsa.illinois.edu/releases/y6a2/",
      "official_Y6_papers":"https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/",
      "public_pipeline_examples":"https://github.com/des-science/y6-ppd-public/",
      "public_des_index_cached":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/",
      "unblinded_candidate_url":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/3x2pt_2025-07-28-20h_UNBLINDED_wmask_nob2.fits",
      "unblinded_candidate_direct_HTTP_2026_11_09":404,
      "direct_download_status":"FAILED_404; stale cached indexed listing cannot be treated as current download access",
      "external_dataset_manifest_2026_11_04":"https://glama.ai/mcp/servers/nesar-ai-assistant/weak-lensing-mcp-server",
      "prior_report":"External survey directory indexed an unblinded 22 MB 3x2pt FITS three months earlier, but direct exact GET on 2026-11-09 returned 404. No data-vector bytes or covariance were acquired.",
      "required_named_inputs":["unblinded cosmic shear xi+/- data-vector","matched complete covariance","redshift-bin n(z)","NLA nuisance priors","corrected scalar-field CLASS/Halofit theory","scale cuts xi+>10',xi->60'","held-out nuisance refit"],
      "S9_scored":False,
      "why_not":"Could not verify and process complete unblinded Y6 xi+/- 2pt FITS plus matched covariance and theory refit; published conditional S8 posterior is NOT the S9 likelihood.",
      "safe_null":"No model-specific chi-squared, p-value, sigma or falsification status may be inferred from a conditional Y6 LambdaCDM S8 number."}

def main(outpath=None):
    data={"status":"PASS_EXACT_PPT_BLINDSPOT_OPTICAL_ROUTING_TOY_SDP_AND_S9_NOT_SCORED",
          "PPT_benchmarks":ppt_benchmarks(),
          "robust_SDP":optimize_tests(),
          "information_kernel":tomography_kernel_no_go(),
          "optical_routing":optical_routing(),
          "gauge_continuum":gauge_covariance(),
          "DES_Y6_gate":des_release_gate(),
          "limitations":"Tight Schmidt witness is finite quantum information; SDP numerical optimality not rigorous; no experimental chip, continuum TOE or new Y6 likelihood."}
    if outpath:
        Path(outpath).write_text(json.dumps(data,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("PASS five_extensions",json.dumps({
        "Pyramid_norm":data["PPT_benchmarks"]["two_UPB_benchmarks"]["Pyramids"]["correlation_trace_norm"],
        "Horodecki_constant":data["PPT_benchmarks"]["Horodecki_all_a_exact_proof"]["exact_nuclear_norm"],
        "SDP":{k:v["solver_approx_full_min_nuclear_norm"] for k,v in data["robust_SDP"].items()},
        "mode_swaps":data["optical_routing"]["minimal_adjacent_swaps_in_one_linear_rail_order"],
        "local_kernel":data["information_kernel"]["max_outcome_probability_difference"],
        "S9_scored":False
    }))
    return data
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
