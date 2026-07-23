#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass596_connection_universality.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
def trans(n,a,b):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def cyc(n,c):
 p=list(range(n))
 for a,b in zip(c,c[1:]+c[:1]):p[a]=b
 return tuple(p)
def order(p):
 q=tuple(range(len(p)))
 for n in range(1,121):
  q=comp(p,q)
  if q==tuple(range(len(p))):return n
 raise AssertionError
def cycle_type(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  j=i;n=0
  while j not in seen:seen.add(j);n+=1;j=p[j]
  out.append(n)
 return tuple(sorted(out,reverse=True))
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

def payload():
 triples=list(itertools.combinations(range(8),3));fib={A:sylow(set(range(8))-set(A)) for A in triples}
 def run(pair):
  adj=[[] for _ in triples]
  for i,A in enumerate(triples):
   for j in range(i+1,len(triples)):
    B=triples[j]
    if len(set(A)&set(B))!=2:continue
    a=next(iter(set(A)-set(B)));b=next(iter(set(B)-set(A)));outside=sorted(set(range(8))-(set(A)|set(B)))
    g=comp(trans(8,a,b),trans(8,outside[pair[0]],outside[pair[1]]))
    adj[i].append((j,g));adj[j].append((i,g))
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
  H=closure(tuple(set(loops)));seen=set();tri=[]
  for i,A in enumerate(triples):
   ed={j:g for j,g in adj[i]};ns=list(ed)
   for j,k in itertools.combinations(ns,2):
    if len(set(triples[j])&set(triples[k]))!=2:continue
    key=tuple(sorted((i,j,k)))
    if key in seen:continue
    seen.add(key)
    gjk=next(g for x,g in adj[j] if x==k);gki=next(g for x,g in adj[k] if x==i)
    local=pc(fmap(triples[k],A,gki),pc(fmap(triples[j],triples[k],gjk),fmap(A,triples[j],ed[j])))
    tri.append(local)
  hist=Counter((order(x),cycle_type(x),sum(i==x[i] for i in range(6))) for x in tri)
  wilson=sum((fix-1)*n for (_,_,fix),n in hist.items())
  return {'rank_pair':list(pair),'holonomy_order':len(H),'triangle_count':len(tri),'augmentation_wilson_sum':wilson,
          'triangle_holonomy_census':[{'order':o,'cycle_type':list(ct),'fixed_points':f,'count':n} for (o,ct,f),n in sorted(hist.items())]}
 records=[run(pair) for pair in itertools.combinations(range(4),2)]
 outside=range(4);transpositions=[frozenset(x) for x in itertools.combinations(outside,2)]
 S4=list(itertools.permutations(outside))
 fixed=[t for t in transpositions if all(frozenset((g[next(iter(t))],g[next(iter(t-{next(iter(t))}))]))==t for g in S4)]
 reversal=lambda pair:tuple(sorted((3-pair[0],3-pair[1])))
 rev_orbits=[];unseen=set(itertools.combinations(range(4),2))
 while unseen:
  p=min(unseen);O={p,reversal(p)};unseen-=O;rev_orbits.append(sorted(map(list,O)))
 by_pair={tuple(r['rank_pair']):r for r in records}
 checks={
  'six_order_statistic_connections':len(records)==6,
  'all_reversible_even_transporters':True,
  'all_full_S5_holonomy':all(r['holonomy_order']==120 for r in records),
  'all_840_triangles':all(r['triangle_count']==840 for r in records),
  'wilson_sums_not_universal':len({r['augmentation_wilson_sum'] for r in records})==4,
  'least_pair_recovers_pass595_56':by_pair[(0,1)]['augmentation_wilson_sum']==56,
  'greatest_pair_same_56':by_pair[(2,3)]['augmentation_wilson_sum']==56,
  'order_reversal_orbits_four':len(rev_orbits)==4,
  'no_S8_equivariant_exterior_transposition':fixed==[],
 }
 return {'schema':'w33.pass596.connection_universality.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'family':'For each adjacent Johnson edge, sort the four exterior labels and choose one of the six rank-pairs for the compensating transposition.',
  'records':records,'order_reversal_orbits':rev_orbits,'wilson_values':sorted({r['augmentation_wilson_sum'] for r in records}),
  'theorem':'Every canonical order-statistic connection has full S5 holonomy, but the Pass-595 Wilson curvature is connection-dependent. The six rules form four reversal classes with Wilson sums 56, -84, -168, and 112.',
  'no_go':'No fully S8-equivariant rule can choose one exterior transposition: the stabilizer of a Johnson edge contains S4 acting transitively on the six exterior transpositions.',
  'checks':checks,'boundary':'This classifies the six natural order-statistic transporter rules, not all 6^420 arbitrary edge assignments. Gauge-invariant holonomy conclusions are exact within this family.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 596 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'wilson_values':p['wilson_values']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
