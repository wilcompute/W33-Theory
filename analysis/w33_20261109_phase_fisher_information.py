#!/usr/bin/env python3
"""A-optimal phase information: W33 selected forest vs redundant pairs.

Uses the full physical conditional POVM for known nine-mode transfer K;
no numerical normal approximation is used for an exact coverage claim.
This is locally asymptotic classical FI only under the phase-only device.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from w33_20261109_full_povm_calibration_bound import make_model
from w33_20261109_phase25_structured_calibration import forest,probes,probabilities

def all_pairs(K):
    return [(j,k) for j in range(9) for k in range(j+1,9)
            if max(abs(K[:,j].conj()*K[:,k]))>1e-10]

def fi_per_launch(K,theta,edges,roots):
    n=9
    D=np.exp(1j*theta)
    KD=K*D[None,:]
    inputs=probes(edges)
    amps=inputs@KD.T
    click=np.abs(amps)**2
    p=np.column_stack([click,1-click.sum(axis=1)])
    phase_diff=(2*np.real(np.conj(amps)[:,:,None]*(1j*inputs[:,None,:]*KD[None,:,:])))
    deriv=np.concatenate([phase_diff,-phase_diff.sum(axis=1,keepdims=True)],axis=1)
    assert deriv.shape==(len(inputs),10,9)
    assert np.min(p)>-1e-10
    # Include even very tiny outcomes accurately without setting FI
    # to infinity; absent outcomes must have exactly zero derivative.
    mask=p>1e-14
    F=np.einsum("qbk,qbl,qb->kl",deriv,deriv,np.where(mask,1/np.maximum(p,1e-14),0))/len(inputs)
    free=[i for i in range(9) if i not in roots]
    F=F[np.ix_(free,free)]
    eig=np.linalg.eigvalsh(F)
    assert min(eig)>1e-10,(min(eig),edges,roots)
    return {"phase_parameter_count":len(free),
            "probe_count":len(inputs),
            "local_Fisher_smallest_eigenvalue_per_total_launch":float(min(eig)),
            "phase_trace_Cramer_Rao_per_total_launch":float(np.trace(np.linalg.inv(F))),
            "phase_worst_axis_variance_per_total_launch":float(1/min(eig))}

def main(path=None):
    Kbase,_,_,_=make_model()
    rng=np.random.default_rng(202611092341)
    rows=[]
    for j,K in enumerate(Kbase):
        roots,tree=forest(K)
        dense=all_pairs(K)
        phase=rng.uniform(-.08,.08,size=9)
        t=fi_per_launch(K,phase,tree,roots)
        f=fi_per_launch(K,phase,dense,roots)
        assert f["phase_parameter_count"]==t["phase_parameter_count"]
        rows.append({"context":j,"connected_components":len(roots),
                     "forest_edge_count":len(tree),"all_observable_pair_edges":len(dense),
                     "forest":t,"dense":f,
                     "forest_trace_variance_over_dense":t["phase_trace_Cramer_Rao_per_total_launch"]/f["phase_trace_Cramer_Rao_per_total_launch"]})
    # Numerical bound pertains to asymptotic CR only, not the conservative
    # finite-count Hoeffding phase chord confidence from last round.
    out={"status":"PASS_AOPTICAL_POVM_PHASE_INFORMATION_FOREST_VS_REDUNDANCY",
         "model":"known K_cal with ONLY input phase offsets; 9 input basis probes plus 2 real/imag coherent probes per edge; every click and no-click outcome contributes Fisher information",
         "two_methods":["maximum-overlap spanning forest of observable edges","all observable input pair-interference edges"],
         "per_setting":rows,
         "mean_forest_over_dense_local_trace_CRLB":float(np.mean([r["forest_trace_variance_over_dense"] for r in rows])),
         "contexts_with_dense_better_than_forest":sum(r["forest_trace_variance_over_dense"]>1 for r in rows),
         "scope":"Asymptotic local CRLB under exact known K and phase-only stationary calibration. Unlike finite-shot simultaneous coverage certificates, does not yield a rigorous effect-norm confidence bound; overcomplete calibration may improve phase covariance but costs more probe configurations and does not automatically beat the 81-probe generic uncertainty certificate.",
         "novelty":"Repository-specific optimality diagnostic for observable phase-support graph; experimental design criterion is standard classical Fisher/A-optimal design."}
    if path:Path(path).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("FISHER_PHASE",json.dumps({"forest_vs_dense_ratios":[round(r["forest_trace_variance_over_dense"],3) for r in rows],
      "dense_advantage_count":out["contexts_with_dense_better_than_forest"]}))
    return out

if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
