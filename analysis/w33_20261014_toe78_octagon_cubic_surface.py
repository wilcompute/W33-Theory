"""TOE78: independent E6 cubic-surface/45 tritangent realization on the
27 native W33 octagons fixed as a set by the two-theta-chord stabilizer.

Proves the UNIQUE 216-invariant SRG(27,10,1,5) from all invariant
unordered-pair orbitals is isomorphic to the independently built
27-line cubic-surface incidence graph. The 45 triangles are the
tritangent planes. Reports the 36 double-sixes too.

The new geometric carrier is an abstract graph-isomorphic model;
the isomorphism is not a canonical physics field identification or
a proven equivalence to the trinification H27 operator representation.
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_H27_shared_octagon_group import certificate as native_certificate
from w33_pass4992_4999_common import Q6

def independent_cubic_geometry():
    vec=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vec if Q6(v)==0]
    qp=[sum(bit<<i for i,bit in enumerate(v)) for v in sing]
    p27=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    l27=[tuple(i for i,P in enumerate(p27) if x in P) for x in qp]
    assert len(p27)==45 and len(l27)==27
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(l27[i])&set(l27[j]):G.add_edge(i,j)
    trit=sorted(t for t in itertools.combinations(range(27),3)
                if all(G.has_edge(u,v) for u,v in itertools.combinations(t,2)))
    assert G.number_of_edges()==135 and len(trit)==45
    c6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6]
    doubles=set()
    for X,Y in itertools.combinations(c6,2):
        if X&Y:continue
        sub=G.subgraph(X|Y)
        if sub.number_of_edges()==30 and set(dict(sub.degree()).values())=={5} and nx.is_bipartite(sub):
            doubles.add(frozenset(X|Y))
    assert len(doubles)==36
    return G,trit,doubles

def certificate():
    native=native_certificate()
    assert native["induced_faithful_permutation_group_order"]==216
    assert native["pair_stabilizer_is_semidirect_H27_by_D8"]
    assert native["native_216_invariant_cubic_surface_intersection_srg_count"]==1
    witness=native["native_216_invariant_cubic_surface_intersection_srg_candidates"][0]
    Edges={tuple(sorted(e)) for e in witness["graph_edges"]}
    assert len(Edges)==135 and witness["triangle_tritangent_count"]==45
    G=nx.Graph();G.add_nodes_from(range(27));G.add_edges_from(Edges)
    assert set(dict(G.degree()).values())=={10}
    e6,tri,ds=independent_cubic_geometry()
    matcher=nx.algorithms.isomorphism.GraphMatcher(G,e6)
    iso=next(matcher.isomorphisms_iter(),None)
    assert iso is not None and len(set(iso.values()))==27
    native_tri=sorted(x for x in itertools.combinations(range(27),3)
                      if all(G.has_edge(u,v) for u,v in itertools.combinations(x,2)))
    assert len(native_tri)==45
    mapped={tuple(sorted(iso[i] for i in T)) for T in native_tri}
    assert mapped==set(tri)
    native_ds={frozenset(next(k for k,v in iso.items() if v==j) for j in D) for D in ds}
    assert len(native_ds)==36
    eig=np.linalg.eigvalsh(nx.to_numpy_array(G,nodelist=list(range(27))))
    assert np.max(abs(eig-np.sort(np.array([-5.]*6+[1.]*20+[10.]))))<1e-8
    rows=[]
    for i,j in itertools.combinations(range(27),2):
        cn=len(set(G[i])&set(G[j]))
        assert cn==(1 if G.has_edge(i,j) else 5)
    return {
      "status":"PASS_TOE78_NATIVE_OCTAGON_H27_D8_CUBIC_SURFACE_GRAPH",
      "native_octagon_count":27,
      "native_216_undirected_pair_orbital_valencies":native["unordered_pair_orbit_valencies"],
      "native_216_invariant_degree10_candidates_tested":native["invariant_degree10_graph_candidate_subsets_tested"],
      "unique_216_invariant_SRG_27_10_1_5":True,
      "selected_pair_orbital_indices":witness["selected_pair_orbit_indices"],
      "native_SRG_edges":len(Edges),
      "native_cubic_tritangents":len(native_tri),
      "native_cubic_double_sixes":len(native_ds),
      "native_cubic_graph_adjacency_spectrum":{"10":1,"1":20,"-5":6},
      "native_to_independent_E6_cubic_line_index_isomorphism":[int(iso[i]) for i in range(27)],
      "native_tritangent_octagon_triples":[list(z) for z in native_tri],
      "native_SRG_adjacency_edges":[list(z) for z in sorted(Edges)],
      "native_216_group_is_H27_by_D8":True,
      "antiunitary_group_boundary":{
        "D8_elements_inverting_H27_center":native["dihedral_reflections_inverting_Heisenberg_center"],
        "D8_elements_preserving_H27_center":native["dihedral_elements_preserving_Heisenberg_center"],
        "nontrivial_complex_central_character_unitary_obstruction":"A unitary U fixes omega I by conjugation, so cannot realize any automorphism z->z^-1 on a fixed Schrodinger H27 representation. Antiunitary K conjugates omega to omega². Distinguish 27-permutation address space from the 3D quantum operator representation."},
      "proof":"Enumerate all 216 pair-stabilizer permutations on 27 shared W33 octagons and all 351 unordered pairs. The five invariant pair-orbit valencies sum to 26; exactly one degree-10 union is SRG(27,10,1,5), verified by all 351 common-neighbor counts. Independently construct the cubic 27-line graph from 45 singular F2^6 triples and check an explicit graph isomorphism, 45 preserved triangles and 36 double-sixes. The normal regular H27 action and D8 action are already group-law verified in the TOE77 producer.",
      "scope":"Exact finite incidence-and-group embedding into cubic-surface 27-line combinatorics. Not a canonical E6 gauge-field representation, particle-mass equation, chiral operator algebra, or physical TOE."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe78_octagon_cubic_surface.json").write_text(
       json.dumps(c,indent=2)+"\n")
    print(c["status"],"PAIR_ORBITS",c["native_216_undirected_pair_orbital_valencies"],
          "SELECTED",c["selected_pair_orbital_indices"],
          "TRITANGENTS",c["native_cubic_tritangents"],
          "DOUBLE_SIX",c["native_cubic_double_sixes"])
