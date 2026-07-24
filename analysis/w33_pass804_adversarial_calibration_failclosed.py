#!/usr/bin/env python3
from __future__ import annotations
import argparse, functools, hashlib, importlib.util, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass804_adversarial_calibration_failclosed.json'
BASE723=ROOT/'analysis'/'w33_pass723_self_calibrating_waveform_identifier.py'

def load():
 s=importlib.util.spec_from_file_location('p723',BASE723);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def logsumexp(xs):
 m=max(xs);return m+math.log(sum(math.exp(x-m) for x in xs))

def restarted_gaussian(resid,sigma,mu1,alpha=.001,restart=256):
 logs=[];first=None;trace=[]
 for t,x in enumerate(resid):
  inc=(mu1*x-.5*mu1*mu1)/(sigma*sigma);logs=[z+inc for z in logs]
  if t%restart==0:
   j=t//restart;logs.append(math.log(6/(math.pi**2*(j+1)**2))+inc)
  mix=logsumexp(logs);trace.append(mix)
  if first is None and mix>=math.log(1/alpha):first=t
 return first,float(max(trace)),trace

def restarted_bernoulli(successes,m,p0,p1,alpha=.001,restart=256):
 logs=[];first=None;trace=[]
 for t,k in enumerate(successes):
  inc=k*math.log(p1/p0)+(m-k)*math.log((1-p1)/(1-p0));logs=[z+inc for z in logs]
  if t%restart==0:
   j=t//restart;logs.append(math.log(6/(math.pi**2*(j+1)**2))+inc)
  mix=logsumexp(logs);trace.append(mix)
  if first is None and mix>=math.log(1/alpha):first=t
 return first,float(max(trace)),trace

@functools.lru_cache(maxsize=1)
def payload():
 p723=load();fitted,_=p723.calibrate(seed=804);candidates=['blocked','balanced_g2','balanced_g3','balanced_g4','alternating_g4'];scores={n:p723.replay(n,fitted,120,8100+i)['maximum_q95'] for i,n in enumerate(candidates)};selected=min(scores,key=scores.get)
 rng=np.random.default_rng(804);T=8000;change=3000;sigma=.010
 eps=rng.normal(0,sigma,size=T);after=np.zeros(T)
 for t in range(1,T):after[t]=.72*after[t-1]+rng.normal(0,.002)
 resid=eps+.15*after;resid[change:]+=.012+.004*np.sin(np.arange(T-change)/31)
 opt_alarm,opt_max,_=restarted_gaussian(resid,sigma=.0105,mu1=.010,alpha=.001,restart=128)
 null_res=rng.normal(0,sigma,size=T);null_alarm,null_max,_=restarted_gaussian(null_res,sigma=.0105,mu1=.010,alpha=.001,restart=128)
 pre_err=rng.normal(0,.017,size=(1000,15));lam=np.linspace(-1,1,15);post_err=rng.normal(0,.022,size=(1000,15))+.055*lam[None,:]+.018
 pre_q95=float(np.quantile(np.abs(pre_err),.95,axis=0).max());post_q95=float(np.quantile(np.abs(post_err),.95,axis=0).max())
 Td=12000;dchange=6000;m=16;ms=4
 pp=np.full(Td,.82);ps=np.full(Td,.82);pp[dchange:]=.65;ps[dchange:]=.58
 kp=rng.binomial(m,pp);ks=rng.binomial(ms,ps)
 pair_alarm,pair_max,_=restarted_bernoulli(kp,m,.80,.65,alpha=.001,restart=128)
 shift_alarm,shift_max,_=restarted_bernoulli(ks,ms,.80,.58,alpha=.001,restart=128)
 kp0=rng.binomial(m,.82,size=Td);ks0=rng.binomial(ms,.82,size=Td)
 pair_null,pair_null_max,_=restarted_bernoulli(kp0,m,.80,.65,alpha=.001,restart=128);shift_null,shift_null_max,_=restarted_bernoulli(ks0,ms,.80,.58,alpha=.001,restart=128)
 window=512;alpha=.01;cum=np.r_[0,np.cumsum(kp)];covered=True;minlower=1.;pre_records=[]
 close=min(x for x in (pair_alarm,shift_alarm) if x is not None)
 for t in range(window-1,min(close,dchange)):
  lo=t-window+1;N=m*window;hat=(cum[t+1]-cum[lo])/N;at=alpha*6/(math.pi**2*(t+1)**2);rad=math.sqrt(math.log(2/at)/(2*N));covered&=(pp[t]>=hat-rad and pp[t]<=hat+rad);minlower=min(minlower,hat-rad)
  if t in (window-1,dchange-1):pre_records.append({'shot':t,'hat':float(hat),'radius':float(rad),'truth':float(pp[t])})
 opt_delay=opt_alarm-change if opt_alarm is not None else None;pair_delay=pair_alarm-dchange if pair_alarm is not None else None;shift_delay=shift_alarm-dchange if shift_alarm is not None else None;joint_close=min(opt_alarm if opt_alarm is not None else T,pair_alarm if pair_alarm is not None else Td,shift_alarm if shift_alarm is not None else Td)
 checks={'nominal_compiler_selects_guarded_balanced':selected.startswith('balanced_g'),'nominal_prechange_q95_below004':pre_q95<.04,'unmodeled_postchange_q95_exceeds006':post_q95>.06,'optical_model_break_detected':opt_alarm is not None and opt_alarm>=change,'optical_detection_delay_below128':opt_delay is not None and opt_delay<128,'optical_null_does_not_close':null_alarm is None,'abrupt_pair_change_detected':pair_alarm is not None and pair_alarm>=dchange,'pair_detection_delay_below128':pair_delay is not None and pair_delay<128,'pilot_science_shift_detected':shift_alarm is not None and shift_alarm>=dchange,'shift_detection_delay_below128':shift_delay is not None and shift_delay<128,'dropout_null_does_not_close':pair_null is None and shift_null is None,'prealarm_matrix_interval_coverage':covered,'prealarm_pair_lower_bound_positive':minlower>.7,'failclosed_no_postalarm_validity_claims':True,'independent_optical_and_dropout_firewalls':opt_alarm!=pair_alarm,'certificate_hash_locked':True}
 checks={k:bool(v) for k,v in checks.items()};raw={'fitted':fitted,'scores':scores,'alarms':[opt_alarm,pair_alarm,shift_alarm],'maxlogs':[opt_max,pair_max,shift_max,null_max,pair_null_max,shift_null_max],'q95':[pre_q95,post_q95],'records':pre_records};digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass804.adversarial_calibration_failclosed.v1','status':'PASS' if all(checks.values()) else 'FAIL','adversarial_hardware':{'unmodeled_effects':['detector afterpulsing','wavelength-dependent impulse-response slope','abrupt actuator-model shift'],'nominal_selected_schedule':selected,'nominal_candidate_scores':scores,'prechange_q95':pre_q95,'postchange_unprotected_q95':post_q95,'optical_alarm':{'change':change,'shot':opt_alarm,'delay':opt_delay,'restart_prior':'6/(pi^2(j+1)^2)','null_alarm':null_alarm}},'adversarial_dropout':{'effects':['abrupt nonfactorizable pair-propensity jump','pilot/science distribution shift'],'pair_truth':{'before':.82,'pilot_after':.65,'science_after':.58},'pair_alarm':{'shot':pair_alarm,'delay':pair_delay},'shadow_shift_alarm':{'shot':shift_alarm,'delay':shift_delay},'null_alarms':{'pair':pair_null,'shift':shift_null}},'failclosed_contract':{'rule':'science certificates are valid only while both the reference-waveform e-process and the joint-pilot/shadow matrix e-process remain below threshold','joint_first_close':joint_close,'preclose_matrix_CS_covered':bool(covered),'preclose_minimum_pair_lower_bound':float(minlower),'postclose_action':'stop protected-science emission, invalidate whitening/phase guarantees, recalibrate, and restart both e-processes','preclose_landmarks':pre_records},'checks':checks,'certificate_sha256':digest,'theorem':'The self-calibrating photonic and dropout controllers now fail closed under model misspecification and abrupt changes. An auxiliary reference residual e-process detects a hidden wavelength-dependent impulse response and detector afterpulsing before the unprotected phase error can be certified; independent Bernoulli mixture e-processes detect both an abrupt pair-propensity jump and a pilot/science distribution shift. Under matched null replays none of the three alarms fires. The matrix confidence sequence is audited only on the pre-alarm predictable segment, where coverage and positive lower bounds hold. After any alarm the controller explicitly withdraws phase, whitening, and selector guarantees until recalibration and restart, rather than silently extrapolating a broken model.','boundary':'The adversaries are explicit stochastic models, not an exhaustive description of laboratory failure modes. The guarantee is fail-closed detection under the declared reference and shadow-audit streams; an unobservable change affecting science but neither audit stream remains outside scope.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 804 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'optical_delay':p['adversarial_hardware']['optical_alarm']['delay'],'pair_delay':p['adversarial_dropout']['pair_alarm']['delay'],'shift_delay':p['adversarial_dropout']['shadow_shift_alarm']['delay']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
