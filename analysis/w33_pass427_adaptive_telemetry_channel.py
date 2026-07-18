#!/usr/bin/env python3
"""Pass 427: divisor-adaptive protected telemetry over flip/erasure/jitter channels."""
from __future__ import annotations
import argparse,json,math
from collections import Counter
from pathlib import Path
import numpy as np

from w33_pass410_414_common import certificate,write_json
from w33_pass422_telemetry_coding_theorem import hamming_systematic

def round_floats(x,digits=12):
    if isinstance(x,float): return round(x,digits)
    if isinstance(x,list): return [round_floats(v,digits) for v in x]
    if isinstance(x,tuple): return [round_floats(v,digits) for v in x]
    if isinstance(x,dict): return {k:round_floats(v,digits) for k,v in x.items()}
    return x

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass427_adaptive_telemetry_channel.json'
SOURCE=ROOT/'data'/'w33_pass422_telemetry_coding_theorem.json'


def protected_length(k:int)->int:
    if k==0:return 0
    r=1
    while 2**r<k+r+1:r+=1
    return k+r


def success_probability(n:int,p:float,e:float)->float:
    """Probability of a distance-3 guaranteed-correct pattern: t=0,s<=2 or t=1,s=0."""
    if n==0:return 1.0
    good=1-p-e
    if good<0:return 0.0
    no_errors=sum(math.comb(n,s)*e**s*good**(n-s) for s in range(3) if s<=n)
    one_error=n*p*good**(n-1)
    return no_errors+one_error


def histogram(source:dict,ordered:bool)->tuple[Counter,int]:
    h=Counter();total=0
    key='ordered_cumulative' if ordered else 'unordered_cumulative'
    for row in source['divisor_types']:
        size=row[key];bits=0 if size<=1 else math.ceil(math.log2(size));weight=row['divisor_multiplicity']*size
        h[bits]+=weight;total+=weight
    return h,total


def expected_bits(h:Counter,total:int,protected:bool)->float:
    return sum(weight*(protected_length(bits) if protected else bits) for bits,weight in h.items())/total


def evaluate(h:Counter,total:int,fixed:int,p:float,sigma:float,e0:float,guard:float)->dict:
    tail=math.erfc(guard/math.sqrt(2))
    erasure=e0+(1-e0)*tail
    duration=1+2*guard*sigma
    adaptive=0.;unprotected=0.;min_success=1.
    for bits,weight in h.items():
        n=protected_length(bits);s=success_probability(n,p,erasure);min_success=min(min_success,s)
        adaptive+=weight*(0 if n==0 else duration*n/s)
        raw_success=(1-p-erasure)**bits if bits else 1
        unprotected+=weight*(0 if bits==0 else duration*bits/raw_success)
    fixed_success=success_probability(fixed,p,erasure)
    return {'guard_sigma':guard,'jitter_tail_erasure':tail,'total_erasure_probability':erasure,'symbol_duration':duration,
      'adaptive_protected_expected_time':adaptive/total,'adaptive_unprotected_expected_time':unprotected/total,
      'fixed_protected_expected_time':duration*fixed/fixed_success,
      'adaptive_gain_over_fixed':duration*fixed/fixed_success-adaptive/total,
      'minimum_frame_guaranteed_success':min_success,'fixed_frame_guaranteed_success':fixed_success}


def build_payload()->dict:
    source=json.loads(SOURCE.read_text());hu,tu=histogram(source,False);ho,to=histogram(source,True)
    classes=[];all_d3=True
    for k in sorted(set(hu)|set(ho)):
        n=protected_length(k)
        if k:
            H,_=hamming_systematic(k);columns={tuple(H[:,j]) for j in range(n)}
            d3=len(columns)==n and tuple([0]*H.shape[0]) not in columns
        else:d3=True
        all_d3 &= d3
        classes.append({'source_bits':k,'protected_bits':n,'parity_bits':n-k,'minimum_distance':3 if k else None,'fits_bytes':math.ceil(n/8),'distance_three_verified':d3})

    scenarios=[];adaptive_always=True
    for ordered,h,total,fixed in [(False,hu,tu,18),(True,ho,to,21)]:
      for p in (0.0001,0.001,0.005):
       for sigma in (0.05,0.10,0.20):
        for e0 in (0.0,0.001):
         candidates=[evaluate(h,total,fixed,p,sigma,e0,g) for g in (1.5,2.0,2.5,3.0,3.5)]
         best=min(candidates,key=lambda x:(x['adaptive_protected_expected_time'],x['guard_sigma']))
         adaptive_always &= best['adaptive_gain_over_fixed']>0
         scenarios.append({'ordered':ordered,'bit_flip_probability':p,'jitter_sigma_fraction':sigma,'base_erasure_probability':e0,'best':best,
           'candidate_expected_times':[{'guard_sigma':x['guard_sigma'],'adaptive':x['adaptive_protected_expected_time'],'fixed':x['fixed_protected_expected_time']} for x in candidates]})

    checks={
      'source_certificate_passes':source['status']=='PASS',
      'unordered_histories_match':tu==58152160,
      'ordered_histories_match':to==346441915,
      'adaptive_unordered_source_average_3_6356':abs(expected_bits(hu,tu,False)-3.635595410385)<1e-12,
      'adaptive_ordered_source_average_6_6352':abs(expected_bits(ho,to,False)-6.635216954046)<1e-12,
      'adaptive_unordered_protected_average_below_6_82':expected_bits(hu,tu,True)<6.82,
      'adaptive_ordered_protected_average_below_10_64':expected_bits(ho,to,True)<10.64,
      'all_shortened_frames_distance_three':all_d3,
      'worst_unordered_still_18_bits':protected_length(max(hu))==18,
      'worst_ordered_still_21_bits':protected_length(max(ho))==21,
      'all_packets_fit_three_bytes':max(x['protected_bits'] for x in classes)<=24,
      'adaptive_protected_wins_all_36_channel_scenarios':len(scenarios)==36 and adaptive_always,
      'all_selected_guards_from_grid':all(x['best']['guard_sigma'] in (1.5,2.0,2.5,3.0,3.5) for x in scenarios),
    };checks={k:bool(v) for k,v in checks.items()}
    payload={'schema':'w33.pass427.adaptive_telemetry_channel.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{
       'packetization':'the measured divisor determines the exact fibre size and therefore the payload length without an extra prefix header',
       'adaptive_frames':'each payload length k uses the shortest systematic binary Hamming frame satisfying 2^r>=k+r+1',
       'average_lengths':f'unordered protected average {expected_bits(hu,tu,True):.12f} bits; ordered protected average {expected_bits(ho,to,True):.12f} bits',
       'robustness':'every nonempty frame has distance three, guaranteeing one bit correction or two known erasures',
       'jitter_model':'Gaussian timing-tail probability is converted to a known erasure; guard width is chosen by finite expected-time optimization',
       'boundary':'expected-time values use a guaranteed-correct-event repeat metric, not a measured link-layer ARQ implementation; real jitter and correlated errors require device calibration'},
      'source_histograms':{'unordered':{str(k):v for k,v in sorted(hu.items())},'ordered':{str(k):v for k,v in sorted(ho.items())}},
      'average_lengths':{'unordered_source':expected_bits(hu,tu,False),'unordered_protected':expected_bits(hu,tu,True),'unordered_fixed':18,
        'ordered_source':expected_bits(ho,to,False),'ordered_protected':expected_bits(ho,to,True),'ordered_fixed':21},
      'frame_classes':classes,'channel_scenarios':scenarios,'checks':checks}
    payload=round_floats(payload);payload['certificate_sha256']=certificate(payload);return payload


def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 427 certificate drift')
 else:write_json(a.output,p)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
