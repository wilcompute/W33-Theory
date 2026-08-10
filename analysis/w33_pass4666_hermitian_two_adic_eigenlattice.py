#!/usr/bin/env python3
"""Pass 4666 -- the Hermitian binary-rank conjecture as a 2-adic eigenlattice equality.

For Q^-(5,q)=GQ(q,q^2), let N be the integral point-line incidence matrix,
L=im_Z(N), and K=ker_Z(N^T).  Since K is the kernel of a homomorphism between
free abelian groups it is primitive.  Over Q, L_Q=K_Q^perp.  Therefore the
saturation of L is exactly K^perp_Z.  The all-odd-q binary rank theorem is
precisely L tensor Z_2 = K^perp tensor Z_2.

Moreover K is intrinsic to the point graph: NN^T=(q^2+1)I+A and, over Z,
ker(N^T)=ker(NN^T), so K is the integral -(q^2+1)-eigenlattice of A.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4666_HERMITIAN_TWO_ADIC_EIGENLATTICE.json'

def vals(q:int):
    v=(q+1)*(q**3+1)
    k=q*(q*q+1)
    mneg=q*(q*q-q+1)
    r=q**4+q*q+1
    lam0=(q+1)*(q*q+1)
    lam1=q*(q+1)
    def v2(n):
        c=0
        while n%2==0:c+=1;n//=2
        return c
    return {'q':q,'points':v,'point_degree':k,'negative_eigenspace_dim':mneg,'rank_Q':r,
            'Gram_nonzero_eigenvalues':[lam0,lam1], 'v2_q2_plus_1':v2(q*q+1),
            'v2_lambda_constant':v2(lam0),'v2_lambda_positive':v2(lam1)}

def main():
    old=json.loads((ROOT/'data/PART_W33_PASS4627_HERMITIAN_RANK_TWO_SATURATION_FRONTIER.json').read_text())
    assert old['rational_theorem']['rank_Q']=='q^4+q^2+1'
    rows=[vals(q) for q in (3,5,7)]
    assert all(r['v2_q2_plus_1']==1 for r in rows)
    assert [r['rank_Q'] for r in rows]==[91,651,2451]
    out={
      'pass':4666,
      'geometry':'Q^-(5,q)=GQ(q,q^2), dual to H(3,q^2)',
      'integral_lattices':{
        'L':'im_Z(N) in Z^v',
        'K':'ker_Z(N^T)',
        'K_is_primitive':True,
        'saturation_of_L':'L_sat=(L tensor Q) intersect Z^v = K^perp_Z',
        'saturation_quotient':'S=K^perp_Z/L, finite; its 2-primary part is exactly the binary rank defect'},
      'graph_intrinsic_kernel':{
        'identity':'N N^T=(q^2+1)I+A_point',
        'integer_kernel_equality':'ker_Z(N^T)=ker_Z(NN^T)',
        'eigenlattice':'K is the integral -(q^2+1)-eigenlattice of A_point',
        'reason_for_kernel_equality':'x^T NN^T x=||N^T x||^2'},
      'two_adic_target':{
        'equivalent_statement':'L tensor Z_2 = K^perp_Z tensor Z_2',
        'equivalent_quotient_statement':'S has trivial 2-primary part',
        'equivalent_Smith_statement':'every nonzero Smith factor of N is odd',
        'equivalent_rank_statement':'rank_F2(N)=q^4+q^2+1'},
      'nonzero_Gram_eigenvalues':{
        'constant':'(q+1)(q^2+1)','positive_constituent':'q(q+1)',
        'odd_q_fact':'v2(q^2+1)=1 for every odd q because q^2=1 mod 8',
        'warning':'The Gram eigenvalues are even for odd q, so Gram nilpotence/eigenvalue valuation alone cannot prove 2-saturation; the integral placement of L inside K^perp is the missing datum.'},
      'exact_anchors':rows,
      'new_reduction':'An all-q proof may be carried out entirely on the point graph plus its integral negative eigenlattice: prove that line-incidence columns generate the full 2-adic annihilator of K.',
      'status':'OPEN: no proof yet that L_(2)=K^perp_(2) for every odd q.',
      'theorem':'The Hermitian/Q-minus binary-rank conjecture is exactly a 2-adic eigenlattice saturation theorem. The rational image is the annihilator of the integral negative eigenspace; the only missing step is equality of the incidence lattice with that annihilator after localization at 2.',
      'boundary':'Exact integral reformulation and q=3,5,7 anchors; the all-q 2-saturation equality remains unproved.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
