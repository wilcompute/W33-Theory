#!/usr/bin/env python3
"""Decide the apparent Pass4795 C3-vs-S3 discrepancy objectwise.

Reconstruct the older dependency-cube quotient exactly from the Pass4795
recipe, but drive it by the *same four PSp transvection generators* used by the
2026-09-01 polar-pair packet carrier.  Then build an explicit equivariant
bijection between the two 45-sets and compare the induced action on the 27
maximal K5 lines.

This is stronger than count/TOM matching: it is a literal paired G-set
certificate.  The Table-of-Marks uniqueness witness remains an independent
cross-check.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter,deque
from pathlib import Path

import networkx as nx
import numpy as np

import w33_20260829_216_clifford_torsor_nogo as base
import w33_20260901_e8_chart_port_holonomy as polar

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_DEGREE45_ACTION_CROSSWALK.json'


def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))

def closure_pairs(A,B):
    I=(tuple(range(45)),tuple(range(45)));S={I};D=deque([I])
    while D:
        a,b=D.popleft()
        for ga,gb in zip(A,B):
            z=(compose(ga,a),compose(gb,b))
            if z not in S:S.add(z);D.append(z)
    return sorted(S)

def porder(p):return base.porder(p)


def old_cube_action():
    pts,pidx,lines,N=base.geometry()
    # Pass4795 residues: 270 four-subsets with even incidence against every line.
    A=np.zeros((40,40),dtype=np.uint8)
    for L in lines:
        for x,y in itertools.combinations(L,2):A[x,y]=A[y,x]=1
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(A[:,C],axis=1)&1):residues.append(tuple(C))
    assert len(residues)==270
    ridx={r:i for i,r in enumerate(residues)};rm=[sum(1<<x for x in r) for r in residues]
    cold=[set() for _ in range(270)]
    for i,j in itertools.combinations(range(270),2):
        if (rm[i]&rm[j]).bit_count()==2:cold[i].add(j);cold[j].add(i)
    tris=[]
    for a in range(270):
        for b in (x for x in cold[a] if x>a):
            for c in cold[a]&cold[b]:
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
    um=[]
    for C in cubes:
        u=0
        for r in C:u|=rm[r]
        assert u.bit_count()==8;um.append(u)

    # Same transvection generators as polar.build().
    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*base.form(x,v)%3
                y=base.norm(tuple((x[k]+z*v[k])%3 for k in range(4)))
                p.append(pidx[y])
            gens40.append(tuple(p))
    chosen=(18,62,77,10);g40=[gens40[i] for i in chosen]
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    def ac(i,g):return cidx[frozenset(ar(r,g) for r in cubes[i])]

    # Generate the 25920 group on cubes and reconstruct Pass4795's 45 blocks as
    # the three cubes fixed by a cube stabilizer, then transport.
    gc=[tuple(ac(i,g) for i in range(135)) for g in g40]
    I=tuple(range(135));G={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gc:
            z=compose(g,a)
            if z not in G:G.add(z);D.append(z)
    assert len(G)==25920
    H=[g for g in G if g[0]==0];assert len(H)==192
    fixed=[i for i in range(135) if all(g[i]==i for g in H)];assert len(fixed)==3
    B0=frozenset(fixed)
    blocks=sorted({frozenset(g[i] for i in B0) for g in G},key=lambda B:tuple(sorted(B)))
    assert len(blocks)==45;bidx={B:i for i,B in enumerate(blocks)}
    gb=[]
    for g in gc:gb.append(tuple(bidx[frozenset(g[i] for i in B)] for B in blocks))

    # Graph intrinsic to old quotient, exactly as Pass4795.
    cube_to_block={c:i for i,B in enumerate(blocks) for c in B};mult=Counter()
    for i,j in itertools.combinations(range(135),2):
        if (um[i]&um[j]).bit_count()==4:
            a,b=cube_to_block[i],cube_to_block[j]
            if a!=b:mult[tuple(sorted((a,b)))]+=1
    Q45=nx.Graph();Q45.add_nodes_from(range(45));Q45.add_edges_from(mult)
    K5=sorted((frozenset(C) for C in nx.find_cliques(Q45)),key=lambda C:tuple(sorted(C)))
    assert len(K5)==27 and {len(C) for C in K5}=={5}
    return gb,Q45,K5


def main():
    _supports,pcharts,pincident,genpairs,PG=polar.build();assert len(PG)==25920
    gp=[a for a,b in genpairs]
    oldg,Qold,Kold=old_cube_action()
    paired=closure_pairs(gp,oldg);assert len(paired)==25920

    # A transitive G-set map is determined by the image of point 0.  Find the
    # unique old point fixed by its stabilizer and transport it.
    H=[z for z in paired if z[0][0]==0];assert len(H)==576
    fixed=[y for y in range(45) if all(b[y]==y for a,b in H)];assert len(fixed)==1
    y0=fixed[0];phi=[None]*45
    for a,b in paired:
        x=a[0];y=b[y0]
        if phi[x] is None:phi[x]=y
        else:assert phi[x]==y
    assert len(set(phi))==45
    for ga,gb in zip(gp,oldg):assert all(phi[ga[x]]==gb[phi[x]] for x in range(45))

    # New polar graph: packets adjacent iff their supports are disjoint, hence
    # completion charts are its maximal K5s.
    Qnew=nx.Graph();Qnew.add_nodes_from(range(45))
    for C in pcharts:
        for a,b in itertools.combinations(C,2):Qnew.add_edge(a,b)
    assert set(frozenset(C) for C in nx.find_cliques(Qnew) if len(C)==5)==set(map(frozenset,pcharts))
    assert all(Qnew.has_edge(i,j)==Qold.has_edge(phi[i],phi[j]) for i,j in itertools.combinations(range(45),2))
    kold={K:i for i,K in enumerate(Kold)}
    linephi=[kold[frozenset(phi[x] for x in C)] for C in pcharts]
    assert len(set(linephi))==27

    # Compute old local image directly at y0 on its three intrinsic K5s.
    incident_old=sorted(i for i,K in enumerate(Kold) if y0 in K);assert len(incident_old)==3
    pos={k:i for i,k in enumerate(incident_old)}
    # line action for every paired element
    image=set()
    for a,b in H:
        perm=[]
        for k in incident_old:
            target=frozenset(b[x] for x in Kold[k]);perm.append(pos[kold[target]])
        image.add(tuple(perm))
    assert len(image)==6
    order_profile=Counter(porder(p) for p in image)
    assert order_profile==Counter({1:1,2:3,3:2})

    out={'schema':'w33.20260901.degree45-action-crosswalk.v1','status':'PASS',
      'ambient':'PSp(4,3)','groupOrder':25920,
      'polarToPass4795PointMap':phi,'polarToPass4795K5Map':linephi,
      'equivariantBijection':True,'graphAndAll27K5Preserved':True,
      'pointStabilizerOrder':576,'pass4795IntrinsicLocalImage':'S3',
      'pass4795LocalImageOrderProfile':{str(k):v for k,v in sorted(order_profile.items())},
      'theorem':'The polar-pair packet carrier and the dependency-cube Pass4795 quotient are literally isomorphic PSp(4,3)-sets under an explicit 45-point equivariant bijection preserving the graph and all 27 maximal K5s. On the old carrier itself, the PSp point stabilizer induces the full S3 on the three incident K5s.',
      'consequence':'The frozen Pass4795 claim PSp-local-image=C3/global two-sheet cyclic orientation is retracted. The later S3 port-gauge theorem is the correct local action.',
      'boundary':'This corrects the action theorem only. Other Pass4795 results not depending on the C3 orientation are untouched.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','bijection':len(set(phi)),'oldLocalImage':'S3','profile':dict(order_profile)},sort_keys=True))

if __name__=='__main__':main()
