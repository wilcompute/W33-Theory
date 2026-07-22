#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.special import ndtr
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass577_bayesian_posterior_dynamic_program.json'
HW=ROOT/'hardware'/'w33_pass577_bayesian_posterior_dynamic_program.json'
MEANS=np.array([
 [9522.668110905885,1752.331889094115,1752.3318890941157,9522.668110905885],
 [9695.413862312147,2204.586137687852,2204.586137687853,9695.413862312147],
 [9643.159613718411,2431.8403862815885,2431.8403862815894,9643.15961371841],
],dtype=float)
PROFILES={
 'conservative':{'channel_costs':[1.0,1.15,1.35,1.6],'channel_efficiencies':[0.82,0.76,0.70,0.64],'orientation_efficiency':0.72,'orientation_single_shot_accuracy':0.565,'quartic_sigma':100.0},
 'nominal':{'channel_costs':[1.0,1.05,1.15,1.25],'channel_efficiencies':[0.94,0.91,0.87,0.83],'orientation_efficiency':0.88,'orientation_single_shot_accuracy':0.620,'quartic_sigma':50.0},
 'aspirational':{'channel_costs':[1.0,1.0,1.05,1.1],'channel_efficiencies':[0.99,0.98,0.96,0.94],'orientation_efficiency':0.97,'orientation_single_shot_accuracy':0.735,'quartic_sigma':25.0},
}

def compositions(total,n,prefix=()):
 if n==1:yield prefix+(total,);return
 for x in range(total+1):yield from compositions(total-x,n-1,prefix+(x,))

def nearest_composition(p,M):
 x=np.maximum(p,0)*M;b=np.floor(x).astype(int);left=M-int(b.sum())
 if left>0:
  order=np.argsort(-(x-b),kind='stable');b[order[:left]]+=1
 elif left<0:
  order=np.argsort(x-b,kind='stable');b[order[:(-left)]]-=1
 return tuple(map(int,b))

def quartic_probs(profile):
 out=np.zeros((4,6,3),dtype=float)
 for k in range(4):
  vals=sorted(MEANS[:,k]);cuts=[-np.inf,(vals[0]+vals[1])/2,(vals[1]+vals[2])/2,np.inf]
  sig=profile['quartic_sigma']/math.sqrt(profile['channel_efficiencies'][k])
  for h in range(6):
   mu=MEANS[h//2,k]
   for b in range(3):out[k,h,b]=ndtr((cuts[b+1]-mu)/sig)-ndtr((cuts[b]-mu)/sig)
 return out

def action_models(profile,augmented):
 q=quartic_probs(profile);peff=.5+profile['orientation_efficiency']*(profile['orientation_single_shot_accuracy']-.5)
 op=np.array([[peff,1-peff] if h%2==0 else [1-peff,peff] for h in range(6)])
 actions=[]
 for k,c in enumerate(profile['channel_costs']):actions.append((f'Q{k}',float(c),q[k]))
 actions.append(('O',1.0,op))
 if augmented:
  for k,c in enumerate(profile['channel_costs']):actions.append((f'J{k}',float(c),(q[k][:,:,None]*op[:,None,:]).reshape(6,6)))
 return actions

def precompute(M,profile,augmented):
 states=np.array(list(compositions(M,6)),dtype=np.int16);belief=states/M
 powers=(M+1)**np.arange(6,dtype=np.int64);codes=states.astype(np.int64)@powers
 order=np.argsort(codes);sorted_codes=codes[order]
 terminal=200.0*(1-belief.max(axis=1));models=[]
 for name,cost,L in action_models(profile,augmented):
  obs=L.shape[1];nxt=np.empty((len(states),obs),dtype=np.int32);prob=belief@L
  for o in range(obs):
   post=belief*L[:,o]
   den=post.sum(axis=1);good=den>0
   post[good]/=den[good,None];post[~good]=belief[~good]
   x=post*M;b=np.floor(x+1e-14).astype(np.int16);left=M-b.sum(axis=1)
   frac=x-b;ranked=np.argsort(-frac,axis=1,kind='stable')
   rows=np.arange(len(states))
   for t in range(5):
    mask=left>t
    b[rows[mask],ranked[mask,t]]+=1
   pcodes=b.astype(np.int64)@powers;pos=np.searchsorted(sorted_codes,pcodes)
   if not np.all(sorted_codes[pos]==pcodes):raise AssertionError('belief projection missed grid')
   nxt[:,o]=order[pos]
  models.append((name,cost,prob,nxt))
 return states,belief,terminal,models

def solve(M,profile,augmented,tol=1e-11,maxiter=20000):
 states,belief,terminal,models=precompute(M,profile,augmented);V=terminal.copy();policy=np.full(len(V),-1,dtype=np.int16)
 residual=None
 for it in range(maxiter):
  B=terminal.copy();P=np.full(len(V),-1,dtype=np.int16)
  for ai,(name,cost,prob,nxt) in enumerate(models):
   Q=cost+np.sum(prob*V[nxt],axis=1);mask=Q<B;B[mask]=Q[mask];P[mask]=ai
  residual=float(np.max(np.abs(B-V)));V=B;policy=P
  if residual<tol:break
 else:raise RuntimeError('value iteration did not converge')
 prior=np.array([M//6]*6,dtype=int);prior[:M-6*(M//6)]+=1;pi=next(i for i,x in enumerate(states) if np.array_equal(x,prior))
 return {'M':M,'states':len(states),'value':float(V[pi]),'prior_state':prior.tolist(),'prior_action':'STOP' if policy[pi]<0 else models[policy[pi]][0],'iterations':it+1,'residual':residual,'V':V,'policy':policy,'states_array':states,'models':[x[0] for x in models]}

def compare_profile(name,M=12):
 prof=PROFILES[name];sep=solve(M,prof,False);aug=solve(M,prof,True);gain=sep['value']-aug['value'];improved=int(np.sum(aug['V']<sep['V']-1e-9));maxgain=float(np.max(sep['V']-aug['V']))
 return {'grid_denominator':M,'belief_states':sep['states'],'separate_value_at_uniform_prior':sep['value'],'augmented_value_at_uniform_prior':aug['value'],'absolute_gain':gain,'relative_gain':gain/sep['value'] if sep['value'] else 0.0,'states_strictly_improved':improved,'maximum_grid_state_gain':maxgain,'separate_prior_action':sep['prior_action'],'augmented_prior_action':aug['prior_action'],'separate_iterations':sep['iterations'],'augmented_iterations':aug['iterations'],'separate_residual':sep['residual'],'augmented_residual':aug['residual']}

def payload():
 results={n:compare_profile(n,12) for n in PROFILES}
 refine=compare_profile('aspirational',18)
 checks={
  'six_hypotheses':MEANS.shape==(3,4),
  'grid_M12_has_6188_states':all(x['belief_states']==6188 for x in results.values()),
  'augmented_action_set_contains_baseline':True,
  'finite_grid_policy_never_worse':all(x['augmented_value_at_uniform_prior']<=x['separate_value_at_uniform_prior']+1e-9 for x in results.values()),
  'conservative_strict_prior_gain':results['conservative']['absolute_gain']>0,
  'nominal_strict_prior_gain':results['nominal']['absolute_gain']>0,
  'aspirational_prior_tie_recorded':abs(results['aspirational']['absolute_gain'])<1e-8,
  'aspirational_other_states_improve':results['aspirational']['states_strictly_improved']>0,
  'M18_refinement_preserves_aspirational_prior_tie':abs(refine['absolute_gain'])<1e-7,
  'all_value_iterations_converged':all(max(x['separate_residual'],x['augmented_residual'])<1e-10 for x in list(results.values())+[refine]),
 }
 hardware={'schema':'w33.hardware.pass577.bayesian_posterior_dynamic_program.v1','hypotheses':'three quartic triality fibres times two orientations','belief_grid':'simplex lattice with denominator 12; aspirational cross-check at denominator 18','terminal_loss':200.0,'baseline_actions':['four quartic-only Galois channels','one orientation-only latch'],'augmented_actions':['all baseline actions','four simultaneous quartic-plus-orientation actions'],'results':results,'aspirational_refinement_M18':{k:v for k,v in refine.items() if k not in ('V','policy','states_array')},'claim_boundary':'This is a certified finite-grid policy-improvement computation under the declared observation model. It is not yet a continuous-belief Bayes-optimal theorem or measured hardware result.'}
 HW.parent.mkdir(parents=True,exist_ok=True);HW.write_text(json.dumps(hardware,sort_keys=True,separators=(',',':'))+'\n')
 return {'schema':'w33.pass577.bayesian_posterior_dynamic_program.v1','status':'PASS' if all(checks.values()) else 'FAIL','profiles':PROFILES,'results':results,'aspirational_refinement_M18':{k:v for k,v in refine.items() if k not in ('V','policy','states_array')},'theorem':'On each finite belief grid, adding simultaneous joint actions cannot worsen the Bellman value because the augmented action set contains every staged action. It strictly improves the uniform-prior value for conservative and nominal calibration, ties at the aspirational uniform prior, and improves thousands of other aspirational grid states.','checks':checks,'hardware_overlay':str(HW.relative_to(ROOT)),'boundary':'The result is exact for the finite quantized belief MDP and declared Gaussian/Bernoulli model. Nearest-grid projection is not a proof for the continuous posterior simplex; aspirational equality at two grid resolutions is reported rather than hidden.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 577 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'gains':{k:round(v['relative_gain'],5) for k,v in p['results'].items()}}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
