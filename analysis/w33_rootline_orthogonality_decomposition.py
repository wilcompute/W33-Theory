#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; P=3

def c(v):
 v=tuple(int(x)%P for x in v)
 if v==(0,0,0,0): raise ValueError
 for x in v:
  if x: return tuple(((1 if x==1 else 2)*y)%P for y in v)
def sp(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P
def spec(A): return Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
def pars(A):
 deg=Counter(map(int,A.sum(1))); la=Counter(); mu=Counter()
 for i,j in combinations(range(A.shape[0]),2):
  k=int(A[i]@A[j]); (la if A[i,j] else mu)[k]+=1
 return {'degree':dict(deg),'lambda':dict(la),'mu':dict(mu),'spectrum':dict(spec(A))}
def wdata():
 pts=[]; seen=set()
 for raw in product(range(P),repeat=4):
  if raw==(0,0,0,0): continue
  z=c(raw)
  if z not in seen: seen.add(z); pts.append(z)
 pi={p:i for i,p in enumerate(pts)}; e=[(i,j) for i,j in combinations(range(40),2) if sp(pts[i],pts[j])==0]
 W=np.zeros((40,40),dtype=np.int8)
 for i,j in e: W[i,j]=W[j,i]=1
 lines=set()
 for i,j in e:
  u,v=pts[i],pts[j]; L=set()
  for a,b in product(range(P),repeat=2):
   if a==0 and b==0: continue
   L.add(pi[c((a*u[t]+b*v[t] for t in range(4)))])
  lines.add(tuple(sorted(L)))
 lines=sorted(lines); pl=defaultdict(list); el={}
 for li,L in enumerate(lines):
  for p in L: pl[p].append(li)
  for x in combinations(L,2): el[tuple(sorted(x))]=li
 axes=[]; va={}
 for p in range(40):
  a,b,d,e=sorted(pl[p])
  for ax in [((a,b),(d,e)),((a,d),(b,e)),((a,e),(b,d))]:
   ax=tuple(sorted(tuple(sorted(z)) for z in ax)); key=(p,ax); axes.append(key)
   for pair in ax: va[(p,pair)]=key
 axes=sorted(axes); ai={a:i for i,a in enumerate(axes)}; qs=[]; seenq=set()
 for a,b in combinations(range(40),2):
  if W[a,b]: continue
  cm=[x for x in range(40) if W[a,x] and W[b,x]]
  for d,e in combinations(cm,2):
   cyc=tuple(sorted(tuple(sorted(x)) for x in ((a,d),(d,b),(b,e),(e,a))))
   if cyc not in seenq: seenq.add(cyc); qs.append(cyc)
 M=np.zeros((120,len(qs)),dtype=np.int8)
 for qi,cyc in enumerate(qs):
  inc=defaultdict(list)
  for u,v in cyc: inc[u].append((u,v)); inc[v].append((u,v))
  for p,es in inc.items():
   lp=tuple(sorted(el[tuple(sorted(x))] for x in es)); M[ai[va[(p,lp)]],qi]=1
 X=(M@M.T>0).astype(np.int8); np.fill_diagonal(X,0); return W,axes,X
def roots():
 r=[]
 for i in range(8):
  for j in range(i+1,8):
   for si in (1,-1):
    for sj in (1,-1):
     x=[0]*8; x[i]=si; x[j]=sj; r.append(tuple(x))
 for s in product((1,-1),repeat=8):
  if sum(x<0 for x in s)%2==0: r.append(tuple(x/2 for x in s))
 V=np.array(r,float); used=set(); reps=[]
 for i in range(240):
  if i in used: continue
  for j in range(i+1,240):
   if j not in used and np.allclose(V[i]+V[j],0): used.add(i); used.add(j); reps.append(np.array(min(tuple(V[i]),tuple(V[j])),float)); break
 R=np.array(sorted(reps,key=lambda x:tuple(x.tolist())),float); A=np.isclose(np.abs(R@R.T),0).astype(np.int8); np.fill_diagonal(A,0); return A
def main():
 W,axes,X=wdata(); E=roots(); gm=nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(X),nx.from_numpy_array(E)); assert gm.is_isomorphic(); mp=dict(gm.mapping)
 tri={p:[mp[i] for i,a in enumerate(axes) if a[0]==p] for p in range(40)}
 C=np.zeros((120,120),dtype=np.int8); T=np.zeros((120,120),dtype=np.int8)
 for p,q in combinations(range(40),2):
  if W[p,q]:
   for a in tri[p]:
    for b in tri[q]: C[a,b]=C[b,a]=1
  else:
   for a in tri[p]:
    for b in tri[q]:
     if E[a,b]: T[a,b]=T[b,a]=1
 ok=np.array_equal(E,C+T) and int(C.sum()//2)==2160 and int(T.sum()//2)==1620 and Counter(map(int,C.sum(1)))==Counter({36:120}) and Counter(map(int,T.sum(1)))==Counter({27:120})
 out={'all_checks_passed':ok,'summary':{'rootline_edges_total':int(E.sum()//2),'collinear_block_edges':int(C.sum()//2),'noncollinear_transport_edges':int(T.sum()//2),'decomposition':'E_rootline = C_collinear + T_noncollinear','transport_connected':nx.number_connected_components(nx.from_numpy_array(T))==1},'collinear_block_graph':pars(C),'noncollinear_transport_graph':pars(T),'rootline_graph':pars(E),'meaning':'Root-line orthogonality decomposes into collinear K3,3 blocks plus noncollinear perfect-matching transport.  The transport graph is the 3-cover carrying the Z3 holonomy.'}
 path=ROOT/'data'/'w33_rootline_orthogonality_decomposition.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
