#!/usr/bin/env python3
"""Continuous 15-parameter local optimization of one ququart measurement basis.

Use the published Witting A5 operator/440 E8 codebook and prior seeded
320-Haar basis search. Parameterize SU4 around the best sampled basis
with exp(-i H), where H spans 15 independent traceless Hermitian matrices.
Optimize mutual information of uniform 440-root labels by L-BFGS-B,
two epsilons, plus independent perturbation restart. Save actual 4x4
basis, exact unitarity/normalization and compare Holevo bound.
Converged local candidates are NOT a proof of global optimal POVM,
and single basis has only 4 outcomes (nonprojective POVM might beat).
"""
from __future__ import annotations
import math,json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261104_ququart_povm_local_unitary_optimizer.json"
def entropy_classical(P):
 P=np.maximum(P,1e-200)
 Q=P.mean(axis=0)
 return float(np.sum(P*np.log2(P/Q))/len(P))
def basis_su4():
 out=[]
 for i in range(4):
  for j in range(i+1,4):
   a=np.zeros((4,4),complex);a[i,j]=a[j,i]=1/math.sqrt(2)
   b=np.zeros((4,4),complex);b[i,j]=-1j/math.sqrt(2);b[j,i]=1j/math.sqrt(2)
   out.extend((a,b))
 for j in range(1,4):
  diag=np.r_[[1.]*j,[-float(j)],[0.]*(3-j)]
  out.append(np.diag(diag)/math.sqrt(j*(j+1)))
 assert len(out)==15
 assert max(abs(np.trace(x)) for x in out)<1e-12
 return np.array(out)
def main():
 co=json.loads((ROOT/"data/toe_20261104_two_e8_witting_basis_information_search.json").read_text())
 ca=json.loads((ROOT/"data/toe_20261104_two_e8_witting_holevo_capacity_scan.json").read_text())
 src=json.loads((ROOT/"data/toe_20261104_witting_operator_dark_spectral_A5_duality.json").read_text())
 root=json.loads((ROOT/"data/toe_20261104_two_e8_root_to_witting_density_codebook.json").read_text())
 B=basis_su4()
 O=np.array(src["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_real"])+1j*np.array(
 src["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_imag"])
 theta0=np.array(root["eight_real_parameters_for_440_states"])
 rng=np.random.default_rng(20261104)
 result=[]
 for rec in co["epsilon_scan"]:
  eps=rec["epsilon"]
  theta=theta0*(eps/.1)
  rho=np.eye(4)[None,:,:]/4+np.einsum("ij,jab->iab",theta,O)
  V0=(np.array(rec["best_sampled_Haar_unitary_rows_real"])+1j*np.array(rec["best_sampled_Haar_unitary_rows_imag"])).T
  assert np.max(abs(V0.conj().T@V0-np.eye(4)))<1e-12
  def calc(x):
   V=expm(-1j*np.einsum("i,ijk->jk",x,B))@V0
   P=np.einsum("ai,nab,bi->ni",V.conj(),rho,V).real
   assert min(P.min(),1)>-1e-9
   return entropy_classical(P)
  old=calc(np.zeros(15))
  assert abs(old-rec["seeded_Haar_best_information_bits"])<1e-10
  runs=[]
  for run in range(2):
   x0=np.zeros(15) if run==0 else rng.normal(scale=.15,size=15)
   opt=minimize(lambda x:-calc(x),x0,method="L-BFGS-B",
    bounds=[(-1.,1.)]*15,
    options={"maxiter":50,"ftol":1e-12,"gtol":1e-7,"maxls":20})
   xx=opt.x
   V=expm(-1j*np.einsum("i,ijk->jk",xx,B))@V0
   score=calc(xx)
   assert abs(score+opt.fun)<1e-9
   assert np.max(abs(V.conj().T@V-np.eye(4)))<1e-10
   runs.append(dict(seed_run=run,information_bits=score,
     iterations=int(opt.nit),function_evaluations=int(opt.nfev),
     optimizer_message=str(opt.message),bounded_local_optimizer_success=bool(opt.success),
     quaternion_operator_error_max=float(np.max(abs(V.conj().T@V-np.eye(4)))),
     physical_ququart_basis_columns_real=V.real.tolist(),
     physical_ququart_basis_columns_imag=V.imag.tolist(),
     local_Su4_exp_15_params=xx.tolist()))
  winner=max(runs,key=lambda z:z["information_bits"])
  assert winner["information_bits"]>=old-1e-9
  hol=next(x["holevo_bound_bits_per_ququart"] for x in ca["epsilon_scan"] if x["epsilon"]==eps)
  assert winner["information_bits"]<hol
  result.append(dict(epsilon=eps,
   original_Witting_40POVM_information_bits=rec["uniform_Witting40_POVM_information_bits"],
   seeded_320_Haar_sampled_best_information_bits=old,
   optimized_best_single_projective_basis_information_bits=winner["information_bits"],
   optimized_basis_improvement_over_Witting_ratio=winner["information_bits"]/rec["uniform_Witting40_POVM_information_bits"],
   ensemble_Holevo_upper_bound_bits=hol,
   best_single_basis_fraction_of_Holevo_upper_bound=winner["information_bits"]/hol,
   local_restart_optimization_results=runs,
   global_optimal_POVM_claimed=False))
 outcome=dict(status="PASS_CONTINUOUS_15_PARAM_SU4_PROJECTIVE_READOUT_IMPROVEMENT",
  root_labels=440,source_traceless_hermitian_basis_dimension=15,
  source_Hilbert_dimension=4,
  epsilon_results=result,
  prior_art="SU4 unitary optimization, Holevo upper bound and E8-Witting rays known. This is an empirical local improvement on the specific 440-state mixed codebook.",
  boundary="Only 2 local restarts around a preselected 320 Haar sample. Not global, not an optimized arbitrary nonprojective POVM, no hardware experiment nor TOE.")
 OUT.write_text(json.dumps(outcome,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(outcome["status"],[(x["epsilon"],x["seeded_320_Haar_sampled_best_information_bits"],x["optimized_best_single_projective_basis_information_bits"]) for x in result],flush=True)
 return outcome
if __name__=="__main__":main()
