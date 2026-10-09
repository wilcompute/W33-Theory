"""Classify 86400 exactly optimal 3-flag isotropy selectors
under the full 25,920-element PSp(4,3) group.

The native harmonic 160-flag Gram projector 160P has diagonal81
and four off diagonal classes {-27,-3,1,9}. Optimal triples
are triangles in the +1 relation graph. Group action on
point-line flags (p,l) is induced by actual projective
symplectic permutations, with full line mapping checked.
Compute orbit decomposition; each orbit size must divide25920,
an EXACT G-set/Symmetry-breaking landscape certificate.

This is not a physical dynamical potential or spacetime.
"""
import json,sys,itertools
from pathlib import Path
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as B
import w33_20261008_five_physics_frontiers as G
import w33_20261008_5state_ritz as E
from w33_20261009_canonical_triplet_isotropy_theorem import certificate as base
def certificate():
 pts,raw_lines=G.projective_points_and_lines()
 pidx={p:i for i,p in enumerate(pts)}
 lines=[tuple(pidx[p] for p in l) for l in raw_lines]
 assert pts==B.make_points() and lines==B.w33_lines(pts)
 edges,*_=E.geometry();lineidx={tuple(z):i for i,z in enumerate(lines)}
 assert all((p,40+j) in edges for j,l in enumerate(lines) for p in l)
 edge_idx={x:i for i,x in enumerate(edges)}
 N=np.zeros((80,160),dtype=np.int64)
 for j,(p,l) in enumerate(edges):N[p,j]=1;N[l,j]=-1
 L=N@N.T;Lp=-47*(L@L@L@L)+900*(L@L@L)-5686*(L@L)+12152*L
 assert np.all((N.T@Lp@N)%80==0)
 P=(12800*np.eye(160,dtype=np.int64)-N.T@Lp@N)//80
 A=P==1;np.fill_diagonal(A,0)
 remaining=set()
 for i in range(160):
  for j in range(i+1,160):
   if not A[i,j]:continue
   for k in range(j+1,160):
    if A[i,k] and A[j,k]:remaining.add((i,j,k))
 assert len(remaining)==86400
 gp=B.projective_group(pts);assert len(gp)==25920
 # Cache only line maps needed for triplets; no large 25920x160 arrays.
 outcomes=[]
 while remaining:
  seed=min(remaining)
  orbit=set();stab_actions=[]
  for g in gp:
   triple=[]
   for f in seed:
    p,l=edges[f]
    pl=tuple(sorted(g[pt] for pt in lines[l-40]))
    triple.append(edge_idx[(g[p],40+lineidx[pl])])
   key=tuple(sorted(triple))
   orbit.add(key)
   if key==seed:stab_actions.append(tuple(seed.index(z) for z in triple))
  assert orbit<=remaining,(len(orbit),len(orbit-remaining))
  assert len(gp)%len(orbit)==0
  assert len(stab_actions)==len(gp)//len(orbit)
  outcomes.append(dict(representative=list(seed),orbit_size=len(orbit),
      stabilizer_order=len(gp)//len(orbit),
      induced_permutation_image_order=len(set(stab_actions)),
      pointwise_triple_stabilizer_order=stab_actions.count((0,1,2)),
      induced_permutation_action_sample=[list(z) for z in sorted(set(stab_actions))]))
  remaining-=orbit
  print('ISOTROPY ORBIT',len(outcomes),len(orbit),'remain',len(remaining),flush=True)
 assert sum(z['orbit_size'] for z in outcomes)==86400
 return dict(status='PASS',G='PSp(4,3)',group_order=25920,total_optimal_triples=86400,
  number_of_orbits=len(outcomes),orbits=sorted(outcomes,key=lambda x:(x['orbit_size'],x['representative'])),
  orbit_stabilizer_verified=True,
  physical_boundary='Exact discrete PSp orbit decomposition of a graph-theoretic 3-flag isotropy selection space. Does not produce a preferred orbit, an energy potential, emergent 3D spacetime, or Lorentzian dynamics.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_PSp_orbits_isotropic_triplets.json').write_text(json.dumps(d,indent=2)+'\n')
 print('ORBIT SIZES',[(o['orbit_size'],o['stabilizer_order']) for o in d['orbits']])
