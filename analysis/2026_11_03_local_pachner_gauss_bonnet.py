#!/usr/bin/env python3
"""Actual local 2D Pachner (1,3),(3,1),(2,2) moves on a triangulated S².
Certified links, Euler, valence curvature and exact Gauss--Bonnet at every move.
No starting dimension-agnostic or 3+1D phase claim.
"""
from __future__ import annotations
import itertools,random,math,json
from collections import Counter,defaultdict
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_pachner_sphere_dimension_obstruction.json'
def f(*x):return frozenset(x)
def start():
    # Octahedron: all choices of one vertex from 3 antipodal pairs.
    return {f(*t) for t in itertools.product((0,1),(2,3),(4,5))}
def topology(T):
    V=set.union(*(set(t) for t in T))
    E=Counter(f(a,b) for t in T for a,b in itertools.combinations(sorted(t),2))
    G=nx.Graph();G.add_nodes_from(V);G.add_edges_from([tuple(e) for e in E])
    assert all(c==2 for c in E.values())
    assert nx.is_connected(G)
    for v in V:
        L=nx.Graph()
        for t in T:
            if v in t:L.add_edge(*tuple(t-{v}))
        assert nx.is_connected(L)
        assert all(k==2 for _,k in L.degree())
        assert len(L.nodes)==len(L.edges)==G.degree(v)
    assert nx.check_planarity(G)[0]
    assert len(V)-len(E)+len(T)==2
    assert sum(6-k for _,k in G.degree())==12
    return {"vertices":len(V),"edges":len(E),"faces":len(T),
       "euler_characteristic":2,
       "gauss_bonnet_angle_sum_radians":4*math.pi,
       "deficit_units_pi_over3":12,
       "max_degree":max(dict(G.degree()).values()),
       "min_degree":min(dict(G.degree()).values()),
       "graph_diameter":nx.diameter(G)},G,E
def one3(T,rng):
    face=rng.choice(tuple(T));w=1+max(max(t) for t in T)
    a,b,c=sorted(face)
    return (T-{face})|{f(a,b,w),f(a,c,w),f(b,c,w)}
def three1(T,rng):
    _,G,_=topology(T)
    candidate=[]
    for v in G:
        if G.degree(v)!=3:continue
        neigh=set(G.neighbors(v));triangle=f(*neigh)
        if triangle in T:continue
        local={t for t in T if v in t}
        if len(local)!=3:continue
        candidate.append((v,local,triangle))
    if not candidate:return None
    v,local,new=rng.choice(candidate)
    return (T-local)|{new}
def two2(T,rng):
    _,G,E=topology(T)
    candidate=[]
    for edge in E:
        u,v=sorted(edge)
        ts=[t for t in T if u in t and v in t]
        a=next(iter(ts[0]-edge));b=next(iter(ts[1]-edge))
        if a==b or G.has_edge(a,b):continue
        candidate.append((u,v,a,b,ts))
    if not candidate:return None
    u,v,a,b,ts=rng.choice(candidate)
    return (T-set(ts))|{f(u,a,b),f(v,a,b)}
def run():
    rng=random.Random(20261103)
    T=start();types=Counter();history=[]
    initial,_,_=topology(T)
    for i in range(360):
        action=rng.choices(["2-2","1-3","3-1"],weights=[7,2,3])[0]
        if action=="2-2":U=two2(T,rng)
        elif action=="1-3":U=one3(T,rng) if len(T)<180 else None
        else:U=three1(T,rng)
        if U is None:continue
        assert len(U.symmetric_difference(T)) in (4,6)
        T=U;types[action]+=1
        topo,_,_=topology(T)
        assert topo["euler_characteristic"]==2
        assert topo["deficit_units_pi_over3"]==12
        history.append({"step":i,"move":action,**topo})
    assert types["2-2"]>=20,types
    assert types["1-3"]>=10,types
    assert types["3-1"]>=5,types
    assert history[-1]["vertices"]!=initial["vertices"]
    out={"status":"PASS_LOCAL_PACHNER_SPHERE_AND_GAUSS_BONNET",
       "initial":initial,"final":history[-1],
       "move_census":dict(types),"accepted_moves":len(history),
       "history":history,
       "topological_dimension":2,
       "exact_discrete_curvature":"With equilateral Euclidean triangles, each vertex deficit δ_v=(6-deg(v))*π/3. Σ_v δ_v =4π at every move (Gauss--Bonnet on S²). This is intrinsic discrete 2D curvature, not an emergent 4D Einstein action.",
       "locality":"1-3 face stellar subdivision, 3-1 inverse on an interior degree-three vertex if inverse face absent, and 2-2 diagonal flip if opposite diagonal absent. Every changed simplex lies inside the affected local disk.",
       "no_go":"Pachner moves preserve PL topology and manifold dimension by construction; random iterates of 2D moves cannot dynamically select a four-dimensional manifold without allowing topology/dimension-changing operations or starting in 4D. This is an explicit local-move negative control.",
       "sources":["https://doi.org/10.1007/s00454-026-00818-w","https://link.springer.com/article/10.1007/s11005-024-01874-0"]}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("PACHNER",dict(types),"START",initial,"FINAL",history[-1]["vertices"],history[-1]["faces"])
if __name__=="__main__":run()
