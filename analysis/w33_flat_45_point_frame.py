#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; P=3

def c(v):
 v=tuple(int(x)%P for x in v)
 if v==(0,0,0,0): raise ValueError
 for x in v:
  if x: return tuple(((1 if x==1 else 2)*y)%P for y in v)
def sp(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P
def spec(A): return Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
def build():
 pts=[]; seen=set()
 for raw in product(range(P), repeat=4):
  if raw==(0,0,0,0): continue
  z=c(raw)
  if z not in seen: seen.add(z); pts.append(z)
 A=np.zeros((40,40),dtype=np.int8)
 for i,j in combinations(range(40),2):
  if sp(pts[i],pts[j])==0: A[i,j]=A[j,i]=1
 return A
def main():
 W=build(); centers={}
 for t in combinations(range(40),3):
  if all(W[a,b]==0 for a,b in combinations(t,2)):
   centers[t]=tuple(x for x in range(40) if all(W[x,a] for a in t))
 flat=[t for t,c in centers.items() if len(c)==4]
 tetrads=sorted(set(tuple(sorted(centers[t])) for t in flat))
 invol={}
 for T in tetrads:
  imgs={tuple(sorted(centers[tuple(sorted(s))])) for s in combinations(T,3)}
  if len(imgs)!=1: raise RuntimeError('bad tetrad involution')
  invol[T]=next(iter(imgs))
 pairs=sorted({tuple(sorted((T,invol[T]))) for T in tetrads})
 blocks=[tuple(sorted(set(a)|set(b))) for a,b in pairs]
 M=np.zeros((40,45),dtype=np.int8)
 for j,B in enumerate(blocks):
  for p in B: M[p,j]=1
 Pgram=M@M.T; Bgram=M.T@M
 by_adj=defaultdict(Counter)
 for i,j in combinations(range(40),2): by_adj[int(W[i,j])][int(Pgram[i,j])]+=1
 A45=np.zeros((45,45),dtype=np.int8)
 for i,j in combinations(range(45),2):
  if len(set(blocks[i])&set(blocks[j]))==2: A45[i,j]=A45[j,i]=1
 ok=(Counter(M.sum(0))==Counter({8:45}) and Counter(M.sum(1))==Counter({9:40}) and by_adj[1]==Counter({3:240}) and by_adj[0]==Counter({1:540}) and np.array_equal(Pgram,8*np.eye(40,dtype=int)+np.ones((40,40),dtype=int)+2*W) and np.array_equal(Bgram,8*np.eye(45,dtype=int)+2*A45) and spec(Pgram)==Counter({72:1,12:24,0:15}) and spec(Bgram)==Counter({72:1,12:24,0:20}))
 out={'all_checks_passed':ok,'summary':{'flat_triples':len(flat),'tetrads':len(tetrads),'dual_tetrad_pairs':len(pairs),'point_block_matrix_shape':[40,45],'block_size_distribution':dict(Counter(M.sum(0))),'point_degree_distribution':dict(Counter(M.sum(1))),'point_pair_coincidence_by_w33_adjacency':{str(k):dict(v) for k,v in by_adj.items()},'point_gram_spectrum':dict(spec(Pgram)),'block_gram_spectrum':dict(spec(Bgram))},'identities':{'point_gram':'M M^T = 8 I_40 + J_40 + 2 A_W33','block_gram':'M^T M = 8 I_45 + 2 A_45','eigenspace_filter':'The flat 45-sector preserves the W33 1+24 eigenspaces and kills the 15-dimensional -4 eigenspace.'},'meaning':'The 45 flat dual tetrad-pair objects form a point-frame over W33.  Point co-incidence inside flat objects recovers W33 adjacency: adjacent pairs occur in 3 blocks, nonadjacent pairs in 1 block.'}
 path=ROOT/'data'/'w33_flat_45_point_frame.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
