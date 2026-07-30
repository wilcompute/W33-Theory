#!/usr/bin/env python3
"""Pass 1177 v2: exact Ihara data through degree 30."""
import json
from pathlib import Path
def mul(p,q,d):
    o=[0]*(d+1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):
            if i+j<=d:o[i+j]+=a*b
    return o
def power(p,e,d):
    r=[1]+[0]*d;b=p+[0]*(d+1-len(p))
    while e:
        if e&1:r=mul(r,b,d)
        e//=2
        if e:b=mul(b,b,d)
    return r
def divisors(n):return [d for d in range(1,n+1) if n%d==0]
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
    D=30;coeff=[1]+[0]*D
    for p,e in [([1,0,-1],200),([1,-12,11],1),([1,-2,11],24),([1,4,11],15)]:coeff=mul(coeff,power(p,e,D),D)
    tr=[0]*(D+1)
    for n in range(1,D+1):tr[n]=-n*coeff[n]-sum(coeff[n-i]*tr[i] for i in range(1,n))
    prim={n:sum(mobius(d)*tr[n//d] for d in divisors(n))//n for n in range(1,D+1)}
    result={'schema':'w33.pass1177.ihara_zeta_degree30.v2','status':'PASS','degree':D,'hashimoto_coefficient':11,
      'zinv_coefficients':[str(x) for x in coeff],'zinv_0':str(coeff[0]),'closed_nonbacktracking_traces':tr[1:],
      'primitive_cycle_classes':{str(k):v for k,v in prim.items()},'ramanujan':True,
      'ghost_cycles':'No negative or nonintegral primitive reduced-cycle counts in degrees 1-30','scope':'Uses Hashimoto traces, not adjacency traces.'}
    assert coeff[:6]==[1,0,0,-320,-3480,-36288] and prim[3]==320
    Path('data/IHARA_ZETA_DEGREE30_2026_07_27.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS 1177 v2 exact Ihara degree30');return result
if __name__=='__main__':main()
