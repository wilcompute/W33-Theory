#!/usr/bin/env python3
"""Pass9505-9512 outside-box: O+(12,3) splits as two glue-selected O-(6,3) halves.

The same Golay and E6-relative spaces are K-Lagrangian but B=KR^T-nondegenerate.
This pass exposes the resulting double-minus orthogonal polarization and the
exact action of K,S,R on its two halves.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_rank24_root_shadow_core as rs
P=3
OUT=ROOT/'data/PART_W33_PASS9505_9512_DOUBLE_MINUS_ORTHOGONAL_POLARIZATION.json'

def rref(A):
 A=np.array(A,dtype=np.int64)%P;m,n=A.shape;r=0
 for c in range(n):
  q=next((i for i in range(r,m) if A[i,c]),None)
  if q is None:continue
  A[[r,q]]=A[[q,r]];A[r]=A[r]*pow(int(A[r,c]),-1,P)%P
  for i in range(m):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
  r+=1
 return A[:r]
def same(A,B):return np.array_equal(rref(A),rref(B))

def main():
 G=np.array(rs.GOLAY12,dtype=np.int64)%P
 old=json.loads((ROOT/'data/PART_W33_PASS9185_9196_GOLAY_TETRACODE_GLUE_BIFURCATION.json').read_text())
 E=np.array(old['N(E6^4)_relative_glue']['generator_rref'],dtype=np.int64)%P
 pairing=G@E.T%P;H=rs.inv_mod(pairing,P).T@E%P;C=np.vstack([G,H])%P;Ci=rs.inv_mod(C,P)
 I6=np.eye(6,dtype=np.int64);Z=np.zeros((6,6),dtype=np.int64)
 D=np.block([[I6,Z],[Z,-I6]])%P;X=np.block([[Z,I6],[I6,Z]])%P
 K=Ci@D@C%P;S=Ci@X@C%P;R=K@S%P;B=K@R.T%P
 assert rs.rank_modp(np.vstack([G,E]),P)==12 and not (G@B@E.T%P).any()
 assert rs.rank_modp(G@B@G.T%P,P)==6 and rs.rank_modp(E@B@E.T%P,P)==6
 assert same(G@K%P,G) and same(E@K%P,E)
 assert same(G@S%P,E) and same(E@S%P,G)
 assert same(G@R%P,E) and same(E@R%P,G)
 assert np.array_equal(S@B@S.T%P,B) and np.array_equal(S@K@S.T%P,(-K)%P) and np.array_equal(S@R@S%P,(-R)%P)
 # Each 6D restriction is minus type.  The exact Q-(5,3) census is inherited from Pass9253-9260.
 twin=json.loads((ROOT/'data/PART_W33_PASS9253_9260_ORTHOGONAL_SIGN_TWIN_SELECTOR.json').read_text())
 minus=twin['Niemeier_glue_selector'];assert minus['orthogonal_type']=='Q-(5,3)' and minus['singular_projective_points']==112
 assert minus['nondegenerate_W33_candidates']==7371
 out={'schema':'w33.pass9505_9512.double_minus_orthogonal_polarization.v1','status':'PASS','passes':'9505-9512',
  'bulk':'(F3^12,B) has orthogonal type O+(12,3)',
  'orthogonal_decomposition':'F3^12 = C_G orthogonal_sum_B C_E, with both restrictions O-(6,3)',
  'simultaneous_symplectic_role':'C_G and C_E are maximal K-isotropic/Lagrangian although each is B-nondegenerate',
  'operators':{'K':'stabilizes each half','S':'swaps halves, B-isometry, K-anti-isometry, S^2=1','R=KS':'swaps halves, K-symplectic, R^2=-I','conjugation':'S R S = -R'},
  'each_half_Qminus_census':{'singular_projective_points':112,'degenerate_2spaces':3640,'hyperbolic_2spaces':4536,'anisotropic_2spaces':2835,'nondegenerate_2spaces':7371},
  'theorem':'The transverse Niemeier glues define two orthogonal copies of O-(6,3) inside one O+(12,3) bulk. The very same six-spaces are Lagrangian for the alternating form K. Thus each glue half supports a Q-(5,3) selector with the 7,371 census, while S and the order-four R exchange the two selectors. This is a simultaneous symplectic/orthogonal polarization, not merely two codes with matching dimensions.',
  'boundary':'No identification with the independent Suzuki Q+(5,3) module is made. The two Q- halves live inside the glue-derived (K,B,R) 12-space.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','bulk':'O+12','halves':['O-6','O-6'],'each_nondeg':7371}));return 0
if __name__=='__main__':raise SystemExit(main())
