"""Pointwise-to-neighborhood quantum coercivity across all 160
single-current-factor hyperplane representatives.

Round13 owns Vopt(q_e)>=25600/77571 at q_e=-a V_e/||V_e||².
For each e and an explicit edge-dual 8-cycle w_e, compute
min nonzero |t_i| (over support of w_e), where
z_i(q_e)=a*t_i. For any ||q-q_e||<=r<
min|t_i|/sqrt39,
|z_i(q)| >= a*(|t_i|-sqrt39*r).
Weighted Cauchy yields
Vopt(q)>= (25600/77571)*(1-sqrt39*r/t_min)^2.
At half critical radius, >=6400/77571 everywhere in the ball.
This is a genuine full-H wavefunction local form bound near
every one-factor zero, with uniform explicit radius. Does NOT
cover multi-factor classical zeros or produce global E0.
"""
import sys,json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261008_5state_ritz import geometry
import w33_pass11769_quantized_current_vacuum as H
def certificate():
 edges,*_=geometry()
 g=H.geometry()
 u=np.rint(40*g['u']).astype(np.int64)
 v=np.rint(40*g['v']).astype(np.int64)
 graph=nx.Graph();graph.add_nodes_from(range(80));graph.add_edges_from(edges)
 ix={frozenset(e):i for i,e in enumerate(edges)}
 tmins=[];bounds=[]
 for e0,(p,l) in enumerate(edges):
  graph.remove_edge(p,l);path=nx.shortest_path(graph,p,l);graph.add_edge(p,l)
  seq=[e0]+[ix[frozenset((path[k],path[k+1]))] for k in range(7)]
  c=np.zeros(160,dtype=np.int64)
  for j,i in enumerate(seq):c[i]=1 if j%2==0 else -1
  w=np.ones(160,dtype=np.int64)-c
  assert np.array_equal(w@u,np.zeros(80,dtype=np.int64)) and w[e0]==0
  dot=v@v[e0]; assert int(v[e0]@v[e0])==3120
  ts=[F(3120-int(x),3120) for x in dot]
  mn=min(abs(ts[i]) for i in range(160) if w[i]!=0)
  assert mn>0
  den=sum((F(int(w[i]*w[i]),1)/ts[i]**2 for i in range(160) if w[i]),F(0))
  lb=F(160*160,400)/den
  tmins.append(mn);bounds.append(lb)
 assert set(tmins)=={tmins[0]} and set(bounds)=={F(25600,77571)}
 mn=tmins[0];r_half=f'{mn}/(2*sqrt(39))'
 lower_half=bounds[0]/4
 assert lower_half>F(0)
 return dict(status='PASS',
   verified_channel_representatives=160,
   exact_t_min=str(mn),
   center_dual_coercivity_bound=str(bounds[0]),
   rigorous_ball_radius_half_min='('+str(mn)+')/(2*sqrt39)',
   rigorous_uniform_energy_lower_on_all_160_balls=str(lower_half),
   theorem='For each edge e, all psi supported in ||q-q_e||<=r< tmin/sqrt39 obey h[psi]>= [25600/77571]*(1-sqrt39*r/tmin)^2 ||psi||². At r=tmin/(2sqrt39), this is 6400/77571. The exact value tmin is common to all 160 edge-transitive strata and is the minimum nonvanishing affine ratio on the support of its 8-cycle dual.',
   proof='For w_e with U.T w=0 and w_e[e]=0, fix q_e. Bound |z_i(q)| >= a*(|t_i|-sqrt39*r) >= a |t_i|*(1-r sqrt39/tmin), and Cauchy weighted-dual energy bound propagates from center to entire ball.',
   boundary='Wavefunctions supported in 160 small neighborhoods, not all configuration R^78. Known simultaneous classical zeros remain and global E0 remains without enclosure.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round14_all160_uniform_tube_bound.json').write_text(json.dumps(d,indent=2)+'\n')
 print('UNIFORM TUBE',d['exact_t_min'],d['rigorous_ball_radius_half_min'],d['rigorous_uniform_energy_lower_on_all_160_balls'])
