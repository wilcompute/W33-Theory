"""TOE86 track I extension: H1/H2 ternary rank signatures on all 13
full-normalizer equivalence classes of 468 admissible square-orbit pairs.
"""
from collections import defaultdict
import json
from itertools import combinations
from analysis.w33_20261015_toe85_h2_relation_module import (
    ROOT,nullspace,action_on_kernel,rank_and_basis
)
from analysis.w33_20261015_toe86_geometry_integral_routing import native,H,IDX
from analysis.w33_20261015_toe86_hom_intertwiners import cycle_basis

DIRECTION_REPS=((0,0,1),(1,0,0),(0,1,0),(1,1,0),(1,2,0))

def calculate():
    prev=json.loads((ROOT/"data/w33_20261015_toe86_geometry_integral_routing.json").read_text(encoding="utf8"))
    classes=prev["orbit_pair_census"]["classes"]
    tris,edges,ei,perms,orbits=native()
    cycles=cycle_basis(edges,ei)
    assert len(cycles)==109
    def oriented(walk):
        v=[0]*135
        for u,w in zip(walk,walk[1:]):
            v[ei[tuple(sorted((u,w)))]]+=1 if u<w else -1
        return v
    def square_walk(ids):
        ns=defaultdict(set)
        for i in ids:
            u,v=edges[i];ns[u].add(v);ns[v].add(u)
        start=min(ns);u=min(ns[start]);w=[start,u]
        while len(w)<4:
            w.append(next(t for t in ns[w[-1]] if t!=w[-2]))
        return w+[start]
    tri_rows=[oriented([a,b,c,a]) for a,b,c in tris]
    records=[]
    for cls in classes:
        a,b=cls["representative"]
        sq=sorted(set(orbits[a])|set(orbits[b]))
        face_rows=tri_rows+[oriented(square_walk(s)) for s in sq]
        r=len(rank_and_basis(face_rows,3))
        basis,free,r2=nullspace([[face_rows[j][i] for j in range(99)]
                                 for i in range(135)],3)
        assert r==r2 and len(basis)==99-r
        face_idx={f:i for i,f in enumerate(tris)}
        sq_idx={s:45+i for i,s in enumerate(sq)}
        signature=[]
        for g in DIRECTION_REPS:
            p=perms[IDX[g]]
            edge_dest=[ei[tuple(sorted((p[u],p[v])))] for u,v in edges]
            edge_sign=[1 if p[u]<p[v] else -1 for u,v in edges]
            def action(row):
                v=[0]*135
                for i,t in enumerate(row):
                    if t:v[edge_dest[i]]=(t*edge_sign[i])%3
                return v
            diff=[[((a-b)%3) for a,b in zip(action(cyc),cyc)]
                  for cyc in cycles]
            h1rank=len(rank_and_basis(face_rows+diff,3))-r
            dest=[];sign=[]
            for i,face in enumerate(face_rows):
                if i<45:
                    j=face_idx[tuple(sorted(p[t] for t in tris[i]))]
                else:
                    s=tuple(sorted(ei[tuple(sorted((p[edges[k][0]],p[edges[k][1]])))]
                                   for k in sq[i-45]))
                    j=sq_idx[s]
                transformed=action(face)
                target=[t%3 for t in face_rows[j]]
                if transformed==target:sgn=1
                else:
                    assert transformed==[(-t)%3 for t in target]
                    sgn=-1
                dest.append(j);sign.append(sgn)
            assert sorted(dest)==list(range(99))
            HM=action_on_kernel(basis,free,(dest,sign),3)
            h2rank=len(rank_and_basis([[(v-int(i==j))%3 for j,v in enumerate(row)]
                                      for i,row in enumerate(HM)],3))
            signature.append({"group_element":list(g),
                              "H1_rank_g_minus_I":h1rank,
                              "H2_rank_g_minus_I":h2rank})
        dirh1=[t["H1_rank_g_minus_I"] for t in signature[1:]]
        dirh2=[t["H2_rank_g_minus_I"] for t in signature[1:]]
        min_h1=[i for i,x in enumerate(dirh1) if x==min(dirh1)]
        min_h2=[i for i,x in enumerate(dirh2) if x==min(dirh2)]
        records.append({"representative":[a,b],"class_size":cls["size"],
                        "face_rank_F2":cls["face_rank_F2"],"face_rank_F3":r,
                        "H1_dimension_F3":109-r,"H2_dimension_F3":99-r,
                        "noncentral_direction_signatures":signature[1:],
                        "center_signature":signature[0],
                        "minimum_H1_direction_indices":min_h1,
                        "minimum_H2_direction_indices":min_h2,
                        "identical_min_direction_sets":min_h1==min_h2})
        print("class",a,b,"size",cls["size"],"r",r,"H1",dirh1,
              "H2",dirh2,"match",min_h1==min_h2,flush=True)
    assert sum(x["class_size"] for x in records)==468
    return {"checked_full_normalizer_classes":len(records),
            "pairs_covered_by_equivariance":468,
            "directions":["(1,0)","(0,1)","(1,1)","(1,2)"],
            "class_representative_signatures":records,
            "rank_F3_pair_count_by_equivalence":{
                 str(rank):sum(x["class_size"] for x in records if x["face_rank_F3"]==rank)
                 for rank in sorted({x["face_rank_F3"] for x in records})},
            "matching_H1_H2_min_direction_pairs":sum(x["class_size"] for x in records
                                                      if x["identical_min_direction_sets"])}

if __name__=="__main__":
    d=calculate()
    p=ROOT/"data/w33_20261015_toe86_pair_polarization.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("SUMMARY",d["rank_F3_pair_count_by_equivalence"],
          d["matching_H1_H2_min_direction_pairs"],"of 468")
