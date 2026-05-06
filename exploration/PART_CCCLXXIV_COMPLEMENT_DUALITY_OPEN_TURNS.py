#!/usr/bin/env python3
"""PART CCCLXXIV -- Complement-Duality Map for Open Turns.

CCCLXX corrected the direct graph statement:

    open turns in G <-> oriented two-edge triples in G.

This part explains the equal count of one-edge triples in G:

    one-edge triples in G <-> two-edge triples in complement(G).

Thus one-edge odd triples are the complement-dual support of open turns in the
complement graph.  The compiler constructs the complement graph, verifies its
triple distribution, and gives the canonical bijection

    one-edge triples in G -> two-edge triples in Gbar -> open turns in Gbar.
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
def complement(adj):
    n=len(adj); return [set(j for j in range(n) if j!=i and j not in adj[i]) for i in range(n)]
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
    if len(mids)!=1: raise ValueError('not two-edge')
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
def mapped_complement_open_turns_from_one_edge_G(adj):
    comp=complement(adj); one=triples_by_edge_count(adj)[1]; out=[]
    for tri in one: out.extend(oriented_open_turns_from_two_edge_triple(tri,comp))
    return sorted(out)
def build_results():
    pts,adj=build_graph(); comp=complement(adj); byG=triples_by_edge_count(adj); byC=triples_by_edge_count(comp); directC=all_open_turns(comp); mapped=mapped_complement_open_turns_from_one_edge_G(adj); checks=[]
    checks.append(ok('G triple distribution', {k:len(v) for k,v in byG.items()}=={0:3240,1:4320,2:2160,3:160}, {k:len(v) for k,v in byG.items()}))
    checks.append(ok('complement triple distribution reversed', {k:len(v) for k,v in byC.items()}=={0:160,1:2160,2:4320,3:3240}, {k:len(v) for k,v in byC.items()}))
    checks.append(ok('one-edge triples in G equal two-edge triples in complement',len(byG[1])==len(byC[2])==4320,{"G1":len(byG[1]),"C2":len(byC[2])}))
    checks.append(ok('complement open turns = 8640',len(directC)==8640,len(directC)))
    checks.append(ok('one-edge G triples orient to complement open turns subset',len(mapped)==2*len(byG[1])==8640,len(mapped)))
    checks.append(ok('mapped complement open turns equal direct complement open turns',mapped==directC,True))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXIV","title":"Complement-Duality Map for Open Turns","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"G_triple_distribution":{str(k):len(v) for k,v in byG.items()},"complement_triple_distribution":{str(k):len(v) for k,v in byC.items()},"duality":"one-edge triples in G are exactly two-edge triples in complement(G)","complement_open_turns":len(directC),"mapped_turns":len(mapped),"architecture_upgrade":"CCCLXX corrected direct open turns as oriented two-edge triples in G. CCCLXXIV explains the one-edge 4320 count as complement-dual: one-edge triples in G are two-edge triples in complement(G), and orient to all complement-open turns.","theorem":"For any triple, edge_count_G + edge_count_complement = 3. Therefore one-edge triples in W33 correspond exactly to two-edge triples in the complement graph. Orienting around the unique middle vertex gives a bijection from one-edge triples of G, with two orientations each, to the open Hashimoto turns of complement(G).","honesty_boundary":"This is a complement-dynamics bridge, not the direct W33 Hashimoto open-turn bridge. Direct W33 open turns remain oriented two-edge triples in G.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXIV_complement_duality_open_turns_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
