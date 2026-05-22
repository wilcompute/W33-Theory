#!/usr/bin/env python3
"""A2/D4 decomposition induced by a 120-axis to 120-root-line isomorphism.

Builds the W33 local-axis graph and the 120 root-line orthogonality graph,
finds a graph isomorphism, and analyzes what W33 points and lines become.

Results verified by the script:
  * Each W33 point's 3 local axes map to an A2-type root-line triad: no internal
    orthogonality, all absolute dot products are 1, and orientations can sum to 0.
  * Each W33 line's 12 local axes map to a D4-type root-line subsystem: internal
    orthogonality graph is 9-regular on 12 vertices with spectrum 9^1 + 0^8 + (-3)^3.
    Its complement is four disjoint triangles.
  * W33 collinearity is recovered from the mapped point triads: for two W33
    points p,q, the number of orthogonal root-line pairs between their two A2
    triads is 9 if p~q and 3 if p not~q.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
P = 3


def canon(v):
    v = tuple(int(x) % P for x in v)
    if v == (0, 0, 0, 0):
        raise ValueError("zero")
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in v)
    raise RuntimeError


def form(u, v):
    return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % P


def build_w33_axis_graph():
    pts=[]; seen=set()
    for raw in product(range(P), repeat=4):
        if raw == (0,0,0,0):
            continue
        c=canon(raw)
        if c not in seen:
            seen.add(c); pts.append(c)
    pi={p:i for i,p in enumerate(pts)}
    edges=[(i,j) for i,j in combinations(range(40),2) if form(pts[i], pts[j]) == 0]
    adj=[[False]*40 for _ in range(40)]
    for i,j in edges: adj[i][j]=adj[j][i]=True
    lines=set()
    for i,j in edges:
        u,v=pts[i],pts[j]; L=set()
        for a,b in product(range(P), repeat=2):
            if a==0 and b==0: continue
            L.add(pi[canon((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(L)))
    lines=sorted(lines)
    pl=defaultdict(list); edge_line={}
    for li,L in enumerate(lines):
        for p in L: pl[p].append(li)
        for e in combinations(L,2): edge_line[tuple(sorted(e))]=li
    axes=[]; vtx_axis={}
    for p in range(40):
        a,b,c,d=sorted(pl[p])
        for ax in [((a,b),(c,d)), ((a,c),(b,d)), ((a,d),(b,c))]:
            ax=tuple(sorted(tuple(sorted(x)) for x in ax)); key=(p,ax); axes.append(key)
            for pair in ax: vtx_axis[(p,pair)] = key
    axes=sorted(axes); ai={a:i for i,a in enumerate(axes)}
    quads=[]; seenq=set()
    for a,b in combinations(range(40),2):
        if adj[a][b]: continue
        common=[x for x in range(40) if adj[a][x] and adj[b][x]]
        for c,d in combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(e)) for e in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in seenq:
                seenq.add(cyc); quads.append(cyc)
    C=np.zeros((120,len(quads)), dtype=np.int8)
    for qi,cyc in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc:
            inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lp=tuple(sorted(edge_line[tuple(sorted(e))] for e in es))
            C[ai[vtx_axis[(p,lp)]], qi]=1
    G=C@C.T; A=(G>0).astype(np.int8); np.fill_diagonal(A,0)
    return pts, np.array(adj, dtype=np.int8), lines, axes, A


def root_lines():
    roots=[]
    for i in range(8):
        for j in range(i+1,8):
            for si in (1,-1):
                for sj in (1,-1):
                    r=[0]*8; r[i]=si; r[j]=sj; roots.append(tuple(r))
    for s in product((1,-1), repeat=8):
        if sum(x < 0 for x in s) % 2 == 0:
            roots.append(tuple(x/2 for x in s))
    V=np.array(roots,float); used=set(); reps=[]
    for i in range(240):
        if i in used: continue
        for j in range(i+1,240):
            if j not in used and np.allclose(V[i]+V[j],0):
                used.add(i); used.add(j); reps.append(np.array(min(tuple(V[i]), tuple(V[j])),float)); break
    reps=sorted(reps, key=lambda r: tuple(r.tolist()))
    R=np.array(reps,float); D=np.abs(R@R.T); A=np.isclose(D,0).astype(np.int8); np.fill_diagonal(A,0)
    return R, A, D


def eig_counter(A):
    return Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))


def main() -> int:
    pts, point_adj, lines, axes, Aw = build_w33_axis_graph()
    R, Ae, D = root_lines()
    gm=nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(Aw), nx.from_numpy_array(Ae))
    if not gm.is_isomorphic():
        raise RuntimeError("no 120-graph isomorphism")
    mp=dict(gm.mapping)

    point_triples={p:[i for i,a in enumerate(axes) if a[0]==p] for p in range(40)}
    line_sets={li: sorted({i for i,a in enumerate(axes) if a[0] in L}) for li,L in enumerate(lines)}

    triad_internal_edges=Counter(); triad_dots=Counter(); zero_sum_choices=Counter()
    for p,idx in point_triples.items():
        e=[mp[i] for i in idx]
        triad_internal_edges[sum(int(Ae[i,j]) for i,j in combinations(e,2))]+=1
        triad_dots[tuple(sorted(float(D[i,j]) for i,j in combinations(e,2)))] += 1
        z=0
        for signs in product((1,-1), repeat=3):
            s=sum(signs[k]*R[e[k]] for k in range(3))
            if np.allclose(s,0): z += 1
        zero_sum_choices[z]+=1

    d4_spectra=Counter(); d4_comp_components=Counter(); d4_absdots=Counter()
    for li,idx in line_sets.items():
        e=[mp[i] for i in idx]
        sub=Ae[np.ix_(e,e)]
        d4_spectra[tuple(sorted(eig_counter(sub).items()))]+=1
        comp=1-sub-np.eye(12,dtype=int)
        H=nx.from_numpy_array(comp)
        d4_comp_components[tuple(sorted(len(c) for c in nx.connected_components(H)))] += 1
        d4_absdots[tuple(sorted(Counter(float(D[i,j]) for i,j in combinations(e,2)).items()))]+=1

    inter=Counter(); inter_by_collinearity=defaultdict(Counter)
    for p,q in combinations(range(40),2):
        Pidx=[mp[i] for i in point_triples[p]]; Qidx=[mp[i] for i in point_triples[q]]
        orth=sum(int(Ae[i,j]) for i in Pidx for j in Qidx)
        inter[orth]+=1; inter_by_collinearity[bool(point_adj[p,q])][orth]+=1

    checks={
        "axis_rootline_isomorphism": sum(abs(int(Aw[i,j])-int(Ae[mp[i],mp[j]])) for i in range(120) for j in range(120)) == 0,
        "forty_A2_point_triads": triad_internal_edges == Counter({0:40}) and triad_dots == Counter({(1.0,1.0,1.0):40}) and zero_sum_choices == Counter({2:40}),
        "forty_D4_line_subsystems": d4_spectra == Counter({((-3,3),(0,8),(9,1)):40}) and d4_comp_components == Counter({(3,3,3,3):40}) and d4_absdots == Counter({((0.0,54),(1.0,12)):40}),
        "collinearity_recovered": inter_by_collinearity[True] == Counter({9:240}) and inter_by_collinearity[False] == Counter({3:540}),
    }
    payload={
        "theorem_name":"A2 Point-Triad and D4 Line-Subsystem Decomposition Theorem",
        "summary":{
            "all_checks_passed":all(checks.values()),
            "point_triads":40,
            "line_subsystems":40,
            "point_triad_type":"A2 root-line triad: three nonorthogonal lines with two zero-sum orientations",
            "line_subsystem_type":"D4 root-line subsystem: 12 lines, internal orthogonality graph degree 9",
            "collinearity_rule":"orthogonality count between two point triads is 9 for collinear W33 points and 3 otherwise",
        },
        "checks":checks,
        "point_triads":{"internal_edge_counts":dict(triad_internal_edges),"absolute_dot_patterns":{str(k):v for k,v in triad_dots.items()},"zero_sum_orientation_counts":dict(zero_sum_choices)},
        "line_subsystems":{"spectra":{str(k):v for k,v in d4_spectra.items()},"complement_component_sizes":{str(k):v for k,v in d4_comp_components.items()},"absolute_dot_patterns":{str(k):v for k,v in d4_absdots.items()}},
        "collinearity_recovery":{"overall":dict(inter),"by_w33_collinearity":{str(k):dict(v) for k,v in inter_by_collinearity.items()}},
        "boundary":"Uses one graph-isomorphism choice; the decomposition is verified for that explicit mapping, but a closed-form formula remains future work."
    }
    out=ROOT/"data"/"w33_axis_rootline_a2_d4_decomposition.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
