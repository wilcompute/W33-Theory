"""TOE70: PSp/PGSp orbit of the twenty-octagon cover and 4D topology gate.

Native PGSp orbit is exact; a 20-face CW complex destroys all three
selected flat holonomy directions and has zero H4 after product with T2.
No four-dimensional overlap index is claimed.
"""
from pathlib import Path
from collections import deque,defaultdict
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1081_1086_core import build_w33,transvection_perm,line_perm,outer_similitude_perm
from w33_20261014_toe69_five_fronts import octagons,windings,COVER

def certificate():
    pts,pidx,lines,lidx,point_lines,frames,fidx,flags,flagidx=build_w33()
    edges,adj,cycles=octagons()
    assert len(flags)==160 and len(cycles)==1620
    ci={tuple(sorted(c)):i for i,c in enumerate(cycles)}
    def cycle_action(point_perm):
        lineper=line_perm(point_perm,lines,lidx)
        edgeper=tuple(flagidx[(point_perm[p],lineper[l])] for p,l in flags)
        assert len(set(edgeper))==160
        return tuple(ci[tuple(sorted(edgeper[e] for e in cycle))] for cycle in cycles)
    generators=tuple(cycle_action(transvection_perm(pts[i],pts,pidx))
                     for i in (0,1,2,4,8,15))
    start=tuple(sorted(COVER))
    seen={start};queue=deque([start])
    while queue:
        state=queue.popleft()
        for g in generators:
            shifted=tuple(sorted(g[i] for i in state))
            if shifted not in seen:
                seen.add(shifted);queue.append(shifted)
    assert len(seen)==25920
    outer=cycle_action(outer_similitude_perm(pts,pidx))
    other=tuple(sorted(outer[i] for i in start))
    assert other not in seen
    # Full PGSp group is PSp union the coset induced by the above similitude.
    # It has 51840 elements; the cover stabilizer is therefore trivial.
    assert 2*len(seen)==51840
    # Determine which alternative octagons meet all 8 vertices using a
    # different through-edge pairing from the exhibited cover.
    owner={e:i for i in COVER for e in cycles[i]}
    assert len(owner)==160
    pairings={}
    for v in range(80):
        groups=defaultdict(list)
        for neighbor,e,sign in adj[v]:
            groups[owner[e]].append(e)
        assert len(groups)==2 and all(len(es)==2 for es in groups.values())
        pairings[v]={frozenset(es) for es in groups.values()}
    eligible=[]
    for i,face in enumerate(cycles):
        vs={v for e in face for v in edges[e]}
        if all(frozenset(e for e in face if v in edges[e]) not in pairings[v]
               for v in vs):
            eligible.append(i)
    unfillable=sorted(set(range(160))-set(e for i in eligible for e in cycles[i]))
    assert len(eligible)==73 and unfillable==[45]
    # All group-equivalent members of the full 51840 orbit inherit this
    # obstruction to a complementary 20-octagon face decomposition.
    faces=[cycles[i] for i in COVER]
    boundary=np.zeros((80,160),dtype=int)
    for e,(a,b) in enumerate(edges):
        boundary[a,e]=-1;boundary[b,e]=1
    d2=np.zeros((160,20),dtype=int)
    for j,face in enumerate(faces):
        sub=defaultdict(list)
        for e in face:
            a,b=edges[e];sub[a].append((b,e,1));sub[b].append((a,e,-1))
        now=min(sub);prev=None
        for k in range(8):
            nxt,e,sign=next(z for z in sub[now] if z[0]!=prev)
            d2[e,j]=sign
            prev,now=now,nxt
        assert now==min(sub)
    assert not np.any(boundary@d2)
    assert all(np.count_nonzero(d2[:,j])==8 for j in range(20))
    assert sorted(np.count_nonzero(d2,axis=1))==[1]*160
    # Disjoint primitive signed supports imply integral rank(d2)=20
    # with a primitive image; rank(d1)=79 as the graph is connected.
    winding=dict(windings(cycles,edges))
    face_windings=[winding.get(i,(0,0,0)) for i in COVER]
    nonzero=[list(x) for x in face_windings if any(x)]
    assert nonzero==[[0,0,-1],[0,1,0],[1,0,0]]
    assert np.linalg.det(np.array(nonzero,dtype=int)) in (-1,1)
    # X: V=80 E=160 F=20, H=(1,61,0); X x T2 H=(1,63,123,61,0)
    Bx=[1,61,0];torus=[1,2,1]
    product=[sum(Bx[j]*torus[k-j] for j in range(3) if 0<=k-j<3)
             for k in range(5)]
    assert product==[1,63,123,61,0]
    return {
      "status":"PASS_TOE70_ORBIT_51840_AND_HOLONOMY_TOPOLOGY_GATE",
      "native_Levi_vertices":80,"native_Levi_edges":160,
      "GQ_octagons":1620,"selected_octahedral_faces":20,
      "symplectic_generator_center_points":[0,1,2,4,8,15],
      "inner_PSp_cover_orbit":len(seen),"inner_cover_stabilizer":1,
      "outer_similitude_image_in_inner_orbit":False,
      "full_PGSp_cover_orbit":51840,"full_cover_stabilizer":1,
      "complementary_cover_no_go":{
         "distinct_locally_compatible_octagons":len(eligible),
         "native_edges_in_no_compatible_octagon":unfillable,
         "applies_to_full_orbit":True,
         "scope":"Blocks complementary octagonal genus-21 embedding starting from ANY cover in this one 51840-element PGSp orbit, not every W33 cover or embedding."},
      "attached_twenty_faces":{
         "CW_vertices_edges_faces":[80,160,20],
         "ranks_over_Z":[79,20],
         "homology_betti":[1,61,0],
         "torsion_in_H1":False,
         "CW_times_T2_betti":product,
         "face_windings_in_three_TOE67_coordinates":nonzero,
         "winding_matrix_rank":3,
         "flat_3deck_holonomies_on_X_are_forced_trivial":True,
         "physical_scope":"New 20-face CW complex, not a manifold. Flat nonzero 3pi phases cannot extend as flat connections; a curved gauge field is not ruled out. No W33 4D overlap index or admissible spin lattice."}
    }

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe70_symmetry_topology.json").write_text(
        json.dumps(c,indent=2)+"\n")
    print(c["status"],c["attached_twenty_faces"]["CW_times_T2_betti"])
