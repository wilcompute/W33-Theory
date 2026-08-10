#!/usr/bin/env python3
"""Pass 4630 bonkers -- one 45x40 matrix realizes H10 three ways.

For the center-quad/sentinel incidence T, TT^T=0 mod 2, so
F2^45 --T^T--> F2^40 --T--> F2^45 is a complex.  Pass4625 gives ranks 15 and
25, hence middle homology dimension ten.  This pass identifies it exactly with
Cperp/C=H10 and with the 2-torsion detected by the integer Smith form.

If x mod2 lies in ker(T mod2), then Tx is even and beta(x)=[Tx/2] in coker_Z(T)
is 2-torsion.  The reduction modulo two of ker_Z(T) is exactly row_F2(T), so
beta has kernel row(T).  Since Smith(T)=1^15 2^10 0^15, its 2-primary torsion is
(F2)^10; dimension forces beta to be an isomorphism from H10 to that torsion.
The same redundant T used for both X and Z checks gives the existing CSS
[[40,10,4]].
"""
from __future__ import annotations
import math,json
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from exploration.w33_center_quad_gq42_e6_bridge import quotient_points

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4630_T_BOCKSTEIN_H10_CSS.json'

def rank2(M):
    A=np.asarray(M,dtype=np.uint8).copy();m,n=A.shape;r=0
    for c in range(n):
        z=np.flatnonzero(A[r:,c])
        if not len(z):continue
        k=r+int(z[0]);A[[r,k]]=A[[k,r]]
        for i in np.flatnonzero(A[:,c]):
            if i!=r:A[i]^=A[r]
        r+=1
        if r==m:break
    return r

def primitive(v):
    den=1
    for x in v:den=sp.ilcm(den,x.q)
    a=[int(x*den) for x in v];g=0
    for x in a:g=math.gcd(g,abs(x))
    if g:a=[x//g for x in a]
    return a

def main()->int:
    pts=quotient_points();T=np.zeros((45,40),dtype=np.int64)
    for i,p in enumerate(pts):T[i,list(p.support_vertices)]=1
    T2=(T%2).astype(np.uint8);r=rank2(T2);assert r==15 and not np.any((T2@T2.T)%2)
    # Smith torsion.
    D=smith_normal_form(sp.Matrix(T),domain=ZZ);diag=[abs(int(D[i,i])) for i in range(min(D.shape))]
    assert diag.count(1)==15 and diag.count(2)==10 and diag.count(0)==15
    # Integral kernel reduction equals binary row space.
    Zker=sp.Matrix(T).nullspace();assert len(Zker)==15
    KZ2=np.array([[x&1 for x in primitive(v)] for v in Zker],dtype=np.uint8)
    assert rank2(KZ2)==15 and rank2(np.vstack([KZ2,T2]))==15
    # Pass4617 identifies row(T)=sentinel C and ker(T)=context Cperp.
    old=json.loads((ROOT/'data/PART_W33_PASS4617_SENTINEL_MINIMUM_SHELL_TRANSPORT.json').read_text())
    assert old['T_rank_F2']==15 and old['point_line_incidence_rank_F2']==25 and old['TN_zero']
    hdim=25-15;assert hdim==10
    enum=json.loads((ROOT/'data/w33_pass228_sentinel_weight_enumerator.json').read_text())
    assert enum['sentinel_40_15_8']['min_distance']==8
    assert enum['context_40_25_4_via_macwilliams']['min_distance']==4
    # CSS with Hx=Hz=T has k=n-rx-rz=10; a weight-4 context/line word is
    # outside the sentinel row code (whose minimum is 8), proving d=4.
    out={'pass':4630,
      'binary_complex':{'complex':'F2^45 --T^T--> F2^40 --T--> F2^45','TTt_zero':True,'rank_T':15,'kernel_T_dimension':25,'middle_homology_dimension':10,'identification':'ker(T)/im(T^T)=Cperp/C=H10'},
      'integer_lift':{'rank_Z':25,'kernel_Z_rank':15,'reduction_of_kernel_Z_equals_row_T_mod2':True,'smith':'1^15 2^10 0^15','coker_2_primary_torsion':'(Z/2)^10'},
      'bockstein':{'map':'for x mod2 in ker(T), beta(x)=[T x / 2] in Tor_2 coker_Z(T)','kernel':'reduction of ker_Z(T)=row_F2(T)','domain_quotient_dimension':10,'target_dimension':10,'isomorphism':True},
      'CSS':{'checks':'H_X=H_Z=T with redundant 45 rows, rank 15 each','parameters':'[[40,10,4]]','k_reason':'40-15-15=10','distance_reason':'ker(T)=Cperp has weight-4 line words while row(T)=C has minimum weight 8'},
      'theorem':'The same 45x40 incidence realizes the protected H10 simultaneously as binary middle homology, as the logical space of the [[40,10,4]] CSS code, and via the canonical Bockstein as the ten-dimensional 2-torsion defect of the integer incidence lattice.',
      'boundary':'Exact finite integral/binary coding theorem; the Bockstein is attached to this incidence matrix and is not a spacetime or physical anomaly interpretation.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
