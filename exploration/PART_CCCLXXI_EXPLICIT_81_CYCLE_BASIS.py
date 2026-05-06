#!/usr/bin/env python3
"""PART CCCLXXI -- Explicit 81-Cycle Homology Basis.

Extracts an explicit GF(2) basis for H1 of the W33 triangle complex.

Pipeline:
1. Build W(3,3) graph with 40 vertices, 240 edges, 160 triangles.
2. Pick a spanning tree; the 201 non-tree edges give fundamental cycle-space
   generators.
3. Compute triangle boundary rank = 120.
4. Reduce fundamental cycles modulo the triangle-boundary span.
5. Keep exactly 81 independent quotient representatives.

This gives a reproducible 81-cycle basis compatible with H1(W33)=81.
"""
from __future__ import annotations
import itertools, json
from collections import deque
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
def triangles(adj): return [(i,j,k) for i,j,k in itertools.combinations(range(len(adj)),3) if j in adj[i] and k in adj[i] and k in adj[j]]
def bit_from_indices(indices):
    x=0
    for i in indices: x ^= (1<<i)
    return x
def rank_and_basis(bits):
    basis={}; kept=[]
    for b in bits:
        x=b
        while x:
            p=x.bit_length()-1
            if p not in basis:
                basis[p]=x; kept.append(b); break
            x ^= basis[p]
    return len(basis),basis,kept
def reduce_by_basis(x,basis):
    while x:
        p=x.bit_length()-1
        if p not in basis: return x
        x ^= basis[p]
    return 0
def spanning_tree(adj):
    n=len(adj); parent={0:None}; q=deque([0]); tree=[]
    while q:
        v=q.popleft()
        for w in sorted(adj[v]):
            if w not in parent:
                parent[w]=v; tree.append(tuple(sorted((v,w)))); q.append(w)
    return tree,parent
def path_in_tree(u,v,parent):
    au=[]; x=u
    while x is not None: au.append(x); x=parent[x]
    av=[]; x=v
    while x is not None: av.append(x); x=parent[x]
    setu=set(au); lca=next(x for x in av if x in setu)
    path=[]; x=u
    while x!=lca:
        path.append(tuple(sorted((x,parent[x])))); x=parent[x]
    rev=[]; x=v
    while x!=lca:
        rev.append(tuple(sorted((x,parent[x])))); x=parent[x]
    return path+rev
def fundamental_cycles(adj,E,edge_index):
    tree,parent=spanning_tree(adj); tree_set=set(tree); cycles=[]
    for e in E:
        if e not in tree_set:
            cyc_edges=path_in_tree(e[0],e[1],parent)+[e]
            cycles.append(bit_from_indices(edge_index[x] for x in cyc_edges))
    return cycles,tree
def triangle_boundaries(Tri,edge_index):
    bits=[]
    for tri in Tri:
        bits.append(bit_from_indices(edge_index[tuple(sorted(e))] for e in itertools.combinations(tri,2)))
    return bits
def quotient_h1_basis(adj):
    E=edges(adj); edge_index={e:i for i,e in enumerate(E)}; Tri=triangles(adj)
    tri_bits=triangle_boundaries(Tri,edge_index); rank_tri,tri_basis,_=rank_and_basis(tri_bits)
    cycles,tree=fundamental_cycles(adj,E,edge_index)
    reps=[]; quotient_basis=dict(tri_basis)
    for cyc in cycles:
        rem=reduce_by_basis(cyc,quotient_basis)
        if rem:
            p=rem.bit_length()-1; quotient_basis[p]=rem; reps.append(cyc)
        if len(reps)==81: break
    return {"E":E,"Tri":Tri,"tree":tree,"cycles":cycles,"rank_tri":rank_tri,"h1_reps":reps}
def bit_weight(x): return x.bit_count()
def build_results():
    pts,adj=build_graph(); data=quotient_h1_basis(adj); checks=[]
    checks.append(ok('vertices/edges/triangles',len(pts)==40 and len(data['E'])==240 and len(data['Tri'])==160,{"V":len(pts),"E":len(data['E']),"T":len(data['Tri'])}))
    checks.append(ok('spanning tree has 39 edges',len(data['tree'])==39,len(data['tree'])))
    checks.append(ok('fundamental cycle count = 201',len(data['cycles'])==201,len(data['cycles'])))
    checks.append(ok('triangle boundary rank = 120',data['rank_tri']==120,data['rank_tri']))
    checks.append(ok('H1 representative count = 81',len(data['h1_reps'])==81,len(data['h1_reps'])))
    checks.append(ok('beta1 identity 201-120=81',len(data['cycles'])-data['rank_tri']==81,len(data['cycles'])-data['rank_tri']))
    weights=[bit_weight(x) for x in data['h1_reps']]
    checks.append(ok('representative weights positive',min(weights)>0,{"min":min(weights),"max":max(weights)}))
    verified=all(c['passed'] for c in checks)
    sample=[]
    for idx,bit in enumerate(data['h1_reps'][:8]):
        edges_idx=[i for i in range(len(data['E'])) if (bit>>i)&1]
        sample.append({"basis_index":idx,"edge_count":len(edges_idx),"edge_indices_first_20":edges_idx[:20]})
    return {"part":"CCCLXXI","title":"Explicit 81-Cycle Homology Basis","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"counts":{"vertices":40,"edges":240,"triangles":160,"spanning_tree_edges":len(data['tree']),"fundamental_cycles":len(data['cycles']),"triangle_boundary_rank":data['rank_tri'],"h1_basis_size":len(data['h1_reps'])},"basis_rule":"spanning-tree fundamental cycles reduced modulo triangle-boundary span over GF2","sample_basis_representatives":sample,"architecture_upgrade":"CCCLXIX recovered beta1=81. CCCLXXI extracts an explicit reproducible 81-cycle quotient basis from fundamental graph cycles modulo triangle boundaries.","theorem":"The W33 triangle complex has a GF2 H1 basis of 81 representatives obtained by reducing the 201 spanning-tree fundamental cycles modulo the 120-dimensional triangle-boundary span. This gives an explicit cycle-basis realization of the H1(W33)=81 matter-scale sector.","honesty_boundary":"This is a GF2 basis. Integral basis and torsion audit are handled separately.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXI_explicit_81_cycle_basis_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
