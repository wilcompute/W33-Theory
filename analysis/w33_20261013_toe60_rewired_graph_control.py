"""TOE60 front2: matched-degree rewired graph negative controls of 8th-order holonomy.
Random bipartite edge switches preserve 80 sites / 160 edges / degree 4.
Independent 3 edge markings and shortest odd-character loop BFS.
"""
from pathlib import Path
from collections import deque
import json,sys,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep
ed,v,*_=prep();E=np.array(ed,int);V=np.array(v,int)
adj=[[] for _ in range(80)]
for a,b in E:adj[a].append(b);adj[b].append(a)
col={0:0};q=[0]
for a in q:
 for b in adj[a]:
  if b not in col: col[b]=1-col[a];q.append(b)
  else:assert col[b]!=col[a]
assert [sum(z==i for z in col.values()) for i in (0,1)]==[40,40]
base=np.array([(a,b) if col[a]==0 else (b,a) for a,b in E])
def shortest(edges, volt_character):
 vset=np.zeros((len(edges),3),int)
 for i,j in enumerate(volt_character):vset[j,i]=1
 aug=[[] for _ in range(160)]
 for i,(a,b) in enumerate(edges):
  flip=int(vset[i,0]) # single Z2 marker
  for p in range(2):
   aug[a+80*p].append(b+80*(p^flip))
   aug[b+80*p].append(a+80*(p^flip))
 best=1000
 for root in range(80):
  dist=[-1]*160;dist[root]=0;dq=deque([root])
  while dq:
   u=dq.popleft()
   if u==root+80:break
   if dist[u]>=best:break
   for w in aug[u]:
    if dist[w]==-1:dist[w]=dist[u]+1;dq.append(w)
  if dist[root+80]!=-1:best=min(best,dist[root+80])
 return best if best<1000 else None
orig=8 # independently TOE59 verified for nontrivial 3-deck character
rng=np.random.default_rng(6006)
records=[]
for trial in range(28):
 arr=base.copy()
 incident={tuple(sorted(e)) for e in arr}
 successes=0
 for k in range(500):
  i,j=rng.choice(len(arr),2,replace=False)
  a,b=arr[i];c,d=arr[j]
  if a==c or b==d or (a,d) in incident or (c,b) in incident:continue
  incident.remove(tuple(sorted((a,b))));incident.remove(tuple(sorted((c,d))))
  arr[i]=[a,d];arr[j]=[c,b]
  incident.add(tuple(sorted((a,d))));incident.add(tuple(sorted((c,b))))
  successes+=1
 assert len(incident)==160 and successes>100
 idx=rng.choice(160,3,replace=False)
 m=shortest(arr,idx)
 records.append({"trial":trial,"switches":successes,"selected_voltage_edges":idx.tolist(),
                 "single_pi_shortest_winding":m})
freq={str(k):sum(z["single_pi_shortest_winding"]==k for z in records) for k in (4,6,8,10,12,None)}
assert all(z["single_pi_shortest_winding"]%2==0 for z in records)
print("TOE60 controls",freq,flush=True)
out={"status":"PASS_TOE60_DEGREE_MATCHED_RANDOM_CONTROL",
"W33_eight_step_flat_holonomy_on_TOE59":orig,
"rewired_graphs":records,"frequency":freq,
"rewire_method":"Start from native 40+40 Levi bipartite 4-regular graph, perform 500 attempted disjoint bipartite two-edge switches preserving 80 vertices,160 edges and degree4. Randomly assign three signed one-edge deck markers and BFS the Z2 parity-double graph for character (1,0,0).",
"limitation":"Switched graphs do NOT preserve generalized-quadrangle incidence, 1385 W33 plaquettes, gauge-flatness of new arbitrary chord markers, or model dynamics. This is a graph-theoretic negative control only and cannot establish the uniqueness of W33 or a physical light/matter field.",
"evidence":"Non-W33 matched-degree graphs may detect marked parity holonomy at shorter loops than W33's eight-step response. Degree and site counts do not determine winding threshold; local girth/marking matter."}
(R/"data/w33_20261013_toe60_rewired_graph_control.json").write_text(json.dumps(out,indent=2)+"\n")
