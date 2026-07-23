#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from pathlib import Path
import numpy as np
import w33_pass630_composite_null_eprocess as p630
import w33_pass634_correlated_optical_decoder as p634
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass635_joint_optical_eprocess_design.json'
ALPHA=.01
CONFUSION_CAPS={'tight':.005,'laboratory':.01,'stress':.02,'wide':.04}

def kl(p,q):
 p=max(1e-15,min(1-1e-15,p));q=max(1e-15,min(1-1e-15,q))
 return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))

def robust_pair_information(eps):
 P=p630.P;R=p630.RAD;L=eps+(1-2*eps)*np.maximum(.001,P-R);U=eps+(1-2*eps)*np.minimum(.999,P+R)
 rows=[]
 for c,d in itertools.permutations(range(4),2):
  info=[]
  for k in range(3):
   if L[d,k]>U[c,k]:info.append(kl(float(L[d,k]),float(U[c,k])))
   elif U[d,k]<L[c,k]:info.append(kl(float(U[d,k]),float(L[c,k])))
   else:info.append(0.)
  rows.append({'null_class':c,'alternative_class':d,'information':info})
 return rows

def maximin_channel_mix(rows):
 vertices=[]
 for active in itertools.combinations(range(15),3):
  A=[[1.,1.,1.,0.]];b=[1.]
  for a in active:
   if a<12:A.append(rows[a]['information']+[-1.]);b.append(0.)
   else:
    r=[0.,0.,0.,0.];r[a-12]=1.;A.append(r);b.append(0.)
  try:x=np.linalg.solve(np.array(A),np.array(b))
  except np.linalg.LinAlgError:continue
  q=x[:3];t=float(x[3])
  if min(q)>=-1e-10 and all(float(np.dot(r['information'],q))>=t-1e-10 for r in rows):vertices.append((t,q,active))
 if not vertices:raise RuntimeError('empty maximin polytope')
 return max(vertices,key=lambda z:z[0])

def continuous_alpha_codesign(t):
 I_guard=.5*(1.25-1-math.log(1.25));I_ref=kl(.8,.9);a_ref=1/I_ref
 def alpha_ref(n):return ALPHA-3*math.exp(-n*t)-2*math.exp(-n*I_guard)
 def derivative(n):
  ar=alpha_ref(n);arp=3*t*math.exp(-n*t)+2*I_guard*math.exp(-n*I_guard)
  return 1-a_ref*arp/ar
 lo=max(math.log(3/ALPHA)/t,math.log(2/ALPHA)/I_guard);hi=lo+3000
 while alpha_ref(hi)<=0 or derivative(hi)<0:hi*=2
 for _ in range(100):
  m=(lo+hi)/2
  if alpha_ref(m)<=0 or derivative(m)<0:lo=m
  else:hi=m
 n=(lo+hi)/2;ac=3*math.exp(-n*t);ag=2*math.exp(-n*I_guard);ar=alpha_ref(n)
 return {'continuous_shared_class_guard_shots':n,'continuous_reference_shots':math.log(2/ar)/I_ref,'alpha_class':ac,'alpha_guard':ag,'alpha_reference':ar,'guard_information':I_guard,'reference_information':I_ref}

def integer_allocation(rows,q,design):
 Lc=math.log(3/design['alpha_class']);Lg=math.log(2/design['alpha_guard']);Lr=math.log(2/design['alpha_reference'])
 n=design['continuous_shared_class_guard_shots'];n0c=n*q[0];n1c=n*q[1];n2c=n*q[2];best=None
 ranges=[range(max(0,math.floor(x)-6),math.ceil(x)+24) for x in (n0c,n1c,n2c)]
 for n0 in ranges[0]:
  for n1 in ranges[1]:
   for n2 in ranges[2]:
    total=n0+n1+n2
    if total*design['guard_information']+1e-12<Lg:continue
    if min(n0*r['information'][0]+n1*r['information'][1]+n2*r['information'][2] for r in rows)+1e-12<Lc:continue
    if best is None or (total,n2,n1,n0)<(sum(best),best[2],best[1],best[0]):best=(n0,n1,n2)
 if best is None:raise RuntimeError('integer allocation search failed')
 nr=math.ceil(Lr/design['reference_information'])
 return {'trace_channel_shots':list(best),'shared_class_guard_shots':sum(best),'reference_shots':nr,'minimum_class_log_evidence':min(sum(best[k]*r['information'][k] for k in range(3)) for r in rows),'required_class_log_evidence':Lc,'guard_log_evidence':sum(best)*design['guard_information'],'required_guard_log_evidence':Lg,'reference_log_evidence':nr*design['reference_information'],'required_reference_log_evidence':Lr}

def payload():
 optical={r['name']:r for r in p634.payload()['profiles']};profiles=[]
 for name,eps in CONFUSION_CAPS.items():
  rows=robust_pair_information(eps);t,q,active=maximin_channel_mix(rows);design=continuous_alpha_codesign(t);integer=integer_allocation(rows,q,design)
  per_decode=math.ceil(8*math.log(11/eps)/optical[name]['minimum_pair_information_per_photon'])
  raw=integer['shared_class_guard_shots']*per_decode+integer['reference_shots']
  active_labels=[]
  for a in active:
   if a<12:active_labels.append([rows[a]['null_class'],rows[a]['alternative_class']])
   else:active_labels.append(['zero_channel',a-12])
  profiles.append({'name':name,'certified_decoding_confusion_cap':eps,'maximin_channel_fractions':q.tolist(),'maximin_class_information_per_decoded_shot':t,'active_constraints':active_labels,'alpha_allocation':{'class':design['alpha_class'],'guard':design['alpha_guard'],'reference':design['alpha_reference'],'sum':design['alpha_class']+design['alpha_guard']+design['alpha_reference']},'continuous_design':design,'integer_design':integer,'raw_photons_per_decoded_Wilson_shot':per_decode,'total_raw_photon_budget':raw,'guard_telemetry_extra_shots':0})
 locked_alloc={r['name']:r['integer_design']['trace_channel_shots'] for r in profiles};locked_raw={r['name']:r['total_raw_photon_budget'] for r in profiles}
 checks={
  'all_alpha_budgets_sum_to_point01':all(abs(r['alpha_allocation']['sum']-ALPHA)<1e-12 for r in profiles),
  'third_trace_zero_classification_allocation':all(r['maximin_channel_fractions'][2]<1e-10 and r['integer_design']['trace_channel_shots'][2]==0 for r in profiles),
  'same_two_worst_pairs_all_profiles':all(r['active_constraints'][:2]==[[2,1],[3,2]] for r in profiles),
  'guard_telemetry_piggybacks_for_free':all(r['guard_telemetry_extra_shots']==0 and r['integer_design']['guard_log_evidence']>=r['integer_design']['required_guard_log_evidence'] for r in profiles),
  'all_class_constraints_met':all(r['integer_design']['minimum_class_log_evidence']>=r['integer_design']['required_class_log_evidence'] for r in profiles),
  'all_reference_constraints_met':all(r['integer_design']['reference_log_evidence']>=r['integer_design']['required_reference_log_evidence'] for r in profiles),
  'integer_allocations_locked':locked_alloc=={'tight':[456,36,0],'laboratory':[462,36,0],'stress':[476,37,0],'wide':[507,40,0]},
  'reference_counts_locked':{r['name']:r['integer_design']['reference_shots'] for r in profiles}=={'tight':153,'laboratory':153,'stress':154,'wide':155},
  'decoder_photons_locked':{r['name']:r['raw_photons_per_decoded_Wilson_shot'] for r in profiles}=={'tight':135,'laboratory':255,'stress':680,'wide':12928},
  'total_raw_budgets_locked':locked_raw=={'tight':66573,'laboratory':127143,'stress':348994,'wide':7071771},
 }
 return {'schema':'w33.pass635.joint_optical_eprocess_design.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'design_principle':{'classification':'Maximize the minimum robust KL information per decoded shot over the three Wilson channels.','guard_piggyback':'Both dark guard modes are observed on every Walsh decoding shot, so covariance-sentinel evidence accumulates without a separate acquisition block.','alpha_codesign':'Minimize shared class/guard shots plus reference shots under alpha_class+alpha_guard+alpha_reference=0.01. At the optimum alpha_class=3 exp(-n I_class) and alpha_guard=2 exp(-n I_guard), with the remaining alpha assigned to the phase reference.','raw_photon_conversion':'The correlated optical pair-error bound determines the raw photons required for each decoded Wilson observation at the selected confusion cap.'},
  'profiles':profiles,
  'theorem':'The optical decoder and anytime e-process admit an exact joint design. Across all four hardware profiles the maximin classifier uses only Tr(U) and Tr(U^2); Tr(U^3) receives zero discrimination budget and remains a falsification channel. Dark-guard telemetry piggybacks on every classification shot, so its anytime covariance monitor costs no additional acquisitions. A one-dimensional alpha-allocation optimization and exact vertex enumeration give certified integer channel counts and total raw-photon budgets.',
  'checks':checks,
  'boundary':'The co-design is exact for the declared robust Bernoulli intervals, cube-stationary Gaussian/compound-Poisson decoder bound, and predictable independent shots. Temporal nuisance drift may be handled only when valid conditional intervals are supplied online.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 635 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'allocations':{r['name']:r['integer_design']['trace_channel_shots'] for r in p['profiles']},'raw_budgets':{r['name']:r['total_raw_photon_budget'] for r in p['profiles']}}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
