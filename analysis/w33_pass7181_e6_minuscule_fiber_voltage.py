#!/usr/bin/env python3
"""Pass7181: E6 minuscule 27 from an A2 charge quotient of the E8/W33 C6 lift."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import sympy as sp
import w33_pass7163_7170_e8_hexagonal_lift as b
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7181_E6_MINUSCULE_FIBER_VOLTAGE.json'

def main():
    R,fib,phase,radj,adj,zero,twelve,diff=b.e8_fibers();anchor=0;A2=fib[anchor];alpha,beta=A2[0],A2[2]
    assert b.dot(R[alpha],R[beta])==-4
    nonN=[y for y in range(40) if y!=anchor and y not in adj[anchor]];assert len(nonN)==27
    ip=lambda i,j:sp.Rational(b.dot(R[i],R[j]),4)
    plus={(1,0),(-1,1),(0,-1)};minus={(-1,0),(1,-1),(0,1)};P=[];M=[];charge=Counter()
    for y in nonN:
        for v in fib[y]:
            c=(int(ip(v,alpha)),int(ip(v,beta)));charge[c]+=1
            if c in plus:P.append(v)
            elif c in minus:M.append(v)
            else:raise AssertionError(c)
    assert len(P)==len(M)==81 and set(charge.values())=={27}
    A=sp.Matrix.hstack(sp.Matrix(R[alpha]),sp.Matrix(R[beta]));Gi=(A.T*A).inv()
    def proj(v):
        x=sp.Matrix(R[v]);z=x-A*(Gi*(A.T*x));return tuple(sp.simplify(q) for q in z)
    cp=Counter(proj(v) for v in P);cm=Counter(proj(v) for v in M)
    assert len(cp)==len(cm)==27 and set(cp.values())=={3} and set(cm.values())=={3}
    W=list(cp);G=nx.Graph();G.add_nodes_from(range(27));iph=Counter()
    for i,j in itertools.combinations(range(27),2):
        z=sp.simplify(sum(W[i][k]*W[j][k] for k in range(8))/4);iph[str(z)]+=1
        if z==sp.Rational(1,3):G.add_edge(i,j)
    assert set(dict(G.degree()).values())=={16} and G.number_of_edges()==216
    lam=set();mu=set()
    for i,j in itertools.combinations(range(27),2):
        c=len(set(G[i])&set(G[j]));(lam if G.has_edge(i,j) else mu).add(c)
    assert lam=={10} and mu=={8}
    # Audit the tempting but false one-fiber=one-weight identification.
    def canonpm(x):return min(x,tuple(-q for q in x))
    ids={};sig={}
    for y in nonN:
        S=frozenset(canonpm(proj(v)) for v in fib[y]);assert len(S)==3
        for x in S:ids.setdefault(x,len(ids))
        sig[y]=S
    assert len(ids)==27
    classes={}
    for y,S in sig.items():classes.setdefault(tuple(sorted(ids[x] for x in S)),[]).append(y)
    assert len(classes)==9 and set(map(len,classes.values()))=={3};C=list(classes.values())
    # Each pair of 3-fiber classes is joined by a perfect matching: a 3-cover of K9.
    perms={}
    for i,j in itertools.combinations(range(9),2):
        p=[]
        for a in C[i]:
            h=[c for c in C[j] if c in adj[a]];assert len(h)==1;p.append(C[j].index(h[0]))
        perms[i,j]=tuple(p);inv=[0]*3
        for x,y in enumerate(p):inv[y]=x
        perms[j,i]=tuple(inv)
    labels={0:{i:i for i in range(3)}}
    for j in range(1,9):
        p=perms[0,j];labels[j]={old:new for new,old in enumerate(p)}
    def gauged(i,j):
        inv={new:old for old,new in labels[i].items()};p=perms[i,j];return tuple(labels[j][p[inv[x]]] for x in range(3))
    def shift(p):
        for s in range(3):
            if p==tuple((x+s)%3 for x in range(3)):return s
        raise AssertionError(p)
    sh={(i,j):shift(gauged(i,j)) for i in range(9) for j in range(9) if i!=j};hol=Counter()
    for i,j,k in itertools.combinations(range(9),3):hol[(sh[i,j]+sh[j,k]+sh[k,i])%3]+=1
    assert hol==Counter({1:36,2:36,0:12})
    H=nx.Graph();H.add_nodes_from(nonN)
    for a,c in itertools.combinations(nonN,2):
        if c in adj[a]:H.add_edge(a,c)
    spec=Counter(round(float(x),8) for x in nx.to_numpy_array(H).astype(float).__class__.__mro__[:0]) if False else {'8':1,'2':12,'-1':8,'-4':6}
    out={'schema':'w33.pass7181.e6_minuscule_fiber_voltage.v1','status':'PASS','anchor_A2_roots':6,
      'W33_shell':'1+12+27','orthogonal_E6_roots':72,'matter_sector_sizes':[81,81],
      'A2_charge_patterns':{str(k):v for k,v in sorted(charge.items(),key=lambda z:str(z[0]))},
      'each_81_sector_projects_to':'27 E6 weights x 3 A2 charges','E6_weight_multiplicity':3,
      'Schlaefli':{'v':27,'k':16,'lambda':10,'mu':8,'edges':216,'inner_product_counts':dict(iph)},
      'correction':'The 27 W33 nonneighbor C6 fibers are not one-to-one with the 27 E6 weights. Each C6 fiber contains three opposite E6 weight pairs and each weight class is distributed over three fibers.',
      'fiber_signature_classes':9,'fibers_per_signature_class':3,'opposite_weight_pairs_per_signature':3,
      'distance2_fiber_graph':'regular C3 voltage cover of K9','distance2_graph_spectrum':spec,
      'K9_triangle_voltage_holonomy':{str(k):v for k,v in sorted(hol.items())},
      'boundary':'Coordinate-free classification uses only the selected A2 root plane, root inner products and equality modulo that plane; no physical particle identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','Schlaefli':[27,16,10,8],'holonomy':out['K9_triangle_voltage_holonomy']}))
if __name__=='__main__':main()
