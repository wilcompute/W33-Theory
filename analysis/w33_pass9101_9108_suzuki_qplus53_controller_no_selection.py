#!/usr/bin/env python3
"""Pass9101-9108: controller of the Suzuki Q+(5,3) selector and no-unique-selection theorem.

Build on Pass9093-9100.  The canonical M12:2 polarization gives a symmetric
nondegenerate form C on U+=F3^6 and 7,371 nondegenerate 2-spaces A, hence W_A.
Here we enumerate the exact 2.M12 image on U+, intersect it with the isometry
and similitude groups of C, identify those finite groups by element-order
census, and compute their orbits on all 11,011 2-spaces.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9101_9108_SUZUKI_QPLUS53_CONTROLLER_NO_SELECTION.json'
P=3

from scripts.w33_2suz_sp12_embedding import analyze as analyze_2suz
from scripts.w33_2suz_m12_2_subgroup import (
 build_m12_2_generators_from_suz,_standard_symplectic_form,_symplectic_inverse,
 _commutant_basis,_find_involutive_commutant_element,_nullspace_basis_mod_p,
 _basis_matrix,_solve_in_basis,_rank_mod_p)
from analysis.w33_pass9093_9100_suzuki_qplus53_w33_selector import canon,rref_rows,two_spaces_6

def key(M):return (np.asarray(M,dtype=np.int64)%P).astype(np.uint8).tobytes()
def closure(gens):
 I=np.eye(gens[0].shape[0],dtype=np.int64)%P;D={key(I):I};q=deque([I])
 while q:
  A=q.popleft()
  for B in gens:
   C=A@B%P;k=key(C)
   if k not in D:D[k]=C;q.append(C)
 return list(D.values())
def order(M):
 I=np.eye(M.shape[0],dtype=np.int64)%P;X=I.copy()
 for n in range(1,100):
  X=X@M%P
  if np.array_equal(X,I):return n
 raise AssertionError
def type2(space,C):
 B=np.array(space,dtype=np.int64).T%P;G=B.T@C@B%P;r=_rank_mod_p(G,P)
 if r<2:return 'degenerate'
 iso=any(z!=(0,0) and int(np.array(z)@G@np.array(z))%P==0 for z in itertools.product(range(P),repeat=2))
 return 'hyperbolic' if iso else 'anisotropic'

def main():
 rep=analyze_2suz();std=rep['standardized_generators'];a=np.array(std['A_std_mod3'])%P;b=np.array(std['B_std_mod3'])%P
 J=_standard_symplectic_form(6,p=P);g=build_m12_2_generators_from_suz(a,b,p=P);x,y=g['x'],g['y'];xi=_symplectic_inverse(x,J,p=P);yc=xi@y@x%P
 comm=_commutant_basis([y,yc],p=P);s=_find_involutive_commutant_element(comm,p=P);I12=np.eye(12,dtype=np.int64)%P
 U=_basis_matrix(_nullspace_basis_mod_p((s-I12)%P,P),p=P);assert U.shape==(12,6)
 gy=_solve_in_basis(U,y@U%P,p=P);gyc=_solve_in_basis(U,yc@U%P,p=P)
 G=closure([gy,gyc]);assert len(G)==190080
 C=U.T@J@x@U%P;assert _rank_mod_p(C,P)==6 and np.array_equal(C,C.T)
 iso=[h for h in G if np.array_equal(h.T@C@h%P,C)]
 sim=[h for h in G if np.array_equal(h.T@C@h%P,C) or np.array_equal(h.T@C@h%P,2*C%P)]
 assert len(iso)==120 and len(sim)==240
 assert Counter(order(h) for h in iso)==Counter({2:31,10:24,5:24,6:20,3:20,1:1})
 assert Counter(order(h) for h in sim)==Counter({20:48,12:40,4:32,2:31,10:24,5:24,6:20,3:20,1:1})
 # These are exactly the direct-product order censuses C2xA5 and C4xA5.

 S=two_spaces_6();si={z:i for i,z in enumerate(S)}
 def act(z,h):return rref_rows(np.array(z,dtype=np.int64)@h.T%P)
 unseen=set(range(len(S)));orbits=[]
 while unseen:
  i=next(iter(unseen));O={si[act(S[i],h)] for h in sim};unseen-=O
  t=type2(S[i],C);assert all(type2(S[j],C)==t for j in O);orbits.append((len(O),t))
 assert len(orbits)==143
 tc=Counter(t for _,t in orbits);assert tc==Counter({'hyperbolic':62,'degenerate':53,'anisotropic':28})
 assert sum(1 for _,t in orbits if t!='degenerate')==90
 assert sum(n for n,t in orbits if t!='degenerate')==7371

 out={'schema':'w33.pass9101_9108.suzuki_qplus53_controller_no_selection.v1','status':'PASS','passes':'9101-9108',
  '2M12_image_on_Uplus':190080,
  'C_isometry_intersection':{'order':120,'element_order_census':dict(sorted(Counter(order(h) for h in iso).items())),'identification':'C2 x A5','projective_strict_controller':'A5'},
  'C_similitude_intersection':{'order':240,'element_order_census':dict(sorted(Counter(order(h) for h in sim).items())),'identification':'C4 x A5'},
  'two_space_orbits_under_similitudes':{'total_orbits':143,'degenerate_orbits':53,'hyperbolic_orbits':62,'anisotropic_orbits':28,'nondegenerate_candidate_orbits':90},
  'theorem':'The M12:2 polarization-compatible 7,371 W33 candidates are not uniquely selected by the controller preserving that polarization: its exact projective strict controller is A5, and even the full C4xA5 similitude group has 90 orbits on the nondegenerate candidates.',
  'claim_boundary':'Exact finite-module no-selection result. A full 2.Suz orbit statement requires data not preserving this chosen M12:2 polarization.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','isom':120,'sim':240,'candidate_orbits':90}))
if __name__=='__main__':main()
