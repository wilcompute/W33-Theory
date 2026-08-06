#!/usr/bin/env python3
"""Pass 4001: exact structural identification of the three maximum-code stabilizers."""
from __future__ import annotations
import hashlib, importlib.util, itertools, json, math
from collections import Counter, deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4001_CODE_STABILIZER_IDENTIFICATION.json'

def load_base():
 p=ROOT/'analysis/w33_pass3991_maximum_code_orbit_census.py'
 spec=importlib.util.spec_from_file_location('base3991',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def inv(p):
 r=[0]*len(p)
 for i,x in enumerate(p):r[x]=i
 return tuple(r)
def order(p):
 seen=set();o=1
 for i in range(len(p)):
  if i not in seen:
   j=i;n=0
   while j not in seen:seen.add(j);j=p[j];n+=1
   o=math.lcm(o,n)
 return o
def closure(gens,compose,n=36):
 e=tuple(range(n));S={e};q=deque([e]);moves=list(gens)+[inv(g) for g in gens]
 while q:
  x=q.popleft()
  for g in moves:
   y=compose(g,x)
   if y not in S:S.add(y);q.append(y)
 return S
def dist(G):return {str(k):v for k,v in sorted(Counter(order(g) for g in G).items())}
def orbits(G,n=36):
 rem=set(range(n));out=[]
 while rem:
  a=min(rem);O={g[a] for g in G};out.append(sorted(O));rem-=O
 return sorted(out,key=lambda x:(len(x),x))
def restrict(p,O):
 idx={x:i for i,x in enumerate(O)};return tuple(idx[p[x]] for x in O)
def kernel(G,O):return {g for g in G if all(g[x]==x for x in O)}
def image(G,O):return {restrict(g,O) for g in G}
def greedy(G,compose,n=36):
 e=tuple(range(n));H={e};gs=[]
 for g in sorted(G,key=order,reverse=True):
  if g not in H:gs.append(g);H=closure(gs,compose,n)
  if len(H)==len(G):break
 return gs
def comm(a,b,compose):return compose(compose(compose(inv(a),inv(b)),a),b)
def derived(G,gens,compose,n=36):
 H=closure([comm(a,b,compose) for a in gens for b in gens],compose,n)
 changed=True
 while changed:
  changed=False;more=[]
  for x in H:
   for g in gens:
    y=compose(compose(g,x),inv(g))
    if y not in H:more.append(y)
  if more:H=closure(list(H)+more,compose,n);changed=True
 return H
def center(G,gens,compose):return {x for x in G if all(compose(x,g)==compose(g,x) for g in gens)}
def find_complement(G,K,compose,target=24):
 K=set(K);E=list(G)
 for a in E:
  if a in K:continue
  for b in E:
   if b in K:continue
   H=closure([a,b],compose)
   if len(H)==target and len(H&K)==1:return H
 for a,b,c in itertools.combinations(E,3):
  H=closure([a,b,c],compose)
  if len(H)==target and len(H&K)==1:return H
 raise AssertionError('no complement')
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 m=load_base();ns,words,adj=m.build_graph();cgens=m.coordinate_generators(ns);G=m.generate_group(cgens);wgens=m.induced_word_generators(words,cgens)
 oa=m.orbit_point(0,wgens);ob=m.orbit_point(next(iter(set(range(945))-oa)),wgens);o135=min([oa,ob],key=len);anchor=min(o135)
 sols,_=m.enumerate_with_anchor(anchor,adj,o135)
 c3=next(c for c in sols if len(set(c)&o135)==3);O3=m.orbit_clique(c3,wgens)
 c15a=next(c for c in sols if len(set(c)&o135)==15);O15a=m.orbit_clique(c15a,wgens)
 c15b=next(c for c in sols if len(set(c)&o135)==15 and c not in O15a);O15b=m.orbit_clique(c15b,wgens)
 reps=[('orbit_540',c3,540),('orbit_270',c15a,270),('orbit_135',c15b,135)]
 records=[]
 for name,rep,osize in reps:
  S={words[i] for i in rep};stab={p for p in G if {m.permute_word(w,p) for w in S}==S};gens=greedy(stab,m.compose);Z=center(stab,gens,m.compose);D1=derived(stab,gens,m.compose);D2=derived(D1,greedy(D1,m.compose),m.compose);D3=derived(D2,greedy(D2,m.compose),m.compose)
  Os=orbits(stab);proof={};identified=''
  if name in ('orbit_540','orbit_270'):
   six=next(x for x in Os if len(x)==6);Im=image(stab,six);K=kernel(stab,six);H=find_complement(stab,K,m.compose)
   assert len(Im)==24 and dist(Im)=={'1':1,'2':9,'3':8,'4':6}
   if name=='orbit_540':
    assert dist(K)=={'1':1,'2':3} and all(m.compose(h,k)==m.compose(k,h) for h in H for k in K)
    identified='S4 x V4';proof={'six_point_image':'S4','kernel':'V4','complement_order':24,'direct_product_commutation':True}
   else:
    assert dist(K)=={'1':1,'2':5,'4':2}
    centralizer={h for h in H if all(m.compose(m.compose(h,k),inv(h))==k for k in K)}
    assert len(centralizer)==12 and dist(centralizer)=={'1':1,'2':3,'3':8}
    identified='D8 semidirect_{sign,alpha} S4';proof={'six_point_image':'S4','kernel':'D8','complement_order':24,'action_kernel':'A4','action_image_order':2,'alpha':'r->r^-1, s->r^2 s'}
  else:
   eight=next(x for x in Os if len(x)==8);Im=image(stab,eight);assert len(Im)==384
   pairs=list(itertools.combinations(eight,2));pair_orbits=[];seen=set()
   for pair in pairs:
    if pair in seen:continue
    O={tuple(sorted((g[pair[0]],g[pair[1]]))) for g in stab};seen|=O;pair_orbits.append(O)
   matching=next(O for O in pair_orbits if len(O)==4 and len({v for e in O for v in e})==8)
   identified='C2 wr S4 = 2^4:S4 = W(B4)';proof={'faithful_eight_point_action_order':384,'invariant_opposite_pair_matching':[list(e) for e in sorted(matching)],'ambient_wreath_order':384}
  records.append({'orbit':name,'orbit_size':osize,'stabilizer_order':len(stab),'identified_group':identified,'center_order':len(Z),'derived_series':[len(stab),len(D1),len(D2),len(D3)],'abelianization_order':len(stab)//len(D1),'element_order_distribution':dist(stab),'coordinate_orbit_sizes':[len(x) for x in Os],'proof':proof})
 payload={'schema':'w33.pass4001.code_stabilizer_identification.v1','status':'PASS_EXACT_THREE_STABILIZER_STRUCTURES','records':records,'hypercube_bridge':'The 135-code stabilizer is the full four-dimensional signed-permutation group W(B4), giving an exact 4-bit hypercube/cross-polytope symmetry bridge.','boundary':'These are stabilizers inside the fixed parent-preserving group O6-(2):2. No claim is made about full automorphism groups outside that parent problem.'}
 payload['semantic_sha256']=sha(payload);OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print('PASS_CODE_STABILIZERS',payload['semantic_sha256'])
if __name__=='__main__':main()
