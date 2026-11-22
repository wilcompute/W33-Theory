"""Exact reproducible *positive* coherent-information witness for real Witting 4->9.
A fixed rank-two ququart input beats the maximally mixed input at 30%
output-rail dephasing. This proves Q>0 for the explicitly defined channel
at that point, not a global optimization or universal threshold.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as base
OUT=ROOT/"data/toe_20261122_native_capacity_input_witness.json"
ROUTING=base.ROUTING
WR=np.array([[.328407966,-.396479532],
             [.160084530,.463275533],
             [.094680683,-.191247123],
             [.093349990,.372494445]])
WI=np.array([[0,0],[.063465203,.290956160],
             [.334154329,.166761570],[.220494940,-.157875940]])

def entropy(a):
    e=np.linalg.eigvalsh((a+a.conj().T)/2)
    assert e.min()>-1e-10
    return float(-sum(x*math.log2(x) for x in e if x>1e-14))

def make_kraus():
    rays,_,_,_=base.geometry()
    V=np.zeros((45,4),complex);V[:40]=rays.conj()/math.sqrt(10)
    K=V[ROUTING].reshape(9,5,4).transpose(1,0,2)
    assert K.shape==(5,9,4)
    assert np.max(abs(sum(k.conj().T@k for k in K)-np.eye(4)))<1e-10
    return K

def coherent_information(K,rho,lam):
    w,U=np.linalg.eigh(rho)
    assert w.min()>-1e-9
    sq=(U*np.sqrt(np.maximum(0,w)))@U.conj().T
    joint=sum(np.outer((k@sq).reshape(36),(k@sq).reshape(36).conj())for k in K)
    joint=joint.reshape(9,4,9,4)
    joint=(1-lam)*joint+lam*joint*np.eye(9)[:,None,:,None]
    output=np.trace(joint,axis1=1,axis2=3)
    return entropy(output)-entropy(joint.reshape(36,36))

def main():
    K=make_kraus()
    W=WR+1j*WI
    rho=W@W.conj().T
    rho/=np.trace(rho)
    eig=np.linalg.eigvalsh(rho)
    assert eig.min()>-1e-10 and eig[2]>.3
    mixed=np.eye(4)/4
    rows=[]
    for lam in (.20,.23,.25,.27,.30,.305,.31,.4,1.):
        rows.append({"dephasing":lam,
          "rank2_witness_coherent_information_bits":coherent_information(K,rho,lam),
          "maximally_mixed_coherent_information_bits":coherent_information(K,mixed,lam)})
    x=next(row for row in rows if row["dephasing"]==.30)
    assert x["rank2_witness_coherent_information_bits"]>.0078
    assert x["maximally_mixed_coherent_information_bits"]<-.23
    r={"status":"PASS","date":"2026-11-22",
      "native_kraus_shape":[5,9,4],
      "input_rank":2,"fixed_rank2_factor_real":WR.tolist(),
      "fixed_rank2_factor_imag":WI.tolist(),
      "input_density_spectrum":eig.tolist(),
      "noise":"(1-lambda)*N+lambda*fully-rail-dephased(N), output 9 rails",
      "measured_positive_oneuse_witness_at_lambda_0p3":x["rank2_witness_coherent_information_bits"],
      "maxmixed_negative_same_noise":x["maximally_mixed_coherent_information_bits"],
      "scan":rows,
      "interpretation":"Constructive fixed physical input: quantum capacity >0 at 30% output-rail dephasing. NOT an optimal capacity or exact threshold.",
      "limit":"Numerical input discovered by search; validated with fixed matrix and channel. No hardware operation or demonstrated fault tolerance."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2)+"\n")
    print("PASS real 4to9 Witting coherent information positive at 30 percent rail dephasing")
    return r
if __name__=="__main__":main()
