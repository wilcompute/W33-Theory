#!/usr/bin/env python3
import itertools, numpy as np, json, math, random, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"
perms=list(itertools.permutations(range(6)));idx={p:i for i,p in enumerate(perms)};e=idx[tuple(range(6))]
def comp(p,q): return tuple(p[q[i]] for i in range(6))
N=len(perms);mult=np.empty((N,N),dtype=np.uint16)
for i,p in enumerate(perms):mult[i]=[idx[comp(p,q)] for q in perms]
inv=np.empty(N,dtype=np.uint16)
for i,p in enumerate(perms):
 ip=[0]*6
 for a,b in enumerate(p):ip[b]=a
 inv[i]=idx[tuple(ip)]
conj=np.empty((N,N),dtype=np.uint16)
for a in range(N):conj[a]=mult[mult[a],inv[a]]
def closure(gens):
 gens=list(set([e]+[int(x) for x in gens]));gens+= [int(inv[x]) for x in gens];gens=list(set(gens));H={e};q=[e]
 while q:
  x=q.pop()
  for g in gens:
   y=int(mult[x,g])
   if y not in H:H.add(y);q.append(y)
 return frozenset(H)
def canonical(H):
 best=None;arr=np.fromiter(H,dtype=np.uint16)
 for a in range(N):
  C=tuple(sorted(map(int,conj[a,arr])))
  if best is None or C<best:best=C
 return best
def find_gens(H):
 gens=[];K=frozenset([e])
 for x in sorted(H):
  if x not in K:
   gens.append(x);K=closure(gens)
   if K==H:break
 return gens
start=time.time();triv=frozenset([e]);key=canonical(triv);reps={key:triv};gensmap={key:[]};queue=[key]
while queue:
 key=queue.pop(0);H=reps[key];gens=gensmap[key];uncovered=set(range(N))-set(H)
 while uncovered:
  g=min(uncovered);dc={int(mult[int(mult[h1,g]),h2]) for h1 in H for h2 in H};uncovered.difference_update(dc);K=closure(gens+[g]);ck=canonical(K)
  if ck not in reps:reps[ck]=K;gensmap[ck]=find_gens(K);queue.append(ck);print('new',len(reps),'order',len(K),'queue',len(queue),'elapsed',time.time()-start,flush=True)
print('TOTAL',len(reps),'elapsed',time.time()-start);out=[]
for key,H in sorted(reps.items(),key=lambda kv:(len(kv[1]),kv[0])):out.append({'order':len(H),'elements':sorted(H),'generators':gensmap[key]})
assert len(out)==56
np.savez_compressed(DATA/'w33_pass1909_s6_group_tables.npz',mult=mult,inv=inv,conj=conj);json.dump(out,open(DATA/'w33_pass1909_s6_subgroups.json','w'))
