#!/usr/bin/env python3
"""Close the full E6 involution ladder onto the cubic 36/45 incidence geometry.

Builds on w33_e6_involution_reconstructs_double_six_tritangent.py.

New exact closure:
  * degree 1 (36): reflections <-> double-sixes;
  * degree 2 (270): products of commuting reflection pairs <-> the 270
    syzygetic double-six pairs, characterized here by 4-line support overlap;
  * degree 4 (45): unique involution for each tritangent, via its pointwise
    fixed triple;
  * degree 3 (540): not merely a 12-sheeted cover of the 45 tritangents.
    If T is its fixed tritangent and q_T the unique degree-4 involution fixing T,
    then w q_T is a reflection r_D and D is disjoint from T.  This gives a
    bijection

        {degree-3 involutions} <-> {(T,D): T tritangent, D double-six, T cap D=empty}

    of size 540 = 45*12.

Thus all four involution degrees participate directly in the cubic incidence
triangle.  The complementary 1080 tritangent/double-six pairs have two-line
intersection and are not degree-3 involution flags.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
import itertools

import w33_e6_involution_reconstructs_double_six_tritangent as B

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_e6_involution_ladder_flags.json'


def main(write=True):
    lines,_=B.line_classes(); meet,tritangents,double_sixes=B.carriers(lines)
    _,W=B.build_weyl(lines); I=tuple(range(27))
    inv=[]
    for p,s in W.items():
        if p!=I and B.compose(p,p)==I:
            inv.append((s,sum(p[i]==i for i in range(27)),p))

    ds_supports=sorted((frozenset().union(*D) for D in double_sixes),key=lambda x:tuple(sorted(x)))
    reflections=[p for s,f,p in inv if s==-1 and f==15]
    refl_by_support={frozenset(i for i in range(27) if p[i]!=i):p for p in reflections}
    assert set(refl_by_support)==set(ds_supports)

    # Degree-2 class = syzygetic double-six pairs = commuting reflection pairs.
    pair_census=Counter(); commuting=[]; products=[]
    for A,C in itertools.combinations(ds_supports,2):
        z=len(A&C); pair_census[z]+=1
        r,s=refl_by_support[A],refl_by_support[C]
        if B.compose(r,s)==B.compose(s,r):
            commuting.append((A,C)); products.append(B.compose(r,s)); assert z==4
        else:
            assert z==6
    assert pair_census==Counter({6:360,4:270})
    degree2=[p for s,f,p in inv if s==1 and f==7]
    assert len(commuting)==270 and len(set(products))==270 and set(products)==set(degree2)

    # Degree-4 class gives a direct tritangent bijection.
    degree4=[p for s,f,p in inv if s==1 and f==3]
    q_by_T={frozenset(i for i in range(27) if p[i]==i):p for p in degree4}
    assert len(q_by_T)==45 and set(q_by_T)==tritangents

    # Degree-3 class gives the 540 disjoint tritangent/double-six flags.
    degree3=[p for s,f,p in inv if s==-1 and f==3]
    fibres=defaultdict(list)
    for w in degree3:
        T=frozenset(i for i in range(27) if w[i]==i); assert T in tritangents; fibres[T].append(w)
    assert len(fibres)==45 and {len(F) for F in fibres.values()}=={12}

    flags=[]
    for T,F in fibres.items():
        q=q_by_T[T]
        image=[]
        for w in F:
            assert B.compose(w,q)==B.compose(q,w)
            r=B.compose(w,q)
            assert B.compose(r,r)==I and W[r]==-1 and sum(r[i]==i for i in range(27))==15
            D=frozenset(i for i in range(27) if r[i]!=i)
            assert D in refl_by_support and len(T&D)==0
            image.append(D); flags.append((T,D))
        # exactly the 12 double-sixes disjoint from T
        expected={D for D in ds_supports if not (T&D)}
        assert len(expected)==12 and set(image)==expected and len(set(image))==12
    assert len(flags)==540 and len(set(flags))==540

    all_pairs=Counter(len(T&D) for T in tritangents for D in ds_supports)
    assert all_pairs==Counter({2:1080,0:540})
    assert set(flags)=={(T,D) for T in tritangents for D in ds_supports if not (T&D)}

    out={
      'schema':'w33.e6_involution_ladder_flags.v1','status':'PASS',
      'headline':'All four nontrivial involution degrees of W(E6) land directly on the cubic 36/45 incidence geometry. Degree-1 reflections are the 36 double-sixes by moved support. Degree-2 involutions are exactly the 270 products of commuting reflection pairs, equivalently the 270 syzygetic double-six pairs with four-line overlap. Degree-4 involutions are in bijection with the 45 tritangents by their pointwise fixed triples. Finally, if w is degree 3 with fixed tritangent T and q_T is the unique degree-4 involution fixing T, then w q_T is the reflection of a double-six D disjoint from T; this is a bijection between the 540 degree-3 involutions and the 540 disjoint tritangent-double-six flags.',
      'involution_ladder':{
        'degree1':{'count':36,'carrier':'double-sixes','map':'moved 12-line support'},
        'degree2':{'count':270,'carrier':'syzygetic double-six pairs','map':'product of commuting reflection pair','support_intersection':4},
        'degree3':{'count':540,'carrier':'disjoint tritangent-double-six flags','map':'w -> (FixLines(w), moved_support(w q_T))'},
        'degree4':{'count':45,'carrier':'tritangents','map':'pointwise fixed three-line set'}
      },
      'double_six_pair_census':{'syzygetic_overlap4':270,'azygetic_overlap6':360,'total':630},
      'degree3_flag_factorization':{'identity':'540=45*12','fibres_per_tritangent':12,'all_540_disjoint_flags_hit_once':True,'q_T_commutes_with_all_12_degree3_fibre_elements':True},
      'full_cross_incidence':{'disjoint_flags':540,'two_line_pairs':1080,'total':1620},
      'crosscheck':'Pass4659 independently gives the same 45x36 0^540,2^1080 tritangent/double-six census.',
      'boundary':'Exact finite W(E6)/cubic-surface theorem. Names syzygetic/azygetic refer to the classical double-six support intersections; no physical E6 dynamics are asserted.',
      'checks':{'degree2_is_270_commuting_reflection_pairs':True,'degree4_bijection_45_tritangents':True,'degree3_bijection_540_disjoint_flags':True,'all_four_involution_degrees_geometric':True}
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out

if __name__=='__main__': main(True)
