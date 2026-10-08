"""Construct and adversarially test the complete 60-qubit/60-ancilla stabilizer readout schedule.

Perfect-check ideal CNOT measurement schedule with 3 X-star matching layers,
8 Z-octagon matching layers (König theorem constructive matching).
Single ancilla fault tail is propagated exactly. This does not prove a
circuit-level threshold; hook faults are explicitly measured.
"""
import sys,json,itertools,collections
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology,add,reduce
OUT=ROOT/"data/w33_20261008_60qubit_full_ancilla_measurement_hook_audit.json"
def schedule(checks,maxweight):
 # König constructive proof: pad 40/20 checks to 60, add dummy multiedges
 # to obtain a 60-by-60 maxweight-regular bipartite multigraph. Remove a
 # perfect matching maxweight times, keeping only physical check edges.
 real={(i,j) for i,row in enumerate(checks) for j in range(60) if row>>j&1}
 mult=collections.Counter({edge:1 for edge in real})
 L=[maxweight]*60;R=[maxweight]*60
 for i,j in real:L[i]-=1;R[j]-=1
 assert min(L)>=0 and min(R)>=0 and sum(L)==sum(R)
 u=v=0
 while u<60 and v<60:
  if L[u]==0:u+=1;continue
  if R[v]==0:v+=1;continue
  t=min(L[u],R[v]);mult[(u,v)]+=t;L[u]-=t;R[v]-=t
 assert all(x==0 for x in L+R)
 layers=[]
 for _ in range(maxweight):
  g=nx.Graph()
  g.add_nodes_from([("c",i) for i in range(60)],bipartite=0)
  g.add_nodes_from([("q",j) for j in range(60)],bipartite=1)
  g.add_edges_from((("c",i),("q",j)) for (i,j),count in mult.items() if count)
  m=nx.algorithms.bipartite.maximum_matching(g,top_nodes={("c",i) for i in range(60)})
  matched=[(c[1],q[1]) for c,q in m.items() if c[0]=="c"]
  assert len(matched)==60 # regular bipartite multigraph => perfect matching
  layer=[]
  for edge in matched:
   mult[edge]-=1
   if edge in real:layer.append(edge);real.remove(edge)
  assert len(layer)==len({i for i,j in layer})==len({j for i,j in layer})
  layers.append(sorted(layer))
 assert not real and all(count==0 for count in mult.values())
 return layers

def main():
 V,E,F,stab,H,b1,b2=topology()
 layersX=schedule(b1,3);layersZ=schedule(b2,8)
 assert sum(map(len,layersX))==120
 assert sum(map(len,layersZ))==160
 assert all(len(layer)==40 for layer in layersX)
 assert all(len(layer)==20 for layer in layersZ)
 # Fault on X ancilla/control propagates X on all remaining data targets;
 # fault Z on Z ancilla/target propagates Z on remaining data controls.
 Xsuffix=[];Zsuffix=[]
 for check,rounds,store in ((b1,layersX,Xsuffix),(b2,layersZ,Zsuffix)):
  byrow=collections.defaultdict(list)
  for layer in rounds:
   for i,j in layer:byrow[i].append(j)
  for i,row in enumerate(check):
   ordered=byrow[i]
   assert sum(1<<j for j in ordered)==row
   for t in range(len(ordered)+1):
    store.append({"check":i,"after_CNOT":t,"propagated_data_support":ordered[t:],
                  "propagated_data_weight":len(ordered)-t})
 # For tails of a single face, Z_stabilizer coset has representative of
 # weight <=4 (either tail or its 8-edge complement).
 Bx={};Bz={}
 for x in b1:add(x,Bx)
 for z in b2:add(z,Bz)
 assert len(Bz)==19
 # Compute all inequivalent Z error cosets at wt<=3.
 seen={}
 for k in range(4):
  for ids in itertools.combinations(range(60),k):
   v=sum(1<<j for j in ids);signature=reduce(v,Bz)
   seen[signature]=min(seen.get(signature,100),k)
 hooks=[]
 for rec in Zsuffix:
  sup=rec["propagated_data_support"]
  v=sum(1<<i for i in sup)
  sig=reduce(v,Bz)
  w=seen.get(sig,min(len(sup),8-len(sup)))
  hooks.append({**rec,"weight_mod_face_stabilizer_upper_bound":min(len(sup),8-len(sup)),
                "reducible_to_weight_3_or_less":sig in seen,
                "exact_minimum_coset_weight_up_to_4":w})
 hist=collections.Counter(row["exact_minimum_coset_weight_up_to_4"] for row in hooks)
 assert max(hist)<=4
 # All single-ancilla X-star hooks are equivalent to wt<=1 modulo a star.
 assert all(min(row["propagated_data_weight"],3-row["propagated_data_weight"])<=1 for row in Xsuffix)
 n4=[x for x in hooks if x["exact_minimum_coset_weight_up_to_4"]==4]
 return {"physical_data_qubits":60,"independent_checks":58,
  "physical_X_ancillas":40,"physical_Z_ancillas":20,
  "total_CNOTs":280,"X_matching_layers":3,"Z_matching_layers":8,
  "nonoverlapping_CNOT_layers_total":11,
  "X_checks_each_weight":3,"Z_checks_each_weight":8,
  "X_check_coupling_incidence_count":120,"Z_check_coupling_incidence_count":160,
  "single_X_ancilla_fault_representative_weight_upper_bound":1,
  "single_Z_ancilla_fault_effective_weight_histogram":dict(hist),
  "single_Z_ancilla_faults_effective_weight4_count":len(n4),
  "single_Z_ancilla_fault_weight4_witness":n4[0] if n4 else None,
  "Z_ancilla_hooks_exceed_unique_Z_correction_radius_3":len(n4)>0,
  "fault_tolerant_syndrome_circuit_proven":False,
  "physical_depolarizing_threshold_proven":False,
  "all_X_layers":[[list(edge) for edge in layer] for layer in layersX],
  "all_Z_layers":[[list(edge) for edge in layer] for layer in layersZ],
  "limitations":"Ideal parallel ancillas and all-to-all check access; sequential X then Z measurements. A single fault on Z face ancilla can cause 4 data Z errors modulo a stabilizer. No timed detector circuit, reset faults or correlated 2-qubit depolarizing noise simulated."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in x.items() if not k.startswith("all_")},flush=True)
 print("CSS_EXTRACTION_HOOK_AUDIT_PASS")
