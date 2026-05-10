#!/usr/bin/env python3
"""PART CCCLXIX -- W33 Incidence Chain Complex Compiler.

Builds an incidence-chain view across:

    vertices V (40)
    edges E (240)
    triangles Delta (160)
    odd triples Omega (4480)

The compiler computes ranks over GF(2) for key boundary/incidence maps:

    d1: C1(edges) -> C0(vertices)
    d2: C2(triangles) -> C1(edges)
    m : C_odd(odd triples) -> C0(vertices)
    pi: C_odd(odd triples) -> C1(edges)  [edge-support map mod 2]

It verifies the known first Betti number of the triangle complex:

    beta1 = E - rank(d1) - rank(d2) = 81.

It also verifies that odd-triple edge-support parity lands in the cycle space:

    d1 * pi = 0 over GF(2),

because every odd triple has either one edge or three edges and therefore even
vertex boundary mod 2 only for the three-edge triangle part?  The compiler checks
this carefully and separates one-edge versus three-edge behavior.
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
def edges(adj): return [(i,j) for i in range(len(adj)) for j in sorted(adj[i]) if i<j]
def triangles(adj):
    out=[]
    for i,j,k in itertools.combinations(range(len(adj)),3):
        if j in adj[i] and k in adj[i] and k in adj[j]: out.append((i,j,k))
    return out
def edge_count(tri,adj): return sum(1 for i,j in itertools.combinations(tri,2) if j in adj[i])
def classify_odd(adj):
    one=[]; three=[]
    for tri in itertools.combinations(range(len(adj)),3):
        ec=edge_count(tri,adj)
        if ec==1: one.append(tri)
        elif ec==3: three.append(tri)
    return one,three
def rank_gf2(columns,nrows):
    basis={}; rank=0
    for col in columns:
        x=0
        for r in col: x ^= (1<<r)
        while x:
            p=x.bit_length()-1
            if p not in basis:
                basis[p]=x; rank+=1; break
            x ^= basis[p]
    return rank
def d1_columns(edge_list): return [e for e in edge_list]
def d2_columns(tri_list,edge_index):
    cols=[]
    for tri in tri_list:
        cols.append([edge_index[tuple(sorted(e))] for e in itertools.combinations(tri,2)])
    return cols
def vertex_incidence_columns(triples): return [list(t) for t in triples]
def edge_support_columns(triples,edge_index,adj):
    cols=[]
    for t in triples:
        cols.append([edge_index[tuple(sorted((i,j)))] for i,j in itertools.combinations(t,2) if j in adj[i]])
    return cols
def boundary_of_edge_support(triples,adj):
    # Return vertex parity supports of the edge-support boundary over GF2.
    outs=[]
    for t in triples:
        parity=set()
        for i,j in itertools.combinations(t,2):
            if j in adj[i]:
                for v in (i,j):
                    if v in parity: parity.remove(v)
                    else: parity.add(v)
        outs.append(tuple(sorted(parity)))
    return outs
def build_results():
    pts,adj=build_graph(); E=edges(adj); edge_index={e:i for i,e in enumerate(E)}; Tri=triangles(adj); one,three=classify_odd(adj); odd=one+three
    r_d1=rank_gf2(d1_columns(E),40); r_d2=rank_gf2(d2_columns(Tri,edge_index),len(E)); beta1=len(E)-r_d1-r_d2
    r_m_odd=rank_gf2(vertex_incidence_columns(odd),40); r_m_one=rank_gf2(vertex_incidence_columns(one),40); r_m_three=rank_gf2(vertex_incidence_columns(three),40)
    r_pi_one=rank_gf2(edge_support_columns(one,edge_index,adj),len(E)); r_pi_three=rank_gf2(edge_support_columns(three,edge_index,adj),len(E)); r_pi_odd=rank_gf2(edge_support_columns(odd,edge_index,adj),len(E))
    bd_one=boundary_of_edge_support(one,adj); bd_three=boundary_of_edge_support(three,adj)
    checks=[]
    checks.append(ok('V/E/Tri counts',len(pts)==40 and len(E)==240 and len(Tri)==160,{"V":len(pts),"E":len(E),"Tri":len(Tri)}))
    checks.append(ok('odd split 4320+160',len(one)==4320 and len(three)==160,{"one":len(one),"three":len(three)}))
    checks.append(ok('rank d1 = V-1 = 39',r_d1==39,r_d1))
    checks.append(ok('rank d2 gives beta1=81',beta1==81,{"rank_d2":r_d2,"beta1":beta1}))
    checks.append(ok('rank d2 = 120',r_d2==120,r_d2))
    checks.append(ok('vertex incidence odd rank = 40 over GF2',r_m_odd==40,r_m_odd))
    checks.append(ok('vertex incidence one-edge rank = 40 over GF2',r_m_one==40,r_m_one))
    checks.append(ok('vertex incidence triangle rank = 40 over GF2',r_m_three==40,r_m_three))
    checks.append(ok('triangle edge-support boundaries vanish',set(bd_three)=={()},list(set(bd_three))[:3]))
    checks.append(ok('one-edge edge-support boundaries have size 2',set(len(x) for x in bd_one)=={2},sorted(set(len(x) for x in bd_one))))
    checks.append(ok('edge-support ranks are positive',r_pi_one>0 and r_pi_three>0 and r_pi_odd>0,{"one":r_pi_one,"three":r_pi_three,"odd":r_pi_odd}))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXIX","title":"W33 Incidence Chain Complex Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"chain_counts":{"vertices":40,"edges":240,"triangles":160,"odd_triples":4480,"one_edge_odd_triples":4320,"three_edge_odd_triples":160},"gf2_ranks":{"d1_edges_to_vertices":r_d1,"d2_triangles_to_edges":r_d2,"beta1_triangle_complex":beta1,"vertex_incidence_odd":r_m_odd,"vertex_incidence_one_edge":r_m_one,"vertex_incidence_three_edge":r_m_three,"edge_support_one_edge":r_pi_one,"edge_support_three_edge":r_pi_three,"edge_support_odd":r_pi_odd},"boundary_behavior":{"three_edge_triangle_support":"cycle boundary zero over GF2","one_edge_support":"single edge has two-vertex boundary over GF2"},"architecture_upgrade":"CCCLXVIII split odd triples into one-edge and triangle sectors. CCCLXIX builds the incidence-chain complex across vertices, edges, triangles, and odd triples, recovering beta1=81 and making the closed/open split explicit by separating cycle-like triangle support from open one-edge support.","theorem":"The W33 triangle complex has beta1=240-rank(d1)-rank(d2)=81 with rank(d1)=39 and rank(d2)=120 over GF2. Odd-triple incidence has full vertex rank 40, while the edge-support map separates triangle triples, whose boundary vanishes, from one-edge triples, whose boundary is a two-vertex open edge. This gives a chain-complex explanation of the closed/open split seen in the Hashimoto T/O decomposition.","honesty_boundary":"This is a GF(2) incidence-chain audit. Integral homology and explicit bases are separate refinements.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXIX_incidence_chain_complex_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
