#!/usr/bin/env python3
"""Pass9213-9220: weld the Niemeier distinguished W33 line to the Suzuki selector.

Every polarization-compatible Suzuki W33 candidate W_A=A+xA already contains
an ordered pair of canonical Lagrangian lines P(A), P(xA).  Therefore marking
one of those lines with the Niemeier line-shadow datum cannot by itself reduce
the 7,371 candidates.  This is checked for every nondegenerate 2-space A.
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'analysis'))
from scripts.w33_2suz_sp12_embedding import analyze as analyze_2suz
from scripts.w33_2suz_m12_2_subgroup import (build_m12_2_generators_from_suz,_standard_symplectic_form,_symplectic_inverse,_commutant_basis,_find_involutive_commutant_element,_nullspace_basis_mod_p,_basis_matrix,_rank_mod_p)
from w33_pass9093_9100_suzuki_qplus53_w33_selector import two_spaces_6
OUT=ROOT/'data/PART_W33_PASS9213_9220_SUZUKI_LINE_WELD_NO_SELECTION.json';P=3

def main():
 rep=analyze_2suz();std=rep['standardized_generators'];a=np.array(std['A_std_mod3'],dtype=np.int64)%P;b=np.array(std['B_std_mod3'],dtype=np.int64)%P
 J=_standard_symplectic_form(6,p=P);g=build_m12_2_generators_from_suz(a,b,p=P);x,y=g['x'],g['y'];xi=_symplectic_inverse(x,J,p=P);yc=xi@y@x%P
 comm=_commutant_basis([y,yc],p=P);s=_find_involutive_commutant_element(comm,p=P);I=np.eye(12,dtype=np.int64)%P
 U=_basis_matrix(_nullspace_basis_mod_p((s-I)%P,P),p=P);assert U.shape==(12,6)
 assert not np.any(U.T@J@U%P);C=U.T@J@x@U%P;assert np.array_equal(C,C.T) and _rank_mod_p(C,P)==6
 total=0;hyper=0;anis=0
 for space in two_spaces_6():
  B=np.array(space,dtype=np.int64).T%P;G=B.T@C@B%P
  if _rank_mod_p(G,P)<2:continue
  iso=any(z!=(0,0) and int(np.array(z,dtype=np.int64)@G@np.array(z,dtype=np.int64))%P==0 for z in itertools.product(range(P),repeat=2))
  hyper+=int(iso);anis+=int(not iso);total+=1
  Lp=U@B%P;Lm=x@U@B%P;W=np.concatenate([Lp,Lm],axis=1)%P
  assert _rank_mod_p(W,P)==4 and _rank_mod_p(W.T@J@W%P,P)==4
  assert not np.any(Lp.T@J@Lp%P) and not np.any(Lm.T@J@Lm%P)
  assert _rank_mod_p(Lp.T@J@Lm%P,P)==2
  assert _rank_mod_p(np.concatenate([Lp,Lm],axis=1),P)==4
 assert (total,hyper,anis)==(7371,5265,2106)
 controller=json.loads((ROOT/'data/PART_W33_PASS9101_9108_SUZUKI_QPLUS53_CONTROLLER_NO_SELECTION.json').read_text())
 assert controller['two_space_orbits_under_similitudes']['nondegenerate_candidate_orbits']==90
 out={'schema':'w33.pass9213_9220.suzuki_line_weld_no_selection.v1','status':'PASS','passes':'9213-9220',
      'candidates':7371,'hyperbolic':5265,'anisotropic':2106,'canonical_lines_per_candidate':2,
      'similitude_candidate_orbits_after_line_marking':90,
      'theorem':'Every one of the 7,371 M12:2-polarization-compatible Suzuki W33 candidates already carries the ordered Lagrangian pair A and xA. Identifying the Niemeier four-point root-shadow line with the first polarization line is therefore structurally natural but nonselecting: it leaves all 7,371 candidates, and the previously computed C4xA5 controller still has 90 nondegenerate candidate orbits.',
      'interpretation':'The line-supported E6^4/A2^12 carriers provide exactly the kind of datum the Suzuki construction already has internally. A unique Suzuki W33 therefore needs extra information beyond a marked line—e.g. glue type, orthogonal sign, or an additional complex structure.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','candidates':total,'line_weld_reduction':0,'controller_orbits':90}))
 return 0
if __name__=='__main__':raise SystemExit(main())
