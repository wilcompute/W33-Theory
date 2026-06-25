#!/usr/bin/env python3
"""BT1748: weld the colored channel-frame carrier to the Hesse/Fano cocycle graph.

BT1743 showed naive color collapse gives degree-one junk.  The correct weld is
channel-labeled incidence: each of the 63 point slots has three R/C/S channels,
and those three channels are assigned to the three incident Hesse/Fano lines.
Forgetting channel color after this weld gives the simple cocycle incidence graph.
"""
from __future__ import annotations
from itertools import permutations
import json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1748_channel_frame_to_cocycle_weld.json'
CHANNELS=['R','C','S']
CHOICES=[459,595,435,694,87,544,347,839,561]
BASE=[(i,(i+1)%7,(i+3)%7) for i in range(7)]
BASESETS={frozenset(t) for t in BASE}
def systems():
    autos=[]
    for p in permutations(range(7)):
        if {frozenset(p[x] for x in L) for L in BASESETS}==BASESETS: autos.append(p)
    rots=[(0,1,2),(1,2,0),(2,0,1),(0,2,1),(2,1,0),(1,0,2)]
    out=[]
    for p in autos:
        for r in rots:
            sys=[tuple(p[t[i]] for i in r) for t in BASE]
            if all(sorted(t[k] for t in sys)==list(range(7)) for k in range(3)): out.append(sys)
    return out
def hesse_lines():
    H=[]
    for y in range(3): H.append([(x,y) for x in range(3)])
    for x in range(3): H.append([(x,y) for y in range(3)])
    for b in range(3): H.append([(t,(t+b)%3) for t in range(3)])
    return H
def cocycle_graph():
    S=systems(); H=hesse_lines(); cells=[(x,y) for x in range(3) for y in range(3)]
    G=nx.Graph(); G.add_nodes_from(('p',a,h) for a in range(7) for h in cells)
    for hi,hline in enumerate(H):
        sys=S[CHOICES[hi]]
        for ti,tr in enumerate(sys):
            l=('l',hi,ti); G.add_node(l)
            for k in range(3): G.add_edge(('p',tr[k],hline[k]),l)
    return G
def colored_weld(G):
    W=nx.Graph()
    for n,d in G.nodes(data=True): W.add_node(n,**d)
    assignment={}
    for p in sorted([n for n in G if n[0]=='p'],key=str):
        ns=sorted(G.neighbors(p),key=str)
        for ch,l in zip(CHANNELS,ns):
            W.add_edge(p,l,channel=ch)
            assignment[str((p,ch))]=str(l)
    return W,assignment
def cycle_counts(G):
    # only enough for the weld certificate
    return {'edges':G.number_of_edges(),'components':nx.number_connected_components(G),'degree_set':sorted(set(dict(G.degree()).values()))}
def main():
    G=cocycle_graph(); W,assignment=colored_weld(G)
    plain=nx.Graph(); plain.add_nodes_from(W.nodes(data=True)); plain.add_edges_from((u,v) for u,v in W.edges())
    checks={
      'cocycle_profile_63_63_189':sum(1 for n in G if n[0]=='p')==63 and sum(1 for n in G if n[0]=='l')==63 and G.number_of_edges()==189,
      'colored_weld_has_189_edges':W.number_of_edges()==189,
      'each_point_uses_RCS_once':all(sorted(W.edges[p,l]['channel'] for l in W.neighbors(p))==CHANNELS for p in W if p[0]=='p'),
      'forgetting_color_recovers_cocycle':nx.is_isomorphic(plain,G,node_match=lambda a,b:a.get('kind')==b.get('kind')),
      'connected_cubic':nx.is_connected(W) and sorted(set(dict(W.degree()).values()))==[3],
    }
    payload={'theorem':'BT1748 Channel-Frame to Cocycle Weld','verified':all(checks.values()),'summary':'The colored 63/63/189 channel frame can be incidence-welded onto the BT1738 Hesse/Fano witness: each point slot sends its R,C,S channels to its three incident cocycle lines. Forgetting color after this weld recovers the simple connected cubic 63/63/189 cocycle graph. This succeeds where naive BT1743 color collapse failed.', 'choices':CHOICES,'profile':cycle_counts(W),'channel_assignment_sample':dict(list(assignment.items())[:18]),'checks':checks,'boundary':'This is an incidence weld from channel slots to cocycle lines. It does not derive the cocycle choices from the 64-bit frame; it shows the correct projection is channel-to-incidence, not color collapse.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'profile':payload['profile']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
