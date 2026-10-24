#!/usr/bin/env python3
"""Physical architecture bridge: W33 forty 4-port optical line buses have
Q(4,3) as their LINE-INTERSECTION graph, dual to W's point graph.

Computes exact 40x40 dual adjacency and explicit graph-isomorphism mapping
to independently constructed Q(4,3) quadric. Hence cheaper rank-8 oracle
is naturally indexed by forty W33 line-bus physical addresses. No actual
40-bus optical phase couplers constructed.
"""
from __future__ import annotations
import json,hashlib,sys
from pathlib import Path
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_linebus_switch_matrix_20261023 import LINES,THROUGH
from w33_pass76_cospectral_mates import build_Q43
from w33_phase_oracle_mod_local_gauge_rank14_20261023 import rank_factor,centered
from w33_phase_oracle_seven_symplectic_pairs_20261023 import pairs_from_alternating

def bus_dual():
    assert len(LINES)==40 and all(len(x)==4 for x in LINES)
    E=np.zeros((40,40),np.uint8)
    for i,L in enumerate(LINES):
        for j in range(i+1,40):
            common=set(L)&set(LINES[j])
            assert len(common)<=1
            if common:E[i,j]=E[j,i]=1
    assert E.shape==(40,40) and np.all(E.sum(axis=1)==12)
    assert np.array_equal(E.astype(int)@E.astype(int),
      8*np.eye(40,dtype=int)-2*E.astype(int)+4*np.ones((40,40),dtype=int))
    for pt,buses in THROUGH.items():
        assert len(buses)==4
        for a in buses:
            for b in buses:
                if a!=b:assert E[a,b]
    return E

def certificate():
    E=bus_dual()
    Q=build_Q43()[1].astype(np.uint8)
    matcher=nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(E),nx.from_numpy_array(Q))
    assert matcher.is_isomorphic()
    mapping=matcher.mapping
    assert set(mapping)==set(range(40)) and set(mapping.values())==set(range(40))
    for i in range(40):
        for j in range(40):
            assert int(E[i,j])==int(Q[mapping[i],mapping[j]])
    B=centered(E)
    rank=rank_factor(E)[0].shape[1]
    gaugerank=rank_factor(B)[0].shape[1]
    pairs=pairs_from_alternating(B)
    assert rank==10 and gaugerank==8 and len(pairs)==4
    # Under duality, a Q(4,3) POINT is a W33 LINE; this is the candidate
    # for a native forty-bus phase-control circuit. It is NOT an optical
    # interaction already available just by sharing a point.
    return {'schema':'w33.line_bus_dual_q43_phase_geometry.v1',
       'forty_W33_line_buses':40,'four_port_rails_per_bus':4,
       'W33_physical_line_bus_reference':'analysis/w33_fractal_linebus_switch_matrix_20261023.py',
       'Q43_point_count':40,'line_bus_intersection_graph_isomorphic_to_Q43':True,
       'bus_to_parabolic_quadric_point_permutation':[mapping[i] for i in range(40)],
       'bus_intersection_adjacency_E':E.astype(int).tolist(),
       'physical_line_bus_dual_binary_adjacency_rank':rank,
       'optimal_local_gauge_cross_phase_rank':gaugerank,
       'symplectic_pair_count':len(pairs),
       'point_graph_W33_gauge_rank':14,
       'bus_dual_Q43_gauge_rank':8,
       'physical_limitation':'Bus intersection is a combinatorial incidence, not automatic coherent photon coupler; no 40-bus phase oracle fabricated',
       'physics_interpretation':'W33 points (two-qutrit Pauli lines) and W33 optical 4-port line buses carry different rank resources despite cospectral mode entropy. Q43 is dual of W33, not a foreign device graph.',
       'prior_art':'Generalized quadrangle W(3,3) duality with Q(4,3) is established; new artifact is exact isomorphism/address permutation tying the previous W33 physical bus manifest to the rank-8 phase compiler.'}
if __name__=='__main__':
    x=certificate()
    x['sha256']=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    (ROOT/'data/w33_linebus_dual_q43_phase_geometry_20261023.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
    print('PASS 40 native line buses = Q43 points via explicit isomorphism; 10 raw/8 gauge rank, four pairs')
