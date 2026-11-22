"""Single-setting Witting POVM dual tomography: 40 vs 25 outcomes.

All three local POVMs are IC (real Hermitian rank 16), but pooling 16
ray labels substantially increases fidelity-estimator variance. A trusted
tomographic entanglement witness is not a Bell nonlocality test.
"""
from __future__ import annotations
import json, math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as prior
OUT=ROOT/"data/toe_20261122_witting_dual_frame_tomography.json"
OLD=[31,7,21,28,22,30,3,15,4,23,26,25,8,1,32,20,19,29,14,38,16,39,11,37]
NEW=[0,1,2,9,6,8,14,11,12,13,15,16,19,21,23,18,27,28,30,32,34,35,37,39]

def run():
    rays,_,_,_=prior.geometry()
    P=np.einsum("ai,aj->aij",rays,rays.conj())
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    B=np.array([np.kron(a,b)/2 for a in (I,X,Y,Z) for b in (I,X,Y,Z)])
    phi=np.eye(4).reshape(16)/2;target=np.outer(phi,phi.conj())
    T=np.array([[np.trace(target@np.kron(a,b.conj())).real for b in B]for a in B])
    data=[]
    for name,sel in [("full40",list(range(40))),("old25",OLD),("new25",NEW)]:
        M=[P[i]/10 for i in sel]
        if len(sel)<40:M.append(sum(P[i]for i in range(40)if i not in sel)/10)
        M=np.asarray(M)
        A=np.einsum("aij,kji->ak",M,B).real
        s=np.linalg.svd(A,compute_uv=False)
        assert s[-1]>1e-10
        pinv=np.linalg.pinv(A)
        C=pinv.T@T@pinv
        p=np.array([[np.vdot(phi,np.kron(a,b.conj())@phi).real for b in M]for a in M])
        err=float(np.max(abs(A.T@C@A-T)))
        value=float((C*p).sum())
        variance=float((C*C*p).sum()-value**2)
        assert err<1e-10 and abs(value-1)<1e-10 and variance>0
        if name=="full40":
            ov=abs(rays.conj()@rays.T)**2
            assert np.max(abs(np.diag(C)-19/4))<1e-11
            for i in range(40):
                for j in range(i+1,40):
                    assert abs(C[i,j]-(-3/2 if ov[i,j]<1e-11 else 7/12))<1e-10
        data.append({"layout":name,"outcomes":len(M),
           "single_ququart_Hermitian_POVM_span_rank":int(np.linalg.matrix_rank(A)),
           "local_frame_condition":float(s[0]/s[-1]),
           "Moore_Penrose_coeff_min":float(C.min()),
           "Moore_Penrose_coeff_max":float(C.max()),
           "fidelity_reconstruction_residual":err,
           "ideal_maximally_entangled_fidelity":value,
           "ideal_Phi_single_shot_estimator_SD":float(math.sqrt(variance))})
    assert all(x["single_ququart_Hermitian_POVM_span_rank"]==16 for x in data)
    assert abs(data[0]["ideal_Phi_single_shot_estimator_SD"]-1.25)<1e-10
    assert abs(data[1]["ideal_Phi_single_shot_estimator_SD"]-7.7082218926255)<1e-9
    assert abs(data[2]["ideal_Phi_single_shot_estimator_SD"]-5.128445190500845)<1e-9
    result={"status":"PASS","date":"2026-11-22",
      "full_40_exact_minimum_norm_three_class_scores":{
         "same_ray":19/4,"orthogonal_rays":-3/2,"distinct_nonorthogonal_rays":7/12},
      "fidelity_estimator":"sum_ij C_ij p_ij, C=pinv(A).T T pinv(A)",
      "layouts":data,
      "limits":"All layouts are IC with calibrated POVMs, but same-label-only witness is invalid after pooling. Moore-Penrose coefficient norm is not globally minimum finite-sample variance; these are ideal target-state variances, not device-independent Bell claims."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS Witting joint-POVM 40/25 IC fidelity dual frames.")
    return result
if __name__=="__main__":run()
