#!/usr/bin/env python3
"""Enumerate ALL 630 pairs of distinct cubic-preserving compact
E6 quarter-turn root packet links on F3^3 and classify their exact
non-flat Wilson plaquettes, integer Wilson action, and preserved
maximal 5D versus 6D coordinate sections.

This is an explicit negative/positive search for DYNAMICAL section
selection in a defined toy Wilson-action ensemble. Stabilizing a
coordinate section is frame dependent; no claim of gauge-invariant
unique spacetime dimension without specifying the covariant section.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter,defaultdict
import json,sys
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261114_e6_Wilson_630_section_stability_census.json"
def main():
    _,triads,_,_,roots=R.load()
    _,Ks=R.pack_roots(roots)
    I=np.eye(27,dtype=np.int64)
    gates=[I+K+K@K for K in Ks]
    for U in gates:assert np.array_equal(U@U.T,I)
    G=nx.Graph();G.add_nodes_from(range(27))
    for t in triads:G.add_edges_from(combinations(t,2))
    sections={5:[],6:[]}
    for s in nx.find_cliques(nx.complement(G)):
        sections[len(s)].append(frozenset(s))
    assert (len(sections[5]),len(sections[6]))==(216,72)
    records=[]
    for i,j in combinations(range(36),2):
        U,V=gates[i],gates[j]
        W=U@V@U.T@V.T
        assert np.array_equal(W@W.T,I)
        moved=not np.array_equal(W,I)
        p=np.argmax(abs(W),axis=0)
        assert len(set(p))==27
        counts={str(size):sum(frozenset(int(p[k]) for k in s)==s for s in sections[size])
                for size in (5,6)}
        tr=int(np.trace(W))
        # Wilson action S_W = 27 - Re Tr W, nonnegative for orthogonal W
        action=27-tr
        assert action>=0
        records.append({"id":[i,j],"nonflat":moved,"trace":tr,
                        "plaquette_action":action,"fixed_sections":counts})
    assert len(records)==630
    nonflat=[r for r in records if r["nonflat"]]
    assert nonflat
    signature=Counter((r["plaquette_action"],r["fixed_sections"]["5"],r["fixed_sections"]["6"]) for r in records)
    stable5=[r for r in nonflat if r["fixed_sections"]["5"] and not r["fixed_sections"]["6"]]
    stable6=[r for r in nonflat if r["fixed_sections"]["6"] and not r["fixed_sections"]["5"]]
    stableboth=[r for r in nonflat if r["fixed_sections"]["5"] and r["fixed_sections"]["6"]]
    stabnone=[r for r in nonflat if not r["fixed_sections"]["5"] and not r["fixed_sections"]["6"]]
    trmin=min(r["plaquette_action"] for r in nonflat)
    minimal=[r for r in nonflat if r["plaquette_action"]==trmin]
    if stable5:best5=min(r["plaquette_action"] for r in stable5)
    else:best5=None
    if stable6:best6=min(r["plaquette_action"] for r in stable6)
    else:best6=None
    res={"status":"PASS_EXHAUSTIVE_630_PAIR_ROOT_LINK_WILSON_SECTION_CENSUS",
         "root_compact_quarter_turn_gates":36,
         "unordered_link_pairs":630,
         "nonflat_count":len(nonflat),
         "flat_count":630-len(nonflat),
         "distinct_action_fixed_section_signatures":[{"action":x,"five":f,"six":s,"count":n}
             for (x,f,s),n in sorted(signature.items())],
         "nonflat_both_types":len(stableboth),
         "nonflat_only_five":len(stable5),
         "nonflat_only_six":len(stable6),
         "nonflat_neither":len(stabnone),
         "smallest_nonflat_wilson_action":trmin,
         "smallest_nonflat_examples":minimal[:12],
         "best_nonflat_action_only_five":best5,
         "best_nonflat_action_only_six":best6,
         "lowest_action_only_five_example":next((r for r in stable5 if r["plaquette_action"]==best5),None),
         "lowest_action_only_six_example":next((r for r in stable6 if r["plaquette_action"]==best6),None),
         "scope":"Only constant-link plaquettes from all 36 quarter-turn packet gates. The Wilson plaquette is gauge covariant and its trace is gauge invariant, but counting coordinate-aligned preserved sections is gauge-frame dependent unless sections are transformed too. A single-plaquette Wilson action does not establish a stable dynamical vacuum or select physical dimensions."}
    OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:res[k] for k in ("status","nonflat_count","flat_count","nonflat_both_types","nonflat_only_five","nonflat_only_six","nonflat_neither","smallest_nonflat_wilson_action","best_nonflat_action_only_five","best_nonflat_action_only_six")},indent=2),flush=True)
    return res
if __name__=="__main__":main()
