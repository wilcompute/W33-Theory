#!/usr/bin/env python3
"""BT517: Cl8 Local Octa-Cube Fold Theorem.

This executes Next Idea 2 from BT515 without claiming the unread paper.

The local radial-dual packet has 14 states:
  6 octahedron vertices  ±e_i      (K4-edge / BC-axis channels)
  8 cube vertices        (±1,±1,±1) (signed Xmin / octahedron-face states)

Define the fold-incidence matrix B[6,8] by containment of an octahedron
vertex in a cube face: ±e_i is incident to cube vertex s=(s1,s2,s3) iff s_i
has the matching sign.  This is the local Cl8-style sign fold.

Exact facts:
  row degree 4, column degree 3, total flags 24=|S4|;
  rank(B)=4;
  B B^T has spectrum 12^1 + 4^3 + 0^2;
  the 14-state bipartite fold graph has spectrum ±2sqrt(3), ±2^3, 0^6;
  it is a (6,8,24)-incidence carrier whose total state count is 14=dim(G2).
"""
from __future__ import annotations

import itertools, json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np


def main()->dict:
    oct_states=[(i,s) for i in range(3) for s in (-1,1)]
    cube_states=list(itertools.product([-1,1], repeat=3))
    B=np.zeros((6,8),dtype=int)
    for oi,(i,s) in enumerate(oct_states):
        for cj,c in enumerate(cube_states):
            if c[i]==s: B[oi,cj]=1
    assert Counter(B.sum(axis=1))==Counter({4:6})
    assert Counter(B.sum(axis=0))==Counter({3:8})
    assert int(B.sum())==24
    assert np.linalg.matrix_rank(B.astype(float))==4

    BBt=B@B.T; BtB=B.T@B
    bb_spec=Counter(int(round(x)) for x in np.linalg.eigvalsh(BBt.astype(float)))
    bt_spec=Counter(int(round(x)) for x in np.linalg.eigvalsh(BtB.astype(float)))
    assert bb_spec==Counter({0:2,4:3,12:1})
    assert bt_spec==Counter({0:4,4:3,12:1})

    A=np.block([[np.zeros((6,6),dtype=int),B],[B.T,np.zeros((8,8),dtype=int)]])
    eig=np.linalg.eigvalsh(A.astype(float))
    eig_round=Counter(round(float(x),10) for x in eig)
    # Store symbolic spectrum separately.
    assert A.shape==(14,14)
    assert np.linalg.matrix_rank(A.astype(float))==8

    G=nx.Graph(); G.add_nodes_from([('O',x) for x in range(6)]); G.add_nodes_from([('C',x) for x in range(8)])
    for i,j in zip(*np.nonzero(B)): G.add_edge(('O',int(i)),('C',int(j)))
    assert G.number_of_nodes()==14 and G.number_of_edges()==24
    assert nx.is_bipartite(G)
    assert sorted(dict(G.degree()).values())==[3]*8+[4]*6

    results={
        'theorem':'BT517 Cl8 Local Octa-Cube Fold Theorem',
        'local_states':{'octahedron_side':6,'cube_dual_side':8,'total':14},
        'fold_matrix':{'shape':[6,8],'row_degree':4,'column_degree':3,'total_flags':24,'rank':4},
        'spectra':{'BBt':{'12':1,'4':3,'0':2},'BtB':{'12':1,'4':3,'0':4},'bipartite_fold':'(+/-2sqrt(3))^1, (+/-2)^3, 0^6'},
        'graph':{'vertices':14,'edges':24,'degree_profile':{'3':8,'4':6},'bipartite':True},
        'interpretation':{'Cl8_style':'8 cube-sign states folded against 6 octahedral axis signs','G2_packet':'6+8=14 local states','S4_flags':'24 incidences are tetrahedral flag count'},
        'substrate_reading':{'14':'dim(G2) local octa-cube state count','24':'|S4| flags / fold incidences','4':'fold rank and tetrahedron vertex count','8':'cube signed face states / Cl8 sign layer'}
    }
    out=Path('data/PART_BT517_CL8_LOCAL_OCTA_CUBE_FOLD_results.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))
    return results

if __name__=='__main__': main()
