"""Exact 4->40 mode Witting POVM Naimark synthesis with loss and binomial
Schmidt-number witness budgets. A 40x4 isometry needs at most 150 active
two-mode Givens operations (vs 780 for a general 40x40 unitary).
Conditional loss model is NOT a measured chip; count efficiencies assume
state-independent losses, unlike the path-dependent optical model.
"""
from __future__ import annotations
import math,json,sys
from pathlib import Path
import numpy as np
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as native
OUT=ROOT/"data/toe_20261122_witting_40mode_naimark_finite_shots.json"

def compile_isometry(rays):
    V=rays.conj()/math.sqrt(10)
    assert np.max(abs(V.conj().T@V-np.eye(4)))<1e-11
    X=V.copy();gates=[]
    for j in range(4):
        for i in range(39,j,-1):
            a,b=X[i-1,j],X[i,j];s=math.hypot(abs(a),abs(b))
            if s<1e-13:continue
            G=np.array([[a.conjugate()/s,b.conjugate()/s],
                        [-b/s,a/s]])
            X[[i-1,i]]=G@X[[i-1,i]]
            gates.append((i-1,i,G))
    assert np.max(abs(X[4:]))<1e-10
    T=X[:4].copy()
    W=np.vstack((T,np.zeros((36,4),complex)))
    for a,b,G in reversed(gates):W[[a,b]]=G.conj().T@W[[a,b]]
    error=float(np.max(abs(W-V)))
    assert error<1e-10 and len(gates)<=150
    return V,T,gates,error

def propagate(T,gates,loss):
    W=np.vstack((T,np.zeros((36,4),complex)))
    for i,j,G in reversed(gates):
        W[[i,j]]=math.sqrt(1-loss)*G.conj().T@W[[i,j]]
    return W

def sufficient_shots(v,eta=.8,alpha=2.866515718791933e-7,power=.9):
    p0=eta*eta*.04
    p1=eta*eta*(.025+.075*v)
    def meets(N):
        critical=int(binom.isf(alpha,N,p0))+1
        return binom.sf(critical-1,N,p1)>=power,critical
    lo,hi=1,1
    while not meets(hi)[0]:hi*=2
    while lo<hi:
        mid=(lo+hi)//2
        if meets(mid)[0]:hi=mid
        else:lo=mid+1
    _,critical=meets(lo)
    assert binom.sf(critical-1,lo,p0)<=alpha
    assert binom.sf(critical-1,lo,p1)>=power
    return {"visibility":v,"count_meeting_target_size_and_power":lo,
       "critical_same_label_events":critical,
       "null_binomial_size":float(binom.sf(critical-1,lo,p0)),
       "alternative_power":float(binom.sf(critical-1,lo,p1))}

def main():
    rays,_,_,_=native.geometry()
    V,T,gates,error=compile_isometry(rays)
    cases=[]
    for p in (0,.001,.005,.01,.02):
        M=propagate(T,gates,p)
        S=np.linalg.eigvalsh(M.conj().T@M)
        assert S.min()>0 and S.max()<1+1e-10
        cases.append({"per_active_two_mode_element_loss":p,
          "mean_power_survival":float(S.mean()),
          "worst_state_power_survival":float(S.min()),
          "best_state_power_survival":float(S.max())})
    assert len(gates)==150
    assert abs(cases[3]["mean_power_survival"]-.8076565962239846)<1e-9
    budgets=[sufficient_shots(v)for v in (.25,.5,1.)]
    r={"status":"PASS","date":"2026-11-22",
       "Naimark_isometry_shape":[40,4],
       "number_two_mode_Givens_rotations":len(gates),
       "generic_40x4_isometry_upper_bound_rotations":150,
       "generic_40x40_undirected_unitary_Reck_upper_bound":780,
       "max_isometry_reconstruction_residual":error,
       "input_four_mode_U":T.round(10).tolist() if False else "unitary 4x4, reconstructed numerically",
       "loss_model":"Each active Givens acts on two rails with equal intensity loss, idle rails lossless; no source/detector/crossing loss",
       "loss_sweep":cases,
       "binomial_one_sided_5sigma_90percent_power":budgets,
       "binomial_test":"For trusted state-independent eta_A=eta_B=.8, count accepted same labels, null p<=eta^2*.04, true alternative eta^2*(.025+.075v). Use exact binomial upper-tail alpha=2.8665e-7 and power>=.9.",
       "limits":"Specific sample counts meet size and power but discrete critical values make binary search insufficient to prove globally minimal N. Optical loss sweep is state-dependent and NOT included in .8 detector efficiency sample-budget assumption. Not device-independent Bell certification, fabrication layout or measured efficiency."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print("PASS 40-mode Witting isometry, loss-aware optical sweep and binomial witness budget")
    return r
if __name__=="__main__":main()
