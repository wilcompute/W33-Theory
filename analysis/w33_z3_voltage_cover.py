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
def co(p,q): return tuple(p[q[i]] for i in range(3))
def iv(p):
 r=[0,0,0]
 for i,j in enumerate(p): r[j]=i
 return tuple(r)
def par(p): return sum(1 for i in range(3) for j in range(i+1,3) if p[i]>p[j])%2
def eig(A): return Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
def build():
 pts=[]; seen=set()
 for raw in product(range(P),repeat=4):
  if raw==(0,0,0,0): continue
  z=c(raw)
  if z not in seen: seen.add(z); pts.append(z)
 pi={p:i for i,p in enumerate(pts)}; E=[(i,j) for i,j in combinations(range(40),2) if sp(pts[i],pts[j])==0]
 W=np.zeros((40,40),dtype=np.int8)
 for i,j in E: W[i,j]=W[j,i]=1
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
def rootgraph():
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
 W,axes,X=build(); E=rootgraph(); gm=nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(X),nx.from_numpy_array(E)); assert gm.is_isomorphic(); mp=dict(gm.mapping)
 tri={p:[mp[i] for i,a in enumerate(axes) if a[0]==p] for p in range(40)}; trans={}; T=np.zeros((120,120),dtype=np.int8)
 for p,q in combinations(range(40),2):
  if W[p,q]: continue
  perm=tuple([j for j,b in enumerate(tri[q]) if E[a,b]][0] for a in tri[p]); trans[(p,q)]=perm; trans[(q,p)]=iv(perm)
  for i,a in enumerate(tri[p]): b=tri[q][perm[i]]; T[a,b]=T[b,a]=1
 labels={0:0}; st=[0]; ok=True
 while st:
  p=st.pop()
  for q in range(40):
   if q==p or W[p,q]: continue
   val=labels[p]^par(trans[(p,q)])
   if q in labels and labels[q]!=val: ok=False
   if q not in labels: labels[q]=val; st.append(q)
 g={0:(0,1,2),1:(1,0,2)}; gp={p:g[labels[p]] for p in range(40)}; zmap={(0,1,2):0,(1,2,0):1,(2,0,1):2}; volts={}
 for k,t in trans.items(): volts[k]=zmap[co(gp[k[1]],co(t,iv(gp[k[0]])))]
 antisym=all(volts[(q,p)]==(-volts[(p,q)])%3 for p,q in volts)
 hs=Counter(); joint=defaultdict(Counter)
 for a,b,d in combinations(range(40),3):
  if W[a,b] or W[b,d] or W[d,a]: continue
  s=(volts[(a,b)]+volts[(b,d)]+volts[(d,a)])%3; cc=sum(1 for x in range(40) if W[x,a] and W[x,b] and W[x,d])
  hs[s]+=1; joint[cc][s]+=1
 base=np.ones((40,40),dtype=np.int8)-np.eye(40,dtype=np.int8)-W
 good=ok and antisym and eig(T)==Counter({27:1,3:75,-3:24,-9:20}) and eig(base)==Counter({27:1,3:15,-3:24}) and hs==Counter({1:1440,2:1440,0:360}) and joint[4]==Counter({0:360}) and joint[1]==Counter({1:1440,2:1440})
 out={'all_checks_passed':good,'summary':{'cover':'connected 3-sheet cover of W33 complement','transport_edges':int(T.sum()//2),'transport_spectrum':dict(eig(T)),'base_complement_spectrum':dict(eig(base)),'parity_gauge_possible':ok,'gauge_labels':dict(Counter(labels.values())),'voltage_distribution':dict(Counter(volts.values())),'antisymmetric_voltage':antisym,'triangle_voltage_sums':dict(hs),'center_split_voltage':{str(k):dict(v) for k,v in joint.items()}},'meaning':'After a parity gauge, every noncollinear triad matching is a cyclic Z3 voltage.  Voltage sum zero occurs exactly on four-centered noncollinear triples; nonzero voltage occurs exactly on one-centered triples.'}
 path=ROOT/'data'/'w33_z3_voltage_cover.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if good else 1
if __name__=='__main__': raise SystemExit(main())
