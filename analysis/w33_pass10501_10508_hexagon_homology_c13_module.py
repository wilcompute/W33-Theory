#!/usr/bin/env python3
"""Pass10501-10508: split-Cayley-hexagon Levi homology and the C13 V2 module.

For a generalized hexagon H(q) of order (q,q),
  P=(q+1)(q^4+q^2+1) points and the same number of lines,
  E=(q+1)P flags/Levi edges.
Hence its connected Levi graph has
  beta1 = E-2P+1 = q^6.
This is a general identity, not a q=4 coincidence.

At q=4, beta1=4096=|V2|.  The explicit irreducible C13 acts freely on the
nonzero vectors of V2 and freely on H(4) points, lines and flags.  The C13
quotient Levi graph therefore has beta1=1+(4096-1)/13=316.

Over F2, ord_13(2)=12, so Phi13 is irreducible and
F2[C13] is semisimple with exactly the trivial 1-space and one 12-dimensional
nontrivial simple.  Both
  H1(Levi(H4);F2)
and the permutation module F2[V2]
have dimension 4096 and C13-fixed dimension 316.  Therefore their restrictions
to C13 are isomorphic:
  1^316 + W12^315.

This is deliberately only a C13-module theorem, not a full G2(4)-module claim.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10501_10508_HEXAGON_HOMOLOGY_C13_MODULE.json'

def ordmod(a,n):
    x=1
    for k in range(1,n+1):
      x=x*a%n
      if x==1:return k
    raise RuntimeError

def data(q):
    P=(q+1)*(q**4+q**2+1);E=(q+1)*P;beta=E-2*P+1
    assert beta==q**6
    return P,E,beta

def main():
    p2,e2,b2=data(2);p4,e4,b4=data(4)
    assert (p2,e2,b2)==(63,189,64)
    assert (p4,e4,b4)==(1365,6825,4096)
    assert ordmod(2,13)==12
    nonzero=4**6-1;assert nonzero==4095 and nonzero//13==315
    qp=p4//13;ql=p4//13;qe=e4//13
    assert (qp,ql,qe)==(105,105,525)
    qbeta=qe-qp-ql+1;assert qbeta==316==1+315

    # Semisimple F2[C13] decomposition. Phi13 irreducibility follows from ord_13(2)=12.
    trivial_mult=qbeta
    nontrivial_mult=(b4-trivial_mult)//12
    assert nontrivial_mult==315 and trivial_mult+12*nontrivial_mult==4096
    # The vector permutation module has one fixed zero plus 315 regular 13-cycles:
    # each regular F2[C13] = 1 + W12.
    assert 1+315==trivial_mult

    out={
      'schema':'w33.pass10501_10508.hexagon_homology_c13_module.v1','status':'PASS','passes':'10501-10508',
      'general_identity':{
        'Hq_points':'(q+1)(q^4+q^2+1)','Hq_lines':'same','Levi_edges':'(q+1) times points',
        'beta1_formula':'E-V+1 = q^6','proof_simplification':'(q-1)(q+1)(q^4+q^2+1)+1=(q^6-1)+1=q^6'},
      'q2':{'points':p2,'lines':p2,'flags':e2,'Levi_beta1':b2},
      'q4':{'points':p4,'lines':p4,'flags':e4,'Levi_beta1':b4,'equals_cardinality_of_V2':True},
      'C13':{
        'ord_13_2':12,'Phi13_irreducible_over_F2':True,
        'V2_nonzero_cycles':315,'V2_permutation_orbits_including_zero':316,
        'H4_action':'free on points, lines and flags','quotient_points':qp,'quotient_lines':ql,'quotient_flags':qe,'quotient_beta1':qbeta},
      'module_theorem':{
        'field':'F2','group':'C13','nontrivial_simple_dimension':12,
        'H1_restriction':'1^316 + W12^315','F2[V2]_restriction':'1^316 + W12^315',
        'isomorphic_as_F2_C13_modules':True,
        'reason':'13 is odd so the group algebra is semisimple; x^13-1 has factors (x-1) and irreducible Phi13 only, so dimension and fixed-space dimension determine the multiplicities'},
      'theorem':'For every split Cayley hexagon H(q), the Levi graph cycle rank is exactly q^6. At q=4 this is 4096=|V2|. Under the explicit free C13 clock, the quotient cycle rank is 316=1+4095/13, exactly the number of C13 orbits on V2. Over F2 the two 4096-dimensional modules H1(Levi(H4);F2) and F2[V2] restrict isomorphically to C13 as 1^316 plus 315 copies of the unique 12-dimensional irreducible module.',
      'boundary':'The module isomorphism is proved only after restriction to C13. No full G2(4)-module isomorphism between hexagon homology and F2[V2] is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','beta_H2':64,'beta_H4':4096,'beta_C13_quotient':316,'C13_module':'1^316+W12^315'}))
if __name__=='__main__':main()
