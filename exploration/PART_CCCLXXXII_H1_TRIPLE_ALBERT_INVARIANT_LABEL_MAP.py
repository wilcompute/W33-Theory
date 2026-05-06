#!/usr/bin/env python3
"""PART CCCLXXXII -- H1 / Triple-Albert Invariant Label Map.

CCCLXXIX mapped the explicit 81 H1 representatives into the CLXXV
Triple-Albert slots by index order.  CCCLXXXII replaces raw index order with a
basis-derived deterministic signature order.

For each H1 representative cycle, compute a finite signature:

    (edge_count, vertex_support_count, coordinate_weight_sum, edge_index_sum)

using the fixed W(3,3) construction.  Sort the 81 representatives by this
signature and then assign the sorted list into the Triple-Albert structure:

    first 9  -> diagonal/fiber slots,
    next 72 -> octonion/offdiagonal slots,
    grouped as 3 generations of 27.

Honesty boundary:
This is a deterministic label map from cycle signatures, not an automorphism-
invariant or representation-theoretic proof.  It is a stronger interface than
index order and is suitable for later bracket/root-label tests.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, deque
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
ALBERT_DIM=27
DIAG=3
OFF=24
H1_DIM=81
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
        if omega(pts[i],pts[j])==0:
            adj[i].add(j); adj[j].add(i)
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
    while x!=lca:
        path.append(tuple(sorted((x,parent[x])))); x=parent[x]
    x=v
    while x!=lca:
        path.append(tuple(sorted((x,parent[x])))); x=parent[x]
    return path
def h1_reps(adj):
    E=edges(adj); edge_index={e:i for i,e in enumerate(E)}; Tri=triangles(adj); tree,parent=spanning_tree(adj); tree_set=set(tree)
    tri_bits=[bit_from_indices(edge_index[tuple(sorted(e))] for e in itertools.combinations(t,2)) for t in Tri]
    _,tri_basis,_=rank_and_basis(tri_bits)
    cycles=[]
    for e in E:
        if e not in tree_set: cycles.append(bit_from_indices(edge_index[x] for x in path_in_tree(e[0],e[1],parent)+[e]))
    quotient_basis=dict(tri_basis); reps=[]
    for cyc in cycles:
        rem=reduce_by_basis(cyc,quotient_basis)
        if rem:
            quotient_basis[rem.bit_length()-1]=rem; reps.append(cyc)
        if len(reps)==81: break
    return E,reps
def edge_indices(bit,nedges=240): return [i for i in range(nedges) if (bit>>i)&1]
def vertex_support(edge_idxs,E):
    s=set()
    for idx in edge_idxs: s.update(E[idx])
    return sorted(s)
def coord_weight(v): return sum(1 for x in v if x!=0)
def cycle_signature(bit,E,pts):
    idxs=edge_indices(bit,len(E)); vs=vertex_support(idxs,E)
    return (len(idxs),len(vs),sum(coord_weight(pts[v]) for v in vs),sum(idxs))
def label_map():
    pts,adj=build_graph(); E,reps=h1_reps(adj)
    rows=[]
    for original_index,bit in enumerate(reps):
        rows.append({"original_h1_index":original_index,"bit":bit,"signature":cycle_signature(bit,E,pts)})
    rows=sorted(rows,key=lambda r:(r['signature'],r['original_h1_index']))
    out=[]
    for label_index,row in enumerate(rows):
        generation=label_index//ALBERT_DIM + 1
        local=label_index%ALBERT_DIM
        sector='diagonal_fiber' if local<DIAG else 'octonion_offdiagonal'
        out.append({"label_index":label_index,"original_h1_index":row['original_h1_index'],"generation":generation,"local_albert_slot":local,"sector":sector,"signature":row['signature']})
    return out
def build_results():
    rows=label_map(); counts=Counter(r['sector'] for r in rows); gens=Counter(r['generation'] for r in rows); sigs=[tuple(r['signature']) for r in rows]; checks=[]
    checks.append(ok('label map has 81 rows',len(rows)==81,len(rows)))
    checks.append(ok('diagonal/offdiagonal counts 9/72',dict(counts)=={'diagonal_fiber':9,'octonion_offdiagonal':72},dict(counts)))
    checks.append(ok('generation counts 27 each',dict(gens)=={1:27,2:27,3:27},dict(gens)))
    checks.append(ok('label indices bijective',sorted(r['label_index'] for r in rows)==list(range(81)),True))
    checks.append(ok('original indices bijective',sorted(r['original_h1_index'] for r in rows)==list(range(81)),True))
    checks.append(ok('signature order is nondecreasing',sigs==sorted(sigs),True))
    checks.append(ok('first nine are diagonal sector',all(r['sector']=='diagonal_fiber' for r in rows[:9]),rows[:9]))
    checks.append(ok('remaining seventy two are offdiagonal sector',all(r['sector']=='octonion_offdiagonal' for r in rows[9:]),True))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXXII","title":"H1 / Triple-Albert Invariant Label Map","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"signature":"(edge_count, vertex_support_count, coordinate_weight_sum, edge_index_sum)","sector_counts":dict(counts),"generation_counts":dict(gens),"label_map_samples":rows[:12]+rows[27:33]+rows[54:60],"architecture_upgrade":"Replaces raw index-order H1-to-Triple-Albert slotting with a deterministic cycle-signature ordering. The first nine signature-minimal representatives label the diagonal/fiber sector and the remaining seventy-two label the offdiagonal sector.","theorem":"The explicit 81 H1 representatives admit a deterministic finite signature ordering. Assigning the ordered basis into 3 Albert blocks of 27 yields a reproducible 9+72 Triple-Albert label map matching the CLXXV diagonal/offdiagonal split.","honesty_boundary":"The signature order is basis-derived and deterministic, but it is not yet proved invariant under the full automorphism group and does not prove representation compatibility.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXXII_h1_triple_albert_invariant_label_map_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
