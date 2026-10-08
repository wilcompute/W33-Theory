"""Global W33 Levi 8-cycle center gluing criterion and census."""
import json,random,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261008_six_toe_frontier_followthrough import levi_graph
OUT=R/"data"/"w33_20261008_global_cycle_center_census.json"

def cycles():
 G=levi_graph()
 assert len(G)==80 and G.number_of_edges()==160
 nbs={i:sorted(G.neighbors(i)) for i in G}
 out=set()
 for root in range(40):
  def dfs(path):
   if len(path)==8:
    if root in nbs[path[-1]]:
     t=tuple(path)
     r=(t[0],)+tuple(reversed(t[1:]))
     out.add(min(t,r))
    return
   for y in nbs[path[-1]]:
    if y not in path and (y>=40 or y>root):
     dfs(path+[y])
  dfs([root])
 return sorted(out)

def analyze():
 c=cycles();N=len(c)
 assert N>0
 # Complete deterministic census: C(1620,2)=1,311,390 pairs.
 # Two 40-bit masks suffice per cycle; bitcount is exact.
 pm=[];lm=[]
 for cy in c:
  x=y=0
  for v in cy:
   if v<40:x|=1<<v
   else:y|=1<<(v-40)
  pm.append(x);lm.append(y)
 census={};witnesses={};balanced=0
 for i in range(N):
  for j in range(i+1,N):
   npnt=(pm[i]&pm[j]).bit_count()
   nlin=(lm[i]&lm[j]).bit_count()
   imbalance=npnt-nlin
   if imbalance==0:balanced+=1
   key=f"p{npnt}_l{nlin}"
   census[key]=census.get(key,0)+1
   if key not in witnesses:
    witnesses[key]={"cycles":[list(c[i]),list(c[j])],
                    "commutator_rank":0 if imbalance==0 else 2,"imbalance":imbalance}
 assert sum(census.values())==N*(N-1)//2
 # Independent exact 80x80 matrix verification on every distinct
 # intersection signature, including the difficult balanced overlaps.
 for entry in witnesses.values():
  a=set(entry["cycles"][0]);b=set(entry["cycles"][1])
  u=np.zeros(80,dtype=int);v=np.zeros(80,dtype=int)
  sa=np.zeros(80,dtype=int);sb=np.zeros(80,dtype=int)
  for x in a:u[x]=1;sa[x]=1 if x<40 else -1
  for x in b:v[x]=1;sb[x]=1 if x<40 else -1
  A=np.outer(u,sa);B=np.outer(v,sb)
  imbalance=entry["imbalance"]
  actual=A@B-B@A
  assert np.array_equal(actual,imbalance*(np.outer(u,sb)-np.outer(v,sa)))
  assert np.linalg.matrix_rank(actual)==entry["commutator_rank"]
 return {"W33_Levi_vertices":80,"Levi_edges":160,"induced_C8_total":N,
   "all_distinct_cycle_pairs":sum(census.values()),
   "commuting_local_center_pairs":balanced,
   "noncommuting_local_center_pairs":N*(N-1)//2-balanced,
   "intersection_signature_census":dict(sorted(census.items())),
   "representative_witnesses":witnesses,
   "exact_criterion":"[C_A,C_B]=0 iff the cycles share equally many point and line vertices, for distinct induced C8 cycles",
   "consequence":"Local h13 centers cannot be identified as globally central except on balanced-intersection subatlases; no gravitational action claimed"}

if __name__=="__main__":
 x=analyze()
 OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print("CYCLES",x["induced_C8_total"],"PAIRS",x["all_distinct_cycle_pairs"],"BALANCED",x["commuting_local_center_pairs"])
 print("INTERSECTIONS",x["intersection_signature_census"])
 print("GLOBAL_CYCLE_CENTERS_PASS")
