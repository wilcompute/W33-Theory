#!/usr/bin/env python3
"""Pass4834: exact six-layer mixed schedule for the [2025,399,14]_2 code.
The six W6 global checks always form K6.  Local checks live in 135 disjoint
15-coordinate cells, so after pinning the global colors 0..5 the remaining
problem is 135 independent exact list-colorings of 12 local checks.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle
from w33_pass4819_4822_outer_code_levi_classification import Qm,nullspace
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4834_CODE399_OPTIMAL_MIXED_SCHEDULE.json'

def rank2(V):
 p={}
 for x in V:
  y=int(x)
  while y:
   k=y.bit_length()-1
   if k in p:y^=p[k]
   else:p[k]=y;break
 return len(p)

def color_cell(R,G):
 n=len(R);A=[set() for _ in R];L=[]
 for i,j in itertools.combinations(range(n),2):
  if R[i]&R[j]:A[i].add(j);A[j].add(i)
 for r in R:
  z=[c for c,g in enumerate(G) if not(r&g)]
  if not z:return None
  L.append(z)
 C=[-1]*n
 def dfs(done):
  if done==n:return True
  U=[i for i in range(n) if C[i]<0]
  i=min(U,key=lambda u:(len([c for c in L[u] if c not in {C[v] for v in A[u] if C[v]>=0}]),-len(A[u])))
  used={C[v] for v in A[i] if C[v]>=0}
  for c in L[i]:
   if c in used:continue
   C[i]=c
   if dfs(done+1):return True
   C[i]=-1
  return False
 return C if dfs(0) else None

def main():
 D=build_all();B=build_bundle();rm=D['rmasks'];U=D['cube_unions'];cubeR=D['cube_residues'];N=np.asarray(D['selected_incidence']);phiU=D['phiU'];phiR=D['phiR'];K5=B['K5'];packets=B['packets']
 hot={tuple(sorted(e)) for e in B['hot']};cold={tuple(sorted(e)) for e in B['cold']};router=hot|cold
 owner=[]
 for T in B['projected']:
  h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
 packet_of={s:p for p,T in enumerate(packets) for s in T};u2r={}
 for R in cubeR:
  u=0
  for r in R:u|=rm[r]
  u2r[u]=tuple(R)
 cells={}
 for ui,u in enumerate(U):
  s=phiU[ui];inc=set(np.flatnonzero(N[s]).tolist());p=packet_of[s];F=sorted(i for i,S in enumerate(K5) if p in S);groups={f:sorted(v for v in inc if owner[v]==f) for f in F};H=sorted({tuple(sorted(groups[f])) for f in F});blocks={}
  for a,b in itertools.combinations(F,2):blocks[(a,b)]=sorted(tuple(sorted((x,y))) for x in groups[a] for y in groups[b])
  cells[s]=(F,H,blocks)
 edges=sorted(router);ei={e:i for i,e in enumerate(edges)};bit=lambda e:1<<ei[e]
 local={};byline=defaultdict(list);gp={}
 for s,(F,H,blocks) in sorted(cells.items()):
  rows=[];info={}
  for pair,E in sorted(blocks.items()):
   e0,e1,e2,e3=E;rows += [bit(e0)^bit(e1),bit(e1)^bit(e2),bit(e2)^bit(e3)];L=next(iter(set(F)-set(pair)));info[L]=(E,e0,e3)
  h0,h1,h2=H;rows += [bit(h0)^bit(h1),bit(h1)^bit(h2)];r=bit(h0)
  for L in F:r^=bit(info[L][1])
  rows.append(r);assert len(rows)==12 and rank2(rows)==12;local[s]=rows
  for L in F:
   E,e0,e3=info[L];j=sum(len(x) for x in byline.values());byline[L].append(j);gp[j]=bit(e3)
 assert sum(map(len,local.values()))==1620
 supports=[]
 for R in local.values():
  z=0
  for r in R:z|=r
  supports.append(z)
 assert all(not(a&b) for a,b in itertools.combinations(supports,2))
 qp=[x for x in range(1,64) if Qm(x)==0];ql=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if (a^b) in qp});Lgeo=[tuple(i for i,Q in enumerate(ql) if p in Q) for p in qp];inc=[sum(1<<i for i,S in enumerate(Lgeo) if p in S) for p in range(45)];W6=nullspace(inc,27);assert len(W6)==6
 W=[0]
 for b in W6:W += [x^b for x in W]
 assert {x.bit_count() for x in W if x}=={12,16} and all(a&b for a,b in itertools.combinations([x for x in W if x],2))
 line=[]
 for L in range(27):
  r=0
  for j in byline[L]:r^=gp[j]
  assert r.bit_count()==15;line.append(r)
 G=[]
 for h in W6:
  r=0
  for L in range(27):
   if(h>>L)&1:r^=line[L]
  G.append(r)
 assert all(a&b for a,b in itertools.combinations(G,2))
 assign={};profiles=Counter()
 for s,R in sorted(local.items()):
  c=color_cell(R,G);assert c is not None,s;assign[s]=c;profiles[tuple(sorted(Counter(c).items()))]+=1
 layers=[[G[c]] for c in range(6)]
 for s,R in sorted(local.items()):
  for r,c in zip(R,assign[s]):layers[c].append(r)
 for R in layers:
  z=0
  for r in R:assert not(z&r);z|=r
 allrows=[r for R in local.values() for r in R]+G;assert len(allrows)==1626 and rank2(allrows)==1626
 out={'pass':4834,'code':'[2025,399,14]_2','check_rank':1626,'global_basis_independent_lower_bound':6,'global_conflict_graph':'K6 for every W6 basis','optimal_mixed_depth':6,'globally_optimal_in_conflict_model':True,'checks_per_layer':[len(x) for x in layers],'cell_color_profile_census':{str(k):v for k,v in profiles.items()},'decoder_radius_preserved':6,'theorem':'Six layers are necessary for every W6 basis and sufficient: the canonical global basis extends to an exact six-coloring of all 1620 local checks, solved independently on the 135 disjoint cells.','boundary':'Optimal only in the one-check-per-coordinate-per-layer parity-check conflict model; no noisy-syndrome or hardware threshold claim.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
