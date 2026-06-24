#!/usr/bin/env python3
"""BT1738: improved Hesse/Fano girth-8 cocycle witness with 44 eight-cycles."""
from __future__ import annotations
from collections import Counter
from itertools import permutations
import json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1738_hesse_fano_8cycle_44_witness.json'
BASE=[(i,(i+1)%7,(i+3)%7) for i in range(7)]
BASESETS={frozenset(t) for t in BASE}
OLD=[459,595,701,694,87,39,347,839,561]
NEW=[459,595,435,694,87,544,347,839,561]
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
def graph(choices):
    S=systems(); H=hesse_lines(); cells=[(x,y) for x in range(3) for y in range(3)]
    G=nx.Graph(); G.add_nodes_from(('p',a,h) for a in range(7) for h in cells)
    for hi,hline in enumerate(H):
        sys=S[choices[hi]]
        for ti,tr in enumerate(sys):
            l=('l',hi,ti); G.add_node(l)
            for k in range(3): G.add_edge(('p',tr[k],hline[k]),l)
    return G
def girth(G):
    best=10**9
    for s in G.nodes:
        dist={s:0}; par={s:None}; q=[s]
        for v in q:
            for w in G[v]:
                if w not in dist:
                    dist[w]=dist[v]+1; par[w]=v; q.append(w)
                elif par[v]!=w and par[w]!=v: best=min(best,dist[v]+dist[w]+1)
    return None if best==10**9 else best
def cycles(G,bound=10):
    D=nx.DiGraph()
    for u,v in G.edges(): D.add_edge(u,v); D.add_edge(v,u)
    seen=set()
    for cyc in nx.simple_cycles(D,length_bound=bound):
        if len(cyc)<3: continue
        n=len(cyc); reps=[]
        for seq in (cyc,list(reversed(cyc))):
            for i in range(n): reps.append(tuple(seq[i:]+seq[:i]))
        seen.add(min(reps,key=str))
    return dict(Counter(map(len,seen)))
def profile(choices):
    G=graph(choices); cyc=cycles(G,10)
    return {'components':nx.number_connected_components(G),'points':sum(1 for n in G if n[0]=='p'),'lines':sum(1 for n in G if n[0]=='l'),'incidences':G.number_of_edges(),'degree_set':sorted(set(dict(G.degree()).values())),'girth':girth(G),'diameter':nx.diameter(G),'cycle_counts_le_10':cyc,'cycle_rank':G.number_of_edges()-G.number_of_nodes()+nx.number_connected_components(G)}
def main():
    old=profile(OLD); new=profile(NEW)
    checks={'new_connected_cubic':new['components']==1 and new['degree_set']==[3],'new_counts_63_63_189':new['points']==63 and new['lines']==63 and new['incidences']==189,'new_girth_8':new['girth']==8,'new_no_4_or_6':new['cycle_counts_le_10'].get(4,0)==0 and new['cycle_counts_le_10'].get(6,0)==0,'eight_cycles_drop_49_to_44':old['cycle_counts_le_10'].get(8)==49 and new['cycle_counts_le_10'].get(8)==44,'ten_cycles_improve_84_to_73':old['cycle_counts_le_10'].get(10)==84 and new['cycle_counts_le_10'].get(10)==73}
    payload={'theorem':'BT1738 Hesse-Fano 44-eight-cycle cocycle witness','verified':all(checks.values()),'summary':'A two-position cocycle update improves the BT1735 witness while preserving connected cubic 63/63/189 incidence and no 4/6-cycles: 8-cycles fall from 49 to 44, and 10-cycles fall from 84 to 73. Girth remains 8, so this is another descent step, not the split-Cayley object.','old_choices':OLD,'new_choices':NEW,'old_profile':old,'new_profile':new,'mutations':[{'hesse_line_index':2,'old_system':701,'new_system':435},{'hesse_line_index':5,'old_system':39,'new_system':544}],'checks':checks,'boundary':'This improves the lexicographic obstruction objective but does not reach girth 10.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'old_8':old['cycle_counts_le_10'].get(8),'new_8':new['cycle_counts_le_10'].get(8),'new_10':new['cycle_counts_le_10'].get(10)},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
