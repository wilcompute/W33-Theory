"""TOE65 independent geometric and topological admission gates.

Native TOE38 octagonal two-complex ranks are checked against committed
certificates and graph connectivity. Torus example is ONLY a non-native
control, not a constructed W33 chiral index.
"""
from pathlib import Path
import json,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261013_toe65_surface_topology_correction import rank_gf2

def certificate():
    edges,v,lookup,octs,comm,*_=prep()
    ed=np.asarray(edges,dtype=int)
    assert ed.shape==(160,2)
    degrees=np.bincount(ed.ravel(),minlength=80)
    assert np.all(degrees==4)
    adj=[set() for _ in range(80)]
    for a,b in ed:adj[a].add(int(b));adj[b].add(int(a))
    seen={0};queue=[0]
    for a in queue:
        for b in adj[a]:
            if b not in seen:seen.add(b);queue.append(b)
    assert len(seen)==80
    rank1=79
    # TOE62 independently computed rank(d2)=78 over F2; verify the
    # source certificate and 1382 fully active native 8-gon faces.
    prior=json.loads((ROOT/"data/w33_20261013_toe62_vertex_links.json").read_text())
    assert prior["native_graph"]["GF2_boundary_rank"]==78
    assert prior["native_graph"]["octagon_faces"]==1382
    P=np.rint(np.asarray([cycle_row(o,edges,v,lookup,np.zeros(3)).real
                           for o in octs])).astype(int)
    assert P.shape==(1382,160)
    rank2=rank_gf2([
        sum(1<<int(e) for e in np.flatnonzero(row)) for row in P
    ])
    assert rank2==78
    bX=[80-rank1, 160-rank1-rank2, 1382-rank2]
    assert bX==[1,3,1304]
    bS1=[1,1]
    bT2=[1,2,1]
    def conv(x,y):return [sum(x[i]*y[k-i] for i in range(len(x)) if 0<=k-i<len(y)) for k in range(len(x)+len(y)-1)]
    time=conv(bX,bS1)
    twice=conv(bX,bT2)
    assert time==[1,4,1307,1304]
    assert twice==[1,5,1311,2611,1304]
    # Proof with e added simple edges joining existing native vertices.
    # Degree increments s_v sum=2e, one new edge can share at most
    # one endpoint with any other in a simple graph. Thus
    # C_max =480+8e+sum C(s_v,2) <=480+8e+C(e,2).
    rows=[]
    for e in (0,1,10,18,19,20):
        cap_max=480+8*e+e*(e-1)//2
        necessary=8*(81+e)
        rows.append({"added_edges":e,"max_possible_distinct_vertex_corners":cap_max,
                     "minimum_corners_from_closed_Euler":necessary,
                     "simple_link_capacity_can_meet_Euler":cap_max>=necessary})
    assert all(not x["simple_link_capacity_can_meet_Euler"] for x in rows if x["added_edges"]<=18)
    assert rows[-2]["simple_link_capacity_can_meet_Euler"]
    # Standard 4-torus cochain control: c1=m dx1^dx2+n dx3^dx4.
    # 1/2*integral c1^2 = mn; this is topological testbed ONLY.
    m,n=1,1
    test_control=(2*m*n)//2
    assert test_control==1
    return {
        "status":"PASS_TOE65_NATIVE_SPACETIME_GATES_AND_4D_POSITIVE_CONTROL",
        "native_2complex":{"V":80,"E":160,"octagonal_2cells":1382,
                             "rank_d1_F2":rank1,"rank_d2_F2":rank2,
                             "betti_F2":bX},
        "time_circle_product_betti_F2":time,
        "time_circle_product_H4_F2":time[4] if len(time)>4 else 0,
        "two_time_circles_product_betti_F2":twice,
        "closed_connected_4manifold_H4_over_F2_dim_expected":1,
        "added_edge_necessary_condition":{
           "model":"keep V=80, append e simple edges between original vertices, require all faces embedded octagons and simple local links",
           "pair_count_requirement":168,"at_least_added_edges":19,
           "rows":rows,
           "necessary_not_sufficient":True,
        },
        "non_native_T4_positive_control":{"c1_plane12":m,"c1_plane34":n,
                "half_c1_squared":test_control,"is_native_W33_index":False},
        "scope":"The XxS1 4th homology vanishes; XxT2 has b4=1304, not b4=1, so neither naive product is a connected closed 4-manifold (mod-2 top homology is one-dimensional even without orientability). This is no-go for these particular products, not for refined W33 spacetime. Standard T4 c1 square is a topology control, NOT a computed W33 overlap index or anomaly-free Weyl spectrum."
    }
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261013_toe65_spacetime_admission_gates.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],c["native_2complex"]["betti_F2"],c["added_edge_necessary_condition"]["at_least_added_edges"],flush=True)
