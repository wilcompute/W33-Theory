"""TOE47 extra front: SINGLE 40-outcome even-Weil cusp-POVM purity assay.

A 40 ray complex projective 2-design in d=5 yields
sum_r p_r**2 = (1+Tr(rho**2))/48 for E_r=P_r/8.
"""
from pathlib import Path
import json,runpy
import numpy as np
R=Path(__file__).resolve().parents[1]
z=runpy.run_path(str(R/"analysis/w33_20261010_toe47_cusp_even5_ic_povm.py"))
P=z["projectors"];rng=np.random.default_rng(47007)
O=R/"data/w33_20261010_toe47_even5_single_povm_purity.json"
def pure(a):
 a=a/np.linalg.norm(a)
 return np.outer(a,a.conj())
rho_pure=pure(rng.normal(size=5)+1j*rng.normal(size=5))
rho_mix=np.eye(5)/5
eps=.06
pair_count=6500
runs=1200
cases={}
for label,rho in [("pure",rho_pure),("maximally_mixed",rho_mix)]:
 prob=np.einsum("ab,pba->p",rho,P).real/8
 assert abs(prob.sum()-1)<1e-12
 C=float(prob@prob);purity=float(np.trace(rho@rho).real)
 assert abs(48*C-1-purity)<1e-12
 # Uniform 40-detector outcome confusion, eps<1, permutation-invariant.
 observed=(1-eps)*prob+eps/40
 Cobs=float(observed@observed)
 Cest=(Cobs-(1-(1-eps)**2)/40)/(1-eps)**2
 assert abs(Cest-C)<1e-12
 counts=rng.binomial(pair_count,Cobs,size=runs)
 est=48*((counts/pair_count-(1-(1-eps)**2)/40)/(1-eps)**2)-1
 pred_se=float(np.sqrt(48**2*Cobs*(1-Cobs)/(pair_count*(1-eps)**4)))
 mean=float(est.mean())
 assert abs(mean-purity)<5*pred_se/np.sqrt(runs),(mean,purity,pred_se)
 cases[label]={"true_purity":purity,"exact_collision":C,"noisy_collision":Cobs,
"calibrated_estimate_mean":mean,"empirical_standard_deviation":float(est.std(ddof=1)),
"predicted_single_trial_se":pred_se,"total_copies_per_trial":2*pair_count}
out={"status":"ONE_FIXED_40_OUTCOME_IC_POVM_ESTIMATES_D5_PURITY",
"single_POVM":"40 outcomes E_r=P_r/8 on 5D even Weil Hilbert space; sum E_r=I5",
"exact_identity":"sum_r Pr(outcome=r)^2=(1+Tr(rho^2))/48",
"unbiased_pair_estimator":"P_hat=48*(1/m)*sum_{j=1}^m indicator(Y_j=Yprime_j)-1; each pair uses two independent copies",
"trusted_uniform_confusion":"observed p_r=(1-eps)p_r+eps/40, C_obs=(1-eps)^2 C +(1-(1-eps)^2)/40; invert exactly if eps is known",
"readout_eps":eps,"pairs_per_trial":pair_count,"simulated_repetitions":runs,
"cases":cases,
"physical_boundary":"40-outcome POVM is mathematically defined in Hilbert dimension 5. No optical circuit implementing it has been compiled. It is not a purity estimator on the original dimension-9 two-qutrit state unless an additional physical encoding is specified. Shot variance can be large and needs comparison against other measurements; uniform known detector error is idealized."
}
O.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"cases":cases}),flush=True)
