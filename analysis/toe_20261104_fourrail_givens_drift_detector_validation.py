#!/usr/bin/env python3
"""Four-mode beam-splitter compilation and STATIC drift falsifier for C4 flux.

Exact 4x4 Givens decomposition of U=exp(-it Hzero/pi) at t=pi/2.
Every complex 2x2 gate encoded, ideal error <1e-12.
Independent small mixing-angle and differential-phase gate errors
drawn once per calibration realization, not iid per photon.
Sample 512 static calibrations each at sigma .005,.02,.05,.1,
compute overlap after recomposition and opposite-port click
probabilities with detector efficiency eta=.85 dark rate .005,
optional uniform total photon survival exp(-gamma*t) gamma=.1.
Use WORST OBSERVED calibration pzero_min and ppi_max in exact
binomial error tails. This is only a finite sampled robustness
envelope, not a uniform interval proof or guaranteed hardware
confidence claim; crosstalk, many-shot drift and source statistics
need experimental characterization.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261104_fourrail_givens_drift_detector_validation.json"
def H(flux):
 A=np.zeros((4,4),dtype=complex)
 for i,j in ((0,1),(1,2),(2,3),(3,0)):
  z=-1 if (i,j)==(3,0) and flux else 1
  A[i,j]=A[j,i]=z
 return A
def compile_mesh(U):
 R=U.copy();gates=[]
 for j in range(3):
  for k in range(3,j,-1):
   a,b=R[k-1,j],R[k,j]
   n=math.hypot(abs(a),abs(b))
   if n<1e-12:continue
   G=np.array([[a.conjugate(),b.conjugate()],[-b,a]])/n
   R[k-1:k+1,:]=G@R[k-1:k+1,:]
   gates.append((k-1,G.conj().T))
 assert np.max(abs(R-np.diag(np.diag(R))))<1e-12
 phases=np.diag(R)
 assert max(abs(abs(x)-1) for x in phases)<1e-12
 V=np.diag(phases)
 for k,G in reversed(gates):
  E=np.eye(4,dtype=complex);E[k:k+2,k:k+2]=G
  V=E@V
 assert np.max(abs(V-U))<1e-12
 return gates,phases
def emitted(gates,phases,rng,sigma):
 V=np.diag(phases)
 for k,G in reversed(gates):
  a,b=rng.normal(0,sigma,2)
  R=np.array([[math.cos(a),math.sin(a)],[-math.sin(a),math.cos(a)]])
  Z=np.diag(np.exp(1j*np.array([b,-b])/2))
  E=np.eye(4,dtype=complex)
  E[k:k+2,k:k+2]=Z@R@G
  V=E@V
 assert np.max(abs(V.conj().T@V-np.eye(4)))<1e-11
 return V
def trials_exact(p0,p1,alpha=2.86651571879e-7,maxn=3000):
 assert 0<=p1<p0<=1
 for n in range(1,maxn+1):
  k=np.arange(1,n+1)
  fp=binom.sf(k-1,n,p1);fn=binom.cdf(k-1,n,p0)
  good=np.flatnonzero((fp<=alpha)&(fn<=alpha))
  if len(good):
   j=int(good[0])
   return dict(n=n,click_threshold=int(k[j]),false_zero_when_pi=float(fp[j]),
     false_pi_when_zero=float(fn[j]))
 return None
def main():
 t=math.pi/2
 U=[expm(-1j*t*H(f)) for f in (False,True)]
 assert abs(abs(U[0][2,0])**2-1)<1e-11
 assert abs(U[1][2,0])<1e-11
 compiled=[compile_mesh(x) for x in U]
 lens=[len(c[0]) for c in compiled]
 rng=np.random.default_rng(20261104)
 eta=.85;dark=.005;gamma=.1;surv=math.exp(-gamma*t)
 def click(p):return dark+(1-dark)*eta*surv*p
 scans=[]
 for sigma in (0,.005,.02,.05,.1):
  vals=[[],[]];uniterr=[[],[]]
  for _ in range(512):
   for j in (0,1):
    V=emitted(*compiled[j],rng,sigma)
    prob=float(abs(V[2,0])**2)
    vals[j].append(click(prob))
    uniterr[j].append(float(np.max(abs(V-U[j]))))
  z=np.array(vals[0]);p=np.array(vals[1])
  assert min(z)>max(p)
  decision=trials_exact(float(z.min()),float(p.max()))
  assert decision is not None
  scans.append(dict(gate_angle_and_phase_sigma=sigma,calibration_realizations=512,
    zero_flux_click_min=float(min(z)),zero_flux_click_mean=float(np.mean(z)),
    zero_flux_click_max=float(max(z)),
    pi_flux_click_min=float(min(p)),pi_flux_click_mean=float(np.mean(p)),
    pi_flux_click_max=float(max(p)),
    min_observed_calibration_population_contrast=float(min(z)-max(p)),
    max_unitary_entrywise_error_zero=float(max(uniterr[0])),
    max_unitary_entrywise_error_pi=float(max(uniterr[1])),
    binomial_rule_for_worst_observed_2_calibrations=decision,
    not_uniform_hardware_calibration_confidence_interval=True))
 # Separately take previous 5-level Lindblad dephase + loss and add detector
 # inefficiency/dark counts; do not compound our mesh's uniform loss again.
 source=ROOT/"data/toe_20261104_e8_c4_flux_photonic_falsifier.json"
 old=json.loads(source.read_text(encoding="utf8"))
 row=next(z for z in old["uniform_loss_plus_markov_site_dephasing_control"]
          if z["uniform_loss_rate"]==.1 and z["site_dephasing_rate"]==.1)
 p0=dark+(1-dark)*eta*row["zero_flux_opposite_probability_unconditional"]
 pp=dark+(1-dark)*eta*row["pi_flux_opposite_probability_unconditional"]
 assert p0>pp
 lindblad_rule=trials_exact(p0,pp)
 result=dict(status="PASS_FOUR_MODE_EXACT_GIVENS_AND_512_STATIC_CALIBRATION_CONTROLS",
   modes=4,target_evolution_time=t,
   ideal_givens_two_mode_gate_counts={"zero_flux":lens[0],"pi_flux":lens[1]},
   ideal_givens_reconstruction_error_less_than_1e_minus12=True,
   ideal_gate_blocks_encoded_as_complex_real_imag=[
      [dict(modes=[k,k+1],real=G.real.tolist(),imag=G.imag.tolist())
       for k,G in mesh[0]] for mesh in compiled],
   residual_output_phases_real_imag=[
      dict(real=mesh[1].real.tolist(),imag=mesh[1].imag.tolist()) for mesh in compiled],
   assumed_detector_efficiency=eta,detector_dark_click_probability=dark,
   assumed_uniform_photon_loss_rate_for_mesh_run=gamma,
   assumed_survival_for_mesh_run=surv,
   detector_click_model="pclick=dark+(1-dark)*eta*survival*p_rail",
   Monte_Carlo_static_mesh_error_calibration=scans,
   Lindblad_dephasing_plus_loss_with_detector_added={
     "source":"data/toe_20261104_e8_c4_flux_photonic_falsifier.json",
     "gamma":.1,"kappa":.1,"eta":eta,"dark":dark,
     "zero_flux_click_probability":p0,"pi_flux_click_probability":pp,
     "exact_iid_binomial_rule_known_fixed_rates":lindblad_rule},
   confidence_firewall="Exact binomial tails hold for fixed known click probabilities. The worst OBSERVED calibration sample is NOT a rigorous confidence region for all possible optical hardware. Static miscalibration persists across photons, so treating averaged Monte-Carlo calibration data as iid per photon is wrong.",
   physical_boundary="A four-mode mathematically compiled U(4) and stochastic controls; actual MZI propagation, source generation, thermal crosstalk, timing noise, detector dead time, and calibration drift need measured parameters. These optics demonstrate existing AB interference, not E8 particles or a completed TOE.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],lens,[(x["gate_angle_and_phase_sigma"],x["binomial_rule_for_worst_observed_2_calibrations"]["n"]) for x in scans],flush=True)
 return result
if __name__=="__main__":main()
