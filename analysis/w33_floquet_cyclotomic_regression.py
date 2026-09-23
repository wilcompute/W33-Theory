#!/usr/bin/env python3
import json
from math import gcd
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
src=json.loads((ROOT/'data/w33_20260923_next5_plus3_physics_frozen.json').read_text())
h={int(k):v for k,v in src['attack3_global_floquet']['phase_histogram_mod12'].items()}
assert sum(h.values())==248
def divisors(n): return [d for d in range(1,n+1) if n%d==0]
def mobius(n):
 p=0; q=n; d=2
 while d*d<=q:
  if q%d==0:
   q//=d; p+=1
   if q%d==0:return 0
   while q%d==0:q//=d
  d+=1
 return -1 if (p+(q>1))%2 else 1
def ramanujan(d,t): return sum(e*mobius(d//e) for e in divisors(gcd(d,t)))
def phi(d): return sum(gcd(k,d)==1 for k in range(1,d+1))
orders={k:12//gcd(12,k) for k in h}
mult={d:next(iter({h[k] for k in h if orders[k]==d}),0) for d in (1,2,3,4,6,12)}
assert mult=={1:80,2:2,3:27,4:2,6:0,12:27}
traces=[sum(mult[d]*ramanujan(d,t) for d in mult) for t in range(12)]
assert traces==src['attack3_global_floquet']['trace_U_power_t_t0_to11']
fixed=[sum(mult[d]*phi(d) for d in mult if t%d==0) for t in range(1,13)]
assert fixed==src['attack3_global_floquet']['fixed_dimensions_t1_to12']
assert [sum(v for k,v in h.items() if k%3==r) for r in range(3)]==[86,81,81]
assert sum(k*v for k,v in h.items())%12==0
out={'schema':'w33.floquet.cyclotomic.regression.v1','multiplicities':mult,'traces':traces,'fixed_dimensions':fixed,'fi_u4_dimensions':[86,81,81],'determinant_exponent_mod12':0,'phi6_absent':True}
(ROOT/'data/w33_floquet_cyclotomic_regression.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
