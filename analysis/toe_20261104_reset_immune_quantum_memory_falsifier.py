#!/usr/bin/env python3
"""Three-time qutrit quantum-memory witness after an entanglement-breaking RESET.

Reference R and input S start maximally entangled. Quantum env E
stores S coherently via SWAP at t1; intermediate device replaces S
with |0><0| (entanglement-breaking); later SWAP releases E to S.
Final R-S entanglement survives. A classical-only env E dephased
at storage yields separable R-S and singlet fraction F=1/3.
An environmentless Markov identity+reset returns F=1/9.
Noise on env modeled by depolarizing E_p gives F=(1+8p)/9,
negativity max(0,(4p-1)/3). Trusted ancilla/time-local
intervention and loss-independent heralding are essential.
A classical-memory EB instrument cannot distribute entanglement
from reference to output across the reset if no quantum bypass.
No indefinite time direction or single-photon cosmology follows.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261104_reset_immune_quantum_memory_falsifier.json"
d=3;I=np.eye(3,dtype=complex)
phi=I.reshape(-1,order="F")/math.sqrt(3)
Phi=np.outer(phi,phi.conj())
P0=np.diag([1.,0.,0.])
SW=np.zeros((9,9),dtype=complex)
for a in range(3):
 for b in range(3):
  SW[a*3+b,b*3+a]=1
U=np.kron(I,SW)
def reset_s(rho):
 m=rho.reshape((3,)*6)
 re=np.einsum("rseRsE->reRE",m)
 out=np.einsum("reRE,sS->rseRSE",re,P0).reshape(27,27)
 assert abs(np.trace(out)-1)<1e-12
 return out
def dep_e(rho,p):
 m=rho.reshape((3,)*6)
 rs=np.einsum("rseRSe->rsRS",m)
 b=np.einsum("rsRS,eE->rseRSE",rs,I/3).reshape(27,27)
 return p*rho+(1-p)*b
def dephase_e(rho):
 m=rho.reshape((3,)*6)
 out=np.einsum("rseRSE,eE->rseRSE",m,I).reshape(27,27)
 assert abs(np.trace(out)-1)<1e-12
 return out
def reduced_rs(rho):
 return np.einsum("rseRSe->rsRS",rho.reshape((3,)*6)).reshape(9,9)
def pt_second(J):return J.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
def negativity(J):return float(-np.sum(np.linalg.eigvalsh(pt_second(J))[np.linalg.eigvalsh(pt_second(J))<0]))
def fidelity(J):return float(np.trace(Phi@J).real)
def evolution(kind="coherent",p=1):
 rho=np.kron(Phi,P0)
 rho=U@rho@U.conj().T # S moved coherently to E; S now |0>
 if kind=="classical":rho=dephase_e(rho)
 if kind=="depolarizing":rho=dep_e(rho,p)
 rho=reset_s(rho) # trusted EB action on S
 rho=U@rho@U.conj().T # coherent env releases R correlation to S
 out=reduced_rs(rho)
 assert abs(np.trace(out)-1)<1e-12
 assert np.linalg.eigvalsh(out).min()>-1e-12
 return out
def exact_two_rates(p0,p1,alpha=2.866515718791933e-7):
 assert -1e-12<=p0<p1<=1+1e-12
 p0=max(0.,min(1.,p0));p1=max(0.,min(1.,p1))
 def evaluate(n):
  k=int(binom.isf(alpha,n,p0))+1
  if k<1 or k>n:return None
  fp=float(binom.sf(k-1,n,p0))
  fn=float(binom.cdf(k-1,n,p1))
  if fp<=alpha*(1+1e-8) and fn<=alpha:
   return dict(n=n,threshold=k,false_positive=fp,false_negative=fn)
  return None
 hi=1
 while evaluate(hi) is None:
  hi*=2
  assert hi<=2**22,(p0,p1,hi)
 lo=0
 while hi-lo>1:
  mid=(hi+lo)//2
  if evaluate(mid) is not None:hi=mid
  else:lo=mid
 return evaluate(hi)
def main():
 coherent=evolution()
 classical=evolution("classical")
 full_dep=evolution("depolarizing",0)
 markov=np.kron(I/3,P0)
 assert abs(fidelity(coherent)-1)<1e-12
 assert abs(fidelity(classical)-1/3)<1e-12
 assert negativity(classical)<1e-12
 assert abs(fidelity(full_dep)-1/9)<1e-12
 assert abs(fidelity(markov)-1/9)<1e-12
 rows=[]
 for p in (0,.2,.25,.3,.5,.6,.8,1):
  rho=evolution("depolarizing",p)
  f=fidelity(rho);neg=negativity(rho)
  assert abs(f-(1+8*p)/9)<1e-12
  assert abs(neg-max(0,(4*p-1)/3))<1e-12
  for eta in (.6,.85,1):
   # Trusted independent heralding and a declared no-click-to-I/3
   # assignment gives a 9D full-trial effective conditional state.
   observed=eta*f+(1-eta)/9
   EB_bound=eta/3+(1-eta)/9
   decision=exact_two_rates(EB_bound,observed) if observed>EB_bound+1e-9 else None
   rows.append(dict(storage_coherence_p=p,independent_herald_efficiency_eta=eta,
     unconditional_reference_singlet_probability=observed,
     separable_memory_upper_bound_with_same_trusted_eta=EB_bound,
     channel_entanglement_negativity=neg,
     conditioned_memory_singlet_fidelity=f,
     exact_binomial_separable_null_vs_model_alt_5sigma_rule=decision,
     witness_positive=observed>EB_bound+1e-9))
 assert next(x for x in rows if x["storage_coherence_p"]==.6 and x["independent_herald_efficiency_eta"]==.85)["witness_positive"]
 result=dict(status="PASS_THREE_TIME_RESET_IMMUNE_QUANTUM_MEMORY_VS_CLASSICAL_EB_FALSIFIER",
  joint_R_S_E_dimension=27,
  input_ref_system_singlet_qutrit_fidelity=1,
  memory_sequential_SWAPS_count=2,
  intermediate_intervention="trusted qutrit entanglement-breaking replacement R_s(rho)=|0><0|Tr_s(rho)",
  recovered_R_output_fidelity_quantum_coherent_memory=fidelity(coherent),
  recovered_R_output_fidelity_classical_dephased_memory=fidelity(classical),
  recovered_R_output_fidelity_markovian_no_quantum_memory=fidelity(markov),
  quantum_coherent_memory_negativity=negativity(coherent),
  classical_dephased_memory_negativity=negativity(classical),
  quantum_storage_depolarizing_fidelity_formula="(1+8p)/9",
  quantum_storage_NPT_iff_p_greater_than_one_quarter=True,
  qutrit_separable_memory_singlet_fraction_upper_bound=1/3,
  noise_herald_exact_binomial_controls=rows,
  witness_operational_requirements="trusted maximally entangled reference, verified EB reset, no unmonitored quantum bypass, independently calibrated state-independent heralding eta; joint R-S singlet measurement.",
  detection_warning="If loss depends on untrusted state or memory, a conditionally selected subensemble need not obey the calibrated eta null. The all-trials test uses no-click assigned random maximally-mixed qutrit, not hidden conditional renormalization.",
  physics_boundary="Quantum memory via SWAP is a textbook example. This explicitly separates stored quantum coherence from classical-only environment memory in a three-time instrument. NOT a single photon past/future self-entanglement measurement or proof of retrocausality.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],"F quantum/classical",fidelity(coherent),fidelity(classical),flush=True)
 return result
if __name__=="__main__":main()
