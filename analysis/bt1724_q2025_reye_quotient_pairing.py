#!/usr/bin/env python3
"""BT1724: q2025 connected 24_2 cover -> linear 12_4 quotient pairing.

This executes the BT1720 follow-up.  It finds explicit pairings of the red
and corrected-blue q2025 domains.  The quotients are connected linear
(12_4,16_3) configurations with beta_1=21.  They are NOT isomorphic to the
BT544/BT1715 cyclic Reye/Klein-Latin model, so q2025 supplies a distinct
connected 48-bus chart rather than the simple parity cover.
"""
from __future__ import annotations
from itertools import combinations
import json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1724_q2025_reye_quotient_pairing.json'
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
def graph(tris):
 G=nx.Graph()
 for p in sorted({x for t in tris for x in t}): G.add_node(('p',p),kind='point')
 for i,t in enumerate(tris):
  G.add_node(('l',i),kind='line')
  for p in t: G.add_edge(('p',p),('l',i))
 return G
def qgraph(labels,pairs):
 G=graph(triples(labels)); Q=nx.Graph(); idx={}
 for i,(a,b) in enumerate(pairs):
  Q.add_node(('p',i),kind='point',pair=(a,b)); idx[('p',a)]=i; idx[('p',b)]=i
 for n in G:
  if n[0]=='l': Q.add_node(n,kind='line')
 for p in [n for n in G if n[0]=='p']:
  for l in G.neighbors(p): Q.add_edge(('p',idx[p]),l)
 return Q
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
def profile(Q):
 ps=[n for n in Q if n[0]=='p']; ls=[n for n in Q if n[0]=='l']
 mx=max(len(set(Q.neighbors(a))&set(Q.neighbors(b))) for a,b in combinations(ps,2))
 return {'nodes':Q.number_of_nodes(),'edges':Q.number_of_edges(),'points':len(ps),'lines':len(ls),'point_degrees':sorted(set(Q.degree(p) for p in ps)),'line_degrees':sorted(set(Q.degree(l) for l in ls)),'connected':nx.is_connected(Q),'beta1':Q.number_of_edges()-Q.number_of_nodes()+nx.number_connected_components(Q),'max_pair_line_overlap':mx}
def main():
 R=reye_graph(); B=bt1715_graph(); red=qgraph(RED,RPAIRS); blue=qgraph(BLUE,BPAIRS)
 checks={'red_linear_12_4_16_3':profile(red)['points']==12 and profile(red)['lines']==16 and profile(red)['point_degrees']==[4] and profile(red)['line_degrees']==[3] and profile(red)['max_pair_line_overlap']==1,'blue_linear_12_4_16_3':profile(blue)['points']==12 and profile(blue)['lines']==16 and profile(blue)['point_degrees']==[4] and profile(blue)['line_degrees']==[3] and profile(blue)['max_pair_line_overlap']==1,'both_beta1_21':profile(red)['beta1']==profile(blue)['beta1']==21,'bt544_reye_equals_bt1715':nx.is_isomorphic(R,B,node_match=lambda x,y:x['kind']==y['kind']),'q2025_quotients_not_bt544_reye':not nx.is_isomorphic(red,R,node_match=lambda x,y:x['kind']==y['kind']) and not nx.is_isomorphic(blue,R,node_match=lambda x,y:x['kind']==y['kind'])}
 payload={'theorem':'BT1724 q2025 connected quotient pairing theorem','verified':all(checks.values()),'summary':'Explicit pairings fold the red and corrected-blue q2025 (24_2,16_3) domains into connected linear (12_4,16_3) quotients with beta_1=21. These quotients are not isomorphic to the BT544/BT1715 cyclic Reye/Klein-Latin chart, so q2025 supplies a distinct connected 48-bus chart.','red_pairing':RPAIRS,'blue_pairing':BPAIRS,'red_profile':profile(red),'blue_profile':profile(blue),'isomorphism_tests':{'BT544_reye_vs_BT1715':True,'red_vs_BT544_reye':False,'blue_vs_BT544_reye':False},'checks':checks,'boundary':'This solves the q2025 quotient pairing as a linear 12_4 bus. It also falsifies the stronger claim that the quotient is the existing BT544 cyclic Reye chart.'}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
 print(json.dumps({'verified':payload['verified'],'red':payload['red_profile'],'blue':payload['blue_profile']},indent=2))
 return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
