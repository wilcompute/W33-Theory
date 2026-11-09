#!/usr/bin/env python3
"""Quantitative 9-mode optical attenuation after exact adjacent Givens synthesis.

The toy photonic model applies a known intensity transmission t per occupied
Givens coupler rail. Unlike output detector efficiencies, internal loss occurs
between noncommuting mode-mixing gates and is state-dependent.
"""
import json,sys
from pathlib import Path
import numpy as np
from w33_20261109_q8_ten_context_optimize import main as optimal
from w33_20261109_q8_ten_context_tomography import projection_design
from w33_20261109_q8_horodecki_ccnr_exact import realign
from w33_20261109_q8_five_extensions import horodecki_state

def givens_network(U,transmission=1.,phase_drift=0.,rng=None):
    # Q R = D, so U^dagger = D^dagger Q. Losses are inserted between
    # physical Givens gates, not lumped into per-outcome efficiencies.
    R=U.copy(); gates=[]; rails=np.zeros(9,dtype=int)
    for col in range(8):
        for row in range(8,col,-1):
            a,b=R[row-1,col],R[row,col]
            n=np.hypot(abs(a),abs(b))
            assert n>1e-13
            g=np.eye(9,dtype=complex)
            g[row-1,row-1]=a.conjugate()/n
            g[row-1,row]=b.conjugate()/n
            g[row,row-1]=-b/n
            g[row,row]=a/n
            R=g@R
            gates.append((g,row-1,row))
            rails[row-1]+=1;rails[row]+=1
    assert len(gates)==36
    out=np.eye(9,dtype=complex)
    if rng is None:rng=np.random.default_rng(20261109)
    for G,i,j in gates:
        Gp=G.copy()
        if phase_drift:
            # Programmed output-arm phase error at each mixing element.
            d=np.eye(9,dtype=complex)
            d[i,i]=np.exp(1j*rng.normal(0,phase_drift))
            d[j,j]=np.exp(1j*rng.normal(0,phase_drift))
            Gp=d@Gp
        D=np.eye(9,dtype=complex)
        D[i,i]=np.sqrt(transmission)
        D[j,j]=np.sqrt(transmission)
        out=D@Gp@out
    out=np.diag(np.diag(R).conjugate())@out
    if transmission==1 and phase_drift==0:
        assert np.max(abs(out-U.conj().T))<3e-12
    return out,rails

def measured_distribution(Ueff,rho):
    # POVM effects E_j=Ueff^dag |j><j| Ueff, conditional on click.
    amps=Ueff@rho@Ueff.conj().T
    q=np.real(np.diag(amps))
    surv=float(sum(q))
    assert min(q)>-1e-11 and surv>0
    return q/surv,surv

def main(path=None):
    meta,(Bell,U,V,ops)=optimal(return_components=True)
    pinv=np.linalg.pinv(np.vstack([
        projection_design(Bell,ops),
        projection_design(U,ops),
        projection_design(V,ops)]),rcond=1e-13)
    rng=np.random.default_rng(20261109195)
    sources={"I9_over_9":np.eye(9)/9,
             "Horodecki_a0p236":horodecki_state(.236)}
    for j in range(12):
        x=rng.normal(size=3)+1j*rng.normal(size=3)
        y=rng.normal(size=3)+1j*rng.normal(size=3)
        x/=np.linalg.norm(x);y/=np.linalg.norm(y)
        v=np.kron(x,y)
        sources[f"separable_product_{j}"]=np.outer(v,v.conj())
    results=[]
    for t,phase in ((1.,0.),(.999,0.),(.995,0.),(.99,0.),(.995,.003),(.99,.01)):
        rnoise=np.random.default_rng(2026110920)
        G1,c1=givens_network(U,t,phase,rnoise)
        G2,c2=givens_network(V,t,phase,rnoise)
        assert np.array_equal(c1,c2)
        assert max(c1)==15
        rv=[]
        for key,rho in sources.items():
            qbell=np.real(np.diag(Bell.conj().T@rho@Bell))
            qU,sU=measured_distribution(U.conj().T if t==1 and phase==0 else G1,rho)
            qV,sV=measured_distribution(V.conj().T if t==1 and phase==0 else G2,rho)
            measured=np.r_[qbell,qU,qV]
            theta=pinv@(measured-1/9)
            rec=np.eye(9)/9+np.einsum("k,kij->ij",theta,ops)
            ccnr=float(np.linalg.svd(realign(rec),compute_uv=False).sum())
            true=float(np.linalg.svd(realign(rho),compute_uv=False).sum())
            eig=float(min(np.linalg.eigvalsh((rec+rec.conj().T)/2)))
            rv.append({"source":key,"true_CCNR":true,
                       "naive_reconstructed_CCNR":ccnr,
                       "calibration_free_false_positive":bool(key.startswith("separable") and ccnr>1+1e-8),
                       "naive_recon_min_eigenvalue":eig,
                       "accepted_rate_generic_1":sU,
                       "accepted_rate_generic_2":sV})
        results.append({"per_gate_intensity_transmission":t,
            "per_gate_rms_phase_error_rad":phase,
            "separable_false_positive_count":sum(x["calibration_free_false_positive"] for x in rv),
            "total_separable_controls":12,
            "generic_output_rail_gate_exposures":c1.tolist(),
            "lowest_approx_intensity_if_fixed_rail_path":float(t**max(c1)),
            "results":rv})
    assert results[0]["separable_false_positive_count"]==0
    out={"status":"PASS_9MODE_Q8_LOSS_NONCOMMUTING_COUPLERS_HARDWARE_TOY",
         "generic_programmed_two_mode_elements_each":36,
         "max_rail_coupler_exposure":15,
         "min_rail_coupler_exposure":1,
         "input_programs":2,"loss_noise_controls":results,
         "assumptions":"Each coupled rail experiences sqrt(t) field transmission after each of 36 programmed Givens; phase errors independently perturb output rails. First eight Bell contexts ideal to isolate generic analyzer effects. State preparation IID, no Poisson noise; detector postselection is normalized.",
         "scope":"Not a fabricated photonic circuit, calibration, source certification, or proof of a physical platform budget. Results only apply to this explicit toy network.",
         "warning":"A noncommuting internal loss cannot generically be repaired by per-output detector-efficiency correction; calibrate full POVMs."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS optical loss",[(r["per_gate_intensity_transmission"],
                               r["per_gate_rms_phase_error_rad"],
                               r["separable_false_positive_count"])
                              for r in results])
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
