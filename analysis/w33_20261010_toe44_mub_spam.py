"""TOE44: calibrated MUB purity estimation with basis-dependent readout and loss.

The model is an explicit 10-setting two-copy collision assay, with each
setting's collision probability from a stabilized pure input versus
unbiased depolarization. Basis-dependent symmetric 9-outcome readout
confusion and independent pairwise loss are injected; the assay's
conditional unbiasedness and confidence coverage are tested.
"""
import json,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1]
O=R/"data/w33_20261010_toe44_mub_spam.json"
rng=np.random.default_rng(44002)
# Construct actual W33 symplectic line spread CONTAINING the computational
# (Z1,Z2) commuting basis, avoiding an unverified MUB geometry assumption.
import itertools
canon=lambda v:min(v,tuple(-x%3 for x in v))
pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
ix={v:j for j,v in enumerate(pts)}
sp=lambda u,v:(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
lines=set()
for i,u in enumerate(pts):
 for v in pts[i+1:]:
  if sp(u,v):continue
  L=tuple(sorted({ix[canon(tuple((a*u[j]+b*v[j])%3 for j in range(4)))]
     for a,b in itertools.product(range(3),repeat=2) if a or b}))
  lines.add(L)
lines=sorted(lines);assert len(lines)==40
zline=tuple(i for i,p in enumerate(pts) if p[0]==0 and p[1]==0)
assert len(zline)==4 and zline in lines
masks=[sum(1<<i for i in L) for L in lines]
bypt={p:[i for i,L in enumerate(lines) if p in L] for p in range(40)}
def extend(mask,chosen):
 if mask==(1<<40)-1:return chosen
 for p in range(40):
  if not mask>>p&1:break
 for k in bypt[p]:
  if masks[k]&mask:continue
  ans=extend(mask|masks[k],chosen+[k])
  if ans:return ans
 return None
spread=extend(masks[lines.index(zline)],[lines.index(zline)])
assert spread and len(spread)==10 and sorted(i for j in spread for i in lines[j])==list(range(40))
# A spread of 10 MUBs, one stabilizer basis contains |00>, rest unbiased.
# A state rho=eta|00><00|+(1-eta)I/9 gives basis collision:
# in eigenbasis eta² + (1-eta²)/9; other 9 bases exactly 1/9.
# These are exact without measuring the 81 basis projectors explicitly.
eta=.62
c_true=np.r_[eta*eta+(1-eta*eta)/9,np.full(9,1/9)]
p_true=eta*eta+(1-eta*eta)/9
assert abs(sum(c_true)-1-p_true)<1e-12
eps=np.linspace(.05,.135,10)
loss=np.linspace(.04,.24,10)
alpha=1-eps
c_obs=alpha**2*c_true+(1-alpha**2)/9
m=900
reps=2400
# Each prepared copy survives with probability 1-loss. Only complete
# two-copy pairs contribute. With independent copies this is square.
n=rng.binomial(m,(1-loss)**2,size=(reps,10))
assert n.min()>0
success=rng.binomial(n,c_obs)
obs=success/n
cal=(obs-(1-alpha**2)/9)/alpha**2
est=cal.sum(axis=1)-1
uncal=obs.sum(axis=1)-1
# Pre-shot standard errors conditional on n. Use exact binomial variance.
se2=np.sum(c_obs*(1-c_obs)/(n*alpha**4),axis=1)
t=(est-p_true)/np.sqrt(se2)
coverage=float(np.mean(np.abs(t)<=1.96))
mean=float(est.mean())
bias_uncal=float(uncal.mean()-p_true)
# A wrong single eps calibration (not actual basis eps values) biases.
wrong_alpha=1-np.mean(eps)
wrong=(obs-(1-wrong_alpha**2)/9)/wrong_alpha**2
wrong_bias=float(wrong.sum(axis=1).mean()-1-p_true)
assert abs(mean-p_true)<.007,(mean,p_true)
assert .925<coverage<.975,coverage
assert abs(bias_uncal)>.01, bias_uncal
# Basis-dependent loss selection independent of outcome is critical.
out={"status":"CALIBRATED_W33_TEN_MUB_SPAM_STRESS",
"model":"ten exact W33 MUB bases; verified W33 isotropic spread contains the Z1,Z2 computational stabilizer basis; rho=eta |00><00|+(1-eta) I/9",
"symplectic_W33_line_count":len(lines),"verified_spread_line_indices":spread,
"verified_zline_point_indices":list(zline),
"eta":eta,"true_global_purity":p_true,
"basis_collision_true":c_true.tolist(),"basis_readout_epsilon":eps.tolist(),
"basis_loss_per_copy":loss.tolist(),"attempted_independent_copy_pairs_per_basis":m,
"number_of_monte_carlo_replicates":reps,
"mean_effective_pairs_per_basis":np.mean(n,axis=0).tolist(),
"calibrated_mean_purity":mean,
"mean_calibrated_bias":float(mean-p_true),
"uncalibrated_bias":bias_uncal,
"single_wrong_epsilon_calibration_bias":wrong_bias,
"standard_error_mean":float(np.mean(np.sqrt(se2))),
"empirical_standard_deviation":float(np.std(est,ddof=1)),
"conditional_gaussian_95pct_coverage":coverage,
"estimator":"p_hat=sum_b ((collision_b- (1-(1-eps_b)^2)/9)/(1-eps_b)^2)-1",
"conditional_exact_variance":"sum_b c_obs_b*(1-c_obs_b)/(n_valid_pairs_b*(1-eps_b)^4)",
"control_limit":"Assumes all ten stabilizer bases are ideal, readout errors basis-specific but symmetric independent, loss MAR (independent of actual measurement value), calibration eps exact, independent state preparations, no time drift.",
"warning":"Not a proof of laboratory performance; outcome-dependent detector loss, phase drift, basis misalignment, non-symmetric confusion matrices, adversarial correlations can invalidate the estimator."}
O.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:out[k] for k in ("status","true_global_purity","calibrated_mean_purity","uncalibrated_bias","conditional_gaussian_95pct_coverage","standard_error_mean")}))
