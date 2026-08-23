#!/usr/bin/env python3
"""Pass9973-9980 outside-box: replace the false additive 13-selector by a C13 neighbor clock.

Two parallel results constrain the V2 side sharply.
(1) Pass9861-9884 found at least three frame-pair relation types and six shared
    sum classes with conflicting relations, falsifying the universal law that a
    frame-pair relation depends only on the sum/difference class.
(2) Pass9921-9944 located the binary Golay code on the A1^24 2-neighbor: every
    type-8 frame direction is a bridge to an embedded A1^24 neighbor whose glue
    is Golay (classical Niemeier fact).

There also cannot be a nontrivial additive homomorphism V2=(F2)^12 -> C13,
because |V2|=4096 is coprime to 13.

But 13 survives multiplicatively. ord_13(2)=12, so Phi_13 is irreducible over
F2. Its 12x12 companion matrix has order 13 and every nonidentity power has no
nonzero fixed vector. Thus V2\{0}, the 4095 frame/neighbor directions, splits
into 315 semiregular cycles of length 13. This is the exact analogue of the
G2-side C13 clocks from Pass9957-9964, but it is an automorphism clock rather
than an additive quotient.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9973_9980_V2_C13_NEIGHBOR_CLOCK.json'
N=12

def rank2(A):
    A=np.array(A,dtype=np.uint8)%2;m,n=A.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]),None)
        if q is None:continue
        if q!=r:A[[r,q]]=A[[q,r]]
        for i in range(m):
            if i!=r and A[i,c]:A[i]^=A[r]
        r+=1
        if r==m:break
    return r

def power(A,k):
    R=np.eye(A.shape[0],dtype=np.uint8)%2;B=A.copy()%2
    while k:
        if k&1:R=R@B%2
        B=B@B%2;k//=2
    return R%2

def main():
    # Phi_13(x)=x^12+...+x+1 companion over F2.
    M=np.zeros((N,N),dtype=np.uint8)
    for i in range(1,N):M[i,i-1]=1
    M[:,N-1]=1
    I=np.eye(N,dtype=np.uint8)%2
    assert np.array_equal(power(M,13),I)
    assert all(not np.array_equal(power(M,k),I) for k in range(1,13))
    fixed_ranks=[rank2((power(M,k)-I)%2) for k in range(1,13)]
    assert fixed_ranks==[12]*12
    # ord_13(2)=12.
    assert pow(2,12,13)==1 and all(pow(2,k,13)!=1 for k in range(1,12))
    assert (2**12-1)//13==315
    assert math.gcd(2**12,13)==1

    sample={'classes':34,'pairs':561,'relation_types_at_least':3,'shared_sum_classes':102,'sum_relation_disagreements':6}
    clocks={'V2_nonzero_frame_neighbor_cycles':315,'G2_vertices':32,'G2_edges':1600,'cycle_length':13}
    out={
      'schema':'w33.pass9973_9980.v2_c13_neighbor_clock.v1','status':'PASS','passes':'9973-9980','outside_box':True,
      'parallel_constraints':{
        'Pass9861_9884':sample,
        'sum_law':'REFUTED: six sampled sum classes carry different frame-pair relations',
        'Pass9921_9944':'type-8 frame directions bridge Leech to A1^24 2-neighbors; binary Golay is the neighbor glue, not a coordinate code on Lambda/2Lambda'},
      'additive_no_go':{'V2_order':4096,'target_C13_order':13,'gcd':1,'nontrivial_group_homomorphism_V2_to_C13':False},
      'multiplicative_C13':{
        'ord_13_of_2':12,'Phi13_irreducible_over_F2':True,'matrix':'companion of x^12+x^11+...+x+1',
        'matrix_order':13,'rank(M^k-I)_for_k_1_to_12':fixed_ranks,'nonzero_fixed_points_for_nonidentity_powers':0,
        'nonzero_V2_directions':4095,'cycles':315,'cycle_length':13},
      'common_clock_counts':clocks,
      'information_consequence':{'observed_frame_relation_symbols_at_least':3,'binary_relation_bit_sufficient':False,'minimum_binary_storage_bits_for_observed_relation':2},
      'theorem':('The 13-state V2 idea is not additive: no nontrivial V2->C13 homomorphism exists and the sampled sum-law is false. Instead F2^12 admits a fixed-point-free order-13 linear automorphism, partitioning its 4,095 nonzero frame/A1^24-neighbor directions into exactly 315 thirteen-cycles. This matches the semiregular C13-clock architecture on the G2 vertices and edges.'),
      'boundary':('The companion-matrix C13 action is an exact abstract GL(12,2) construction. It is not yet proved to lie in the actual Co0 stabilizer of the canonical V2, so the common-clock comparison is an algebraic target rather than an established Leech-equivariant weld. The frame-relation statements retain the Pass9861 sample boundary.')}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','cycles':clocks,'fixed_ranks':fixed_ranks}));return 0
if __name__=='__main__':raise SystemExit(main())
