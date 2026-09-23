#!/usr/bin/env python3
"""Bridge canonical E6-id cubic labels to the current physical-Clifford H27 address gauge.

Two exact 27-point gauges coexist in the repository:

1. canonical E6-id labels 0..26 carrying the signed 45-term E6 cubic;
2. the current regular H27 address gauge (a,b,c)=Z^a X^b omega^c selected by
   the physical Clifford-648 dictionary.

They are isomorphic incidence geometries but are NOT the identity labeling.
This producer finds the deterministic gauge permutation by requiring:

* e6id 0 -> H27 identity (0,0,0);
* all 45 canonical cubic triads map to the 45 current five-direction right cosets;
* the canonical firewall bad-nine spread maps to the nine current center cosets.

The resulting map is then the correct object-level bridge for Fourier/compiler
questions in the current H27 gauge.
"""
from __future__ import annotations

import itertools,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e6id_current_h27_gauge_bridge.json"
CANON=ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json"

def hmul(g,h):
    a,b,c=g; A,B,C=h
    return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)

def right_cosets_H(subgroup):
    H=tuple(itertools.product(range(3),repeat=3))
    unseen=set(H);out=[]
    while unseen:
        g=min(unseen)
        C=frozenset(hmul(g,x) for x in subgroup)
        out.append(C);unseen-=C
    return out

def adjacency(triads):
    A=[[False]*27 for _ in range(27)]
    for t in triads:
        for i,j in itertools.combinations(t,2):
            A[i][j]=A[j][i]=True
    return A

def main(write=True):
    canonical=json.loads(CANON.read_text())
    addr=json.loads((ROOT/"data/w33_e8_matter81_h27_address_operator_compiler.json").read_text())
    affine=json.loads((ROOT/"artifacts/e6_cubic_affine_heisenberg_model.json").read_text())

    tri_can=[tuple(sorted(map(int,x["triple"]))) for x in canonical["solution"]["d_triples"]]
    bad_can=[tuple(sorted(map(int,t))) for t in affine["fiber_triads_e6id"]]
    assert len(set(tri_can))==45 and len(set(bad_can))==9

    H=tuple(itertools.product(range(3),repeat=3))
    hindex={h:i for i,h in enumerate(H)}
    current_triads=[]
    direction_triads=[]
    for row in addr["address_space"]["selected_base_directions"]:
        g=tuple(map(int,row["generator"]))
        S=frozenset(((0,0,0),g,hmul(g,g)))
        lines=[tuple(sorted(hindex[x] for x in C)) for C in right_cosets_H(S)]
        assert len(lines)==9
        direction_triads.append(lines)
        current_triads.extend(lines)
    assert len(set(current_triads))==45
    center_triads=direction_triads[0]

    Ac=adjacency(tri_can); At=adjacency(current_triads)
    fcan=[None]*27; fcur=[None]*27
    for k,t in enumerate(bad_can):
        for v in t:fcan[v]=k
    for k,t in enumerate(center_triads):
        for v in t:fcur[v]=k
    assert all(x is not None for x in fcan+fcur)

    mapping=[-1]*27;used=[False]*27
    mapping[0]=0;used[0]=True
    nodes=0

    def fiber_ok(v,w):
        for u in range(27):
            if mapping[u]>=0:
                if (fcan[u]==fcan[v]) != (fcur[mapping[u]]==fcur[w]):
                    return False
        return True

    def compatible(v,w):
        if used[w] or not fiber_ok(v,w):return False
        for u in range(27):
            if mapping[u]>=0 and Ac[v][u]!=At[w][mapping[u]]:
                return False
        return True

    def dfs(depth):
        nonlocal nodes
        nodes+=1
        if depth==27:return True
        best_v=None; best_candidates=None
        for v in range(27):
            if mapping[v]>=0:continue
            C=[w for w in range(27) if compatible(v,w)]
            if not C:return False
            if best_candidates is None or len(C)<len(best_candidates):
                best_v=v;best_candidates=C
                if len(C)==1:break
        assert best_v is not None and best_candidates is not None
        for w in best_candidates:
            mapping[best_v]=w;used[w]=True
            if dfs(depth+1):return True
            used[w]=False;mapping[best_v]=-1
        return False

    assert dfs(1)
    assert nodes==27
    e6_to_h=[H[i] for i in mapping]
    assert len(set(e6_to_h))==27 and e6_to_h[0]==(0,0,0)

    mapped45={tuple(sorted(mapping[v] for v in t)) for t in tri_can}
    mapped9={tuple(sorted(mapping[v] for v in t)) for t in bad_can}
    current45=set(current_triads); center9=set(center_triads)
    assert mapped45==current45
    assert mapped9==center9

    address_to_frame={
      tuple(map(int,k.split(","))):int(v)
      for k,v in addr["address_space"]["address_to_complete_frame"].items()
    }
    e6_to_frame=[address_to_frame[h] for h in e6_to_h]
    assert len(set(e6_to_frame))==27 and e6_to_frame[0]==0

    out={
      "schema":"w33.e6id_current_h27_gauge_bridge.v1",
      "status":"PASS_CANONICAL_E6ID_CUBIC_GAUGE_IS_EXPLICITLY_CONJUGATED_TO_CURRENT_PHYSICAL_CLIFFORD_H27_GAUGE",
      "headline":"The canonical signed E6 cubic and the current physical-Clifford H27 address chart are now connected by an explicit 27-point permutation. With e6id 0 anchored at H27 identity and the canonical bad-nine spread required to map to the current central spread, deterministic constraint propagation fixes a bijection that sends all 45 canonical cubic triads exactly to the 45 current five-direction right cosets and all nine firewall fibers exactly to the nine current center cosets.",
      "anchors":{
        "canonical_e6id":0,
        "current_H27_address":[0,0,0],
        "complete_frame":0,
        "bad9_target":"current pure-center direction <(0,0,1)>"
      },
      "search":{
        "method":"MRV backtracking on the colored GQ(2,4) point graph with fiber-spread preservation",
        "search_nodes":nodes,
        "deterministic_candidate_order":"lexicographic H27 address order"
      },
      "maps":{
        "e6id_to_current_H27_address":{str(i):list(e6_to_h[i]) for i in range(27)},
        "e6id_to_complete_frame":{str(i):e6_to_frame[i] for i in range(27)}
      },
      "incidence":{
        "canonical_cubic_triads":45,
        "current_address_lines":45,
        "mapped_full45_equal":True,
        "canonical_firewall_fibers":9,
        "current_center_cosets":9,
        "mapped_bad9_equal":True
      },
      "gauge_consequence":"Pass1103's older Heisenberg coordinates remain a valid exact gauge for the canonical cubic, but compiler Fourier coordinates must use this explicit bridge before applying the current physical-Clifford H27 Schrodinger representation.",
      "boundary":"This is a finite gauge conjugacy fixed by explicit anchors. The anchored incidence isomorphism is a coordinate choice, not a dynamical vacuum selection or an assertion that the two earlier coordinate tables were literally identical.",
      "parents":[
        "extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json",
        "artifacts/e6_cubic_affine_heisenberg_model.json",
        "data/w33_e8_matter81_h27_address_operator_compiler.json"
      ],
      "checks":{
        "27_point_bijection":True,
        "anchor_e6id0_to_identity":True,
        "full45_exact":True,
        "bad9_to_current_center_exact":True,
        "complete_frame_map_bijective":True,
        "old_and_current_gauges_not_identified":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":print(json.dumps(main(True),indent=2))
