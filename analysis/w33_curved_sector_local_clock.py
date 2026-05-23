#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis'))
import w33_z3_voltage_cover as vc
P=3

def common_centers(W,t): return tuple(x for x in range(40) if all(W[x,a] for a in t))
def clique_lines(W): return sorted(tuple(sorted(c)) for c in nx.find_cliques(nx.from_numpy_array(W)) if len(c)==4)
def get_voltage(W,axes,X,E):
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
 g={0:(0,1,2),1:(1,0,2)}; z={(0,1,2):0,(1,2,0):1,(2,0,1):2}; gp={p:g[lab[p]] for p in range(40)}
 return {k:z[vc.co(gp[k[1]],vc.co(t,vc.iv(gp[k[0]])))] for k,t in tr.items()}
def F(volt,t):
 a,b,c=tuple(sorted(t)); return (volt[(a,b)]+volt[(b,c)]+volt[(c,a)])%3
def main():
 W,axes,X=vc.build(); E=vc.rootgraph(); volt=get_voltage(W,axes,X,E); lines=clique_lines(W)
 point_lines={p:[L for L in lines if p in L] for p in range(40)}
 center_summary=[]; omitted_summary=[]; global_triads=Counter(); f_by_center=defaultdict(Counter); f_by_center_omit=[]
 for x in range(40):
  Ls=point_lines[x]
  assert len(Ls)==4
  for oi,O in enumerate(Ls):
   chosen=[L for L in Ls if L!=O]
   buckets=[[p for p in L if p!=x] for L in chosen]
   local=Counter()
   for tri in product(*buckets):
    t=tuple(sorted(tri)); cc=len(common_centers(W,t)); cur=F(volt,t); local[(cc,cur)]+=1; f_by_center[x][cur]+=1; global_triads[(cc,cur)]+=1
   f_by_center_omit.append(tuple(local.items()))
   omitted_summary.append({'center':x,'omitted_line':list(O),'distribution':{str(k):v for k,v in sorted(local.items())}})
 for x in range(40): center_summary.append({'center':x,'curvature_distribution':dict(f_by_center[x]),'flat':f_by_center[x][0],'curved':f_by_center[x][1]+f_by_center[x][2]})
 center_dist=Counter((s['flat'],s['curved'],s['curvature_distribution'].get(1,0),s['curvature_distribution'].get(2,0)) for s in center_summary)
 omit_dist=Counter(str(dict(k)) for k in f_by_center_omit)
 ok=(center_dist==Counter({(36,72,36,36):40}) and len(omit_dist)==1 and list(omit_dist.values())==[160] and global_triads==Counter({(4,0):1440,(1,1):1440,(1,2):1440}))
 out={'all_checks_passed':ok,'summary':{'centers':40,'lines_through_each_center':4,'centered_triad_choices_per_center':108,'per_center_distribution':{str(k):v for k,v in center_dist.items()},'per_omitted_pencil_line_pattern':dict(omit_dist),'global_center_incidence_by_center_count_and_curvature':{str(k):v for k,v in global_triads.items()}},'interpretation':'Around each point, the 12 neighbours form four 3-point pencil branches.  Centered noncollinear triads are 4*3^3=108 choices.  The Z3 curvature splits every local 108-clock uniformly into 36 flat, 36 curvature +1, and 36 curvature -1 events; per omitted pencil line the split is 9,9,9.'}
 path=ROOT/'data'/'w33_curved_sector_local_clock.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
