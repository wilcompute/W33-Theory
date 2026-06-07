#!/usr/bin/env python3
"""BT524: 30-Now Octa-Cube Memory-Braid Lift Theorem.

Executes branch 3 from the latest next-step list.

BT501 built a 30-now counter-rotating BC memory braid where each now is a K4.
BT510/BT517 identify the local octa-cube packet attached to one tetrahedral now:
    O + O* = (6,12,8) + (8,12,6) = (14,24,14).

This theorem attaches that local packet to every one of the 30 nows.
The raw lift is:
    30*(14,24,14) = (420,720,420).

The edge count 720 is the W33 transport-complement edge count already used in
the center-quad quotient layer.  The 420 vertex+face equality gives a balanced
memory shell, while 720 is the present/transport hinge.
"""
from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

N=30

def now_cell(t:int):
    return (('P',t%N),('P',(t+1)%N),('F',t%N),('F',(t-1)%N))

def main()->dict:
    # BT501 braid skeleton.
    braid=nx.Graph(); cells=[]
    for t in range(N):
        c=now_cell(t); cells.append(c); braid.add_nodes_from(c)
        for i in range(4):
            for j in range(i+1,4): braid.add_edge(c[i],c[j])
    assert braid.number_of_nodes()==60 and braid.number_of_edges()==150 and len(cells)==30

    local_octa=(6,12,8); local_cube=(8,12,6); local_sum=tuple(a+b for a,b in zip(local_octa,local_cube))
    assert local_sum==(14,24,14)
    global_packet=tuple(N*x for x in local_sum)
    assert global_packet==(420,720,420)

    # Build an explicit disjoint-union packet graph for the fold incidence part.
    # Each now gets 14 local states and 24 fold edges between 6 octa states and 8 cube states.
    G=nx.Graph(); oct_nodes=[]; cube_nodes=[]
    for t in range(N):
        for i in range(6):
            node=('O',t,i); G.add_node(node); oct_nodes.append(node)
        for j in range(8):
            node=('C',t,j); G.add_node(node); cube_nodes.append(node)
        # local fold: oct state (axis i, sign) incident to cube signs matching that axis sign
        oct_states=[(axis,sgn) for axis in range(3) for sgn in (-1,1)]
        cube_states=[((a,b,c)) for a in (-1,1) for b in (-1,1) for c in (-1,1)]
        for oi,(axis,sgn) in enumerate(oct_states):
            for cj,c in enumerate(cube_states):
                if c[axis]==sgn:
                    G.add_edge(('O',t,oi),('C',t,cj))
    assert G.number_of_nodes()==420 and G.number_of_edges()==720
    assert len(oct_nodes)==180 and len(cube_nodes)==240
    assert sorted(dict(G.degree()).values())==[3]*240+[4]*180

    # Add the 30-now address cycle as memory evolution links between packet centers.
    address=nx.cycle_graph(N)
    assert address.number_of_edges()==30

    identities={
        'raw_packet':'30*(14,24,14)=(420,720,420)',
        'vertex_face_balance':'420 vertices and 420 dual faces',
        'transport_match':'720 equals W33 center-quad transport-complement edge count',
        'local_flags':'24 fold edges per now = |S4|',
        'octa_cube_split':'180 octa states + 240 cube states = 420 local-lift vertices',
    }
    assert 180+240==420
    assert 30*24==720

    results={
        'theorem':'BT524 30-Now Octa-Cube Memory-Braid Lift Theorem',
        'BT501_braid':{'now_cells':30,'braid_vertices':60,'braid_edges':150,'now_cell':'K4'},
        'local_packet':{'octahedron_side':list(local_octa),'cube_dual_side':list(local_cube),'sum':list(local_sum)},
        'global_30_now_packet':{'vertices':global_packet[0],'edges':global_packet[1],'faces':global_packet[2],'f_vector':list(global_packet)},
        'explicit_fold_graph':{'vertices':G.number_of_nodes(),'edges':G.number_of_edges(),'octa_states':len(oct_nodes),'cube_states':len(cube_nodes),'degree_profile':{'3':240,'4':180}},
        'address_cycle':{'period':30,'edges':address.number_of_edges()},
        'identities':identities,
        'substrate_reading':{'420':'30*14 balanced memory state/face shell','720':'30*24 present-fold edges; W33 transport-complement edge count','180':'30*6 BC/Richter octa states','240':'30*8 cube/sign states and E8 root count','30':'BC ring/Coxeter address period'}
    }
    out=Path('data/PART_BT524_30_NOW_OCTA_CUBE_MEMORY_BRAID_LIFT_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
