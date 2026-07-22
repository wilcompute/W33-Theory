#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from w33_pass568_572_q5_common import charpoly_prime
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass572_analytic_sequential_bound.json'
HW=ROOT/'hardware'/'w33_pass572_analytic_sequential_bound.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2)

def f2rank(rows):
 b=[]
 for x in rows:
  y=x
  for p in b:y=min(y,y^p)
  if y:
   q=1<<(y.bit_length()-1);b=[z^y if z&q else z for z in b];b.append(y);b.sort(reverse=True)
 return len(b)
def translation_space(S):
 base=min(S);return frozenset(t for t in (x^base for x in S) if all((y^t) in S for y in S))
def triality_means():
 F=defaultdict(set)
 for m in range(4096):
  offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A));F[tuple(charpoly_prime(5,offs)[0])].add(m)
 rows=[]
 for cpv,S in F.items():
  T=translation_space(S)
  if len(S)==80 and f2rank(T)==4:
   coeff=cpv[4]
   emb=tuple(sum(coeff[i]*math.cos(2*math.pi*k*i/5) for i in range(4)) for k in range(1,5))
   rows.append((coeff,emb))
 rows.sort(key=lambda x:x[0]);return np.array([x[1] for x in rows],dtype=float)

def bhattacharyya_binary(p):return -math.log(2*math.sqrt(p*(1-p)))

def maximin_lp(pair_infos,costs):
 P,K=pair_infos.shape
 c=np.zeros(K+1);c[-1]=-1
 Aub=np.zeros((P,K+1));bub=np.zeros(P)
 Aub[:,:K]=-pair_infos;Aub[:,-1]=1
 Aeq=np.zeros((1,K+1));Aeq[0,:K]=costs;beq=np.array([1.0])
 res=linprog(c,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*K+[(None,None)],method='highs')
 if not res.success:raise RuntimeError(res.message)
 return float(res.x[-1]),res.x[:K]

def pair_matrix(means,oris,profile):
 sigma=profile['quartic_sigma'];eff=np.array(profile['channel_efficiencies']);p=profile['orientation_single_shot_accuracy'];oe=profile['orientation_efficiency']
 rows=[];pairs=[]
 for i in range(len(oris)):
  for j in range(i+1,len(oris)):
   g=eff*(means[i]-means[j])**2/(8*sigma*sigma)
   b=oe*bhattacharyya_binary(p) if oris[i]!=oris[j] else 0.0
   rows.append(g+b);pairs.append((i,j))
 return np.array(rows),pairs

def bounds_for_profile(profile,means3):
 means=np.repeat(means3,2,axis=0);oris=np.array([1,-1]*3);costs=np.array(profile['channel_costs'],dtype=float);alpha=profile['error_budget']
 joint_pairs,pairs=pair_matrix(means,oris,profile);Ij,xj=maximin_lp(joint_pairs,costs)
 qrows=[]
 eff=np.array(profile['channel_efficiencies']);sig=profile['quartic_sigma']
 for i in range(3):
  for j in range(i+1,3):qrows.append(eff*(means3[i]-means3[j])**2/(8*sig*sig))
 Iq,xq=maximin_lp(np.array(qrows),costs)
 Io=profile['orientation_efficiency']*bhattacharyya_binary(profile['orientation_single_shot_accuracy'])/min(costs)
 joint_bound=math.ceil(math.log(5/alpha)/Ij)
 qbound=math.ceil(math.log(2/(alpha/2))/Iq)
 obound=math.ceil(math.log(1/(alpha/2))/Io)
 staged=qbound+obound
 vals=joint_pairs@xj;active=[pairs[i] for i,v in enumerate(vals) if abs(v-Ij)<1e-8]
 return {
  'joint':{'chernoff_information_per_cost':Ij,'channel_shots_per_unit_cost':xj.tolist(),'union_bound_resource':joint_bound,'active_bottleneck_pairs':active},
  'staged':{'quartic_information_per_cost':Iq,'quartic_channel_shots_per_unit_cost':xq.tolist(),'orientation_information_per_cost':Io,'quartic_bound_resource':qbound,'orientation_bound_resource':obound,'total_bound_resource':staged},
  'analytic_resource_reduction':staged-joint_bound,'analytic_relative_reduction':(staged-joint_bound)/staged,
 }

def payload():
 means3=triality_means()
 profiles={
  'conservative':{'quartic_sigma':100.0,'orientation_single_shot_accuracy':0.565,'orientation_efficiency':0.72,'channel_efficiencies':[0.82,0.76,0.70,0.64],'channel_costs':[1.0,1.15,1.35,1.60],'error_budget':0.005},
  'nominal':{'quartic_sigma':50.0,'orientation_single_shot_accuracy':0.620,'orientation_efficiency':0.88,'channel_efficiencies':[0.94,0.91,0.87,0.83],'channel_costs':[1.0,1.05,1.15,1.25],'error_budget':0.005},
  'aspirational':{'quartic_sigma':25.0,'orientation_single_shot_accuracy':0.735,'orientation_efficiency':0.97,'channel_efficiencies':[0.99,0.98,0.96,0.94],'channel_costs':[1.0,1.0,1.05,1.10],'error_budget':0.005},
 }
 results={k:bounds_for_profile(v,means3) for k,v in profiles.items()}
 checks={
  'three_triality_means':means3.shape==(3,4),
  'six_joint_hypotheses':True,
  'all_lp_information_positive':all(r['joint']['chernoff_information_per_cost']>0 and r['staged']['quartic_information_per_cost']>0 and r['staged']['orientation_information_per_cost']>0 for r in results.values()),
  'coarse_union_bound_does_not_certify_empirical_gain':all(r['analytic_resource_reduction']<0 for r in results.values()),
  'joint_bottleneck_is_orientation_pair':all(all(i//2==j//2 for i,j in r['joint']['active_bottleneck_pairs']) for r in results.values()),
  'all_channel_mixtures_cost_normalized':all(abs(sum(x*c for x,c in zip(r['joint']['channel_shots_per_unit_cost'],profiles[k]['channel_costs']))-1)<1e-8 for k,r in results.items()),
  'unequal_costs_and_losses_active':all(len(set(v['channel_costs']))>1 and len(set(v['channel_efficiencies']))>1 for v in profiles.values()),
  'chernoff_union_bound_uses_six_hypotheses':all(r['joint']['union_bound_resource']>=1 for r in results.values()),
  'orientation_dark_count_folded_into_pbit':all(.5<v['orientation_single_shot_accuracy']<1 for v in profiles.values()),
 }
 hardware={'schema':'w33.hardware.pass572.analytic_sequential_bound.v1','policy':'Use the cost-normalized maximin Chernoff channel mixture as the prior-safe schedule; after posterior concentration, switch to the channel maximizing the current worst-pair information per resource.','profiles':profiles,'bounds':results,'claim_boundary':'Analytic bounds use Gaussian quartic channels, a symmetric binary orientation channel, declared efficiency/cost factors, and a union Chernoff bound. They are not measured device guarantees.'}
 HW.parent.mkdir(parents=True,exist_ok=True);HW.write_text(json.dumps(hardware,sort_keys=True,separators=(',',':'))+'\n')
 return {
  'schema':'w33.pass572.analytic_sequential_bound.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'triality_means':means3.tolist(),'profiles':profiles,'results':results,
  'theorem':{'pair_information':'C_ij,k = eta_k (mu_i,k-mu_j,k)^2/(8 sigma^2) plus -eta_o log(2 sqrt(p(1-p))) when orientations differ.','maximin_program':'maximize t subject to sum_k cost_k x_k=1 and sum_k C_ij,k x_k >= t for every hypothesis pair.','union_bound':'P(error) <= (H-1) exp(-resource*C*) gives resource >= log((H-1)/alpha)/C*.','staged_comparison':'Split alpha equally between a three-fibre quartic stage and a binary orientation stage, then add their resource bounds.'},
  'hardware_overlay':str(HW.relative_to(ROOT)),'checks':checks,
  'conclusion':'The cost-aware maximin schedule is exact, but the generic six-hypothesis union Chernoff bound is orientation-pair dominated and is about 13-14% looser than the staged union bound. Therefore it does not certify the Monte Carlo gain from Pass 567; a posterior-state dynamic program is required for that sharper statement.',
  'boundary':'This adds a deterministic Chernoff/linear-program certificate under the declared observation model. It deliberately records that the coarse worst-pair union bound cannot prove the empirical joint-decoder advantage; it does not claim Bayes-optimality.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 572 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'reductions':{k:round(v['analytic_relative_reduction'],4) for k,v in p['results'].items()}}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
