#!/usr/bin/env python3
"""Pass10025-10032 outside-box: the glue F9 and E8/3E8 unitary branch are one functor.

Let (V,K) be symplectic over F3 and let R be symplectic with R^2=-I.  In the
row-vector convention used by the glue scripts, define

  B = K R^T,
  h = B - i K,   i^2=-1 in F9, conjugation(i)=-i.

Then B is symmetric nondegenerate and h is Hermitian when R is interpreted as
multiplication by i:

  h(xR,y)= i h(x,y),
  h(x,yR)=-i h(x,y)=conj(i) h(x,y),
  h(y,x)=conj(h(x,y)).

This is exactly the unitary/Hermitian mechanism used independently by the new
parallel E8/3E8 H(3,9) branch, up to the harmless choice i <-> -i.  The E8
example has F9-dimension 4; the transverse Niemeier glue has F9-dimension 6.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_rank24_root_shadow_core as rs
OUT=ROOT/'data/PART_W33_PASS10025_10032_UNIVERSAL_F9_HERMITIANIZATION.json'
P=3

def main():
    G=np.array(rs.GOLAY12,dtype=np.int64)%P
    cert=json.loads((ROOT/'data/PART_W33_PASS9185_9196_GOLAY_TETRACODE_GLUE_BIFURCATION.json').read_text())
    E=np.array(cert['N(E6^4)_relative_glue']['generator_rref'],dtype=np.int64)%P
    pairing=G@E.T%P
    Hdual=rs.inv_mod(pairing,P).T@E%P
    C=np.vstack([G,Hdual])%P;Ci=rs.inv_mod(C,P)
    I6=np.eye(6,dtype=np.int64);Z=np.zeros((6,6),dtype=np.int64)
    D=np.block([[I6,Z],[Z,-I6]])%P
    Swap=np.block([[Z,I6],[I6,Z]])%P
    K=Ci@D@C%P;S=Ci@Swap@C%P;R=K@S%P
    I12=np.eye(12,dtype=np.int64)%P
    assert np.array_equal(R@R%P,(-I12)%P)
    assert np.array_equal(R@K@R.T%P,K)
    assert np.array_equal(K.T%P,(-K)%P) and rs.rank_modp(K,P)==12
    B=K@R.T%P
    assert np.array_equal(B.T%P,B) and rs.rank_modp(B,P)==12

    # Matrix identities encoding h sesquilinearity in the row-vector convention.
    # h = (real part B, i-coefficient -K).
    # First slot x->xR: (R B, -R K) must equal i*(B,-K)=(K,B) in pair notation.
    assert np.array_equal(R@B%P,K)
    assert np.array_equal((-R@K)%P,B)
    # Second slot y->yR: (B R^T, -K R^T) = (-K,-B) = -i*(B,-K).
    assert np.array_equal(B@R.T%P,(-K)%P)
    assert np.array_equal((-K@R.T)%P,(-B)%P)

    out={
      'schema':'w33.pass10025_10032.universal_f9_hermitianization.v1','status':'PASS','passes':'10025-10032','outside_box':True,
      'construction':{'input':'nondegenerate alternating K over F3 plus symplectic R with R^2=-I','symmetric_form':'B=K R^T','Hermitian_form':'h=B-iK over F9','F9_scalar':'i acts as R'},
      'verified_actual_glue':{'F3_dimension':12,'F9_dimension':6,'rank_K':12,'rank_B':12,'B_symmetric':True,'R_squared':'-I','R_symplectic':True},
      'exact_identities':['R B = K','-R K = B','B R^T = -K','-K R^T = -B'],
      'Hermitian_laws':['h(xR,y)=i h(x,y)','h(x,yR)=conj(i) h(x,y)=-i h(x,y)','h(y,x)=conj(h(x,y))'],
      'parallel_unitary_branch':{'E8_mod_3':'H(3,9) on an F9^4 Hermitian space','glue':'F9^6 Hermitian space','relation':'same symplectic-complex-to-Hermitian mechanism, with rank 4 versus rank 6 and possibly i <-> -i convention'},
      'theorem':'A symplectic F3 space equipped with a symplectic complex structure R^2=-I canonically Hermitianizes to F9 via h=K R^T-iK. The actual transverse Niemeier glue realizes this in dimension 6, while the parallel E8/3E8 H(3,9) construction is the dimension-4 instance of the same algebraic mechanism.',
      'boundary':'The Hermitianization identities are exact. This identifies a common algebraic functor; it does not identify the rank-4 E8 and rank-6 glue geometries as the same polar space or lattice.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','F9_dimensions':[4,6],'actual_glue_rank':12}))
    return 0
if __name__=='__main__':raise SystemExit(main())
