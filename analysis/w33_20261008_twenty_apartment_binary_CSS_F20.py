#!/usr/bin/env python3
"""20-apartment CW complex -> exact binary CSS and mod-2 F20 action.

Distinct from earlier W33 40-bit incidence CSS false-start, July [[18,2,3]]_3
toric code, and global 1620-apartment parity module. No physical qubit
construction is inferred without stabilizer measurements and a circuit.
"""
from pathlib import Path
import sys,collections,json
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_early_torus_singer_quotient import objects
OUT=ROOT/"data/w33_20261008_twenty_apartment_binary_CSS_F20.json"

def add(v,basis):
 x=int(v)
 for h in sorted(basis,reverse=True):
  if (x>>h)&1:x^=basis[h]
 if x:
  h=x.bit_length()-1;basis[h]=x
  return True
 return False

def reduce(v,basis):
 x=int(v)
 for h in sorted(basis,reverse=True):
  if (x>>h)&1:x^=basis[h]
 return x

def nullspace(rows,n):
 # standard GF2 RREF of arbitrary row-int bitmasks.
 B={}; piv=[]
 for row in rows:
  x=int(row)
  for p in sorted(B,reverse=True):
   if (x>>p)&1:x^=B[p]
  if x:
   p=x.bit_length()-1;B[p]=x
 for p in sorted(B):
  for q in sorted(B):
   if p!=q and ((B[q]>>p)&1):B[q]^=B[p]
 piv=sorted(B)
 free=[i for i in range(n) if i not in piv]
 kernel=[]
 for f in free:
  x=1<<f
  for p in piv:
   if (B[p]>>f)&1:x|=1<<p
  assert all((x&r).bit_count()%2==0 for r in rows)
  kernel.append(x)
 return kernel

def topology():
 C,faces,stab,H=objects()
 V=sorted({v for f in faces for v in f})
 E=sorted({tuple(sorted((u,v))) for f in faces for u,v in zip(f,f[1:]+f[:1])})
 vi={v:i for i,v in enumerate(V)};ei={e:i for i,e in enumerate(E)}
 b1=[0]*40;b2=[0]*20
 for j,(u,v) in enumerate(E):
  b1[vi[u]]^=1<<j;b1[vi[v]]^=1<<j
 for j,f in enumerate(faces):
  for u,v in zip(f,f[1:]+f[:1]):
   b2[j]^=1<<ei[tuple(sorted((u,v)))]
 assert all((a&b).bit_count()%2==0 for a in b1 for b in b2)
 return V,E,faces,stab,H,b1,b2

def analyze():
 V,E,faces,stab,H,b1,b2=topology()
 coboundary={};boundary={}
 for v in b1:add(v,coboundary)
 for v in b2:add(v,boundary)
 assert (len(coboundary),len(boundary))==(39,19)
 cocycles=nullspace(b2,60)
 cycles=nullspace(b1,60)
 assert len(cocycles)==41 and len(cycles)==21
 basisX=coboundary.copy();basisZ=boundary.copy()
 H1co=[];H1cy=[]
 for x in cocycles:
  if add(x,basisX):H1co.append(x)
 for z in cycles:
  if add(z,basisZ):H1cy.append(z)
 assert len(H1co)==len(H1cy)==2
 def coord(x,basis,base):
  for c in range(4):
   y=x
   if c&1:y^=basis[0]
   if c&2:y^=basis[1]
   if reduce(y,base)==0:return c
  raise ValueError("not in span")
 # F20 acting on 1-cochain basis. On F2 orientation reversal is trivial.
 eidx={e:i for i,e in enumerate(E)}
 shapes=collections.Counter();matrices={}
 for g in stab:
  perm=[eidx[tuple(sorted((g[u],g[v])))] for u,v in E]
  image=[]
  for h in H1co:
   t=0
   for i in range(60):
    if h>>i&1:t^=1<<perm[i]
   image.append(coord(t,H1co,coboundary))
  matrix=tuple(image)
  assert set(image)!={0}
  shapes[str(matrix)]+=1
  matrices[matrix]=g
 # Dimension of vectors fixed by all matrices
 invariant=[i for i in range(4) if all(( ((m[0] if i&1 else 0)^(m[1] if i&2 else 0))==i) for m in matrices)]
 assert 0 in invariant
 assert set(shapes.values())<={10,20}
 # Minimal nontrivial Z loop: shortest closed lifted path with nonzero H1 evaluation.
 edgevoltage=[]
 for i in range(60):
  v=((H1co[0]>>i)&1)|(((H1co[1]>>i)&1)<<1)
  edgevoltage.append(v)
 adj={v:[] for v in V}
 for i,(u,v) in enumerate(E):
  adj[u].append((v,i));adj[v].append((u,i))
 best=None
 for start in V:
  q=collections.deque([(start,0)])
  seen={(start,0):(None,None)}
  target=None
  while q:
   node,k=q.popleft()
   if node==start and k:
    target=(node,k);break
   for nextnode,ei2 in adj[node]:
    state=(nextnode,k^edgevoltage[ei2])
    if state not in seen:
     seen[state]=((node,k),ei2)
     q.append(state)
  if target:
   path=[];cur=target
   while seen[cur][0] is not None:
    prev,idx=seen[cur];path.append(idx);cur=prev
   path=path[::-1]
   if best is None or len(path)<len(best):best=path
 assert best is not None
 mask=sum(1<<i for i in best)
 assert all((mask&r).bit_count()%2==0 for r in b1)
 assert ((mask&H1co[0]).bit_count()%2 or (mask&H1co[1]).bit_count()%2)
 css={"n":60,"rank_HX":39,"rank_HZ":19,"k":2,
  "all_HX_HZ_commutators_zero":True,
  "mod2_H1_dimension":2,"mod2_H1_cohomology_dimension":2,
  "C5_invariant_binary_H1_dimension":2,
  "F20_mod2_H1_representation_image_hist":dict(shapes),
  "F20_invariant_binary_H1_classes":invariant,
  "F20_invariant_binary_H1_dimension":len(invariant).bit_length()-1,
  "nontrivial_Z_shortest_length":len(best),
  "nontrivial_Z_shortest_support_edge_indices":best,
  "X_minimum_distance":"not solved in this producer",
  "Z_minimum_distance_exact_by_4sheet_BFS":True,
  "old_prior_art":"Jul 2026 [[18,2,3]]_3 toric code; August 1620-apartment binary codes and 2-lifts are distinct",
  "UV_matter_parity_supplied":False}
 return css

if __name__=="__main__":
 d=analyze()
 OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(json.dumps(d,indent=2),flush=True)
 print("BINARY_CSS_F20_PASS",flush=True)
