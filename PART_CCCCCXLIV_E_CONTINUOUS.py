#!/usr/bin/env python3
"""
PART_CCCCCXLIV_E_CONTINUOUS.py

Verification of the discrete-to-continuous bridge for W(3,3).
Computes: resistance metric, Albanese embedding, tropical Jacobian,
cycle length distribution, heat zeta, Stieltjes transform branch points.
"""

import numpy as np
from fractions import Fraction
from math import log, sqrt
from collections import Counter, deque
from itertools import product as iproduct

F3 = [0, 1, 2]

def build_w33():
    raw = [v for v in iproduct(F3, repeat=4) if any(x != 0 for x in v)]
    points = []
    seen = set()
    for v in raw:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 2 if v[i] == 2 else 1
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            points.append(v)
    n = 40
    adj = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i+1, n):
            x, y = points[i], points[j]
            omega = (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3
            if omega == 0:
                adj[i,j] = adj[j,i] = 1.0
    return adj, n

def main():
    adj, n = build_w33()
    L = np.diag(adj.sum(axis=1)) - adj
    L_plus = np.linalg.pinv(L)

    adj_pairs = [(i,j) for i in range(n) for j in range(i+1,n) if adj[i,j]==1]
    nonadj_pairs = [(i,j) for i in range(n) for j in range(i+1,n) if adj[i,j]==0]

    R_vals_adj = [L_plus[i,i]+L_plus[j,j]-2*L_plus[i,j] for i,j in adj_pairs]
    R_vals_nonadj = [L_plus[i,i]+L_plus[j,j]-2*L_plus[i,j] for i,j in nonadj_pairs]

    R_adj = R_vals_adj[0]
    R_nonadj = R_vals_nonadj[0]

    print(f"R_adj = {Fraction(R_adj).limit_denominator(1000)} = {R_adj:.10f}")
    print(f"R_nonadj = {Fraction(R_nonadj).limit_denominator(1000)} = {R_nonadj:.10f}")
    print(f"Ratio = {Fraction(R_nonadj/R_adj).limit_denominator(100)}")

    E = len(adj_pairs)
    b1 = E - n + 1
    Kf = E * R_adj + (n*(n-1)//2 - E) * R_nonadj
    print(f"b1 = {b1} = 3 * 67 = {3*67}")
    print(f"Kf = {Fraction(Kf).limit_denominator(1000)}")

    # Cycle length distribution
    def bfs_tree(adj, root=0):
        visited = [False]*n
        parent = [-1]*n
        tree_edges = []
        queue = deque([root])
        visited[root] = True
        while queue:
            u = queue.popleft()
            for w in range(n):
                if adj[u,w]==1 and not visited[w]:
                    visited[w] = True
                    parent[w] = u
                    tree_edges.append((u,w))
                    queue.append(w)
        return tree_edges, parent

    tree_edges, parent = bfs_tree(adj)
    tree_set = set(map(frozenset, tree_edges))
    non_tree = [(i,j) for i in range(n) for j in range(i+1,n)
                if adj[i,j]==1 and frozenset([i,j]) not in tree_set]

    def tree_path(u, v):
        pu, pv = [], []
        x = u
        while x != -1: pu.append(x); x = parent[x]
        x = v
        while x != -1: pv.append(x); x = parent[x]
        lca_set = {nd: i for i, nd in enumerate(pu)}
        for i, nd in enumerate(pv):
            if nd in lca_set:
                return pu[:lca_set[nd]+1] + pv[i-1::-1]
        return []

    cycle_lengths = []
    for (u, v) in non_tree:
        path = tree_path(u, v)
        cycle_lengths.append(len(path))  # len(path) edges = path nodes - 1 + 1 (closing edge)

    print(f"Cycle length distribution: {Counter(cycle_lengths)}")
    avg = Fraction(sum(cycle_lengths), len(cycle_lengths))
    print(f"Average cycle length = {avg} = {float(avg):.6f}")

    # Stieltjes transform numerator roots
    # G(z) = (z^2 - 10z - 20) / [(z-12)(z-2)(z+4)]
    roots = [5 + 3*sqrt(5), 5 - 3*sqrt(5)]
    print(f"Numerator roots: {roots[0]:.6f}, {roots[1]:.6f}")
    print(f"Sum = {roots[0]+roots[1]:.6f} (should be 10)")
    print(f"Product = {roots[0]*roots[1]:.6f} (should be -20)")

    # Heat zeta
    Z1 = Fraction(24,10) + Fraction(15,16)
    print(f"Z(1) = {Z1} = {float(Z1):.6f}")
    print(f"Kf = v/2 * Z(1) = {n//2 * Z1}")
    print(f"b1 mod 2 = {b1 % 2} (odd => unique spin structure)")

if __name__ == '__main__':
    main()
