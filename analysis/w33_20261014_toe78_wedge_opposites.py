"""TOE78: canonical opposite-vertex map from every W33 Levi 2-arc
to exactly 27 girth-eight cycles. This is a direct intrinsic
incidence geometry, not a numerical 27 coincidence.

At an incidence vertex v, fix two distinct incident flag edges
e1,e2. Every cycle of length 8 containing both has a unique
antipodal vertex at distance four along it. Prove by exact W33
cycle census that 27 such cycles map bijectively onto the 27
vertices of the same bipartition class nonadjacent to v by a
Levi two-step path. The map is automatically stabilizer-equivariant.
"""
from __future__ import annotations
import itertools,collections,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_embedded_theta_exterior_flux import build
def certificate():
    edges,cycles,patch,chords=build()
    assert len(edges)==160 and len(cycles)==1620
    graph=[set() for _ in range(80)]
    flag=[[] for _ in range(80)]
    cyc_membership=[set() for _ in range(160)]
    for i,(u,v) in enumerate(edges):
        graph[u].add(v);graph[v].add(u)
        flag[u].append(i);flag[v].append(i)
    assert all(len(F)==4 for F in flag)
    for k,C in enumerate(cycles):
        for e in C:cyc_membership[e].add(k)
    def antipodal(v,start_edge,C):
        A=collections.defaultdict(list)
        for e in C:
            a,b=edges[e];A[a].append((b,e));A[b].append((a,e))
        assert len(A)==8 and all(len(x)==2 for x in A.values())
        x,y=edges[start_edge]
        nxt=y if x==v else x
        last,current=v,nxt
        for _ in range(3):
            nxts=[z for z,_ in A[current] if z!=last]
            assert len(nxts)==1
            last,current=current,nxts[0]
        assert current!=v
        return current
    errors=[];types=collections.Counter()
    per_wedge=[]
    representative=None
    for v in range(80):
        # Two-step distance neighbors in *same* partite class.
        close={v}
        for other in graph[v]:close|=graph[other]
        otherpart=set(range(0,40) if v<40 else range(40,80))
        opposite=otherpart-close
        assert len(opposite)==27
        for a,b in itertools.combinations(sorted(flag[v]),2):
            intersection=sorted(cyc_membership[a]&cyc_membership[b])
            types["point" if v<40 else "line"]+=1
            antimap={c:antipodal(v,a,cycles[c]) for c in intersection}
            if len(intersection)!=27 or set(antimap.values())!=opposite:
                errors.append([v,a,b,len(intersection),len(set(antimap.values()))])
            row={"center":v,"two_incident_flag_edges":[a,b],
                 "octagons":len(intersection),
                 "distinct_opposite_midpoint_vertices":len(set(antimap.values()))}
            per_wedge.append(row)
            if set((a,b))==set(chords):
                representative={
                  "center":v,"two_native_theta_chord_global_edges":sorted(chords),
                  "native_shared_octagon_to_canonical_opposite_vertex":
                    [[c,antimap[c]] for c in intersection],
                  "opposite_vertex_class":"point" if v<40 else "line"}
    assert len(per_wedge)==480 and types=={"point":240,"line":240}
    assert not errors,errors[:3]
    assert representative is not None, "theta chords must form a centered Levi 2-arc"
    assert len(representative["native_shared_octagon_to_canonical_opposite_vertex"])==27
    return {
      "status":"PASS_TOE78_ALL_W33_WEDGES_27_OPPOSITE_BIJECTION",
      "Levi_vertices_edges_girth8_cycles":[80,160,1620],
      "incidence_two_arc_count":480,
      "two_arc_bipartition_classes":dict(types),
      "every_wedge_octagons":27,
      "every_wedge_antipodal_opposite_vertices":27,
      "wedge_octagon_incidences":480*27,
      "octagon_wedge_incidences":1620*8,
      "all_480_wedges_verified_distinct_midpoint_bijections":True,
      "chosen_theta_chord_opposite_map":representative,
      "intrinsic_proof":"In GQ(3,3), a point/line center v has 27 noncollinear/nonconcurrent same-type opposite vertices. For each opposite u and each incident line/point neighbor of v there is a unique shortest path of length 4 from v to u starting through that neighbor, by the generalized-quadrangle axiom. Two distinct chosen first steps form a unique 8-cycle, giving an equivariant bijection between opposite vertices and octagons through the centered wedge.",
      "equivariance":"Every Levi automorphism preserving the wedge sends opposite vertices to opposite vertices and octagons to octagons; midpoint-of-an-eight-cycle commutes with this action, independently of coordinates.",
      "scope":"A canonical finite W33 incidence-geometric H27 address-space carrier for a centered wedge. Identifying an exact prior E6 cubic-frame coordinate gauge or a qutrit operator representation remains a separate problem; no physical TOE follows."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe78_wedge_27_opposites.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],c["chosen_theta_chord_opposite_map"]["center"],
          c["chosen_theta_chord_opposite_map"]["opposite_vertex_class"])
