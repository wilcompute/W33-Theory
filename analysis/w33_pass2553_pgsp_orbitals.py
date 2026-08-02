from __future__ import annotations
import itertools,collections,hashlib,json,time
import numpy as np
Q=3
def norm(v):
 v=tuple(int(x)%3 for x in v)
 for x in v:
  if x:return tuple((1 if x==1 else 2)*y%3 for y in v)
 raise ValueError
O=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%3
def symp(a,b):return int(np.array(a)@O@np.array(b)%3)
def transvection(v):v=np.array(v,dtype=int)%3;return (np.eye(4,dtype=int)+np.outer(v,O@v))%3
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def geom():
 pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={p:i for i,p in enumerate(pts)};edges=[]
 for i,j in itertools.combinations(range(40),2):
  if symp(pts[i],pts[j])==0:edges.append((i,j))
 lines=set()
 for i,j in edges:
  a=np.array(pts[i]);b=np.array(pts[j]);lines.add(tuple(sorted(pi[norm((u*a+v*b)%3)] for u,v in itertools.product(range(3),repeat=2) if u or v)))
 lines=sorted(lines);li={x:i for i,x in enumerate(lines)};frames=[(a,b) for a,b in itertools.combinations(range(40),2) if set(lines[a]).isdisjoint(lines[b])];fi={x:i for i,x in enumerate(frames)}
 def point_perm(M):return tuple(pi[norm(M@np.array(p))] for p in pts)
 def frame_perm(pp):
  lp=tuple(li[tuple(sorted(pp[x] for x in L))] for L in lines);return tuple(fi[tuple(sorted((lp[a],lp[b])))] for a,b in frames)
 mats=[transvection(v) for v in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0)]]+[np.diag([1,2,1,2])%3];pg=[point_perm(M) for M in mats];fg=[frame_perm(p) for p in pg];return pg,fg
def actions():
 pg,fg=geom();ident=tuple(range(40));idF=tuple(range(540));seen={ident:idF};q=collections.deque([ident])
 while q:
  p=q.popleft();f=seen[p]
  for a,b in zip(pg,fg):
   np_=compose(a,p)
   if np_ not in seen:seen[np_]=tuple(b[f[i]] for i in range(540));q.append(np_)
 assert len(seen)==51840;return list(seen.values())
def orbitals(group):
 rel=np.full((540,540),-1,dtype=np.int16);reps=[];sizes=[]
 for a in range(540):
  for b in range(540):
   if rel[a,b]>=0:continue
   Oset={(p[a],p[b]) for p in group};r=len(reps)
   for x,y in Oset:rel[x,y]=r
   reps.append((a,b));sizes.append(len(Oset))
 assert len(reps)==22;return rel,reps,sizes
def structure(rel,reps):
 r=len(reps);P=np.zeros((r,r,r),dtype=np.int64)
 for k,(a,b) in enumerate(reps):
  for x in range(540):P[int(rel[a,x]),int(rel[x,b]),k]+=1
 val=[int(np.sum(rel[a]==k)) for k,(a,b) in enumerate(reps)];tr=[int(rel[b,a]) for a,b in reps];return P,val,tr
def canon(blocks):return tuple(sorted((tuple(sorted(b)) for b in blocks if b),key=lambda b:(0 if 0 in b else 1,b)))
_cache={}
def refine(P,blocks):
 blocks=canon(blocks)
 if blocks in _cache:return _cache[blocks]
 B=np.zeros((len(blocks),22),dtype=np.int64)
 for a,A in enumerate(blocks):B[a,list(A)]=1
 S=np.einsum('ai,ijk,bj->kab',B,P,B,optimize=True);sigs=[tuple(S[k].ravel().tolist()) for k in range(22)];nb=[]
 for C in blocks:
  groups=collections.defaultdict(list)
  for k in C:groups[sigs[k]].append(k)
  nb.extend(groups.values())
 nb=canon(nb);ans=blocks if nb==blocks else refine(P,nb);_cache[blocks]=ans;return ans
def block_products(P,blocks):
 B=np.zeros((len(blocks),22),dtype=np.int64)
 for a,A in enumerate(blocks):B[a,list(A)]=1
 return np.einsum('ai,ijk,bj->kab',B,P,B,optimize=True)
def is_comm(P,blocks):return bool(np.array_equal(block_products(P,blocks),block_products(P,blocks).transpose(0,2,1)))
def constants_hash(P,blocks):
 S=block_products(P,blocks);out=[]
 for a in range(len(blocks)):
  for b in range(len(blocks)):
   vals=[]
   for C in blocks:z={int(S[k,a,b]) for k in C};assert len(z)==1;vals.append(next(iter(z)))
   out.append((a,b,vals))
 return hashlib.sha256(json.dumps(out,separators=(',',':')).encode()).hexdigest()
def main():
 G=actions();rel,reps,sizes=orbitals(G);P,val,tr=structure(rel,reps);unseen=set(range(1,22));tor=[]
 while unseen:
  i=min(unseen);o=tuple(sorted({i,tr[i]}));tor.append(o);unseen-=set(o)
 closures={};seeds=0
 for mask in range(1,1<<len(tor)):
  if not(mask&1):continue
  selected=set().union(*(set(tor[i]) for i in range(len(tor)) if mask>>i&1));rest=set(range(1,22))-selected
  if not rest:continue
  c=refine(P,[{0},selected,rest]);seeds+=1;closures[c]=closures.get(c,0)+1
 comm=[]
 for blocks,count in closures.items():
  if is_comm(P,blocks):comm.append({'rank':len(blocks),'blocks':[list(x) for x in blocks],'valencies':[sum(val[i] for i in x) for x in blocks],'seed_count':count,'constants_sha256':constants_hash(P,blocks)})
 comm.sort(key=lambda z:(z['rank'],z['blocks']));out={'pgsp_rank':22,'transpose_orbits':[list(x) for x in tor],'transpose_orbit_count':len(tor),'binary_seeds_tested':seeds,'distinct_coherent_closures':len(closures),'commutative_fusions':comm,'commutative_rank_distribution':dict(sorted(collections.Counter(z['rank'] for z in comm).items())),'nontrivial_min_rank':min((z['rank'] for z in comm if z['rank']>2),default=None)};out['sha256_without_hash_field']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest();print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
