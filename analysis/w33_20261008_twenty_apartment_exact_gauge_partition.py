"""Exactly soluble pure Z2 and Z3 Wilson plaquette action on selected 20 faces.

Quotienting vertex gauge redundancy gives q^2 flat holonomy sectors per
realizable curvature, because rank H1=2. Relation weights are all units,
so a roots-of-unity filter gives closed finite partition functions.
No dynamics in continuous physical spacetime is inferred.
"""
import json,math,sys,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/"data"
OUT=D/"w33_20261008_twenty_apartment_exact_gauge_partition.json"
def dp(q):
 # DP count of flux configurations indexed by 0..20 nonzero faces and signed total charge mod q
 state={(0,0):1}
 for i in range(20):
  nxt=collections.Counter()
  for (charge,w),n in state.items():
   for x in range(q):
    nxt[((charge+x)%q,w+(x!=0))]+=n
  state=dict(nxt)
 return {str(k):state.get((0,k),0) for k in range(21)}
def main():
 counts2=dp(2);counts3=dp(3)
 assert all(counts2[str(k)]==(math.comb(20,k) if k%2==0 else 0) for k in range(21))
 # nonzero F3 face values +/-1, coefficient orientation signs can be
 # absorbed by bijection x->sign*x; roots-of-unity projection identical.
 def closed3(w):return ((1<<0)*math.comb(20,w)*(2**w+2*(-1)**w))//3
 assert all(counts3[str(k)]==closed3(k) for k in range(21))
 assert sum(counts2.values())==2**19 and sum(counts3.values())==3**19
 # Partition in quotient-of-vertex-gauge configuration space.
 # Each realizable field strength has q^2 gauge orbits.
 def partition(beta,q,c):
  t=math.exp(-beta*(1-math.cos(2*math.pi/q)))
  return (q*q)*sum(n*t**w for w,n in enumerate(c))
 Z2=[counts2[str(i)] for i in range(21)]
 Z3=[counts3[str(i)] for i in range(21)]
 result={"plaquettes":20,"underlying_CW_is_branched_not_a_manifold":True,
 "Z2_curvature_code":"[20,19,2]_2 even parity",
 "Z3_curvature_code":"[20,19,2]_3 single signed face-charge constraint",
 "Z2_exact_face_weight_enumerator":counts2,
 "Z3_exact_face_weight_enumerator":counts3,
 "Z2_reduced_state_count":4*(2**19),
 "Z3_reduced_state_count":9*(3**19),
 "Z2_partition_closed_form":"2*((1+t)^20+(1-t)^20); t=exp(-2*beta)",
 "Z3_partition_closed_form":"3*((1+2*t)^20+2*(1-t)^20); t=exp(-3*beta/2)",
 "Z2_lowest_positive_action":4,
 "Z3_lowest_positive_action":3,
 "beta_1_gauge_quotiented_partition_Z2":partition(1,2,Z2),
 "beta_1_gauge_quotiented_partition_Z3":partition(1,3,Z3),
 "beta_infinity_GSD_Z2":4,
 "beta_infinity_GSD_Z3":9,
 "finite_CW_no_refinement_or_GR_limit_derived":True,
 "interpretation":"Exact finite Wilson action and flat topological sectors of a fixed CW complex. No local relativistic propagating gauge/gravitational degrees of freedom or continuum limit proven."}
 return result
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(json.dumps({k:v for k,v in x.items() if not k.endswith("enumerator")},indent=2),flush=True)
 print("WILSON_PARTITION_PASS")
