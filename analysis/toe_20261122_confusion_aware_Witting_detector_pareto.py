"""Recompute unbiased two-ququart fidelity-score variance under WRONG-RAY
labels, for full40 and three different compressed25 Witting detectors.

Model: independently on Alice/Bob, each measured ray label is replaced
uniformly among all 40 labels with known probability epsilon, THEN pooled.
The confusion matrix is known and invertible if epsilon<1. Asymmetric
unknown crosstalk, temporal drift and loss are NOT handled in this model.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as base
OUT=ROOT/"data/toe_20261122_confusion_aware_Witting_detector_pareto.json"
OLD=base.OLD
NEW=base.BALANCED
CAND=[0,1,24,14,6,8,32,13,12,5,22,16,38,21,23,18,11,28,26,30,27,35,37,39]

def matrix(labels):
    if len(labels)==40:return np.eye(40)
    assert len(labels)==24 and len(set(labels))==24
    C=np.zeros((25,40))
    C[np.arange(24),labels]=1
    C[-1,[i for i in range(40) if i not in labels]]=1
    return C

def main():
    rays,_,_,_=base.geometry()
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    B=np.array([np.kron(a,b)/2 for a in (I,X,Y,Z)for b in (I,X,Y,Z)])
    raysP=np.einsum("ai,aj->aij",rays,rays.conj())
    AA=np.einsum("aij,kji->ak",raysP,B).real/10
    phi=np.eye(4).reshape(16)/2
    TT=np.array([[np.vdot(phi,np.kron(a,b.conj())@phi).real for b in B]for a in B])
    p40=abs(rays.conj()@rays.T)**2/400
    data=[]
    for eps in (0,.05,.15,.3):
        M=(1-eps)*np.eye(40)+eps/40*np.ones((40,40))
        layouts=[]
        for name,labels in (("full40",list(range(40))),("older25",OLD),
                            ("privacyFisher25",NEW),("newVariance25",CAND)):
            C=matrix(labels)
            A=C@M@AA
            assert np.linalg.matrix_rank(A)==16
            coeff=np.linalg.pinv(A).T@TT@np.linalg.pinv(A)
            joint=C@M@p40@M.T@C.T
            mean=float((coeff*joint).sum())
            sd=float(np.sqrt((coeff*coeff*joint).sum()-mean*mean))
            assert abs(mean-1)<1e-10
            layouts.append({"layout":name,"outcomes":len(C),
                            "unbiased_fidelity_score_mean":mean,
                            "single_shot_fidelity_estimator_sd":sd,
                            "local_POVM_analysis_condition":float(np.linalg.cond(A))})
        assert layouts[3]["single_shot_fidelity_estimator_sd"]<layouts[2]["single_shot_fidelity_estimator_sd"]
        data.append({"known_wrong_label_probability":eps,"layouts":layouts})
    assert abs(data[2]["layouts"][3]["single_shot_fidelity_estimator_sd"]-6.05632334)<1e-7
    result={"status":"PASS","date":"2026-11-22",
       "noise":"Each true 40-ray detector label independently replaced with probability epsilon by a fresh uniform 40-label draw, then pooled; same known confusion matrix at both parties",
       "full_ququart_tomography_rank":16,"noise_sweep":data,
       "interpretation":"The new 25-bin compromise retains smaller ideal-Phi fidelity-score SD than old/privacyFisher designs under known symmetric label crosstalk, but NOT universally robust to unknown drift.",
       "boundaries":"Known calibrated confusion only, not asymmetric adversarial drift, optical loss, detector efficiency, nor a globally optimal estimator. No real chip, no device-independent entanglement certification."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS calibrated wrong-ray confusion Witting dual-frame variance comparison")
    return result
if __name__=="__main__":main()
