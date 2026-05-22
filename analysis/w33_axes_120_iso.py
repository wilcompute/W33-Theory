#!/usr/bin/env python3
"""Explicit 120-object isomorphism test.

Builds the W33 local-axis graph and the 120-line orthogonality graph from the
240-vector E8 set, then finds a labeled graph isomorphism.
"""
from __future__ import annotations

import hashlib, json
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
            return tuple((inv*y) % P for y in v)
    raise RuntimeError


def form(u, v):
    return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % P


def params(A):
    deg = Counter(map(int, A.sum(axis=1)))
    lam = Counter(); mu = Counter()
    for i, j in combinations(range(A.shape[0]), 2):
        c = int(A[i] @ A[j])
        (lam if A[i, j] else mu)[c] += 1
    eig = Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
    return dict(deg=deg, lam=lam, mu=mu, eig=eig)


def w33_axes():
    pts = [] ; seen = set()
    for raw in product(range(P), repeat=4):
        if raw == (0,0,0,0): continue
        c = canon(raw)
        if c not in seen:
            seen.add(c); pts.append(c)
    pi = {p:i for i,p in enumerate(pts)}
    edges = [(i,j) for i,j in combinations(range(40),2) if form(pts[i], pts[j]) == 0]
    adj = [[False]*40 for _ in range(40)]
    for i,j in edges: adj[i][j] = adj[j][i] = True
    lines = set()
    for i,j in edges:
        u,v = pts[i], pts[j]
        L = set()
        for a,b in product(range(P), repeat=2):
            if a == 0 and b == 0: continue
            L.add(pi[canon((a*u[t] + b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(L)))
    lines = sorted(lines)
    pl = defaultdict(list); edge_line = {}
    for li,L in enumerate(lines):
        for p in L: pl[p].append(li)
        for e in combinations(L,2): edge_line[tuple(sorted(e))] = li
    axes=[]; vtx_axis={}
    for p in range(40):
        a,b,c,d = sorted(pl[p])
        m = [((a,b),(c,d)), ((a,c),(b,d)), ((a,d),(b,c))]
        for ax in m:
            ax = tuple(sorted(tuple(sorted(x)) for x in ax))
            key=(p,ax); axes.append(key)
            for pair in ax: vtx_axis[(p,pair)] = key
    axes = sorted(axes); ai = {a:i for i,a in enumerate(axes)}
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
            C[ai[vtx_axis[(p,lp)]], qi] = 1
    G=C@C.T
    A=(G>0).astype(np.int8); np.fill_diagonal(A,0)
    return axes, A, C


def e8_lines():
    vecs=[]
    for i in range(8):
        for j in range(i+1,8):
            for si in (1,-1):
                for sj in (1,-1):
                    r=[0]*8; r[i]=si; r[j]=sj; vecs.append(tuple(r))
    for s in product((1,-1), repeat=8):
        if sum(x < 0 for x in s) % 2 == 0:
            vecs.append(tuple(x/2 for x in s))
    V=np.array(vecs,float)
    used=set(); reps=[]
    for i in range(240):
        if i in used: continue
        for j in range(i+1,240):
            if j not in used and np.allclose(V[i]+V[j],0):
                used.add(i); used.add(j)
                reps.append(np.array(min(tuple(V[i]), tuple(V[j])), float))
                break
    reps=sorted(reps, key=lambda r: tuple(r.tolist()))
    R=np.array(reps,float)
    D=np.abs(R@R.T)
    A=np.isclose(D,0).astype(np.int8); np.fill_diagonal(A,0)
    return reps, A


def h(A):
    return hashlib.sha256(A.astype(np.int8).tobytes()).hexdigest()


def main():
    axes, Aw, C = w33_axes()
    reps, Ae = e8_lines()
    m = nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(Aw), nx.from_numpy_array(Ae))
    ok = m.is_isomorphic()
    mp = dict(m.mapping) if ok else {}
    mismatch = sum(abs(int(Aw[i,j]) - int(Ae[mp[i], mp[j]])) for i in range(120) for j in range(120)) if ok else -1
    out = {
        "all_checks_passed": ok and mismatch == 0 and params(Aw) == params(Ae),
        "summary": {
            "w33_axes": 120, "e8_lines": 120, "isomorphism_found": ok,
            "edge_mismatch_count": mismatch,
            "graph_parameters": "SRG(120,63,30,36)",
            "spectrum": "63^1 + 3^84 + (-9)^35",
            "axis_quadrangle_shape": list(C.shape),
            "axis_row_degree": 54,
            "quadrangle_col_weight": 4,
            "w33_graph_sha256": h(Aw), "e8_graph_sha256": h(Ae)
        },
        "w33_params": {k:{str(a):b for a,b in v.items()} for k,v in params(Aw).items()},
        "e8_params": {k:{str(a):b for a,b in v.items()} for k,v in params(Ae).items()},
        "mapping_w33_axis_index_to_e8_line_index": {str(k): int(v) for k,v in sorted(mp.items())},
        "first_12_mapping_rows": [
            {"axis_index": i, "axis": [axes[i][0], [[int(x) for x in pair] for pair in axes[i][1]]], "line_index": int(mp[i])}
            for i in range(12)
        ],
        "boundary": "This is an explicit graph isomorphism. It is not yet a closed-form coordinate formula."
    }
    path = ROOT / "data" / "w33_axes_120_iso.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out["summary"], indent=2, sort_keys=True))
    return 0 if out["all_checks_passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
