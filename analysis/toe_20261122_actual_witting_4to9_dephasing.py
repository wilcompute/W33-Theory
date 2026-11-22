"""Actual 4->9 routed Witting coherent channel under output-rail dephasing.

This supplements the identity-to-entanglement-breaking DEP0LARIZING PROXY.
For the actual 5-Kraus routed 4->9 channel, computes coherent information
on maximally mixed ququart input after partial dephasing of 9 retained rails.
Positive coherent information proves a quantum-capacity lower bound.
Negative coherent information on this input is NOT a zero-capacity proof.
At full dephasing the output is classical-quantum and Q=0.
"""
from __future__ import annotations
import math,json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as source
OUT=ROOT/"data/toe_20261122_actual_witting_4to9_dephasing.json"
ROUTING=[0,22,14,19,6,7,2,11,33,38,35,40,23,31,10,32,8,43,29,36,27,44,
         9,15,21,16,12,25,3,37,13,41,20,5,34,26,30,17,42,24,18,39,28,1,4]

def entropy(mat):
    e=np.linalg.eigvalsh((mat+mat.conj().T)/2)
    assert e.min()>-1e-10
    return float(-sum(x*math.log2(x)for x in e if x>1e-12))

def main():
    rays,_,_,_=source.geometry()
    B=np.zeros((45,4),complex);B[:40]=rays.conj()/math.sqrt(10)
    assert np.max(abs(B.conj().T@B-np.eye(4)))<1e-11
    K=B[ROUTING].reshape(9,5,4).transpose(1,0,2)
    assert K.shape==(5,9,4)
    assert np.max(abs(sum(k.conj().T@k for k in K)-np.eye(4)))<1e-11
    J=sum(np.outer(k.reshape(36),k.reshape(36).conj())for k in K)/4
    assert abs(np.trace(J)-1)<1e-11
    out=sum(k@k.conj().T for k in K)/4
    def choi(lam):
        blocks=J.reshape(9,4,9,4).copy()
        for i in range(9):
            for j in range(9):
                if i!=j:blocks[i,:,j,:]*=(1-lam)
        return blocks.reshape(36,36)
    def values(lam):
        state=choi(lam)
        reduced=(1-lam)*out+lam*np.diag(out.diagonal())
        Ic=entropy(reduced)-entropy(state)
        pt=state.reshape(9,4,9,4).transpose(0,3,2,1).reshape(36,36)
        minpt=float(np.linalg.eigvalsh((pt+pt.conj().T)/2).min())
        return Ic,minpt
    initial=values(0)[0]
    assert initial>1
    assert values(1)[0]<0
    critical=brentq(lambda lam:values(lam)[0],0,.999999999)
    assert .22<critical<.24
    scan=[{"output_rail_dephasing_fraction":p,
           "maximally_mixed_input_coherent_information_bits":values(p)[0],
           "min_partial_transpose_Choi_eigenvalue":values(p)[1]}
          for p in (0,.1,.2,.25,.5,.75,.9,.99,1)]
    assert scan[0]["min_partial_transpose_Choi_eigenvalue"]<-.1
    assert abs(scan[-1]["min_partial_transpose_Choi_eigenvalue"])<1e-10
    result={"status":"PASS","date":"2026-11-22",
      "channel":"Native existing Witting 40-ray -> five Kraus operators of shape 9x4",
      "Kraus_shape":[5,9,4],
      "noise":"N_lambda=(1-lambda)N+lambda Delta_output circ N, complete rail-basis dephasing Delta_output",
      "positive_maximally_mixed_input_coherent_information_at_zero":initial,
      "positive_coherent_information_ends_for_maxmixed_at_lambda":float(critical),
      "scans":scan,
      "quantum_capacity_lower_bound_for_lambda_below_crossing":"Q(N_lambda)>=Ic(I4/4,N_lambda)>0",
      "fully_dephased_lambda1_is_entanglement_breaking":True,
      "essential_scope":"Specific maximally mixed input. For larger lambda, this negative coherent information does NOT prove capacity zero. At lambda=1 fully output-dephased channel is entanglement breaking. Distinct from identity-to-reprepare proxy, and no physical channel measured."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS actual Witting 4->9 dephasing coherent-information witness",critical)
    return result
if __name__=="__main__":main()
