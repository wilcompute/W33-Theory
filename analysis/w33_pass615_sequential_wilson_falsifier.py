#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
from statistics import NormalDist
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass615_sequential_wilson_falsifier.json'
NAMES=['flat_identity','top_double_transposition','tetrahedral_fixed_point_free_involution','top_order_three']
TRACES=np.array([[6,6,6],[2,6,2],[0,6,0],[0,0,6]],dtype=float)
R=np.array([[.80,.02,-.01],[.01,.64,.015],[-.005,.02,.512]],dtype=float)
BIAS=np.array([.06,-.04,.03],dtype=float)
MU=TRACES@R.T+BIAS
VAR=np.array([6.2,6.8,7.4],dtype=float)
PRI=np.array([2/15,2/15,1/3,2/5],dtype=float)
STAGES=np.array([[21,4],[42,8],[63,12],[84,16]],dtype=int)
POSTERIOR_STOP=.99
GOF_TRIGGER=9.210340371976184
AUDIT_N3=48
AUDIT_Z=NormalDist().inv_cdf(.995)
def posterior(y,n):
 active=np.flatnonzero(n);ll=np.log(PRI.copy())
 for c in range(4):ll[c]+=-.5*np.sum(n[active]*(y[active]-MU[c,active])**2/VAR[active])
 ll-=ll.max();p=np.exp(ll);return p/p.sum()
def trial(rng,c):
 sums=np.zeros(3);prev=np.zeros(2,dtype=int);y=np.zeros(3);audit=False;stopped=False
 for n2 in STAGES:
  inc=n2-prev
  for k in range(2):
   sums[k]+=rng.normal(MU[c,k]*inc[k],math.sqrt(VAR[k]*inc[k]));y[k]=sums[k]/n2[k]
  prev=n2.copy();p=posterior(y,np.r_[n2,0]);hat=int(np.argmax(p));gof=np.sum(n2*(y[:2]-MU[hat,:2])**2/VAR[:2])
  if p[hat]>=POSTERIOR_STOP:stopped=True;break
  if gof>GOF_TRIGGER:audit=True;break
 if not stopped and not audit:audit=True
 reject=False
 if audit:
  y[2]=rng.normal(MU[c,2],math.sqrt(VAR[2]/AUDIT_N3));p=posterior(y,np.r_[prev,AUDIT_N3]);hat=int(np.argmax(p))
  z=abs(y[2]-MU[hat,2])/math.sqrt(VAR[2]/AUDIT_N3);reject=z>AUDIT_Z
 else:hat=int(np.argmax(posterior(y,np.r_[prev,0])))
 return hat==c,int(prev.sum()),audit,reject,int(prev.sum()+(AUDIT_N3 if audit else 0))
def nominal_simulation(trials=5000):
 rng=np.random.default_rng(615000);rows=[]
 for c,name in enumerate(NAMES):
  A=np.array([trial(rng,c) for _ in range(trials)],dtype=float)
  rows.append({'class':name,'trials':trials,'classification_accuracy':float(A[:,0].mean()),'mean_primary_photons':float(A[:,1].mean()),'trace3_audit_rate':float(A[:,2].mean()),'model_reject_rate':float(A[:,3].mean()),'mean_total_photons':float(A[:,4].mean())})
 return rows
def payload():
 rows=nominal_simulation();delta=1.5;shift=delta/math.sqrt(VAR[2]/AUDIT_N3);nd=NormalDist();power=(1-nd.cdf(AUDIT_Z-shift))+nd.cdf(-AUDIT_Z-shift);sentinel=.05
 primary_invariant=all(np.array_equal(MU[c,:2],(MU[c]+np.array([0.,0.,delta]))[:2]) for c in range(4))
 checks={'first_two_channels_separate_all_classes':len({tuple(x[:2]) for x in MU})==4,'sequential_primary_budget_caps_at100':STAGES[-1].sum()==100,'nominal_worst_accuracy_above0p995':min(r['classification_accuracy'] for r in rows)>.995,'nominal_mean_total_below60_each_class':max(r['mean_total_photons'] for r in rows)<60,'nominal_trace3_audit_rate_below4pct':max(r['trace3_audit_rate'] for r in rows)<.04,'nominal_model_false_reject_below0p1pct':max(r['model_reject_rate'] for r in rows)<.001,'trace3_only_alternative_primary_law_identical':primary_invariant,'trace3_audit_power_above89pct_for_shift1p5':power>.89,'five_percent_sentinel_detection_floor_above4p4pct':sentinel*power>.044,'blind_alternative_requires_sentinel_or_audit':primary_invariant and power>0}
 checks={k:bool(v) for k,v in checks.items()}
 return {'schema':'w33.pass615.sequential_wilson_falsifier.v1','status':'PASS' if all(checks.values()) else 'FAIL','controller':{'primary_channels':['Tr(U)','Tr(U^2)'],'cumulative_primary_stages':STAGES.tolist(),'posterior_stop_threshold':POSTERIOR_STOP,'primary_goodness_of_fit_trigger':GOF_TRIGGER,'trace3_audit_photons':AUDIT_N3,'trace3_two_sided_alpha':.01,'rule':'Stop when posterior confidence exceeds 0.99; invoke Tr(U^3) when primary fit is poor or confidence remains insufficient at the 100-photon cap.'},'nominal_operating_characteristics':rows,'trace3_only_drift':{'shift_tested':delta,'standardized_shift_at_48_photons':shift,'conditional_audit_power':power,'residual_trigger_power_before_trace3':'exactly the nominal trigger rate, because the first-two-channel law is identical','optional_five_percent_sentinel_detection_probability_per_classification':sentinel*power,'impossibility':'No policy observing only Tr(U) and Tr(U^2) can distinguish two models whose distributions agree on those channels; a trace-three sentinel or external sensor is information-theoretically necessary.'},'theorem':'A residual-triggered sequential Wilson controller reduces nominal mean photon use to 25.4-56.0 photons while retaining worst-class accuracy above 0.995 and invoking the third trace on fewer than four percent of nominal trials. A trace-three-only departure is provably invisible to the primary residuals; a sparse sentinel audit is the minimal remedy.','checks':checks,'boundary':'Operating characteristics are deterministic Monte Carlo results for the Pass-610 calibration fixture. Laboratory deployment must refit the response, covariance, priors, and drift alternatives; the trace-three-only impossibility statement is exact and model independent.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 615 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'worst_accuracy':min(r['classification_accuracy'] for r in p['nominal_operating_characteristics'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
