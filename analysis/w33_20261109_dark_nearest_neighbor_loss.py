#!/usr/bin/env python3
"""40-port W33 dark state: nearest-neighbor optical light-cone bound.

Starting photon at end port 0 on a line of 40 rails; 2-rail adjacent
beam splitters cannot populate port 39 in <39 sequential layers. Exact
39-layer state-prep saturates bound, trading depth for connectivity.
Include actual per-coupler loss at each of 39 stages, not scalar scaling.
"""
import sys,json,math
from pathlib import Path
import numpy as np
from w33_20261109_flux_dark_mode_fragility import build

def construction(target,eta=1.,order=None):
    n=len(target)
    if order is None:order=list(range(n))
    p=np.abs(target[order])**2
    state=np.zeros(n,dtype=complex);state[0]=1.
    gates=[]
    for i in range(n-1):
        residual=math.sqrt(float(sum(p[i:])))
        if residual<1e-14:raise ValueError("zero residual")
        c=math.sqrt(float(p[i]))/residual
        s=math.sqrt(float(sum(p[i+1:])))/residual
        x,y=state[i],state[i+1]
        state[i]=c*x-s*y
        state[i+1]=s*x+c*y
        # pair loss AFTER each Givens. If eta=1 this reconstructs
        # sqrt(target probabilities); if eta<1, proportional scaling
        # of the remaining amplitude follows automatically.
        state[i]*=math.sqrt(eta)
        state[i+1]*=math.sqrt(eta)
        gates.append({"source_physical_port":i,
            "target_physical_port":i+1,"cos":c,"sin":s})
    state*=np.sign(target[order]).astype(complex)
    canonical=np.zeros(n,dtype=complex)
    canonical[np.array(order)]=state
    return canonical,gates

def quantify(ideal,real,B):
    throughput=float(np.vdot(real,real).real)
    normalized=real/math.sqrt(throughput)
    fidelity=float(abs(np.vdot(ideal,normalized))**2)
    dark_leak=float(np.linalg.norm(B.T@normalized)**2)
    return {"source_survival":throughput,
            "conditional_target_state_fidelity":fidelity,
            "conditional_short_time_line_leakage_t2_coefficient":dark_leak}

def main(path=None):
    B,edges,G=build();n=40
    A=B@B.T-4*np.eye(40)
    P=(8*np.eye(40)-4*A+np.ones((40,40)))/24
    psi=P[:,0]/math.sqrt(3/8)
    assert np.linalg.norm(B.T@psi)<1e-13
    original,g=construction(psi,1.)
    assert np.linalg.norm(original-psi)<1e-13
    assert len(g)==39
    assert abs(g[-1]["sin"]-1)<1e-12 or g[-1]["cos"]>0
    low_to_high=sorted(range(n),key=lambda i:-abs(psi[i])**2)
    sorted_output,_=construction(psi,1.,low_to_high)
    assert np.linalg.norm(sorted_output-psi)<1e-13
    cases={}
    for eta in (1.,.995,.99,.98,.95):
        natural,_=construction(psi,eta)
        sorted_,_=construction(psi,eta,low_to_high)
        cases[str(eta)]={"natural_40port_label_order":quantify(psi,natural,B),
                         "intensity_sorted_output_label_order":quantify(psi,sorted_,B)}
        assert cases[str(eta)]["intensity_sorted_output_label_order"]["source_survival"]>=cases[str(eta)]["natural_40port_label_order"]["source_survival"]-1e-12
    # For a 1D nearest-neighbor brickwork, support after d layers is
    # contained in sites [0,d] by induction. Since |psi_39|>0, d>=39.
    assert abs(psi[39])>1e-6
    assert len(g)==n-1
    out={"status":"PASS_W33_DARK_STATE_NEAREST_NEIGHBOR_39_DEPTH_LIGHT_CONE_AND_LOSS",
         "target_photonic_mode_amplitudes":[float(x) for x in psi],
         "target_support_size":int(sum(abs(psi)>1e-12)),
         "mode_line_geometry":"40 rails in physical chain, nearest-neighbor adjacent two-port Givens only",
         "single_initial_photon_port":0,
         "minimum_optical_interference_depth_from_locality":39,
         "constructive_serial_2port_Givens_count":39,
         "constructive_depth":39,
         "phase_pi_flips":int(sum(psi<0)),
         "full_coupler_program_natural_order":g,
         "port_label_order_for_sorted_intensity":low_to_high,
         "per_two_mode_gate_intensity_survival_controls":cases,
         "exact_ideal_preparation_amplitude_error":float(max(abs(original-psi))),
         "proof":"A nearest-neighbor unitary layer can enlarge support by at most one rail from the initial end port. Port39 has nonzero W33 dark amplitude, so depth is at least39. This explicit sequential chain of 39 Givens rotations and 12 pi sign phases reaches the target exactly, saturating the light-cone bound.",
         "physical_caution":"Sorting labels to increase throughput changes physical W33 incidence wiring and may add costly routing; sorting is not free under fixed hardware adjacency. This only prepares an initial 40-mode state, not an 80-mode W33 graph Hamiltonian, heralded single-photon source, readout, Bell test, or fault-tolerant device. Loss assumes independent equal intensity eta per addressed pair after each gate; no disconnected detector efficiencies or phase jitter.",
         "prior_art":"Linear-optical Givens preparation and one-dimensional causal light-cone bounds are standard; native W33 amplitudes make the resource comparison specific."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("LINEAR_CHAIN",json.dumps({"depth":39,"gates":39,"survival_natural_99":cases["0.99"]["natural_40port_label_order"]["source_survival"],
        "survival_sorted_99":cases["0.99"]["intensity_sorted_output_label_order"]["source_survival"],
        "fidelity_natural_99":cases["0.99"]["natural_40port_label_order"]["conditional_target_state_fidelity"]}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
