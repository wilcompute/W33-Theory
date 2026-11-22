"""Capacity bounds for a precisely defined proxy interpolation:
    L_lam(rho) = (1-lam)*rho+lam*(rho+I4)/5.

The Witting 40-ray measure/reprepare operation is exactly the EB endpoint.
The universal symmetric 1->2 cloning broadcast extension at lam=.5
proves antidegradability and hence zero quantum capacity for lam>=.5.
This is NOT the distinct earlier coherent 4->9 Witting channel.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261122_witting_coherence_cloning_capacity.json"

def coherent_info(lam):
    a=1-.8*lam
    p=[a+(1-a)/16]+[(1-a)/16]*15
    return 2+sum(v*math.log2(v)for v in p if v>1e-15)

def main():
    # Explicit symmetric universal cloning broadcast channel:
    # C(rho)=2/(d+1) Pi_sym (rho tensor I_d) Pi_sym,
    # both marginals alpha=(d+2)/(2(d+1))=3/5.
    d=4;S=np.zeros((16,16))
    for i in range(d):
        for j in range(d):S[4*i+j,4*j+i]=1
    Psym=(np.eye(16)+S)/2
    rng=np.random.default_rng(20261122)
    errs=[]
    for _ in range(8):
        Z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        rho=Z@Z.conj().T;rho/=np.trace(rho)
        twin=2/5*Psym@np.kron(rho,np.eye(4))@Psym
        a=np.einsum("iaja->ij",twin.reshape(4,4,4,4))
        b=np.einsum("aiaj->ij",twin.reshape(4,4,4,4))
        ideal=.6*rho+.4*np.eye(4)/4
        errs.extend([float(np.max(abs(a-ideal))),float(np.max(abs(b-ideal)))])
        assert abs(np.trace(twin)-1)<1e-12
    assert max(errs)<1e-11
    t=brentq(coherent_info,.01,.95)
    samples=[]
    for lam in (0,.1,.25,t,.5,.6,.75,.9,1):
        a=1-.8*lam
        N=max(0,6*(5*a-1)/16)
        f=a+(1-a)/16
        samples.append({"lam":float(lam),"alpha":float(a),
           "Choi_singlet_fraction":float(f),
           "Choi_negativity":float(N),
           "maximally_mixed_oneuse_coherent_information":float(coherent_info(lam)),
           "certified_Q_lower_bound_bits":float(max(0,coherent_info(lam))),
           "zero_capacity_by_antidegradability":bool(lam>=.5-1e-12),
           "entanglement_breaking":bool(lam>=1-1e-12)})
    assert all(s["Choi_negativity"]>0 for s in samples[:-1])
    assert all(s["zero_capacity_by_antidegradability"]for s in samples[4:])
    r={"status":"PASS","date":"2026-11-22",
       "channel":"Lambda_lambda=(1-lambda)*Identity+lambda*Witting_Measure_Reprepare",
       "exact_measure_reprepare":"E(rho)=(rho+I4)/5",
       "depolarizing_alpha":"1-4*lambda/5",
       "cloning_broadcast_map":"C(rho)=2/5 Pi_sym (rho tensor I4) Pi_sym",
       "clone_marginals":"Tr_1 C=Tr_2 C=.6 rho+.4 I4/4",
       "max_cloning_marginal_residual":max(errs),
       "coherent_information_witness_zero_lambda":float(t),
       "zero_quantum_capacity_proven_for_lambda_ge":.5,
       "entanglement_breaking_only_at_lambda":1.,
       "scan":samples,
       "limits":"For .3862<lambda<.5 these tests do not decide Q. Non-entanglement-breaking states persist for .5<=lambda<1 despite Q=0. Proxy channel is NOT original Witting 4-to-9 channel; no physical device."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print("PASS universal cloning antidegradable window, capacity vs entanglement boundaries")
    return r
if __name__=="__main__":main()
