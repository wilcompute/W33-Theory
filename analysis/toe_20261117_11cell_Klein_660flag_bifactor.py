"""Exact 11x60 = 660 flag dictionary from a complementary
A5 and C11 in PSL2(11), using explicit 2x2 matrices over F11.

The 11-cell has 660 flags, regular G=PSL2(11) action;
its rank-0 (vertices) and rank-3 (facets) each have 11
faces, stabilizers A5 order60 in possibly different A5
conjugacy classes. The Klein-cubic distinguished projective
60-point orbit is G/C11 (previous independent verifier).

Since any A5 H and C11 U have H∩U=1 and |H|*|U|=660,
the map from regular flags g to (gH,gU) identifies every
flag with exactly one (11-face,60-cubic-point) pair.
This is a pair-incidence BIJECTION, but NOT an isometry
or map preserving all face ranks (edges, triangles, cells).
"""
import json
from pathlib import Path
from toe_20261117_11cell_Klein_equivariant_orbit_bridge import (
 I,T,S,canon,mult,subgroup
)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_11cell_660flags_11faces_60Klein_bifactor.json"
def order(g):
    x=I
    for k in range(1,661):
        x=mult(x,g)
        if x==I:return k
    raise AssertionError("not group element")
def verify():
    G=sorted(subgroup([S,T]))
    assert len(G)==660
    I2=[x for x in G if order(x)==2]
    I3=[x for x in G if order(x)==3]
    assert (len(I2),len(I3))==(55,110)
    pair=None
    H=None
    for a in I2:
        for b in I3:
            if order(mult(a,b))==5:
                h=subgroup([a,b])
                assert len(h)==60
                pair=(a,b)
                H=h
                break
        if H is not None:break
    assert H is not None
    U=subgroup([T])
    assert len(U)==11 and H.intersection(U)=={I}
    products={mult(h,u) for h in H for u in U}
    assert len(products)==660 and products==set(G)
    def coset(g,group):return frozenset(mult(g,h) for h in group)
    VC={coset(g,H) for g in G}
    KC={coset(g,U) for g in G}
    assert (len(VC),len(KC))==(11,60)
    vi={v:i for i,v in enumerate(sorted(VC,key=lambda x:min(x)))}
    pi={v:i for i,v in enumerate(sorted(KC,key=lambda x:min(x)))}
    flags=[{"PSL2_11_matrix":list(g),
            "abstract_11face_id":vi[coset(g,H)],
            "Klein_60point_orbit_id":pi[coset(g,U)]}
           for g in G]
    keys={(x["abstract_11face_id"],x["Klein_60point_orbit_id"])
          for x in flags}
    assert len(keys)==660
    assert keys=={(i,j) for i in range(11) for j in range(60)}
    for a in I2[::7]:
        for b in G[::51]:
            ga=mult(a,b)
            assert vi[coset(ga,H)]==vi[coset(mult(a,b),H)]
            assert pi[coset(ga,U)]==pi[coset(mult(a,b),U)]
    matrix=[[-1]*60 for _ in range(11)]
    for i,v in enumerate(flags):
        k=v["abstract_11face_id"];m=v["Klein_60point_orbit_id"]
        assert matrix[k][m]==-1
        matrix[k][m]=i
    assert all(k>=0 for row in matrix for k in row)
    return {"status":"PASS_EXPLICIT_PSL2_11_A5_C11_COMPLEMENTARY_FLAG_KLEIN_11x60_BIJECTION",
       "PSL2_mod11_order":len(G),
       "involution_element_count":len(I2),
       "order3_element_count":len(I3),
       "explicit_A5_generator_order2":list(pair[0]),
       "explicit_A5_generator_order3":list(pair[1]),
       "generator_product_order5":order(mult(*pair)),
       "generated_A5_order":len(H),
       "generated_C11_order":len(U),
       "intersection_size":len(H.intersection(U)),
       "product_set_cardinality":len(products),
       "eleven_face_cosets":len(VC),
       "sixty_Klein_orbit_cosets":len(KC),
       "full_11x60_pairs":len(keys),
       "explicit_flag_table":flags,
       "matrix_entry_flag_index":matrix,
       "face_rank_caution":"The selected explicit A5 subgroup may represent either the vertex or facet conjugacy class of the 11-cell. Both classes have index11 and the complementary factorization holds for either; identifying this matrix subgroup with a named rank requires matching the user's 11-cell flag-generator convention.",
       "noncanonical_G_equivariant_map":"Select a regular 11-cell base flag and A5 face stabilizer H, plus a Klein cubic eigenline fixed by U=C11. Then g->(gH,gU) is a bijection between 660 flags and 11x60 pairs. It is equivariant under left G multiplication.",
       "geometry_limit":"Pair dictionary is exact group combinatorics; it does not prove incidence at ranks1/2, continuous geometric embedding, special holonomy, gauge groups, chiral spectra or physical TOE.",
       "references":["https://arxiv.org/abs/math/0606660",
          "https://arxiv.org/abs/1001.4853"]}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["generated_A5_order"],z["full_11x60_pairs"])
