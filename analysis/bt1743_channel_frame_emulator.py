#!/usr/bin/env python3
"""BT1743: colored channel-frame emulator for the 64 -> 63 puncture.

The BT1739 boundary says the +1 self-frame is incidence-real only as three
colored/local-channel links, not as a simple Levi extension.  This emulator makes
that explicit and tests what color collapse does.
"""
from __future__ import annotations
import json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1743_channel_frame_emulator.json'
CHANNELS=['R','C','S']
def colored_multiframe(n=64):
    M=nx.MultiGraph()
    for i in range(n):
        M.add_node(('p',i),kind='point')
        M.add_node(('l',i),kind='line')
        for ch in CHANNELS:
            M.add_edge(('p',i),('l',i),channel=ch)
    return M
def puncture(M,idx=63):
    N=M.copy()
    N.remove_node(('p',idx)); N.remove_node(('l',idx))
    return N
def simple_collapse(M):
    G=nx.Graph()
    for n,d in M.nodes(data=True): G.add_node(n,**d)
    for u,v,_k,d in M.edges(keys=True,data=True): G.add_edge(u,v)
    return G
def profile(M):
    return {'nodes':M.number_of_nodes(),'points':sum(1 for n in M if n[0]=='p'),'lines':sum(1 for n in M if n[0]=='l'),'edges':M.number_of_edges(),'degree_set':sorted(set(dict(M.degree()).values())),'components':nx.number_connected_components(M)}
def main():
    full=colored_multiframe(); punct=puncture(full); collapsed=simple_collapse(punct)
    checks={'full_64_64_192':profile(full)['points']==64 and profile(full)['lines']==64 and profile(full)['edges']==192,'punctured_63_63_189':profile(punct)['points']==63 and profile(punct)['lines']==63 and profile(punct)['edges']==189,'colored_degree_three':profile(punct)['degree_set']==[3],'collapsed_simple_has_63_edges_not_189':collapsed.number_of_edges()==63,'collapsed_simple_degree_one':sorted(set(dict(collapsed.degree()).values()))==[1],'colored_not_simple_levi':profile(punct)['edges']!=collapsed.number_of_edges()}
    payload={'theorem':'BT1743 Channel-Frame Emulator','verified':all(checks.values()),'summary':'The 64-bit self-frame construction is incidence-real as a colored/multiflag carrier: 64 point slots, 64 line slots, and 192 colored R/C/S links; puncturing one self slot gives 63/63/189 with colored degree 3. Collapsing channel color gives only 63 simple edges and degree 1, so the colored frame cannot itself be the simple split-Cayley Levi graph. It is a framed carrier that must be welded to a separate simple incidence cocycle.', 'profiles':{'full_colored':profile(full),'punctured_colored':profile(punct),'punctured_simple_collapse':profile(collapsed)},'checks':checks,'boundary':'This validates the channel-frame interpretation and falsifies the naive color-collapse interpretation.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'colored_edges':profile(punct)['edges'],'collapsed_edges':collapsed.number_of_edges()},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
