#!/usr/bin/env python3
"""Independent 45-triad hypergraph audit of E6's three nine-coordinate
H27-address fibres. Verify determinant support and trace tensor support
WITHOUT asserting the fixed addresses equal canonical 3x3 matrix blocks.
"""
import itertools, json
from pathlib import Path
from collections import Counter
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261113_e6_nine_sector_trace_hypergraph.json"
can=json.loads((ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json").read_text())
bridge=json.loads((ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text())
eh={int(i):tuple(map(int,h)) for i,h in bridge["maps"]["e6id_to_current_H27_address"].items()}
terms=[tuple(map(int,x["triple"])) for x in can["solution"]["d_triples"]]
sectors={b:{i for i,h in eh.items() if h[1]==b} for b in range(3)}
def incidence(points,triples):
    G=nx.Graph()
    for p in points:G.add_node(("p",p),side=0)
    for j,t in enumerate(triples):
        G.add_node(("t",j),side=1)
        for p in t:G.add_edge(("p",p),("t",j))
    return G
def nm(a,b):return a["side"]==b["side"]
def main():
    profiles=[]
    model_points=set(range(9))
    canonical_det=[tuple(3*i+perm[i] for i in range(3))
                   for perm in itertools.permutations(range(3))]
    canonical=incidence(model_points,canonical_det)
    for b in range(3):
        pts=sectors[b]
        internal=[tr for tr in terms if set(tr)<=pts]
        assert len(pts)==9 and len(internal)==6
        G=incidence(pts,internal)
        matcher=nx.algorithms.isomorphism.GraphMatcher(G,canonical,node_match=nm)
        assert matcher.is_isomorphic()
        m=next(matcher.isomorphisms_iter())
        mapping={str(p):m[("p",p)][1] for p in pts}
        profiles.append({"b":b,"internal_triples":len(internal),
                         "is_det_3x3_support":True,"one_matrix_coordinate_map":mapping,
                         "degrees":dict(Counter(dict(G.degree()).values()))})
    cross=[tr for tr in terms if len({eh[i][1] for i in tr})==3]
    assert len(cross)==27
    cross_pair=[]
    for a,b in ((0,1),(1,2),(0,2)):
        G=nx.Graph()
        for p in sectors[a]|sectors[b]:G.add_node(p)
        for tr in cross:
            i=next(x for x in tr if eh[x][1]==a)
            j=next(x for x in tr if eh[x][1]==b)
            G.add_edge(i,j)
        comps=[G.subgraph(c) for c in nx.connected_components(G)]
        assert len(comps)==3
        assert all(len(z.nodes())==6 and len(z.edges())==9 and
                   nx.is_bipartite(z) and
                   all(z.degree(v)==3 for v in z) for z in comps)
        cross_pair.append({"b_pair":[a,b],"bipartite_connected_components":[6,6,6],
                           "component_edges":[9,9,9],"pairwise_projection_is_3K33":True})
    # Each pair from distinct blocks occurs in at most one cross-triad.
    for a,b in ((0,1),(1,2),(0,2)):
        pairs=[tuple(sorted((next(x for x in t if eh[x][1]==a),
                            next(x for x in t if eh[x][1]==b)))) for t in cross]
        assert len(set(pairs))==27
    out={"status":"PASS_THREE_DETERMINANT_SUPPORTS_AND_TRACE_PAIR_PROJECTIONS",
         "total_signed_cubic_support_terms":45,
         "determinant_like_hypergraphs":profiles,
         "trace_cross_terms":27,
         "cross_sector_bipartite_projections":cross_pair,
         "no_claim_about_exact_signed_coordinate_equivalence":True,
         "next_proof_needed":"Choose compatible bases for all three 9-sets, and solve the signs/phases of the 27 cross terms to prove a simultaneous coordinate equivalence to det A + det B + det C - tr ABC."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":out["status"],"internal":[p["is_det_3x3_support"] for p in profiles],
                      "cross_3K33":[p["pairwise_projection_is_3K33"] for p in cross_pair]},indent=2))
    return out
if __name__=="__main__":main()
