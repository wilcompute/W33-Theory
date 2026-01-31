#!/usr/bin/env python3
"""Find an embedding of the Schlaefli 27 graph (lines on cubic) inside W(3,3) lines.

Procedure:
- construct the Schlaefli adjacency from a 27-orbit of W(E6) (E8 roots) (re-uses logic)
- build W33 points and 40 lines (K4 cliques of the point graph)
- build the line-disjointness graph on 40 lines (edge if two lines are skew/disjoint)
- search for a 27-node induced subgraph isomorphic to the Schlaefli graph using VF2
- if found, write mapping and compute stabilizer size of the corresponding double-six pulled back to W33

Outputs:
- tools/artifacts/schlafli_embedding.json (mapping and stabilizer summary)
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

# --- E8 / Schlaefli helper (copied) ---
E8_SIMPLE_ROOTS = np.array(
    [
        [1, -1, 0, 0, 0, 0, 0, 0],
        [0, 1, -1, 0, 0, 0, 0, 0],
        [0, 0, 1, -1, 0, 0, 0, 0],
        [0, 0, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, 0, 1, -1, 0, 0],
        [0, 0, 0, 0, 0, 1, -1, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
    ],
    dtype=float,
)
E6_SIMPLE_ROOTS = E8_SIMPLE_ROOTS[2:8]


def construct_e8_roots():
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in [1.0, -1.0]:
                for sj in [1.0, -1.0]:
                    r = np.zeros(8)
                    r[i], r[j] = si, sj
                    roots.append(r)
    for bits in range(256):
        signs = np.array([1.0 if (bits >> k) & 1 else -1.0 for k in range(8)])
        if int(np.sum(signs < 0)) % 2 == 0:
            roots.append(signs * 0.5)
    return np.array(roots)


def snap(v: np.ndarray, tol: float = 1e-6):
    s = np.round(v * 2) / 2
    if np.max(np.abs(v - s)) < tol:
        return tuple(s.tolist())
    return tuple(np.round(v, 8).tolist())


def weyl_reflect(v: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    return v - 2 * np.dot(v, alpha) / np.dot(alpha, alpha) * alpha


def compute_we6_orbits(roots: np.ndarray):
    keys = [snap(r) for r in roots]
    key_to_idx = {k: i for i, k in enumerate(keys)}
    used = np.zeros(len(roots), dtype=bool)
    orbits = []
    for start in range(len(roots)):
        if used[start]:
            continue
        orbit = [start]
        used[start] = True
        frontier = [start]
        while frontier:
            cur = frontier.pop()
            v = roots[cur]
            for alpha in E6_SIMPLE_ROOTS:
                w = weyl_reflect(v, alpha)
                j = key_to_idx[snap(w)]
                if not used[j]:
                    used[j] = True
                    orbit.append(j)
                    frontier.append(j)
        orbits.append(orbit)
    return orbits


def build_schlafli_adj(roots: np.ndarray, orbit_idx):
    R = roots[orbit_idx]
    gram = R @ R.T
    n = len(orbit_idx)
    adj = np.zeros((n, n), dtype=np.uint8)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(gram[i, j] - 1.0) < 1e-9:
                adj[i, j] = adj[j, i] = 1
    return adj


# --- W33 helper ---


def canonical_point(v):
    v = tuple(int(x % 3) for x in v)
    if not any(v):
        return None
    for i in range(4):
        if v[i] != 0:
            inv = 1 if v[i] == 1 else 2
            return tuple((inv * x) % 3 for x in v)
    raise RuntimeError()


def construct_w33_points():
    pts = []
    seen = set()
    for vec in itertools.product([0, 1, 2], repeat=4):
        if vec == (0, 0, 0, 0):
            continue
        rep = canonical_point(vec)
        if rep not in seen:
            seen.add(rep)
            pts.append(rep)
    return pts


def omega(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def compute_w33_lines(points):
    # isotropic 2-dim subspaces (lines) -> 40 lines each with 4 points
    idx = {p: i for i, p in enumerate(points)}
    lines = set()
    n = len(points)
    for i in range(n):
        p = points[i]
        for j in range(i + 1, n):
            q = points[j]
            if omega(p, q) != 0:
                continue
            sub = set()
            for a in [0, 1, 2]:
                for b in [0, 1, 2]:
                    if a == 0 and b == 0:
                        continue
                    vec = tuple(((a * p[k] + b * q[k]) % 3) for k in range(4))
                    rep = canonical_point(vec)
                    sub.add(rep)
            if len(sub) == 4:
                lines.add(tuple(sorted(idx[v] for v in sub)))
    return sorted(lines)


# --- embedding search ---


def main():
    roots = construct_e8_roots()
    orbits = compute_we6_orbits(roots)
    o27 = next(o for o in orbits if len(o) == 27)
    sch_adj = build_schlafli_adj(roots, o27)
    G_sch = nx.Graph()
    G_sch.add_nodes_from(range(27))
    for i in range(27):
        for j in range(i + 1, 27):
            if sch_adj[i, j]:
                G_sch.add_edge(i, j)

    wpts = construct_w33_points()
    wlines = compute_w33_lines(wpts)
    # Line-line disjointness graph
    G_lines = nx.Graph()
    G_lines.add_nodes_from(range(len(wlines)))
    for i in range(len(wlines)):
        for j in range(i + 1, len(wlines)):
            if set(wlines[i]).isdisjoint(set(wlines[j])):
                G_lines.add_edge(i, j)

    print("W33 lines:", len(wlines))
    print("Schlafli degrees in 27-graph should be 16; checking...")
    degs = [d for _, d in G_sch.degree()]
    print(Counter(degs))

    # GraphMatcher: find subgraph in G_lines isomorphic to G_sch
    GM = nx.algorithms.isomorphism.GraphMatcher(G_lines, G_sch)
    mapping = None
    for iso in GM.subgraph_isomorphisms_iter():
        mapping = iso
        break

    if mapping is None:
        print(
            "No embedding of Schlaefli graph found inside W33 line-disjointness graph."
        )
        return

    # mapping: keys are nodes in G_lines, values are nodes in G_sch. invert
    sch_to_w = {sch_i: int(w_i) for w_i, sch_i in mapping.items()}

    # example double-six from earlier we6 output
    # we can reconstruct example from double_six_from_schlafli.py deterministic example
    # use find_k6_cliques and is_double_six from that context to get an example A,B

    # For now, compute stabilizer size of an example double-six pulled back
    # Use the example from w33_we6_double_six_stabilizer's output: A and B lists
    example = {
        "A": [0, 1, 2, 3, 4, 26],
        "B": [19, 20, 21, 22, 24, 25],
    }
    # map schlafli indices to w33 line indices
    A_lines = [wlines[sch_to_w[a]] for a in example["A"]]
    B_lines = [wlines[sch_to_w[b]] for b in example["B"]]

    # build automorphism group on 40 points using symplectic similitudes (reuse earlier code)
    # simple version: re-run generator closure (not saved)
    from w33_aut_group_construct import build_points, generate_group

    pts = build_points()
    G, gens = generate_group(pts)

    # function to see image of a line set under permutation p
    def image_of_lineset(p, lineset):
        return {tuple(sorted(p[i] for i in line)) for line in lineset}

    Aset = set(tuple(sorted(l)) for l in A_lines)
    Bset = set(tuple(sorted(l)) for l in B_lines)

    stab = 0
    for g in G:
        Ag = image_of_lineset(g, A_lines)
        Bg = image_of_lineset(g, B_lines)
        if (Ag == Aset and Bg == Bset) or (Ag == Bset and Bg == Aset):
            stab += 1

    out = {
        "sch_to_w_mapping": sch_to_w,
        "A_w33_lines": [list(map(int, l)) for l in A_lines],
        "B_w33_lines": [list(map(int, l)) for l in B_lines],
        "pullback_double_six_stabilizer_size": stab,
    }
    (ART / "schlafli_embedding.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Found embedding and wrote artifacts/schlafli_embedding.json")


if __name__ == "__main__":
    main()
