"""Exact polar-plane permutation-module symplectic test for W33 H27.

Compute invariant alternating bilinear forms on F3[13] and rank on the
12D augmentation module, under explicit point-stabilizer generators.
This tests a candidate bridge with the H13 12D phase space; it does
not identify the two group actions or Lie algebras.
"""
import json,itertools,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"analysis"))
from w33_20261008_h27_h13_five_frontiers import J,canon,um
from w33_20261008_five_physics_frontiers import projective_points_and_lines
OUT=R/"data"/"w33_20261008_polar13_symplectic_module.json"

def rref_rank(a,p=3):
 a=np.array(a,dtype=np.int64)%p
 r=0
 for j in range(a.shape[1]):
  t=next((i for i in range(r,a.shape[0]) if a[i,j]%p),None)
  if t is None:continue
  a[[r,t]]=a[[t,r]]
  a[r]=(a[r]*pow(int(a[r,j]),-1,p))%p
  for i in range(a.shape[0]):
   if i!=r and a[i,j]:
    a[i]=(a[i]-a[i,j]*a[r])%p
  r+=1
  if r==a.shape[0]:break
 return r

def generator(a):
 a=np.array(a,dtype=int)%3
 assert np.array_equal((a.T@J@a)%3,J%3)
 return a

def analyze():
 pts,_=projective_points_and_lines()
 p=pts[pts.index((1,0,0,0))]
 plane=sorted(v for v in pts if v[3]==0)
 assert len(plane)==13
 idx={v:i for i,v in enumerate(plane)}
 E=np.eye(4,dtype=int)
 Ux=generator(um(1,0,0));Uy=generator(um(0,1,0))
 L1=generator([[1,0,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,1]])
 L2=generator([[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]])
 D=generator([[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,-1]])
 G=[Ux,Uy,L1,L2,D]
 perm=[tuple(idx[canon(g@np.asarray(v))] for v in plane) for g in G]
 assert all(len(set(z))==13 for z in perm)
 # Closure of the *projective* polar-plane action, not Sp4 matrix group.
 identity=tuple(range(13));closure={identity};queue=[identity]
 for t in queue:
  for s in perm:
   w=tuple(t[s[i]] for i in range(13))
   if w not in closure:closure.add(w);queue.append(w)
 print('COMPUTED_POINT_STABILIZER_IMAGE_ORDER',len(closure),flush=True)
 assert len(closure) in (216,432)
 # Canonical 1 + four triplet orbit decomposition under Ux,Uy.
 remaining=set(range(13));orbits=[]
 while remaining:
  st=min(remaining);todo={st}
  for v in tuple(todo):
   pass
  queue=[st]
  for v in queue:
   for q in perm[:2]:
    w=q[v]
    if w not in todo:todo.add(w);queue.append(w)
  remaining-=todo;orbits.append(sorted(todo))
 assert sorted(map(len,orbits))==[1,3,3,3,3]
 # Signed oriented pair orbits: if an orbit includes its transpose,
 # invariant skew bilinear forms vanish on that entire orbital.
 seen=set();alternating=[]
 for i in range(13):
  for j in range(13):
   if i==j or (i,j) in seen:continue
   todo={(i,j)};queue=[(i,j)]
   for a,b in queue:
    for q in perm:
     w=(q[a],q[b])
     if w not in todo:todo.add(w);queue.append(w)
   rev={(b,a) for a,b in todo}
   seen |=todo|rev
   if todo&rev:continue
   M=np.zeros((13,13),dtype=int)
   for a,b in todo:M[a,b]=1
   for a,b in rev:M[a,b]=2
   assert all(np.array_equal(M[np.ix_(q,q)],M) for q in perm)
   alternating.append(M)
 B=np.zeros((13,12),int)
 anchor=idx[p]
 others=[q for q in range(13) if q!=anchor]
 for i,v in enumerate(others): B[v,i]=1;B[anchor,i]=2
 aug=[(B.T@M@B)%3 for M in alternating]
 # Search all F3 coefficient combinations (reasonable if dimension <=9)
 d=len(aug)
 ranks={}
 witness=None
 if d<=10:
  for vec in itertools.product(range(3),repeat=d):
   Q=sum((c*e for c,e in zip(vec,aug)),np.zeros((12,12),int))%3
   rank=rref_rank(Q)
   ranks[rank]=ranks.get(rank,0)+1
   if rank==12 and witness is None:witness=list(vec)
 else:
  rng=np.random.default_rng(20261008)
  for _ in range(500):
   vec=rng.integers(0,3,size=d)
   Q=sum((int(c)*e for c,e in zip(vec,aug)),np.zeros((12,12),int))%3
   rank=rref_rank(Q)
   ranks[rank]=ranks.get(rank,0)+1
   if rank==12 and witness is None:witness=[int(v) for v in vec]
 return {"plane_points":13,"H27_plane_orbit_sizes":sorted(map(len,orbits)),
   "tested_symplectic_stabilizer_generators":len(G),
   "projective_stabilizer_image_order":len(closure),
   "invariant_alternating_form_dimension":d,
   "augmentation_rank":12,
   "alternating_rank_histogram":ranks,
   "nondegenerate_witness_coefficients":witness,
   "max_attained_rank":max(ranks),
   "scope":"This tests induced projective point permutation action on augmentation, NOT an equivariant identification with C8 Jacobi sp6 module",
   "generators":[m.tolist() for m in G],
   "point_orbits":orbits}

if __name__=="__main__":
 x=analyze()
 OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(json.dumps({k:v for k,v in x.items() if k!="generators"},indent=2))
 print("POLAR_MODULE_TEST_PASS")
