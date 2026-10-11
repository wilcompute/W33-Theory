"""TOE47: unbiased W33 quartic gap under trusted basis-dependent SPAM and loss.

Derives exact conditional covariance of independent 2-block Pauli-power
estimators and exact conditional variance of the four-block quartic gap.
Readout model: symmetric 9-outcome confusion; survival missing at random.
"""
from pathlib import Path
import json,runpy
import numpy as np
R=Path(__file__).resolve().parents[1]
a=runpy.run_path(str(R/"analysis/w33_20261010_toe47_dark_fisher_rank.py"))
W=a["W"];proj=a["proj"];chosen=a["chosen"];lines=a["lines"];M=a["Pminus"];rho=a["rho"]
mu=a["mu"];q=a["q"];k=2/135
O=R/"data/w33_20261010_toe47_spam_gap_exact_variance.json"
rng=np.random.default_rng(47001)
eps=np.linspace(.04,.16,10)
loss=np.linspace(.04,.28,10)
n_attempted=1000
trials=240
bases=[]
for j,l in enumerate(chosen):
 ids=list(lines[l]);P=proj[9*j:9*(j+1)]
 prob=np.einsum("ab,tba->t",rho,P).real; prob=prob/prob.sum()
 val=np.array([[np.trace(P[t]@W[p]) for t in range(9)] for p in ids])
 assert np.max(abs(abs(val)-1))<1e-12
 assert np.max(abs(prob@val.T-mu[ids]))<1e-12
 observed=(1-eps[j])*prob+eps[j]/9
 assert abs(observed.sum()-1)<1e-12
 alpha=1-eps[j]
 zz=val/alpha
 # correction centered so E observed(z)=mu
 assert np.max(abs(observed@zz.T-mu[ids]))<1e-12
 ES=zz@np.diag(observed)@zz.conj().T
 EP=zz@np.diag(observed)@zz.T
 single_C=ES-np.outer(mu[ids],mu[ids].conj())
 single_P=EP-np.outer(mu[ids],mu[ids])
 bases.append((ids,observed,zz,single_C,single_P))
def variance_conditional(counts):
 # qAB and qCD are real, independently constructed on four shot blocks
 covs=[]
 for b,c in ((0,1),(2,3)):
  CV=np.zeros((40,40))
  for j,(ids,prob,zz,C,P) in enumerate(bases):
   A=n_eval=[counts[b,j],counts[c,j]]
   c1,c2=C/counts[b,j],C/counts[c,j]
   p1,p2=P/counts[b,j],P/counts[c,j]
   x=mu[ids]
   Euu1=np.outer(x,x)+p1;Euu2=np.outer(x,x)+p2
   Eub1=np.outer(x,x.conj())+c1;Eub2=np.outer(x,x.conj())+c2
   mat=2*np.real(Euu1*Euu2.conj()+Eub1*Eub2.conj())-np.outer(q[ids],q[ids])
   CV[np.ix_(ids,ids)]=mat
  assert min(np.linalg.eigvalsh(CV))>-1e-10
  covs.append(CV)
 C1,C2=covs
 target=M@q
 return float(k*k*(np.trace(M@C1@M@C2)+target@C1@target+target@C2@target))
actual=[]; analytic=[]; naive=[]; min_valid_observed=10**9
for trial in range(trials):
 n=rng.binomial(n_attempted,(1-loss)**2,size=(4,10))
 assert n.min()>0
 min_valid_observed=min(min_valid_observed,int(n.min()))
 z=np.zeros((4,40),complex)
 for j,(ids,prob,val,C,P) in enumerate(bases):
  for b in range(4):
   counts=rng.multinomial(n[b,j],prob)
   z[b,ids]=val@counts/n[b,j]
 qab=2*np.real(z[0]*z[1].conj())
 qcd=2*np.real(z[2]*z[3].conj())
 actual.append(float(k*(M@qab)@(M@qcd)))
 analytic.append(variance_conditional(n))
 # uncalibrated control: raw measured eigenvalues
 raw=z.copy()
 for j,(ids,_,_,_,_) in enumerate(bases):raw[:,ids]*=1-eps[j]
 qu=2*np.real(raw[0]*raw[1].conj())
 qv=2*np.real(raw[2]*raw[3].conj())
 naive.append(float(k*(M@qu)@(M@qv)))
actual=np.array(actual);analytic=np.array(analytic);naive=np.array(naive)
true=float(k*np.linalg.norm(M@q)**2)
emp=float(np.var(actual,ddof=1))
pred=float(analytic.mean())
assert abs(actual.mean()-true)<5*np.sqrt(pred/trials),(actual.mean(),true,pred)
assert .75<emp/pred<1.3,(emp,pred)
# Hoeffding/McDiarmid finite-sample conservative bound conditional on valid
# counts: each outcome changes <=2/alpha n in 4 complex Pauli components;
# one group modifies at most 4 qAB entries by <=4/(alpha n) (or worse
# if partner corrected by 1/alpha, giving 4/(alpha² n));
# ||qCD||<=2 sqrt(40)/alpha_min^2 for observed corrected estimates;
# so per shot |delta g| <= 64 sqrt(40)/(135 alpha_min^4*n).
# All 40 setting/block groups have >= n_min valid n, leading
# sum c_i² <= 40*const²/n_min. This is very loose but certified.
alpha_min=float(min(1-eps));valid_min=min_valid_observed
cconst=64*np.sqrt(40)/(135*alpha_min**4)
bound_95=float(np.sqrt(.5*(40*cconst*cconst/valid_min)*np.log(40)))
out={"status":"EXACT_CONDITIONAL_QUARTIC_VARIANCE_WITH_MAR_LOSS_AND_BASIS_CONFUSION",
"shots":{"attempted_per_setting_per_block":n_attempted,"basis_count":10,"four_blocks":4,
"total_attempted_copies_per_trial":40*n_attempted,"replicates":trials},
"basis_readout_eps":eps.tolist(),"basis_per_copy_loss":loss.tolist(),
"rho_true_gap":true,"mean_calibrated_estimate":float(actual.mean()),
"empirical_variance":emp,"mean_exact_conditional_variance":pred,
"variance_ratio_empirical_to_exact":float(emp/pred),
"mean_uncalibrated_estimate":float(naive.mean()),
"corrected_estimator":"z_{b,p}=sample average of eigenvalue(Wp)/(1-eps_basis) among survived outputs; q_AB=2Re(zA conj zB); ghat=(2/135)(Pminus q_AB).(Pminus q_CD). Conditional on count array n>0: E ghat=g.",
"exact_covariance_formula":"For blocks a,b: ES_a,pq=mu_p conj(mu_q)+C_pq/n_a, EP_a,pq=mu_p mu_q+P_pq/n_a; Cov(q_ab,p,q_ab,q)=2Re(EP_a,pq conj(EP_b,pq)+ES_a,pq conj(ES_b,pq))-q_p q_q; off-base block covariance=0.",
"exact_variance_formula":"For C_ab and C_cd covariance matrices and t=Pminus q: Var(ghat|n)=(2/135)^2*(Tr(P C_ab P C_cd)+t^T(C_ab+C_cd)t).",
"very_conservative_distribution_free_95pct_radius":bound_95,
"minimum_observed_valid_pairs_per_setting_and_block":valid_min,
"warning":"The McDiarmid radius is conditional on the observed minimum valid count across the simulated trials and exact known confusion parameters, and is deliberately loose; NOT a uniform unconditional bound for arbitrary future data. Conditional exact moments assume TRUE probabilities/epsilon and survival MAR. This is an oracle variance benchmark, not a plug-in confidence interval and does not handle uncertain calibration, outcome-dependent loss, drift, or coherently correlated detector errors.",
"prior_art":"MUB classical shadows, independent-sample quartic U-statistics and symmetric detector correction are established tools; the exact W33 -4 statistic and formula here are this producer's specialized implementation."}
O.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"true":true,"mean":out["mean_calibrated_estimate"],"var":emp,"exact_var":pred,"ratio":emp/pred,"uncal":out["mean_uncalibrated_estimate"]}),flush=True)
