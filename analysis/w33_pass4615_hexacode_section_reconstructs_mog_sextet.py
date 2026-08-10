#!/usr/bin/env python3
"""Pass 4615 -- the paired-axis hexacode section reconstructs a unique Golay sextet.

Canonical renumbering of the independently developed Golay result that briefly
used Pass4607 before a parallel lane's earlier 4607--4614 reservation surfaced.

Pass4592 found an exact [18,6,8] binary concatenated-hexacode subcode inside the
repo's extended binary Golay G24, with six zero coordinates. The 45 weight-8
subcode words are Golay octads. Their pair-frequency-10 graph on the 18 active
coordinates is six disjoint K3s, reconstructing the six binary [3,2,2] inner
triples. Among all 6!=720 matchings of the six zero coordinates to those six
triples, exactly one makes the resulting six tetrads a Golay sextet: every union
of two tetrads is a Golay octad.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import w33_pass4592_paired_axes_simplex_hexacode_golay as p4592
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4615_HEXACODE_SECTION_RECONSTRUCTS_MOG_SEXTET.json'
def main():
    G=p4592.golay24();octads={x for x in G if x.bit_count()==8};assert len(octads)==759
    basis=[G[1<<i] for i in range(12)];sub=p4592.enum_code(basis[:6]);assert len(sub)==64
    zeros=[j for j in range(24) if all(((x>>j)&1)==0 for x in sub)];active=[j for j in range(24) if j not in zeros]
    assert zeros==[17,18,19,20,21,22] and len(active)==18
    sub18={p4592.restrict_word(x,active) for x in sub};mins=[x for x in sub18 if x.bit_count()==8];assert len(mins)==45
    assert {sum((x>>i)&1 for x in mins) for i in range(18)}=={20}
    pairfreq={(i,j):sum(((x>>i)&1) and ((x>>j)&1) for x in mins) for i,j in itertools.combinations(range(18),2)}
    assert Counter(pairfreq.values())==Counter({8:135,10:18})
    adj=[set() for _ in range(18)]
    for (i,j),c in pairfreq.items():
        if c==10:adj[i].add(j);adj[j].add(i)
    seen=set();triples=[]
    for i in range(18):
        if i in seen:continue
        C={i};stack=[i];seen.add(i)
        while stack:
            u=stack.pop()
            for v in adj[u]:
                if v not in seen:seen.add(v);C.add(v);stack.append(v)
        assert len(C)==3 and all(v in adj[u] for u,v in itertools.combinations(C,2));triples.append(tuple(sorted(active[k] for k in C)))
    triples=sorted(triples);assert len(triples)==6
    valid=[]
    for perm in itertools.permutations(zeros):
        tetrads=[set(triples[i])|{perm[i]} for i in range(6)]
        if all(sum(1<<j for j in tetrads[a]|tetrads[b]) in octads for a,b in itertools.combinations(range(6),2)):
            valid.append((perm,[tuple(sorted(T)) for T in tetrads]))
    assert len(valid)==1;perm,tetrads=valid[0]
    out={'pass':4615,'canonical_renumbering_from_collision_alias':4607,'hexacode_section':{'parameters':'[18,6,8] zero-padded inside G24','weight8_octads':45,'active_points':18,'zero_coordinates':zeros,'point_frequency_in_45_octads':20,'pair_frequency_distribution':{'8':135,'10':18}},'recovered_inner_columns':{'high_pair_frequency':10,'graph':'6 disjoint K3','triples':triples},'sextet_completion':{'matchings_tested':720,'valid_matchings':1,'zero_coordinate_assignment':list(perm),'six_tetrads':tetrads,'pairwise_tetrad_unions_checked':15,'all_pairwise_unions_are_Golay_octads':True},'theorem':'The exact 6D Golay/hexacode section recovered from the paired cubic axes reconstructs six inner-code triples, and ambient G24 uniquely matches its six zero coordinates to complete them to a Golay sextet.','boundary':'Coordinate-explicit code/design theorem; no O^-(6,2) subgroup-of-M24 claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
