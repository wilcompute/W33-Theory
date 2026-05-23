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
def f(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P
def cp(p,q): return tuple(p[q[i]] for i in range(3))
def iv(p):
 r=[0,0,0]
 for i,j in enumerate(p): r[j]=i
 return tuple(r)
def w():
 pts=[]; seen=set()
 for raw in product(range(P),repeat=4):
  if raw==(0,0,0,0): continue
  z=c(raw)
  if z not in seen: seen.add(z); pts.append(z)
 pi={p:i for i,p in enumerate(pts)}; E=[(i,j) for i,j in combinations(range(40),2) if f(pts[i],pts[j])==0]
 A=np.zeros((40,40),dtype=np.int8)
 for i,j in E: A[i,j]=A[j,i]=1
 lines=set()
 for i,j in E:
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
  if A[a,b]: continue
  com=[x for x in range(40) if A[a,x] and A[b,x]]
  for d,e in combinations(com,2):
   cyc=tuple(sorted(tuple(sorted(x)) for x in ((a,d),(d,b),(b,e),(e,a))))
   if cyc not in seenq: seenq.add(cyc); qs.append(cyc)
 M=np.zeros((120,len(qs)),dtype=np.int8)
 for qi,cyc in enumerate(qs):
  inc=defaultdict(list)
  for u,v in cyc: inc[u].append((u,v)); inc[v].append((u,v))
  for p,es in inc.items():
   lp=tuple(sorted(el[tuple(sorted(x))] for x in es)); M[ai[va[(p,lp)]],qi]=1
 G=M@M.T; X=(G>0).astype(np.int8); np.fill_diagonal(X,0); return A,axes,X
def rg():
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
 W,axes,X=w(); E=rg(); gm=nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(X),nx.from_numpy_array(E)); assert gm.is_isomorphic(); mp=dict(gm.mapping)
 tri={p:[mp[i] for i,a in enumerate(axes) if a[0]==p] for p in range(40)}; tr={}
 for p,q in combinations(range(40),2):
  if W[p,q]: continue
  perm=tuple([j for j,b in enumerate(tri[q]) if E[a,b]][0] for a in tri[p]); tr[(p,q)]=perm; tr[(q,p)]=iv(perm)
 even={(0,1,2),(1,2,0),(2,0,1)}; hol=Counter(); centers=Counter(); joint=defaultdict(Counter); total=0
 for a,b,d in combinations(range(40),3):
  if W[a,b] or W[b,d] or W[d,a]: continue
  h=cp(tr[(d,a)],cp(tr[(b,d)],tr[(a,b)])); cc=sum(1 for x in range(40) if W[x,a] and W[x,b] and W[x,d])
  hol[h]+=1; centers[cc]+=1; joint[cc][h]+=1; total+=1
 ok=total==3240 and centers==Counter({1:2880,4:360}) and set(hol)<=even and joint[4]==Counter({(0,1,2):360}) and sum(joint[1].values())==2880 and (0,1,2) not in joint[1]
 out={'all_checks_passed':ok,'summary':{'noncollinear_triples':total,'center_counts':dict(centers),'holonomy_counts':{str(k):v for k,v in hol.items()},'identity_center_four':dict(joint[4]),'nonidentity_center_one':{str(k):v for k,v in joint[1].items()}},'meaning':'Matching transport between noncollinear point triads has only cyclic order-three holonomy. Identity corresponds to four common centers; nonidentity corresponds to one common center.'}
 path=ROOT/'data'/'w33_z3_triad_holonomy.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
