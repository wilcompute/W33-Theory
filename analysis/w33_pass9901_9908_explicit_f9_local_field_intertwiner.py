#!/usr/bin/env python3
"""Pass9901-9908: explicit F9/local-field intertwiner for the transverse glue phase space.

Pass9237-9244 constructs the actual Golay/E6 glue matrices K and R on F3^12,
and Pass9253-9260 proves that on the Golay Lagrangian G,

    C_-(u,v) = K(u,Rv) = I_6.

This pass upgrades the later local-field observation to an explicit basis.
Let P be the 12x12 matrix whose rows are G followed by G R.  Then

    P K P^T = J0,         P R = J0 P,
    J0 = [[0,I],[-I,0]].

Writing row coordinates as (a,b) in F3^6+F3^6 identifies them with
z=a+b*i in F9^6, i^2=-1.  Right multiplication by J0 is multiplication by i.
The same J0 is exactly the alternating form

    Tr_{F9/F3}(-i sum z_j conjugate(w_j)).

For pi=1-zeta_9, Phi_9(1-pi)=
pi^6-6pi^5+15pi^4-21pi^3+18pi^2-9pi+3, so modulo 3 it is pi^6.  After the
unramified quadratic base change Q3(i), O_L/3 is therefore F9[pi]/(pi^6), whose
six coefficient layers are precisely F9^6 additively.
"""
from __future__ import annotations
import json,sys,itertools
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'analysis'))
import w33_rank24_root_shadow_core as rs
OUT=ROOT/'data/PART_W33_PASS9901_9908_EXPLICIT_F9_LOCAL_FIELD_INTERTWINER.json'
P3=3

def f9_mul(x,y):
    a,b=x;c,d=y
    return ((a*c+2*b*d)%3,(a*d+b*c)%3)
def f9_conj(x):return (x[0]%3,(-x[1])%3)
def f9_trace(x):return (2*x[0])%3

def main():
    # Rebuild the exact glue K,R from the canonical previous certificates.
    G=np.array(rs.GOLAY12,dtype=np.int64)%P3
    cert=json.loads((ROOT/'data/PART_W33_PASS9185_9196_GOLAY_TETRACODE_GLUE_BIFURCATION.json').read_text())
    E=np.array(cert['N(E6^4)_relative_glue']['generator_rref'],dtype=np.int64)%P3
    pairing=G@E.T%P3
    H=rs.inv_mod(pairing,P3).T@E%P3
    C=np.vstack([G,H])%P3;Ci=rs.inv_mod(C,P3)
    I6=np.eye(6,dtype=np.int64);Z=np.zeros((6,6),dtype=np.int64)
    D=np.block([[I6,Z],[Z,-I6]])%P3
    Swap=np.block([[Z,I6],[I6,Z]])%P3
    K=Ci@D@C%P3;S=Ci@Swap@C%P3;R=K@S%P3
    I12=np.eye(12,dtype=np.int64)%P3
    Cminus=G@K@(G@R%P3).T%P3
    assert np.array_equal(Cminus,I6%P3)
    assert np.array_equal(R@R%P3,(-I12)%P3)

    # The actual simultaneous Darboux/F9 basis.
    Basis=np.vstack([G,G@R%P3])%P3
    assert rs.rank_modp(Basis,P3)==12
    J0=np.block([[Z,I6],[-I6,Z]])%P3
    assert np.array_equal(Basis@K@Basis.T%P3,J0)
    assert np.array_equal(Basis@R%P3,J0@Basis%P3)

    # Verify the standard F9 trace-Hermitian alternating form on one coordinate.
    one=(1,0); ii=(0,1); minus_i=(0,2)
    f9_basis=[one,ii]
    B=np.zeros((2,2),dtype=np.int64)
    for r,z in enumerate(f9_basis):
        for c,w in enumerate(f9_basis):
            B[r,c]=f9_trace(f9_mul(minus_i,f9_mul(z,f9_conj(w))))
    assert np.array_equal(B,np.array([[0,1],[2,0]],dtype=np.int64))
    assert f9_mul(ii,ii)==(2,0)
    # In grouped real/imag coordinates the six-coordinate direct sum is J0.

    # Cyclotomic uniformizer polynomial and its mod-3 degeneration.
    coeff=[1,-6,15,-21,18,-9,3]  # pi^6 ... constant
    assert [x%3 for x in coeff]==[1,0,0,0,0,0,0]

    out={
      'schema':'w33.pass9901_9908.explicit_f9_local_field_intertwiner.v1',
      'status':'PASS','passes':'9901-9908',
      'actual_glue_basis':{
        'basis_rows':'P=[G; G R]','rank':12,
        'identities':['P K P^T = J0','P R = J0 P'],
        'J0':'[[0,I6],[-I6,0]]',
        'meaning':'The actual glue (K,R) is explicitly transported to the standard F9^6 trace-Hermitian phase space by the row basis P.'},
      'F9_model':{
        'field':'F3[i]/(i^2+1)','dimension_over_F3':2,'six_coordinate_space':'F9^6 = F3^12',
        'R':'multiplication by i: (a,b)->(-b,a)',
        'K':'Tr_F9/F3(-i sum_j z_j conjugate(w_j))',
        'one_coordinate_K_matrix':[[0,1],[2,0]]},
      'local_field':{
        'L':'Q3(i,zeta_9)','unramified_degree':2,'ramification_index':6,'degree_over_Q3':12,
        'uniformizer':'pi=1-zeta_9',
        'uniformizer_polynomial':'pi^6 - 6 pi^5 + 15 pi^4 - 21 pi^3 + 18 pi^2 - 9 pi + 3',
        'mod_3_relation':'pi^6=0',
        'residue_quotient':'O_L/3 O_L ~= F9[pi]/(pi^6)',
        'associated_graded':'six copies of F9'},
      'theorem':('The transverse Niemeier glue phase space is not merely abstractly F9^6: the explicit basis P=[G;GR] simultaneously sends its actual alternating form and complex structure to the standard trace-Hermitian F9 model. The same six F9 coordinates are the coefficient layers of O_{Q3(i,zeta9)}/3 via pi=1-zeta9.'),
      'boundary':('The finite-module intertwiner is explicit and exact. The local-field quotient statement uses the standard unramified/totally-ramified compositum and the Eisenstein polynomial above. This does not yet identify an integral Niemeier lattice with an O_L lattice before reduction mod 3.')
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','basis_rank':12,'PKPt':'J0','PR':'J0P','graded_F9_layers':6}))
    return 0
if __name__=='__main__':raise SystemExit(main())
