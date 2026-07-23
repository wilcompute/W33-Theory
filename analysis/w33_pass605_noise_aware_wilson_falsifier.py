#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from pathlib import Path
from statistics import NormalDist
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass605_noise_aware_wilson_falsifier.json'
TRACES={
 'flat_identity':(6,6,6),
 'top_double_transposition':(2,6,2),
 'tetrahedral_fixed_point_free_involution':(0,6,0),
 'top_order_three':(0,0,6),
}
PROBS={'flat_identity':'2/15','top_double_transposition':'2/15','tetrahedral_fixed_point_free_involution':'1/3','top_order_three':'2/5'}

def mean(t,a):return (a*t[0],a*a*t[1],a**3*t[2])
def pairwise(a):
 out={}
 for x,y in itertools.combinations(TRACES,2):out[f'{x}|{y}']=math.dist(mean(TRACES[x],a),mean(TRACES[y],a))
 return out
def shot_bound(a,dark,alpha=.01):
 ds=pairwise(a);pair=min(ds,key=ds.get);dm=ds[pair];z=NormalDist().inv_cdf(1-alpha/3)
 N=math.ceil(24*z*z*(1+2*dark)/(dm*dm))
 return pair,dm,N

def payload():
 alpha=.01;dark=.01;table=[]
 for a in (1.0,.9,.8,.7,.6,.5,.4,.3):
  pair,dm,N=shot_bound(a,dark,alpha);table.append({'coherent_amplitude_retention':a,'limiting_pair':pair,'minimum_Mahalanobis_numerator':dm,'shots_per_trace_for_union_bound_1pct':N})
 crossover=math.sqrt((-9+math.sqrt(113))/16)
 histogram={str(eps):math.ceil(math.log(8/.05)/(2*eps*eps)) for eps in (.05,.03,.02,.01)}
 checks={
  'four_ideal_trace_classes_unique':len(set(TRACES.values()))==4,
  'probabilities_sum_one':2/15+2/15+1/3+2/5==1,
  'scaled_mean_law_a_a2_a3':mean(TRACES['flat_identity'],.5)==(3.0,1.5,.75),
  'limiting_pair_at_unit_retention_is_two_involutions':table[0]['limiting_pair']=='top_double_transposition|tetrahedral_fixed_point_free_involution',
  'unit_retention_23_shots_at_dark1pct':table[0]['shots_per_trace_for_union_bound_1pct']==23,
  'retention08_50_shots_at_dark1pct':table[2]['shots_per_trace_for_union_bound_1pct']==50,
  'crossover_exact_between_limiting_pairs':abs(crossover-0.3191929092193553)<1e-15,
  'below_crossover_order3_pair_limits':table[-1]['limiting_pair']=='tetrahedral_fixed_point_free_involution|top_order_three',
  'histogram_three_percent_2820_loops':histogram['0.03']==2820,
  'shot_requirement_monotone_with_loss':all(table[i]['shots_per_trace_for_union_bound_1pct']<table[i+1]['shots_per_trace_for_union_bound_1pct'] for i in range(len(table)-1)),
 }
 return {'schema':'w33.pass605.noise_aware_wilson_falsifier.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'measurement_model':{'effective_coherent_amplitude_retention':'a = sqrt(power transmission) times coherent visibility per traversal','class_mean':'(a Tr U, a^2 Tr U^2, a^3 Tr U^3)','trace_estimator_variance_bound':'6(1+2d)/N independently for each power trace, where d is dark-count-to-signal variance ratio','classifier':'nearest scaled class mean in Euclidean/Mahalanobis distance'},
  'ideal_classes':{k:{'trace_fingerprint':list(v),'probability':PROBS[k]} for k,v in TRACES.items()},
  'analytic_falsifier':{'familywise_error_target':alpha,'dark_variance_ratio':dark,'normal_union_bound':'3 Phi(-d_min sqrt(N)/(2 sqrt(6(1+2d))))','limiting_pair_crossover_amplitude':crossover,'crossover_exact':'sqrt((-9+sqrt(113))/16)','shot_table':table},
  'histogram_certification':{'method':'simultaneous Hoeffding bound over four classes at 95 percent confidence','shots_for_absolute_frequency_error':histogram},
  'theorem':'Under the stated six-channel Gaussian trace-estimator model, the four Wilson classes remain identifiable at finite loss. The limiting confusion changes at a=sqrt((-9+sqrt(113))/16): above it the two involution classes dominate, below it the fixed-point-free involution and order-three classes dominate.',
  'checks':checks,'boundary':'The thresholds are analytic consequences of the explicitly stated noise model, not vendor-independent laboratory guarantees. Device-specific covariance, phase bias, mode-dependent loss, and detector calibration must replace the conservative variance proxy before an experiment.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 605 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'shot_table':p['analytic_falsifier']['shot_table']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
