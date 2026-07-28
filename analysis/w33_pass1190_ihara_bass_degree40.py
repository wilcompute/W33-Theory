#!/usr/bin/env python3
"""Pass 1190: exact Ihara--Bass expansion and primitive cycles through degree 40."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1190_ihara_bass_degree40.json'
DEGREE=40

def mul(p,q,d):
    out=[0]*(d+1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):
            if i+j<=d: out[i+j]+=a*b
    return out

def power(poly,e,d):
    r=[1]+[0]*d;b=poly+[0]*(d+1-len(poly))
    while e:
        if e&1:r=mul(r,b,d)
        e//=2
        if e:b=mul(b,b,d)
    return r

def divisors(n): return [d for d in range(1,n+1) if n%d==0]
def mobius(n):
    if n==1:return 1
    m=n;p=0;d=2
    while d*d<=m:
        if m%d==0:
            m//=d;p+=1
            if m%d==0:return 0
            while m%d==0:m//=d
        d+=1
    if m>1:p+=1
    return -1 if p%2 else 1

def main():
    coeff=[1]+[0]*DEGREE
    for poly,e in [([1,0,-1],200),([1,-12,11],1),([1,-2,11],24),([1,4,11],15)]:
        coeff=mul(coeff,power(poly,e,DEGREE),DEGREE)
    tr=[0]*(DEGREE+1)
    for n in range(1,DEGREE+1):
        tr[n]=-n*coeff[n]-sum(coeff[n-i]*tr[i] for i in range(1,n))
    primitive={n:sum(mobius(d)*tr[n//d] for d in divisors(n))//n for n in range(1,DEGREE+1)}
    prefix=[1,0,0,-320,-3480,-36288,-251840,-1626240,-9084540,-44369280,-182477184]
    assert coeff[:11]==prefix
    assert tr[1:11]==[0,0,960,13920,181440,1818240,19178880,214015200,2359466880,25940386560]
    assert primitive[3]==320 and primitive[4]==3480 and primitive[5]==36288
    assert all(isinstance(v,int) and v>=0 for v in primitive.values())
    result={'schema':'w33.pass1190.ihara_bass_degree40.v1','status':'PASS','degree':40,
      'hashimoto_quadratic_coefficient':11,
      'formula':'det(I-uB)=(1-u^2)^200(1-12u+11u^2)(1-2u+11u^2)^24(1+4u+11u^2)^15',
      'inverse_ihara_coefficients':coeff,
      'closed_nonbacktracking_traces':{str(n):tr[n] for n in range(1,41)},
      'primitive_reduced_cycle_classes':{str(n):primitive[n] for n in range(1,41)},
      'mobius_identity':'Tr(B^n)=sum_{d|n} d*pi_d',
      'checks':{'coefficient_is_k_minus_one':True,'degree10_prefix_locked':coeff[:11]==prefix,
                'no_lengths_1_or_2':primitive[1]==primitive[2]==0,'primitive_triangles':primitive[3]==320,
                'all_counts_integral_nonnegative':all(isinstance(v,int) and v>=0 for v in primitive.values())},
      'scope':'Ihara prime reduced-cycle classes from Hashimoto traces, not ordinary adjacency traces.'}
    assert all(result['checks'].values())
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS 1190 exact Ihara degree40 primitive cycles locked')
    return result
if __name__=='__main__':main()
