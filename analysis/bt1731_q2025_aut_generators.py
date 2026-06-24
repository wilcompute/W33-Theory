#!/usr/bin/env python3
"""BT1731: q2025 low-symmetry chart automorphism generators."""
from __future__ import annotations
from itertools import combinations
from collections import Counter
import json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1731_q2025_aut_generators.json'
RPAIRS=[('YXX','YXY'),('ZZY','ZZZ'),('IZZ','XXZ'),('XII','XYI'),('IXX','YZZ'),('IYX','IYZ'),('IIX','IXY'),('IXI','XZX'),('IIZ','XXY'),('YXI','ZII'),('XXI','ZXX'),('ZYI','ZZI')]
BPAIRS=[('IXZ','YZI'),('IZI','ZXZ'),('ZXI','ZYY'),('XXX','XZI'),('XZY','XZZ'),('YIX','YXZ'),('YZY','ZIY'),('YZX','ZXY'),('IZY','ZZX'),('IZX','YIZ'),('XIY','XYY'),('YYX','YYZ')]
RED=['XXI','IXI','XII','IXY','XXY','XZX','IYZ','ZXX','ZZY','YXY','XYI','YXI','ZZI','ZZZ','IIZ','XXZ','IZZ','ZYI','IXX','IYX','YXX','ZII','YZZ','IIX']
BLUE=['YZX','IZY','ZXZ','XYY','ZZX','YXZ','IZI','YYZ','YZI','IXZ','XXX','XIY','XZZ','IZX','YZY','YIZ','XZI','YYX','ZYY','XZY','YIX','ZXY','ZIY','ZXI']
BITS={'I':(0,0),'X':(1,0),'Y':(1,1),'Z':(0,1)}
def vec(s):
 x=[]; z=[]
 for ch in s:
  a,b=BITS[ch]; x.append(a); z.append(b)
 return tuple(x+z)
def add(a,b): return tuple((x+y)%2 for x,y in zip(a,b))
def symp(a,b):
 n=len(a)//2
 return sum(a[i]*b[n+i]+a[n+i]*b[i] for i in range(n))%2
def triples(labels):
 V={vec(s):s for s in labels}; S=set(V); out=set()
 for a,b in combinations(S,2):
  c=add(a,b)
  if c in S and any(c) and symp(a,b)==0: out.add(tuple(sorted([V[a],V[b],V[c]])))
 return sorted(out)
def qgraph(labels,pairs):
 G=nx.Graph(); idx={}
 for i,p in enumerate(pairs):
  G.add_node(('p',i),kind='point',pair=p)
  for lab in p: idx[lab]=i
 for li,t in enumerate(triples(labels)):
  G.add_node(('l',li),kind='line',triple=t)
  for lab in t: G.add_edge(('p',idx[lab]),('l',li))
 return G
def auts(G):
 GM=nx.algorithms.isomorphism.GraphMatcher(G,G,node_match=lambda a,b:a['kind']==b['kind'])
 return list(GM.isomorphisms_iter())
def perm_summary(G,phi):
 ps=sorted([n for n in G if n[0]=='p'],key=str); ls=sorted([n for n in G if n[0]=='l'],key=str)
 pperm=[ps.index(phi[p]) for p in ps]; lperm=[ls.index(phi[l]) for l in ls]
 return {'point_perm':pperm,'line_perm':lperm,'moved_points':sum(i!=j for i,j in enumerate(pperm)),'moved_lines':sum(i!=j for i,j in enumerate(lperm))}
def prof(G):
 D=nx.DiGraph()
 for u,v in G.edges(): D.add_edge(u,v); D.add_edge(v,u)
 seen=set()
 for cyc in nx.simple_cycles(D,length_bound=10):
  if len(cyc)<3: continue
  n=len(cyc); reps=[]
  for seq in (cyc,list(reversed(cyc))):
   for i in range(n): reps.append(tuple(seq[i:]+seq[:i]))
  seen.add(min(reps,key=str))
 return {'nodes':G.number_of_nodes(),'edges':G.number_of_edges(),'beta1':G.number_of_edges()-G.number_of_nodes()+1,'cycle_counts_le_10':dict(Counter(map(len,seen)))}
def main():
 red=qgraph(RED,RPAIRS); blue=qgraph(BLUE,BPAIRS); RA=auts(red); BA=auts(blue)
 red_nontriv=[a for a in RA if any(k!=v for k,v in a.items())]
 checks={'red_aut_size_2':len(RA)==2,'blue_aut_size_1':len(BA)==1,'red_has_one_involution_generator':len(red_nontriv)==1 and perm_summary(red,red_nontriv[0])['moved_points']>0,'both_beta1_21':prof(red)['beta1']==prof(blue)['beta1']==21,'low_symmetry_vs_reye_576':len(RA)<576 and len(BA)<576}
 payload={'theorem':'BT1731 q2025 automorphism generator classifier','verified':all(checks.values()),'summary':'The q2025 red quotient has exactly one nontrivial color-preserving automorphism, an involution; the q2025 blue quotient is rigid. This gives canonical low-symmetry fingerprints for the two new 48-bus charts and separates them from the cyclic Reye/BT1715 chart with automorphism size 576.','red':{'automorphism_count':len(RA),'profile':prof(red),'generator':perm_summary(red,red_nontriv[0]) if red_nontriv else None},'blue':{'automorphism_count':len(BA),'profile':prof(blue),'generator':None},'checks':checks,'boundary':'Automorphisms are color-preserving incidence automorphisms of the quotient charts, not Pauli-group conjugation automorphisms upstairs.'}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
 print(json.dumps({'verified':payload['verified'],'red_aut':len(RA),'blue_aut':len(BA)},indent=2))
 return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
