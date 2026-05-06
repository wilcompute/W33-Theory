#!/usr/bin/env python3
"""PART CCCLXXXI -- Direct vs Complement Open Dynamics.

Compares direct W33 open Hashimoto turns with complement-open dynamics.

Direct graph G:
    open turns = oriented two-edge triples in G = 4320.

Complement graph Gbar:
    open turns = oriented two-edge triples in Gbar = 8640.

Since one-edge triples in G are exactly two-edge triples in Gbar, the one-edge
odd-triple sector of G maps to complement-open dynamics, not direct open
dynamics.  This compiler builds both open-turn sets, compares size/degree
profiles, and records the exact duality.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
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
def open_turns(adj):
    out=[]
    for a in range(len(adj)):
        for b in adj[a]:
            for c in adj[b]:
                if c!=a and c not in adj[a]: out.append((a,b,c))
    return out
def turn_middle_profile(turns): return Counter(b for a,b,c in turns)
def turn_start_profile(turns): return Counter(a for a,b,c in turns)
def line_graph_state_count(adj): return sum(len(row) for row in adj)
def build_results():
    pts,G=build_graph(); C=complement(G); byG=triples_by_edge_count(G); byC=triples_by_edge_count(C); turnsG=open_turns(G); turnsC=open_turns(C); midG=turn_middle_profile(turnsG); midC=turn_middle_profile(turnsC); checks=[]
    checks.append(ok('direct open turns G = 4320',len(turnsG)==4320,len(turnsG)))
    checks.append(ok('complement open turns = 8640',len(turnsC)==8640,len(turnsC)))
    checks.append(ok('complement doubles direct open turns',len(turnsC)==2*len(turnsG),{"G":len(turnsG),"C":len(turnsC)}))
    checks.append(ok('G two-edge triples orient to direct open turns',2*len(byG[2])==len(turnsG),{"two_edge_G":len(byG[2]),"turnsG":len(turnsG)}))
    checks.append(ok('G one-edge triples orient to complement open turns',2*len(byG[1])==len(turnsC),{"one_edge_G":len(byG[1]),"turnsC":len(turnsC)}))
    checks.append(ok('middle profile G uniform 108',set(midG.values())=={108},sorted(set(midG.values()))))
    checks.append(ok('middle profile complement uniform 216',set(midC.values())=={216},sorted(set(midC.values()))))
    checks.append(ok('directed edge states G/complement',line_graph_state_count(G)==480 and line_graph_state_count(C)==1080,{"G":line_graph_state_count(G),"C":line_graph_state_count(C)}))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXXI","title":"Direct vs Complement Open Dynamics","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"direct_G":{"directed_edges":line_graph_state_count(G),"open_turns":len(turnsG),"middle_turns_per_vertex":sorted(set(midG.values())),"support":"oriented two-edge triples in G"},"complement_G":{"directed_edges":line_graph_state_count(C),"open_turns":len(turnsC),"middle_turns_per_vertex":sorted(set(midC.values())),"support":"oriented two-edge triples in complement(G), equivalently oriented one-edge triples in G"},"triple_distributions":{"G":{str(k):len(v) for k,v in byG.items()},"complement":{str(k):len(v) for k,v in byC.items()}},"architecture_upgrade":"CCCLXXIV separated direct W33 open turns from complement-dual one-edge triples. CCCLXXXI compares the two open dynamics systems and shows complement-open dynamics doubles the direct open-turn count, with uniform middle profiles 216 versus 108.","theorem":"Direct W33 open dynamics has 4320 turns supported by oriented two-edge triples in G. Complement-open dynamics has 8640 turns supported by oriented two-edge triples in complement(G), equivalently oriented one-edge triples in G. Thus the one-edge odd-triple sector naturally belongs to complement-open dynamics, not direct Hashimoto dynamics.","honesty_boundary":"This compares turn sets and uniform profiles. A full spectral comparison of the corresponding open-turn transition operators is a further refinement.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXXI_direct_complement_open_dynamics_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
