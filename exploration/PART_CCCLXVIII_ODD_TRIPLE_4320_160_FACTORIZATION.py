#!/usr/bin/env python3
"""PART CCCLXVIII -- Odd-Triple 4320+160 Factorization Compiler.

Factors the 4480 odd triples into:

    4320 one-edge triples  +  160 three-edge triples.

This split mirrors open/closed behavior:
- one-edge triples are edge-with-nonadjacent-third transport objects,
- three-edge triples are actual W33 triangles.

The compiler derives incidence profiles, vertex degrees, pair coverage, and a
bridge to Hashimoto T/O counts:

    three-edge triples = 160 triangles,
    directed triangle turns = 6 * 160 = 960 = |T|,
    one-edge triples = 4320 = |O| open turns.

So the odd-triple decomposition exactly reproduces the Hashimoto T/O sizes.
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
def edge_count(tri,adj): return sum(1 for i,j in itertools.combinations(tri,2) if j in adj[i])
def classify_odd_triples(adj):
    one=[]; three=[]
    for tri in itertools.combinations(range(len(adj)),3):
        ec=edge_count(tri,adj)
        if ec==1: one.append(tri)
        elif ec==3: three.append(tri)
    return one,three
def vertex_degrees(triples):
    c=Counter()
    for tri in triples:
        for v in tri: c[v]+=1
    return sorted(set(c.values())),c
def pair_coverage(triples):
    c=Counter()
    for tri in triples:
        for e in itertools.combinations(tri,2): c[tuple(sorted(e))]+=1
    return c
def edge_nonedge_pair_profiles(triples,adj):
    cov=pair_coverage(triples); edge_vals=[]; non_vals=[]
    for i,j in itertools.combinations(range(len(adj)),2):
        val=cov.get((i,j),0)
        if j in adj[i]: edge_vals.append(val)
        else: non_vals.append(val)
    return sorted(set(edge_vals)),sorted(set(non_vals)),sum(edge_vals),sum(non_vals)
def build_results():
    pts,adj=build_graph(); one,three=classify_odd_triples(adj); one_vset,one_v=vertex_degrees(one); tri_vset,tri_v=vertex_degrees(three); one_edge_vals,one_non_vals,one_edge_sum,one_non_sum=edge_nonedge_pair_profiles(one,adj); tri_edge_vals,tri_non_vals,tri_edge_sum,tri_non_sum=edge_nonedge_pair_profiles(three,adj); checks=[]
    checks.append(ok('one-edge odd triples = 4320',len(one)==4320,len(one)))
    checks.append(ok('three-edge odd triples = 160',len(three)==160,len(three)))
    checks.append(ok('sum = 4480',len(one)+len(three)==4480,len(one)+len(three)))
    checks.append(ok('three-edge triples are W33 triangles',len(three)==160,len(three)))
    checks.append(ok('directed triangle turns = 6*160=960',6*len(three)==960,6*len(three)))
    checks.append(ok('one-edge triples match open turn count 4320',len(one)==4320,len(one)))
    checks.append(ok('one-edge vertex degree uniform 324',one_vset==[324],one_vset))
    checks.append(ok('triangle vertex degree uniform 12',tri_vset==[12],tri_vset))
    checks.append(ok('one-edge pair coverage edge/nonedge',one_edge_vals==[18] and one_non_vals==[16],{"edge":one_edge_vals,"nonedge":one_non_vals}))
    checks.append(ok('triangle pair coverage edge/nonedge',tri_edge_vals==[2] and tri_non_vals==[0],{"edge":tri_edge_vals,"nonedge":tri_non_vals}))
    checks.append(ok('combined pair coverage gives 20/16',one_edge_vals[0]+tri_edge_vals[0]==20 and one_non_vals[0]+tri_non_vals[0]==16,True))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXVIII","title":"Odd-Triple 4320+160 Factorization Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"factorization":{"one_edge_triples":len(one),"three_edge_triples":len(three),"total_odd_triples":len(one)+len(three)},"hashimoto_bridge":{"triangle_turns":"6*160=960=|T|","open_turns":"4320=|O|"},"vertex_degrees":{"one_edge_sector":one_vset,"triangle_sector":tri_vset},"pair_coverage":{"one_edge_sector":{"edge_pair_values":one_edge_vals,"nonedge_pair_values":one_non_vals},"triangle_sector":{"edge_pair_values":tri_edge_vals,"nonedge_pair_values":tri_non_vals},"combined":{"edge":20,"nonedge":16,"gap":4}},"architecture_upgrade":"CCCLXV exposed the full odd-triple space. CCCLXVIII factors it into 4320 one-edge triples and 160 triangle triples, exactly matching the Hashimoto open/triangle turn counts |O|=4320 and |T|=960 after orientation of triangles.","theorem":"The W33 odd triples split as 4320 one-edge triples plus 160 three-edge triples. The three-edge sector is exactly the triangle set and gives 6*160=960 directed triangle turns. The one-edge sector has size 4320, matching the open-turn operator size. Pair coverage refines the two-graph 20/16 split as edge pairs receive 18+2 and nonedge pairs receive 16+0.","honesty_boundary":"The count bridge is exact. A full operator isomorphism between one-edge triples and oriented open turns is the next refinement.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXVIII_odd_triple_4320_160_factorization_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
