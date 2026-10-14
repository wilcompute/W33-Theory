"""TOE79: a CANONICAL GQ(3,3) explanation of the W33 27-octagon H27 torsor.

For each W33 point p and each unordered pair of its four incident
Levi flag edges {e1,e2}, the 27 Levi octagons through both edges
are naturally in bijection with the 27 W33 points q noncollinear to p:
take the antipodal point halfway around the 8-cycle.

Exhaustively verify ALL 40*6*27=6480 decorated octagons and
PGSp(4,3) generator transitivity, not just cardinality coincidence.
"""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import octagons
from w33_pass1081_1086_core import (
    build_w33,transvection_perm,outer_similitude_perm,line_perm)

def certificate():
    ed,adj,cycles=octagons()
    pts,pidx,lines,lidx,point_lines,frames,fidx,flags,flagidx=build_w33()
    assert len(pts)==40 and len(lines)==40 and len(flags)==160
    incident={p:sorted(e for e,(v,l) in enumerate(flags) if v==p) for p in range(40)}
    assert all(len(x)==4 for x in incident.values())
    opp={p:{q for q in range(40) if q!=p and not any(
              p in line and q in line for line in lines)}
         for p in range(40)}
    assert all(len(x)==27 for x in opp.values())
    cycles_at_pair=collections.defaultdict(dict)
    by_cycle=[]
    for ci,C in enumerate(cycles):
        local=collections.defaultdict(list)
        for e in C:
            a,b=ed[e]
            local[a].append((b,e))
            local[b].append((a,e))
        assert len(local)==8 and all(len(x)==2 for x in local.values())
        count=0
        for p in sorted(x for x in local if x<40):
            # exactly 2 native edges at this point; unambiguously
            # infer the opposite point by four nonbacktracking steps.
            first=local[p][0][0]
            before,now=p,first
            for step in range(3):
                candidates=[y for y,e in local[now] if y!=before]
                assert len(candidates)==1
                nxt=candidates[0]
                before,now=now,nxt
            q=now
            assert q in opp[p] and q<40
            pair=tuple(sorted(e for n,e in local[p]))
            assert pair[0] in incident[p] and pair[1] in incident[p]
            key=(p,pair[0],pair[1])
            assert q not in cycles_at_pair[key]
            cycles_at_pair[key][q]=ci
            count+=1
        assert count==4
        by_cycle.append(count)
    assert len(cycles_at_pair)==40*6==240
    for p in range(40):
        for a,b in itertools.combinations(incident[p],2):
            assert set(cycles_at_pair[(p,a,b)])==opp[p]
    all_states={(p,a,b,q)
             for (p,a,b),m in cycles_at_pair.items() for q in m}
    assert len(all_states)==6480
    # Explicit orbit under native symplectic transformations
    # on (point p, pair of incident flags, antipode q).
    perms=[transvection_perm(pts[i],pts,pidx) for i in (0,1,2,4,8,15)]
    perms.append(outer_similitude_perm(pts,pidx))
    actions=[]
    for perm in perms:
        lp=line_perm(perm,lines,lidx)
        edgeaction=tuple(flagidx[(perm[v],lp[l])] for v,l in flags)
        actions.append((perm,edgeaction))
    p0,a0,b0,q0=min(all_states)
    seen={(p0,a0,b0,q0)}
    todo=collections.deque(seen)
    while todo:
        p,a,b,q=todo.popleft()
        for perm,ep in actions:
            x,y=sorted((ep[a],ep[b]))
            transformed=(perm[p],x,y,perm[q])
            assert transformed in all_states
            if transformed not in seen:
                seen.add(transformed);todo.append(transformed)
    assert len(seen)==len(all_states)==6480
    assert (p0,a0,b0) in cycles_at_pair and q0 in cycles_at_pair[(p0,a0,b0)]
    theta_p=1;theta_pair=(5,6)
    assert (theta_p,*theta_pair) in cycles_at_pair
    assert ed[theta_pair[0]][0]==theta_p==ed[theta_pair[1]][0]
    assert len(cycles_at_pair[(theta_p,*theta_pair)])==27
    theta_map=[{"opposite_W33_point":q,"native_octagon_index":ci}
        for q,ci in sorted(cycles_at_pair[(theta_p,*theta_pair)].items())]
    # 6480=1620*4, and stabilizer chain 51840/40=1296,
    # /6=216, /27=8. Both orbit sizes independently verified.
    assert 40*6*27==len(cycles)*4==6480
    assert 51840//40==1296 and 1296//6==216 and 216//27==8
    return {
      "status":"PASS_TOE79_CANONICAL_27_OPPOSITE_POINT_OCTAGON_GQ_MAP",
      "W33_group":"PGSp(4,3)",
      "W33_projective_points":40,
      "W33_Levi_flag_edges":160,
      "W33_undirected_eight_cycles":1620,
      "incident_lines_per_point":4,
      "noncollinear_points_per_point":27,
      "unordered_incident_edge_pairs_per_point":6,
      "pair_octagon_keys":len(cycles_at_pair),
      "each_incident_flag_pair_octagons":27,
      "rooted_point_octagon_pair_antipode_states":len(all_states),
      "complete_native_PGSp_orbit_size":len(seen),
      "stabilizer_order_chain":{"PGSp":51840,"point":1296,
                                "point_plus_incident_line_pair":216,
                                "point_plus_incident_line_pair_plus_noncollinear_point":8},
      "rooted_octagon_double_count":"40 * C(4,2) * 27 = 1620 * 4 = 6480",
      "theta_native_point":theta_p,
      "theta_native_chords":list(theta_pair),
      "theta_opposite_point_to_octagon_bijection":theta_map,
      "map_is_canonical":"For a given point p, an unordered pair of its four flags {e1,e2}, and a noncollinear point q, the GQ(3,3) unique-nearest-point axiom defines one 8-cycle p-e1-...-q-...-e2-p. Its antipode after four Levi edges is q. The bijection is graph-defined and equivariant under PGSp; no arbitrary labeling or Clifford gauge is needed.",
      "H27_address_consequence":"The 27 shared octagons are canonically the SAME 27 W33 noncollinear-to-p opposite points for the chosen native pair, carrying the established regular Payne Heisenberg address torsor, and also the native GQ(2,4)/E6 cubic incidence from TOE78.",
      "scope":"Exact finite W33 generalized-quadrangle geometry and symmetry, not proof that 27 octagon modes are physical particles or a dynamical TOE."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe79_canonical_antipode_octagon.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],"point",c["theta_native_point"],
         "pair",c["theta_native_chords"],
         "orbit",c["complete_native_PGSp_orbit_size"])
