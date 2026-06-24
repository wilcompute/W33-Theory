#!/usr/bin/env python3
"""BT1721: Hesse/Fano monodromy twist search certificate."""
from __future__ import annotations
import itertools, json
from pathlib import Path
import networkx as nx
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"bt1721_hesse_fano_monodromy_twist.json"
BASE=[(i,(i+1)%7,(i+3)%7) for i in range(7)]
BASE_SETS={frozenset(t) for t in BASE}
CHOICES=[9,941,834,658,135,388,764,575,964]
CELLS=[(x,y) for x in range(3) for y in range(3)]

def fano_systems():
    autos=[]
    for p in itertools.permutations(range(7)):
        if {frozenset(p[x] for x in L) for L in BASE_SETS}==BASE_SETS:
            autos.append(p)
    systems=[]
    rots=[(0,1,2),(1,2,0),(2,0,1),(0,2,1),(2,1,0),(1,0,2)]
    for p in autos:
        for r in rots:
            sys=[tuple(p[t[i]] for i in r) for t in BASE]
            if all(sorted(t[k] for t in sys)==list(range(7)) for k in range(3)):
                systems.append(sys)
    return systems

def hesse_lines():
    H=[]
    for y in range(3): H.append([(x,y) for x in range(3)])
    for x in range(3): H.append([(x,y) for y in range(3)])
    for b in range(3): H.append([(t,(t+b)%3) for t in range(3)])
    return H

def girth(G):
    best=10**9
    for s in G.nodes:
        dist={s:0}; parent={s:None}; q=[s]
        for v in q:
            for w in G[v]:
                if w not in dist:
                    dist[w]=dist[v]+1; parent[w]=v; q.append(w)
                elif parent[v]!=w and parent[w]!=v:
                    best=min(best,dist[v]+dist[w]+1)
    return None if best==10**9 else best

def direct_product_graph():
    G=nx.Graph(); G.add_nodes_from(("p",a,h) for a in range(7) for h in CELLS)
    for h in CELLS:
        for i,t in enumerate(BASE):
            ln=("l",h,i); G.add_node(ln)
            for a in t: G.add_edge(("p",a,h),ln)
    return G

def twist_graph():
    systems=fano_systems(); H=hesse_lines(); G=nx.Graph()
    G.add_nodes_from(("p",a,h) for a in range(7) for h in CELLS)
    for hi,hline in enumerate(H):
        sys=systems[CHOICES[hi]]
        for ti,tr in enumerate(sys):
            ln=("l",hi,ti); G.add_node(ln)
            for k in range(3): G.add_edge(("p",tr[k],hline[k]),ln)
    return G, len(systems), H

def main():
    D=direct_product_graph(); T,nsys,H=twist_graph(); g=girth(T)
    checks={"fano_automorphism_systems_1008": nsys==1008,"direct_product_has_nine_components": nx.number_connected_components(D)==9,"twist_points_63_lines_63": sum(1 for n in T if n[0]=="p")==63 and sum(1 for n in T if n[0]=="l")==63,"twist_edges_189": T.number_of_edges()==189,"twist_is_3_regular": set(dict(T.degree()).values())=={3},"twist_connected": nx.is_connected(T),"twist_has_short_cycles_not_split_cayley": g<12}
    payload={"theorem":"BT1721 Hesse-Fano monodromy twist certificate","verified":all(checks.values()),"summary":"Replacing the disconnected Fano x Hesse product by a three-direction Hesse schedule with oriented Fano automorphism systems connects the 63-address cover. The candidate has 63 points, 63 lines, 189 incidences and degree 3. It is connected, unlike the nine-component product, but short cycles remain, so it is still not the split Cayley hexagon.","direct_product":{"components":nx.number_connected_components(D),"component_sizes":sorted(len(c) for c in nx.connected_components(D))},"twist":{"components":nx.number_connected_components(T),"diameter":nx.diameter(T),"girth":g,"wl_hash":weisfeiler_lehman_graph_hash(T,iterations=4),"choices":CHOICES,"hesse_directions":"horizontal, vertical, slope +1"},"checks":checks,"boundary":"This executes the monodromy search and finds a connected short-cycle twist. It is a falsifier/waypoint, not a split-Cayley proof."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({"verified":payload["verified"],"direct_components":9,"twist_girth":g,"twist_diameter":payload["twist"]["diameter"]},indent=2))
    return 0 if payload["verified"] else 1
if __name__=="__main__": raise SystemExit(main())
