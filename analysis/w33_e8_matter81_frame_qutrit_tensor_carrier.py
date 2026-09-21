#!/usr/bin/env python3
"""Objectwise 81 = 27 complete-factorisation frames x 3 external qutrit phases.

This composes three already-certified layers without changing their gauges:
  * MCCCXC: an E8 matter 81 factors as 27 E6 minuscule weights x 3 A2 lifts;
  * MCCCXCI: the 27 weights carry exactly 45 zero-sum tritangent triples;
  * Holotrade crossrepo theorem: the cubic-surface 27 are complete two-qutrit
    factorisation frames.

The new calculation makes the 81-root map explicit in one frozen coordinate
chart and checks the full cubic lift.

For coordinate=0, matter_81_coset_1:
  1. group the 81 E8 roots by their projected E6 weight;
  2. identify the 27-weight complement-Schlaefli graph with W33's independent
     27 cubic-line carrier, anchored at lexicographic weight 0 -> cubic line 0;
  3. sort the common three A2 phase pairs and label them qutrit phases 0,1,2;
  4. label every E8 root by (cubic line / complete frame, phase).

For each of the 45 zero-sum E6 triples, exhaust all 3^3 phase lifts. Exactly
six are zero-sum E8 triples, namely the six permutations of phases (0,1,2).
Hence there are 45*6=270 zero-sum E8 cubic triples and every one of the 81
roots lies in 10 of them.

The map is canonical only relative to the displayed E8 coordinate/sector and
the anchored graph-isomorphism gauge. The tensor-factorisation meaning of the
27 base objects is imported from the certified Holotrade crossrepo theorem.
"""
from __future__ import annotations
import importlib.util
import itertools
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
if str(ROOT/"analysis") not in sys.path: sys.path.insert(0,str(ROOT/"analysis"))
OUT=ROOT/"data/w33_e8_matter81_frame_qutrit_tensor_carrier.json"

from analysis.w33_e8_e6_a2_coordinate_decomposition import sectorize_by_coordinate, block_pair
from analysis.w33_e6_minuscule_27_a2_phase_factorization import project_to_e6
from analysis.w33_e6_45_tritangent_zero_sum_bridge import edge_list, triangle_list, vector_sum
from analysis.w33_tetracode_e8_root_system_bridge import inner

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def add3(a,b,c):
    return tuple(a[i]+b[i]+c[i] for i in range(len(a)))

def main(write=True):
    coordinate=0; sector_key="matter_81_coset_1"
    sectors=sectorize_by_coordinate(coordinate)
    roots=sectors[sector_key]
    assert len(roots)==81

    by_weight=defaultdict(list)
    for r in roots:
        by_weight[project_to_e6(r,coordinate)].append(r)
    weights=sorted(by_weight)
    assert len(weights)==27 and Counter(len(v) for v in by_weight.values())==Counter({3:27})

    phase_sets={tuple(sorted(block_pair(r,coordinate) for r in rs)) for rs in by_weight.values()}
    assert len(phase_sets)==1
    phases=next(iter(phase_sets))
    assert len(phases)==3
    phase_index={p:i for i,p in enumerate(phases)}

    # Complement-Schlaefli / tritangent graph on the projected weights.
    edges=edge_list(weights,Fraction(-2,3))
    triangles=triangle_list(edges,len(weights))
    assert len(edges)==135 and len(triangles)==45
    assert all(all(x==0 for x in vector_sum([weights[i] for i in t])) for t in triangles)

    WG=nx.Graph(); WG.add_nodes_from(range(27)); WG.add_edges_from(edges)
    assert set(dict(WG.degree()).values())=={10}

    common=load(ROOT/"analysis/w33_pass4992_4999_common.py","common81frame")
    base=common.build_base()
    G27=base["G27"]
    tritangents={tuple(sorted(t)) for t in base["tritangents"]}
    assert G27.number_of_nodes()==27 and G27.number_of_edges()==135 and len(tritangents)==45

    # Gauge-fix one weight and one cubic line. GraphMatcher insertion order is
    # deterministic for the frozen graphs; the theorem is explicitly gauge-relative.
    nx.set_node_attributes(WG,{i:(i==0) for i in WG},"anchor")
    nx.set_node_attributes(G27,{i:(i==0) for i in G27},"anchor")
    GM=nx.algorithms.isomorphism.GraphMatcher(WG,G27,node_match=lambda a,b:a["anchor"]==b["anchor"])
    iso=next(GM.isomorphisms_iter())
    assert iso[0]==0 and len(set(iso.values()))==27
    transported={tuple(sorted(iso[i] for i in t)) for t in triangles}
    assert transported==tritangents

    # Root -> (frame, qutrit phase) is a bijection.
    root_records=[]
    keyset=set()
    root_by_weight_phase={}
    for wi,w in enumerate(weights):
        for r in by_weight[w]:
            pi=phase_index[block_pair(r,coordinate)]
            key=(iso[wi],pi)
            assert key not in keyset
            keyset.add(key)
            root_by_weight_phase[(wi,pi)]=r
            root_records.append({
              "root":[str(x) for x in r],
              "weight_index":wi,
              "complete_frame":iso[wi],
              "external_qutrit_phase":pi,
              "a2_phase_pair":[str(x) for x in block_pair(r,coordinate)]
            })
    assert len(keyset)==81
    assert keyset=={(f,p) for f in range(27) for p in range(3)}

    # Lift every base tritangent through all 27 phase assignments.
    lifted=[]
    phase_pattern=Counter()
    per_root=Counter()
    per_base=Counter()
    for t in triangles:
        for ps in itertools.product(range(3),repeat=3):
            rr=[root_by_weight_phase[(t[k],ps[k])] for k in range(3)]
            if all(x==0 for x in add3(*rr)):
                base_tri=tuple(sorted(iso[i] for i in t))
                phase_pattern[tuple(sorted(ps))]+=1
                per_base[base_tri]+=1
                for k in range(3): per_root[(iso[t[k]],ps[k])]+=1
                lifted.append({"base_tritangent":list(base_tri),"phases":list(ps)})
    assert len(lifted)==270
    assert set(per_base.values())=={6} and len(per_base)==45
    assert set(per_root.values())=={10} and len(per_root)==81
    assert phase_pattern==Counter({(0,1,2):270})
    assert all(len(set(x["phases"]))==3 for x in lifted)

    cross=json.loads((ROOT/"data/w33_qutrit_frame_mu12_bundle_carrier_crossrepo.json").read_text())
    assert cross["status"]=="PASS_CROSSREPO_OBJECTWISE_27_FRAME_FIBREWISE_MU12_CARRIER"

    out={
      "schema":"w33.e8_matter81_frame_qutrit_tensor_carrier.v1",
      "status":"PASS_E8_MATTER81_EQUALS_27_COMPLETE_FRAMES_X_3_EXTERNAL_QUTRIT_PHASES",
      "headline":"One frozen E8 matter-81 chart now has a literal bijection root <-> (complete two-qutrit factorisation frame, external A2/qutrit phase). The projected 27 weights map by an anchored graph isomorphism to the independent W33 cubic-line carrier, which the crossrepo theorem identifies with the 27 complete factorisation frames. Each frame has exactly three A2 lifts. The 45 E6 zero-sum tritangents lift to exactly 270 E8 zero-sum triples: six per tritangent, precisely the six permutations using phases 0,1,2 once each. Every one of the 81 roots lies in ten such triples.",
      "chart":{"coordinate":coordinate,"sector":sector_key,"root_count":81,"base_weight_count":27,"phase_count":3},
      "tensor_factorization":{
        "identity":"81 = 27 complete two-qutrit factorisation frames x 3 external qutrit phases",
        "root_to_frame_phase_bijective":True,
        "phase_pairs":[[str(x) for x in p] for p in phases],
        "weight_to_complete_frame":{str(i):iso[i] for i in range(27)}
      },
      "cubic_lift":{
        "base_tritangents":45,
        "phase_assignments_tested_per_tritangent":27,
        "zero_sum_E8_triples":270,
        "zero_sum_lifts_per_base_tritangent":6,
        "allowed_phase_multiset":[0,1,2],
        "rule":"an E6 zero-sum tritangent lifts to an E8 zero-sum triple iff the three roots use the three distinct external qutrit phases",
        "triples_per_root":10,
        "factorization":"270 = 45 * 3!; 10 = 5 base tritangents per frame * 2 phase completions"
      },
      "operational_reading":"The E8 matter shell is a frame register tensored with one external qutrit label at the object-set level. Cubic/root-addition incidence is not arbitrary across the qutrit factor: it is the antisymmetric phase-conservation rule using one of each of the three A2 weights.",
      "root_records":root_records,
      "boundary":"The complete-frame numbering is an anchored coordinate gauge, not a canonical physical generation label. This is a finite root/incidence/tensor-label theorem; it does not provide a Hilbert-space tensor-product factorization of the full E8 adjoint representation, a Yukawa coefficient, or a vacuum.",
      "parents":[
        "analysis/w33_e6_minuscule_27_a2_phase_factorization.py",
        "analysis/w33_e6_45_tritangent_zero_sum_bridge.py",
        "data/w33_qutrit_frame_mu12_bundle_carrier_crossrepo.json"
      ],
      "checks":{
        "81_to_27x3_bijection":True,
        "transported_45_tritangents_exact":True,
        "270_zero_sum_E8_cubic_triples":True,
        "six_phase_permutations_per_tritangent":True,
        "ten_cubic_triples_per_root":True
      }
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","chart","tensor_factorization","cubic_lift")},indent=2))
    return out

if __name__=="__main__": main(True)
