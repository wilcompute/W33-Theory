#!/usr/bin/env python3
"""Pass10145-10152: exact Ihara zeta and Ramanujan status of Heawood tensor K6.

This retains the mathematically good part of the parallel proposal while removing
the unsupported quantum-code-distance conclusion.

Heawood H: 14 vertices, 3-regular, spectrum
    +3^1, -3^1, (+sqrt(2))^6, (-sqrt(2))^6.
K6: 6 vertices, 5-regular, spectrum 5^1, (-1)^5.
For the categorical/tensor product G=H x K6, adjacency is A_H tensor A_K6,
so G has 84 vertices, degree 15 and the product spectrum.  H is bipartite and
K6 is non-bipartite, hence G is connected and bipartite.

The nontrivial largest absolute eigenvalue is 5 sqrt(2), below the 15-regular
Ramanujan bound 2 sqrt(14).  Therefore G is Ramanujan.

Bass's regular-graph determinant formula gives
  Z_G(u)^-1=(1-u^2)^(m-n) prod_lambda (1-lambda*u+14*u^2),
with n=84,m=630,m-n=546. Pairing +/- eigenvalues yields an exact factorization
with integer quartics.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10145_10152_IHARA_HEAWOOD_TENSOR_K6.json'

def main():
    nH,dH=14,3;nK,dK=6,5
    n=nH*nK;d=dH*dK;m=n*d//2;q=d-1
    assert (n,d,m,m-n,q)==(84,15,630,546,14)
    # Exact spectrum encoded by lambda^2 and signed multiplicity pairs.
    spectrum={'15':1,'-15':1,'5sqrt2':6,'-5sqrt2':6,'3':5,'-3':5,'sqrt2':30,'-sqrt2':30}
    assert sum(spectrum.values())==84
    nontrivial_sq=max(50,9,2)
    assert nontrivial_sq < 4*q # 50 < 56
    # Paired Bass factors: (1+q u^2)^2-lambda^2 u^2.
    paired={
      'lambda2_225':{'power':1,'factor':[1,0,-197,0,196]},
      'lambda2_9':{'power':5,'factor':[1,0,19,0,196]},
      'lambda2_50':{'power':6,'factor':[1,0,-22,0,196]},
      'lambda2_2':{'power':30,'factor':[1,0,26,0,196]},
    }
    for key,v in paired.items():
        lam2=int(key.split('_')[-1]);c=v['factor']
        assert c==[1,0,2*q-lam2,0,q*q]
    out={
      'schema':'w33.pass10145_10152.ihara_heawood_tensor_k6.v1','status':'PASS','passes':'10145-10152',
      'graph':{'construction':'categorical/tensor product Heawood x K6','vertices':84,'degree':15,'edges':630,'connected':True,'bipartite':True},
      'spectrum':spectrum,
      'Ramanujan':{'q=d-1':14,'bound':'2*sqrt(14)','bound_squared':56,'largest_nontrivial_abs':'5*sqrt(2)','largest_nontrivial_squared':50,'is_Ramanujan':True},
      'Ihara_inverse':{
        'Bass_exponent_m_minus_n':546,
        'factorization':'(1-u^2)^546 (1-197u^2+196u^4) (1+19u^2+196u^4)^5 (1-22u^2+196u^4)^6 (1+26u^2+196u^4)^30',
        'paired_factors':paired},
      'Ihara_RH':'For a finite connected (q+1)-regular graph, the nontrivial Ihara-RH condition is equivalent to the Ramanujan adjacency bound; it holds here because 50<56.',
      'theorem':'Heawood tensor K6 is an 84-vertex connected bipartite 15-regular Ramanujan graph. Its Ihara zeta inverse has the displayed exact Bass factorization, and its nontrivial poles satisfy the regular-graph Ihara Riemann-hypothesis circle condition.',
      'removed_parallel_claim':'This graph-theoretic Ramanujan/Ihara result does NOT by itself certify an optimal W33 quantum-code distance. Expander eigenvalues alone are insufficient for that coding-theoretic conclusion.',
      'boundary':'All graph spectrum and Bass factors are exact. No identification with a physical Holonet coupling graph or a specific CSS/check complex is asserted.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','n':84,'d':15,'Ramanujan':True,'Ihara_Bass_exponent':546}))
    return 0
if __name__=='__main__':raise SystemExit(main())
