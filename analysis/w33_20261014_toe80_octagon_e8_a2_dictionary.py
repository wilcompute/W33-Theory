"""TOE80 native W33 octagon -> E8-derived E6 27 weight x A2 3 phase
dictionary. This deliberately reuses the independent, older exact
Part MCCCXC E8/E6/A2 construction rather than silently rediscovering it.

For all four E8 E6+A2 coordinate choices and both 81-root matter sectors,
construct an explicit (noncanonical!) graph isomorphism from the 27
native W33 octagons to the 27 projected E6 weights. Verify the COMPLETE
27x27 Gram matrix over Fraction, and show that nonadjacent octagon
weight differences give exactly the independent 72 E6 roots.
Each native octagon address carries precisely three A2 phase lifts.

Physical caveat: a graph isomorphism has 51840 Weyl gauge choices
(and 1920 with a chosen anchor). It cannot on its own be called a
canonical particle/field identification or a predicted physical mass.
"""
from __future__ import annotations
from collections import defaultdict,Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json,sys
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe80_native_octagon_e6_roots import certificate as native
from w33_e6_minuscule_27_a2_phase_factorization import project_to_e6
from w33_e8_e6_a2_coordinate_decomposition import sectorize_by_coordinate,block_pair
from w33_tetracode_e8_root_system_bridge import inner,subtract,scale

def certificate():
    c=native()
    Q=c["native_projector_integer_numerator_27x27"]
    assert len(Q)==27
    G=nx.Graph()
    G.add_nodes_from(range(27))
    for i,j in combinations(range(27),2):
        if Q[i][j]==-2:G.add_edge(i,j)
    assert G.number_of_edges()==135
    assert set(dict(G.degree()).values())=={10}
    rows=[]
    for coord in range(4):
        sectors=sectorize_by_coordinate(coord)
        e6roots=set(sectors["E6_zero_coordinate_roots"])
        assert len(e6roots)==72
        sector_sets=[]
        for key in ("matter_81_coset_1","matter_81_coset_2"):
            roots=sectors[key]
            assert len(roots)==81
            by_weight=defaultdict(set)
            for r in roots:
                w=project_to_e6(r,coord)
                by_weight[w].add(block_pair(r,coord))
            weights=sorted(by_weight)
            assert len(weights)==27
            assert set(map(len,by_weight.values()))=={3}
            E=nx.Graph()
            E.add_nodes_from(range(27))
            for i,j in combinations(range(27),2):
                if inner(weights[i],weights[j])==Fraction(-2,3):
                    E.add_edge(i,j)
            assert E.number_of_edges()==135
            matcher=nx.algorithms.isomorphism.GraphMatcher(G,E)
            mapping=next(matcher.isomorphisms_iter(),None)
            assert mapping is not None and len(set(mapping.values()))==27
            # Pull E8-derived Gram through exact W33 octagon address map.
            for i in range(27):
                for j in range(27):
                    assert inner(weights[mapping[i]],weights[mapping[j]])==Fraction(Q[i][j],3), (coord,key,i,j)
            # The E8 independent 72-root set coincides EXACTLY
            # with all nonadjacent native-octagon weight differences.
            derived=set()
            for i,j in combinations(range(27),2):
                if G.has_edge(i,j):continue
                a=weights[mapping[i]]
                b=weights[mapping[j]]
                diff=subtract(a,b)
                assert inner(diff,diff)==Fraction(2)
                derived.add(diff)
                derived.add(scale(Fraction(-1),diff))
            assert len(derived)==72
            assert derived==e6roots
            # Each octagon has three exact, distinct A2 lifts; the A2
            # phase labels are the original unmodified E8 root pair.
            octagon_to_weight=[mapping[i] for i in range(27)]
            octagon_phase_lifts=[
              [[str(x) for x in phase] for phase in sorted(by_weight[weights[mapping[i]]])]
              for i in range(27)]
            assert all(len(row)==3 for row in octagon_phase_lifts)
            assert len({tuple(x) for row in octagon_phase_lifts for x in row})==3
            rows.append({
              "E8_A2_coordinate":coord,
              "matter_81_sector":key,
              "exact_E8_roots":len(roots),
              "native_octagon_addresses":27,
              "e6_root_differences_matching_independent_E8_roots":72,
              "native_octagon_to_E8_projected_weight_index":octagon_to_weight,
              "three_A2_phases_per_octagon":octagon_phase_lifts,
              "full_27x27_rational_Gram_equal":True,
              "all_72_E6_roots_match_as_exact_Fraction_vectors":True
            })
            sector_sets.append(set(weights))
        # Dual minuscule branches should be negatives in this fixed
        # E6+A2 embedding. If they fail, record instead of inventing.
        dual=(sector_sets[0]=={scale(Fraction(-1),w) for w in sector_sets[1]})
        rows[-2]["dual_matter_sector_projected_weights_opposite"]=dual
        rows[-1]["dual_matter_sector_projected_weights_opposite"]=dual
    assert len(rows)==8
    assert all(r["full_27x27_rational_Gram_equal"] for r in rows)
    return {
      "status":"PASS_TOE80_EIGHT_E8_MATTER_TO_NATIVE_W33_OCTAGON_DICTIONARIES",
      "native_W33_octagon_carrier":27,
      "E8_E6_A2_coordinate_choices":4,
      "matter_sector_branches_per_choice":2,
      "verified_independent_81_root_sectors":len(rows),
      "total_E8_matter_root_sector_memberships":sum(x["exact_E8_roots"] for x in rows),
      "exact_E6_weights_per_sector":27,
      "exact_A2_phase_lifts_per_native_octagon":3,
      "E6_roots_recovered_from_nonadjacent_native_octagon_differences":72,
      "all_729_fraction_Gram_entries_per_sector_match":True,
      "natural_Weyl_graph_isomorphism_gauge_choices_unanchored":51840,
      "natural_Weyl_graph_isomorphism_gauge_choices_one_address_anchor":1920,
      "each_coordinate_sector_noncanonical_address_maps":rows,
      "critical_limit":"Eight exact finite dictionaries, one per choice of four A2 coordinates and two 81-root matter sectors. The labels and 3-phase fibers are gauge choices and representations, not physical particles, spinors, mass eigenstates or canonical time bins. E8-to-E6+A2 is previously established in this repository (Part MCCCXC); new work is the exact interface to 27 NATIVE W33 octagon addresses."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe80_octagon_e8_a2_dictionaries.json").write_text(
        json.dumps(c,indent=2)+"\n")
    print(c["status"],"branches",c["verified_independent_81_root_sectors"],
          "dual",[(x["E8_A2_coordinate"],x["dual_matter_sector_projected_weights_opposite"]) for x in c["each_coordinate_sector_noncanonical_address_maps"][::2]])
