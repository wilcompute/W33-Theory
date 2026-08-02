#!/usr/bin/env python3
from __future__ import annotations
import collections, hashlib, importlib.util, itertools, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'analysis/w33_pass1801_1805_common.py';PACK=ROOT/'data/w33_pass1837_middle_layer_compression.json'
ARCH=ROOT/'archive/dirs/TOE_tomotope_flag_model_conjugacy_v01_20260228_bundle/TOE_tomotope_flag_model_conjugacy_v01_20260228/tomotope_flag_model_192.json'

def load_common():
 s=importlib.util.spec_from_file_location('w33_common',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m

def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def inv(p):
 z=[0]*len(p)
 for i,j in enumerate(p):z[j]=i
 return tuple(z)
def porder(p):
 seen=[False]*len(p);o=1
 import math
 for i in range(len(p)):
  if seen[i]:continue
  j=i;n=0
  while not seen[j]:seen[j]=True;n+=1;j=p[j]
  o=math.lcm(o,n)
 return o

def subgroup_generated(gens,n):
 I=tuple(range(n));seen={I};q=collections.deque([I])
 while q:
  x=q.popleft()
  for g in gens:
   y=compose(g,x)
   if y not in seen:seen.add(y);q.append(y)
 return seen

def main():
 D=load_common().build_geometry();G=D['graph'];pack=json.loads(PACK.read_text());res=pack['residual_vertices'];duad_index=pack['residual_to_duad_index'];duads=list(itertools.combinations(range(6),2));local=[duads[duad_index[str(r)]] for r in res];octs=[set(D['octets'][r][0])|set(D['octets'][r][1]) for r in res]
 # Curved events, profiles, centers, and selected local carrier.
 all_events=[];labels={};layer={};center={}
 for t in itertools.combinations(range(40),3):
  if G.subgraph(t).number_of_edges():continue
  c=set(range(40))-set(t)
  for x in t:c&=set(G[x])
  if len(c)!=1:continue
  e=tuple(sorted((next(iter(c)),)+t));all_events.append(e)
  deg={x:sum(1 for y in e if x!=y and G.has_edge(x,y)) for x in e};cc=[x for x,v in deg.items() if v==3];assert len(cc)==1;center[e]=cc[0]
  z=[len(set(e)&o) for o in octs];m=max(z);ix=tuple(i for i,v in enumerate(z) if v==m)
  k='unique' if (m,len(ix))==(3,1) else 'tie2' if (m,len(ix))==(2,2) else 'tie3' if (m,len(ix))==(3,2) else None;assert k
  labels[e]=ix;layer[e]=k
 all_events=sorted(set(all_events));fixed=0;S=sorted(e for e in all_events if layer[e] in ('tie2','tie3') and fixed in labels[e]);assert len(S)==192;si={e:i for i,e in enumerate(S)}
 secondary={e:next(x for x in labels[e] if x!=fixed) for e in S}
 # Exceptional S6 and its fixed-duad stabilizer H of order 48.
 F=[tuple(x) for x in pack['canonical_six_line_pack']];Fset={frozenset(x) for x in F};ident=tuple(range(40));seen={ident:tuple(range(45))};q=collections.deque([ident])
 while q:
  pp=q.popleft();op=seen[pp]
  for gp,ge,gl,gf,go,gos in D['acts']+[D['outer']]:
   np_=compose(gp,pp)
   if np_ not in seen:seen[np_]=tuple(go[op[i]] for i in range(45));q.append(np_)
 s6=[(pp,op) for pp,op in seen.items() if {frozenset(op[i] for i in x) for x in F}==Fset];assert len(s6)==720
 fixed_res=res[fixed];Hraw=[(pp,op) for pp,op in s6 if op[fixed_res]==fixed_res];assert len(Hraw)==48
 Hpoint=[pp for pp,op in Hraw];hp_index={p:i for i,p in enumerate(Hpoint)}
 Hperm=[]
 for pp in Hpoint:
  z=tuple(si[tuple(sorted(pp[x] for x in e))] for e in S);Hperm.append(z)
 assert len(set(Hperm))==48
 # Multiplication table and inverses in H.
 mul=[[hp_index[compose(Hpoint[a],Hpoint[b])] for b in range(48)] for a in range(48)];eid=hp_index[ident];hinv=[]
 for a in range(48):hinv.append(next(b for b in range(48) if mul[a][b]==eid and mul[b][a]==eid))
 # Four regular H-orbits, two per selected layer.
 unseen=set(range(192));orbits=[]
 while unseen:
  x=min(unseen);O={p[x] for p in Hperm};assert len(O)==48;orbits.append(sorted(O));unseen-=O
 bylayer=collections.defaultdict(list)
 for O in orbits:
  ls={layer[S[x]] for x in O};assert len(ls)==1;bylayer[next(iter(ls))].append(O)
 assert sorted(map(len,bylayer['tie2']))==[48,48] and sorted(map(len,bylayer['tie3']))==[48,48]
 # Complete invariant relation table on selected flags.
 def rsig(e,f):
  ce,cf=center[e],center[f];le=set(e)-{ce};lf=set(f)-{cf}
  return (layer[e],layer[f],len(set(e)&set(f)),int(ce==cf),int(ce in lf),int(cf in le),len(le&lf),
          int(G.has_edge(ce,cf)) if ce!=cf else 0,
          sum(int(G.has_edge(ce,x)) for x in lf if x!=ce),sum(int(G.has_edge(cf,x)) for x in le if x!=cf),
          sum(int(G.has_edge(x,y)) for x in le for y in lf if x!=y),int(secondary[e]==secondary[f]),len(set(local[secondary[e]])&set(local[secondary[f]])))
 sigids={};R=np.empty((192,192),dtype=np.int16)
 for i,e in enumerate(S):
  for j,f in enumerate(S):
   z=rsig(e,f)
   if z not in sigids:sigids[z]=len(sigids)
   R[i,j]=sigids[z]
 # Commutator subgroup, quotient C2xC2, and unique sign character vanishing on center.
 comm=set()
 for a in range(48):
  for b in range(48):comm.add(mul[mul[mul[a][b]][hinv[a]]][hinv[b]])
 changed=True
 while changed:
  changed=False
  for a in list(comm):
   for b in list(comm):
    c=mul[a][b]
    if c not in comm:comm.add(c);changed=True
 assert len(comm)==12
 cosets=[];unseenH=set(range(48))
 while unseenH:
  a=min(unseenH);C={mul[a][c] for c in comm};cosets.append(sorted(C));unseenH-=C
 assert len(cosets)==4;coset_of={x:i for i,C in enumerate(cosets) for x in C};qid=coset_of[eid]
 central=[a for a in range(48) if all(mul[a][b]==mul[b][a] for b in range(48))];assert len(central)==2;z=next(a for a in central if a!=eid);qz=coset_of[z]
 chars=[]
 for bits in itertools.product(range(2),repeat=4):
  if bits[qid]!=0:continue
  if all(bits[coset_of[mul[a][b]]]==(bits[coset_of[a]]^bits[coset_of[b]]) for a in range(48) for b in range(48)):chars.append(bits)
 chi=next(bits for bits in chars if any(bits) and bits[qz]==0);assert len([bits for bits in chars if any(bits) and bits[qz]==0])==1
 twist=[mul[z][a] if chi[coset_of[a]] else a for a in range(48)];assert len(set(twist))==48 and all(twist[mul[a][b]]==mul[twist[a]][twist[b]] for a in range(48) for b in range(48))
 # All automorphisms: 24 inner maps, and their compositions with the sign twist.
 auts=[]
 for a in range(48):
  inn=tuple(mul[mul[a][h]][hinv[a]] for h in range(48))
  for use_twist in (0,1):
   phi=tuple(twist[inn[h]] if use_twist else inn[h] for h in range(48))
   if phi not in auts:auts.append(phi)
 assert len(auts)==48
 def layer_candidates(A,B):
  ba=A[0];bb=B[0];coordA=[p[ba] for p in Hperm];coordB=[p[bb] for p in Hperm];assert len(set(coordA))==len(set(coordB))==48
  invA={x:h for h,x in enumerate(coordA)};invB={x:h for h,x in enumerate(coordB)};U=sorted(A+B);sub=R[np.ix_(U,U)];pos={x:i for i,x in enumerate(U)};out=[]
  for ai,phi in enumerate(auts):
   phiinv=[0]*48
   for h,k in enumerate(phi):phiinv[k]=h
   for t in range(48):
    ti=hinv[t];tau={}
    for h,x in enumerate(coordA):tau[x]=coordB[mul[phi[h]][t]]
    for k,x in enumerate(coordB):tau[x]=coordA[phiinv[mul[k][ti]]]
    perm=np.array([pos[tau[x]] for x in U],dtype=np.int16)
    if np.array_equal(sub,sub[np.ix_(perm,perm)]):out.append((ai,t,tuple(tau[x] for x in U)))
  return U,out
 U2,C2=layer_candidates(*bylayer['tie2']);U3,C3=layer_candidates(*bylayer['tie3'])
 fullc=[];pos2={x:i for i,x in enumerate(U2)};pos3={x:i for i,x in enumerate(U3)}
 byaut2=collections.defaultdict(list);byaut3=collections.defaultdict(list)
 for ai,t,p in C2:byaut2[ai].append((t,p))
 for ai,t,p in C3:byaut3[ai].append((t,p))
 for ai in sorted(set(byaut2)&set(byaut3)):
  for t2,p2 in byaut2[ai]:
   for t3,p3 in byaut3[ai]:
    tau=list(range(192))
    for x,y in zip(U2,p2):tau[x]=y
    for x,y in zip(U3,p3):tau[x]=y
    tau=tuple(tau)
    if all(tau[tau[i]]==i for i in range(192)) and np.array_equal(R,R[np.ix_(tau,tau)]):
     K=subgroup_generated(Hperm+[tau],192);spec=collections.Counter(porder(p) for p in K);orbs=[];un=set(range(192))
     while un:
      x=min(un);O={p[x] for p in K};orbs.append(len(O));un-=O
     fullc.append({'aut_index':ai,'translation_tie2':t2,'translation_tie3':t3,'tau':tau,'group_order':len(K),'order_spectrum':dict(sorted(spec.items())),'flag_orbits':sorted(orbs)})
 archived=json.loads(ARCH.read_text())['symmetry96_order_spectrum'];archspec={int(k):v for k,v in archived.items()}
 matches=[c for c in fullc if c['group_order']==96 and c['order_spectrum']==archspec and c['flag_orbits']==[96,96]]
 out={'H_order':48,'H_orbit_layers':{k:list(map(len,v)) for k,v in bylayer.items()},'relation_count':len(sigids),'automorphism_count_H':len(auts),
      'layer_candidate_counts':{'tie2':len(C2),'tie3':len(C3)},'full_relation_automorphism_candidates':len(fullc),'archived_spectrum':archspec,'wd4plus_matches':len(matches)}
 if matches:
  m=matches[0];out['canonical_match']={k:v for k,v in m.items() if k!='tau'};out['canonical_match']['tau_sha256']=hashlib.sha256(bytes(m['tau'])).hexdigest();out['canonical_match']['tau']=list(m['tau'])
 out['sha256_without_hash_field']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
