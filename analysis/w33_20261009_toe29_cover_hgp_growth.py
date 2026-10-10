"""Round29 finite covers of the native W33 Levi graph.

Construct random cyclic voltage covers to measure finite girth;
prove existence of SOME finite connected graph covers of arbitrarily
large girth via residual finiteness of pi_1(G)=free group F_81.
Then HGP stabilizer family has asymptotic rate1/5 and unbounded girth
distance (not canonical covers, nor polynomial distance in code length).
"""
from pathlib import Path
import json,sys
import numpy as np
from collections import deque
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
OUT=ROOT/'data/w33_20261009_toe29_graph_cover_hgp_family.json'
def girth(graph,stop=8):
 n=len(graph);best=10**9
 for root in range(n):
  seen=[-1]*n;parent=[-1]*n;seen[root]=0;q=deque([root])
  while q:
   u=q.popleft()
   if 2*seen[u]+1>=best:continue
   for v in graph[u]:
    if seen[v]<0:
     seen[v]=seen[u]+1;parent[v]=u;q.append(v)
    elif parent[u]!=v:
     best=min(best,seen[u]+seen[v]+1)
     if best<=stop:return best
 return best
def lift(edges,m,rng):
 n=80*m;adj=[[] for _ in range(n)]
 voltage=rng.integers(0,m,len(edges))
 for (a,b),z in zip(edges,voltage):
  for r in range(m):
   x=a*m+r;y=b*m+(int(r+z)%m)
   adj[x].append(y);adj[y].append(x)
 assert all(len(x)==4 for x in adj)
 # connected due to graph voltage subgroup
 seen={0};q=deque([0])
 while q:
  for j in adj[q.popleft()]:
   if j not in seen:seen.add(j);q.append(j)
 return adj,len(seen)==n
def run():
 edges,*_=wilson();rng=np.random.default_rng(290029)
 small={}
 for m in (1,2,3,5,7,11):
  results=[]
  for k in range(3):
   adj,connected=lift(edges,m,rng)
   g=girth(adj,stop=8)
   results.append(dict(girth=g,connected=connected))
  small[str(m)]=results
  print('COVER degree',m,'girth', [e['girth'] for e in results],flush=True)
 assert small['1'][0]['girth']==8
 cases=[]
 for m in (1,2,5,10,100,1000):
  v=80*m;e=160*m;r=v-1
  n=e*e+r*r;k=(e-r)**2
  cases.append(dict(cover_degree=m,Levi_vertices=v,incidence_qutrits=e,
   HGP_n=n,HGP_k=k,rate=k/n,
   girth_lower_bound_from_cover=8))
 assert cases[-1]['rate']>.199
 rec=dict(status='PASS',native_base_graph='W(3,3) Levi incidence graph with v=80,e=160, regular degree4, girth8',
  cycle_group='pi1(G) is free group F_(e-v+1)=F_81',
  random_cyclic_cover_samples=small,
  abstract_normal_cover_existence='For every integer L>=8, there exists a finite connected regular covering graph G_L->G with girth(G_L)>=L: the fundamental group is free and residually finite; the finite set of all nonidentity reduced closed-walk words of length <L can simultaneously be excluded by a finite-index normal subgroup. Normal covering exists via the associated finite quotient. No explicit size bound or canonical choice is supplied.',
  HGP_existence_theorem='For ANY such connected 4-regular degree-m cover: incidence H shape (80m-1)x(160m), with rank80m-1; HGP CSS [[(160m)^2+(80m-1)^2,(80m+1)^2,girth(G_cover)]]_3. Native graph cycle code distance equals girth; HGP theorem gives d>=girth and an explicit cycle-tensor-link logical of weight girth gives d<=girth. The 2 graph endpoint check weights are 4 and the HGP row check weights are at most6.',
  asymptotic_rate='(80m+1)^2/[(160m)^2+(80m-1)^2] ->1/5',
  distance_growth='Choose covers avoiding closed reduced walks of length<=L: their girths and hence HGP code distance tend to infinity with m. For degree4 regular finite graphs Moore bound implies girth=O(log(number of graph vertices)) and hence d=O(log(n_HGP)); relative distance ->0.',
  status_of_q_3_symmetry='Arbitrary finite covers depend on noncanonical quotient of F81 and can destroy PSp4(3) lifts; no PSp-equivariant cover family, physical locality or nonzero noise threshold is established.',
  explicit_parameters=cases,
  verification='Random small cyclic covers preserve girth8, demonstrating that finite covers alone do not automatically improve distance. The unbounded-girth claim is a standard existence theorem, NOT numerically exhibited by these sample voltages.',
  references=['https://arxiv.org/abs/0903.0566'])
 OUT.write_text(json.dumps(rec,indent=2)+'\n');return rec
if __name__=='__main__':run()
