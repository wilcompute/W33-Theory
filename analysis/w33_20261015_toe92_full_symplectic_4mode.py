"""TOE92: certify global projective PSp(4,3) four-mode Witting action.

Enumerate all 40-ray permutations from 5 symplectic transvections.
Assign 4x4 unitary words along a BFS spanning tree. For every one of
the 5*|G| Cayley edges, verify projective multiplication closes in U4.
If some relation has nontrivial scalar, report an explicit central
phase word; do NOT claim a linear honest representation of PSp.
"""
from __future__ import annotations
import json,math
from collections import deque
import numpy as np
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe91_symplectic_phase_audit import transvection,R
from analysis.w33_20261015_toe91_symplectic_unitary_lift import lift
def comp(p,q): return tuple(p[q[i]] for i in range(40))
def calculate():
 vs=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,1,0,0]]
 perms=[tuple(transvection(v)) for v in vs]
 unit=[]
 for perm in perms:
  u,err,c=lift(perm)
  u*=np.exp(-1j*np.angle(c)/3)
  assert np.max(abs(u@u@u-np.eye(4)))<1e-8
  unit.append(u)
 identity=tuple(range(40))
 # Geometric decomposition into the separate two symplectic planes with 4 generators
 small={identity};q=deque([identity])
 while q:
  p=q.popleft()
  for g in perms[:4]:
   nxt=comp(g,p)
   if nxt not in small:small.add(nxt);q.append(nxt)
 # Now the cross-plane root
 nodes={identity:0};word=[None];parent=[None]
 matrices=[np.eye(4,dtype=complex)]
 queue=deque([identity]);max_phase_resid=0.;nontriv=None;edges=0
 while queue:
  p=queue.popleft()
  ix=nodes[p];curr=matrices[ix]
  for k,g in enumerate(perms):
   nxt=comp(g,p)
   prod=unit[k]@curr
   edges+=1
   if nxt not in nodes:
    nodes[nxt]=len(matrices)
    matrices.append(prod)
    parent.append((ix,k))
    queue.append(nxt)
   else:
    target=matrices[nodes[nxt]]
    alpha=np.trace(target.conj().T@prod)/4
    residual=float(np.max(abs(prod-alpha*target)))
    max_phase_resid=max(max_phase_resid,residual)
    if residual>2e-8:raise AssertionError((k,ix,residual))
    if nontriv is None and abs(alpha-1)>1e-5:
     def get_word(i):
      result=[]
      while parent[i] is not None:
       i,k=parent[i];result.append(int(k))
      return list(reversed(result))
     nontriv={'left_word_generators':get_word(ix),
               'last_generator':int(k),
               'same_projective_permutation_target_word':get_word(nodes[nxt]),
               'scalar_phase_real':round(float(alpha.real),10),
               'scalar_phase_imag':round(float(alpha.imag),10),
               'projective_loop_identity':True}
  if len(nodes)>25920:raise AssertionError('Unexpected group order >25920')
 assert len(nodes)==25920,(len(nodes),len(small))
 assert max_phase_resid<2e-8
 assert nontriv is not None
 # Verify distinct projected group elements give distinct ray actions by construction
 sizes={}
 for k,g in enumerate(perms):
  p=identity
  for order in range(1,20):
   p=comp(g,p)
   if p==identity:break
  sizes[str(k)]=order
  assert order==3
 print('GROUP',len(small),len(nodes),edges,max_phase_resid,flush=True)
 print('CENTRAL RELATION',nontriv,flush=True)
 return {'group':'PSp(4,3) via five explicitly mapped F3 symplectic transvections',
  'four_plane_local_generators_projective_subgroup_order':len(small),
  'full_projective_group_order':len(nodes),
  'generator_vectors_F3':vs,
  'generator_orders_in_projective_permutation_group':sizes,
  'all_Cayley_edges_verified':edges,
  'maximum_projective_unitary_closure_residual':round(max_phase_resid,10),
  'explicit_scalar_projective_cocycle_relation':nontriv,
  'scope':'All 25920 projective ray permutations close with four-mode U(4) unitary lifts, numerically checked over all Cayley edges. Phases constitute a projective representation; no canonical globally linear PSp action, physical gate calibration, or ququart-to-CSS encoding is proven.'}
if __name__=='__main__':
 d=calculate()
 (ROOT/'data/w33_20261015_toe92_full_symplectic_4mode.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
