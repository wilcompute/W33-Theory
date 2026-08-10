#!/usr/bin/env python3
"""Pass 4662 (outside box) — recover the E6 45 from the code alone.

Pass4658 derived a code-intrinsic SRG(36,15,6,6) on the 36 minimum words of
C=[135,16,30]_2 using joint Jacobi profiles against the weight-45 shell.  This
pass uses only that intrinsic 36-graph to manufacture a 45-carrier:

  * it has exactly 135 maximal K4 cliques;
  * the anticompleteness graph on those K4s is 2-regular with 45 components C3;
  * the union of the three K4s in each component is a 12-subset of the 36
    minimum words, giving 45 objects.

The internal PSp action is transitive on these 45 objects with stabilizer 576.
That stabilizer fixes exactly one protected 16-line support, giving a unique
PSp-equivariant bijection to the Pass4585/4616 protected E6-tritangent 45.
Thus the code alone reconstructs the 45 after its own Jacobi graph is formed.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry, build_line_perm, nullspace2, perm_group, transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4662_CODE_INTRINSIC_45_K4_TRIANGLE_REGEN.json'

def pmask(mask,p):
    y=0; x=int(mask)
    while x:
        b=x&-x; i=b.bit_length()-1; x^=b; y|=1<<p[i]
    return y

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry(); Astar=np.asarray(Astar,dtype=np.uint8); n=40; j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(n) for k in range(i+1,n) if Astar[i,k]])
    V=set(span(B9)); rep=lambda x:min(int(x),int(x)^j)
    def ap_fiber(ap):
        x=0
        for i in ap:x^=cols[int(i)]
        return rep(x)
    def ap_line(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        s=rep(cols[opp[0][0]]^cols[opp[0][1]]); t=rep(cols[opp[1][0]]^cols[opp[1][1]])
        return tuple(sorted((s,t,ap_fiber(ap))))
    selected=sorted({ap_line(ap) for ap in apartments});sing=sorted(set().union(*(set(L) for L in selected)));sidx={x:i for i,x in enumerate(sing)}
    N=np.zeros((135,270),dtype=np.uint8)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    B=nullspace2(N.T);assert len(B)==16
    bm=[]
    for b in B:
        m=0
        for i,z in enumerate(b):
            if int(z):m|=1<<i
        bm.append(m)
    words=[0]
    for b in bm:words += [x^b for x in words]
    minimum=sorted(w for w in words if w.bit_count()==30);shell45=sorted(w for w in words if w.bit_count()==45)
    assert (len(minimum),len(shell45))==(36,432)

    # Reconstruct Pass4658 Jacobi graph from code shells only.
    classes=defaultdict(list)
    for a,b in itertools.combinations(range(36),2):
        sig=Counter(tuple(sorted(((minimum[a]&u).bit_count(),(minimum[b]&u).bit_count()))) for u in shell45)
        classes[tuple(sorted(sig.items()))].append((a,b))
    assert sorted(map(len,classes.values()))==[270,360]
    E=next(v for v in classes.values() if len(v)==270);G36=nx.Graph();G36.add_nodes_from(range(36));G36.add_edges_from(E)
    assert set(dict(G36.degree()).values())=={15}

    K4=[frozenset(C) for C in nx.find_cliques(G36) if len(C)==4];assert len(K4)==135
    def anticomplete(A,B):return all(not G36.has_edge(a,b) for a in A for b in B)
    H=nx.Graph();H.add_nodes_from(range(135))
    for a,b in itertools.combinations(range(135),2):
        if anticomplete(K4[a],K4[b]):H.add_edge(a,b)
    assert H.number_of_edges()==135 and set(dict(H.degree()).values())=={2}
    comps=[frozenset(c) for c in nx.connected_components(H)]
    assert len(comps)==45 and all(len(c)==3 and nx.is_isomorphic(H.subgraph(c),nx.cycle_graph(3)) for c in comps)
    code45=[]
    for C in comps:
        U=frozenset().union(*(K4[i] for i in C));assert len(U)==12
        sub=G36.subgraph(U); assert nx.number_connected_components(sub)==3 and all(len(c)==4 for c in nx.connected_components(sub))
        outside=set(range(36))-set(U);assert {sum(G36.has_edge(x,y) for x in U) for y in outside}=={6}
        code45.append(U)
    code45=set(code45);assert len(code45)==45

    # Exact PSp action on minimum words and code45.
    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    def act_v(x,g):return rep(pmask(rep(x),g))
    def act_word(w,g):
        z=0
        for i in range(135):
            if (w>>i)&1:z|=1<<sidx[act_v(sing[i],g)]
        return z
    midx={w:i for i,w in enumerate(minimum)}
    def minperm(g):return tuple(midx[act_word(w,g)] for w in minimum)
    gp={g:minperm(g) for g in G}
    def act45(U,g):return frozenset(gp[g][i] for i in U)
    U0=min(code45,key=lambda U:tuple(sorted(U)));orb={act45(U0,g) for g in G};assert orb==code45
    St=[g for g in G if act45(U0,g)==U0];assert len(St)==576

    # Independently constructed protected 45 on the 40 W33 lines.
    fibers=defaultdict(list)
    for ap in apartments:fibers[ap_fiber(ap)].append(tuple(map(int,ap)))
    protected={frozenset().union(*(set(ap) for ap in F)) for F in fibers.values()};assert len(protected)==45 and all(len(U)==16 for U in protected)
    def actP(U,g):return frozenset(g[i] for i in U)
    fixed=[U for U in protected if all(actP(U,g)==U for g in St)];assert len(fixed)==1
    P0=fixed[0];mapping={}
    for g in G:
        a=act45(U0,g);b=actP(P0,g)
        if a in mapping:assert mapping[a]==b
        mapping[a]=b
    assert len(mapping)==45 and set(mapping.values())==protected
    old=json.loads((ROOT/'data/PART_W33_PASS4616_EXPLICIT_45_E6_INTERTWINER.json').read_text());assert old['equivariant_bijection_size']==45

    out={'pass':4662,'code_intrinsic_chain':{'minimum_words':36,'Jacobi_graph':'SRG(36,15,6,6)','maximal_K4':135,'K4_anticompleteness_edges':135,'K4_anticompleteness_components':'45 C3','union_supports':45,'union_size':12,'induced_graph_per_union':'3 K4','external_degree_into_union':6},
      'action_bridge':{'PSp_orbit_size':45,'stabilizer_order':576,'fixed_protected45_supports':1,'equivariant_bijection_to_protected45':True,'Pass4616_target':'center-quad/E6-tritangent45'},
      'theorem':'The E6/protected 45 is reconstructible from C=[135,16,30]_2 alone: the intrinsic 36-minword Jacobi graph has 135 K4s whose anticompleteness graph is 45 disjoint triangles; the 45 three-K4 unions form a transitive PSp carrier with the exact protected/E6 stabilizer.',
      'boundary':'Exact finite code/graph/G-set reconstruction only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
