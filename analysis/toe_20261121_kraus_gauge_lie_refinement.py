"""Optimize loss-aware 10-mode Witting decoder by unitary Kraus-gauge refinement.

Starts from the *previous committed deterministic* 200-Haar U(5) search
and performs 400 seeded local Lie-algebra perturbations per decoder.
No ideal CPTP decoder changes, no physical chip claimed.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
import toe_20261121_fivefront_rank5_optical_noise as native
import toe_20261121_rank5_loss_mesh_break_even as optics
import toe_20261121_kraus_gauge_loss_optimizer as prior

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261121_kraus_gauge_lie_refinement.json"
LOSS=.02
SEED=20261121

def simulate_gauged(Kraus,T,G):
    R=prior.gauge_mix(Kraus,G)
    U=prior.full_unitary(R)
    return optics.simulated_recovery(U,T,LOSS)

def refine(Kraus,T,initial,rng,niter=400):
    Gr=np.asarray(initial["best_random_unitary_matrix_real"],dtype=float)
    Gi=np.asarray(initial["best_random_unitary_matrix_imag"],dtype=float)
    G=Gr+1j*Gi
    assert np.max(abs(G.conj().T@G-np.eye(5)))<1e-10
    before=simulate_gauged(Kraus,T,G)
    best=before["unconditional_fidelity"]
    accepted=0
    for k in range(niter):
        step=.14 if k<100 else .065 if k<250 else .025
        Z=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5))
        H=(Z+Z.conj().T)/2
        H/=np.linalg.norm(H,ord="fro")
        Gtry=expm(1j*step*H)@G
        test=simulate_gauged(Kraus,T,Gtry)
        if test["unconditional_fidelity"]>best+1e-12:
            best=test["unconditional_fidelity"]
            G=Gtry
            accepted+=1
    after=simulate_gauged(Kraus,T,G)
    assert abs(after["unconditional_fidelity"]-best)<1e-10
    assert best>before["unconditional_fidelity"]
    assert np.max(abs(G.conj().T@G-np.eye(5)))<1e-10
    return {
       "previous_200_Haar_best":before["unconditional_fidelity"],
       "refined_lossy_entanglement_fidelity":best,
       "refined_average_survival":after["survival_average"],
       "accepted_improvements":accepted,
       "local_perturbations":niter,
       "best_G_real":G.real.tolist(),
       "best_G_imag":G.imag.tolist(),
       "optical_mesh_elements":after["mesh_gate_count"]
    }

def main():
    rays,_,_,_=native.prior.geometry()
    d,Ropt,Rpetz,T,_,_=native.optimize_decoder(rays)
    rng=np.random.default_rng(SEED)
    baseline=prior.main()
    p=refine(Rpetz,T,baseline["Petz"],rng)
    s=refine(Ropt,T,baseline["SDP_rank5"],rng)
    assert p["refined_lossy_entanglement_fidelity"]>.789
    assert s["refined_lossy_entanglement_fidelity"]>.802
    assert s["refined_lossy_entanglement_fidelity"]>p["refined_lossy_entanglement_fidelity"]
    obj={"status":"PASS","date":"2026-11-21","loss_per_active_two_mode_gate":LOSS,
         "Petz":p,"SDP_rank5":s,
         "math":"Same five-Kraus CPTP recovery before and after U(5) mixing; loss changes the physical mesh.",
         "limitation":"Not a globally optimal U5, unitary-completion, mesh or manufacturable device. No unmodeled loss or crosstalk."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
    print("PASS local Kraus-gauge Lie refinement",p["refined_lossy_entanglement_fidelity"],
          s["refined_lossy_entanglement_fidelity"])
    return obj

if __name__=="__main__":main()
