#!/usr/bin/env python3
"""Pass 1883: complete MacWilliams transform and exact shell design strength."""
from __future__ import annotations
import hashlib,json,math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/w33_pass1876_exact_dual_weight_enumerator.json'
OUT=ROOT/'data/w33_pass1883_full_primal_weight_enumerator.json'
N=240

def kraw(j,w):
 lo=max(0,j-(N-w));hi=min(j,w)
 return sum((-1)**i*math.comb(w,i)*math.comb(N-w,j-i) for i in range(lo,hi+1))

def canonical_hash(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 src=json.loads(SRC.read_text());dual={int(k):v for k,v in src['dual_weight_enumerator'].items()}
 primal={}
 for j in range(N+1):
  num=sum(B*kraw(j,w) for w,B in dual.items());assert num%(1<<45)==0;primal[j]=num//(1<<45)
 shells={}
 for w in (12,14,16):
  A=primal[w];l1=Fraction(A*w,N);l2=Fraction(A*math.comb(w,2),math.comb(N,2))
  shells[str(w)]={'blocks':A,'lambda1':l1.numerator,'lambda2_numerator':l2.numerator,'lambda2_denominator':l2.denominator,'exact_design_strength':1,'reason_not_2_design':f'lambda_2={l2.numerator}/{l2.denominator} is nonintegral'}
 checks={
  'dual_total_2pow45':sum(dual.values())==1<<45,
  'primal_total_2pow195':sum(primal.values())==1<<195,
  'all_odd_coefficients_zero':all(primal[i]==0 for i in range(1,N+1,2)),
  'minimum_distance_4':primal[1]==primal[2]==primal[3]==0 and primal[4]>0,
  'known_low_coefficients':[primal[i] for i in (4,6,8,10,12)]==[540,9600,424170,17523360,891792940],
  'complement_symmetry':all(primal[i]==primal[N-i] for i in range(N+1)),
  'shell12_not_2design':shells['12']['lambda2_denominator']!=1,
  'shell14_not_2design':shells['14']['lambda2_denominator']!=1,
  'shell16_not_2design':shells['16']['lambda2_denominator']!=1}
 out={'schema':'w33.pass1883.full_primal_weight_enumerator.v1','status':'PASS','length':N,'dimension':195,'dual_dimension':45,'primal_weight_enumerator':{str(k):v for k,v in primal.items() if v},'checks':checks,'shell_designs':shells,'theorem':'The complete primal [240,195,4] enumerator is the exact MacWilliams transform of the frozen 2^45-word dual histogram. Edge transitivity makes every nonempty shell a 1-design; the weight-12, 14, and 16 shells are not 2-designs because their required pair multiplicities are nonintegral.','boundary':'The design-strength statement is exact for weights 12,14,16. No higher-design claim is inferred from the univariate enumerator alone.'}
 assert all(checks.values()),{k:v for k,v in checks.items() if not v}
 out['sha256_without_hash_field']=canonical_hash(out);OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'status':'PASS','A12':primal[12],'A14':primal[14],'A16':primal[16],'sha256':out['sha256_without_hash_field']},indent=2));return out
if __name__=='__main__':main()
