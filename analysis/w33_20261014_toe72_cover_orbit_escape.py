"""TOE72: classify six second-order 20-loop cover moves under full PGSp.

Exact finite group permutations only. Seven distinct full PGSp orbits of size
51840 each are exhibited (one initial + six neighboring). A pair-flip
tunneling move therefore NEVER connects states inside the initial orbit;
it connects that orbit to six *different* cover orbits. This corrects a
possible erroneous restriction of the effective dynamics to one orbit.
"""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1081_1086_core import build_w33,transvection_perm,line_perm,outer_similitude_perm
from w33_20261014_toe69_five_fronts import octagons,COVER
from w33_20261014_toe71_quantum_pairing import geometry,loop_count

def certificate():
    pts,idx,lines,lidx,_,_,_,flags,flagidx=build_w33()
    ed,adj,cycles=octagons()
    _,_,choices,base=geometry()
    lookup={tuple(sorted(c)):i for i,c in enumerate(cycles)}
    def to_cover(config):
        router={}
        for v,k in enumerate(config):
            for a,b in choices[v][k]:
                router[v,a]=b;router[v,b]=a
        seen=set();found=[]
        for v in range(80):
            for _,edge,_ in adj[v]:
                if (v,edge) in seen:continue
                u=v;incoming=edge;chain=[]
                while (u,incoming) not in seen:
                    seen.add((u,incoming));chain.append(incoming)
                    nxt=router[u,incoming]
                    a,b=ed[nxt];u=b if a==u else a;incoming=nxt
                assert len(chain)==8
                found.append(lookup[tuple(sorted(chain))])
        counts=collections.Counter(found)
        assert len(seen)==320 and len(counts)==20 and set(counts.values())=={2}
        return tuple(sorted(counts))
    seed=tuple(sorted(COVER))
    assert to_cover(base)==seed and loop_count(base,ed,adj,choices)==20
    neighbors=[];changes=[]
    histogram=collections.Counter()
    for a,b in itertools.combinations(range(80),2):
        for ka in range(3):
            if ka==base[a]:continue
            for kb in range(3):
                if kb==base[b]:continue
                cfg=base.copy();cfg[a]=ka;cfg[b]=kb
                n=loop_count(cfg,ed,adj,choices)
                histogram[n]+=1
                if n==20:
                    neighbors.append(to_cover(cfg));changes.append([a,b,ka,kb])
    assert histogram=={18:12628,19:6,20:6}
    assert len(neighbors)==len(set(neighbors))==6
    def action(per):
        lp=line_perm(per,lines,lidx)
        ep=tuple(flagidx[(per[p],lp[l])] for p,l in flags)
        return tuple(lookup[tuple(sorted(ep[e] for e in c))] for c in cycles)
    generators=[action(transvection_perm(pts[i],pts,idx))
                for i in (0,1,2,4,8,15)]
    outer=action(outer_similitude_perm(pts,idx))
    def image(g,c):
        return tuple(sorted(g[i] for i in c))
    # Transitively transport the tuple (cover, six neighbors) through PSp.
    # Each cover in the original orbit has trivial stabilizer, so the
    # six recorded neighboring images are uniquely associated to it.
    start=(seed,*neighbors)
    known={seed};queue=collections.deque([start]);family=[start]
    while queue:
        batch=queue.popleft()
        for g in generators:
            nxt=tuple(image(g,c) for c in batch)
            if nxt[0] not in known:
                known.add(nxt[0]);queue.append(nxt);family.append(nxt)
    assert len(known)==25920
    external=[tuple(image(outer,c) for c in batch) for batch in family]
    assert all(row[0] not in known for row in external)
    expanded=known|{row[0] for row in external}
    assert len(expanded)==51840
    family.extend(external)
    assert all(c not in expanded for batch in family for c in batch[1:])
    # Independently classify all six neighboring covers under PGSp.
    groups=generators+[outer]
    labels=[]
    for j,target in enumerate(neighbors):
        seen={target};q=collections.deque([target])
        while q:
            state=q.popleft()
            for g in groups:
                other=image(g,state)
                if other not in seen:
                    seen.add(other);q.append(other)
        assert len(seen)==51840
        labels.append({"neighbor":j,"orbit_size":len(seen),
                       "other_neighbor_indices":[i for i,c in enumerate(neighbors)
                                                 if c in seen],
                       "intersects_original_orbit":bool(seen.intersection(expanded))})
    assert all(r["other_neighbor_indices"]==[r["neighbor"]] for r in labels)
    assert not any(r["intersects_original_orbit"] for r in labels)
    # Every original-orbit state has six two-flip neighbors; one in each
    # of six distinct additional full-group orbits. None are within it.
    return {
      "status":"PASS_TOE72_SEVEN_DISTINCT_COVER_ORBITS",
      "original_cover_size_PSp":25920,
      "original_cover_size_PGSp":51840,
      "original_orbit_trivial_stabilizer":True,
      "all_two_vertex_pair_flip_histogram":{str(k):v for k,v in histogram.items()},
      "six_seed_double_flips":changes,
      "each_of_six_neighbor_covers_distinct":True,
      "neighbor_orbit_classification":labels,
      "number_of_proved_distinct_full_PGSp_orbits":7,
      "number_of_proved_ground_cover_states_lower":7*51840,
      "second_order_links_remaining_inside_initial_orbit":0,
      "second_order_links_leaving_initial_orbit_per_state":6,
      "effective_second_order_hopping_per_link":"-2*t^2/J (two orderings, each intermediate loop count 19)",
      "scope":"Seven full-group orbits proved distinct; not necessarily all cover orbits. Exact combinatorial second-order edge structure, not diagonalization of the full 3^80 qutrit Hamiltonian or emergent gravity."
    }

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe72_seven_cover_orbits.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],c["number_of_proved_ground_cover_states_lower"])
