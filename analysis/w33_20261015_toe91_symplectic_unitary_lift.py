"""TOE91: explicit four-generator projective unitary lifts for Witting PSp(4,3).

Construct 4x4 U from one Witting orthonormal tetrad and compatibility
phases read from every ray's coordinates. Verify all 40 projective ray
images, unitary condition, order-three scalar cocycles, and action on
40 orthogonal tetrads. This is not a mapping into two-qutrit CSS gates.
"""
from __future__ import annotations
import json,numpy as np
from analysis.w33_20261015_toe91_symplectic_phase_audit import ROOT,R,transvection
from tools.bt1408_witting_contextual_communication_bridge import find_tetrads
def lift(perm):
 B=np.array([0,1,2,3]);D=np.array([perm[i] for i in B])
 r=R[B].T; t=R[D].T
 G=r.conj().T@R.T
 H=t.conj().T@R[np.array(perm)].T
 # Solve target phase U*r_i ∝ ray_perm(i): lambda_j G_jh = c_h H_jh.
 phase={0:1+0j};links={}
 for h in range(40):
  support=[j for j in range(4) if abs(G[j,h])>1e-9 and abs(H[j,h])>1e-9]
  for i in support:
   for j in support:
    if i==j:continue
    v=(H[i,h]/G[i,h])/(H[j,h]/G[j,h]) # lambda_i/lambda_j
    links.setdefault(j,[]).append((i,v))
 frontier=[0]
 while frontier:
  j=frontier.pop()
  for i,v in links.get(j,[]):
   cand=phase[j]*v
   cand/=abs(cand)
   if i not in phase:phase[i]=cand;frontier.append(i)
   else:assert abs(phase[i]-cand)<1e-8
 assert len(phase)==4
 U=t@np.diag([phase[j] for j in range(4)])@r.conj().T
 assert np.max(abs(U.conj().T@U-np.eye(4)))<1e-10
 worst=max(1-abs(np.vdot(U@R[i],R[perm[i]])) for i in range(40))
 assert worst<1e-10
 eig=U@U@U
 scalar=np.trace(eig)/4
 assert np.max(abs(eig-scalar*np.eye(4)))<1e-9
 return U,worst,scalar

def certificate():
 tetrads=[tuple(b) for b in find_tetrads(list(R))]
 all_bases=set(frozenset(b) for b in tetrads)
 records=[]
 for j in range(4):
  v=[int(k==j) for k in range(4)]
  perm=transvection(v)
  U,res,z=lift(perm)
  assert all(frozenset(perm[k] for k in b) in all_bases for b in tetrads)
  # Fix global phase so generator's cube is I; use numerical complex root.
  U=U*np.exp(-1j*np.angle(z)/3)
  assert np.max(abs(U@U@U-np.eye(4)))<1e-9
  records.append({'generator_F3_vector':v,'permutation_40':perm,
   'phase_adjusted_4x4_unitary_real':[[round(float(y.real),12) for y in row] for row in U],
   'phase_adjusted_4x4_unitary_imag':[[round(float(y.imag),12) for y in row] for row in U],
   'max_projective_ray_image_residual':round(float(res),12),
   'max_orthonormality_residual':round(float(np.max(abs(U.conj().T@U-np.eye(4)))),12),
   'generator_cube_is_identity':True,'maps_all_40_tetrads':True})
  print('LIFT',j,'unital',records[-1]['max_orthonormality_residual'],'40 rays all',flush=True)
 return {'tested_generators':records,'basis_mapping_source':'docs/witting_graph_isomorphism.md and tools/witting_graph_isomorphism.py',
  'status':'Explicit numerical U(4) projective lifts for four symplectic transvections. Projective cocycle across the full PSp group and global normalizer classification not established.',
  'physics_limit':'A 4D ququart unitary is not, by itself, a physically native 135-qutrit CSS Clifford operator.'}
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261015_toe91_symplectic_unitary_lift.json').write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
