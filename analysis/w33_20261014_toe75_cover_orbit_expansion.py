"""TOE75 exhaustive distinct PGSp-orbit classification of all 20 newly
adjacent exact 20-octagon covers, extending certified seven-orbit baseline.

This classifies CANDIDATE covers only: it does not enumerate the complete
set of all exact covers or the complete 3**80 pairing Hamiltonian.
The separate TOE75 structural test independently proves all 20 candidates
lie outside each of the previous seven full-group orbits.
"""
from __future__ import annotations
import collections,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe74_quantum_neighbors import certificate as neighborhoods
from w33_20261014_toe69_five_fronts import octagons
from w33_pass1081_1086_core import (
    build_w33,transvection_perm,outer_similitude_perm,line_perm)

def certificate():
    prev=neighborhoods()
    seven={tuple(x) for x in prev["seven_seed_cover_cycle_lists"]}
    cand=sorted({
       tuple(cv)
       for row in prev["neighborhood_summary"]
       for cv in row["local_neighbor_cover_identifiers"]}-seven)
    assert len(cand)==20
    pts,pidx,lines,lidx,_,_,_,flags,flagidx=build_w33()
    ed,adj,cycles=octagons()
    lookup={tuple(sorted(c)):i for i,c in enumerate(cycles)}
    def action(per):
        lp=line_perm(per,lines,lidx)
        eperm=tuple(flagidx[(per[p],lp[l])] for p,l in flags)
        return tuple(lookup[tuple(sorted(eperm[e] for e in c))]
                     for c in cycles)
    gens=[action(transvection_perm(pts[i],pts,pidx))
          for i in (0,1,2,4,8,15)]
    gens.append(action(outer_similitude_perm(pts,pidx)))
    candidates=set(cand)
    new_orbits=[]
    while candidates:
        target=min(candidates)
        seen={target};todo=collections.deque([target])
        hits={target}
        while todo:
            state=todo.popleft()
            for gg in gens:
                other=tuple(sorted(gg[e] for e in state))
                if other not in seen:
                    seen.add(other);todo.append(other)
                    if other in candidates:hits.add(other)
        n=len(seen)
        assert 51840%n==0 and n>0
        candidates-=hits
        new_orbits.append({
           "seed_cover_cycle_ids":list(target),
           "orbit_size":n,
           "stabilizer_order_in_PGSp":51840//n,
           "number_of_20_new_neighbor_candidates_in_this_orbit":len(hits),
           "new_neighbor_indices_in_original_20_list":[cand.index(q)
                                        for q in sorted(hits)]})
    assert sum(r["number_of_20_new_neighbor_candidates_in_this_orbit"]
               for r in new_orbits)==20
    assert len(candidates)==0
    total_new=sum(z["orbit_size"] for z in new_orbits)
    return {
      "status":"PASS_TOE75_COMPLETE_ORBIT_CLASSIFICATION_OF_20_NEW_NEIGHBORS",
      "original_certified_distinct_full_group_orbits":7,
      "original_certified_distinct_cover_states":362880,
      "separately_certified_20_candidates_outside_seven_old_orbits":True,
      "number_of_new_candidates":20,
      "new_distinct_candidate_orbits":len(new_orbits),
      "new_orbits":new_orbits,
      "total_new_exact_cover_configs_from_extra_orbits":total_new,
      "proved_total_distinct_cover_orbits_at_least":7+len(new_orbits),
      "proved_total_distinct_20_cycle_cover_states_at_least":362880+total_new,
      "unclassified_candidates_from_initial_20":0,
      "rigorous_group_method":"Full orbit BFS on native octagon 1620-point permutation representation induced from six symplectic transvections plus outer similitude. Orbits partition the 20 candidate covers; all distinct orbit sizes divide group order 51840. Baseline independent TOE75 structural certificate establishes none of the 20 lie in the previous seven orbits.",
      "limitation":"All 20 neighboring covers classified, NOT the entire W33 20-loop exact-cover state space. Additional longer-distance ground covers may form further PGSp orbits. No emergent spacetime or physical TOE."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe75_all_new_neighbor_orbits.json").write_text(
        json.dumps(c,indent=2)+"\n")
    print(c["status"],"extra",c["new_distinct_candidate_orbits"],
       "total_orbits",c["proved_total_distinct_cover_orbits_at_least"],
       "total_states",c["proved_total_distinct_20_cycle_cover_states_at_least"])
