#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; P=3

def canon(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x: return tuple(((1 if x==1 else 2)*y)%P for y in v)
    raise ValueError

def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P

def w33():
    pts=[]; seen=set()
    for raw in product(range(P), repeat=4):
        if raw==(0,0,0,0): continue
        c=canon(raw)
        if c not in seen: seen.add(c); pts.append(c)
    pi={p:i for i,p in enumerate(pts)}
    e=[(i,j) for i,j in combinations(range(40),2) if form(pts[i],pts[j])==0]
    adj=np.zeros((40,40),dtype=np.int8)
    for i,j in e: adj[i,j]=adj[j,i]=1
    lines=set()
    for i,j in e:
        u,v=pts[i],pts[j]; L=set()
        for a,b in product(range(P),repeat=2):
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
            if cyc not in sq: sq.add(cyc); quads.append((cyc,tuple(sorted((a,b,c,d)))))
    C=np.zeros((120,len(quads)),dtype=np.int8)
    for qi,(cyc,verts) in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc: inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lp=tuple(sorted(el[tuple(sorted(x))] for x in es))
            C[ai[va[(p,lp)]],qi]=1
    G=C@C.T; A=(G>0).astype(np.int8); np.fill_diagonal(A,0)
    return lines, axes, quads, A

def rootgraph():
    r=[]
    for i in range(8):
        for j in range(i+1,8):
            for si in (1,-1):
                for sj in (1,-1):
                    x=[0]*8; x[i]=si; x[j]=sj; r.append(tuple(x))
    for s in product((1,-1),repeat=8):
        if sum(x<0 for x in s)%2==0: r.append(tuple(x/2 for x in s))
    V=np.array(r,float); used=set(); reps=[]
    for i in range(240):
        if i in used: continue
        for j in range(i+1,240):
            if j not in used and np.allclose(V[i]+V[j],0):
                used.add(i); used.add(j); reps.append(np.array(min(tuple(V[i]),tuple(V[j])),float)); break
    reps=sorted(reps,key=lambda x:tuple(x.tolist())); R=np.array(reps,float)
    D=np.abs(R@R.T); A=np.isclose(D,0).astype(np.int8); np.fill_diagonal(A,0)
    return A,D

def sig(S,A,D):
    idx=sorted(S); sub=A[np.ix_(idx,idx)]
    deg=tuple(sorted(Counter(map(int,sub.sum(1))).items()))
    eig=tuple(sorted(Counter(int(round(x)) for x in np.linalg.eigvalsh(sub.astype(float))).items()))
    comp=1-sub-np.eye(len(idx),dtype=int)
    comps=tuple(sorted(len(c) for c in nx.connected_components(nx.from_numpy_array(comp))))
    dots=tuple(sorted(Counter(float(D[i,j]) for i,j in combinations(idx,2)).items()))
    return str(dict(deg=deg,eig=eig,comp=comps,dots=dots))

def main():
    lines,axes,quads,A1=w33(); A2,D=rootgraph()
    gm=nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(A1),nx.from_numpy_array(A2)); assert gm.is_isomorphic(); mp=dict(gm.mapping)
    tri={p:set(mp[i] for i,a in enumerate(axes) if a[0]==p) for p in range(40)}
    line_sets=[set().union(*(tri[p] for p in L)) for L in lines]
    quad_sets=[set().union(*(tri[p] for p in verts)) for cyc,verts in quads]
    ls=Counter(sig(S,A2,D) for S in line_sets); qs=Counter(sig(S,A2,D) for S in quad_sets)
    # count overlaps between the two species
    inter=Counter(len(L&Q) for L in line_sets for Q in quad_sets)
    ok=len(ls)==1 and list(ls.values())==[40] and len(qs)==1 and list(qs.values())==[1620]
    out={'all_checks_passed':ok,'summary':{'line_species_count':40,'quadrangle_species_count':1620,'line_species_signature':next(iter(ls)),'quadrangle_species_signature':next(iter(qs)),'line_quadrangle_intersections':dict(inter)},'boundary':'Line and quadrangle 12-root-line unions are classified by internal orthogonality signature under one explicit axis/root-line isomorphism.'}
    path=ROOT/'data'/'w33_rootline_line_vs_quadrangle_species.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
