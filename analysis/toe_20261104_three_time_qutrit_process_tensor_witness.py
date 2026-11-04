#!/usr/bin/env python3
"""Operational, ancilla-assisted three-time qutrit process-tensor control.

Two sequential depolarizing qutrit channels E_t with choice of
intermediate intervention I, unitary X, dephase or reprepare. Exact
9x9 Choi states, input-output partial transpose, causal trace,
81x81 product-comb Markov control and independent erasure flags.
A Choi fidelity >1/3 is a rigorous entanglement-breaking channel
exclusion with trusted entangled reference/process tomography.
It does NOT exclude every classical hidden-memory process without
ancilla/trust assumptions, nor show future/past self-entanglement.
"""
from __future__ import annotations
import math,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261104_three_time_qutrit_process_tensor_witness.json"
d=3
I=np.eye(d,dtype=complex)
phi=I.reshape(-1,order="F")/math.sqrt(3)
Phi=np.outer(phi,phi.conj())
swap=np.zeros((9,9),dtype=complex)
for a in range(d):
 for b in range(d):swap[a+d*b,b+d*a]=1
def dep(r,t):
 return t*r+(1-t)*np.trace(r)*I/3
def compose_channel(t,mid):
 def E(r):
  x=dep(r,t)
  if mid=="identity":y=x
  elif mid=="cyclic_X":
   X=np.roll(I,1,axis=0);y=X@x@X.conj().T
  elif mid=="dephase":y=np.diag(np.diag(x))
  elif mid=="reprepare_zero":y=np.trace(x)*np.diag([1,0,0])
  else:raise ValueError(mid)
  return dep(y,t)
 return E
def choi(channel):
 J=np.zeros((9,9),dtype=complex)
 for i in range(3):
  for j in range(3):
   E=np.zeros((3,3),dtype=complex);E[i,j]=1
   J+=np.kron(E,channel(E))/3
 assert abs(np.trace(J)-1)<1e-12
 assert np.min(np.linalg.eigvalsh(J))>-1e-12
 return J
def pt_output(J):
 X=J.reshape(3,3,3,3)
 return X.transpose(0,3,2,1).reshape(9,9)
def negativity(J):
 return float(sum(abs(v) for v in np.linalg.eigvalsh(pt_output(J))
          if v<0))
def input_marginal(J):
 return np.einsum('iaja->ij',J.reshape(3,3,3,3))
def tensor_choi(M,N):
 return np.kron(M,N)
def main():
 rows=[]
 for t in (0,.24,.26,.45,.5,.6,.75,1):
  one=choi(lambda x:dep(x,t))
  assert np.max(abs(input_marginal(one)-I/3))<1e-12
  assert abs(float(np.trace(Phi@one).real)-(1+8*t)/9)<1e-12
  n1=negativity(one)
  assert abs(n1-max(0,(4*t-1)/3))<1e-12
  comb=tensor_choi(one,one)
  assert comb.shape==(81,81)
  assert abs(np.trace(comb)-1)<1e-11
  assert np.max(abs(np.trace(comb.reshape(9,9,9,9),axis1=1,axis2=3)-one))<1e-12
  cells={}
  for m in ("identity","cyclic_X","dephase","reprepare_zero"):
   J=choi(compose_channel(t,m))
   assert np.max(abs(input_marginal(J)-I/3))<1e-12
   neg=negativity(J)
   if m in ("dephase","reprepare_zero"):assert neg<1e-11
   if m in ("identity","cyclic_X"):
    assert abs(neg-max(0,(4*t*t-1)/3))<1e-11
   F=float(np.trace(Phi@J).real)
   if m=="identity":assert abs(F-(1+8*t*t)/9)<1e-11
   cells[m]=dict(Choi_entanglement_negativity=neg,
     singlet_fraction_to_identity=F,
     identity_reference_witness_F_gt_one_third=bool(F>1/3+1e-10),
     channel_entanglement_breaking_excluded_by_any_negative_PT=bool(neg>1e-10))
  rows.append(dict(step_depolarizing_transmission_t=t,
    each_link_Choi_singlet_fraction=float(np.trace(Phi@one).real),
    each_link_entanglement_negativity=n1,
    three_time_2link_process_tensor_is_Markov_product=True,
    intermediate_interventions=cells,
    both_links_NPT_but_end_to_end_identity_entanglement_broken=
       bool(n1>1e-10 and cells["identity"]["Choi_entanglement_negativity"]<1e-10)))
 assert next(x for x in rows if x["step_depolarizing_transmission_t"]==.45)["both_links_NPT_but_end_to_end_identity_entanglement_broken"]
 assert next(x for x in rows if x["step_depolarizing_transmission_t"]==.6)["intermediate_interventions"]["identity"]["Choi_entanglement_negativity"]>0
 erasures=[]
 for t in (.45,.6,.8):
  F=(1+8*t*t)/9
  for eta in (.6,.8,.95,1):
   survived=eta*eta
   erasures.append(dict(t=t,step_survival_eta=eta,both_links_survival_probability=survived,
    unconditioned_accepted_singlet_fraction=survived*F,
    conditioned_on_success_singlet_fraction=F,
    genuine_process_entanglement_witness_if_ancilla_and_trusted_heralding=
      bool(F>1/3),
    naive_unconditioned_threshold_F_gt_third=bool(survived*F>1/3)))
 assert any(x["genuine_process_entanglement_witness_if_ancilla_and_trusted_heralding"] and
           not x["naive_unconditioned_threshold_F_gt_third"] for x in erasures)
 result=dict(status="PASS_EXPLICIT_THREE_TIME_QUTRIT_CHOIS_INTERVENTIONS_MARKOV_CONTROL",
    time_slices=3,quantum_links=2,system_dimension=3,
    link_Choi_dimension=9,product_process_tensor_dimension=81,
    intermediate_intervention_set=["identity","cyclic_X","dephase","reprepare_zero"],
    individual_link_NPT_iff_t_greater_than=.25,
    two_link_identity_process_NPT_iff_t_greater_than=.5,
    entanglement_witness="Normalized Choi singlet fraction F=Tr(Phi J)>1/3 excludes entanglement-breaking qutrit channel, with a prepared maximally entangled ancilla reference and trusted tomography.",
    per_link_analytical_F="(1+8t)/9",
    two_link_identity_F="(1+8*t*t)/9",
    link_analytical_negativity="max(0,(4t-1)/3)",
    two_link_analytical_negativity="max(0,(4*t*t-1)/3)",
    no_classical_memory_witness_from_only_unconditional_populations=True,
    Markovian_quantum_process_tensor_can_be_entangled_across_temporal_link=True,
    temporal_NPT_not_equal_nonMarkovian_memory=True,
    t_sweep_with_four_interventions=rows,
    two_link_heralded_erasure_controls=erasures,
    classical_memory_scope="A trusted entangled reference tests whether a channel is entanglement-breaking. A hidden memory model allowing arbitrary quantum ancilla, postselection or measurement-context dependence is not excluded. Conversely 2025/26 literature cautions that entanglement-breaking temporal processes can retain nonclassical temporal correlations in other tests.",
    physical_limitation="No explicit single photon experiment constructed: preparing a qutrit entangled reference, carrying reference through three times, closing loss loopholes and process-tensor tomography require independent experimental engineering. This is a memoryless Markov comb toy, not retrocausality.",
    prior_art="Process-tensor formalism Pollock et al PRL2018; quantum non-Markovianity; recent Di Pietra et al accepted PRL 21 Oct2026 temporal witnesses; Vieira Ku Budroni 2025 entanglement-breaking temporal processes.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],"t=.45 links entangled but end EB",rows[3]["both_links_NPT_but_end_to_end_identity_entanglement_broken"],flush=True)
 return result
if __name__=="__main__":main()
