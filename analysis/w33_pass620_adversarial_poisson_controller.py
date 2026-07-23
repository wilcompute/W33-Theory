#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass620_adversarial_poisson_controller.json'
NAMES=['flat_identity','top_double_transposition','tetrahedral_fixed_point_free_involution','top_order_three']
TR=np.array([[6,6,6],[2,6,2],[0,6,0],[0,0,6]],float)
R=np.array([[.80,.02,-.01],[.01,.64,.015],[-.005,.02,.512]],float);BIAS=np.array([.06,-.04,.03]);MU=TR@R.T+BIAS
PRI=np.array([2/15,2/15,1/3,2/5]);BASE=.55;GAIN=.10;PN=(BASE+GAIN*MU)/(2*BASE);LOGP=np.log(PN);LOGQ=np.log(1-PN)
STAGES=np.array([[84,16],[168,32],[252,48],[336,64]],int);SCENARIOS=['nominal','common_loss','mode_loss','leakage','imbalance','trace3_drift','combined']
CANDIDATES=[(.40,64),(.45,64),(.50,64),(.55,64),(.60,64),(.70,48)]

def params(s,c):
 mu=MU[c].copy();loss=np.ones(3);imb=np.zeros(3)
 if s=='common_loss':loss[:]=.55
 elif s=='mode_loss':loss=np.array([.65,.48,.72])
 elif s=='leakage':mu=.84*mu+.16*np.mean(MU,axis=0)
 elif s=='imbalance':imb=np.array([.035,-.025,.03])
 elif s=='trace3_drift':mu[2]+=1.5
 elif s=='combined':loss=np.array([.62,.50,.70]);mu=.88*mu+.12*np.mean(MU,axis=0);imb=np.array([.025,-.02,.025]);mu[2]+=1.
 return np.clip((BASE+GAIN*mu)/(2*BASE)+imb,.02,.98),loss

def posterior(P,M,active):
 ll=np.log(PRI)+np.sum(P[list(active)]*LOGP[:,list(active)]+M[list(active)]*LOGQ[:,list(active)],axis=1);ll-=ll.max();q=np.exp(ll);return q/q.sum()
def deviance(P,M,c,active):
 d=0.
 for k in active:
  T=P[k]+M[k]
  if not T:continue
  ph=P[k]/T;p=PN[c,k]
  if P[k]:d+=2*P[k]*math.log(ph/p)
  if M[k]:d+=2*M[k]*math.log((1-ph)/(1-p))
 return d

def trial(rng,c,s,sentinel,n3):
 pt,loss=params(s,c);P=np.zeros(3,int);M=np.zeros(3,int);prev=np.zeros(2,int);audit=False
 for st in STAGES:
  inc=st-prev
  for k in (0,1):
   T=rng.poisson(2*BASE*inc[k]*loss[k]);z=rng.binomial(T,pt[k]);P[k]+=z;M[k]+=T-z
  prev=st.copy();po=posterior(P,M,(0,1));hat=int(po.argmax());g=deviance(P,M,hat,(0,1))
  if g>6.0:audit=True;break
  if po[hat]>=.99:
   audit=rng.random()<sentinel;break
 else:audit=True
 reject=False
 if audit:
  T=rng.poisson(2*BASE*n3*loss[2]);z=rng.binomial(T,pt[2]);P[2]=z;M[2]=T-z;po=posterior(P,M,(0,1,2));hat=int(po.argmax());g=deviance(P,M,hat,(0,1,2));zz=0 if not T else abs(z-T*PN[hat,2])/math.sqrt(T*PN[hat,2]*(1-PN[hat,2]));reject=g>11.345 or zz>2.576
 else:hat=int(posterior(P,M,(0,1)).argmax())
 correct=hat==c;safe=correct if s in ('nominal','common_loss','mode_loss') else (correct or reject)
 return correct,reject,audit,int(prev.sum()+(n3 if audit else 0)),int(P.sum()+M.sum()),safe

def evaluate(q,n3,trials,seed):
 rng=np.random.default_rng(seed);rows={}
 for s in SCENARIOS:
  A=[]
  for c in range(4):
   z=np.array([trial(rng,c,s,q,n3) for _ in range(trials)],float);A.append(z.mean(axis=0))
  rows[s]=np.array(A)
 nom=rows['nominal'];nontrace=min(rows['common_loss'][:,0].min(),rows['mode_loss'][:,0].min(),rows['leakage'][:,5].min(),rows['imbalance'][:,5].min(),rows['combined'][:,5].min());r=rows['trace3_drift'][:,1].min();batch=1-(1-r)**5
 return {'sentinel_probability':q,'audit_photons':n3,'mean_nominal_budget':float(nom[:,3].mean()),'nominal_worst_accuracy':float(nom[:,0].min()),'nominal_max_false_reject':float(nom[:,1].max()),'non_trace_adversarial_safe_floor':float(nontrace),'trace3_single_run_detection_floor':float(r),'trace3_five_run_detection_floor':float(batch),'minimax_score':float(min(nontrace,batch)),'rows':rows}

def payload():
 grid=[]
 for q,n in CANDIDATES:
  r=evaluate(q,n,500,620000+int(1000*q)+n);grid.append({k:v for k,v in r.items() if k!='rows'})
 feasible=[r for r in grid if r['mean_nominal_budget']<=205 and r['nominal_worst_accuracy']>=.98 and r['nominal_max_false_reject']<=.025];winner=max(feasible,key=lambda r:(r['minimax_score'],-r['mean_nominal_budget']))
 q=winner['sentinel_probability'];n=winner['audit_photons'];final=evaluate(q,n,3000,621000);rows=[]
 for s in SCENARIOS:
  for c,name in enumerate(NAMES):
   x=final['rows'][s][c];rows.append({'scenario':s,'class':name,'correct_rate':float(x[0]),'reject_rate':float(x[1]),'audit_rate':float(x[2]),'mean_exposure_budget':float(x[3]),'mean_detected_photons':float(x[4]),'safe_rate':float(x[5])})
 checks={
  'paired_Poisson_rates_positive':float(PN.min())>0 and float(PN.max())<1,
  'finite_grid_selects_0p55_64':q==.55 and n==64,
  'maximum_exposure_cap464':int(STAGES[-1].sum()+n)==464,
  'nominal_worst_accuracy_above0p985':final['nominal_worst_accuracy']>.985,
  'nominal_false_reject_below0p02':final['nominal_max_false_reject']<.02,
  'common_loss_correct_floor_above0p96':final['rows']['common_loss'][:,0].min()>.96,
  'mode_loss_correct_floor_above0p97':final['rows']['mode_loss'][:,0].min()>.97,
  'leakage_safe_floor_above0p97':final['rows']['leakage'][:,5].min()>.97,
  'imbalance_safe_floor_above0p93':final['rows']['imbalance'][:,5].min()>.93,
  'combined_safe_floor_above0p75':final['rows']['combined'][:,5].min()>.75,
  'trace3_single_run_detection_above0p23':final['trace3_single_run_detection_floor']>.23,
  'trace3_five_run_detection_above0p75':final['trace3_five_run_detection_floor']>.75,
 }
 checks={k:bool(v) for k,v in checks.items()}
 return {'schema':'w33.pass620.adversarial_poisson_controller.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'measurement_model':{'counts':'paired Poisson interferometer outputs; conditional plus-count is binomial and cancels common loss','nominal_plus_probabilities':PN.tolist(),'primary_stages':STAGES.tolist(),'posterior_stop':.99,'primary_deviance_audit_trigger':6.0,'audit_reject_thresholds':{'global_deviance':11.345,'trace3_z':2.576}},
  'minimax_search':{'candidates':[list(x) for x in CANDIDATES],'constraints':{'mean_nominal_budget_max':205,'nominal_accuracy_min':.98,'nominal_false_reject_max':.025},'objective':'maximize the minimum of the non-trace adversarial safe floor and the five-classification trace3-drift detection probability','grid_results':grid,'winner':[q,n]},
  'selected_controller':{'sentinel_probability':q,'trace3_audit_photons':n,'maximum_exposure_cap':int(STAGES[-1].sum()+n),'final_trials_per_class_scenario':3000,'summary':{k:v for k,v in final.items() if k!='rows'},'operating_rows':rows},
  'theorem':'In the paired-Poisson model with common loss, mode-dependent loss, leakage, detector imbalance, and trace-three-only drift, the finite minimax search selects a 55-percent sentinel probability and a 64-photon audit. It retains nominal worst-class accuracy above 0.985, has safe-rate floors above 0.93 for isolated leakage/imbalance attacks, and detects the otherwise invisible trace-three drift with probability above 0.75 within five classifications.',
  'checks':checks,'boundary':'The finite candidate grid and deterministic Monte Carlo certificate are exact as software outputs for the declared adversarial family, but they are not universal statistical guarantees. Device deployment must refit count rates and expand the adversary set.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 620 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'winner':p['minimax_search']['winner'],'score':p['selected_controller']['summary']['minimax_score']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
