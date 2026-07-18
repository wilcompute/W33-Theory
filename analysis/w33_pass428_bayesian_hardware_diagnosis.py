#!/usr/bin/env python3
"""Pass 428: Bayesian component diagnosis with correlated synthetic noise."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np

from w33_pass410_414_common import certificate,write_json
from w33_pass423_hardware_inverse_compiler import build_dictionary

def round_floats(x,digits=12):
    if isinstance(x,float): return round(x,digits)
    if isinstance(x,list): return [round_floats(v,digits) for v in x]
    if isinstance(x,tuple): return [round_floats(v,digits) for v in x]
    if isinstance(x,dict): return {k:round_floats(v,digits) for k,v in x.items()}
    return x

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass428_bayesian_hardware_diagnosis.json'
SOURCE=ROOT/'data'/'w33_pass418_defect_atlas.json'

FAMILY_PRIOR={'detector_gain':.15,'native_coupler':.25,'parasitic_crosstalk':.20,'phase_trim':.25,'delay_register':.13}
NULL_PRIOR=.02
TAU=2.0


def family_modes(entries:list[dict])->np.ndarray:
    names=sorted({e['family'] for e in entries});cols=[]
    for name in names:
        v=np.array([e['family']==name for e in entries],float);v/=np.linalg.norm(v);cols.append(v)
    return np.column_stack(cols)


def precision_apply(X:np.ndarray,U:np.ndarray,sigma:float,kappa:float)->np.ndarray:
    return (X-U@((kappa*kappa/(sigma*sigma+kappa*kappa))*(U.T@X)))/(sigma*sigma)


def noise(rng:np.random.Generator,n:int,U:np.ndarray,sigma:float,kappa:float)->np.ndarray:
    return sigma*rng.normal(size=n)+kappa*U@rng.normal(size=U.shape[1])


def posterior(y:np.ndarray,D:np.ndarray,components:list[dict],U:np.ndarray,sigma:float,kappa:float)->tuple[np.ndarray,float]:
    PD=precision_apply(D,U,sigma,kappa);Py=precision_apply(y,U,sigma,kappa)
    q=np.sum(D*PD,axis=0);s=D.T@Py
    logbf=-.5*np.log1p(TAU*TAU*q)+.5*TAU*TAU*s*s/(1+TAU*TAU*q)
    counts={f:sum(c['family']==f for c in components) for f in FAMILY_PRIOR}
    lp=np.array([math.log(FAMILY_PRIOR[c['family']]/counts[c['family']])+logbf[i] for i,c in enumerate(components)])
    ln=math.log(NULL_PRIOR);mx=max(float(lp.max()),ln);den=math.exp(ln-mx)+float(np.exp(lp-mx).sum())
    return np.exp(lp-mx)/den,math.exp(ln-mx)/den


def low_rank_log_bf(y:np.ndarray,X:np.ndarray,U:np.ndarray,sigma:float,kappa:float)->float:
    PX=precision_apply(X,U,sigma,kappa);Py=precision_apply(y,U,sigma,kappa)
    G=X.T@PX;v=X.T@Py;M=np.eye(X.shape[1])/(TAU*TAU)+G
    return float(-.5*np.linalg.slogdet(np.eye(X.shape[1])+TAU*TAU*G)[1]+.5*v@np.linalg.solve(M,v))


def build_payload()->dict:
    source=json.loads(SOURCE.read_text());entries=source['entries'];D,components=build_dictionary(entries);U=family_modes(entries);rng=np.random.default_rng(428)
    selected=[]
    for family in FAMILY_PRIOR:
        ids=[i for i,c in enumerate(components) if c['family']==family]
        selected.extend([ids[j] for j in np.linspace(0,len(ids)-1,10,dtype=int)])
    scenarios=[];all_records=[]
    for sigma,kappa in ((.08,.04),(.15,.08),(.25,.12)):
        top1=top5=famok=0;brier=[];confidence=[]
        for true in selected:
            y=1.5*D[:,true]+noise(rng,D.shape[0],U,sigma,kappa)
            post,pnull=posterior(y,D,components,U,sigma,kappa);order=np.argsort(post)[::-1]
            top1+=int(order[0]==true);top5+=int(true in order[:5]);famok+=int(components[order[0]]['family']==components[true]['family'])
            confidence.append(float(post[true]));brier.append(float(np.sum((post-np.eye(1,len(post),true)[0])**2)+pnull*pnull))
            if len(all_records)<12:
                all_records.append({'sigma':sigma,'correlation_scale':kappa,'injected':components[true]['name'],'injected_family':components[true]['family'],
                  'top_component':components[int(order[0])]['name'],'top_probability':float(post[order[0]]),'true_probability':float(post[true]),'null_probability':pnull,
                  'top5':[components[int(i)]['name'] for i in order[:5]]})
        scenarios.append({'sigma':sigma,'correlation_scale':kappa,'trials':len(selected),'top1_correct':top1,'top5_correct':top5,'family_correct':famok,
          'mean_true_posterior':float(np.mean(confidence)),'minimum_true_posterior':float(np.min(confidence)),'mean_brier_score':float(np.mean(brier))})

    delay_id=next(i for i,c in enumerate(components) if c['family']=='delay_register')
    coords=components[delay_id]['coordinate_ids'];trim_ids=[next(i for i,c in enumerate(components) if c['family']=='phase_trim' and c['coordinate_ids']==[x]) for x in coords]
    delay_bf=[];trim_bf=[]
    for _ in range(24):
        y=1.5*D[:,delay_id]+noise(rng,D.shape[0],U,.10,0.0)
        delay_bf.append(low_rank_log_bf(y,D[:,[delay_id]],U,.10,0.0)-low_rank_log_bf(y,D[:,trim_ids],U,.10,0.0))
        y=D[:,trim_ids]@np.array([1.5,-1.0,.7])+noise(rng,D.shape[0],U,.10,0.0)
        trim_bf.append(low_rank_log_bf(y,D[:,[delay_id]],U,.10,0.0)-low_rank_log_bf(y,D[:,trim_ids],U,.10,0.0))

    checks={
      'dictionary_has_387_components':len(components)==387,
      'family_priors_plus_null_sum_one':abs(sum(FAMILY_PRIOR.values())+NULL_PRIOR-1)<1e-15,
      'family_common_modes_orthonormal':np.max(np.abs(U.T@U-np.eye(U.shape[1])))<1e-12,
      'three_noise_scenarios':len(scenarios)==3,
      'at_least_149_of_150_top1':sum(x['top1_correct'] for x in scenarios)>=149,
      'all_150_top5':sum(x['top5_correct'] for x in scenarios)==150,
      'all_150_family_correct':sum(x['family_correct'] for x in scenarios)==150,
      'low_noise_mean_posterior_above_0_999':scenarios[0]['mean_true_posterior']>.999,
      'delay_model_wins_all_24_shared_faults':min(delay_bf)>0,
      'three_trim_model_wins_all_24_independent_faults':max(trim_bf)<0,
      'delay_bayes_factors_well_separated':min(delay_bf)>0.2 and max(trim_bf)<-50,
    };checks={k:bool(v) for k,v in checks.items()}
    payload={'schema':'w33.pass428.bayesian_hardware_diagnosis.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{
       'posterior':'the 387-component Pass-423 dictionary is upgraded from a sparse point estimate to normalized component and null posteriors with family-level priors',
       'correlated_noise':'the likelihood includes independent readout noise plus four orbit-family common modes through an analytic Woodbury precision',
       'synthetic_recovery':f"{sum(x['top1_correct'] for x in scenarios)}/150 top-1, 150/150 top-5, and 150/150 family recovery across three seeded correlated-noise regimes",
       'hierarchical_model_selection':'a shared three-bin delay and three independent phase trims are separated by low-rank marginal likelihood, including the Occam determinant penalty',
       'boundary':'priors, amplitude scale, transfer dictionary, and covariance are synthetic calibration assumptions; no physical-device posterior or empirical failure rate is claimed'},
      'priors':{'null':NULL_PRIOR,'families':FAMILY_PRIOR,'amplitude_standard_deviation':TAU},
      'noise_scenarios':scenarios,'selected_posteriors':all_records,
      'delay_vs_trim':{'delay_component':components[delay_id]['name'],'phase_trim_components':[components[i]['name'] for i in trim_ids],
        'shared_delay_log_bayes_factor_range':[min(delay_bf),max(delay_bf)],'independent_trims_log_bayes_factor_range':[min(trim_bf),max(trim_bf)],
        'sign_convention':'positive favors shared delay; negative favors three independent trims'},
      'checks':checks}
    payload=round_floats(payload);payload['certificate_sha256']=certificate(payload);return payload


def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 428 certificate drift')
 else:write_json(a.output,p)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
