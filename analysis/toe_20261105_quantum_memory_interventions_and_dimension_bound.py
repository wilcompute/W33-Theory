#!/usr/bin/env python3
"""Trusted intervention independence and Schmidt-number memory dimension gate.

Complete ideal R,S,E qutrit SWAP-storage-SWAP process: across identity,
X, Z, Fourier, dephasing and two replacement CPTP instruments on
accessible S at middle time, final R-S entangled fidelity remains1.
Coherent E is untouched; classicalized E via ANY Haar basis complete
dephasing always returns an EB R-S state F=1/3.
Without interventions and trusting the memory bottleneck this alone
doesn't establish exotic time physics. Singlet F>m/d certifies Schmidt
number>m for target reference-output state and a dimension-of-quantum
communication bound on sole coherent memory. For d3, observing F>2/3
excludes any sole 2D quantum memory bottleneck. Not a device-independent
witness; reference control, reset, leakage and herald calibration crucial.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):sys.path.insert(0,str(p))
import toe_20261104_reset_immune_quantum_memory_falsifier as old
OUT=ROOT/"data/toe_20261105_quantum_memory_interventions_and_dimension_bound.json"
I=old.I
P0=old.P0
def channel_on_s(rho,kind):
 if kind in ("reset0","reset1"):
  j=0 if kind=="reset0" else 1
  rho4=rho.reshape((3,)*6)
  reduced=np.einsum("rseRsE->reRE",rho4)
  dest=np.diag([int(x==j) for x in range(3)])
  return np.einsum("reRE,sS->rseRSE",reduced,dest).reshape(27,27)
 if kind=="dephase":
  v=np.zeros_like(rho)
  for j in range(3):
   Proj=np.diag([int(x==j) for x in range(3)])
   K=np.kron(np.kron(I,Proj),I)
   v+=K@rho@K
  return v
 if kind=="identity":return rho
 X=np.roll(I,1,axis=0)
 Z=np.diag(np.exp(2j*np.pi*np.arange(3)/3))
 Fourier=np.exp(2j*np.pi*np.outer(np.arange(3),np.arange(3))/3)/math.sqrt(3)
 U={"X":X,"Z":Z,"Fourier":Fourier}[kind]
 W=np.kron(np.kron(I,U),I)
 return W@rho@W.conj().T
def environment_dephase(rho,W):
 out=np.zeros_like(rho)
 for i in range(3):
  p=W[:,i:i+1]@W[:,i:i+1].conj().T
  L=np.kron(np.eye(9),p)
  out+=L@rho@L
 return out
def main():
 rho0=np.kron(old.Phi,P0)
 loaded=old.U@rho0@old.U.conj().T
 assert abs(np.trace(loaded)-1)<1e-12
 interventions=["identity","X","Z","Fourier","dephase","reset0","reset1"]
 records=[]
 for name in interventions:
  a=channel_on_s(loaded,name)
  release=old.reduced_rs(old.U@a@old.U.conj().T)
  coherent=old.fidelity(release)
  assert abs(coherent-1)<1e-11
  classical=environment_dephase(loaded,I)
  clrelease=old.reduced_rs(old.U@channel_on_s(classical,name)@old.U.conj().T)
  fclass=old.fidelity(clrelease)
  assert abs(fclass-1/3)<1e-11
  assert old.negativity(clrelease)<1e-11
  records.append(dict(intervention=name,
    quantum_memory_recovered_singlet_fraction=coherent,
    dephased_classical_memory_singlet_fraction=fclass,
    recovered_entanglement_negativity=old.negativity(release),
    no_accessible_intervention_can_affect_coherently_stored_E_in_ideal_SWAPS=True))
 rng=np.random.default_rng(20261105)
 arbitrary=[]
 for _ in range(32):
  x=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
  U,R=np.linalg.qr(x)
  U=U*np.diag(R).conj()/abs(np.diag(R))
  d=environment_dephase(loaded,U)
  f=old.fidelity(old.reduced_rs(old.U@old.reset_s(d)@old.U.conj().T))
  assert abs(f-1/3)<1e-10
  arbitrary.append(f)
 # Maximum singlet overlap for a normalized Schmidt rank-m state:
 # m/d, attained by uniform equal Schmidt amplitudes in m dimensions.
 def schmidt_state(m):
  x=np.zeros(9,complex)
  for k in range(m):x[3*k+k]=1/math.sqrt(m)
  return np.outer(x,x.conj())
 ranks=[]
 for m in (1,2,3):
  b=float(np.trace(old.Phi@schmidt_state(m)).real)
  assert abs(b-m/3)<1e-12
  ranks.append(dict(Schmidt_rank_m=m,max_singlet_fidelity_m_over_three=b))
 old_data=json.loads((ROOT/"data/toe_20261104_reset_immune_quantum_memory_falsifier.json").read_text())
 chosen=next(z for z in old_data["noise_herald_exact_binomial_controls"] if z["storage_coherence_p"]==.6 and z["independent_herald_efficiency_eta"]==.85)
 result=dict(status="PASS_THREE_TIME_QUTRIT_7_INTERVENTIONS_32_CLASSICAL_ADVERSARIES_AND_MEMORY_BOTTLENECK",
  S_R_E_total_dimension=27,
  middle_instruments=records,
  arbitrary_classical_memory_dephasing_Haar_bases=32,
  recovered_fidelity_classical_E_any_test_basis_max=float(max(arbitrary)),
  Schmidt_number_m_singlet_fraction_upper_bounds=ranks,
  trusted_perfect_identity_recovery_requires_quantum_bottleneck_dimension_at_least3=True,
  noisy_memory_p_greater_than_5_over8_recovery_singlet_exceeds_rank2_upper_bound=True,
  p_equal_point6_eta085_Binomial_exact_rule=chosen["exact_binomial_separable_null_vs_model_alt_5sigma_rule"],
  no_click_assumption="Independent, state-independent η, no unobserved coherent quantum bypass; no-click qutrit assigned maximally mixed. The exact binomial bounds apply ONLY to this declared statistical model.",
  scientific_priority="Schmidt-number witnesses, quantum-memory SWAP examples and EB channel caveats all known. These 7+32 intervention controls apply the old W33 temporal proposal to a quantifiable memory-dimension falsifier, not independent proof of photon self-entanglement.",
  caveat="A general multitime process with correlated initial reference-environment state, adaptive classical apparatus, or an untrusted extra quantum path is not excluded. No laboratory implementation.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
 print(result["status"],"F",[(x["intervention"],x["quantum_memory_recovered_singlet_fraction"]) for x in records],flush=True)
 return result
if __name__=="__main__":main()
