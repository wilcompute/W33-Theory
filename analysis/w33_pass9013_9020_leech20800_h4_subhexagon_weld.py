#!/usr/bin/env python3
"""Pass9013-9020: identify the 20,800 bare-Leech six-space G-set with H(2) subhexagons of H(4).

This is a group-action/literature weld, not a cardinality guess.

Internal exact input (Pass8789-8796): the bare six-spaces form a transitive
G=G2(4):2 action of degree 20,800, with point stabilizer order 24,192 and
rank-14 subdegrees recorded below.

External exact inputs:
- De Wispelaere--Van Maldeghem, Theorem 4: H(4) contains exactly 20,800
  order-2 subhexagons; a fixed one has stabilizer G2(2).2.  Their Table 2
  gives all 13 coarse intersection counts.
- GAP Character Table Library for G2(4).2 lists the index-20,800 maximal
  subgroup class as 2 x U3(3).2, order 24,192.  Since U3(3).2 ~= G2(2),
  this is the same stabilizer type.

Hence both transitive actions are the same coset G-set G/H, up to choice of
basepoint/conjugate H.  The rank-14 Leech orbitals refine the 13 classical
intersection types by splitting exactly one of the two size-3024 coarse types
into the unique transpose pair 1512+1512.  We do NOT identify which of the two
3024 intersection types splits here; that remains a separate objectwise task.
"""
from collections import Counter
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9013_9020_LEECH20800_H4_SUBHEXAGON_WELD.json'
G=503_193_600
H=24_192
assert G//H==20_800 and G%H==0
leech=[1,63,72,126,252,252,378,1512,1512,1512,2016,3024,4032,6048]
assert sum(leech)==20_800
# Pass8789's unique nonsymmetric transpose pair is two of the three degree-1512 orbitals.
fused=[1,63,72,126,252,252,378,1512,2016,3024,3024,4032,6048]
classical=[1,72,252,2016,63,126,1512,6048,378,3024,3024,252,4032]
assert Counter(fused)==Counter(classical)
assert sum(classical)==20_800
assert H==2*12_096
out={
 'schema':'w33.pass9013_9020.leech20800_h4_subhexagon_weld.v1','status':'PASS','passes':'9013-9020',
 'group':'G2(4):2','group_order':G,'degree':20800,
 'Leech_action':{'source':'Pass8789-8796','point_stabilizer_order':H,'rank':14,'subdegrees':leech,'unique_transpose_pair_degrees':[1512,1512]},
 'classical_action':{'object':'order-2 subhexagons H(2) inside split Cayley hexagon H(4)','count':20800,'stabilizer':'G2(2).2 = 2 x U3(3).2','stabilizer_order':H,'Table2_coarse_counts':classical},
 'GAP_CTblLib':{'index_20800_maximal_subgroup':'2 x U3(3).2','order':H},
 'coarse_refinement':{'Leech_rank14_fused_counts':fused,'matches_Table2_multiset':True,'unresolved':'which one of the two classical 3024 intersection types splits into the oriented 1512+1512 pair'},
 'external_sources':['https://cage.ugent.be/geometry/Files/305/Jay2.pdf','https://www.math.rwth-aachen.de/~Thomas.Breuer/ctbllib/ctbltoc/data/G2%284%29.2.html'],
 'theorem':'The 20,800 bare-Leech six-spaces and the 20,800 order-2 subhexagons of H(4) are the same transitive G2(4):2 coset G-set G/H (up to basepoint/conjugate H), with H of order 24,192 and type 2 x U3(3).2. The Leech rank-14 orbital geometry refines the classical 13 intersection types by splitting exactly one size-3024 type into its unique transpose pair of size 1512+1512.',
 'claim_boundary':'Exact transitive G-set/coset identification from the internally certified action plus published stabilizer/count and CTblLib maximal-subgroup class. No explicit coordinate bijection between Leech six-spaces and H(4) subhexagons is constructed here.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','degree':20800,'stabilizer':H,'coarse_types':13,'orbital_rank':14}))
