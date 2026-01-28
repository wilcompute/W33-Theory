#!/usr/bin/env python3
"""Analyze H27 vs Schläfli graph and switching equivalence.

Builds:
- H27: induced subgraph on 27 non-neighbors of a W33 vertex
- Schläfli intersection graph (27 lines on cubic surface)
- Schläfli skew graph (complement of intersection)

Computes:
- SRG parameters (k, λ, μ)
- Seidel matrix eigenvalues (switching class invariants)
- Triangle counts and spectra
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    n = len(proj_points)

    def omega(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1

    return adj, proj_points


def h27_from_w33(adj, v0=0):
    n = adj.shape[0]
    non_neighbors = [j for j in range(n) if j != v0 and adj[v0, j] == 0]
    idx = {v: i for i, v in enumerate(non_neighbors)}

    h_adj = np.zeros((27, 27), dtype=int)
    for i, vi in enumerate(non_neighbors):
        for j, vj in enumerate(non_neighbors):
            if i < j and adj[vi, vj]:
                h_adj[i, j] = h_adj[j, i] = 1

    return h_adj, non_neighbors


# --- Schläfli graph via blow-up model ---

def build_27_lines():
    lines = []
    for i in range(1, 7):
        lines.append(('E', i))  # exceptional
    for i in range(1, 7):
        lines.append(('C', i))  # conics
    for i in range(1, 7):
        for j in range(i+1, 7):
            lines.append(('L', i, j))  # line through i,j
    return lines


def lines_intersect(L1, L2):
    if L1 == L2:
        return False

    t1, t2 = L1[0], L2[0]

    # E_i
    if t1 == 'E' and t2 == 'E':
        return False
    if t1 == 'C' and t2 == 'C':
        return False

    # E_i with C_j
    if t1 == 'E' and t2 == 'C':
        return L1[1] != L2[1]
    if t1 == 'C' and t2 == 'E':
        return L1[1] != L2[1]

    # E_i with L_{jk}
    if t1 == 'E' and t2 == 'L':
        return L1[1] in L2[1:]
    if t1 == 'L' and t2 == 'E':
        return L2[1] in L1[1:]

    # C_i with L_{jk}
    if t1 == 'C' and t2 == 'L':
        return L1[1] in L2[1:]
    if t1 == 'L' and t2 == 'C':
        return L2[1] in L1[1:]

    # L_{ij} with L_{kl}
    if t1 == 'L' and t2 == 'L':
        s1 = set(L1[1:])
        s2 = set(L2[1:])
        # intersect iff disjoint pairs
        return len(s1 & s2) == 0

    return False


def schlafli_intersection_graph():
    lines = build_27_lines()
    n = len(lines)
    adj = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i+1, n):
            if lines_intersect(lines[i], lines[j]):
                adj[i, j] = adj[j, i] = 1

    return adj, lines


def graph_parameters(adj):
    n = adj.shape[0]
    degrees = adj.sum(axis=1)
    k_set = set(int(d) for d in degrees)
    k = int(degrees[0]) if len(k_set) == 1 else None

    # lambda, mu
    lam_set = set()
    mu_set = set()
    for i in range(n):
        for j in range(i+1, n):
            common = int(np.dot(adj[i], adj[j]))
            if adj[i, j] == 1:
                lam_set.add(common)
            else:
                mu_set.add(common)

    return {
        "n": n,
        "degree_set": sorted(k_set),
        "k": k,
        "lambda_set": sorted(lam_set),
        "mu_set": sorted(mu_set),
        "edges": int(adj.sum() // 2),
    }


def seidel_eigenvalues(adj):
    n = adj.shape[0]
    # Seidel matrix: 0 on diag, -1 for edges, +1 for non-edges
    J = np.ones((n, n), dtype=int)
    S = J - np.eye(n, dtype=int) - 2 * adj
    eigs = np.linalg.eigvalsh(S)
    # round for stability
    return [round(float(x), 6) for x in eigs]


def triangle_count(adj):
    # count triangles via trace(A^3)/6
    A = adj.astype(int)
    return int(np.trace(A @ A @ A) // 6)


def main():
    # W33 -> H27
    w33_adj, _ = build_w33()
    h_adj, h_vertices = h27_from_w33(w33_adj, v0=0)

    # Schläfli graphs
    sch_adj, lines = schlafli_intersection_graph()
    sch_comp = np.ones_like(sch_adj) - np.eye(sch_adj.shape[0], dtype=int) - sch_adj

    # Parameters
    h_params = graph_parameters(h_adj)
    sch_params = graph_parameters(sch_adj)
    comp_params = graph_parameters(sch_comp)

    # Seidel spectra
    h_seidel = seidel_eigenvalues(h_adj)
    sch_seidel = seidel_eigenvalues(sch_adj)
    comp_seidel = seidel_eigenvalues(sch_comp)

    # Triangle counts
    h_tri = triangle_count(h_adj)
    sch_tri = triangle_count(sch_adj)
    comp_tri = triangle_count(sch_comp)

    results = {
        "h27_params": h_params,
        "schlafli_intersection_params": sch_params,
        "schlafli_skew_params": comp_params,
        "h27_triangles": h_tri,
        "schlafli_intersection_triangles": sch_tri,
        "schlafli_skew_triangles": comp_tri,
        "h27_seidel_eigs": h_seidel,
        "schlafli_intersection_seidel_eigs": sch_seidel,
        "schlafli_skew_seidel_eigs": comp_seidel,
    }

    out_path = ROOT / "artifacts" / "schlafli_h27_switching.json"
    out_path.write_text(np.array2string(np.array(h_seidel)) + "\n")
    # overwrite with JSON for stability
    import json
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("H27 params:", h_params)
    print("Schlafli intersection params:", sch_params)
    print("Schlafli skew params:", comp_params)
    print("Triangle counts:", h_tri, sch_tri, comp_tri)
    print("Seidel eigenvalue multiset sizes:", len(set(h_seidel)), len(set(sch_seidel)), len(set(comp_seidel)))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
