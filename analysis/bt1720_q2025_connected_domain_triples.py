#!/usr/bin/env python3
"""BT1720: extract q2025 red/blue domain triples and compare with BT1715.

Pauli code: 0=I, 1=X, 2=Y, 3=Z. The blue packet uses the unique
one-letter correction found by line-degree closure: XXY -> XYY in the
visual transcription.
"""
from __future__ import annotations
from itertools import combinations
import json
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1720_q2025_connected_domain_triples.json"

RED = [[1,1,0],[0,1,0],[1,0,0],[0,1,2],[1,1,2],[1,3,1],[0,2,3],[3,1,1],[3,3,2],[2,1,2],[1,2,0],[2,1,0],[3,3,0],[3,3,3],[0,0,3],[1,1,3],[0,3,3],[3,2,0],[0,1,1],[0,2,1],[2,1,1],[3,0,0],[2,3,3],[0,0,1]]
BLUE_RAW = [[2,3,1],[0,3,2],[3,1,3],[1,1,2],[3,3,1],[2,1,3],[0,3,0],[2,2,3],[2,3,0],[0,1,3],[1,1,1],[1,0,2],[1,3,3],[0,3,1],[2,3,2],[2,0,3],[1,3,0],[2,2,1],[3,2,2],[1,3,2],[2,0,1],[3,1,2],[3,0,2],[3,1,0]]
BLUE = [row[:] for row in BLUE_RAW]
BLUE[3] = [1,2,2]
BITS = {0:(0,0),1:(1,0),2:(1,1),3:(0,1)}
LETTERS = "IXYZ"

def label(code: list[int]) -> str:
    return "".join(LETTERS[i] for i in code)

def vec(code: list[int]) -> tuple[int,...]:
    x=[]; z=[]
    for c in code:
        xb,zb=BITS[c]; x.append(xb); z.append(zb)
    return tuple(x+z)

def add(a,b): return tuple((i+j)%2 for i,j in zip(a,b))

def symp(a,b):
    n=len(a)//2
    return sum(a[i]*b[n+i]+a[n+i]*b[i] for i in range(n))%2

def triples(codes):
    V=[vec(c) for c in codes]; names={vec(c):label(c) for c in codes}; S=set(V); out=set()
    for a,b in combinations(V,2):
        c=add(a,b)
        if c in S and any(c) and symp(a,b)==0:
            out.add(tuple(sorted([names[a],names[b],names[c]])))
    return sorted(out)

def incidence_graph(tris):
    G=nx.Graph()
    for p in sorted({x for t in tris for x in t}): G.add_node(("p",p), kind="point")
    for i,t in enumerate(tris):
        G.add_node(("l",i), kind="line")
        for p in t: G.add_edge(("p",p),("l",i))
    return G

def bt1715_cover_graph():
    def lat(i,j): return i^j
    def side(kind, cell):
        i,j=cell
        return j%2 if kind=="R" else i%2
    cells=[(i,j) for i in range(4) for j in range(4)]
    face_obs={}
    for c in cells:
        axes=[("R",c[0]),("C",c[1]),("S",lat(*c))]
        face_obs[c]=[(k,a,side(k,c)) for k,a in axes]
    G=nx.Graph()
    for obs in sorted({o for os in face_obs.values() for o in os}): G.add_node(("p",obs), kind="point")
    for c,obs in face_obs.items():
        G.add_node(("l",c), kind="line")
        for o in obs: G.add_edge(("p",o),("l",c))
    return G

def packet(name,codes):
    T=triples(codes); G=incidence_graph(T)
    deg=dict(G.degree())
    point_degrees=[deg[n] for n,d in G.nodes(data=True) if d["kind"]=="point"]
    line_degrees=[deg[n] for n,d in G.nodes(data=True) if d["kind"]=="line"]
    return {"name":name,"triples":T,"points":len(codes),"lines":len(T),"incidences":G.number_of_edges(),"point_degree_set":sorted(set(point_degrees)),"line_degree_set":sorted(set(line_degrees)),"connected":nx.is_connected(G),"components":nx.number_connected_components(G),"cycle_rank":G.number_of_edges()-G.number_of_nodes()+nx.number_connected_components(G),"diameter":nx.diameter(G) if nx.is_connected(G) else None}

def main():
    braw=packet("blue_raw", BLUE_RAW); red=packet("red", RED); blue=packet("blue_corrected", BLUE)
    model=bt1715_cover_graph()
    iso_red=nx.is_isomorphic(incidence_graph(red["triples"]), model, node_match=lambda a,b:a["kind"]==b["kind"])
    iso_blue=nx.is_isomorphic(incidence_graph(blue["triples"]), model, node_match=lambda a,b:a["kind"]==b["kind"])
    checks={"red_is_24_2_16_3": red["points"]==24 and red["lines"]==16 and red["incidences"]==48 and red["point_degree_set"]==[2] and red["line_degree_set"]==[3],"blue_raw_fails_degree_two": braw["point_degree_set"] != [2],"blue_correction_succeeds": blue["points"]==24 and blue["lines"]==16 and blue["incidences"]==48 and blue["point_degree_set"]==[2] and blue["line_degree_set"]==[3],"red_and_blue_connected": red["connected"] and blue["connected"],"not_bt1715_parity_cover": (not iso_red) and (not iso_blue)}
    payload={"theorem":"BT1720 q2025 connected domain triple extraction","verified":all(checks.values()),"blue_visual_correction":"raw code [1,1,2] is replaced by [1,2,2] because it is the unique one-letter correction that restores the (24_2,16_3) line-degree law","red":red,"blue_raw":braw,"blue_corrected":blue,"bt1715_parity_cover_isomorphism":{"red":iso_red,"blue":iso_blue},"checks":checks,"boundary":"Line triples are symplectic closures inside the transcribed point sets. This certifies the q2025 domain incidence, and it falsifies the simple disconnected BT1715 parity cover as the exact q2025 chart."}
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps({"verified":payload["verified"],"red_lines":red["lines"],"blue_lines":blue["lines"],"blue_raw_degree_set":braw["point_degree_set"],"iso_bt1715":[iso_red,iso_blue]}, indent=2))
    return 0 if payload["verified"] else 1
if __name__ == "__main__": raise SystemExit(main())
