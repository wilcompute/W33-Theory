#!/usr/bin/env python3
"""Exact n-step second moments of simple random walk on integral Heisenberg H(Z).
Proof: each step uniformly X±,Y±, so horizontal increments have mean0
and variance 1/2. z_n=sum_{k=1}^n x_{k-1} Delta y_k is a martingale
with orthogonal increments, yielding E[z_n^2]=n(n-1)/8, while
E[x_n^2]=E[y_n^2]=n/2. These are sub-Riemannian,
not isotropic 3D Brownian or emergent Lorentzian 3+1 spacetime.
"""
import json
from collections import defaultdict
from fractions import Fraction as F
STEPS=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0))
def multiply(a,b):
 x,y,z=a;u,v,w=b
 return x+u,y+v,z+w+x*v
def verify(N=12):
 paths={(0,0,0):1};rows=[]
 for n in range(N+1):
  den=4**n
  sx=sum(x*x*c for (x,y,z),c in paths.items())
  sy=sum(y*y*c for (x,y,z),c in paths.items())
  sz=sum(z*z*c for (x,y,z),c in paths.items())
  assert sx*2==n*den
  assert sy*2==n*den
  assert sz*8==n*(n-1)*den
  rows.append(dict(step=n,occupied_group_elements=len(paths),
    E_x_squared=str(F(sx,den)),E_y_squared=str(F(sy,den)),
    E_center_squared=str(F(sz,den))))
  next_paths=defaultdict(int)
  for a,c in paths.items():
   for b in STEPS:next_paths[multiply(a,b)]+=c
  paths=next_paths
 assert rows[-1]["occupied_group_elements"]==5167
 return dict(status="PASS",verified_integer_path_counts_up_to=N,
   exact_all_n_theorem=["E[x_n^2]=n/2","E[y_n^2]=n/2",
                        "E[z_n^2]=n(n-1)/8"],
   proof="Independent zero-mean step increments, E(dx^2)=E(dy^2)=1/2, E(dy_k|past)=0, center increment x_(k-1)*dy_k; martingale orthogonality gives sum_(k=1)^n E[x_(k-1)^2]/2 = n(n-1)/8.",
   moment_table=rows,
   consequence="Horizontal rms ~sqrt(n), central rms ~n; no isotropic 3D diffusive scaling or 3+1 Lorentzian spacetime follows.",
   notes="Discrete n=1 central variance zero. Finite H_p agrees with integral group only before wraparound; theorem is on infinite integral H(Z).")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
