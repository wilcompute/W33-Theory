#!/usr/bin/env python3
"""Passes 4782–4784 — reconstruct the 270 router as triangle geometry of SRG(45,12,3,3).

4782: the 270 involution residues are exactly the 270 triangles of the 45-point
      quotient reconstructed from the 135 dependency cubes.
4783: the 27 hot Petersen fibers are exactly the 27 maximal K5s of that quotient;
      each K5 contributes its ten 3-subsets, with Petersen adjacency given by
      triangle intersection one.
4784: every quotient vertex has neighborhood 3 K4.  Triangle pairs sharing an
      edge form the degree-6 residue orbital; pairs sharing exactly one vertex
      split into cold degree12, hot degree3, and the paired directed orbitals
      8/9 of degree12 each.  The PGSp outer involution swaps precisely 8<->9.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4782_4784_SRG45_TRIANGLE_K5_ROUTER.json'

def main()->int:
    pts,pidx,lines,A,apartments,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(A[:,C],axis=1)&1):residues.append(tuple(C))
    ridx={r:i for i,r in enumerate(residues)};rm=[sum(1<<x for x in r) for r in residues]
    cold_support=[set() for _ in range(270)]
    for i,j in itertools.combinations(range(270),2):
        if (rm[i]&rm[j]).bit_count()==2:cold_support[i].add(j);cold_support[j].add(i)
    tris=[]
    for a in range(270):
        for b in (x for x in cold_support[a] if x>a):
            for c in cold_support[a]&cold_support[b]:
                if c>b:tris.append((a,b,c))
    dep=[t for t in tris if rm[t[0]]^rm[t[1]]^rm[t[2]]==0]
    non=[t for t in tris if rm[t[0]]^rm[t[1]]^rm[t[2]]]
    assert len(dep)==len(non)==540
    ed={tuple(sorted(e)):i for i,t in enumerate(dep) for e in itertools.combinations(t,2)}
    en={tuple(sorted(e)):i for i,t in enumerate(non) for e in itertools.combinations(t,2)}
    adj=[set() for _ in range(1080)]
    for e in ed:
        a=ed[e];b=540+en[e];adj[a].add(b);adj[b].add(a)
    cubes=[];seen=set()
    for s in range(1080):
        if s in seen:continue
        Q=[s];seen.add(s);V=[]
        while Q:
            u=Q.pop();V.append(u)
            for v in adj[u]:
                if v not in seen:seen.add(v);Q.append(v)
        R=set()
        for u in V:R.update(dep[u] if u<540 else non[u-540])
        assert len(V)==8 and len(R)==6;cubes.append(frozenset(R))
    assert len(cubes)==135;cidx={C:i for i,C in enumerate(cubes)}
    um=[0]*135
    for i,C in enumerate(cubes):
        for r in C:um[i]|=rm[r]
        assert um[i].bit_count()==8

    _,G,F=build_groups(pts,pidx,lines);assert (len(G),len(F))==(25920,51840)
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    def ac(i,g):return cidx[frozenset(ar(r,g) for r in cubes[i])]
    Hc=[g for g in G if ac(0,g)==0];assert len(Hc)==192
    fixed=[i for i in range(135) if all(ac(i,g)==i for g in Hc)];assert len(fixed)==3
    block0=frozenset(fixed)
    blocks=sorted({frozenset(ac(i,g) for i in block0) for g in G},key=lambda B:tuple(sorted(B)));assert len(blocks)==45
    bidx={B:i for i,B in enumerate(blocks)};cube_to_block={c:i for i,B in enumerate(blocks) for c in B};assert len(cube_to_block)==135

    # selected135 relation and 45-point quotient.
    S135=nx.Graph();S135.add_nodes_from(range(135))
    for i,j in itertools.combinations(range(135),2):
        if (um[i]&um[j]).bit_count()==4:S135.add_edge(i,j)
    assert S135.number_of_edges()==810 and set(dict(S135.degree()).values())=={12}
    mult=Counter()
    for i,j in S135.edges():
        a,b=cube_to_block[i],cube_to_block[j]
        if a!=b:mult[tuple(sorted((a,b)))]+=1
    assert set(mult.values())=={3} and len(mult)==270
    Q45=nx.Graph();Q45.add_nodes_from(range(45));Q45.add_edges_from(mult)
    assert set(dict(Q45.degree()).values())=={12}
    A45=nx.to_numpy_array(Q45,nodelist=range(45),dtype=int)
    assert np.array_equal(A45@A45,9*np.eye(45,dtype=int)+3*np.ones((45,45),dtype=int))

    # 4782: every residue belongs to three cubes -> three quotient blocks -> a triangle.
    rtri=[]
    for r in range(270):
        C=[i for i,U in enumerate(cubes) if r in U];assert len(C)==3
        T=tuple(sorted({cube_to_block[i] for i in C}));assert len(T)==3
        assert all(Q45.has_edge(a,b) for a,b in itertools.combinations(T,2));rtri.append(T)
    assert len(set(rtri))==270
    qtri={tuple(sorted(t)) for clique in nx.enumerate_all_cliques(Q45) if len(clique)==3 for t in [clique]}
    assert len(qtri)==270 and set(rtri)==qtri

    # Residue orbitals.
    H=[g for g in G if ar(0,g)==0];unseen=set(range(270));orbs=[]
    while unseen:
        x=min(unseen);O=sorted({ar(x,h) for h in H});orbs.append(O);unseen-=set(O)
    assert [len(O) for O in orbs]==[1,12,16,48,16,6,24,96,12,12,24,3]
    oi={x:k for k,O in enumerate(orbs) for x in O};trans={}
    for g in G:
        x=ar(0,g)
        if x not in trans:trans[x]=g
    def inv(p):
        q=[0]*len(p)
        for i,j in enumerate(p):q[j]=i
        return tuple(q)
    def rel(a,b):return oi[ar(b,inv(trans[a]))]

    # 4783: maximal cliques are 27 K5s, each containing ten residue triangles.
    maxc=list(nx.find_cliques(Q45));assert Counter(map(len,maxc))==Counter({5:27})
    K5=[frozenset(C) for C in maxc];tri_to_K=defaultdict(list)
    rtri_idx={T:i for i,T in enumerate(rtri)}
    for k,C in enumerate(K5):
        for T in itertools.combinations(sorted(C),3):tri_to_K[rtri_idx[T]].append(k)
    assert len(tri_to_K)==270 and set(map(len,tri_to_K.values()))=={1}
    hotK=set()
    for C in K5:
        R=[rtri_idx[T] for T in itertools.combinations(sorted(C),3)]
        P=nx.Graph();P.add_nodes_from(R)
        for a,b in itertools.combinations(R,2):
            if len(set(rtri[a])&set(rtri[b]))==1:P.add_edge(a,b);hotK.add(tuple(sorted((a,b))))
        assert nx.is_isomorphic(P,nx.petersen_graph())
    hotOrb={tuple(sorted((a,b))) for a in range(270) for b in range(a+1,270) if rel(a,b)==11}
    assert hotK==hotOrb and len(hotK)==405

    # 4784: local 3K4 and complete translation of the low-degree orbitals.
    assert all(sorted((len(C),Q45.subgraph(C).number_of_edges()) for C in nx.connected_components(Q45.subgraph(list(Q45.neighbors(v)))))==[(4,6),(4,6),(4,6)] for v in Q45)
    by_inter=defaultdict(Counter)
    for i,j in itertools.combinations(range(270),2):by_inter[len(set(rtri[i])&set(rtri[j]))][rel(i,j)]+=1
    assert by_inter[2]==Counter({5:810})
    # unordered counts split the paired directed orbitals 8/9 according to index ordering;
    # as directed relations each has subdegree 12.
    assert set(by_inter[1])=={1,8,9,11}
    assert sum(by_inter[1].values())==5265 and by_inter[1][1]==1620 and by_inter[1][11]==405

    outer=next(iter(set(F)-set(G)));op=[]
    for k,O in enumerate(orbs):op.append(rel(ar(0,outer),ar(O[0],outer)))
    assert op==[0,1,2,3,4,5,6,7,9,8,10,11]

    out={'passes':[4782,4783,4784],
      '4782_triangle_model':{'quotient':'SRG(45,12,3,3)','quotient_edges':270,'selected135_edges_above_each_quotient_edge':3,
        'quotient_triangles':270,'residues':270,'residue_to_triangle_bijection':True},
      '4783_K5_Petersen':{'maximal_K5':27,'triangles_per_K5':10,'each_triangle_in_unique_K5':True,
        'Petersen_fibers':27,'hot_edges':405,'hot_relation':'two K5 triangles intersect in exactly one quotient vertex'},
      '4784_local_chirality':{'neighborhood_of_each_45_vertex':'3 K4','triangle_pair_shared_edge_orbital':5,'shared_edge_subdegree':6,
        'shared_one_vertex_orbitals':[1,8,9,11],'cold_orbital':1,'hot_orbital':11,'paired_chiral_orbitals':[8,9],
        'outer_orbital_permutation':op,'outer_swaps_only_chiral_pair_in_this_low_degree_layer':True},
      'theorem':'The entire 270-residue router admits a 45-point triangle model: residues are all triangles of SRG(45,12,3,3), hot Petersen fibers are the ten triangles inside its 27 maximal K5s, and the PGSp outer involution reverses the unique paired PSp chirality 8<->9 among one-vertex triangle intersections.',
      'boundary':'Exact finite graph/group identification. The word chirality denotes the paired directed PSp orbitals exchanged by the outer automorphism.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
