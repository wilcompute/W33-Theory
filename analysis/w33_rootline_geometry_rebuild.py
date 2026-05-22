#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
P=3

def canon(v):
    v=tuple(int(x)%P for x in v)
    if v==(0,0,0,0): raise ValueError
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%P for y in v)

def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P

def params(A):
    deg=Counter(map(int,A.sum(1))); la=Counter(); mu=Counter()
    for i,j in combinations(range(A.shape[0]),2):
        c=int(A[i]@A[j]); (la if A[i,j] else mu)[c]+=1
    eig=Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
    return dict(deg=dict(deg), lam=dict(la), mu=dict(mu), eig=dict(eig))

def w33():
    pts=[]; seen=set()
    for raw in product(range(P), repeat=4):
        if raw==(0,0,0,0): continue
        c=canon(raw)
        if c not in seen: seen.add(c); pts.append(c)
    pi={p:i for i,p in enumerate(pts)}
    e=[(i,j) for i,j in combinations(range(40),2) if form(pts[i],pts[j])==0]
    adj=np.zeros((40,40), dtype=np.int8)
    for i,j in e: adj[i,j]=adj[j,i]=1
    lines=set()
    for i,j in e:
        u,v=pts[i],pts[j]; L=set()
        for a,b in product(range(P), repeat=2):
            if a==0 and b==0: continue
            L.add(pi[canon((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(L)))
    lines=sorted(lines); pl=defaultdict(list); el={}
    for li,L in enumerate(lines):
        for p in L: pl[p].append(li)
        for x in combinations(L,2): el[tuple(sorted(x))]=li
    axes=[]; va={}
    for p in range(40):
        a,b,c,d=sorted(pl[p])
        for ax in [((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]:
            ax=tuple(sorted(tuple(sorted(z)) for z in ax)); key=(p,ax); axes.append(key)
            for pair in ax: va[(p,pair)]=key
    axes=sorted(axes); ai={a:i for i,a in enumerate(axes)}
    quads=[]; sq=set()
    for a,b in combinations(range(40),2):
        if adj[a,b]: continue
        common=[x for x in range(40) if adj[a,x] and adj[b,x]]
        for c,d in combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(x)) for x in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in sq: sq.add(cyc); quads.append(cyc)
    C=np.zeros((120,len(quads)), dtype=np.int8)
    for qi,cyc in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc: inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lp=tuple(sorted(el[tuple(sorted(x))] for x in es))
            C[ai[va[(p,lp)]],qi]=1
    G=C@C.T; A=(G>0).astype(np.int8); np.fill_diagonal(A,0)
    return adj, lines, axes, A

def rootgraph():
    r=[]
    for i in range(8):
        for j in range(i+1,8):
            for si in (1,-1):
                for sj in (1,-1):
                    x=[0]*8; x[i]=si; x[j]=sj; r.append(tuple(x))
    for s in product((1,-1), repeat=8):
        if sum(x<0 for x in s)%2==0: r.append(tuple(x/2 for x in s))
    V=np.array(r,float); used=set(); reps=[]
    for i in range(240):
        if i in used: continue
        for j in range(i+1,240):
            if j not in used and np.allclose(V[i]+V[j],0):
                used.add(i); used.add(j); reps.append(np.array(min(tuple(V[i]),tuple(V[j])),float)); break
    reps=sorted(reps, key=lambda x: tuple(x.tolist()))
    R=np.array(reps,float); D=np.abs(R@R.T); A=np.isclose(D,0).astype(np.int8); np.fill_diagonal(A,0)
    return A

def main():
    padj, lines, axes, A1=w33(); A2=rootgraph()
    m=nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(A1), nx.from_numpy_array(A2))
    assert m.is_isomorphic(); mp=dict(m.mapping)
    tri={p:set(mp[i] for i,a in enumerate(axes) if a[0]==p) for p in range(40)}
    d4={li:set().union(*(tri[p] for p in L)) for li,L in enumerate(lines)}
    inc=np.zeros((40,40), dtype=np.int8)
    for p,T in tri.items():
        for li,S in d4.items():
            if T<=S: inc[p,li]=1
    d4adj=np.zeros((40,40), dtype=np.int8); inter=Counter()
    for i,j in combinations(range(40),2):
        s=len(d4[i]&d4[j]); inter[s]+=1
        if s==3: d4adj[i,j]=d4adj[j,i]=1
    lineadj=np.zeros((40,40), dtype=np.int8)
    for i,j in combinations(range(40),2):
        if set(lines[i])&set(lines[j]): lineadj[i,j]=lineadj[j,i]=1
    ok=(Counter(len(x) for x in tri.values())==Counter({3:40}) and
        Counter(x for T in tri.values() for x in T)==Counter({i:1 for i in range(120)}) and
        Counter(len(x) for x in d4.values())==Counter({12:40}) and int(inc.sum())==160 and
        Counter(map(int,inc.sum(1)))==Counter({4:40}) and Counter(map(int,inc.sum(0)))==Counter({4:40}) and
        inter==Counter({0:540,3:240}) and int(np.sum(np.abs(lineadj-d4adj)))==0 and
        params(d4adj)=={'deg':{12:40},'lam':{2:240},'mu':{4:540},'eig':{-4:15,2:24,12:1}})
    out={'all_checks_passed':ok,'summary':{'triads':40,'twelve_sets':40,'incidences':int(inc.sum()),'intersection_distribution':dict(inter),'rebuilt_graph':'SRG(40,12,2,4)'},'d4_graph':params(d4adj),'line_graph_mismatch':int(np.sum(np.abs(lineadj-d4adj)))}
    path=ROOT/'data'/'w33_rootline_geometry_rebuild.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
