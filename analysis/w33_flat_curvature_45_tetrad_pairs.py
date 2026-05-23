#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; P=3

def canon(v):
 v=tuple(int(x)%P for x in v)
 if v==(0,0,0,0): raise ValueError
 for x in v:
  if x: return tuple(((1 if x==1 else 2)*y)%P for y in v)
def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P
def srg(A):
 deg=Counter(map(int,A.sum(1))); la=Counter(); mu=Counter()
 for i,j in combinations(range(A.shape[0]),2):
  c=int(A[i]@A[j]); (la if A[i,j] else mu)[c]+=1
 eig=Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
 return {'degree':dict(deg),'lambda':dict(la),'mu':dict(mu),'spectrum':dict(eig)}
def build():
 pts=[]; seen=set()
 for raw in product(range(P), repeat=4):
  if raw==(0,0,0,0): continue
  c=canon(raw)
  if c not in seen: seen.add(c); pts.append(c)
 A=np.zeros((40,40),dtype=np.int8)
 for i,j in combinations(range(40),2):
  if form(pts[i],pts[j])==0: A[i,j]=A[j,i]=1
 return A
def main():
 W=build(); centers={}
 for t in combinations(range(40),3):
  if all(W[a,b]==0 for a,b in combinations(t,2)):
   centers[t]=tuple(x for x in range(40) if all(W[x,a] for a in t))
 center_count=Counter(len(c) for c in centers.values())
 flat=[t for t,c in centers.items() if len(c)==4]
 tetrads=set(tuple(sorted(centers[t])) for t in flat)
 # Add the original flat triples' tetrads too: every 4-centered triad sits in a unique 4-coclique.
 for t in flat:
  tetrads.add(tuple(sorted(t + (next(x for x in centers[tuple(sorted(centers[t][:3]))] if x not in t),)))) if False else None
 # The 90 tetrads are exactly center-sets; each has four 3-subsets, all flat.
 tetrads=sorted(tetrads)
 tetrad_mult=Counter(tuple(sorted(centers[t])) for t in flat)
 consistent=True; invol={}
 for T in tetrads:
  imgs={tuple(sorted(centers[tuple(sorted(s))])) for s in combinations(T,3)}
  consistent &= len(imgs)==1
  invol[T]=next(iter(imgs))
 fixed=sum(1 for T in tetrads if invol[T]==T)
 pairs=sorted({tuple(sorted((T,invol[T]))) for T in tetrads})
 pair_sets=[frozenset(set(a)|set(b)) for a,b in pairs]
 pair_inter=Counter(len(pair_sets[i]&pair_sets[j]) for i,j in combinations(range(len(pair_sets)),2))
 A32=np.zeros((45,45),dtype=np.int8); A12=np.zeros((45,45),dtype=np.int8)
 for i,j in combinations(range(45),2):
  z=len(pair_sets[i]&pair_sets[j])
  if z==2: A32[i,j]=A32[j,i]=1
  if z==0: A12[i,j]=A12[j,i]=1
 bip_edges=Counter(); line_side_edges=Counter()
 for a,b in pairs:
  A=set(a); B=set(b)
  bip_edges[sum(W[x,y] for x in A for y in B)] += 1
  line_side_edges[sum(W[x,y] for x,y in combinations(A,2)) + sum(W[x,y] for x,y in combinations(B,2))] += 1
 ok=(center_count==Counter({1:2880,4:360}) and len(tetrads)==90 and set(tetrad_mult.values())=={4} and consistent and fixed==0 and len(pairs)==45 and pair_inter==Counter({2:720,0:270}) and srg(A32)=={'degree':{32:45},'lambda':{22:720},'mu':{24:270},'spectrum':{32:1,2:24,-4:20}} and srg(A12)=={'degree':{12:45},'lambda':{3:270},'mu':{3:720},'spectrum':{12:1,3:20,-3:24}} and bip_edges==Counter({16:45}) and line_side_edges==Counter({0:45}))
 out={'all_checks_passed':ok,'summary':{'noncollinear_triads_by_center_count':dict(center_count),'flat_triples':len(flat),'tetrads':len(tetrads),'tetrad_multiplicity_from_flat_triples':dict(Counter(tetrad_mult.values())),'dual_tetrad_pairs':len(pairs),'fixed_tetrads_under_center_involution':fixed,'pair_intersections':dict(pair_inter),'bipartite_edges_per_dual_pair':dict(bip_edges)},'intersection_graph_45':srg(A32),'disjointness_graph_45':srg(A12),'meaning':'Flat curvature triples form 90 four-point cocliques.  Taking centers of any 3-subset defines a fixed-point-free involution on the 90 tetrads, yielding 45 dual tetrad pairs.  The 45-pair intersection graph is SRG(45,32,22,24), matching the earlier E6/Schlaefli transport graph.'}
 path=ROOT/'data'/'w33_flat_curvature_45_tetrad_pairs.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
