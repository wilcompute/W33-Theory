#!/usr/bin/env python3
"""Pass5384: all-odd apartment/footprint gauge exact sequence.

Parallel Pass5376 proves for every odd prime power q that im_2(F)=C_W^perp,
rank_2(F)=g=q(q^2+1)/2, ker_2(F^T)=C_W, and therefore the apartment-code
zero-footprint kernel K0 equals the already-defined gauge/dependency sector D_q.

The apartment code C_A has dimension q^4 (Pass5066/Levi quotient theorem), while
its P-component parity image is exactly C_F=im(F^T), dimension g.  Hence

  0 -> D_q=K0 -> C_A -> C_F -> 0

is exact for all odd q, with

  dim D_q = q^4-g
          = q(q-1)(2q^2+q+1)/2.

The parallel all-odd theorem also gives
  C_F=[(q+1)(q^2+1), q(q^2+1)/2, 2(q+1)]_2.

This isolates the remaining all-odd apartment-distance problem: the footprint
quotient is completely known; any failure of d(C_A)=q^4 must now be explained by
how a nonzero footprint coset or the kernel D_q realizes small apartment Hamming
weight.  At q=5 Pass5262/5380 settle both sides, but no all-q q^4 claim is made.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5384_ALLODD_APARTMENT_FOOTPRINT_GAUGE_SEQUENCE.json'

def row(q):
    g=q*(q*q+1)//2; k0=q**4-g; closed=q*(q-1)*(2*q*q+q+1)//2
    assert k0==closed
    return {'q':q,'apartment_dimension':q**4,'footprint_dimension':g,
            'gauge_kernel_dimension':k0,'footprint_length':(q+1)*(q*q+1),
            'footprint_distance':2*(q+1)}

def main():
    rows={str(q):row(q) for q in (3,5,7,9,11,13,17,19,25,27)}
    assert rows['5']['gauge_kernel_dimension']==560
    out={'pass':5384,'status':'THEOREM_ALLODD_APARTMENT_FOOTPRINT_GAUGE_EXACT_SEQUENCE',
      'domain':'all odd prime powers q',
      'exact_sequence':'0 -> D_q=K0 -> C_A -> C_F -> 0',
      'dimensions':{'dim_C_A':'q^4','dim_C_F':'q(q^2+1)/2',
                    'dim_Dq':'q(q-1)(2q^2+q+1)/2'},
      'footprint_code':'[(q+1)(q^2+1), q(q^2+1)/2, 2(q+1)]_2',
      'kernel_identity':'K0=D_q for every odd q, by the parallel Pass5376 all-odd footprint-rank theorem.',
      'distance_frontier':'The quotient code C_F and its minimum dual-grid shell are completely known. The remaining all-odd apartment-distance q^4 problem is not a footprint-rank problem anymore; it is a Hamming-weight problem inside D_q and its nonzero footprint cosets.',
      'q5_specialization':'At q=5, Pass5262 and Pass5380 give C_A=[73125,625,625]_2 and D_5=K0=[73125,560,1000]_2.',
      'samples':rows,
      'boundary':'No all-odd minimum-distance formula for C_A or D_q is asserted beyond already proved anchors.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
