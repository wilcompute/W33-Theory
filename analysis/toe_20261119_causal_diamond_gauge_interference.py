#!/usr/bin/env python3
"""Gauge-invariant two-path interference on a four-event causal DAG diamond.

A DAG has no directed closed cycles. Nevertheless, comparing two
forward-only paths with equal endpoints yields a gauge-invariant Wilson
holonomy and retarded interference. The bare retarded determinant stays
independent of every phase. This is a finite U(1) transport toy.
"""
from pathlib import Path
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_causal_diamond_gauge_interference.json"

def diamond_operator(angles):
    """Four U1 link angles: 0->1,0->2,1->3,2->3."""
    a,b,c,d=angles
    T=np.zeros((4,4),dtype=complex)
    T[0,1]=np.exp(1j*a)
    T[0,2]=np.exp(1j*b)
    T[1,3]=np.exp(1j*c)
    T[2,3]=np.exp(1j*d)
    return T

def observables(angles,mass=1.3,alpha=.6):
    T=diamond_operator(angles)
    assert np.linalg.norm(T@T@T)<1e-12
    G=np.linalg.inv(mass*np.eye(4)-alpha*T)
    one=T[0,1]*T[1,3]
    two=T[0,2]*T[2,3]
    relative=one*np.conj(two)
    expected=(alpha*alpha/mass**3)*(one+two)
    assert abs(G[0,3]-expected)<1e-12
    det=np.linalg.det(mass*np.eye(4)-alpha*T)
    assert abs(det-mass**4)<1e-12
    return {"directed_edges":4,"causal_directed_cycles":0,
            "path_left_phase":float(np.angle(one)),
            "path_right_phase":float(np.angle(two)),
            "gauge_invariant_relative_holonomy_real_imag":[float(relative.real),float(relative.imag)],
            "retarded_source_to_destination_amplitude_real_imag":[float(G[0,3].real),float(G[0,3].imag)],
            "retarded_probability_like_intensity":float(abs(G[0,3])**2),
            "phase_blind_determinant_real_imag":[float(det.real),float(det.imag)],
            "predicted_intensity":(alpha**4/mass**6)*(2+2*relative.real)}

def study():
    cases=[]
    for phase in (0.,math.pi/3,math.pi/2,math.pi):
        x=observables([0.,0.,0.,phase])
        assert abs(x["retarded_probability_like_intensity"]-x["predicted_intensity"])<1e-12
        cases.append({"relative_phase":phase,**x})
    I=[x["retarded_probability_like_intensity"] for x in cases]
    assert I[0]>I[1]>I[2]>I[3]-1e-15
    assert I[3]<1e-25
    rng=np.random.default_rng(20261119)
    frame_checks=[]
    for k in range(40):
        angles=rng.uniform(-math.pi,math.pi,4)
        phases=rng.uniform(-math.pi,math.pi,4)
        base=observables(angles)
        T=diamond_operator(angles)
        U=np.diag(np.exp(1j*phases))
        transformed=U@T@U.conj().T
        new_angles=[np.angle(transformed[0,1]),np.angle(transformed[0,2]),
                    np.angle(transformed[1,3]),np.angle(transformed[2,3])]
        new=observables(new_angles)
        assert abs(base["retarded_probability_like_intensity"]-new["retarded_probability_like_intensity"])<1e-12
        p=complex(*base["gauge_invariant_relative_holonomy_real_imag"])
        q=complex(*new["gauge_invariant_relative_holonomy_real_imag"])
        assert abs(p-q)<1e-12
        z=complex(*base["retarded_source_to_destination_amplitude_real_imag"])
        w=complex(*new["retarded_source_to_destination_amplitude_real_imag"])
        assert abs(w-z*np.exp(1j*(phases[0]-phases[3])))<1e-12
        frame_checks.append(abs(p-q))
    return {"date":"2026-11-19","status":"PASS gauge-covariant causal diamond retarded interference",
      "four_reference_phases":cases,"random_local_gauge_frame_trials":len(frame_checks),
      "largest_gauge_invariant_holonomy_error":max(frame_checks),
      "exact_formula":"G_0,3=(alpha²/m³)(U_01 U_13 + U_02 U_23)",
      "gauge_invariant_path_difference":"W=(U_01 U_13)*conj(U_02 U_23); |G_0,3|²=(alpha^4/m^6)[2+2 Re(W)]",
      "causal_determinant":"det(mI-alpha T)=m^4 independent of phases, because the forward-edge matrix T is strictly upper triangular.",
      "physical_limit":"No closed TIMELIKE path is required: the comparison uses one path and the inverse transport of another, not a backwards physical causal signal. Gauge link phases and coherent quantum/wave transport are supplied inputs; not emergent photons, full QED, a Born rule, or gravity.",
      "TOE_solved":False}

def main():
    result=study()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"status":"PASS","gauge_trials":result["random_local_gauge_frame_trials"],
                      "delta0_intensity":result["four_reference_phases"][0]["retarded_probability_like_intensity"],
                      "delta_pi_intensity":result["four_reference_phases"][-1]["retarded_probability_like_intensity"],
                      "output":str(OUT)}))
if __name__=="__main__":main()
