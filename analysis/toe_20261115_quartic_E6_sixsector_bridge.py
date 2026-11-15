#!/usr/bin/env python3
"""Quartic point-geometry bridge unlocking the E6 six-sector missed by
all scalar 45-octet-linear and point-pair Q channels.

Existing BT766/Pass1536 45 K4,4 octets and the 27 five-clique
partitions are prior art. New operator: product of TWO point-pair
octet-membership channels. When the two octets are disjoint, their
common 27-line support is a ONE-HOT selector. 270 independent
four-point selectors form a 270x27 tight reconstruction frame.
"""
from itertools import combinations
from collections import Counter
import sys,json
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1536_frame_dual_k44_code import build_geometry
OUT=ROOT/"data"/"toe_20261115_quartic_E6_sixsector_bridge.json"

def run():
    data=build_geometry()
    octets=data["octets"]
    points=[tuple(p) for p in data["points"]]
    assert len(octets)==45 and len(points)==40
    S=[frozenset(left+right) for left,right in octets]
    octet_idx={S[i]:i for i in range(45)}
    C=np.zeros((45,45),dtype=np.int64)
    for i,j in combinations(range(45),2):
        if S[i].isdisjoint(S[j]):C[i,j]=C[j,i]=1
        else:assert len(S[i]&S[j])==2
    assert np.array_equal(C.sum(axis=0),np.full(45,12))
    lines=sorted(tuple(sorted(x)) for x in nx.find_cliques(nx.from_numpy_array(C)))
    assert len(lines)==27 and all(len(x)==5 for x in lines)
    lindex={frozenset(x):i for i,x in enumerate(lines)}
    T=np.zeros((45,27),dtype=np.int64)
    for i,line in enumerate(lines):T[list(line),i]=1
    A=T.T@T-5*np.eye(27,dtype=np.int64)
    E=(A-10*np.eye(27,dtype=np.int64))@(A-np.eye(27,dtype=np.int64))
    assert np.array_equal(T@E,np.zeros((45,27),dtype=np.int64))
    assert np.array_equal(E@E,90*E) and int(np.trace(E))==540

    P=np.zeros((40,45),dtype=np.int64)
    for i,octet in enumerate(S):P[list(octet),i]=1
    nonedge_pairs=[]
    for i,(left,right) in enumerate(octets):
        p,q=left[:2]
        assert not data["graph"].has_edge(p,q)
        assert np.flatnonzero(P[p]*P[q]).tolist()==[i]
        nonedge_pairs.append((p,q))
    # Degree-2 point-pair signal for octet a is exactly T[a,:].
    quadratic=np.array([P[p]*P[q]@T for p,q in nonedge_pairs])
    assert np.array_equal(quadratic,T)
    assert np.linalg.matrix_rank(quadratic)==21
    assert np.array_equal(quadratic@E,np.zeros((45,27),dtype=np.int64))
    # Degree-4 monomial: two independent nonedge-pair certificates
    # for disjoint octets a,b; unique cubic line contains a AND b.
    adjacent_pairs=sorted((i,j) for i,j in combinations(range(45),2) if C[i,j])
    assert len(adjacent_pairs)==270
    quartic=np.array([quadratic[i]*quadratic[j] for i,j in adjacent_pairs])
    assert quartic.shape==(270,27)
    assert np.array_equal(quartic.sum(axis=1),np.ones(270,dtype=np.int64))
    assert np.array_equal(quartic.sum(axis=0),np.full(27,10,dtype=np.int64))
    assert np.array_equal(quartic.T@quartic,10*np.eye(27,dtype=np.int64))
    assert np.linalg.matrix_rank(quartic)==27
    assert np.linalg.matrix_rank(quartic@E)==6
    assert np.count_nonzero(quartic@E)>0
    # Reconstruction identity: y = (1/10) R^T z for z=Ry.
    probe=np.arange(-13,14,dtype=np.int64)
    assert np.array_equal(quartic.T@(quartic@probe),10*probe)
    # Every selector involves FOUR DISTINCT W33 rays.
    quartets=[(*nonedge_pairs[i],*nonedge_pairs[j]) for i,j in adjacent_pairs]
    assert all(len(set(four))==4 for four in quartets)

    # Full equivariance, ALL 40 projective symplectic transvections.
    pairs_index={pair:k for k,pair in enumerate(adjacent_pairs)}
    point_index={p:i for i,p in enumerate(points)}
    def form(u,v):
        return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3
    def normalize(v):
        v=tuple(x%3 for x in v)
        mul=1 if next(x for x in v if x)==1 else 2
        return tuple(mul*x%3 for x in v)
    permutation_orders=Counter()
    for axis in points:
        point_perm=[point_index[normalize(tuple(
            p[k]+form(p,axis)*axis[k] for k in range(4)))]
            for p in points]
        assert len(set(point_perm))==40
        octet_perm=[octet_idx[frozenset(point_perm[p] for p in s)] for s in S]
        assert len(set(octet_perm))==45
        line_perm=[lindex[frozenset(octet_perm[k] for k in line)]
                   for line in lines]
        assert len(set(line_perm))==27
        row_perm=[pairs_index[tuple(sorted((octet_perm[i],octet_perm[j])))]
                  for i,j in adjacent_pairs]
        assert len(set(row_perm))==270
        assert np.array_equal(quartic[np.ix_(row_perm,line_perm)],quartic)
        permutation_orders[len(set(line_perm))]+=1
    assert permutation_orders=={27:40}
    return {
        "status":"EXACT_QUARTIC_W33_TO_E6_FULL_27_LINE_SELECTORS",
        "prior_art":"BT766/Pass1536 gave 45 induced K4,4 octets; TOE24 and 2026-11-15 direct dictionary gave 45 octets ->27 five-clique partitions. New result: degree-four point signals multiply two rank-21 quadratic octet certificates into a FULL rank-27 one-hot 270x27 frame, including the previously dark six.",
        "nonedge_pairs_one_per_octet":len(nonedge_pairs),
        "quadratic_45x27_rank":21,"quadratic_dark_sector_dimension":6,
        "disjoint_octet_pairs":len(adjacent_pairs),
        "unique_cubic_line_per_pair":True,
        "W33_point_quartet_inputs":len(quartets),
        "quartic_270x27_rank":27,
        "quartic_dark_sextet_rank":6,
        "quartic_Gram_identity":"R^T R = 10 I_27",
        "singular_values_all":"sqrt(10) (27 copies)",
        "exact_reconstruction_identity":"R^T (R y)/10 = y for any y in R^27",
        "ten_orthogonal_replicates_per_cubic_line":10,
        "all_40_symplectic_transvections_covariant":True,
        "four_distinct_points_each_selector":True,
        "sample_point_quartet":[int(z) for z in quartets[0]],
        "sample_cubic_line_label":int(np.argmax(quartic[0])),
        "scope":"This is a combinatorial / polynomial feature map, not a deterministic single-photon quartic interaction or gauge-theoretic E6 coupling. Physical use needs joint correlation measurement or explicitly engineered nonlinear interaction; no claim of a TOE proof."
    }

if __name__=="__main__":
    o=run()
    OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS",o["status"],"rank",o["quartic_270x27_rank"],
          "dark",o["quartic_dark_sextet_rank"],flush=True)
