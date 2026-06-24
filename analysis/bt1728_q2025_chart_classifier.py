#!/usr/bin/env python3
"""BT1728: classify the q2025 connected 48-bus charts against Reye/BT1715."""
from __future__ import annotations
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1728_q2025_chart_classifier.json'
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
 T=triples(labels); G=nx.Graph(); idx={}
 for i,p in enumerate(pairs):
  G.add_node(('p',i),kind='point',pair=p)
  for lab in p: idx[lab]=i
 for li,t in enumerate(T):
  G.add_node(('l',li),kind='line',triple=t)
  for lab in t: G.add_edge(('p',idx[lab]),('l',li))
 return G
def reye_graph():
 OFF={(0,1):2,(0,2):1,(0,3):0,(1,0):2,(1,2):1,(1,3):1,(2,0):1,(2,1):1,(2,3):1,(3,0):2,(3,1):0,(3,2):0}
 G=nx.Graph()
 for a in range(4):
  for b in range(3): G.add_node(('p',(a,b)),kind='point')
 lines=[]
 for a in range(4): lines.append([(a,b) for b in range(3)])
 for omit in range(4):
  for t in range(3): lines.append([(a,(t+OFF[(omit,a)])%3) for a in range(4) if a!=omit])
 for i,L in enumerate(lines):
  G.add_node(('l',i),kind='line')
  for p in L: G.add_edge(('p',p),('l',i))
 return G
def bt1715_graph():
 def lat(i,j): return i^j
 G=nx.Graph(); axes=[('R',i) for i in range(4)]+[('C',i) for i in range(4)]+[('S',i) for i in range(4)]
 for a in axes: G.add_node(('p',a),kind='point')
 for i in range(4):
  for j in range(4):
   G.add_node(('l',(i,j)),kind='line')
   for a in [('R',i),('C',j),('S',lat(i,j))]: G.add_edge(('p',a),('l',(i,j)))
 return G
def spectra(G):
 A=nx.to_numpy_array(G,nodelist=sorted(G.nodes(), key=str))
 vals=np.linalg.eigvalsh(A)
 return {str(k):v for k,v in sorted(Counter(round(float(x),6) for x in vals).items())}
def cycle_counts(G,max_len=10):
 D=nx.DiGraph()
 for u,v in G.edges(): D.add_edge(u,v); D.add_edge(v,u)
 seen=set()
 for cyc in nx.simple_cycles(D,length_bound=max_len):
  if len(cyc)<3: continue
  n=len(cyc); rots=[]
  for seq in (cyc,list(reversed(cyc))):
   for i in range(n): rots.append(tuple(seq[i:]+seq[:i]))
  seen.add(min(rots,key=str))
 return {str(k):v for k,v in sorted(Counter(map(len,seen)).items())}
def aut_count(G):
 GM=nx.algorithms.isomorphism.GraphMatcher(G,G,node_match=lambda a,b:a['kind']==b['kind'])
 return sum(1 for _ in GM.isomorphisms_iter())
def profile(G):
 return {'nodes':G.number_of_nodes(),'edges':G.number_of_edges(),'connected':nx.is_connected(G),'beta1':G.number_of_edges()-G.number_of_nodes()+nx.number_connected_components(G),'spectrum':spectra(G),'cycle_counts_le_10':cycle_counts(G,10),'automorphisms_color_preserving':aut_count(G)}
def main():
 graphs={'red':qgraph(RED,RPAIRS),'blue':qgraph(BLUE,BPAIRS),'reye_bt544':reye_graph(),'bt1715_klein_latin':bt1715_graph()}
 iso={}
 for a,b in combinations(graphs,2):
  iso[f'{a}__{b}']=nx.is_isomorphic(graphs[a],graphs[b],node_match=lambda x,y:x['kind']==y['kind'])
 checks={'red_aut_2':aut_count(graphs['red'])==2,'blue_aut_1':aut_count(graphs['blue'])==1,'reye_and_bt1715_same':iso['reye_bt544__bt1715_klein_latin'] is True,'red_blue_not_same':iso['red__blue'] is False,'q2025_not_reye':all(not iso[k] for k in ['red__reye_bt544','red__bt1715_klein_latin','blue__reye_bt544','blue__bt1715_klein_latin']),'all_beta1_21':all(profile(G)['beta1']==21 for G in graphs.values())}
 payload={'theorem':'BT1728 q2025 48-bus chart classifier','verified':all(checks.values()),'summary':'The q2025 red and blue quotients are connected linear 12_4/16_3 48-bus charts with beta1=21, but they are spectrally and automorphically distinct from each other and from the BT544/BT1715 cyclic Reye chart. Red has automorphism group size 2; blue has size 1; cyclic Reye/BT1715 has size 576.','profiles':{k:profile(v) for k,v in graphs.items()},'isomorphism_matrix':iso,'checks':checks}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
 print(json.dumps({'verified':payload['verified'],'automorphisms':{k:payload['profiles'][k]['automorphisms_color_preserving'] for k in graphs},'checks':checks},indent=2))
 return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
