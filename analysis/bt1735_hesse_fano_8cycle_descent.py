#!/usr/bin/env python3
"""BT1735: descend the Hesse/Fano cocycle obstruction from 54 to 49 8-cycles."""
from __future__ import annotations
from collections import Counter
from itertools import permutations
import json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1735_hesse_fano_8cycle_descent.json'
BASE=[(i,(i+1)%7,(i+3)%7) for i in range(7)]
BASESETS={frozenset(t) for t in BASE}
OLD=[459,595,363,694,87,39,347,839,561]
NEW=[459,595,701,694,87,39,347,839,561]
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
def profile(ch):
    G=graph(ch); cyc=cycles(G,10)
    return {'components':nx.number_connected_components(G),'points':sum(1 for n in G if n[0]=='p'),'lines':sum(1 for n in G if n[0]=='l'),'incidences':G.number_of_edges(),'degree_set':sorted(set(dict(G.degree()).values())),'girth':girth(G),'diameter':nx.diameter(G),'cycle_counts_le_10':cyc,'cycle_rank':G.number_of_edges()-G.number_of_nodes()+nx.number_connected_components(G)}
def main():
    old=profile(OLD); new=profile(NEW)
    checks={'new_connected_cubic':new['components']==1 and new['degree_set']==[3],'new_counts_63_63_189':new['points']==63 and new['lines']==63 and new['incidences']==189,'girth_stays_8':new['girth']==8,'four_six_still_zero':new['cycle_counts_le_10'].get(4,0)==0 and new['cycle_counts_le_10'].get(6,0)==0,'eight_cycles_reduced_54_to_49':old['cycle_counts_le_10'].get(8)==54 and new['cycle_counts_le_10'].get(8)==49,'ten_cycle_cost_75_to_84':old['cycle_counts_le_10'].get(10)==75 and new['cycle_counts_le_10'].get(10)==84}
    payload={'theorem':'BT1735 Hesse-Fano 8-cycle descent certificate','verified':all(checks.values()),'summary':'A single cocycle mutation improves the split-Cayley waypoint: the witness remains connected, cubic, 63/63/189, and free of 4- and 6-cycles, while the 8-cycle count drops from 54 to 49. The tradeoff is that 10-cycles rise from 75 to 84, so the next search should optimize a lexicographic objective: kill 8-cycles first, then minimize 10-cycles.','old_choices':OLD,'new_choices':NEW,'old_profile':old,'new_profile':new,'mutation':{'hesse_line_index':2,'old_system':363,'new_system':701},'checks':checks,'boundary':'This does not reach girth 10; it is a verified descent step on the girth-8 obstruction layer.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'old_8':old['cycle_counts_le_10'].get(8),'new_8':new['cycle_counts_le_10'].get(8),'new_10':new['cycle_counts_le_10'].get(10)},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
