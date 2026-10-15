"""TOE86: integral SNF for representatives of all 13 pair classes."""
from __future__ import annotations
from collections import Counter,defaultdict
import json
from sympy import Matrix,ZZ
from sympy.matrices.normalforms import smith_normal_form
from analysis.w33_20261015_toe85_h2_relation_module import ROOT
from analysis.w33_20261015_toe86_geometry_integral_routing import native
def certificate():
    census=json.loads((ROOT/"data/w33_20261015_toe86_geometry_integral_routing.json").read_text(encoding="utf8"))["orbit_pair_census"]
    sigs=json.loads((ROOT/"data/w33_20261015_toe86_pair_polarization.json").read_text(encoding="utf8"))["class_representative_signatures"]
    lookup={tuple(x["representative"]):x for x in sigs}
    tris,edges,ei,perms,orbits=native()
    def walk_square(s):
        ns=defaultdict(set)
        for i in s:
            u,v=edges[i];ns[u].add(v);ns[v].add(u)
        v=min(ns);w=[v,min(ns[v])]
        while len(w)<4:w.append(next(k for k in ns[w[-1]] if k!=w[-2]))
        return w+[v]
    def oriented(walk):
        v=[0]*135
        for u,w in zip(walk,walk[1:]):
            v[ei[tuple(sorted((u,w)))]]+=1 if u<w else -1
        return v
    triangles=[oriented([a,b,c,a]) for a,b,c in tris]
    records=[]
    for cls in census["classes"]:
        a,b=cls["representative"]
        sq=sorted(set(orbits[a])|set(orbits[b]))
        rows=triangles+[oriented(walk_square(s)) for s in sq]
        M=Matrix(rows).T
        S=smith_normal_form(M,domain=ZZ)
        diag=[abs(int(S[i,i])) for i in range(99) if S[i,i]!=0]
        assert all(diag[i+1]%diag[i]==0 for i in range(len(diag)-1))
        inv=Counter(diag)
        r0=len(diag)
        r2=cls["face_rank_F2"]
        r3=lookup[(a,b)]["face_rank_F3"]
        assert r2==sum(d%2!=0 for d in diag)
        assert r3==sum(d%3!=0 for d in diag)
        obj={"representative":[a,b],"class_size":cls["size"],
             "rational_rank":r0,"ranks_F2_F3":[r2,r3],
             "nonunit_smith_factors":[d for d in diag if d>1],
             "H2_free_rank_Z":99-r0,"H1_free_rank_Z":109-r0,
             "H1_Z_torsion":[d for d in diag if d>1]}
        records.append(obj)
        print("SNF",a,b,"size",cls["size"],"ranks",r0,r2,r3,
              "torsion",obj["nonunit_smith_factors"],flush=True)
    return {"pairs_classified":468,"class_count":13,
            "classes":records,
            "torsion_free_pair_count":sum(x["class_size"] for x in records
                                          if not x["nonunit_smith_factors"]),
            "torsion_pattern_pair_counts":dict(Counter(
                str(x["nonunit_smith_factors"]) for x in records
                for _ in range(x["class_size"])))}
if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe86_pair_integral.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("DISTRIBUTION",d["torsion_pattern_pair_counts"])
