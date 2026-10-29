#!/usr/bin/env python3
"""Exact finite Heisenberg group H27 chiral sector and intrinsic Cayley growth.
The H_p family has non-Riemannian homogeneous dimension 4, not 3+1 spacetime.
"""
import json,math
import numpy as np

def group_law(u,v,p=None):
 a,b,c=u;x,y,z=v
 t=(a+x,b+y,c+z+a*y)
 return tuple(w%p for w in t) if p else t

def balls(R,p=None):
 seen={(0,0,0)};front=seen;counts=[1]
 gens=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0))
 for radius in range(1,R+1):
  nxt={group_law(g,h,p) for g in front for h in gens}-seen
  seen|=nxt;front=nxt;counts.append(len(seen))
 return counts

def h27_blocks():
 w=np.exp(2j*np.pi/3)
 mats=[]
 for k in range(3):
  M=np.zeros((9,9),complex)
  for a in range(3):
   for b in range(3):
    u=3*a+b
    for dx in (-1,1):M[3*((a+dx)%3)+b,u]+=1
    for dy in (-1,1):M[3*a+(b+dy)%3,u]+=w**(k*a*dy)
  assert np.max(np.abs(M-M.conj().T))<1e-13
  mats.append(M)
 assert np.max(np.abs(mats[1].conj()-mats[2]))<1e-12
 eig=[np.linalg.eigvalsh(M) for M in mats]
 err=float(np.max(np.abs(eig[1]-eig[2])))
 assert err<1e-12
 shifts=[float(-2*math.sin(2*math.pi*k/3)) for k in range(3)]
 assert abs(shifts[1]+shifts[2])<1e-12
 return dict(regular_rep_dim=27,central_sector_dims=[9]*3,
             conjugate_sector_eigenvalue_max_gap=err,
             explicit_K_odd_center_term="i*(Z-Z^-1)",
             imposed_term_sector_shifts=shifts,
             energies=[[round(float(x),9) for x in row] for row in eig])

def verify():
 integral=balls(15)
 finite=balls(15,211)
 assert integral==finite
 small=balls(8,3)
 assert small[-1]==27 and next(i for i,v in enumerate(small) if v==27)==4
 assert integral[15]==21569 and integral[7]==1069
 # Established Bass-Guivarch growth exponent:
 # ranks of H/[H,H] and [H,H] are 2,1, weighted 1,2.
 dimension=1*2+2*1
 assert dimension==4
 return dict(status="PASS",H27_ball_volumes=small,H27_diameter=4,
             infinite_integer_Heisenberg_ball_volumes_r0_to15=integral,
             H211_matching_ball_volumes_r0_to15=finite,
             volume_doubling_B14_over_B7=integral[14]/integral[7],
             established_homogeneous_growth_dimension=dimension,
             central_H27=h27_blocks(),
             boundary="Natural bounded-degree H_p address graphs: growth dimension4 is sub-Riemannian, not Einstein 3+1; chirality splitting needs an imposed K-odd term.")

if __name__=="__main__":print(json.dumps(verify(),indent=2))
