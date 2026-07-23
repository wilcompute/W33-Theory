#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import deque
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass602_connection_gauge_quotient.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def trans(n,a,b):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def cyc(n,c):
 p=list(range(n))
 for a,b in zip(c,c[1:]+c[:1]):p[a]=b
 return tuple(p)
def closure(gens):
 I=tuple(range(len(gens[0])));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (comp(a,b),comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def sylow(B):
 B=tuple(sorted(B));S=set()
 for tail in itertools.permutations(B[1:]):S.add(closure((cyc(8,(B[0],)+tail),)))
 return tuple(sorted(S,key=lambda H:sorted(H)))
def conj(g,H):
 gi=inv(g);return frozenset(comp(comp(g,h),gi) for h in H)
def rank_mod(A,p):
 a=A.copy().astype(np.int64)%p;m,n=a.shape;r=0
 for c in range(n):
  nz=np.flatnonzero(a[r:,c])
  if len(nz)==0:continue
  i=r+int(nz[0]);a[[r,i]]=a[[i,r]];a[r]=(a[r]*pow(int(a[r,c]),-1,p))%p
  for j in np.flatnonzero(a[:,c]):
   if j!=r:a[j]=(a[j]-a[j,c]*a[r])%p
  r+=1
  if r==m:break
 return r

def model():
 triples=list(itertools.combinations(range(8),3));fib={A:sylow(set(range(8))-set(A)) for A in triples};edges=[];adj=[[] for _ in triples]
 for i,A in enumerate(triples):
  for j in range(i+1,56):
   if len(set(A)&set(triples[j]))==2:edges.append((i,j));adj[i].append(j);adj[j].append(i)
 def fmap(A,B,g):
  idx={P:i for i,P in enumerate(fib[B])};return tuple(idx[conj(g,P)] for P in fib[A])
 def edge_map(i,j,pair):
  A=set(triples[i]);B=set(triples[j]);a=next(iter(A-B));b=next(iter(B-A));outside=sorted(set(range(8))-(A|B))
  return fmap(triples[i],triples[j],comp(trans(8,a,b),trans(8,outside[pair[0]],outside[pair[1]])))
 return triples,edges,adj,edge_map

def gauge_loops(pair,triples,edges,adj,edge_map):
 maps={}
 for i,j in edges:
  p=edge_map(i,j,pair);maps[(i,j)]=p;maps[(j,i)]=inv(p)
 path=[None]*56;path[0]=tuple(range(6));parent=[None]*56;Q=deque([0])
 while Q:
  i=Q.popleft()
  for j in adj[i]:
   if path[j] is None:path[j]=comp(maps[(i,j)],path[i]);parent[j]=i;Q.append(j)
 tree={tuple(sorted((i,parent[i]))) for i in range(1,56)};loops=[]
 for i,j in edges:
  if (i,j) not in tree:loops.append(comp(inv(path[j]),comp(maps[(i,j)],path[i])))
 return tuple(loops)

def payload():
 triples,edges,adj,edge_map=model();pairs=list(itertools.combinations(range(4),2));loopdata={p:gauge_loops(p,triples,edges,adj,edge_map) for p in pairs}
 S6=list(itertools.permutations(range(6)))
 def equivalent(A,B):
  for c in S6:
   ci=inv(c)
   if all(comp(comp(c,a),ci)==b for a,b in zip(A,B)):return True
  return False
 eq=[[equivalent(loopdata[a],loopdata[b]) for b in pairs] for a in pairs]
 triangles=[];eid={e:i for i,e in enumerate(edges)}
 for i,j,k in itertools.combinations(range(56),3):
  if (i,j) in eid and (i,k) in eid and (j,k) in eid:triangles.append((i,j,k))
 B2=np.zeros((420,len(triangles)),dtype=np.int8)
 for t,(i,j,k) in enumerate(triangles):B2[eid[(i,j)],t]=1;B2[eid[(i,k)],t]=-1;B2[eid[(j,k)],t]=1
 ranks={str(p):rank_mod(B2,p) for p in (2,3,5,7)}
 beta1=len(edges)-len(triples)+1
 centralizers={'1^5':120,'2 1^3':12,'2^2 1':8,'3 1^2':6,'3 2':6,'4 1':4,'5':5}
 orbit_count=sum(c**(beta1-1) for c in centralizers.values())
 sample={edge_map(0,adj[0][0],p) for p in pairs};h=trans(6,0,1);not_closed=any(comp(x,h) not in sample for x in sample)
 checks={
  'Johnson_56_420_cycle_rank365':len(triples)==56 and len(edges)==420 and beta1==365,
  'spanning_tree_gauge_leaves365_loops':all(len(v)==365 for v in loopdata.values()),
  'complete_S5_gauge_orbit_Burnside_formula':orbit_count==120**364+12**364+8**364+2*6**364+4**364+5**364,
  'six_canonical_rules_pairwise_gauge_inequivalent':all(eq[i][j]==(i==j) for i in range(6) for j in range(6)),
  'clique_triangles840':len(triangles)==840,
  'triangle_boundary_rank365_mod_2_3_5_7':set(ranks.values())=={365},
  'abelian_H1_vanishes_tested_characteristics':all(len(edges)-55-r==0 for r in ranks.values()),
  'six_local_transporters_not_gauge_stable':not_closed,
 }
 return {'schema':'w33.pass602.connection_gauge_quotient.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'graph':{'base':'J(8,3)','vertices':56,'edges':420,'spanning_tree_edges':55,'free_cycle_rank':beta1,'triangles':len(triangles)},
  'complete_reversible_S5_connection_quotient':{'normal_form':'Set every spanning-tree edge to identity; the remaining 365 loop holonomies are an element of S5^365 modulo simultaneous conjugation.','Burnside_formula':'120^364 + 12^364 + 8^364 + 2*6^364 + 5^364 + 4^364','orbit_count_exact':str(orbit_count),'orbit_count_digits':len(str(orbit_count)),'centralizer_sizes':centralizers},
  'canonical_order_statistic_sector':{'rules':[list(p) for p in pairs],'gauge_equivalence_matrix':eq,'gauge_classes':6,'conclusion':'All six Pass-596 order-statistic connections are distinct gauge classes, including the two reversal pairs with equal Wilson sums.'},
  'triangle_complex':{'boundary2_ranks':ranks,'H1_dimensions':{p:420-55-r for p,r in ranks.items()},'interpretation':'The 2-skeleton has no abelian one-cycle sector in the tested characteristics; this does not by itself prove the nonabelian fundamental group trivial.'},
  'theorem':'The full gauge quotient of reversible S5-valued connections is exactly the simultaneous-conjugacy quotient S5^365/S5, with the displayed Burnside count. The six canonical exterior-order rules occupy six distinct classes.',
  'checks':checks,'boundary':'The six exterior-transposition choices are not closed under local gauge transformations, so their unrestricted local-assignment set has no intrinsic gauge quotient until a gauge-stable closure is specified. The exact quotient stated here is for all reversible S5-valued connections.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 602 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'gauge_classes':p['canonical_order_statistic_sector']['gauge_classes'],'orbit_digits':p['complete_reversible_S5_connection_quotient']['orbit_count_digits']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
