"""Trusted Schmidt-number witness corrected for path-dependent 40-mode loss.

For the actual compiled Naimark 4->40 interferometer, derive lossy POVM
effects Mi=|row_i><row_i| and same-label S=sum_i Mi tensor conjugate(Mi).
For every SEPARABLE rho, Tr(rho S)<=lambda_max(S^(T_B)), a rigorous PPT
upper bound, without assuming state-independent efficiency. Simulated
power loss per active two-mode Givens operation is NOT measured hardware.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as base
import toe_20261122_witting_40mode_naimark_finite_shots as optics
OUT=ROOT/"data/toe_20261122_loss_calibrated_witting_schmidt_witness.json"

def count_budget(null,alt,alpha=2.866515718791933e-7,power=.9):
    def test(N):
        critical=int(binom.isf(alpha,N,null))+1
        return binom.sf(critical-1,N,alt)>=power,critical
    lo=1;hi=1
    while not test(hi)[0]:hi*=2
    while lo<hi:
        mid=(lo+hi)//2
        if test(mid)[0]:hi=mid
        else:lo=mid+1
    _,k=test(lo)
    assert binom.sf(k-1,lo,null)<=alpha
    assert binom.sf(k-1,lo,alt)>=power
    return int(lo),int(k)

def main():
    rays,_,_,_=base.geometry()
    V,T,gates,err=optics.compile_isometry(rays)
    assert len(gates)==150 and err<1e-10
    phi=np.eye(4,dtype=complex).reshape(16)/2
    trials=[]
    for loss in (0,.001,.005,.01,.02,.03,.05):
        W=optics.propagate(T,gates,loss)
        P=np.einsum("ai,aj->aij",W.conj(),W)
        S=sum(np.kron(p,p.conj())for p in P)
        Spt=sum(np.kron(p,p)for p in P)
        target=float(np.vdot(phi,S@phi).real)
        PPT_bound=float(np.linalg.eigvalsh(Spt)[-1].real)
        assert target>PPT_bound+1e-4
        n,k=count_budget(PPT_bound,target)
        # If each local effect has unknown Hermitian operator-norm error
        # <=epsilon, then ||S_actual-S_nom|| <= 2*epsilon*sum_i ||Mi|| + N*epsilon**2.
        # Two such worst-case shifts must fit within the nominal gap.
        L=float(np.trace(W.conj().T@W).real)
        gap=target-PPT_bound
        epsilon=(-4*L+math.sqrt((4*L)**2+8*len(P)*gap))/(4*len(P))
        assert epsilon>0
        trials.append({"power_loss_per_active_two_mode_operation":loss,
          "mean_single_photon_survival":float(np.trace(W.conj().T@W).real/4),
          "ideal_phi_same_label_probability":target,
          "rigorous_PPT_separable_bound":PPT_bound,
          "entanglement_witness_gap":target-PPT_bound,
          "sufficient_per_effect_operator_norm_calibration_tolerance":epsilon,
          "illustrative_sufficient_iid_launch_pairs_5sigma_90percent_power":n,
          "same_label_event_critical_count":k})
    r=trials[4]
    assert abs(r["ideal_phi_same_label_probability"]-.0458217956271)<1e-9
    assert abs(r["rigorous_PPT_separable_bound"]-.0256710192242)<1e-9
    assert r["illustrative_sufficient_iid_launch_pairs_5sigma_90percent_power"]==3130
    assert abs(r["sufficient_per_effect_operator_norm_calibration_tolerance"]-.00188236556836)<1e-10
    return_value={"status":"PASS","date":"2026-11-22",
      "proof":"For a separable state rho, partial transpose rho^Gamma is positive trace-one; Tr(rho S)=Tr(rho^Gamma S^Gamma)<=lambda_max(S^Gamma).",
      "measurement":"S=sum_i Mi tensor conjugate(Mi), Mi=|40mode optical row_i><row_i|",
      "Naimark_active_two_mode_rotations":len(gates),
      "optical_loss_sweep":trials,
      "limits":"Correct for the precisely modeled and KNOWN lossy optical POVM. Binomial count assumes iid and exact effects, no backgrounds, no source contamination; measured calibration errors can invalidate this bound. Not device-independent entanglement certification or a real apparatus."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(return_value,indent=2)+"\n")
    print("PASS calibrated lossy Witting entanglement witness with rigorous PPT separable bounds")
    return return_value
if __name__=="__main__":main()
