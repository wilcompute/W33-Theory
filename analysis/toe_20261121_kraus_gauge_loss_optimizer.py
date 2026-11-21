"""Kraus-unitary gauge search for lower-loss ten-mode Witting recovery.

For five Kraus operators R_j, R'_j=sum_l G[j,l]R_l (G unitary U5)
describes EXACTLY the same CPTP map. The corresponding 10x9 Stinespring
matrix and its 10x10 unitary extension do NOT generally yield the same
loss pattern after Reck compilation. We benchmark physical mesh choices.

All outputs use an assumed per-active-two-mode-element power-loss model;
these are not fabricated optical chips or a global mesh optimum.
"""
from __future__ import annotations
import sys,json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
sys.path.insert(0,str(Path(__file__).resolve().parent))
import toe_20261121_fivefront_rank5_optical_noise as decoder
import toe_20261121_rank5_loss_mesh_break_even as optical
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261121_kraus_gauge_loss_optimizer.json"
SEED=20261121

def full_unitary(Kraus):
    W=Kraus.reshape(10,9)
    U=np.column_stack((W,null_space(W.conj().T)))
    assert np.max(abs(U.conj().T@U-np.eye(10)))<1e-10
    return U

def random_haar_U5(rng):
    Z=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5))
    Q,R=np.linalg.qr(Z)
    diagonal=np.diag(R)
    return Q*(diagonal/abs(diagonal))[None,:]

def gauge_mix(Kraus,G):
    """A unitary change of Kraus basis preserves the CP map exactly."""
    mixed=np.einsum("jk,kab->jab",G,Kraus)
    oldTP=sum(K.conj().T@K for K in Kraus)
    newTP=sum(K.conj().T@K for K in mixed)
    assert np.max(abs(oldTP-newTP))<1e-10
    assert np.max(abs(G.conj().T@G-np.eye(5)))<1e-10
    # Stronger check: the full CP map is invariant, not just TP.
    rho=np.diag(np.arange(1,10,dtype=float)/45).astype(complex)
    rho[0,1]=.01+.01j
    rho[1,0]=rho[0,1].conjugate()
    oldOut=sum(K@rho@K.conj().T for K in Kraus)
    newOut=sum(K@rho@K.conj().T for K in mixed)
    assert np.max(abs(oldOut-newOut))<1e-10
    return mixed

def evaluate(Kraus,T,loss,N,rng):
    baseline=optical.simulated_recovery(full_unitary(Kraus),T,loss)
    top=baseline["unconditional_fidelity"]
    best=None
    vals=[]
    for j in range(N):
        G=random_haar_U5(rng)
        W=full_unitary(gauge_mix(Kraus,G))
        test=optical.simulated_recovery(W,T,loss)
        if j==0:
            ideal=optical.simulated_recovery(W,T,0)["unconditional_fidelity"]
            original=optical.simulated_recovery(full_unitary(Kraus),T,0)["unconditional_fidelity"]
            assert abs(ideal-original)<1e-10
        vals.append(test["unconditional_fidelity"])
        if test["unconditional_fidelity"]>top:
            top=test["unconditional_fidelity"]
            best=(G,test)
    return {
      "seeded_random_unitary_trials":N,
      "baseline_unconditional_fidelity":baseline["unconditional_fidelity"],
      "baseline_survival":baseline["survival_average"],
      "mean_random_gauge_fidelity":float(np.mean(vals)),
      "best_unconditional_fidelity":top,
      "best_random_unitary_matrix_real":best[0].real.tolist()if best else None,
      "best_random_unitary_matrix_imag":best[0].imag.tolist()if best else None,
      "best_survival":best[1]["survival_average"]if best else baseline["survival_average"],
      "best_mesh_gate_count":best[1]["mesh_gate_count"]if best else baseline["mesh_gate_count"]
    }

def main():
    rays,_,_,_=decoder.prior.geometry()
    d,Ropt,Rpetz,T,_,_=decoder.optimize_decoder(rays)
    rng=np.random.default_rng(SEED)
    loss=.02
    p=evaluate(Rpetz,T,loss,200,rng)
    s=evaluate(Ropt,T,loss,200,rng)
    assert p["best_unconditional_fidelity"]>p["baseline_unconditional_fidelity"]
    assert s["best_unconditional_fidelity"]>s["baseline_unconditional_fidelity"]
    assert s["best_unconditional_fidelity"]>p["best_unconditional_fidelity"]
    assert s["best_unconditional_fidelity"]>.785
    result={"status":"PASS","date":"2026-11-21",
       "assumed_per_active_gate_power_loss":loss,
       "Kraus_unitary_freedom":"R'_j=sum_k G[j,k]R_k, G unitary U5; lossless quantum channel unchanged",
       "Petz":p,"SDP_rank5":s,
       "scope":"200 seeded Haar-U5 samples each, no global physical-layout optimality; model uses identical two-rail intensity loss after each active Reck rotation and ignores extra waveguide/detector/source losses"}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS: same quantum map; different lossy optical mesh.",p["best_unconditional_fidelity"],s["best_unconditional_fidelity"])
    return result
if __name__=="__main__":main()
