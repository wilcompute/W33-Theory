#!/usr/bin/env python3
"""PART CCCLXX -- Open-Turn / Two-Edge Triple Isomorphism.

This part corrects and sharpens the odd-triple/open-turn bridge.

A Hashimoto open turn is an ordered nonbacktracking path

    a -> b -> c

with a~b, b~c, a != c, and a not adjacent to c.  Therefore its underlying
3-vertex induced subgraph has exactly TWO graph edges, not one.

Thus the canonical bijection is:

    open Hashimoto turns  <->  oriented two-edge triples.

There are 2160 two-edge triples.  Each has a unique middle vertex and two
orientations, hence 2*2160 = 4320 open turns.

The 4320 one-edge odd triples are not canonically the open turns in the graph;
they are the complement-dual parity partner, because a one-edge triple in G is a
two-edge triple in the complement graph.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
Vector=Tuple[int,int,int,int]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def mul(a,u): return tuple((a*u[i])%MOD for i in range(4))
def omega(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%MOD
def canon(v):
    for a in v:
        if a%MOD: return mul(1 if a==1 else 2,v)
    raise ValueError('zero')
def points():
    pts=[]; seen=set()
    for v in itertools.product(range(MOD), repeat=4):
        if v==(0,0,0,0): continue
        c=canon(v)
        if c not in seen: seen.add(c); pts.append(c)
    return pts
def build_graph():
    pts=points(); adj=[set() for _ in pts]
    for i,j in itertools.combinations(range(len(pts)),2):
        if omega(pts[i],pts[j])==0: adj[i].add(j); adj[j].add(i)
    return pts,adj
def edge_count(tri,adj): return sum(1 for i,j in itertools.combinations(tri,2) if j in adj[i])
def triples_by_edge_count(adj):
    d={0:[],1:[],2:[],3:[]}
    for tri in itertools.combinations(range(len(adj)),3): d[edge_count(tri,adj)].append(tri)
    return d
def middle_vertex(two_edge_triple,adj):
    deg={v:0 for v in two_edge_triple}
    for i,j in itertools.combinations(two_edge_triple,2):
        if j in adj[i]: deg[i]+=1; deg[j]+=1
    mids=[v for v,d in deg.items() if d==2]
    if len(mids)!=1: raise ValueError('not a two-edge path triple')
    return mids[0]
def oriented_open_turns_from_two_edge_triple(tri,adj):
    b=middle_vertex(tri,adj); endpoints=[v for v in tri if v!=b]
    return [(endpoints[0],b,endpoints[1]),(endpoints[1],b,endpoints[0])]
def all_open_turns(adj):
    turns=[]
    for a in range(len(adj)):
        for b in adj[a]:
            for c in adj[b]:
                if c!=a and c not in adj[a]: turns.append((a,b,c))
    return sorted(turns)
def mapped_open_turns(adj):
    turns=[]
    for tri in triples_by_edge_count(adj)[2]: turns.extend(oriented_open_turns_from_two_edge_triple(tri,adj))
    return sorted(turns)
def complement_edge_count(tri,adj): return 3-edge_count(tri,adj)
def build_results():
    pts,adj=build_graph(); by=triples_by_edge_count(adj); direct=all_open_turns(adj); mapped=mapped_open_turns(adj); checks=[]
    checks.append(ok('triple distribution', {k:len(v) for k,v in by.items()}=={0:3240,1:4320,2:2160,3:160}, {k:len(v) for k,v in by.items()}))
    checks.append(ok('two-edge triples = 2160',len(by[2])==2160,len(by[2])))
    checks.append(ok('open turns = 4320',len(direct)==4320,len(direct)))
    checks.append(ok('two orientations per two-edge triple',2*len(by[2])==len(direct),{"two_edge":len(by[2]),"open":len(direct)}))
    checks.append(ok('canonical mapped turns equal direct open turns',mapped==direct,True))
    checks.append(ok('one-edge triples are count-equal but not direct support',len(by[1])==len(direct),{"one_edge":len(by[1]),"open":len(direct)}))
    checks.append(ok('one-edge triples are complement two-edge triples',all(complement_edge_count(t,adj)==2 for t in by[1]),True))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXX","title":"Open-Turn / Two-Edge Triple Isomorphism","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"triple_distribution":{str(k):len(v) for k,v in by.items()},"canonical_isomorphism":"open Hashimoto turns <-> oriented two-edge triples","counts":{"two_edge_triples":len(by[2]),"oriented_two_edge_triples":2*len(by[2]),"open_turns":len(direct),"one_edge_odd_triples":len(by[1])},"correction":"one-edge odd triples have the same count as open turns but are complement-dual, not the canonical graph-open-turn support","architecture_upgrade":"CCCLXVIII matched counts. CCCLXX constructs the exact canonical bijection: each two-edge triple has a unique middle vertex and two orientations, giving precisely the 4320 open Hashimoto turns.","theorem":"In W(3,3), the canonical support of an open Hashimoto turn is a two-edge induced triple. The map from a two-edge triple to its two endpoint orientations around the unique middle vertex is a bijection onto all open nonbacktracking turns. One-edge odd triples are count-equal because they are two-edge triples in the complement graph.","honesty_boundary":"This corrects the earlier count-only bridge. Any use of one-edge odd triples for open dynamics requires an explicit complement-duality map, not the direct Hashimoto support map.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXX_open_turn_two_edge_triple_isomorphism_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
