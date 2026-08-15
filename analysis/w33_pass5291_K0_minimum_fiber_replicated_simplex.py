#!/usr/bin/env python3
"""Pass5291 (outside-box): every q=5 K0 minimum fiber is a replicated simplex code.

Pass5290 gives, on each P block of a fixed W-point footprint, a 4-dimensional
binary local fiber code of length 225 in which all 15 nonzero words have weight
40. A Fourier/Walsh inversion determines its generator-column multiplicities
uniquely.

Let n_a be the number of generator columns of type a in F2^4. For every nonzero
message u, wt(uG)=40, so the Walsh transform is constant away from u=0. Inverting
gives
  n_0=150,
  n_a=5 for every nonzero a in F2^4.
Thus after deleting 150 zero columns the local code is exactly a 5-fold column
replication of the binary simplex [15,4,8] code: [75,4,40].

Across the 25 diagonal controller-sheet blocks, every nonzero column type occurs
125 times and 3750 columns are zero. After deleting zero columns the fixed-point
K0 minimum fiber is the 125-fold replicated simplex [1875,4,1000]. Consequently
its 15 nonzero words are pairwise Hamming distance 1000 and intersect in exactly
500 effective support coordinates.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5291_K0_MINIMUM_FIBER_REPLICATED_SIMPLEX.json'

def multiplicities(length,weight):
    # For a k=4 linear code with all 15 nonzero words of common weight w,
    # Walsh inversion gives n0=(N+15(N-2w))/16 and n_a=(N-(N-2w))/16=w/8.
    S=length-2*weight
    n0=(length+15*S)//16
    n=(length-S)//16
    assert n0+15*n==length and 8*n==weight
    return n0,n

def main():
    zloc,nloc=multiplicities(225,40)
    assert (zloc,nloc)==(150,5)
    zglob,nglob=multiplicities(5625,1000)
    assert (zglob,nglob)==(3750,125)
    effective=15*nglob
    assert effective==1875 and 8*nglob==1000
    # Any two distinct nonzero words differ by another nonzero word.
    pair_distance=1000
    pair_intersection=(1000+1000-pair_distance)//2
    assert pair_intersection==500
    out={
      'pass':5291,
      'status':'THEOREM_Q5_K0_MINIMUM_FIBER_IS_REPLICATED_SIMPLEX',
      'local_zero_columns':zloc,
      'local_multiplicity_each_nonzero_F2_4_column':nloc,
      'local_effective_code':'[75,4,40]_2 = 5-fold replication of binary simplex [15,4,8]',
      'local_zero_extended_code':'[225,4,40]_2 with 150 identically-zero fiber coordinates',
      'controller_blocks':25,
      'global_zero_columns_in_25block_region':zglob,
      'global_multiplicity_each_nonzero_F2_4_column':nglob,
      'global_effective_code':'[1875,4,1000]_2 = 125-fold replication of binary simplex [15,4,8]',
      'global_zero_extended_code':'[5625,4,1000]_2 with 3750 identically-zero fiber coordinates',
      'nonzero_words':15,
      'pairwise_distance_between_distinct_nonzero_words':pair_distance,
      'pairwise_support_intersection':pair_intersection,
      'proof_method':'Walsh inversion of the constant-weight condition on all 15 nonzero messages of F2^4.',
      'boundary':'Exact fixed-point q5 fiber-code theorem. It is a coding-theoretic simplex structure, not a claim of a physical simplex state space.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
