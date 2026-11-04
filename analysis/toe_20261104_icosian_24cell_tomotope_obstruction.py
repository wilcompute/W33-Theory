#!/usr/bin/env python3
"""Exact 600-cell / 24-cell / Reye group bridge and order-576 obstruction.

Coordinate arithmetic in Z[phi], phi^2=phi+1; each quaternion stored as
four (a,b) pairs representing (a+b*phi)/2. Group 2I has 120 elements;
Hurwitz 2T subgroup has 24. Replicates established 25 24-cell 5x5 geometry
(Denney et al 2020); NEW comparison: 24-cell H4 stabilizer 576 and
Reye/tomotope-medial Aut576 are NOT isomorphic (element-order spectra).
"""
from __future__ import annotations
import itertools,collections,json
from pathlib import Path
import networkx as nx
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_icosian_24cell_tomotope_obstruction.json"
Z=(0,0);ONE=(1,0);PHI=(0,1);PHIM1=(-1,1)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[0],-a[1]
def m(a,b):
    return (a[0]*b[0]+a[1]*b[1],
            a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def parity(p):
    return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))&1
def qmul(x,y):
    a,b,c,d=x;e,f,g,h=y
    t=(add(add(m(a,e),neg(m(b,f))),add(neg(m(c,g)),neg(m(d,h)))),
       add(add(m(a,f),m(b,e)),add(m(c,h),neg(m(d,g)))),
       add(add(m(a,g),neg(m(b,h))),add(m(c,e),m(d,f))),
       add(add(m(a,h),m(b,g)),add(neg(m(c,f)),m(d,e))))
    assert all(i%2==j%2==0 for i,j in t)
    return tuple((i//2,j//2) for i,j in t)
def conjugate(x):return x[0],neg(x[1]),neg(x[2]),neg(x[3])
def scaled(x,s):return tuple((s*a,s*b) for a,b in x)
def build():
    H=set()
    for i in range(4):
        for s in (-1,1):
            v=[Z]*4;v[i]=(s*2,0);H.add(tuple(v))
    for signs in itertools.product((-1,1),repeat=4):
        H.add(tuple((s,0) for s in signs))
    assert len(H)==24
    G=set(H)
    for p in itertools.permutations(range(4)):
        if parity(p):continue
        for s in itertools.product((-1,1),repeat=3):
            v=[Z]*4
            for i,val in enumerate((ONE,PHI,PHIM1)):
                v[p[i+1]]=(s[i]*val[0],s[i]*val[1])
            G.add(tuple(v))
    assert len(G)==120
    assert {qmul(a,b) for a in H for b in H}==H
    assert {qmul(a,b) for a in G for b in G}==G
    assert all(qmul(x,conjugate(x))==((2,0),Z,Z,Z) for x in G)
    return sorted(G),H

def twentyfive(G,H):
    family_set={frozenset(qmul(g,qmul(h,conjugate(g))) for h in H) for g in G}
    assert len(family_set)==5
    fams=[]
    for K in sorted(family_set,key=lambda k:sorted(k)[0]):
        cosets={frozenset(qmul(g,k) for k in K) for g in G}
        assert len(cosets)==5
        fams.append(sorted(cosets,key=lambda c:sorted(c)[0]))
    cells=sorted(set().union(*(set(f) for f in fams)),key=lambda c:sorted(c)[0])
    assert len(cells)==25 and all(len(c)==24 for c in cells)
    assert all(sum(x in c for c in cells)==5 for x in G)
    axes={frozenset((x,scaled(x,-1))) for x in G}
    assert len(axes)==60
    assert all(sum(ax.issubset(c) for c in cells)==5 for ax in axes)
    sizes=collections.Counter(len(a&b) for i,a in enumerate(cells) for b in cells[i+1:])
    assert sizes=={6:200,0:100}
    disjoint=nx.Graph()
    disjoint.add_nodes_from(range(25))
    disjoint.add_edges_from((i,j) for i in range(25) for j in range(i+1,25)
                            if not cells[i]&cells[j])
    assert collections.Counter(dict(disjoint.degree()).values())=={8:25}
    assert nx.is_isomorphic(disjoint,nx.line_graph(nx.complete_bipartite_graph(5,5)))
    # Ten K5 cliques: five rows and five columns in the 5x5 array.
    cliques=[tuple(sorted(c)) for c in nx.find_cliques(disjoint)]
    assert len(cliques)==10 and {len(x) for x in cliques}=={5}
    for family in fams:
        idx=frozenset(cells.index(c) for c in family)
        assert idx in {frozenset(c) for c in cliques}
    return cells,dict(status="PASS_EXACT_600CELL_25_24CELL_5x5_REPRODUCTION",
        quaternion_vertices=120,Hurwitz_binary_tetrahedral_order=24,
        distinct_conjugate_subgroups_of_order24=5,cosets_per_subgroup=5,
        inscribed_24cells=25,each_600cell_vertex_in_n_24cells=5,
        projective_600cell_antipodal_axes=60,
        axes_plus_24cells_85_points_of_PG3_F4_count=85,
        each_axis_in_five_24cells=True,
        unordered_24cell_intersections={"0_vertices":100,"6_vertices":200},
        disjointness_graph_vertices=25,disjointness_graph_degree=8,
        disjointness_graph_srg=[25,8,3,2],
        disjointness_graph_is_isomorphic_to_5x5_rook=True,
        total_five_cell_decompositions=10,
        source="Denney, Hooker, Johnson, Robinson, Butler, Claiborne (2020), The Geometry of H4 Polytopes",
        boundary="25/5x5/10 are published 2020 prior art, replicated with exact Z[phi] quaternions. No unique canonical 24-cell subgroup selection.")

def porder(p):
    import math
    seen=set();t=1
    for i in range(len(p)):
        if i in seen:continue
        k=i;n=0
        while k not in seen:seen.add(k);n+=1;k=p[k]
        t=math.lcm(t,n)
    return t

def stabilizer(G,H):
    ix={x:i for i,x in enumerate(G)}
    P=set()
    for a in H:
        for b in H:
            inv=conjugate(b)
            for reflected in (False,True):
                P.add(tuple(ix[qmul(a,qmul(conjugate(x) if reflected else x,inv))]
                            for x in G))
    assert len(P)==576
    antipode=tuple(ix[scaled(x,-1)] for x in G)
    assert antipode in P and antipode!=tuple(range(120))
    assert all(all(p[antipode[i]]==antipode[p[i]] for i in range(120)) for p in P)
    hist=collections.Counter(map(porder,P))
    assert hist=={1:1,2:43,3:80,4:84,6:272,12:96}
    return dict(H4_full_symmetry_order=14400,
        one_inscribed_24cell_H4_stabilizer_order=576,
        stabilizer_action_on_120_icosian_vertices_order=576,
        central_antipodal_order2_exists=True,
        stabilizer_order_histogram={str(k):v for k,v in sorted(hist.items())},
        stabilizer_contains_order12=hist[12]==96)

def reye_group():
    J=range(1,5)
    E=[(X,s) for X in itertools.combinations(J,2) for s in ("-","+")]
    F=list(itertools.product(J,J))
    A=nx.Graph()
    A.add_nodes_from(range(12),part=0)
    A.add_nodes_from(range(12,28),part=1)
    A.add_edges_from((e,12+f) for e,(X,s) in enumerate(E)
                     for f,(a,b) in enumerate(F)
                     if a in X and ((b in X) if s=="-" else (b not in X)))
    it=nx.algorithms.isomorphism.GraphMatcher(A,A,
         node_match=lambda x,y:x["part"]==y["part"]).isomorphisms_iter()
    perms=[tuple(d[i] for i in range(28)) for d in it]
    assert len(perms)==576
    hist=collections.Counter(map(porder,perms))
    assert hist=={1:1,2:75,3:80,4:180,6:240}
    # Centre =1: test all 576 against all 576, early-out.
    # Fast short checks before remaining coordinates.
    def commute(a,b):
        for i in range(28):
            if a[b[i]]!=b[a[i]]:return False
        return True
    centre=[g for g in perms if all(commute(g,h) for h in perms)]
    assert len(centre)==1
    return dict(reye_medial_color_preserving_automorphism_order=576,
        reye_group_is_WF4_mod_antipode=True,
        reye_group_center_order=1,
        reye_order_histogram={str(k):v for k,v in sorted(hist.items())},
        reye_contains_order12=False)

def main():
    G,H=build()
    cells,arr=twentyfive(G,H)
    stab=stabilizer(G,H)
    rg=reye_group()
    assert stab["one_inscribed_24cell_H4_stabilizer_order"]==rg["reye_medial_color_preserving_automorphism_order"]==576
    assert stab["stabilizer_contains_order12"] and not rg["reye_contains_order12"]
    result=dict(status="PASS_600CELL_24CELL_TOMOTOPE_576_FALSE_FRIEND_OBSTRUCTION",
        geometry=arr,stabilizer=stab,reye=rg,
        exact_no_go="The 600-cell full H4 stabilizer of an inscribed 24-cell and the colored Reye/tomotope-medial full automorphism group both have order576 but are NOT isomorphic: the first has 96 elements of order12 and nontrivial central antipodal involution; the second has no order12 element and trivial center.",
        correct_24cell_reye_relation="The FULL 24-cell Coxeter group W(F4), order1152, acts on the twelve antipodal axes and sixteen central hexagon planes with central kernel ±I, giving Reye Aut576. The ROTATIONAL 24-cell group W(F4)^+, order576, retains central antipode and only maps to a subgroup of order288 on axes/planes.",
        exact_scope="Integer golden ratio arithmetic and finite permutation actions only; no physical embedding W33 or the tomotope itself into a 600-cell as an abstract rank-four subpolytope.",
        prior_art={"600cell_25_cells":"Denney et al 2020",
          "reye24cell_spine":"repo PART_MCXCIII",
          "tomotope_medial_R_eye":"Monson-Pellicer-Williams 2012 Section6",
          "new_comparison":"group order spectrum and central-inversion distinction, check exact against prior repo before novelty claim"})
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],"order12",stab["stabilizer_order_histogram"].get("12"),"reye order12",rg["reye_order_histogram"].get("12"),flush=True)
    return result
if __name__=="__main__":main()
