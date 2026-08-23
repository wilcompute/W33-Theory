#!/usr/bin/env python3
"""Pass8481-8488: objectwise Leech 36-sheet component <-> local W33 line geometry.

Strengthens Pass8101/8201 from a common abstract H27:GL2(3) controller to a
literal incidence/fibre isomorphism.  One 36-vertex mixed-Leech-Lagrangian
component (intersection size 9) is identified with the 36 W33 lines avoiding a
fixed W33 point; the canonical 12 three-sheet Leech fibres go to the twelve
triples of such lines through the twelve neighbours of that point.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np, networkx as nx
from analysis.w33_pass8101_8108_leech_h27_gl23_lagrangian_controller import lagrangians,proj
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8481_8488_LEECH36_W33_LOCAL36_OBJECTWISE.json'

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%3 for y in v)
    raise ValueError
P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={v:i for i,v in enumerate(P)}
J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]],int)%3

def adj(i,j):return i!=j and int(np.array(P[i])@J@np.array(P[j]))%3==0

def main():
    # Leech component.
    L=lagrangians();A=np.zeros((144,144),np.uint8)
    for i,j in itertools.combinations(range(144),2):
        if len(L[i]&L[j])==9:A[i,j]=A[j,i]=1
    G=nx.from_numpy_array(A);CC=[sorted(c) for c in nx.connected_components(G)]
    assert list(map(len,CC))==[36,36,36,36];C=CC[0];AL=A[np.ix_(C,C)]
    fibres=defaultdict(list)
    for loc,g in enumerate(C):fibres[proj(L[g])].append(loc)
    FL=[frozenset(x) for x in fibres.values()];assert len(FL)==12 and set(map(len,FL))=={3}

    # W33 lines in PG(3,3).
    lines=set()
    for i,j in itertools.combinations(range(40),2):
        if not adj(i,j):continue
        u=np.array(P[i]);v=np.array(P[j]);S=set()
        for a,b in itertools.product(range(3),repeat=2):
            if a or b:S.add(pi[canon(tuple(map(int,(a*u+b*v)%3)))])
        if len(S)==4:lines.add(frozenset(S))
    lines=sorted(lines,key=lambda x:tuple(sorted(x)));assert len(lines)==40
    p=0;WL=[x for x in lines if p not in x];assert len(WL)==36
    AW=np.zeros((36,36),np.uint8)
    for i,j in itertools.combinations(range(36),2):
        if WL[i]&WL[j]:AW[i,j]=AW[j,i]=1
    nbr=[q for q in range(40) if adj(p,q)]
    FW=[frozenset(i for i,L0 in enumerate(WL) if q in L0) for q in nbr]
    assert len(FW)==12 and set(map(len,FW))=={3}

    # Colored augmented graphs force fibre preservation.
    def aug(A0,F):
        X=nx.Graph()
        for i in range(36):X.add_node(('v',i),kind='v')
        for i,j in np.argwhere(np.triu(A0,1)):X.add_edge(('v',int(i)),('v',int(j)))
        for k,S in enumerate(F):
            X.add_node(('f',k),kind='f')
            for i in S:X.add_edge(('f',k),('v',i))
        return X
    GL,GW=aug(AL,FL),aug(AW,FW)
    gm=nx.algorithms.isomorphism.GraphMatcher(GL,GW,node_match=lambda a,b:a['kind']==b['kind'])
    iso=next(gm.isomorphisms_iter());vm={i:iso[('v',i)][1] for i in range(36)}
    assert all(bool(AL[i,j])==bool(AW[vm[i],vm[j]]) for i in range(36) for j in range(36))
    spec=Counter(round(float(x),8) for x in np.linalg.eigvalsh(AL.astype(float)))
    assert spec==Counter({2.0:20,-4.0:12,-1.0:3,11.0:1})
    out={'schema':'w33.pass8481_8488.leech36_w33_local36_objectwise.v1','status':'PASS','passes':'8481-8488',
      'Leech_component':{'vertices':36,'adjacency':'mixed Lagrangians intersect in 9 elements','fibres':'12 x 3'},
      'W33_target':{'vertices':'36 lines not through fixed point p','adjacency':'lines intersect','fibres':'for each of 12 neighbours q~p, the 3 lines through q avoiding p'},
      'spectrum':'11^1 + 2^20 + (-1)^3 + (-4)^12','explicit_colored_graph_isomorphism':True,
      'theorem':'One mixed-Leech 36-component is objectwise the local W33 line geometry away from a point, including its canonical 12x3 sheet system. This upgrades the common H27:GL2(3) controller to a literal incidence/fibre weld.',
      'claim_boundary':'Exact finite combinatorial/controller identification; no physical identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','vertices':36,'fibres':12}))
if __name__=='__main__':main()
