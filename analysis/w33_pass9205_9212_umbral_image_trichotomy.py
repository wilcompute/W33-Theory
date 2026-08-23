#!/usr/bin/env python3
"""Pass9205-9212: umbral-image trichotomy for the three rank-24 W33 carriers.

Classical Niemeier automorphism quotients are used only as ambient groups.  The
actual carrier elements are the explicit ones already verified in Passes
8965-9012/9173-9196, so their images modulo the root Weyl group are read off
from their construction and checked against the explicit Golay monomial witness.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_rank24_root_shadow_core as rs
OUT=ROOT/'data/PART_W33_PASS9205_9212_UMBRAL_IMAGE_TRICHOTOMY.json'

def cycle_type(perm):
 seen=set();lens=[]
 for i in range(len(perm)):
  if i in seen:continue
  j=i;n=0
  while j not in seen:seen.add(j);n+=1;j=perm[j]
  lens.append(n)
 return sorted(lens)

def main():
 # E8^3: local order-3 E8 Coxeter component lies in W(E8); factor 3-cycle survives.
 e8_image={'ambient_umbral_quotient':'S3','image_order':3,'image_type':'3-cycle of the three E8 factors'}
 # E6^4: the order-9 carrier is diagonal in W(E6)^4, so its entire umbral image is trivial.
 e6_image={'ambient_umbral_quotient':'2.S4 (order 48; isomorphic to GL(2,3))','image_order':1,'image_type':'identity','reason':'carrier lies in W(E6)^4'}
 # A2^12: local Coxeter twists are Weyl; signed Golay monomial part survives.
 perm=rs.PERM;signs=rs.SIGNS_MOD3
 assert cycle_type(perm)==[3,3,3,3]
 t=np.zeros((12,12),dtype=np.int64)
 for src,dst in enumerate(perm):t[dst,src]=signs[src]%3
 assert np.array_equal(np.linalg.matrix_power(t,3)%3,np.eye(12,dtype=np.int64))
 words=rs.golay_codewords();assert all(tuple((t@np.array(w,dtype=np.int64))%3) in words for w in words)
 a2_image={'ambient_umbral_quotient':'2.M12','image_order':3,'permutation_projection_cycle_shape':'3^4','M12_class':'3B','image_type':'order-3 signed monomial lift over M12 class 3B'}
 out={'schema':'w33.pass9205_9212.umbral_image_trichotomy.v1','status':'PASS','passes':'9205-9212',
      'E8^3':e8_image,'E6^4':e6_image,'A2^12':a2_image,
      'root_shadow_types':{'E8^3':'all 40 W33 points','E6^4':'one W33 line plus A2^12 root kernel','A2^12':'one W33 line'},
      'theorem':'The same rank-24 W(3,3) quotient is carried by three sharply different Niemeier automorphism-quotient classes: an S3 3-cycle for E8^3, the identity for the diagonal E6^4 carrier, and an order-3 2.M12 element projecting to M12 class 3B (cycle shape 3^4) for A2^12. Thus the W33 quotient does not determine the umbral image, and root-shadow type plus umbral image gives a strictly finer carrier invariant.',
      'classical_boundary':'The ambient Niemeier quotient groups are classical input. The carrier images follow from the explicit repository constructions. The M12 name 3B uses the ATLAS convention in which cycle shape 3^4 is class 3B.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','images':['S3:3-cycle','identity','2.M12:3B-lift']}))
 return 0
if __name__=='__main__':raise SystemExit(main())
