#!/usr/bin/env python3
"""Pass5299 (bonkers): all-odd local same-point fibers and their relation module.

Let X be the W(3,q) Levi graph, q odd, with v=(q+1)(q^2+1) point vertices and
v line vertices.  Chamber stars are indexed by Levi edges.  Pass5110 proves the
complete chamber-star dependency kernel is the binary cut space of X.

At each W-point p, take even combinations of its q+1 incident chamber stars and
mod out the all-(q+1) point cut.  This local quotient has dimension q-1.  Over
all v points the direct sum of local fibers therefore has dimension
v(q-1)=q^4-1.

A cut is represented by point labels a and line labels b, with edge coefficient
a_p+b_l.  Because q+1 is even, the point-even condition reduces to N b=0,
where N is W point-line incidence.  Pass5130 gives nullity_2(N)=
g=q(q^2+1)/2 for odd q.  After quotienting the global constant (1,1), the
relations among the local fibers are canonically ker(N)/<1>, of dimension g-1.
Hence the image D_q of all same-point chamber-star differences has

    dim D_q=(q^4-1)-(g-1)=q^4-g.

Pass5201 puts D_q in the zero-P residual K0.  Since dim K0=q^4-rank_2(F), the
all-odd footprint-rank equality rank_2(F)=g is equivalent to D_q=K0.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5299_ALLODD_LOCAL_FIBER_RELATION_THEOREM.json'

def row(q):
    v=(q+1)*(q*q+1);g=q*(q*q+1)//2
    local_total=v*(q-1);relations=g-1;image=local_total-relations
    assert local_total==q**4-1 and image==q**4-g
    return {'q':q,'base_points':v,'local_fiber_dimension':q-1,'direct_sum_dimension':local_total,
      'incidence_nullity_g':g,'relation_dimension':relations,'same_point_difference_dimension':image}

def main():
    A={str(q):row(q) for q in (3,5,7,9,11)}
    assert A['5']['direct_sum_dimension']==624 and A['5']['relation_dimension']==64 and A['5']['same_point_difference_dimension']==560
    out={'pass':5299,'status':'THEOREM_ALLODD_LOCAL_FIBER_RELATIONS_ARE_LEVI_INCIDENCE_KERNEL_MOD_CONSTANT',
      'domain':'odd prime powers q',
      'local_fiber':'At each W-point: even subspace of F2^(q+1) modulo the all-ones point cut, dimension q-1.',
      'relation_module':'ker_2(N)/<1>, where N is W point-line incidence; dimension g-1 with g=q(q^2+1)/2.',
      'same_point_difference_code':'D_q has dimension q^4-g and lies in the zero-P residual K0.',
      'rank_equivalence':'rank_2(F)=g iff D_q=K0.',
      'q5_specialization':'156 copies of the 4D PG(3,2) fiber give 624 local dimensions; 64 global relations leave the 560-dimensional K0.',
      'q5_relation_64_note':'The dimension 64 matches the q5 footprint hull dimension from Pass5209, but no canonical identification of those two 64-dimensional modules is claimed here.',
      'anchors':A,
      'boundary':'This theorem reduces all-odd footprint-rank equality to generation K0=D_q; it does not prove that final equality for every odd q.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
