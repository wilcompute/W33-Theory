#!/usr/bin/env python3
"""Explicit MZI/Givens compilation of Witting A5 generators and 440 mixed states.

A single pure-state 4-port unitary cannot create mixed rho.
Instead for each E8-derived ququart rho, diagonalize rho=V diag(w) V†:
classically sample input eigenmode k with probabilities w_k, apply
V using at most six two-mode complex Givens and output a single
photon. This prepares mixed rho as a classical ensemble; no
ancillary entanglement is implied. Compile true native U4 generators
of both A5 classes, including projective 3/5 powers. Static drift
on all Givens is sampled and Witting40 readout TV errors quantified.
No physical chip, measured efficiencies or robust calibration bounds.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):sys.path.insert(0,str(p))
from toe_20261104_fourrail_givens_drift_detector_validation import compile_mesh,emitted
from exploration.w33_witting_srg_bridge import construct_witting_rays
OUT=ROOT/"data/toe_20261104_witting_mixed_state_mzi_preparation_controls.json"
def main():
 b=json.loads((ROOT/"data/toe_20261104_witting_operator_dark_spectral_A5_duality.json").read_text())
 g=json.loads((ROOT/"data/toe_20261104_witting_A5_unitary_lift_and_fisher.json").read_text())
 roots=json.loads((ROOT/"data/toe_20261104_two_e8_root_to_witting_density_codebook.json").read_text())
 O=np.array(b["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_real"])+1j*np.array(
 b["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_imag"])
 theta=np.array(roots["eight_real_parameters_for_440_states"])
 rays=np.array(construct_witting_rays())
 P=np.einsum("ia,ib->iab",rays,rays.conj())
 assert np.max(abs(np.sum(P,axis=0)-10*np.eye(4)))<1e-10
 def probs(rho):return np.real(np.einsum("iab,ba->i",P,rho))/10
 generators=[]
 for record in g["group_records"]:
  for elt in record["verified_Witting_projective_unitary_generators"]:
   U=np.array(elt["U4_real"])+1j*np.array(elt["U4_imag"])
   gates,diag=compile_mesh(U)
   ord=elt["order"]
   power=np.linalg.matrix_power(U,ord)
   assert np.max(abs(power-power[0,0]*np.eye(4)))<1e-9
   generators.append(dict(A5_class_index=record["A5_class_index"],
    generator_order=ord,required_Givens_count=len(gates),
    max_mesh_reconstruction_error=float(np.max(abs(U-_compose(gates,diag)))),
    projective_order_phase_real=float(power[0,0].real),
    projective_order_phase_imag=float(power[0,0].imag)))
 enc=[]
 for eps in (.1,.2):
  tt=theta*(eps/.1)
  R=np.eye(4)[None,:,:]/4+np.einsum("ij,jab->iab",tt,O)
  eig,V=np.linalg.eigh(R)
  assert eig.min()>0
  gate_max=0;gate_counts=[];err=0.
  for i in range(440):
   gates,diag=compile_mesh(V[i])
   gate_counts.append(len(gates));gate_max=max(gate_max,len(gates))
   Vrec=_compose(gates,diag)
   reconstructed=Vrec@np.diag(eig[i])@Vrec.conj().T
   err=max(err,float(np.max(abs(reconstructed-R[i]))))
  assert gate_max<=6 and err<1e-11
  enc.append(dict(epsilon=eps,root_state_count=440,all_rho_PSD=True,
    state_prep_mixture_classical_eigenmode_probs=eig[:8].tolist(),
    root_state_MZI_two_mode_gate_counts_histogram={str(n):int(gate_counts.count(n)) for n in sorted(set(gate_counts))},
    maximum_gates_for_4mode_mixed_state_prep=gate_max,
    maximum_440_mixed_state_density_matrix_mesh_reconstruction_error=err,
    all_440_preparable_by_classical_mixture_plus_4port_unitary=True))
 # Static calibration drift: 16 sample rho_j=I/4 +/- .1 O_j.
 # The classical source eigenstate distribution w is assumed stable.
 rng=np.random.default_rng(20261104)
 scans=[]
 for sigma in (0,.005,.02,.05,.1):
  tvs=[]
  for j in range(8):
   for sign in (-1,1):
    rho=np.eye(4)/4+sign*.1*O[j]
    w,U=np.linalg.eigh(rho)
    mesh=compile_mesh(U)
    target=probs(rho)
    for trial in range(128):
     V=emitted(*mesh,rng,sigma)
     noisy=V@np.diag(w)@V.conj().T
     tvs.append(float(np.sum(abs(probs(noisy)-target))/2))
  scans.append(dict(static_gate_mix_angle_and_phase_sigma=sigma,
    static_calibration_realizations_per_state=128,
    state_sign_controls=16,
    total_traces=len(tvs),
    Witting_POVM_TV_mean=float(np.mean(tvs)),
    Witting_POVM_TV_p95=float(np.quantile(tvs,.95)),
    Witting_POVM_TV_max_observed=float(max(tvs))))
  if sigma==0:assert max(tvs)<1e-10
 assert all(scans[i]["Witting_POVM_TV_mean"]<scans[i+1]["Witting_POVM_TV_mean"] for i in range(len(scans)-1))
 result=dict(status="PASS_WITTING_A5_FOUR_PORT_COMPILED_MIXED_STATE_440_PREP_AND_DRIFT",
  hardware_modes=4,native_interferometer_two_mode_givens_upper_bound=6,
  source_mixed_state_requires_classical_eigenmode_randomization=True,
  A5_ququart_group_generator_mesh_certificates=generators,
  E8_root_440_mixed_state_preparation=enc,
  output_readout_Witting40_POVM_static_drift_controls=scans,
  optical_achievability_qualification="Universal 4x4 passive unitary + CLASSICAL source-mode eigenstate mixture + calibrated 40-effect Witting analyzer; simulations only. No chip layout, real phase drift process or detector calibration.",
  prior_art="Reck/Clements 4x4 decomposition and classical randomized mixed-state preparation are standard. The new test compiles concrete native A5 Witting U4 and 440 actual packet/E8 ququart density family.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],"generators",[x["required_Givens_count"] for x in generators],
  "drift",[(z["static_gate_mix_angle_and_phase_sigma"],z["Witting_POVM_TV_mean"]) for z in scans],flush=True)
 return result
def _compose(gates,phases):
 M=np.diag(phases)
 for k,G in reversed(gates):
  E=np.eye(4,dtype=complex);E[k:k+2,k:k+2]=G;M=E@M
 return M
if __name__=="__main__": main()
