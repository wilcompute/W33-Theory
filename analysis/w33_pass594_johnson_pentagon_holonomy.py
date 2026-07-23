#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass594_johnson_pentagon_holonomy.json'
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
def order(p):
 q=tuple(range(len(p)))
 for n in range(1,61):
  q=comp(p,q)
  if q==tuple(range(len(p))):return n
 raise AssertionError
def closure(gens):
 I=tuple(range(len(gens[0])));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (comp(a,b),comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def trans(n,a,b):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def cyc(n,c):
 p=list(range(n))
 for a,b in zip(c,c[1:]+c[:1]):p[a]=b
 return tuple(p)
def sylow(B):
 B=tuple(sorted(B));S=set()
 for tail in itertools.permutations(B[1:]):S.add(closure((cyc(8,(B[0],)+tail),)))
 return tuple(sorted(S,key=lambda H:sorted(H)))
def conj(g,H):
 gi=inv(g);return frozenset(comp(comp(g,h),gi) for h in H)
def edge_transport(A,B):
 A=set(A);B=set(B);a=next(iter(A-B));b=next(iter(B-A));outside=sorted(set(range(8))-(A|B));return comp(trans(8,a,b),trans(8,outside[0],outside[1]))
def payload():
 triples=list(itertools.combinations(range(8),3));fib={A:sylow(set(range(8))-set(A)) for A in triples};adj=[[] for _ in triples]
 for i,A in enumerate(triples):
  for j in range(i+1,len(triples)):
   B=triples[j]
   if len(set(A)&set(B))==2:
    g=edge_transport(A,B);adj[i].append((j,g));adj[j].append((i,g))
 def fmap(A,B,g):
  idx={P:i for i,P in enumerate(fib[B])};return tuple(idx[conj(g,P)] for P in fib[A])
 def pc(q,p):return tuple(q[p[i]] for i in range(6))
 path=[None]*56;path[0]=tuple(range(6));Q=deque([0])
 while Q:
  i=Q.popleft();A=triples[i]
  for j,g in adj[i]:
   if path[j] is None:path[j]=pc(fmap(A,triples[j],g),path[i]);Q.append(j)
 loops=[]
 for i,A in enumerate(triples):
  for j,g in adj[i]:loops.append(pc(inv(path[j]),pc(fmap(A,triples[j],g),path[i])))
 H=closure(tuple(set(loops)));triangles=[]
 for i,A in enumerate(triples):
  ed={j:g for j,g in adj[i]};ns=list(ed)
  for j,k in itertools.combinations(ns,2):
   if len(set(triples[j])&set(triples[k]))!=2:continue
   gjk=next(g for x,g in adj[j] if x==k);gki=next(g for x,g in adj[k] if x==i);local=pc(fmap(triples[k],A,gki),pc(fmap(triples[j],triples[k],gjk),fmap(A,triples[j],ed[j])));triangles.append(pc(inv(path[i]),pc(local,path[i])))
 HT=closure(tuple(set(triangles)))
 checks={'Johnson_vertices56':len(triples)==56,'Johnson_degree15':set(len(x) for x in adj)=={15},'six_pentagons_each':all(len(x)==6 for x in fib.values()),'edge_transports_even_A8':all(parity(g)==0 for x in adj for _,g in x),'edge_transports_map_triples':all(tuple(sorted(g[t] for t in triples[i]))==triples[j] for i,x in enumerate(adj) for j,g in x),'connection_reversible':all(fmap(triples[j],triples[i],g)==inv(fmap(triples[i],triples[j],g)) for i,x in enumerate(adj) for j,g in x),'full_holonomy_order120':len(H)==120,'holonomy_element_orders_S5':Counter(order(x) for x in H)==Counter({1:1,2:25,3:20,4:30,5:24,6:20}),'triangle_holonomies_generate_full_group':HT==H,'triangle_holonomies_orders_1_2_3':set(order(x) for x in set(triangles))=={1,2,3},'degree6_action_faithful':len(H)==120}
 return {'schema':'w33.pass594.johnson_pentagon_holonomy.v1','status':'PASS' if all(checks.values()) else 'FAIL','bundle':{'base':'Johnson graph J(8,3)','base_vertices':56,'base_degree':15,'fibre':'six Sylow-5 pentagons on the complementary five-set','total_flags':336},'connection':{'edge_rule':'For adjacent triples exchanging a and b, use (a b) times the transposition of the two smallest points outside their union; this is an even A8 transporter.','reversible':True,'gauge':'spanning-tree trivialization from the canonical triple'},'holonomy':{'order':len(H),'identification':'S5 in its exceptional transitive degree-six action, equivalently PGL(2,5) on P1(F5)','element_order_histogram':dict(sorted(Counter(order(x) for x in H).items())),'distinct_triangle_holonomies':len(set(triangles)),'triangle_order_histogram':dict(sorted(Counter(order(x) for x in set(triangles)).items())),'triangles_generate_full_holonomy':HT==H,'outer_automorphism_seed':'The faithful S5 action on six pentagons is the classical exceptional S5 < S6 action underlying the outer automorphism of S6.'},'interpretation':'The 336 Singer flags form a nontrivial six-state icosahedral/P1(F5) local system over J(8,3). Even the elementary Johnson triangles generate the full S5 fibre holonomy.','checks':checks,'boundary':'The connection depends on the stated canonical edge rule, although its full-holonomy conclusion is gauge invariant for that rule. No equality with the repository 2160-slot Witting holonomy is asserted.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'holonomy':p['holonomy']['order']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
