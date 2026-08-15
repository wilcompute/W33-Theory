#!/usr/bin/env python3
"""Pass5269 (outside-box): every q5 K0 block-minimum support is a W-point footprint.

Pass5262 proves d_block(K0)=25 by the complete weight-8 footprint-dual shell.
Let S be the block support of a nonzero K0 word with |S|=25.  In the proof,
for t_D=|S cap D|,

  300|S| <= sum_D C(t_D,2) <= 25 C(|S|,2).

At |S|=25 both sides equal 7500, so equality holds everywhere.  In particular:

  * every nonzero t_D equals 2 (the lower inequality is sharp only at t=0,2);
  * every unordered pair of blocks in S has the maximum shell codegree 25.

Pass5232 identifies shell codegree25 with relation R1, the adjacency relation of
the q=5 P-block graph NO_5^+(5).  Thus S is a 25-clique.  The authoritative
Pass5238 maximum-clique census finds exactly 156 cliques of size25, and they are
exactly the W(3,5) point footprints.  Therefore the entire block-minimum SUPPORT
shell of K0 is exactly those 156 point footprints.

This is strikingly parallel to C_F itself: its Hamming minimum supports are the
same 156 point footprints.  The two codes live in different spaces/metrics, so
this is a shared support geometry, not an identification of the codes.

Known realizations: for each W point p there are six chamber stars based at p.
Any difference of two of them lies in K0, has the point footprint of p as its 25
active P blocks, and has local weight40 in every active block.  Hence every one
of the 156 block-minimum support types is realized, with at least C(6,2)=15
explicit weight1000 words on that support.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5269_ZEROP_BLOCK_MINIMUM_SUPPORT_RIGIDITY.json'

def main():
    w=25;r=600;lam=25
    lhs=r*w//2;rhs=lam*w*(w-1)//2
    assert lhs==rhs==7500
    out={'pass':5269,'status':'THEOREM_Q5_ZEROP_BLOCK_MINIMUM_SUPPORTS_ARE_POINT_FOOTPRINTS',
      'zero_footprint_block_distance':25,
      'moment_equality_value':7500,
      'equality_conditions':['Every weight-8 dual shell check meets a block-minimum support in 0 or 2 blocks.','Every pair of blocks in the support has shell pair-codegree25, i.e. lies in relation R1.'],
      'support_graph':'A 25-clique in NO_5^+(5).',
      'maximum_clique_census':'Pass5238: exactly156 maximum 25-cliques, exactly the W(3,5) point footprints.',
      'block_minimum_supports':156,
      'shared_geometry':'The Hamming-minimum supports of C_F and the block-minimum supports of K0 are the same 156 point footprints.',
      'explicit_realizations':'For each point p, differences of the C(6,2)=15 pairs of chamber stars based at p give K0 words of weight1000 on that support, with 25 local blocks of weight40.',
      'boundary':'Support classification only. It does not claim that the 2340 adjacent-star differences exhaust all K0 words with a given minimum block support or all weight1000 K0 words.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
