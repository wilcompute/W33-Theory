#!/usr/bin/env python3
"""Pass9237-9244 outside-box: two Niemeier glues generate a symplectic/F9 structure.

The Golay [12,6,6] glue and the quotient-selected E6-relative [12,6,3]
glue are proved transverse in F3^12.  After dualizing their pairing, their
sum is a hyperbolic polarization.  The associated grading K is itself a
nondegenerate alternating form; the exchange S is orthogonal and
anti-symplectic; R=KS has R^2=-I and preserves K, giving an F9 complex
structure on the six-qutrit symplectic space.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_rank24_root_shadow_core as rs
OUT=ROOT/'data/PART_W33_PASS9237_9244_TRANSVERSE_GLUE_SYMPLECTIC_COMPLEX.json';P=3

def main():
 G=np.array(rs.GOLAY12,dtype=np.int64)%P
 cert=json.loads((ROOT/'data/PART_W33_PASS9185_9196_GOLAY_TETRACODE_GLUE_BIFURCATION.json').read_text())
 E=np.array(cert['N(E6^4)_relative_glue']['generator_rref'],dtype=np.int64)%P
 assert rs.rank_modp(G,P)==rs.rank_modp(E,P)==6
 assert not np.any(G@G.T%P) and not np.any(E@E.T%P)
 assert rs.rank_modp(np.vstack([G,E]),P)==12
 pairing=G@E.T%P;assert rs.rank_modp(pairing,P)==6
 H=rs.inv_mod(pairing,P).T@E%P;assert np.array_equal(G@H.T%P,np.eye(6,dtype=np.int64))
 C=np.vstack([G,H])%P;Ci=rs.inv_mod(C,P)
 I6=np.eye(6,dtype=np.int64);Z=np.zeros((6,6),dtype=np.int64)
 D=np.block([[I6,Z],[Z,-I6]])%P;XCH=np.block([[Z,I6],[I6,Z]])%P
 K=Ci@D@C%P;S=Ci@XCH@C%P;R=K@S%P;I12=np.eye(12,dtype=np.int64)%P
 assert np.array_equal(K.T%P,(-K)%P) and not np.any(np.diag(K)%P) and rs.rank_modp(K,P)==12
 assert np.array_equal(K@K%P,I12)
 assert not np.any(G@K@G.T%P) and not np.any(E@K@E.T%P)
 assert np.array_equal(G@K@H.T%P,I6)
 assert np.array_equal(S@S%P,I12) and np.array_equal(S@S.T%P,I12)
 assert rs.rank_modp(np.vstack([E,G@S%P]),P)==6 and rs.rank_modp(np.vstack([G,E@S%P]),P)==6
 assert np.array_equal(S@K@S.T%P,(-K)%P)
 assert np.array_equal(R@R%P,(-I12)%P) and np.array_equal(np.linalg.matrix_power(R,4)%P,I12)
 assert np.array_equal(R@K@R.T%P,K)
 out={'schema':'w33.pass9237_9244.transverse_glue_symplectic_complex.v1','status':'PASS','passes':'9237-9244',
      'intersection_dimension':0,'sum_dimension':12,'cross_pairing_rank':6,
      'K':{'rank':12,'alternating':True,'K_squared':'I','Golay_and_E6_glues_are_Lagrangian':True},
      'S':{'order':2,'orthogonal_for_standard_dot':True,'swaps_the_two_glue_Lagrangians':True,'anti_symplectic_for_K':True},
      'R_equals_KS':{'order':4,'R_squared':'-I','symplectic_for_K':True,'field_reading':'x^2+1 is irreducible over F3, so R equips F3^12 with an F9-module structure of dimension 6'},
      'theorem':'The two distinct Niemeier glue codes are opposite maximal isotropics of F3^12. Their transverse pairing canonically manufactures a nondegenerate 12D alternating form and an order-4 symplectic complex structure. Thus the E6^4/Golay carrier pair itself generates a six-qutrit phase space together with an F9 structure; this structure is not inserted from the original W33 quotient.',
      'boundary':'The F9 module statement is exact. Identifying the full centralizer of R inside Sp(12,3) with a specific finite unitary group is standard classical-group theory but is not recomputed by enumeration here.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','intersection':0,'K_rank':12,'R_order':4,'F9_dimension':6}))
 return 0
if __name__=='__main__':raise SystemExit(main())
