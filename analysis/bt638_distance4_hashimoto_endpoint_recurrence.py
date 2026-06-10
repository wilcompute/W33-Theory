#!/usr/bin/env python3
"""BT638: distance-4 Hashimoto endpoint recurrence.

Build W(3,3) as the symplectic polar graph on PG(3,3), fold directed
Hashimoto walks to Levi flags, and verify that the terminal distance-4 endpoint
sequence is governed by the full Ihara/Hashimoto polynomial.  Omitting the -1
trivial sheet leaves the alternating +/-24 parity residue.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
import networkx as nx
import numpy as np


def norm(v):
    for x in v:
        if x % 3:
            inv = 1 if x == 1 else 2
            return tuple((inv*y) % 3 for y in v)
    raise ValueError("zero")


def form(a,b):
    return (a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1]) % 3


def poly_res(coeff, seq, n):
    return sum(coeff[i]*seq[n-i] for i in range(len(coeff)))


def main():
    pts = sorted({norm(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    G = nx.Graph(); G.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if form(pts[i], pts[j]) == 0: G.add_edge(i,j)

    lines = sorted(tuple(sorted(c)) for c in nx.find_cliques(G) if len(c)==4)
    edge_to_line = {}
    for li,L in enumerate(lines):
        for e in itertools.combinations(L,2): edge_to_line[tuple(sorted(e))] = li

    flags = sorted((p,li) for li,L in enumerate(lines) for p in L)
    fidx = {f:i for i,f in enumerate(flags)}
    X = nx.Graph(); X.add_nodes_from(range(160))
    for i,(p,l) in enumerate(flags):
        for j in range(i+1,160):
            q,m = flags[j]
            if p==q or l==m: X.add_edge(i,j)
    dist = np.zeros((160,160), dtype=np.int8)
    for i,dmap in nx.all_pairs_shortest_path_length(X):
        for j,d in dmap.items(): dist[i,j]=d

    arcs = sorted([(u,v) for u,v in G.edges()] + [(v,u) for u,v in G.edges()])
    aidx = {a:i for i,a in enumerate(arcs)}
    B = np.zeros((480,480), dtype=np.int64)
    for ai,(u,v) in enumerate(arcs):
        for w in G.neighbors(v):
            if w != u: B[ai,aidx[(v,w)]] = 1
    T = np.zeros((160,480), dtype=np.int64)
    for ai,(p,q) in enumerate(arcs):
        T[fidx[(p, edge_to_line[tuple(sorted((p,q)))])], ai] = 1

    endpoint=[]; shell_sets={}
    P = np.eye(480, dtype=np.int64)
    for n in range(11):
        if n>0: P = P @ B
        F = T @ P @ T.T
        shell_sets[str(n)] = {str(r): sorted(set(map(int, F[dist==r].ravel()))) for r in range(5)}
        v4 = shell_sets[str(n)]["4"]
        assert len(v4) == 1
        endpoint.append(v4[0])

    full = [1,-9,-9,-123,-113,-1199,121,1331]
    no_minus = [1,-10,1,-124,11,-1210,1331]
    full_res = [poly_res(full, endpoint, n) for n in range(7,11)]
    no_minus_res = [poly_res(no_minus, endpoint, n) for n in range(6,11)]

    checks = {
        "W33_40_240_12": (G.number_of_nodes(), G.number_of_edges(), sorted(set(dict(G.degree()).values()))) == (40,240,[12]),
        "lines_40_partition_edges_240": len(lines)==40 and len(edge_to_line)==240,
        "flag_graph_160_480_6_diam4": (X.number_of_nodes(), X.number_of_edges(), sorted(set(dict(X.degree()).values())), nx.diameter(X)) == (160,480,[6],4),
        "hashimoto_480_fold_TTt_3I": B.shape==(480,480) and np.array_equal(T@T.T, 3*np.eye(160,dtype=np.int64)),
        "terminal_uniform_0_to_10": all(len(shell_sets[str(n)]["4"])==1 for n in range(11)),
        "full_recurrence_zero": full_res == [0,0,0,0],
        "minus_one_omission_residue_pm24": no_minus_res == [24,-24,24,-24,24],
        "cubic_endpoint_mu28": endpoint[3] == 28,
    }
    result = {
        "bt":638,
        "title":"Distance-4 Hashimoto endpoint recurrence theorem",
        "endpoint_values_n0_to_n10": endpoint,
        "full_hashimoto_polynomial":"(x-11)(x-1)(x+1)(x^2-2x+11)(x^2+4x+11)",
        "full_coefficients": full,
        "full_residuals_n7_to_n10": full_res,
        "without_minus_one_residuals_n6_to_n10": no_minus_res,
        "generating_function":"z^2(3+z-11z^2-33z^3)/((1-z^2)(1-11z)(1-2z+11z^2)(1+4z+11z^2))",
        "key_interpretation":"Terminal distance-4 folded-Hashimoto endpoints carry the full Ihara recurrence; the omitted -1 sheet is exactly an alternating +/-24 parity residue.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out=Path("data/PART_BT638_DISTANCE4_HASHIMOTO_ENDPOINT_RECURRENCE_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
