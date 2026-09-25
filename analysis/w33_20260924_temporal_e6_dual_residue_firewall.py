#!/usr/bin/env python3
from __future__ import annotations

import itertools, json, sys
from collections import Counter, deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_temporal_e6_dual_residue_firewall.json"

from analysis.w33_20260924_history_invariant_cycle_orientation import TRIS

def graph_from_triads(tris,n=27):
    A=np.zeros((n,n),dtype=int)
    for t in tris:
        for i,j in itertools.combinations(t,2):
            assert A[i,j]==0
            A[i,j]=A[j,i]=1
    return A

def spectrum(A):
    vals=np.linalg.eigvalsh(A.astype(float))
    return {
      str(int(round(x))):sum(abs(vals-x)<1e-7)
      for x in sorted(set(round(float(y)) for y in vals),reverse=True)
    }

def cn_hist(A,adjacent):
    n=len(A); c=Counter()
    for i,j in itertools.combinations(range(n),2):
        if bool(A[i,j]) != adjacent:
            continue
        c[int(A[i]@A[j])]+=1
    return dict(sorted(c.items()))

def distance_hist(A):
    n=len(A); hist=Counter()
    for s in range(n):
        dist=[-1]*n;dist[s]=0;q=deque([s])
        while q:
            u=q.popleft()
            for v in np.flatnonzero(A[u]):
                v=int(v)
                if dist[v]<0:
                    dist[v]=dist[u]+1;q.append(v)
        assert all(x>=0 for x in dist)
        for t in range(s+1,n):
            hist[dist[t]]+=1
    return dict(sorted(hist.items()))

def triangle_count(A):
    return int(round(np.trace(A@A@A)/6))

def main():
    e6=json.loads(
      (ROOT/"artifacts/e6_cubic_affine_heisenberg_model.json").read_text()
    )
    q43=json.loads(
      (ROOT/"data/w33_20260924_history_bigcell_q43_compactification.json").read_text()
    )
    p7186=json.loads(
      (ROOT/"data/PART_W33_PASS7186_E8_MATTER_H27_CAYLEY.json").read_text()
    )
    gauge=json.loads(
      (ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text()
    )
    temporal=[tuple(sorted(map(int,t))) for t in TRIS]
    affine=sorted({
      tuple(sorted(map(int,t)))
      for rec in e6["affine_u_lines"]
      for t in rec["triads"]
    })
    fibers=[tuple(sorted(map(int,t))) for t in e6["fiber_triads_e6id"]]
    assert len(temporal)==len(affine)==36
    assert len(fibers)==9

    T=graph_from_triads(temporal)
    E=graph_from_triads(affine)

    for A in (T,E):
        assert set(map(int,A.sum(axis=1)))=={8}
        assert int(A.sum()//2)==108
        assert triangle_count(A)==36

    st=spectrum(T);se=spectrum(E)
    expected={"8":1,"2":12,"-1":8,"-4":6}
    assert st==se==expected
    assert q43["null_history_graph"]["adjacency_spectrum"]==expected
    assert p7186["spectrum"]=="8^1 + 2^12 + (-1)^8 + (-4)^6"

    t_adj=cn_hist(T,True); e_adj=cn_hist(E,True)
    t_non=cn_hist(T,False);e_non=cn_hist(E,False)
    assert t_adj==e_adj=={1:108}
    assert t_non=={2:162,4:81}
    assert e_non=={0:27,3:216}

    dt=distance_hist(T);de=distance_hist(E)
    assert dt=={1:108,2:243}
    assert de=={1:108,2:216,3:27}
    assert max(dt)==2 and max(de)==3
    assert p7186["diameter"]==3
    assert q43["null_history_graph"]["induced_from_Q43_line_intersection_graph"]

    # The E6 firewall fibres are exactly the 27 distance-three / zero-CN pairs.
    zero_pairs={
      (i,j) for i,j in itertools.combinations(range(27),2)
      if not E[i,j] and int(E[i]@E[j])==0
    }
    fiber_pairs={
      tuple(sorted((i,j)))
      for t in fibers
      for i,j in itertools.combinations(t,2)
    }
    assert zero_pairs==fiber_pairs and len(zero_pairs)==27

    F=E.copy()
    for i,j in fiber_pairs:
        F[i,j]=F[j,i]=1
    assert set(map(int,F.sum(axis=1)))=={10}
    assert cn_hist(F,True)=={1:135}
    assert cn_hist(F,False)=={5:216}
    assert spectrum(F)=={"10":1,"1":20,"-5":6}

    # The common-neighbour histogram is an isomorphism invariant.
    # Its mismatch proves there is no vertex or triad relabelling between them.
    assert t_non!=e_non

    assert e6["cross_checks"]["firewall_bad_triads_match_fiber_triads"]
    assert gauge["incidence"]["mapped_full45_equal"] is True
    assert gauge["incidence"]["mapped_bad9_equal"] is True

    out={
      "schema":"w33.20260924.temporal_e6_dual_residue_firewall.v1",
      "status":"PASS_TEMPORAL_36_AND_E6_AFFINE_36_ARE_COSPECTRAL_NONISOMORPHIC_DUAL_RESIDUES",
      "shared_shadow":{
        "vertices":27,"degree":8,"edges":108,"triangles":36,
        "spectrum":expected,
        "adjacent_common_neighbors":{"1":108},
        "vertex_triangle_degree":4,
        "each_edge_in_exactly_one_triangle":True,
      },
      "temporal_line_side":{
        "source":"Q(4,3) line-side Bell big cell",
        "diameter":2,
        "pair_distance_histogram":{str(k):v for k,v in dt.items()},
        "nonedge_common_neighbor_histogram":{str(k):v for k,v in t_non.items()},
        "zero_common_neighbor_nonedge_pairs":0,
        "producer_status":q43["status"],
      },
      "E6_point_side":{
        "source":"W(3,3) H27 / E8 matter-fibre Cayley graph",
        "diameter":3,
        "pair_distance_histogram":{str(k):v for k,v in de.items()},
        "nonedge_common_neighbor_histogram":{str(k):v for k,v in e_non.items()},
        "zero_common_neighbor_nonedge_pairs":27,
        "pass7186_status":p7186["status"],
        "pass7186_intersection_array":p7186["intersection_array"],
      },
      "firewall_completion":{
        "fiber_triads":9,
        "fiber_pairs":27,
        "fiber_pairs_equal_all_zero_CN_nonedges":True,
        "completed_graph":"SRG(27,10,1,5)",
        "completed_spectrum":{"10":1,"1":20,"-5":6},
      },
      "no_go":{
        "hypergraphs_isomorphic":False,
        "proof_invariant":"nonedge common-neighbour histogram",
        "temporal":"{2:162, 4:81}; diameter 2",
        "E6_affine":"{0:27, 3:216}; diameter 3",
        "same_spectrum_does_not_identify_the_36_triads":True,
      },
      "dual_residue_reading":(
        "The two 27-by-36 triangle systems are the point/line-dual residual "
        "constructions that the odd-q firewall keeps distinct.  On the E6/W33 "
        "point side, 27 remote points support 36 affine line-triads and the nine "
        "fiber triads close the 27 distance-three pairs.  On the temporal Q(4,3) "
        "line side, 27 lines disjoint from the Bell line support 36 point-triads; "
        "their null graph already has diameter two and no zero-common-neighbour "
        "nonedges.  They share counts and spectrum but not incidence geometry."
      ),
      "theorem":(
        "The temporal 36-triangle complex and the E6 affine 36-triad complex "
        "are a new exact cospectral firewall pair: both are 8-regular 27-vertex "
        "graphs with 108 edges, 36 triangles and spectrum "
        "8^1+2^12+(-1)^8+(-4)^6, yet they are not isomorphic.  The temporal "
        "nonedges have 2 or 4 common neighbours, whereas the E6 nonedges have "
        "0 or 3.  The 27 E6 zero-common-neighbour pairs are exactly the nine "
        "firewall-fiber triangles; adding them produces SRG(27,10,1,5)."
      ),
      "boundary":(
        "This explicitly blocks the tempting identification temporal-36 = "
        "E6-affine-36.  The correct bridge is dual/cospectral, not objectwise. "
        "No continuum dynamics or particle assignment is inferred."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "spectrum":expected,
      "temporal_nonedge_CN":t_non,
      "E6_nonedge_CN":e_non,
      "fiber_completion":out["firewall_completion"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
