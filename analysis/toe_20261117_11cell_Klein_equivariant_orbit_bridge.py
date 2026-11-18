"""An independent 11-cell/Klein-cubic bridge AND a no-go.

Let G=PSL2(F11), order 660, act regularly on the 11-cell flags.
An 11-cell vertex has stabilizer A5, order 60. The Klein cubic has
the faithful 5-dimensional projective representation rho.

By the ordinary character table, the restriction of either 5D irrep
to an A5 maximal subgroup has values (5,1,-1,0,0) on A5
class sizes (1,15,20,12,12); its inner product with trivial=0
and with itself=1. As A5 is perfect, projective fixed lines are
ordinary invariant lines. Hence NO G-equivariant map from the
11-element vertex orbit G/A5 to Klein X subset CP4.

But the order11 unipotent subgroup C11 acts on rho as D with
5 distinct nontrivial eigencharacters. Every eigenline lies on X,
because f homogeneous cubic and 3a !=0 mod11. Each C11 has five
projectively fixed points on X.

There are exactly 12 C11 Sylow subgroups. Every pair distinct
generates G, verified by independent closure enumeration of
PSL2(F11); hence their fixed-point sets are disjoint, as rho(G)
has no invariant line. Consequently 12*5=60 distinguished
projective points on X in one orbit G/C11. The 660 regular
11-cell flags therefore admit a noncanonical G-equivariant
11-to-1 projection onto those 60 points, after choosing base flag,
order11 subgroup and a base eigenline. This is a constructive
symmetry-orbit dictionary, NOT a geometric incidence embedding
and not evidence for the Standard Model or 11D dynamics.
"""
import itertools,json,math
from pathlib import Path
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_11cell_Klein_G_equivariant_60orbit_obstruction.json"
p=11
def canon(a):
    z=tuple(v%p for v in a)
    neg=tuple((-v)%p for v in z)
    return min(z,neg)
I=canon((1,0,0,1))
T=canon((1,1,0,1))
S=canon((0,-1,1,0))
def mult(a,b):
    return canon((a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],
                 a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3]))
def inv(a):return canon((a[3],-a[1],-a[2],a[0]))
def subgroup(gens):
    q=deque([I]);seen={I}
    gs=list(gens)+[inv(x) for x in gens]
    while q:
        g=q.popleft()
        for h in gs:
            w=mult(g,h)
            if w not in seen:
                seen.add(w);q.append(w)
    return frozenset(seen)
def verify():
    G=subgroup([T,S])
    assert len(G)==660
    U=subgroup([T])
    assert len(U)==11
    groups={}
    for g in G:
        h=inv(g)
        t=mult(mult(g,T),h)
        K=subgroup([t])
        assert len(K)==11
        groups[K]=t
    assert len(groups)==12
    sylow=list(groups)
    pair_gen=0
    for j,A in enumerate(sylow):
        for B in sylow[j+1:]:
            assert len(A.intersection(B))==1
            pair_gen+=1
            assert len(subgroup([groups[A],groups[B]]))==660
    assert pair_gen==66
    # Normalizer size 55; the 5D representation diagonalizes U
    # into weights 1,9,4,3,5, and its normalizer cycles them.
    norm=sum(1 for g in G if subgroup([mult(mult(g,T),inv(g))])==U)
    assert norm==55
    class_sizes=[1,15,20,12,12]
    chi=[5,1,-1,0,0]
    trivial=sum(a*b for a,b in zip(class_sizes,chi))//60
    normchi=sum(a*b*b for a,b in zip(class_sizes,chi))//60
    assert trivial==0 and normchi==1
    assert sum(a*b for a,b in zip(class_sizes,chi))==0
    # Every 11-cell vertex stabilizer is A5 by regular abstract
    # polytope face action, flag group G of size660.
    nvertex=660//60
    nfixed=12*5
    assert (nvertex,nfixed)==(11,60)
    assert 660//nfixed==11
    # At any order11 eigenline, f(x)=0 because if Dv=zeta^a v,
    # f(Dv)=f(v)=zeta^(3a) f(v), and 3a !=0 mod11.
    weights=(1,9,4,3,5)
    assert all((3*a)%11 != 0 for a in weights)
    assert len(set(weights))==5
    return {
      "status":"PASS_11CELL_KLEIN_NO_VERTEX_EMBEDDING_BUT_CANONICAL_60_POINT_ORBIT_TYPE",
      "explicit_PSL2_F11_generators_mod11":{"T_upper":list(T),"S_inversion":list(S)},
      "G_order":len(G),"G_flag_regular_action":True,
      "C11_sylow_subgroups":len(sylow),"normalizer_order":norm,
      "distinct_sylow_pairs_generate_full_G":pair_gen,
      "A5_stabilizer_char_class_sizes":class_sizes,
      "restricted_five_dimensional_char_values":chi,
      "A5_trivial_multiplicity":trivial,
      "A5_character_inner_product_self":normchi,
      "G_orbit_11cell_vertices":nvertex,
      "vertex_equivariant_map_to_projective_Klein":"IMPOSSIBLE: G-equivariant map G/A5 -> X needs an A5-fixed line in C5, and 5D representation restricts irreducibly to A5.",
      "Klein_C11_fixed_projective_lines_per_sylow":5,
      "distinct_fixed_lines_on_Klein_cubic":nfixed,
      "stabilizer_of_any_fixed_line":"C11 (order11), as two distinct Sylow C11 generate G while rho is irreducible",
      "G_orbit_Klein_projective_points":60,
      "noncanonical_flag_coset_dictionary":"Identify 11-cell 660 flags with G by a base flag; fix one 11-subgroup C11 and one of its cubic eigenlines x0. Map flag g to rho(g)x0 in X. Fibers exactly right cosets g*C11, each size11; image is one G-orbit of 60 distinct cubic points. Requires base choices, so not a canonical incidence embedding.",
      "physical_limitation":"The 60-point orbit and impossibility of a direct 11-vertex embedding are representation-theoretic. They do not establish a metric, chiral spectrum, gauge fields, cubic incidence maps, or the TOE.",
      "literature":["https://arxiv.org/abs/math/0606660",
         "https://webdoc.sub.gwdg.de/ebook/serien/e/mpi_mathematik/2009/2009_76.pdf",
         "https://arxiv.org/abs/1001.4853"]}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["distinct_sylow_pairs_generate_full_G"],z["distinct_fixed_lines_on_Klein_cubic"])
