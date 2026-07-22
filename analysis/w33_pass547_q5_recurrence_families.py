#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from w33_pass543_547_common import *
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass547_q5_recurrence_families.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2);B=(1,1,2,2,3,3,3,3,2,3,2,2)
def fibs(n):
 F=[0,1]
 while len(F)<=n:F.append(F[-1]+F[-2])
 return F
def lucas(n,F):return 2 if n==0 else F[n-1]+F[n+1]
def vp(n,p):
 if n==0:return 10**9
 v=0
 while n%p==0:n//=p;v+=1
 return v
def real_pair(x):
 assert x[1]==0 and x[2]==x[3]
 return (x[0]-x[2],-x[2])
def real_norm(x):a,b=x;return a*a-a*b-b*b
def real_mul(x,y):
 a,b=x;c,d=y
 return (a*c+b*d,a*d+b*c-b*d)
def real_pow(x,n):
 r=(1,0)
 while n:
  if n&1:r=real_mul(r,x)
  x=real_mul(x,x);n//=2
 return r
def sparse_formula(r,F):return (2*(F[2*r+1]+1),2*F[2*r])
def predicted_sparse_vlambda(m):
 if m%2:return 10**9
 r=m//2
 return 2*m+(2+4*vp(r,5) if r%2 else 0)
def payload():
 C=CycPrime(5);sparse=(1,)+(0,)*11;cpS,tsS,_=charpoly_prime(5,sparse);seqS=recurrence_traces(cpS,tsS,1000,C);F=fibs(2002)
 cpC1,tsC1,_=charpoly_prime(5,(1,)*12);cpC2,tsC2,_=charpoly_prime(5,(2,)*12);seqC1=recurrence_traces(cpC1,tsC1,300,C);seqC2=recurrence_traces(cpC2,tsC2,300,C)
 cpA,tsA,_=charpoly_prime(5,A);cpB,tsB,_=charpoly_prime(5,B);seqA=recurrence_traces(cpA,tsA,300,C);seqB=recurrence_traces(cpB,tsB,300,C)
 sparse_real=[real_pair(x) if any(x) else (0,0) for x in cpS]
 formulas=[];pi=(2,-1)
 for r in range(0,501):
  pair=sparse_formula(r,F);N=real_norm(pair);expectedN=4*lucas(r,F)**2 if r%2==0 else 20*F[r]**2
  actual=(4,0) if r==0 else real_pair(seqS[2*r-1]);expected=real_mul(real_pow(pi,2*r),pair)
  formulas.append({'r':r,'pair':pair,'norm':N,'expected_norm':expectedN,'actual_trace':actual,'expected_trace':expected})
 checks={
  'sparse_charpoly_x5_minus5pi_x3_plus25u_x':sparse_real==[(1,0),(0,0),(-10,5),(0,0),(25,-25),(0,0)],
  'sparse_odd_traces_zero':all(not any(seqS[m-1]) for m in range(1,1001,2)),
  'sparse_closed_form_500':all(formulas[r]['actual_trace']==formulas[r]['expected_trace'] and formulas[r]['norm']==formulas[r]['expected_norm'] for r in range(501)),
  'sparse_valuation_law_1000':all(vlam(seqS[m-1],C)==predicted_sparse_vlambda(m) for m in range(1,1001)),
  'constant_families_galois_conjugate':cpC2==[C.sigma(2,x) for x in cpC1],
  'constant_valuation_sequences_equal_300':all(vlam(x,C)==vlam(y,C) for x,y in zip(seqC1,seqC2)),
  'odd_switch_recurrences_identical':cpA==cpB and tsA==tsB and seqA==seqB,
  'odd_switch_exact_charpoly_degree5':len(cpA)==6 and any(cpA[-1]),
 }
 sample={m:predicted_sparse_vlambda(m) for m in range(2,31)}
 return {'schema':'w33.pass547.q5_recurrence_families.v1','status':'PASS' if all(checks.values()) else 'FAIL','one_pair_theorem':{'characteristic_polynomial':'x(x^4-5*pi*x^2+25*u), t=zeta5+zeta5^-1, pi=2-t, u=1-t, pi^2=5u','power_sum_recurrence':'R_r=5*pi R_(r-1)-25*u R_(r-2), R_r=tr(D^(2r)); odd traces vanish','normalization':'S_r=R_r/pi^(2r)=2(F_(2r+1)+1)+2F_(2r)t','relative_norm':'N(S_r)=4L_r^2 for even r and 20F_r^2 for odd r','all_m_valuation':'v_lambda(tr D^m)=infinity for odd m; for even m=2r it is 2m when r is even, and 2m+2+4v_5(r) when r is odd','sample_m2_to30':sample,'proof_dependency':'Uses the elementary Fibonacci valuation identity v_5(F_r)=v_5(r), derived from rank of apparition 5 and the F_(5n)/F_n identity.'},'constant_family':{'c1_charpoly':cpC1,'c2_charpoly':cpC2,'relation':'sigma_2 Galois conjugate; therefore identical lambda-valuation sequence'},'odd_switch_family':{'charpoly':cpA,'A_equals_B':cpA==cpB,'relation':'The Pass-540 odd icosahedral switch has one shared order-five recurrence for every trace power.'},'checks':checks,'boundary':'An all-exponent valuation theorem is proved for the one-pair orbit. Constant and odd-switch families receive exact recurrences and covariance, but no claimed closed valuation formula.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 547 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
