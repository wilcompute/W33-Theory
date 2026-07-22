#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from collections import defaultdict
from pathlib import Path
import numpy as np
from w33_pass543_547_common import charpoly_prime
from w33_pass566_q5_twisted_walsh_krawtchouk import A,translation_space,f2rank
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass567_joint_bayesian_decoder.json'
HW=ROOT/'hardware'/'w33_pass567_joint_bayesian_decoder.json'

def triality_levels():
 F=defaultdict(set)
 for m in range(4096):
  offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A));F[tuple(charpoly_prime(5,offs)[0])].add(m)
 rows=[]
 for cpv,S in F.items():
  T=translation_space(S)
  if len(S)==80 and f2rank(T)==4:
   coeff=cpv[4]
   emb=tuple(sum(coeff[i]*math.cos(2*math.pi*k*i/5) for i in range(4)) for k in range(1,5))
   products={1 if math.prod((A[i]*(4 if (m>>i)&1 else 1))%5 for i in range(12))%5==1 else -1 for m in S}
   rows.append((coeff,emb,products))
 rows.sort(key=lambda x:x[0])
 return rows

def normalize(p):
 s=p.sum();return p/s if s else np.ones_like(p)/len(p)
def best_channel(post,means):
 avg=post@means;return int(np.argmax(post@((means-avg)**2)))
def gauss_like(y,mu,sigma):
 z=(y-mu)/sigma;return np.exp(-0.5*z*z)
def update(post,means,oris,channel,y,z,sigma,pbit,use_quartic=True,use_orientation=True):
 like=np.ones(len(post))
 if use_quartic:like*=gauss_like(y,means[:,channel],sigma)
 if use_orientation:like*=np.where(oris==z,pbit,1-pbit)
 return normalize(post*like)

def simulate(profile,means,oris,trials=1000,seed=567):
 rng=np.random.default_rng(seed);threshold=profile['posterior_threshold'];sigma=profile['quartic_sigma'];pbit=profile['orientation_single_shot_accuracy'];cap=10000
 joint=[];staged=[];errors_joint=errors_staged=0
 for _ in range(trials):
  h=int(rng.integers(len(oris)))
  p=np.ones(len(oris))/len(oris);n=0
  while p.max()<threshold and n<cap:
   ch=best_channel(p,means);y=rng.normal(means[h,ch],sigma);z=oris[h] if rng.random()<pbit else -oris[h]
   p=update(p,means,oris,ch,y,z,sigma,pbit,True,True);n+=1
  joint.append(n);errors_joint+=int(np.argmax(p)!=h)
  p=np.ones(len(oris))/len(oris);n=0
  while n<cap:
   marg=np.array([p[2*i]+p[2*i+1] for i in range(3)])
   if marg.max()>=threshold:break
   ch=best_channel(p,means);y=rng.normal(means[h,ch],sigma)
   p=update(p,means,oris,ch,y,oris[h],sigma,pbit,True,False);n+=1
  while p.max()<threshold and n<cap:
   z=oris[h] if rng.random()<pbit else -oris[h]
   p=update(p,means,oris,0,0.0,z,sigma,pbit,False,True);n+=1
  staged.append(n);errors_staged+=int(np.argmax(p)!=h)
 def stats(a):
  x=np.array(a);return {'mean':float(x.mean()),'median':float(np.median(x)),'p90':float(np.quantile(x,.9)),'p99':float(np.quantile(x,.99)),'max':int(x.max())}
 js,ss=stats(joint),stats(staged)
 return {'joint':js,'staged':ss,'mean_shot_reduction':ss['mean']-js['mean'],'relative_reduction':(ss['mean']-js['mean'])/ss['mean'],'joint_errors':errors_joint,'staged_errors':errors_staged,'trials':trials}

def payload():
 levels=triality_levels();means3=np.array([x[1] for x in levels],dtype=float)
 means=np.repeat(means3,2,axis=0);oris=np.array([1,-1]*3)
 profiles={
  'conservative':{'quartic_sigma':100.0,'orientation_single_shot_accuracy':0.565,'posterior_threshold':0.995},
  'nominal':{'quartic_sigma':50.0,'orientation_single_shot_accuracy':0.620,'posterior_threshold':0.995},
  'aspirational':{'quartic_sigma':25.0,'orientation_single_shot_accuracy':0.735,'posterior_threshold':0.995},
 }
 results={name:simulate(cfg,means,oris,1000,567+i) for i,(name,cfg) in enumerate(profiles.items())}
 checks={
  'three_triality_levels':len(levels)==3,
  'six_joint_hypotheses':len(oris)==6,
  'each_fibre_has_both_orientations':all(x[2]=={-1,1} for x in levels),
  'all_profiles_joint_beats_staged':all(r['mean_shot_reduction']>0 for r in results.values()),
  'all_relative_reductions_positive':all(r['relative_reduction']>0 for r in results.values()),
  'posterior_error_below_two_percent':all(r['joint_errors']<=20 and r['staged_errors']<=20 for r in results.values()),
  'finite_stopping_all_trials':all(r['joint']['max']<10000 and r['staged']['max']<10000 for r in results.values()),
  'triality_means_distinct':len({tuple(np.round(x,9)) for x in means3})==3,
 }
 hardware={'schema':'w33.hardware.pass567.joint_bayesian_decoder.v1','hypotheses':['triality_fibre_30_or_55_or_75','orientation_plus_or_minus'],'shared_shot_outputs':['one selected quartic Galois channel','orientation latch bit'],'policy':'Choose the Galois channel with maximum posterior variance; update the six-state posterior with the joint Gaussian-Bernoulli likelihood; stop when max posterior exceeds the configured threshold.','profiles':profiles,'results':results,'claim_boundary':'Shot reductions are conditional on the declared Gaussian and binary-readout model and concurrent availability of both outputs. They are not measured hardware performance.'}
 HW.parent.mkdir(parents=True,exist_ok=True);HW.write_text(json.dumps(hardware,sort_keys=True,separators=(',',':'))+'\n')
 return {'schema':'w33.pass567.joint_bayesian_decoder.v1','status':'PASS' if all(checks.values()) else 'FAIL','triality_quartic_coefficients':[x[0] for x in levels],'triality_embedding_means':[x[1] for x in levels],'profiles':profiles,'results':results,'hardware_overlay':str(HW.relative_to(ROOT)),'conclusion':'The joint six-hypothesis posterior reuses every quartic shot for orientation evidence. Under all three declared calibration profiles it reaches the same posterior threshold with fewer mean shots than a staged quartic-then-orientation decoder.','checks':checks,'boundary':'This is a deterministic-seed Monte Carlo certificate under a declared Gaussian quartic model and symmetric binary orientation channel. It does not claim device-independent optimality or measured photon counts.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 567 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'reductions':{k:round(v['relative_reduction'],4) for k,v in p['results'].items()}}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
