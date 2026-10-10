"""TOE32: native W33 17-fold cover local ball growth and quantum tails.

Exactly verify radius<=4 tree-like exponential growth from girth10,
which differs from 3D cubic volume scaling; continuous-time local
adjacency Schr dynamics has analytic nonzero leading amplitudes at all
finite distances, so no strict null-cone without added mechanics.
"""
from pathlib import Path
from collections import deque
import json,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
OUT=ROOT/'data/w33_20261010_toe32_cover_causal_growth.json'
def run():
 cover=json.loads((ROOT/'data/w33_20261009_toe31_compact_voltage_cover.json').read_text())
 v=cover['smallest_connected_cover_found_in_this_search']['voltages'];p=17
 ed,D,C=wilson();N=80*p
 G=[[] for _ in range(N)]
 for (a,b),z in zip(ed,v):
  for x in range(p):
   i=a*p+x;j=b*p+((x+z)%p)
   G[i].append(j);G[j].append(i)
 assert all(len(g)==4 for g in G)
 roots=[0,1,16,17,34,51,68,85,170,340,680,1000,1359]
 samples=[]
 for root in roots:
  dist=[-1]*N;dist[root]=0;qq=deque([root])
  while qq:
   x=qq.popleft()
   for y in G[x]:
    if dist[y]==-1:dist[y]=dist[x]+1;qq.append(y)
  shell=[dist.count(i) for i in range(max(dist)+1)]
  assert shell[:5]==[1,4,12,36,108],(root,shell[:5])
  balls=np.cumsum(shell).tolist()
  samples.append(dict(root=root,diameter_eccentricity=max(dist),first_nine_shell_sizes=shell[:9],
    radius_0_to_8_balls=balls[:9]))
 assert all(s['radius_0_to_8_balls'][:5]==[1,5,17,53,161] for s in samples)
 # Contrast tree-like volume and cubic spacetime shell:
 cubic=[(4*r**3+6*r**2+8*r+3)//3 for r in range(0,5)]
 assert cubic==[1,7,25,63,129]
 # For continuous-time Schr evolution exp(-itA), first nonzero
 # term at distance d is (-it)^d/d! (A^d)_{uv}. Since A^d counts
 # walks and is >0 for u,v distance d, this coefficient is nonzero.
 # Therefore no IDENTICALLY zero amplitude on a strict graph cone
 # for any finite d. Accidental zeros may occur at special times.
 # Bound |<u|U(t)|v>| <= sum_{n=d}∞ (4|t|)^n/n!.
 bounds={}
 t=.1
 for dist in range(1,9):
  x=4*t
  rhs=math.exp(x)-sum(x**n/math.factorial(n) for n in range(dist))
  bounds[str(dist)]=rhs
 assert bounds['4']<.002
 r=dict(status='PASS',base='connected degree17 W33 Levi cover with 1360 vertices and exact girth10',n=N,degree=4,girth=10,
   sampled_root_ball_growth=samples,infinite_degree4_tree_shell_r0_to4=[1,4,12,36,108],
   sampled_native_ball_counts_r0_to4=[1,5,17,53,161],cubic_Z3_spatial_ball_counts_r0_to4=cubic,
   exact_reason='In a 4-regular graph of girth 10 the rooted neighborhood through radius4 is a tree, so shells grow as 4*3^(r-1) for 1<=r<=4. By contrast Z3 cubic lattice ball volume = (4r³+6r²+8r+3)/3; this is imposed locality, not the same volume growth.',
   t_dimensionless=t,conservative_continuous_time_amplitude_upper_bound_by_distance=bounds,
   quantum_dynamical_no_strict_cone='For U(t)=exp(-it A), the Taylor coefficient for first nonzero graph-distance d is (-i)^d(A^d)uv/d!, nonzero because positive walk count. Thus a strictly vanishing finite-speed cone is not a property of continuous-time finite-range quantum hopping; approximate Lieb–Robinson behavior is possible instead. The tail bound uses graph max row sum4.',
   distinction='No physical spacetime, metric, universal c, Einstein dynamics or critical spectral dimension derived. Existing Round28 LEAPFROG strict discrete step-cone uses a different dynamical update.')
 OUT.write_text(json.dumps(r,indent=2)+'\n');print('TOE32 graph balls',samples[0]['radius_0_to_8_balls'],'ecc',samples[0]['diameter_eccentricity'],flush=True)
 return r
if __name__=='__main__':run()
