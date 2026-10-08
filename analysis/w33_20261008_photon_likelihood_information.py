#!/usr/bin/env python3
"""Single-device photonic topology-test Bhattacharyya benchmarks.

Two alternative 27-port walks are treated as simple hypotheses, with
ideal logical couplers. Known-source self probability and adversarial
relabeling of 26 destinations are included explicitly. Measured device
loss and systematic calibration uncertainty are NOT modeled.
"""
import sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_dual_27_electrical_transport import build_graphs
OUT=ROOT/"data"/"w33_20261008_photon_likelihood_information.json"
DEPTHS=(1,2,4,8,16,32,64)
design=json.loads((ROOT/"data/w33_20261008_five_physics_deepening.json").read_text())["physical_photonic"]

def unitary(a,layers,t,r):
    step=np.eye(27,dtype=np.complex128)
    theta=t/r; co=np.cos(theta); si=np.sin(theta)
    for matching in layers:
        m=np.eye(27,dtype=np.complex128)
        for i,j in matching:
            m[i,i]=co;m[j,j]=co
            m[i,j]=-1j*si;m[j,i]=-1j*si
        step=m@step
    u=np.linalg.matrix_power(step,r)
    assert np.max(np.abs(u.conj().T@u-np.eye(27)))<1e-10
    return u

def affinity(a,b):
    return float(np.dot(np.sqrt(a),np.sqrt(b)))

def study():
    graphs=build_graphs()
    res=[]
    for r in DEPTHS:
        probs={}
        for name,a in graphs.items():
            u=unitary(a,design[name]["nine_layer_schedule"],.78,r)
            probs[name]=np.abs(u)**2
        p=probs["point_far_H27"];q=probs["line_transverse_null"]
        ids=np.arange(27)
        # Input 0 fixed, self port recognized; only 26 outputs adversarially permuted.
        known=affinity(p[:,0],q[:,0])
        anonymous=[]
        sorted_self=[]
        for i in ids:
            k=ids[ids!=i]
            sorted_self.append(float(np.sqrt(p[i,i]*q[i,i])+
                              affinity(np.sort(p[k,i]),np.sort(q[k,i]))))
            anonymous.append(affinity(np.sort(p[:,i]),np.sort(q[:,i])))
        # Most conservative across source-index placements for two candidate
        # physical layouts (permutation of the source labels as well).
        worst_cross=0
        for i in ids:
            for j in ids:
                k=ids[ids!=i];l=ids[ids!=j]
                val=float(np.sqrt(p[i,i]*q[j,j])+
                          affinity(np.sort(p[k,i]),np.sort(q[l,j])))
                worst_cross=max(worst_cross,val)
        assert 0<=known<=1+1e-11
        assert max(sorted_self)<=1+1e-11
        # Genuinely permutation-INVARIANT classifier: sort the observed
        # 27-outcome histogram, compare distance to the two sets of
        # 27 sorted predicted distributions, and choose nearest set.
        # Separating margin is the min infinity distance over ALL
        # 27x27 possible source-port correspondences.
        template0=[np.sort(p[:,i]) for i in ids]
        template1=[np.sort(q[:,i]) for i in ids]
        margin=min(float(np.max(np.abs(a-b))) for a in template0 for b in template1)
        assert margin>1e-8
        for eta in (.98,.99,.995,.999):
            survival=eta**(9*r)
            b=1-survival*(1-worst_cross)
            n=math.ceil(math.log(1/(2*.05))/(-math.log(b))) if b<1 else None
            # Sorting is 1-Lipschitz for sup norm; if all 27
            # empirical bin frequencies are within margin/4, nearest
            # template is correctly classified irrespective of labels.
            # 27 Hoeffding events <= 2*27*exp(-2n*(margin/4)^2).
            sort_n=math.ceil(8*math.log(2*27/.05)/(margin**2))
            expected=math.ceil(sort_n/survival)
            res.append({"repetitions":r,"stages":9*r,"survival_per_stage":eta,
                        "min_full_anonymous_sorted_linf_margin":margin,
                        "successful_single_source_detections_sufficient_95pct":sort_n,
                        "expected_launches_under_uniform_loss_for_label_invariant_test":expected,
                        "worst_source_port_relabeling_affinity":worst_cross,
                        "best_case_exact_label_Bhatta_affinity":known,
                        "max_affinity_fixed_source_relabel_destinations":max(sorted_self),
                        "max_affinity_fully_anonymous_destination":max(anonymous),
                        "per_launched_erasures_included_affinity":b,
                        "error_5pct_Bhattacharyya_launch_upper_bound":n})
    summary={}
    for eta in (.98,.99,.995,.999):
        row=min((x for x in res if x["survival_per_stage"]==eta),
                key=lambda z:z["error_5pct_Bhattacharyya_launch_upper_bound"] if z["error_5pct_Bhattacharyya_launch_upper_bound"] is not None else float("inf"))
        summary[str(eta)]={k:row[k] for k in ("stages","repetitions","error_5pct_Bhattacharyya_launch_upper_bound","worst_source_port_relabeling_affinity")}
    sorted_results={}
    for eta in (.98,.99,.995,.999):
        row=min((z for z in res if z["survival_per_stage"]==eta),
                key=lambda z:z["expected_launches_under_uniform_loss_for_label_invariant_test"])
        sorted_results[str(eta)]={k:row[k] for k in (
                "stages","min_full_anonymous_sorted_linf_margin",
                "successful_single_source_detections_sufficient_95pct",
                "expected_launches_under_uniform_loss_for_label_invariant_test")}
    return {"experiments":res,"optimal_depths_by_eta":summary,
            "permutation_invariant_95pct_designs":sorted_results,
            "interpretation":"Sorted-histogram classifier handles arbitrary source and detector label permutations by comparing nearest predicted distribution sets; no device errors",
            "bound_scope":"Sorted-histogram 95pct guarantee is conditional on n successful independent detections at any single source. Expected launches assume uniform independent loss, not a 95pct-guaranteed launch budget. Pairwise Bhattacharyya result requires specified simple hypotheses and is NOT a composite-label unknown protocol."}

if __name__=="__main__":
    x=study()
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps(x["optimal_depths_by_eta"],indent=2),flush=True)
    print('PERMUTATION_INVARIANT',json.dumps(x["permutation_invariant_95pct_designs"],sort_keys=True),flush=True)
    print("PHOTON_INFORMATION_PASS",flush=True)
