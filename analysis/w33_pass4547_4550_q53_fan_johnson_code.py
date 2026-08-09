#!/usr/bin/env python3
"""Passes 4547/4550 -- the Q(5,3) prism carrier is a 9D fan code with a J(10,3) shell.

Fix a noncollinear point pair x,y in Q(5,3)=GQ(3,9).  Its ten common
neighbors z_i give ten rungs r_i, where r_i is the binary indicator of the two
lines xz_i and yz_i in the 280-vertex line graph.  Let A be that line graph and
put y_i=A r_i over F2.

The full ten-rung fan is in ker A (Pass 4526), so sum_i y_i=0.  A direct GQ
count gives, for a k-rung coefficient set R,

    wt( sum_{i in R} y_i ) = 20*(k mod 2) + 4*k*(10-k).

Reason: the 20 fan lines each see k selected fan lines; the 80 external lines
through one of the z_i meet both members of one rung and contribute zero; for
every ordered i!=j there are exactly two remaining common-neighbor lines of
xz_i and yz_j, contributing iff exactly one of i,j lies in R.

The only coefficient relation is the all-ten fan: if 0<k<10, the displayed
weight is positive.  Hence the local image is a [280,9,56] binary code.  Modulo
R~R^c its complete weight enumerator is

  1 + 10 z^56 + 45 z^64 + 210 z^96 + 120 z^104 + 126 z^120.

The 120 three-rung words are exactly the protected triangular-prism images from
Pass 4524.  For two triples R,R', their Hamming distance is the fan-code weight
at k=|R triangle R'|.  Thus distance 64 occurs exactly for |R intersect R'|=2;
the distance-64 graph is the Johnson graph J(10,3).  Intersections 1 and 0 both
give distance 96, so Hamming distance deliberately coarsens the full Johnson
association scheme.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4547_4550_Q53_FAN_JOHNSON_CODE.json'


def fan_weight(k:int)->int:
    assert 0<=k<=10
    return 20*(k&1)+4*k*(10-k)


def main()->int:
    assert [fan_weight(k) for k in range(11)] == [0,56,64,104,96,120,96,104,64,56,0]

    # Coefficient subsets modulo the unique all-ten complement relation.
    enumerator=Counter()
    for k in range(5):
        enumerator[fan_weight(k)] += __import__('math').comb(10,k)
    enumerator[fan_weight(5)] += __import__('math').comb(10,5)//2
    assert enumerator == Counter({96:210,120:126,104:120,64:45,56:10,0:1})
    assert sum(enumerator.values())==512

    triples=list(itertools.combinations(range(10),3))
    assert len(triples)==120
    dist=Counter(); relation=Counter()
    for a,b in itertools.combinations(triples,2):
        r=len(set(a)&set(b)); k=2*(3-r); d=fan_weight(k)
        dist[d]+=1; relation[(r,d)]+=1
    assert relation == Counter({(1,96):3780,(0,96):2100,(2,64):1260})

    # J(10,3) adjacency is intersection size two.  Verify its standard degree
    # and the non-SRG split (intersection one versus zero) rather than calling
    # the Hamming two-distance shell strongly regular.
    nbr=[set() for _ in triples]
    for i,j in itertools.combinations(range(120),2):
        if len(set(triples[i])&set(triples[j]))==2:
            nbr[i].add(j);nbr[j].add(i)
    assert {len(x) for x in nbr}=={21}
    common_adj=Counter();common_non=Counter()
    for i,j in itertools.combinations(range(120),2):
        c=len(nbr[i]&nbr[j])
        (common_adj if j in nbr[i] else common_non)[c]+=1
    assert common_adj==Counter({8:1260})
    assert common_non==Counter({4:3780,0:2100})

    out={
      'passes':[4547,4550],
      'geometry':{'GQ':'Q(5,3)=GQ(3,9)','noncollinear_point_pairs':4536,'rungs_per_pair':10},
      'local_fan_code':{
        'length':280,'dimension':9,'minimum_distance':56,'codewords':512,
        'kernel_relation':'sum of all ten rung images = 0; no other coefficient relation',
        'weight_formula':'w(k)=20*(k mod 2)+4*k*(10-k)',
        'weight_enumerator':{str(k):v for k,v in sorted(enumerator.items())}},
      'prism_shell':{
        'words_per_fan':120,'weight':104,
        'global_prisms':4536*120,
        'global_images_distinct_by_pass4524':True,
        'pair_distance_counts':{str(k):v for k,v in sorted(dist.items())},
        'distance64_iff_triple_intersection':2,
        'distance96_iff_triple_intersection':[0,1],
        'distance64_graph':'Johnson J(10,3)','johnson_degree':21,
        'johnson_adjacent_common_neighbors':8,
        'johnson_nonadjacent_common_neighbors_by_intersection':{'1':4,'0':0}},
      'boundary':'Exact local GQ counting plus Pass 4524 global injectivity. The protected Hamming metric merges the Johnson intersection-1 and intersection-0 relations; no W33-style edge-fiber collapse is claimed.'}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__': raise SystemExit(main())
