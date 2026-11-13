#!/usr/bin/env python3
"""A falsifiable ideal 35-mode interferometric signature of the
order-six USp8 -> order-three Lambda2_0(8) central quotient.

Use coherent one-photon direct sum C8⊕C27, gate diag(g8,U27).
After THREE pulses: -I8 ⊕ +I27, so equal-arm
C8/C27 superposition returns orthogonal to original.
After SIX pulses: I35, full revival. Global -I8 is not
individually measurable within one irrep; comparing
TWO REPRESENTATIONS provides the relative phase.

A proposed optical benchmark, NOT a measured test of physical time
or direct evidence of an E6 universe.
"""
from pathlib import Path
import json,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261113_USp8_to_E6_Z2_central_interferometric_witness.json"

def main():
    d=json.loads((ROOT/"data/toe_20261113_USp8_8mode_Albert_clock_exact_group_check.json").read_text())
    g=np.array(d["8mode_group_real"])+1j*np.array(d["8mode_group_imag"])
    Ucert=json.loads((ROOT/"data/toe_20261113_Albert_cyclic_clock_sections.json").read_text())
    U=np.zeros((27,27),dtype=complex)
    for i,j,v in Ucert["signed_E6_clock_matrix_27_sparse_entries"]:U[i,j]=v
    assert np.max(abs(np.linalg.matrix_power(g,3)+np.eye(8)))<1e-10
    assert np.max(abs(np.linalg.matrix_power(U,3)-np.eye(27)))<1e-12
    direct=np.zeros((35,35),dtype=complex)
    direct[:8,:8]=g
    direct[8:,8:]=U
    assert np.max(abs(direct.conj().T@direct-np.eye(35)))<1e-10
    rng=np.random.default_rng(20261113)
    a=rng.normal(size=8)+1j*rng.normal(size=8)
    b=rng.normal(size=27)+1j*rng.normal(size=27)
    a/=np.linalg.norm(a);b/=np.linalg.norm(b)
    state=np.r_[a,b]/math.sqrt(2)
    assert abs(np.vdot(state,state)-1)<1e-12
    overlap3=np.vdot(state,np.linalg.matrix_power(direct,3)@state)
    overlap6=np.vdot(state,np.linalg.matrix_power(direct,6)@state)
    assert abs(overlap3)<1e-9
    assert abs(overlap6-1)<1e-9
    only8=np.r_[a,np.zeros(27)]
    only27=np.r_[np.zeros(8),b]
    assert abs(abs(np.vdot(only8,np.linalg.matrix_power(direct,3)@only8))-1)<1e-9
    assert abs(abs(np.vdot(only27,np.linalg.matrix_power(direct,3)@only27))-1)<1e-9
    sigma=.10
    e=math.exp(-sigma*sigma/2)
    expected_dark=(1-e)/2
    expected_bright=(1+e)/2
    assert expected_dark<.003 and expected_bright>.997
    out={
      "status":"PASS_35MODE_USP8_E6_CENTRAL_Z2_RELATIVE_PHASE_CLOCK_WITNESS",
      "optical_mode_count":35,"defining_representation_modes":8,"wedge_traceless_representation_modes":27,
      "clock_eight_order":6,"clock_twentyseven_order":3,
      "third_pulse_action":"(-I8) direct_sum (+I27)",
      "sixth_pulse_action":"(+I8) direct_sum (+I27)",
      "balanced_two_irrep_input_revival_probability_after_three":float(abs(overlap3)**2),
      "balanced_two_irrep_input_revival_probability_after_six":float(abs(overlap6)**2),
      "single_irrep_initial_state_three_pulse_absolute_overlap":1.0,
      "independent_gaussian_relative_phase_noise_sigma_radians":sigma,
      "mean_dark_output_probability_after_three_with_relative_phase_noise":expected_dark,
      "mean_bright_output_probability_after_six_with_relative_phase_noise":expected_bright,
      "fourier_signature":"The relative Z2 center is detectable by interference across the direct sum, but NOT from probabilities within either standalone irrep.",
      "boundary":"This is a proposed 35-path coherent optical protocol using both representations and a phase reference. Not a physical measurement, not evidence of extra spacetime dimensions, and not a sub-8-path implementation of the full 27D clock. Phase drifts, optical losses and true gate synthesis must be calibrated."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ["status","balanced_two_irrep_input_revival_probability_after_three","balanced_two_irrep_input_revival_probability_after_six","mean_dark_output_probability_after_three_with_relative_phase_noise"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
