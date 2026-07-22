#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
from w33_pass543_547_common import *
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass544_binary_switch_spectral_fibre.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2);B=(1,1,2,2,3,3,3,3,2,3,2,2)
def f2rank(rows,n):
 rows=[sum((b&1)<<i for i,b in enumerate(r)) for r in rows];rank=0
 for col in range(n):
  piv=next((i for i in range(rank,len(rows)) if (rows[i]>>col)&1),None)
  if piv is None:continue
  rows[rank],rows[piv]=rows[piv],rows[rank]
  for i in range(len(rows)):
   if i!=rank and ((rows[i]>>col)&1):rows[i]^=rows[rank]
  rank+=1
 return rank
def payload():
 target=tuple(charpoly_prime(5,A)[0]);hist=Counter();keep=[]
 for bits in itertools.product((1,4),repeat=12):
  offs=tuple(a*s%5 for a,s in zip(A,bits));cpv=tuple(charpoly_prime(5,offs)[0]);hist[cpv]+=1
  if cpv==target:keep.append(tuple(1 if s==4 else 0 for s in bits))
 S=set(keep);weights=Counter(sum(v) for v in keep);complement=all(tuple(1-x for x in v) in S for v in S);linear=all(tuple(a^b for a,b in zip(x,y)) in S for x in S for y in S)
 C=classes(5);G=nx.Graph();G.add_nodes_from(range(12))
 for i,u in enumerate(C):
  for j in range(i+1,12):
   if leg(omega(u,C[j],5),5)==1:G.add_edge(i,j)
 auts=[tuple(d[i] for i in range(12)) for d in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter()]
 sq=tuple(x*x%5 for x in A);stab=[p for p in auts if tuple(sq[p[i]] for i in range(12))==sq]
 unseen=set(keep);orbs=[]
 while unseen:
  v=next(iter(unseen));O={tuple(v[p[i]] for i in range(12)) for p in stab};O|={tuple(1-x for x in w) for w in O};O&=S;orbs.append(O);unseen-=O
 switch=tuple(0 if a==b else 1 for a,b in zip(A,B));switch_orbit=next(i for i,o in enumerate(orbs) if switch in o)
 edges=list(G.edges());boundary_rows=[]
 for u,v in edges:
  r=[0]*12;r[u]=r[v]=1;boundary_rows.append(r)
 rank=f2rank(boundary_rows,12);cycle_dim=len(edges)-12+1
 checks={
  'all_4096_scanned':sum(hist.values())==4096,
  'exact_spectral_image_98':len(hist)==98,
  'target_fibre_80':len(keep)==80,
  'global_complement_closed':complement,
  'target_not_linear_code':not linear,
  'icosahedral_aut_120':len(auts)==120,
  'magnitude_stabilizer_20':len(stab)==20,
  'target_18_orbits_under_stabilizer_and_complement':len(orbs)==18,
  'pass540_switch_in_target':switch in S,
  'pass540_switch_weight5':sum(switch)==5,
  'cut_space_rank11':rank==11,
  'cycle_space_dimension19':cycle_dim==19,
 }
 return {'schema':'w33.pass544.binary_switch_spectral_fibre.v1','status':'PASS' if all(checks.values()) else 'FAIL','scan':{'sign_words':4096,'distinct_exact_charpolys':len(hist),'target_fibre':len(keep),'weight_distribution':dict(sorted(weights.items())),'linear_code':linear,'complement_closed':complement},'group_action':{'icosahedral_automorphisms':len(auts),'square_magnitude_stabilizer':len(stab),'spectral_fibre_orbits':sorted(len(o) for o in orbs),'pass540_orbit_index':switch_orbit,'pass540_orbit_size':len(orbs[switch_orbit])},'cohomology':{'vertex_switch_space_dimension':12,'global_sign_kernel_dimension':1,'cut_space_dimension':rank,'cycle_space_dimension':cycle_dim,'closed_cycle_observables':'blind to every vertex sign switch'},'conclusion':'The exact spectrum-preserving fibre is a nonlinear 80-word subset of the 12-cube, not a binary linear kernel.','checks':checks,'boundary':'Classification is for the fixed Pass-540 magnitude profile, not all full-support q=5 sections.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 544 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
