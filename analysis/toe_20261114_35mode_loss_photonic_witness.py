#!/usr/bin/env python3
"""Practical central-Z2 8+27 mode interferometer: independent
branch-dependent loss, relative Gaussian phase jitter, detector loss,
dark clicks, optimal discrimination upper bound, and explicit
one-photon erasure Knill–Laflamme NO-GO.

Pulse count 3: hypotheses H1(g8^3=-I8,U27^3=I) vs H0(+I,+I).
Outputs are UNCONDITIONAL per input photon, and conditional on
survival separately; no hidden postselection.
"""
from pathlib import Path
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261114_35mode_central_phase_photonic_noise_and_erasure_nogo.json"

def signal(n,eta8,eta27,sigma,sign):
    a=eta8**n;b=eta27**n
    # balanced preparation, relative phase random Gaussian
    p=(a+b+2*sign*math.sqrt(a*b)*math.exp(-sigma*sigma/2))/4
    survival=(a+b)/2
    assert -1e-12<=p<=survival+1e-12
    return {"p_unconditioned_return":p,"p_survive":survival,
            "p_return_conditioned_survival":p/survival,
            "branch_intensity_8":a,"branch_intensity_27":b}
def observed(p,detector,dark):
    # independent threshold click from dark count or detected
    # return photon, not photon-number resolving
    return 1-(1-dark)*(1-detector*p)
def shots_bound(p1,p0,error=1e-6):
    # For equal priors, quantum-independent Bernoulli observations;
    # classical Bhattacharyya bound P_e <= (1/2) BC^N.
    B=math.sqrt(p1*p0)+math.sqrt((1-p1)*(1-p0))
    assert 0<B<1
    n=math.ceil(math.log(2*error)/math.log(B))
    assert .5*B**n<=error
    return {"Bhattacharyya_coefficient":B,
            "shots_for_Bhattacharyya_upper_bound_error":n,
            "target_Bayes_error_upper_bound":error}
def erasure_KL():
    # Logical |000>,|111>,|222> in one photon 27-path space.
    W=np.zeros((27,3),dtype=np.int64)
    sites=[0,13,26]
    for i,j in enumerate(sites):W[j,i]=1
    assert np.array_equal(W.T@W,np.eye(3,dtype=np.int64))
    # Loss Kraus E_j=sqrt(1-eta)|vac><j|.
    # P E_i†E_j P=(1-eta)|i_L><j_L| for j among code sites.
    # This is not proportional to I3 even for i=j.
    Gram=[[W.T[:,a:a+1]@W[b:b+1,:] for b in sites] for a in sites]
    # Directly test diagonal logical loss channel E_site^dag E_site
    loss_projector=W.T@np.diag([int(j==sites[0]) for j in range(27)])@W
    assert np.array_equal(loss_projector,np.diag([1,0,0]))
    assert not np.array_equal(loss_projector,np.eye(3))
    # Uniform complete loss erases any logical state to same vacuum:
    # E_j†E_k span full matrix algebra on one-photon subspace.
    return {"single_photon_modes":27,"logical_dim":3,
            "example_projected_loss_Kraus_product":loss_projector.tolist(),
            "full_photon_loss_exactly_correctable":False,
            "general_single_photon_loss_no_go":"For complete mode-resolved loss Kraus set {sqrt(1-eta)|vac><j|}, their pair products span the full End(C^27), so no code dim>=2 in the one-photon sector satisfies Knill-Laflamme for arbitrary photon loss. Classical heralding does not restore erased logical amplitudes."}

def main():
    # Purely illustrative component numbers, NOT experimental measurements.
    eta8=.98;eta27=.95;detector=.82;dark=1e-5;sigma=.10
    hypotheses={}
    for n,sgn in [(3,-1),(6,+1)]:
        alt=signal(n,eta8,eta27,sigma,+1)
        pred=signal(n,eta8,eta27,sigma,sgn)
        clicks_pred=observed(pred["p_unconditioned_return"],detector,dark)
        clicks_alt=observed(alt["p_unconditioned_return"],detector,dark)
        hypotheses[str(n)]={"clock_central_prediction":pred,
                            "null_no_relative_pi":alt,
                            "return_detector_click_probability_pred":clicks_pred,
                            "return_detector_click_probability_null":clicks_alt}
    error=shots_bound(hypotheses["3"]["return_detector_click_probability_pred"],
                      hypotheses["3"]["return_detector_click_probability_null"])
    # A zero-loss control: 3-pulse dark, 6-pulse bright.
    assert abs(signal(3,1,1,0,-1)["p_unconditioned_return"])<1e-12
    assert abs(signal(6,1,1,0,+1)["p_unconditioned_return"]-1)<1e-12
    assert 0<hypotheses["3"]["return_detector_click_probability_pred"]<hypotheses["3"]["return_detector_click_probability_null"]<1
    erasure=erasure_KL()
    r={
      "status":"PASS_LOSS_AND_NOISE_CALIBRATED_CENTRAL_Z2_AND_PHOTON_LOSS_KL_NOGO",
      "mode_count":35,"branches":[8,27],
      "assumed_component_parameters_NOT_measured":{
         "per_pulse_8_branch_transmission":eta8,
         "per_pulse_27_branch_transmission":eta27,
         "relative_phase_jitter_std_radians":sigma,
         "detector_efficiency":detector,
         "per_shot_dark_click_probability":dark},
      "photonic_trials":hypotheses,
      "three_pulse_classical_two_hypothesis_Bhattacharyya_bound":error,
      "full_loss_no_go":erasure,
      "control_no_loss_three_pulse_return":0,
      "control_no_loss_six_pulse_return":1,
      "limitations":"Ideal equal coherent preparation; independent intensity loss per application; no mode-dependent crosstalk, leakage or temporal drift. The shot bound assumes known calibrated hypotheses and iid trials. An arbitrary imposed path phase pi produces the same interference: an observed dip is not uniquely evidence of USp8 or fundamental spacetime dynamics. Unrecoverable full photon loss of one carrier requires physical redundancy/ancilla photons, beyond virtual qutrit encoding."
    }
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":r["status"],"3pulse":hypotheses["3"],"shots_bound":error,
                      "erasure_correctable":erasure["full_photon_loss_exactly_correctable"]},indent=2),flush=True)
    return r
if __name__=="__main__":main()
