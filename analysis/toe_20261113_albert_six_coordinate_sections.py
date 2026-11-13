#!/usr/bin/env python3
"""Exact coordinate-supported 6-dimensional totally cubic-null sections.

For a square-free 45-term cubic N, dN(u,v,-)=0 on a coordinate subspace
iff its coordinate set meets every cubic triple in <=1 point. Enumerate
all maximal such sets as cliques of the complement of the 2-section
hypergraph. This is an algebraic *analogue* of E6 ExFT section constraints,
not an EFT section without identifying the appropriate dual invariant.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261113_albert_six_coordinate_sections.json"

def main():
    can=json.loads((ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json").read_text(encoding="utf-8"))
    tr={tuple(sorted(map(int,x["triple"]))):(1 if int(x["sign"])%3==1 else -1)
        for x in can["solution"]["d_triples"]}
    assert len(tr)==45
    addr=json.loads((ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text())
    eh={int(k):tuple(map(int,v)) for k,v in addr["maps"]["e6id_to_current_H27_address"].items()}
    G=nx.Graph()
    G.add_nodes_from(range(27))
    for t in tr:
        G.add_edges_from(combinations(t,2))
    assert G.number_of_nodes()==27 and G.number_of_edges()==135
    assert set(dict(G.degree()).values())=={10}
    graph_complement=nx.complement(G)
    assert set(dict(graph_complement.degree()).values())=={16}
    cliques=[tuple(sorted(c)) for c in nx.find_cliques(graph_complement)]
    maxima=max(map(len,cliques))
    biggest=sorted(c for c in cliques if len(c)==maxima)
    assert maxima==6
    assert len(biggest)==72,len(biggest)
    assert len(set(biggest))==72
    for section in biggest:
        assert len(section)==6
        for tritangent in tr:
            assert len(set(section)&set(tritangent))<=1
        # This directly certifies d(u,v,z)=0 for u,v from section,
        # since every coefficient with two indices in section vanishes.
    # Every 6-section has 6 commuting coordinate derivatives according
    # to the 45-term cubic support, but not a preferred signature/metric.
    by_fibre=Counter(tuple(sum(eh[i][1]==b for i in sec) for b in range(3)) for sec in biggest)
    by_fibre_sorted=Counter(tuple(sorted((sum(eh[i][1]==b for i in sec) for b in range(3)))) for sec in biggest)
    intersect=Counter(len(set(a)&set(b)) for a,b in combinations(biggest,2))
    adjacency=nx.Graph()
    adjacency.add_nodes_from(range(len(biggest)))
    for i,j in combinations(range(len(biggest)),2):
        if len(set(biggest[i])&set(biggest[j]))==5:adjacency.add_edge(i,j)
    out={
      "schema":"toe.albert.45_term_coordinate_null_six_sections.v1",
      "status":"PASS_72_SIX_COORDINATE_BILINEAR_CUBIC_NULL_SECTIONS",
      "signed_cubic_triples":45,
      "27_2section_graph_degree":10,
      "pair_edges":G.number_of_edges(),
      "complement_graph_degree":16,
      "maximal_clique_sizes":dict(Counter(str(len(c)) for c in cliques)),
      "maximum_coordinate_supported_cubic_null_dimension":maxima,
      "number_of_maximal_six_coordinate_sections":len(biggest),
      "all_six_sections":[list(c) for c in biggest],
      "b_fibre_section_composition":{str(k):v for k,v in sorted(by_fibre.items())},
      "unordered_b_fibre_composition":{str(k):v for k,v in sorted(by_fibre_sorted.items())},
      "six_section_pair_intersection_histogram":{str(k):v for k,v in sorted(intersect.items())},
      "five_coordinate_overlap_adjacency_edges":adjacency.number_of_edges(),
      "gradient_bilinear_test":"For all u,v supported on a listed sixer and arbitrary z, the polarized tensor T(u,v,z)=0 because every triple contains at most one support index",
      "scope":"Exact support bound for sections SPANNED BY COORDINATE AXES only. Does not prove global maximal dimension among arbitrary linear subspaces, does not prove actual exceptional-field-theory upper-index section condition or derive Lorentz spacetime.",
      "literature_analogy":"Hohm-Samtleben E6(6) exceptional field theory uses a 27-component extended internal coordinate and a covariant section constraint admitting six ordinary internal directions."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:out[k] for k in ["status","maximal_clique_sizes","number_of_maximal_six_coordinate_sections","unordered_b_fibre_composition","six_section_pair_intersection_histogram"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
