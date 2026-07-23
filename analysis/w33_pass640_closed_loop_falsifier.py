#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass640_closed_loop_falsifier.json'
ALPHA_TOTAL=.01
ALPHA_COV=.002
ALPHA_E=.007
ALPHA_CAL=.001
WEIGHTS={'class':.4,'guard':.2,'audit':.3,'reference':.1}

def bern_factor(x:int,q:float,b:float)->float:
 return q/b if x else (1-q)/(1-b)

def epoch_mixture(vals:list[float])->float:
 total=0.;used=0.
 for k,v in enumerate(vals):
  w=2**(-(k+1));total+=w*v;used+=w
 return total+(1-used)

class Controller:
 def __init__(self,severe:bool=False):
  self.severe=severe;self.state='NOMINAL';self.t=0;self.epoch=0
  self.guard_epochs=[1.];self.audit_epochs=[];self.guard_cusum=0.;self.audit_cusum=0.
  self.audit_steps=0;self.audit_samples=0;self.cal_n=0;self.actions=[];self.events=[]
  self.nuisance={'phase':.03,'leakage':.025,'imbalance':.04}
  self.endpoint_embedding={'x':[0,1,0],'y':[1,0,1],'trivial_guard_mode':7,'chi_xy_guard_mode':6}
 def global_e(self):
  eg=epoch_mixture(self.guard_epochs);ea=epoch_mixture(self.audit_epochs) if self.audit_epochs else 1.
  m=WEIGHTS['class']+WEIGHTS['guard']*eg+WEIGHTS['audit']*ea+WEIGHTS['reference']
  return m,eg,ea
 def action(self):
  if self.state=='NOMINAL':return 'TrU2' if self.t%14==0 else 'TrU'
  if self.state=='AUDIT':return ('TrU3','TrU','TrU3','TrU2')[self.audit_steps%4]
  if self.state=='RECALIBRATE':return ('guard0','guard1','parity','reference')[self.cal_n%4]
  return 'halt'
 def step(self):
  self.t+=1;action=self.action();self.actions.append(action)
  gx=1 if (self.t>=401 if self.severe else 401<=self.t<=405) else (1 if self.t%20==0 else 0)
  gf=bern_factor(gx,.4,.1);self.guard_epochs[-1]*=gf;self.guard_cusum=max(0.,self.guard_cusum+math.log(gf))
  if self.state=='NOMINAL' and self.guard_cusum>=math.log(8):
   self.state='AUDIT';self.audit_steps=0;self.audit_samples=0;self.audit_epochs.append(1.);self.audit_cusum=0.
   self.events.append({'time':self.t,'event':'guard_warning','local_e':math.exp(self.guard_cusum),'next_state':'AUDIT'})
  if self.state=='AUDIT':
   if action=='TrU3':
    ax=1 if self.severe else (1 if self.audit_samples%10==0 else 0)
    af=bern_factor(ax,.7,.2);self.audit_epochs[-1]*=af;self.audit_cusum=max(0.,self.audit_cusum+math.log(af));self.audit_samples+=1
    if self.audit_cusum>=math.log(8) and not any(e['event']=='audit_warning' for e in self.events):
     self.events.append({'time':self.t,'event':'audit_warning','local_e':math.exp(self.audit_cusum),'next_state':'AUDIT'})
   self.audit_steps+=1
   if not self.severe and self.audit_samples>=64:
    self.state='RECALIBRATE';self.cal_n=0
    self.events.append({'time':self.t,'event':'enter_recalibrate','audit_epoch_e':self.audit_epochs[-1],'next_state':'RECALIBRATE'})
  elif self.state=='RECALIBRATE':
   self.cal_n+=1
   if self.cal_n>=256:
    old=dict(self.nuisance);self.nuisance={'phase':.06,'leakage':.05,'imbalance':.08}
    self.epoch+=1;self.guard_epochs.append(1.);self.state='NOMINAL';self.guard_cusum=0.
    self.events.append({'time':self.t,'event':'recalibrated','epoch':self.epoch,'old_nuisance_radii':old,'new_nuisance_radii':dict(self.nuisance),'endpoint_embedding':self.endpoint_embedding,'next_state':'NOMINAL'})
  m,eg,ea=self.global_e()
  if m>=1/ALPHA_E and self.state!='SAFE_HALT':
   self.state='SAFE_HALT';self.events.append({'time':self.t,'event':'safe_halt','global_e':m,'threshold':1/ALPHA_E,'next_state':'SAFE_HALT'})
  return {'time':self.t,'action':action,'state':self.state,'global_e':m,'guard_mixture':eg,'audit_mixture':ea}

def replay(severe:bool,horizon:int=2000):
 c=Controller(severe);trace=[]
 for _ in range(horizon):
  row=c.step()
  if row['time'] in (400,401,402,405,413,529,785,1000,2000) or c.events and c.events[-1]['time']==row['time']:trace.append(row)
  if c.state=='SAFE_HALT':break
 counts={a:c.actions.count(a) for a in sorted(set(c.actions))}
 m,eg,ea=c.global_e()
 return {'scenario':'structural_departure' if severe else 'recoverable_covariance_drift','final_time':c.t,'final_state':c.state,'events':c.events,'action_counts':counts,'final_global_e':m,'final_guard_mixture':eg,'final_audit_mixture':ea,'final_nuisance_radii':c.nuisance,'trace':trace}

def payload():
 recover=replay(False);severe=replay(True)
 checks={
  'global_alpha_ledger_point01':abs(ALPHA_COV+ALPHA_E+ALPHA_CAL-ALPHA_TOTAL)<1e-15,
  'mixture_weights_sum_one':abs(sum(WEIGHTS.values())-1)<1e-15,
  'epoch_weights_sum_below_one':sum(2**(-(k+1)) for k in range(16))==1-2**-16,
  'recoverable_guard_warning_at401':recover['events'][0]['event']=='guard_warning' and recover['events'][0]['time']==401,
  'recoverable_activates_64_TrU3_shots':recover['action_counts'].get('TrU3')==64,
  'recoverable_enters_recalibration_at529':any(e['event']=='enter_recalibrate' and e['time']==529 for e in recover['events']),
  'recoverable_recalibrates_at785':any(e['event']=='recalibrated' and e['time']==785 for e in recover['events']),
  'recoverable_returns_nominal':recover['final_state']=='NOMINAL',
  'recoverable_updates_nuisance_intervals':recover['final_nuisance_radii']=={'phase':.06,'leakage':.05,'imbalance':.08},
  'severe_guard_warning_at401':severe['events'][0]['event']=='guard_warning' and severe['events'][0]['time']==401,
  'severe_audit_warning_at405':any(e['event']=='audit_warning' and e['time']==405 for e in severe['events']),
  'severe_safe_halt_at413':severe['final_state']=='SAFE_HALT' and severe['final_time']==413,
  'severe_global_e_crosses_threshold':severe['final_global_e']>=1/ALPHA_E,
  'endpoint_parity_embedding_locked':Controller().endpoint_embedding=={'x':[0,1,0],'y':[1,0,1],'trivial_guard_mode':7,'chi_xy_guard_mode':6},
 }
 digest=hashlib.sha256(json.dumps([recover,severe],sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass640.closed_loop_falsifier.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'global_validity':{'total_anytime_error':ALPHA_TOTAL,'matrix_covariance_CS':ALPHA_COV,'adaptive_e_mixture':ALPHA_E,'recalibration_confidence_budget':ALPHA_CAL,'e_process_weights':WEIGHTS,'final_rejection_rule':'SAFE_HALT only when the weighted e-process mixture reaches 1/alpha_e. CUSUM warnings change acquisition but are not inferential rejections.','epoch_rule':'Every predictably opened audit/recalibration epoch receives weight 2^(-(k+1)); unused tail weight remains at the constant e-value 1. Convex mixtures and predictable channel selection preserve the e-process property.','nuisance_update_rule':'At each shot, likelihood-ratio boundaries are selected from the currently valid covariance/scalar confidence sets using only past data. Recalibration intervals may widen immediately; future narrowing requires confidence-set support.'},
  'controller':{'states':['NOMINAL','AUDIT','RECALIBRATE','SAFE_HALT'],'nominal_schedule':'13 Tr(U) shots for every 1 Tr(U^2) shot','audit_schedule':'Tr(U^3), Tr(U), Tr(U^3), Tr(U^2), repeated','recalibration_schedule':'guard0, guard1, endpoint parity, phase reference, repeated','guard_warning':'one-sided Bernoulli CUSUM with null boundary 0.1, alternative 0.4, warning e=8','audit_warning':'one-sided Tr(U^3) CUSUM with null boundary 0.2, alternative 0.7, warning e=8','endpoint_fibre':'existing H8 guard modes 7 (trivial) and 6 (chi_xy), endpoint translations 010 and 101'},
  'replays':[recover,severe],
  'theorem':'A single closed-loop controller can adapt channel allocation, activate Tr(U^3), recalibrate the endpoint-parity fibre, and update nuisance intervals without sacrificing an anytime guarantee. Operational CUSUM warnings are separated from inferential rejection; all actual rejection evidence lives in a weighted mixture of predictably selected e-process epochs. Together with the matrix covariance confidence sequence and a summable recalibration budget, the global false-halt probability is at most 0.01. The recoverable replay enters audit at shot 401, collects 64 held-out Tr(U^3) shots, recalibrates at shot 785, and returns to nominal operation; the structural-departure replay safely halts at shot 413.','replay_sha256':digest,'checks':checks,'boundary':'The validity theorem assumes the declared conditional Bernoulli interval bounds and the Pass 639 bounded-residual covariance confidence sequence. CUSUM warning times are operational triggers only. The deterministic replays certify controller logic, not empirical hardware performance.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 640 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'recoverable_state':p['replays'][0]['final_state'],'severe_halt':p['replays'][1]['final_time']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
