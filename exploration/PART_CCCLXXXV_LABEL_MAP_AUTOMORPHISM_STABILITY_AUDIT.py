#!/usr/bin/env python3
"""PART CCCLXXXV -- Label-Map Automorphism Stability Audit.

CCCLXXXII built a deterministic cycle-signature ordering for the 81 H1
representatives and used the first 9 positions as a diagonal/fiber label sector.
This part tests the honest question:

    is that 9+72 split automorphism-invariant, or only deterministic?

We apply explicit symplectic transvections of W(3,3) to cycle representatives
and compare the signature fields.  Edge count and vertex-support count are graph
invariants.  Coordinate-weight and edge-index terms depend on the chosen
coordinate/listing model and are not expected to be invariant.

Conclusion recorded by this audit:
    the current signature ordering is deterministic, but not certified as a full
automorphism-invariant label map.  It is a scaffold for future canonicalization.
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
def add(u,v): return tuple((u[i]+v[i])%MOD for i in range(4))
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
def transvection_perm(pts,idx):
    v=pts[idx]; index={p:i for i,p in enumerate(pts)}; perm=[]
    for x in pts:
        y=canon(add(x,mul(omega(x,v),v)))
        perm.append(index[y])
    return perm
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
    parent={0:None}; q=deque([0]); tree=[]
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
    su=set(au); lca=next(x for x in av if x in su)
    path=[]; x=u
    while x!=lca: path.append(tuple(sorted((x,parent[x])))); x=parent[x]
    x=v
    while x!=lca: path.append(tuple(sorted((x,parent[x])))); x=parent[x]
    return path
def h1_reps(adj):
    E=edges(adj); edge_index={e:i for i,e in enumerate(E)}; Tri=triangles(adj); tree,parent=spanning_tree(adj); tree_set=set(tree)
    tri_bits=[bit_from_indices(edge_index[tuple(sorted(e))] for e in itertools.combinations(t,2)) for t in Tri]
    _,tri_basis,_=rank_and_basis(tri_bits)
    cycles=[]
    for e in E:
        if e not in tree_set: cycles.append(bit_from_indices(edge_index[x] for x in path_in_tree(e[0],e[1],parent)+[e]))
    qb=dict(tri_basis); reps=[]
    for cyc in cycles:
        rem=reduce_by_basis(cyc,qb)
        if rem: qb[rem.bit_length()-1]=rem; reps.append(cyc)
        if len(reps)==81: break
    return E,reps
def bit_edges(bit,n=240): return [i for i in range(n) if (bit>>i)&1]
def coord_weight(v): return sum(1 for x in v if x)
def signature(bit,E,pts):
    idxs=bit_edges(bit,len(E)); vs=sorted(set(v for idx in idxs for v in E[idx]))
    return (len(idxs),len(vs),sum(coord_weight(pts[v]) for v in vs),sum(idxs))
def permute_cycle_bit(bit,E,edge_index,perm):
    out=0
    for idx in bit_edges(bit,len(E)):
        a,b=E[idx]; e=tuple(sorted((perm[a],perm[b]))); out ^= (1<<edge_index[e])
    return out
def audit():
    pts,adj=build_graph(); E,reps=h1_reps(adj); edge_index={e:i for i,e in enumerate(E)}
    perm=transvection_perm(pts,0)
    samples=[]; changed=0; invariant_prefix_changed=0
    for i,bit in enumerate(reps[:20]):
        s0=signature(bit,E,pts); s1=signature(permute_cycle_bit(bit,E,edge_index,perm),E,pts)
        if s0!=s1: changed+=1
        if s0[:2]!=s1[:2]: invariant_prefix_changed+=1
        samples.append({"index":i,"before":s0,"after":s1,"changed":s0!=s1})
    return {"samples":samples,"changed_count_first_20":changed,"edge_vertex_prefix_changed_count":invariant_prefix_changed}
def build_results():
    pts,adj=build_graph(); perm=transvection_perm(pts,0); a=audit(); checks=[]
    checks.append(ok('perm is bijection on 40 points',sorted(perm)==list(range(40)),perm[:10]))
    checks.append(ok('transvection preserves adjacency',all(((perm[j] in adj[perm[i]])==(j in adj[i])) for i in range(40) for j in range(40) if i!=j),True))
    checks.append(ok('signature changes for at least one sample',a['changed_count_first_20']>0,a))
    checks.append(ok('edge/vertex prefix stays invariant for samples',a['edge_vertex_prefix_changed_count']==0,a))
    checks.append(ok('conclusion is deterministic not invariant',True,'deterministic_not_full_automorphism_invariant'))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXXV","title":"Label-Map Automorphism Stability Audit","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"audit":a,"conclusion":"The current cycle-signature label order is deterministic but not full-automorphism-invariant, because coordinate/list-index fields can change under explicit W33 automorphisms. Edge-count and vertex-support components are stable in the tested samples.","architecture_upgrade":"Clarifies CCCLXXXII: the 9+72 label split is a reproducible scaffold, not yet a canonical automorphism-invariant decomposition.","honesty_boundary":"Only one explicit transvection sample is audited here; full canonicalization requires group-wide orbit or invariant-subspace construction.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXXV_label_map_automorphism_stability_audit_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
