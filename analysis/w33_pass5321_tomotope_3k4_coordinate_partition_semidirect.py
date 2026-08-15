#!/usr/bin/env python3
"""Pass5321: geometric realization of Gamma(T)=(C2)^4:S3 on tesseract face pairs.

Pass5319 realizes the published tomotope group as W(D4)/Z acting on the 12
antipodal square-face pairs of the tesseract.  Pass5320 finds three invariant
perfect-matching orbitals whose union is 3 K4.

The three K4 components have a direct coordinate meaning.  A square face fixes
an unordered pair of the four coordinate axes.  Antipodal pairing leaves two
sign classes per coordinate pair.  The 12 objects therefore group as

  (01 with 23), (02 with 13), (03 with 12),

namely the three complementary 2+2 partitions of four axes, four face-pairs per
partition.  The induced tomotope action on these three components is S3; its
kernel has order16 and is elementary abelian C2^4.  Hence the natural action
itself realizes

    Gamma(T) = (C2)^4 : S3

without relying only on abstract group invariants.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup

from analysis.w33_pass5310_tesseract_rotation_d4_tomotope_doublecovers import signed_groups
from analysis.w33_pass5319_d4_tesseract_facepairs_tomotope_action import build_face_pairs,induced
from analysis.w33_pass5320_tesseract_rotation_vs_d4_facepair_orbital_fusion import orbitals,small_graph_components

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5321_TOMOTOPE_3K4_COORDINATE_PARTITION_SEMIDIRECT.json'

def key(g,n):return tuple(g(i) for i in range(n))
def component_perm(g,components):
    sets=[set(c) for c in components];out=[]
    for C in sets:
        I={g(x) for x in C};out.append(next(i for i,D in enumerate(sets) if I==D))
    return tuple(out)

def main():
    V,vi,B,R,D=signed_groups();faces,pairs,labels=build_face_pairs(V,vi)
    G=induced(D,faces,pairs);assert G.order()==96
    O=orbitals(G);components,deg,edges=small_graph_components(O)
    assert components==[[0,1,10,11],[2,3,8,9],[4,5,6,7]] and deg==[3]*12 and edges==18

    fixed=[tuple(x['fixed_coordinates']) for x in labels]
    coordinate_partitions=[]
    for C in components:
        ps=sorted(set(fixed[i] for i in C))
        assert len(ps)==2 and set(ps[0]).isdisjoint(ps[1]) and set(ps[0])|set(ps[1])==set(range(4))
        coordinate_partitions.append([list(ps[0]),list(ps[1])])
    assert coordinate_partitions==[
      [[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]
    ]

    cperms={component_perm(g,components) for g in G.generate_schreier_sims()}
    assert len(cperms)==6
    Cgroup=PermutationGroup([Permutation(list(p)) for p in cperms]);assert Cgroup.order()==6
    assert Counter(int(g.order()) for g in Cgroup.generate_schreier_sims())==Counter({2:3,3:2,1:1})

    ker=[g for g in G.generate_schreier_sims() if component_perm(g,components)==(0,1,2)]
    K=PermutationGroup(ker);assert K.order()==16 and K.abelian_invariants()==[2,2,2,2]
    assert Counter(int(g.order()) for g in K.generate_schreier_sims())==Counter({2:15,1:1})
    assert sorted(map(len,K.orbits()))==[4,4,4]

    out={'pass':5321,'status':'THEOREM_TOMOTOPE96_NATURAL_FACEPAIR_ACTION_REALIZES_C2_4_SEMIDIRECT_S3',
      'objects':12,'small_relation_graph':'3 K4','components':components,
      'coordinate_partition_labels':coordinate_partitions,
      'interpretation':'Each K4 component is the four antipodal face-pairs attached to one complementary 2+2 partition of the four tesseract coordinate axes.',
      'component_action':{'image_order':6,'image':'S3','permuted_objects':'three complementary 2+2 axis partitions'},
      'kernel':{'order':16,'structure':'(C2)^4','element_orders':{'1':1,'2':15},'orbits_on_12':[4,4,4]},
      'semidirect_product':'Gamma(T) = (C2)^4 : S3 is realized directly by this natural tesseract face-pair action.',
      'bridge':'The normal 16-module from Pass5309/5310 is now visible as the kernel fixing the three 2+2 coordinate partitions, while the S3 quotient permutes those partitions.',
      'boundary':'This identifies the tomotope group action with D4/tesseract coordinate geometry. It does not identify the distinct orientation-preserving order192 double cover with W(D4).'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
