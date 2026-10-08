"""Exact small-weight X-distance exclusion, independently of the MILP solver.

All weight<=5 cocycles checked by meet-in-the-middle of stabilizer syndrome
and nontrivial evaluation on the two stored logical homology classes.
"""
import json,collections,itertools,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology,add,nullspace
D=ROOT/"data";OUT=D/"w33_20261008_binary_CSS_exhaustive_distance.json"
def main():
 _,E,_,_,_,b1,b2=topology()
 B={}
 for r in b2:add(r,B)
 Z=[]
 for v in nullspace(b1,60):
  if add(v,B):Z.append(v)
 assert len(Z)==2
 cols=[]
 for i in range(60):
  sy=sum((1<<j) for j,r in enumerate(b2) if (r>>i)&1)
  log=sum((1<<j) for j,r in enumerate(Z) if (r>>i)&1)
  cols.append((sy,log))
 def fingerprint(q):
  s=l=0
  for i in q:
   a,b=cols[i];s^=a;l^=b
  return s,l
 counts={}
 for k in (1,2,3):
  n=0
  for q in itertools.combinations(range(60),k):
   s,l=fingerprint(q)
   if not s and l:raise AssertionError((k,q,l))
   n+=1
  counts[str(k)]=n
 pairs=collections.defaultdict(list)
 for q in itertools.combinations(range(60),2):
  a,b=fingerprint(q);pairs[a].append((q,b))
 def check(q,k):
  a,b=fingerprint(q)
  for p,c in pairs.get(a,()):
   if not (set(q)&set(p)):
    if b^c:raise AssertionError(("nontrivial_below6",k,q,p))
 for q in itertools.combinations(range(60),2):check(q,4)
 for q in itertools.combinations(range(60),3):check(q,5)
 counts["4_via_2plus2"]=1770
 counts["5_via_3plus2"]=34220
 # Read independently MILP-validated sixth-weight witness, test check parity
 milp=json.loads((D/"w33_20261008_twenty_apartment_X_cosystole.json").read_text())
 x=min((r["X_operator_support_edge_indices"] for r in milp["logical_operators"]),key=len)
 assert len(x)==6
 assert fingerprint(x)[0]==0 and fingerprint(x)[1]!=0
 out={"n":60,"k":2,"distance_X_exact":6,"distance_Z_exact":8,
      "overall_css_distance_exact":6,
      "two_logical_cycle_basis_weights":[z.bit_count() for z in Z],
      "all_X_cocycles_weight_below_six_are_stabilizer_or_zero":True,
      "weight_le_three_direct_enumerated":counts,
      "X_weight6_witness_indices":x,
      "X_weight6_witness_nonzero_logical_pairing":fingerprint(x)[1],
      "method":"all weights 1-3 direct, weight4=2+2 and weight5=3+2 syndrome meet-in-middle; MILP independent weight6 witness and length8 lifted-cover BFS from prior producer",
      "no_claim_on_technical_fault_tolerance_threshold":True}
 return out
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps(r,indent=2),flush=True);print("BINARY_DISTANCE_EXHAUSTIVE_PASS",flush=True)
