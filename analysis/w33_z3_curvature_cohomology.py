#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis'))
import w33_z3_voltage_cover as vc

def rankp(A,p=3):
 A=np.array(A,dtype=np.int16)%p; m,n=A.shape; r=0
 for c in range(n):
  piv=next((i for i in range(r,m) if A[i,c]%p),None)
  if piv is None: continue
  if piv!=r: A[[r,piv]]=A[[piv,r]]
  A[r]=(A[r]*(1 if A[r,c]==1 else 2))%p
  for i in range(m):
   if i!=r and A[i,c]%p: A[i]=(A[i]-A[i,c]*A[r])%p
  r+=1
 return r

def main():
 W,axes,X=vc.build(); E=vc.rootgraph()
 gm=nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(X),nx.from_numpy_array(E)); assert gm.is_isomorphic(); mp=dict(gm.mapping)
 tri={p:[mp[i] for i,a in enumerate(axes) if a[0]==p] for p in range(40)}; tr={}
 for p,q in combinations(range(40),2):
  if W[p,q]: continue
  perm=tuple([j for j,b in enumerate(tri[q]) if E[a,b]][0] for a in tri[p]); tr[(p,q)]=perm; tr[(q,p)]=vc.iv(perm)
 lab={0:0}; st=[0]
 while st:
  p=st.pop()
  for q in range(40):
   if q==p or W[p,q]: continue
   val=lab[p]^vc.par(tr[(p,q)])
   if q not in lab: lab[q]=val; st.append(q)
 g={0:(0,1,2),1:(1,0,2)}; zm={(0,1,2):0,(1,2,0):1,(2,0,1):2}; gp={p:g[lab[p]] for p in range(40)}
 volt={k:zm[vc.co(gp[k[1]],vc.co(t,vc.iv(gp[k[0]])))] for k,t in tr.items()}
 ed=[e for e in combinations(range(40),2) if not W[e[0],e[1]]]; ei={e:i for i,e in enumerate(ed)}
 tri2=[t for t in combinations(range(40),3) if all(not W[a,b] for a,b in combinations(t,2))]
 tet=[s for s in combinations(range(40),4) if all(not W[a,b] for a,b in combinations(s,2))]
 d0=np.zeros((len(ed),40),dtype=np.int8); d1=np.zeros((len(tri2),len(ed)),dtype=np.int8)
 for k,(i,j) in enumerate(ed): d0[k,i]=2; d0[k,j]=1
 F={}; curv=Counter(); centers=defaultdict(Counter)
 for ti,(a,b,c) in enumerate(tri2):
  for sg,e in [(1,(b,c)),(2,(a,c)),(1,(a,b))]: d1[ti,ei[e]]=sg
  val=(volt[(a,b)]+volt[(b,c)]+volt[(c,a)])%3; F[(a,b,c)]=val; curv[val]+=1
  cc=sum(1 for x in range(40) if W[x,a] and W[x,b] and W[x,c]); centers[cc][val]+=1
 tri_i={t:i for i,t in enumerate(tri2)}; d2=np.zeros((len(tet),len(tri2)),dtype=np.int8); bianchi=0; pat=Counter()
 for k,(a,b,c,d) in enumerate(tet):
  vals=[]; s=0
  for sg,face in [(1,(b,c,d)),(2,(a,c,d)),(1,(a,b,d)),(2,(a,b,c))]: d2[k,tri_i[face]]=sg; vals.append(F[face]); s=(s+sg*F[face])%3
  bianchi += int(s!=0); pat[tuple(sorted(Counter(vals).items()))]+=1
 r0,r1,r2=rankp(d0),rankp(d1),rankp(d2); h1=len(ed)-r1-r0; h2=len(tri2)-r2-r1
 ok=(r0,r1,r2,h1,h2)==(39,501,2739,0,0) and bianchi==0 and curv==Counter({1:1440,2:1440,0:360})
 out={'all_checks_passed':ok,'summary':{'edges':len(ed),'triangles':len(tri2),'tetrahedra':len(tet),'rank_d0':r0,'rank_d1':r1,'rank_d2':r2,'H1_F3':h1,'H2_F3':h2,'curvature_values':dict(curv),'center_curvature':{str(k):dict(v) for k,v in centers.items()},'bianchi_violations':bianchi,'tetra_patterns':{str(k):v for k,v in pat.items()}},'meaning':'Curvature F=dA is exact on the W33-complement clique complex.  dF=0 on every tetrahedron.  H1 and H2 over F3 vanish for the tested skeleton, so this finite phase curvature has no hidden F3 cohomology at dimensions 1 or 2.'}
 path=ROOT/'data'/'w33_z3_curvature_cohomology.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
