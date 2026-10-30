#!/usr/bin/env python3
"""Exact local moment calculation of intrinsic H_p Cayley walk.
Proves the horizontal 2 + central weight-2 anisotropy, not spacetime.
"""
from fractions import Fraction
from collections import defaultdict
import json

def Hmul(a,b):
 x,y,z=a;u,v,w=b
 return x+u,y+v,z+w+x*v

STEP=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0))
def lap(f,x):
 return sum(f(Hmul(x,t)) for t in STEP)-4*f(x)
def verify():
 laws={
 'x':(lambda x:x[0],lambda x:0),
 'y':(lambda x:x[1],lambda x:0),
 'z':(lambda x:x[2],lambda x:0),
 'x_squared':(lambda x:x[0]**2,lambda x:2),
 'y_squared':(lambda x:x[1]**2,lambda x:2),
 'z_squared':(lambda x:x[2]**2,lambda x:2*x[0]**2),
 'y_times_z':(lambda x:x[1]*x[2],lambda x:2*x[0])
 }
 points=[(x,y,z) for x in range(-3,4) for y in range(-3,4)
                     for z in (-3,0,3)]
 for name,(f,target) in laws.items():
  for p in points:assert lap(f,p)==target(p),(name,p)
 # Group commutator of the horizontal generators yields unit center.
 X=(1,0,0);Y=(0,1,0);Xi=(-1,0,0);Yi=(0,-1,0)
 cur=(0,0,0)
 for step in (X,Y,Xi,Yi):cur=Hmul(cur,step)
 assert cur==(0,0,1)
 # Weighted dilation r maps x,y,z to rx,ry,r^2 z.
 # The two horizontal right-invariant vector fields are
 # D_x = d/dx, D_y=d/dy+x*d/dz, hence the continuum
 # sub-Laplacian D_x^2+D_y^2, homogeneous order two.
 return dict(status="PASS",exact_polynomial_identities=list(laws.keys()),
   tested_points=len(points),commutator_loop_length=4,
   commutator_center_shift=cur,homogeneous_weights=[1,1,2],
   Hausdorff_homogeneous_dimension=4,
   continuum_horizontal_generator="(d/dx)^2+(d/dy+x*d/dz)^2",
   discrete_laplacian="L f(g)=f(g X)+f(g X^-1)+f(g Y)+f(g Y^-1)-4 f(g)",
   key_anisotropy="L(z^2)=2*x^2, while L(x^2)=L(y^2)=2; no constant Euclidean vertical diffusivity.",
   boundary="A wave recurrence on this graph has finite graph-propagation speed but does not produce a 3+1 Lorentzian geometry or a unique causal light cone for physics.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
