#!/usr/bin/env python3
"""BT1741: local rigidity census around the BT1738 44-eight-cycle cocycle.

This continues from BT1738.  It exhaustively scans every one-coordinate mutation
of the 9 Hesse-line cocycle choices, retaining only connected cubic 63/63/189
incidence graphs with no 4-cycles and no 6-cycles.  None improves the current
lexicographic score (8-cycles, 10-cycles, diameter) = (44,73,9).
"""
from __future__ import annotations
from collections import Counter, defaultdict
from itertools import permutations
import json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1741_cocycle_local_rigidity.json'
BASE=[(i,(i+1)%7,(i+3)%7) for i in range(7)]
BASESETS={frozenset(t) for t in BASE}
W=[459,595,435,694,87,544,347,839,561]
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
S=systems(); H=hesse_lines(); CELLS=[(x,y) for x in range(3) for y in range(3)]
def graph(ch):
    G=nx.Graph(); G.add_nodes_from(('p',a,h) for a in range(7) for h in CELLS)
    for hi,hline in enumerate(H):
        sys=S[ch[hi]]
        for ti,tr in enumerate(sys):
            l=('l',hi,ti); G.add_node(l)
            for k in range(3): G.add_edge(('p',tr[k],hline[k]),l)
    return G
def count_cycles_len(G,L):
    nodes=list(G.nodes()); idx={v:i for i,v in enumerate(nodes)}
    adj=[[idx[w] for w in G.neighbors(v)] for v in nodes]
    count=0
    for s in range(len(nodes)):
        path=[s]; seen={s}
        def dfs(v,depth):
            nonlocal count
            if depth==L:
                if s in adj[v] and path[1] < path[-1]: count += 1
                return
            for w in adj[v]:
                if w==s or w<s or w in seen: continue
                seen.add(w); path.append(w); dfs(w,depth+1); path.pop(); seen.remove(w)
        dfs(s,1)
    return count
def score(ch):
    G=graph(ch)
    if not nx.is_connected(G): return None
    if set(dict(G.degree()).values())!={3}: return None
    if G.number_of_edges()!=189 or sum(1 for n in G if n[0]=='p')!=63 or sum(1 for n in G if n[0]=='l')!=63: return None
    if count_cycles_len(G,4) or count_cycles_len(G,6): return None
    return (count_cycles_len(G,8), count_cycles_len(G,10), nx.diameter(G))
def main():
    base=score(W)
    assert base==(44,73,9)
    hist=Counter(); viable=[]; checked=0
    for pos in range(9):
        for val in range(len(S)):
            if val==W[pos]: continue
            ch=list(W); ch[pos]=val; checked+=1
            sc=score(ch)
            if sc is not None:
                hist[sc]+=1
                if sc <= base: viable.append({'score':sc,'position':pos,'value':val,'choices':ch})
    best=min(hist) if hist else None
    checks={'fano_systems_1008':len(S)==1008,'base_score_44_73_9':base==(44,73,9),'one_mutations_checked':checked==9*(1008-1),'viable_no_4_6_count_222':sum(hist.values())==222,'no_one_step_improvement':best>=base,'base_only_at_best_or_ties':all(tuple(x['score'])>=base for x in viable)}
    payload={'theorem':'BT1741 cocycle local rigidity census','verified':all(checks.values()),'summary':'Exhaustive one-coordinate mutation around the BT1738 Hesse/Fano cocycle finds 222 connected cubic 63/63/189 candidates with no 4/6-cycles among 9063 mutations, but none improves the current score (44 eight-cycles, 73 ten-cycles, diameter 9). The descent now requires coordinated multi-position mutation or a different cocycle parameterization.','base_choices':W,'base_score':base,'mutations_checked':checked,'viable_candidates_no_4_6':sum(hist.values()),'best_one_mutation_score':best,'score_histogram':{str(k):v for k,v in sorted(hist.items())},'nonworse_candidates':viable[:20],'checks':checks,'boundary':'This is a local rigidity certificate, not a global impossibility theorem.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'checked':checked,'viable':sum(hist.values()),'base_score':base,'best_one_mutation_score':best},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
