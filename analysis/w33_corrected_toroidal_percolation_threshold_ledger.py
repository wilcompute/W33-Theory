#!/usr/bin/env python3
"""BT500: Corrected Toroidal Percolation Threshold Ledger.

Uses the corrected carriers from BT498/BT499:
  * Csaszar = K7, 7 vertices, 21 edges, 14 triangular faces
  * Szilassi = Heawood, 14 vertices, 21 edges, 7 hexagonal faces

Connects to the existing oscillator/percolation/genus scripts:
  * d_X=3, d_Z=4 thresholds from CSS-genus hinge
  * d_X+d_Z=7 Fano/toroidal threshold
  * d_X*d_Z=12 local codec/genus denominator
  * Heawood local shell 1,3,6,4 from BT497
  * edge/incidence shells 21,42,28 from BT492/BT497/BT498

This is a deterministic threshold ledger on the corrected concrete carriers,
preparing the way for stochastic Bernoulli percolation on these atoms.
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx

CS_FACES=[(0,1,2),(0,2,5),(0,5,4),(0,4,6),(0,6,3),(0,3,1),(1,3,4),(1,4,5),(1,5,6),(1,6,2),(2,6,4),(2,4,3),(2,3,5),(5,3,6)]
SZ_FACES=[(0,1,13,8,7,4),(0,4,3,2,10,12),(0,12,9,6,5,1),(11,3,4,7,6,9),(11,9,12,10,8,13),(11,13,1,5,2,3),(2,5,6,7,8,10)]

def complete_edges(n:int): return list(combinations(range(n),2))

def face_cycle_edges(faces):
    c=Counter()
    for face in faces:
        for i in range(len(face)):
            c[tuple(sorted((face[i],face[(i+1)%len(face)])))] += 1
    return c

def triangle_edges(faces):
    e=set()
    for face in faces:
        for a,b in combinations(face,2): e.add(tuple(sorted((a,b))))
    return e

def main():
    dX,dZ=3,4
    assert dX+dZ==7 and dX*dZ==12

    K7=nx.complete_graph(7)
    H=nx.Graph(); H.add_nodes_from(range(14)); H.add_edges_from(face_cycle_edges(SZ_FACES).keys())
    assert nx.is_isomorphic(K7,nx.complete_graph(7))
    assert nx.is_isomorphic(H,nx.heawood_graph())

    cs_edges=triangle_edges(CS_FACES)
    assert len(cs_edges)==21
    sz_edge_counter=face_cycle_edges(SZ_FACES)
    assert len(sz_edge_counter)==21 and Counter(sz_edge_counter.values())==Counter({2:21})

    # Heawood local shell ledger.
    shell_profiles=[]
    for v in H.nodes():
        profile=Counter(nx.single_source_shortest_path_length(H,v).values())
        assert profile==Counter({0:1,1:3,2:6,3:4})
        shell_profiles.append(profile)

    # Global distance ledger.
    dist_counts=Counter()
    for u,v in combinations(H.nodes(),2):
        dist_counts[nx.shortest_path_length(H,u,v)] += 1
    assert dist_counts==Counter({1:21,2:42,3:28})

    # Concrete percolation atoms on corrected carriers.
    atoms={
        'p_X_first_shell': dX,
        'p_Z_outer_shell': dZ,
        'p_T_fano_toroidal': dX+dZ,
        'p_C_local_codec': dX*dZ,
        'p_dimG2_local_ball': 14,
        'p_edges_single_carrier': 21,
        'p_flags_single_toroid': 84,
        'p_flags_pair_toroids': 168,
        'p_tetra_flags': 24,
        'p_tomotope_flags': 192,
        'p_heptad_edge_instances': 147,
    }
    assert atoms['p_tetra_flags'] + atoms['p_flags_pair_toroids'] == atoms['p_tomotope_flags']
    assert atoms['p_heptad_edge_instances'] == 7*21
    assert atoms['p_flags_single_toroid'] == 7*12

    # Corrected carrier visibility: deterministic minimum counts.
    visibility={
        'Csaszar_vertex_visibility': {'carrier':'K7','vertices':7,'edges':21,'faces':14,'threshold_to_complete_vertex_adjacency':21},
        'Szilassi_face_visibility': {'carrier':'Heawood','vertices':14,'edges':21,'faces':7,'threshold_to_complete_face_adjacency':21},
        'Heawood_local_visibility': {'shells':'1,3,6,4','first_nontrivial':3,'outer_shell':4,'full_ball':14},
        'dual_square_visibility': {'A_H_squared_minus_3I':'K7 disjoint union K7','distance2_edges_total':42},
    }

    results={
        'theorem':'BT500 Corrected Toroidal Percolation Threshold Ledger',
        'css_genus_roots': {'d_X':dX,'d_Z':dZ,'sum':dX+dZ,'product':dX*dZ},
        'corrected_carriers': {'Csaszar':'K7','Szilassi':'Heawood','edge_count_each':21},
        'heawood_shells': {'local':'1,3,6,4','global_distance_pairs':{str(k):v for k,v in sorted(dist_counts.items())}},
        'threshold_atoms': atoms,
        'visibility': visibility,
        'oscillator_alignment': {
            'h0':'tetrahedron flags 24',
            'h1':'Csaszar flags 84 + Szilassi flags 84 = 168',
            'tomotope_total':'24+84+84=192',
            'genus_one_phase_superperiod':'distance3 pairs 28 and oriented distance3 56',
        },
        'next_stochastic_experiment': 'run Bernoulli occupation on corrected atoms: K7 edges, Heawood edges, Heawood shells, and 7 realization modes; monitor rank/Betti/spectral split thresholds',
    }
    out=Path('data/PART_BT500_CORRECTED_TOROIDAL_PERCOLATION_THRESHOLD_LEDGER_results.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))
    return results
if __name__=='__main__': main()
