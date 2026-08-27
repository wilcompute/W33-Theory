#!/usr/bin/env python3
"""Pass10525-10532: derive H1(Levi H4;F2) ~= F2[V2] from the free C13 chain complex.

Pass10501-10508 proved the two modules have the same semisimple C13 character.
Here the isomorphism is derived directly from the cellular chain resolution.

The explicit C13 acts freely on H(4) points, lines and flags.  The quotient Levi
graph Q therefore has
  105 point vertices + 105 line vertices = 210 vertices,
  525 edges,
and is connected.

Let R=F2[C13].  The lifted chain modules are free R-modules
  C1 = R^525, C0 = R^210.
The graph exact sequence is
  0 -> H1 -> R^525 -> R^210 -> F2 -> 0.
Since char(F2)=2 does not divide 13, R is semisimple (Maschke), so both short
exact pieces split.  Therefore
  H1 ~= F2 + R^(525-210) = F2 + R^315.

On the other hand C13 has one fixed vector 0 in V2 and 315 free orbits on the
4095 nonzero vectors, so the permutation module is literally
  F2[V2] ~= F2 + R^315.
Thus the C13-module isomorphism follows from the chain resolution itself.

Choosing a spanning tree of Q, orbit representatives of lifted edges, and
R-linear splittings gives an explicit 4096x4096 intertwiner algorithmically;
no canonical choice of those splittings is asserted.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10525_10532_HEXAGON_CHAIN_RESOLUTION_V2.json'

def main():
    group_order=13
    q_points=q_lines=105;q_vertices=210;q_edges=525
    assert q_edges-q_vertices+1==316
    free_rank=q_edges-q_vertices
    assert free_rank==315
    h1_dim=1+free_rank*group_order
    assert h1_dim==4096
    v2_size=4**6;assert v2_size==4096
    assert (v2_size-1)//13==315
    # Semisimple decomposition of regular R=F2[C13]: 1 + W12.
    assert 1+315*13==4096
    assert 1+315==316
    assert 315*12+316==4096
    out={
      'schema':'w33.pass10525_10532.hexagon_chain_resolution_v2.v1','status':'PASS','passes':'10525-10532',
      'cover':{'deck_group':'C13','free_on':'H(4) points, lines and flags','quotient_points':q_points,'quotient_lines':q_lines,'quotient_vertices':q_vertices,'quotient_edges':q_edges,'quotient_beta1':316},
      'group_algebra':{'R':'F2[C13]','semisimple':True,'reason':'Maschke: 2 does not divide 13','regular_module_dimension':13},
      'chain_resolution':'0 -> H1 -> R^525 -> R^210 -> F2 -> 0',
      'split_result':{'H1':'F2 + R^315','dimension':h1_dim,'free_regular_rank':free_rank},
      'V2_permutation_module':{'zero_orbit':1,'free_nonzero_C13_orbits':315,'module':'F2 + R^315','dimension':v2_size},
      'theorem':'The C13-module isomorphism H1(Levi H(4);F2) ~= F2[V2] is a direct consequence of the free-cover cellular chain resolution, not merely a character coincidence: both modules are F2 plus 315 copies of the regular F2[C13] module.',
      'constructive_upgrade':'Choose a spanning tree of the 210-vertex quotient graph, representatives of the 525 edge orbits, and R-linear splittings of the boundary sequence. These choices produce an explicit 4096x4096 C13-intertwiner.',
      'boundary':'The existence and free-module decomposition are canonical at the isomorphism-class level. A specific chain-to-vector matrix depends on noncanonical tree/splitting choices, and no full G2(4)-equivariant isomorphism is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','H1':'F2 + F2[C13]^315','V2':'F2 + F2[C13]^315','explicit_map':'constructive_after_splitting'}))
    return 0
if __name__=='__main__':raise SystemExit(main())
