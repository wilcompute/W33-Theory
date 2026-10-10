"""Round27 full qutrit CSS ideal-syndrome decoder benchmark.

Two independent ternary syndrome spaces (Wilson for X errors,
vertex Gauss for Z errors), meet-in-the-middle exact radius-three
search and reproducible independent full-qutrit Pauli noise simulations.
Not a circuit-level fault-tolerance demonstration.
"""
from pathlib import Path
from collections import Counter
import math,sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson,selected_basis,MATCHES
OUT=ROOT/'data/w33_20261009_toe27_qutrit_ideal_decoder.json'
class Radius3:
 def __init__(self,H):
  self.H=np.asarray(H,dtype=np.uint8)%3
  self.n=self.H.shape[1]
  self.single=[(e,s,self.H[:,e]*s%3) for e in range(self.n) for s in (1,2)]
  self.by_key={bytes(s):(j,) for j,(_,_,s) in enumerate(self.single)}
  self.pair={}
  for i,(e,_,a) in enumerate(self.single):
   for j in range(i+1,len(self.single)):
    e2,_,b=self.single[j]
    if e==e2:continue
    key=bytes((a+b)%3)
    if key not in self.pair:self.pair[key]=(i,j)
 def decode(self,syndrome):
  y=np.asarray(syndrome,dtype=np.uint8)%3
  if not np.any(y):return np.zeros(self.n,dtype=np.uint8),0
  key=bytes(y)
  if key in self.by_key:choice=self.by_key[key]
  elif key in self.pair:choice=self.pair[key]
  else:
   choice=None
   for j,(_,_,v) in enumerate(self.single):
    k=bytes((y+3-v)%3)
    if k in self.pair:
     choice=self.pair[k]+(j,)
     break
   if choice is None:return None,None
  x=np.zeros(self.n,dtype=np.uint8)
  for j in choice:
   edge,val,_=self.single[j];x[edge]=(x[edge]+val)%3
  if not np.array_equal(self.H.astype(np.int16)@x%3,y):
   raise AssertionError('decoder returned incorrect syndrome')
  return x,int(np.count_nonzero(x))
def run(trials=500):
 ed,D,C=wilson();f=np.zeros(160,dtype=np.int16);f[MATCHES[8]]=1
 mask=C.astype(np.int16)@f%3==0
 S=C[mask]
 b=selected_basis(S)
 assert len(b)==80
 Hx=(S[b].astype(np.int16)%3).astype(np.uint8)
 Hz=(D[:-1].astype(np.int16)%3).astype(np.uint8)
 assert Hz.shape==(79,160)
 dx=Radius3(Hx);dz=Radius3(Hz)
 tests=[]
 rng=np.random.default_rng(20261009)
 for w in (0,1,2,3):
  for k in range(20):
   x=np.zeros(160,dtype=np.uint8);z=np.zeros(160,dtype=np.uint8)
   supp=rng.choice(160,size=w,replace=False)
   for edge in supp:
    a,b=rng.integers(0,3,size=2)
    while not (a or b):a,b=rng.integers(0,3,size=2)
    x[edge]=a;z[edge]=b
   xhat,_=dx.decode(Hx.astype(np.int16)@x%3)
   zhat,_=dz.decode(Hz.astype(np.int16)@z%3)
   # Decode only up to stabilizer equivalence: weight-four Gauss stars
   # can relate distinct weight-three X errors of the same syndrome.
   xr=(x.astype(np.int16)-xhat.astype(np.int16))%3
   zr=(z.astype(np.int16)-zhat.astype(np.int16))%3
   assert (not np.any(C.astype(np.int16)@xr%3)
           and not np.any(D.astype(np.int16)@zr%3)
           and int(f@zr)%3==0),(w,k)
  tests.append(dict(error_support_size=w,trials=20,recovered_all=True))
 records={}
 for p in (.002,.005,.01,.02):
  fail=Counter();counts=Counter()
  for j in range(trials):
   x=np.zeros(160,dtype=np.uint8);z=np.zeros(160,dtype=np.uint8)
   sites=np.flatnonzero(rng.random(160)<p)
   for edge in sites:
    a,b=rng.integers(0,3,size=2)
    while not(a or b):a,b=rng.integers(0,3,size=2)
    x[edge]=a;z[edge]=b
   xx,wx=dx.decode(Hx.astype(np.int16)@x%3)
   zz,wz=dz.decode(Hz.astype(np.int16)@z%3)
   ok=False
   if xx is not None and zz is not None:
    xr=(x.astype(np.int16)-xx.astype(np.int16))%3
    zr=(z.astype(np.int16)-zz.astype(np.int16))%3
    ok=(not np.any(C.astype(np.int16)@xr%3)
        and not np.any(D.astype(np.int16)@zr%3)
        and int(f@zr)%3==0)
   counts[len(sites)]+=1
   if not ok:fail['total']+=1
   if len(sites)<=3:assert ok
  tail=sum(math.comb(160,k)*p**k*(1-p)**(160-k) for k in range(4,161))
  assert fail['total']/trials <= tail+max(.055,3*math.sqrt(tail*(1-tail)/trials))
  records[str(p)]=dict(trials=trials,physical_Pauli_error_probability=p,
   logical_recovery_failure_count=int(fail['total']),
   empirical_failure_fraction=fail['total']/trials,
   empirical_error_weight_counts={str(k):v for k,v in sorted(counts.items())},
   binomial_P_at_least_four_errors=float(tail))
  print('QUTRIT DECODER',p,'failure',fail['total'],'/',trials,'P>=4',round(tail,6),flush=True)
 result=dict(status='PASS',code='[[160,1,8]]_3',
  check_matrix_dimensions={'X_error_Wilson_H':list(Hx.shape),
                           'Z_error_Gauss_H':list(Hz.shape)},
  shortest_recovery_radius=3,
  decoder='Exact meet-in-the-middle ternary syndrome lookup: precompute 320 one-link syndromes and at most 50,880 two-link syndromes, search up to a third link; separate X/Z CSS channels.',
  syndrome_columns_nonzero_and_unique_X=len(dx.by_key)==320,
  syndrome_columns_nonzero_and_unique_Z=len(dz.by_key)==320,
  exact_radius_tests=tests,
  iid_depolarizing_8_Paulis_samples=records,
  upper_bound_circuit_FREE='Any arbitrary Pauli error on at most 3 physical qutrits is corrected up to its stabilizer class by this ideal-syndrome decoder, since each component X/Z has weight <=3. Under independent p total nonidentity errors, logical failure is bounded by Binomial(160,p) tail >=4. This is a perfect-syndrome data-error-only statement, not a threshold.',
  limitations='Decoder assumes noiseless Gauss/Wilson syndrome and connectivity to all 159 independent stabilizers; ignores hook errors, ancilla faults, measurement noise, correlated loss/leakage and decoding latency. Not a fault-tolerant threshold.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':run()
