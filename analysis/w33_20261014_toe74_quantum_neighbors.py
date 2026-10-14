"""TOE74: actual second-order two-local-flip neighborhoods of ALL seven seeds.

Unlike TOE73's six-matching star COMPRESSION, compute every one of
12640 possible two-vertex changes from each one of seven known exact
20-octagon pairing configurations. No group-orbit classification of
new boundary states is claimed without a separate coset audit.
"""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe71_quantum_pairing import geometry,loop_count
from w33_20261014_toe69_five_fronts import octagons,COVER

def build_cover(config,ed,adj,opts,lookup):
    through={}
    for v,i in enumerate(config):
        for a,b in opts[v][i]:
            through[v,a]=b;through[v,b]=a
    seen=set();counter=collections.Counter()
    for v in range(80):
        for neighbor,e,s in adj[v]:
            if (v,e) in seen:continue
            u=v;enter=e;visited=[]
            while (u,enter) not in seen:
                seen.add((u,enter));visited.append(enter)
                leave=through[u,enter]
                a,b=ed[leave];u=b if a==u else a;enter=leave
            assert len(visited)==8
            counter[lookup[tuple(sorted(visited))]]+=1
    assert len(seen)==320 and len(counter)==20
    assert all(x==2 for x in counter.values())
    return tuple(sorted(counter))

def all_pair_moves(config,ed,adj,opts,lookup,with_covers=True):
    hist=collections.Counter();moves=[]
    for a,b in itertools.combinations(range(80),2):
        for x in range(3):
            if x==config[a]:continue
            for y in range(3):
                if y==config[b]:continue
                cfg=config.copy();cfg[a]=x;cfg[b]=y
                loops=loop_count(cfg,ed,adj,opts)
                hist[loops]+=1
                if loops==20:
                    cv=build_cover(cfg,ed,adj,opts,lookup)
                    moves.append((a,b,x,y,cv))
    assert sum(hist.values())==12640
    assert sum(1 for a,b,x,y,cv in moves)==hist[20]
    return hist,moves

def certificate():
    ed,adj,opts,base=geometry()
    _,_,cycles=octagons()
    lookup={tuple(sorted(c)):i for i,c in enumerate(cycles)}
    start=tuple(sorted(COVER))
    assert build_cover(base,ed,adj,opts,lookup)==start
    hist,moves=all_pair_moves(base,ed,adj,opts,lookup)
    assert hist=={18:12628,19:6,20:6}
    first_targets=[m[4] for m in moves]
    assert len(set(first_targets))==6
    seeds=[base]
    for a,b,x,y,target in moves:
        state=base.copy();state[a]=x;state[b]=y
        assert build_cover(state,ed,adj,opts,lookup)==target
        seeds.append(state)
    seed_covers=[build_cover(c,ed,adj,opts,lookup) for c in seeds]
    assert len(set(seed_covers))==7
    summaries=[];all_second=set()
    for i,state in enumerate(seeds):
        h,nbrs=all_pair_moves(state,ed,adj,opts,lookup)
        keys=[x[4] for x in nbrs]
        assert len(set(keys))==len(keys)
        all_second.update(keys)
        incidence={str(j):int(seed_covers[j] in keys)
                   for j in range(7) if j!=i}
        if i:
            assert incidence["0"]==1
        else:
            assert sum(incidence.values())==6
        summaries.append({
          "seed_index":i,
          "local_20_loop_degree":h[20],
          "local_19_loop_changes":h[19],
          "local_18_loop_changes":h[18],
          "links_to_other_six_given_representatives":incidence,
          "local_neighbor_cover_identifiers":[list(cv) for cv in keys]})
    # The 7 seed set is not claimed closed. This calculation explicitly
    # exhibits additional covers reachable in another one or two pair moves.
    outside=all_second-set(seed_covers)
    return {
      "status":"PASS_TOE74_ALL_SEVEN_SEED_TWO_FLIP_NEIGHBORHOODS",
      "native_vertices_edges":[80,160],
      "known_distinct_PGSp_orbits":7,
      "tested_pair_flips_per_seed":12640,
      "total_pair_flip_tests":7*12640,
      "seven_seed_cover_cycle_lists":[list(c) for c in seed_covers],
      "neighborhood_summary":summaries,
      "distinct_second_order_neighbor_covers_over_seven_seeds":len(all_second),
      "distinct_new_covers_outside_seven_representatives":len(outside),
      "compressed_star_is_full_induced_seven_orbit_graph":False,
      "limitation":"This surveys two-flip neighborhoods of SEVEN chosen orbit representatives, not every member of all 7*51840 covers. Being outside the seven SEED states does not mean outside the seven symmetry ORBITS. Further group-membership testing is required before claiming new inequivalent orbits."
    }
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe74_quantum_neighbors.json").write_text(
        json.dumps(c,indent=2)+"\n")
    print(c["status"],[(z["seed_index"],z["local_20_loop_degree"]) for z in c["neighborhood_summary"]])
