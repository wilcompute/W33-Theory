"""TOE48: invertible general readout confusion, rigorous union-bound CI,
and outcome-dependent loss non-identifiability; no physical hardware claim."""
import runpy,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
a=runpy.run_path(str(R/"analysis/w33_20261010_toe47_dark_fisher_rank.py"))
rng=np.random.default_rng(48001)
rho=a["rho"];M=a["Pminus"];q=a["q"];W=a["W"];pjs=a["proj"];chosen=a["chosen"];lines=a["lines"]
eps=.08; n=1200; trials=150; failure=.05
dimen=9
# independent column-stochastic nonuniform 9x9 confusion, one per setting
bases=[];betas=[]
for j,l in enumerate(chosen):
 ids=list(lines[l]);proj=pjs[j*9:(j+1)*9]
 p=np.einsum("ab,tba->t",rho,proj).real
 base=rng.uniform(.02,.08,(9,9))
 base/=base.sum(axis=0)
 C=.9*np.eye(9)+.1*base
 assert np.allclose(C.sum(axis=0),1)
 vals=np.array([[np.trace(proj[t]@W[x]) for t in range(9)] for x in ids])
 inverse=np.linalg.inv(C)
 weight=vals@inverse
 assert np.max(abs(weight@C-vals))<1e-12
 assert np.max(abs((C@p)@weight.T-np.einsum("ab,pba->p",rho,W)[ids]))<1e-12
 bases.append((ids,C@p,weight))
 betas.append(float(np.max(abs(weight))))
B=max(betas)
def calc():
 z=np.zeros((4,40),complex)
 for j,(ids,prob,weight) in enumerate(bases):
  for k in range(4):
   cnt=rng.multinomial(n,prob)
   z[k,ids]=weight@cnt/n
 qab=2*np.real(z[0]*z[1].conj())
 qcd=2*np.real(z[2]*z[3].conj())
 return float((2/135)*np.dot(M@qab,M@qcd))
truth=float((2/135)*np.linalg.norm(M@q)**2)
results=np.array([calc() for _ in range(trials)])
# Hoeffding real & imaginary of each 4x40 corrected complex mean:
# each in [-B,B], Pr(|Re error|>t) <= 2exp(-n t²/(2B²)).
# Union over 320 component choices: failure <= 640 exp(-n t²/2B²).
t=B*np.sqrt(2*np.log(640/failure)/n)
e=np.sqrt(2)*t
dq=4*e+2*e*e
# |q_p|<=2 and sum_p q_p <=8 for any physical two-qutrit state,
# so ||q||_2 <=4. 4 batches yield ||dq|| <=sqrt40*dq.
rad=(2/135)*(8*np.sqrt(40)*dq+40*dq*dq)
coverage=float(np.mean(abs(results-truth)<=rad))
assert coverage>=.95
assert abs(results.mean()-truth)<5*results.std(ddof=1)/np.sqrt(trials)
# *Physical* nonidentifiability from unknown outcome-dependent loss:
# given r_j=1/9 observed surviving, two distinct physical nine-outcome
# probability vectors p0 and p1 produce the same conditional observations.
r=np.ones(9)/9
eta0=np.full(9,.8)
eta1=np.linspace(.68,.92,9)
p0=r/eta0;p0/=p0.sum()
p1=r/eta1;p1/=p1.sum()
assert np.max(abs(eta0*p0/(eta0@p0)-eta1*p1/(eta1@p1)))<1e-15
purity0=float(p0@p0);purity1=float(p1@p1)
assert abs(purity0-purity1)>1e-5
# both diag in same orthogonal stabilizer basis -> bona fide quantum states.
proj=pjs[:9]
r0=np.einsum("i,ijk->jk",p0,proj)
r1=np.einsum("i,ijk->jk",p1,proj)
assert abs(np.trace(r0@r0).real-purity0)<1e-12
assert abs(np.trace(r1@r1).real-purity1)<1e-12
out={"status":"TOE48_GENERAL_READOUT_CI_AND_MNAR_IDENTIFIABILITY_FIREWALL",
"general_confusion":{"settings":10,"outcomes":9,"max_inverse_corrected_eigenvalue_magnitude":B,
"total_attempted_copies_per_trial":4*10*n,"independent_blocks":4,
"shots_each_setting_each_block":n,"random_trials":trials,"true_gap":truth,
"mean_estimated_gap":float(results.mean()),"sd_estimated_gap":float(results.std(ddof=1)),
"confidence_target":.95,"a_priori_uniform_Hoeffding_radius":float(rad),
"empirical_coverage":coverage,
"proof":"For 160 complex means=320 real bounded components, union Hoeffding: Pr(max |component error|> B sqrt(2 ln(640/alpha)/n))<=alpha. If |mu error|<=e=sqrt(2)t, power-pair error<=4e+2e². Since ||q||<=4, G=(2/135)<Pq,Pq>, the gap error bounded by (2/135)(8sqrt40 dq +40 dq²). Readout matrices known, invertible, and sampling independent."},
"MNAR":{"outcome_efficiencies_case0":eta0.tolist(),"outcome_efficiencies_case1":eta1.tolist(),
"same_postselected_outcomes":r.tolist(),
"different_state_purity0":purity0,"different_state_purity1":purity1,
"purity_difference":purity1-purity0,"identical_postselection_residual":float(max(abs(eta0*p0/(eta0@p0)-eta1*p1/(eta1@p1))))},
"conclusion":"General KNOWN full-rank readout can be corrected with a finite-sample (loose) a priori interval. Outcome-dependent UNKNOWN detector efficiencies make even nine-basis postselected probabilities non-identifying: different physical quantum density matrices have identical survivors. No sample size repairs this unless efficiencies are independently bounded/calibrated.",
"physical_boundary":"Synthetic confusion matrices, one basis MNAR witness, no calibrated photonic apparatus, no unknown confusion confidence procedure. The Hoeffding interval may be much wider than the physical gap range and does not imply useful power."}
(R/"data/w33_20261010_toe48_spam_identifiability.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"true":truth,"mean":out["general_confusion"]["mean_estimated_gap"],"radius":rad,"purity_diff":purity1-purity0}))
