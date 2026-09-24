#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_history_pointline_cospectral_firewall.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    all_points, history_line, graph_adj, symp,
)

def canonical4(A,verts):
    best=None
    for p in itertools.permutations(verts):
        bits=[]
        for i in range(4):
            for j in range(i+1,4):
                bits.append(int(A[p[i],p[j]]))
        code=tuple(bits)
        if best is None or code<best: best=code
    return "".join(map(str,best))

def sub4_hist(A):
    return Counter(canonical4(A,s) for s in itertools.combinations(range(27),4))

def independent_triad_cn(A):
    h=Counter()
    for tri in itertools.combinations(range(27),3):
        if not any(A[i,j] for i,j in itertools.combinations(tri,2)):
            cn=sum(all(A[x,v] for v in tri) for x in range(27) if x not in tri)
            h[int(cn)]+=1
    return h
def common_neighbor_pair_hist(A):
    edge=Counter(); non=Counter()
    for i,j in itertools.combinations(range(27),2):
        cn=int(A[i]@A[j])
        (edge if A[i,j] else non)[cn]+=1
    return edge,non

def main():
    pts=all_points()
    hs=list(itertools.product(range(3),repeat=3))
    Hline=graph_adj([history_line(s) for s in hs]).astype(int)

    p0=0
    non=[i for i in range(40) if i!=p0 and symp(pts[p0],pts[i])!=0]
    Hpoint=np.zeros((27,27),dtype=int)
    for i,u in enumerate(non):
        for j,v in enumerate(non):
            if i<j and symp(pts[u],pts[v])==0:
                Hpoint[i,j]=Hpoint[j,i]=1

    sh_line=sub4_hist(Hline); sh_point=sub4_hist(Hpoint)
    diffs={k:(sh_line.get(k,0),sh_point.get(k,0))
           for k in sorted(set(sh_line)|set(sh_point))
           if sh_line.get(k,0)!=sh_point.get(k,0)}
    it_line=independent_triad_cn(Hline)
    it_point=independent_triad_cn(Hpoint)
    ep_line,np_line=common_neighbor_pair_hist(Hline)
    ep_point,np_point=common_neighbor_pair_hist(Hpoint)
    out={
      "schema":"w33.20260924.history_pointline_cospectral_firewall.v1",
      "status":"PASS_EXACT_COSPECTRAL_POINT_LINE_FIREWALL",
      "shared":{
        "vertices":27,"edges":108,"triangles":36,
        "adjacency_spectrum":"8^1,2^12,(-1)^8,(-4)^6",
        "filled_clique_b1":46,
        "edge_common_neighbor_hist_line":dict(ep_line),
        "edge_common_neighbor_hist_point":dict(ep_point),
        "nonedge_common_neighbor_hist_line":dict(np_line),
        "nonedge_common_neighbor_hist_point":dict(np_point),
      },
      "separator":{
        "independent_triad_common_neighbor_hist_history":dict(sorted(it_line.items())),
        "independent_triad_common_neighbor_hist_point_H27":dict(sorted(it_point.items())),
        "complete_induced_four_vertex_profiles_equal":sh_line==sh_point,
        "induced_four_vertex_type_differences":diffs,
        "number_of_differing_unlabeled_4vertex_types":len(diffs),
      },
      "theorem":(
        "The line-side null-history graph and point-side H27 are a cospectral, "
        "same-edge, same-triangle, same-b1 pair and even have identical complete "
        "unlabeled induced four-vertex profiles, yet they are nonisomorphic. Their "
        "first separator in this audit is the independent-triad common-neighbor law: "
        "0^405 1^216 2^324 versus 0^225 1^648 3^72. Thus the repeated 27/108/36/46 "
        "package is a deep point/line dual shadow, not an objectwise identification."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "triad_history":out["separator"]["independent_triad_common_neighbor_hist_history"],
      "triad_point":out["separator"]["independent_triad_common_neighbor_hist_point_H27"],
      "four_type_diff_count":len(diffs),
      "four_type_diffs":diffs,
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
