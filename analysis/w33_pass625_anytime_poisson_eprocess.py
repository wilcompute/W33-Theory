#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from pathlib import Path
import numpy as np
from scipy.stats import binom,poisson
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass625_anytime_poisson_eprocess.json'
P=np.array([[0.9472727272727274,0.8590909090909091,0.7901818181818181],[0.66,0.85,0.6058181818181818],[0.5163636363636364,0.8454545454545455,0.5136363636363637],[0.5,0.5045454545454545,0.782]],dtype=float)
NAMES=['flat_identity','top_double_transposition','tetrahedral_fixed_point_free_involution','top_order_three']
ALPHA=.01;DELTA=.12;HORIZON=10;BUDGET=340

def logsumexp(a,b):
 m=np.maximum(a,b);return m+np.log(np.exp(a-m)+np.exp(b-m))
def crossing_masks(n,p0,K=HORIZON):
 pp=min(.999,p0+DELTA);pm=max(.001,p0-DELTA);out=[]
 for m in range(K+1):
  N=m*n;s=np.arange(N+1)
  if N==0:out.append(np.array([False]));continue
  lp=s*np.log(pp/p0)+(N-s)*np.log((1-pp)/(1-p0))
  lm=s*np.log(pm/p0)+(N-s)*np.log((1-pm)/(1-p0))
  out.append(logsumexp(lp,lm)-math.log(2)>=math.log(1/ALPHA))
 return out
def crossing_probability(q,n,p0,p,K=HORIZON):
 hit=0.;states=[None]*(K+1);states[0]=np.array([1.]);pmf=binom.pmf(np.arange(n+1),n,p);masks=crossing_masks(n,p0,K)
 for t in range(K):
  new=[None]*(K+1)
  for m in range(t+1):
   a=states[m]
   if a is None:continue
   stay=a*(1-q);new[m]=stay if new[m] is None else new[m]+stay
   y=np.convolve(a,pmf)*q;mask=masks[m+1];hit+=float(y[mask].sum());y[mask]=0
   new[m+1]=y if new[m+1] is None else new[m+1]+y
  states=new
 return hit
def optimize():
 rows=[]
 for n in (24,32,40,48,56,64,72,80,96,112,128):
  for qi in range(1,21):
   q=qi/20
   if HORIZON*q*n>BUDGET+1e-12:continue
   vals=[]
   for p0 in P[:,2]:
    vals.extend([crossing_probability(q,n,p0,max(.001,p0-DELTA)),crossing_probability(q,n,p0,min(.999,p0+DELTA))])
   rows.append({'q':q,'audit_photons':n,'expected_ten_run_audit_budget':HORIZON*q*n,'worst_ten_run_power':min(vals),'powers':vals})
 rows.sort(key=lambda r:(r['worst_ten_run_power'],-r['expected_ten_run_audit_budget']),reverse=True);return rows

def bern_lr(s,n,p_alt,p0):return (p_alt/p0)**s*((1-p_alt)/(1-p0))**(n-s)
def poisson_gamma_e(c,t,lam0,a=.5,b=.5):
 return (b**a/math.gamma(a))*math.gamma(c+a)/(b+t)**(c+a)*math.exp(lam0*t)/(lam0**c)
def payload():
 grid=optimize();win=grid[0];q=win['q'];n=win['audit_photons']
 five=[];ten=[];null=[]
 for p0 in P[:,2]:
  five.extend([crossing_probability(q,n,p0,max(.001,p0-DELTA),5),crossing_probability(q,n,p0,min(.999,p0+DELTA),5)])
  ten.extend([crossing_probability(q,n,p0,max(.001,p0-DELTA),10),crossing_probability(q,n,p0,min(.999,p0+DELTA),10)])
  null.append(crossing_probability(q,n,p0,p0,10))
 lam0=3.7;t=2.0;cut=120;expect=sum(poisson.pmf(c,lam0*t)*poisson_gamma_e(c,t,lam0) for c in range(cut+1))
 pair_kl={}
 for i,j in itertools.combinations(range(4),2):
  vals=[]
  for k in range(2):
   p,q0=P[i,k],P[j,k];vals.append(p*math.log(p/q0)+(1-p)*math.log((1-p)/(1-q0)))
  pair_kl[f'{NAMES[i]}|{NAMES[j]}']=vals
 checks={
  'paired_probabilities_strictly_between0_1':bool(np.all((P>0)&(P<1))),
  'primary_two_channels_separate_classes':len({tuple(x[:2]) for x in P})==4,
  'pairwise_LR_unit_expectation_example':abs(sum(binom.pmf(s,20,P[0,0])*bern_lr(s,20,P[1,0],P[0,0]) for s in range(21))-1)<1e-12,
  'poisson_gamma_mixture_unit_expectation':abs(expect-1)<2e-10,
  'finite_grid_winner_0p85_40':q==.85 and n==40,
  'winner_expected_budget340':abs(HORIZON*q*n-340)<1e-12,
  'ten_run_worst_power_above0p872':min(ten)>.872,
  'five_run_worst_power_above0p463':min(five)>.463,
  'actual_null_crossing_below0p0038':max(null)<.0038,
  'Ville_bound_is_0p01':ALPHA==.01,
  'all_primary_pair_KLs_positive':all(min(v)>0 for v in pair_kl.values()),
  'no_Monte_Carlo_used':True,
 }
 checks={k:bool(v) for k,v in checks.items()}
 return {'schema':'w33.pass625.anytime_poisson_eprocess.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'anytime_classification':{'paired_Poisson_reduction':'Conditioning independent Poisson plus/minus counts on their total gives a binomial observation. Common multiplicative loss cancels from the plus probability.','pairwise_eprocess':'LR_{d/c}(t)=product over predictably selected channels of (p_d/p_c)^S ((1-p_d)/(1-p_c))^(N-S). Under class c this is a nonnegative martingale.','class_eprocess':'E_c=(1/3) sum_{d != c} LR_{d/c}.','confidence_sequence':'C_t={c:E_c(t)<1/alpha}. Ville guarantees that the true class remains in C_t for all t with probability at least 1-alpha. Stopping when C_t is a singleton therefore has anytime misclassification probability at most alpha.','alpha':ALPHA,'pairwise_KL_per_detected_photon':pair_kl},
  'loss_monitor':{'gamma_Poisson_eprocess':'For cumulative count C over exposure t under rate lambda0, E=(b^a/Gamma(a))*Gamma(C+a)/(b+t)^(C+a)*exp(lambda0*t)/lambda0^C. Inverting E<1/alpha gives an anytime confidence sequence for total intensity while the conditional binomial process handles class/phase.','default_prior':{'a':.5,'b':.5},'numerical_expectation_check':expect},
  'trace3_adversary':{'null_plus_probabilities':P[:,2].tolist(),'minimum_absolute_probability_shift':DELTA,'two_sided_eprocess':'One-half LR(p0+delta versus p0) plus one-half LR(p0-delta versus p0); predictable sentinel skipping preserves the e-process.','search_constraint':'expected trace-three audit exposure through ten classifications <=340','winner':{'sentinel_probability':q,'audit_photons':n,'expected_ten_run_audit_budget':HORIZON*q*n,'worst_detection_by5':min(five),'worst_detection_by10':min(ten),'per_direction_detection_by10':ten,'actual_null_crossing_by10':null},'top_grid':[{k:v for k,v in r.items() if k!='powers'} for r in grid[:10]]},
  'theorem':'An anytime-valid paired-Poisson controller is obtained by combining classwise likelihood-ratio e-processes with a Gamma-Poisson loss monitor and a two-sided trace-three sentinel e-process. At alpha=0.01, optional stopping and adaptive channel selection preserve error control. Under the declared |Delta p3|>=0.12 alternative and a ten-run expected audit budget of 340, the exact finite-state search selects q=0.85 and 40 audit photons, with worst detection probability above 0.872 by ten classifications and above 0.463 by five.',
  'checks':checks,'boundary':'The Ville guarantees are exact for the declared paired-Poisson/binomial model and remain valid under predictable adaptive sampling. The numerical power values are deterministic finite binomial sums for the stated shift family; misspecified detector dependence or adversaries with smaller shifts require a widened model.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 625 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'winner':p['trace3_adversary']['winner']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
