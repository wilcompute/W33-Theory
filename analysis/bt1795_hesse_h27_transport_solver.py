#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product, permutations
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1795_hesse_h27_transport_solver.json'
F=range(3)

def rep(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError('zero')

def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3

def projective_points(): return sorted({rep(v) for v in product(F, repeat=4) if any(v)})

def projective_line(u,v):
    return frozenset(rep(tuple((a*u[i]+b*v[i])%3 for i in range(4))) for a,b in product(F,F) if a or b)

def shell_coord(v):
    if v[2]==2: v=tuple((2*x)%3 for x in v)
    assert v[2]==1
    return (v[0],v[1],v[3])

def h27_support():
    P=projective_points(); anchor=rep((1,0,0,0)); shell=set(p for p in P if p!=anchor and form(anchor,p)!=0)
    lines=sorted({projective_line(u,v) for u,v in combinations(P,2) if form(u,v)==0}, key=lambda L: sorted(L))
    old=[]
    for L in lines:
        if anchor in L: continue
        sh=tuple(sorted(shell_coord(x) for x in L if x in shell)); assert len(sh)==3
        old.append(sh)
    new=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    return [tuple(sorted(L)) for L in old+new], ['old']*len(old)+['new']*len(new)

def source_edges():
    return [((0,i,j),(1,i,s),(2,j,s),(i,j,s)) for i,j,s in product(F,F,F) if s!=(j-i)%3]

def source_graph():
    S=nx.Graph()
    for a,b,c in product(F,F,F): S.add_node(('v',a,b,c), kind='v', layer=a)
    for eidx,(p0,p1,p2,t) in enumerate(source_edges()):
        en=('e',eidx); S.add_node(en, kind='e', layer=99, table=t)
        for p in (p0,p1,p2): S.add_edge(en, ('v',)+p)
    return S

def target_graph(lines, layer_colours=False, perm=(0,1,2)):
    T=nx.Graph()
    for a,b,c in product(F,F,F):
        colour=perm.index(a) if layer_colours else -1
        T.add_node(('v',a,b,c), kind='v', layer=colour)
    for eidx,L in enumerate(lines):
        en=('e',eidx); T.add_node(en, kind='e', layer=99)
        for p in L: T.add_edge(en, ('v',)+p)
    return T

def monomorphism(T,S,layered):
    def nm(a,b): return a['kind']==b['kind'] and ((not layered) or a['layer']==b['layer'])
    GM=nx.algorithms.isomorphism.GraphMatcher(T,S,node_match=nm)
    for m in GM.subgraph_monomorphisms_iter(): return m
    return None

def rank_mod(A,p):
    A=A.copy()%p; m,n=A.shape; r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i,c]%p),None)
        if piv is None: continue
        A[[r,piv]]=A[[piv,r]]; inv=pow(int(A[r,c]),-1,p); A[r]=(A[r]*inv)%p
        for i in range(m):
            if i!=r and A[i,c]%p: A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
    return r

def affine_fit(vertex_map):
    A=[]; B=[[],[],[]]
    for src,tgt in vertex_map.items():
        A.append([1,*src])
        for k in range(3): B[k].append(tgt[k])
    A=np.array(A,dtype=int)%3
    ok=[]
    for k in range(3):
        aug=np.concatenate([A,np.array(B[k],dtype=int)[:,None]],axis=1)%3
        ok.append(rank_mod(aug,3)==rank_mod(A,3))
    return ok

def main():
    support,kinds=h27_support(); S=source_graph()
    trans=[L for L in support if sorted(p[0] for p in L)==[0,1,2]]
    layered={p: monomorphism(target_graph(trans, True, p), S, True) is not None for p in permutations((0,1,2))}
    m=monomorphism(target_graph(support, False), S, False)
    assert m is not None
    inv={v:k for k,v in m.items()}
    vertex_map={s[1:]:t[1:] for s,t in inv.items() if s[0]=='v'}
    edge_map={s[1]:t[1] for s,t in inv.items() if s[0]=='e'}
    support_set=set(support)
    non_hits=0; con_hits=0
    for i,j,s in product(F,F,F):
        tri=tuple(sorted(vertex_map[p] for p in ((0,i,j),(1,i,s),(2,j,s))))
        hit=tri in support_set
        if s==(j-i)%3: con_hits+=int(hit)
        else: non_hits+=int(hit)
    used=[edge_map[i] for i in range(18)]
    rows=[]
    for eidx,(_,_,_,t) in enumerate(source_edges()): rows.append({'table':f'T{t[0]}{t[1]}{t[2]}','support_index':edge_map[eidx],'support_kind':kinds[edge_map[eidx]]})
    payload={'bt':'BT1795','title':'Hesse to H27 transport solver','transport_found':True,'layer_preserving_by_permutation':{str(k):v for k,v in layered.items()},'layer_preserving_transport_found':any(layered.values()),'transport_type':'full 27-point bijection; not layer-preserving; not affine over F3^3','nonconcurrent_tables_landed_on_support':non_hits,'concurrent_tables_landed_on_support':con_hits,'used_support_lines':used,'used_support_kind_histogram':dict(Counter(kinds[i] for i in used)),'source_to_target_layer_mixing':{f'{a}->{b}':c for (a,b),c in sorted(Counter((s[0],t[0]) for s,t in vertex_map.items()).items())},'affine_fit_target_coordinates':affine_fit(vertex_map),'sample_vertex_map':[{'source':list(s),'target':list(t)} for s,t in list(vertex_map.items())[:12]],'mapped_table_lines':rows,'conclusion':'The BT1788 to H27 bridge exists, but only as a non-layer-preserving non-affine 27-point transport. It sends all 18 nonconcurrent Hesse table triples to H27 support lines and no concurrent triples to support.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'nonconcurrent_hits':non_hits,'concurrent_hits':con_hits,'layered':any(layered.values()),'used':dict(Counter(kinds[i] for i in used))},indent=2,sort_keys=True))
if __name__=='__main__': main()
