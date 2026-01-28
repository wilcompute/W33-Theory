#!/usr/bin/env python3
"""Greedy decision tree for Z3 edge labels from simple features."""
from __future__ import annotations

from itertools import product
import json
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_witting_40_rays():
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays = []
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -omega**mu, omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -omega**mu, -omega**nu]) / sqrt3)
            rays.append(np.array([1, -omega**mu, 0, omega**nu]) / sqrt3)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
    return rays


def construct_f3_points():
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
    return proj_points


def omega_symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build_nonorth_edges(rays, tol=1e-8):
    edges = []
    for i in range(len(rays)):
        for j in range(i + 1, len(rays)):
            if abs(np.vdot(rays[i], rays[j])) >= tol:
                edges.append((i, j))
    return edges


def phase_to_k(angle):
    return int(np.rint(angle / (np.pi / 6.0))) % 12


def solve_edge_potential(rays):
    edges = build_nonorth_edges(rays)
    edge_index = {e: idx for idx, e in enumerate(edges)}
    triangles = []
    for i in range(40):
        for j in range(i + 1, 40):
            if (i, j) not in edge_index:
                continue
            for k in range(j + 1, 40):
                if (i, k) in edge_index and (j, k) in edge_index:
                    triangles.append((i, j, k))

    d1 = np.zeros((len(triangles), len(edges)), dtype=int)
    t = np.zeros(len(triangles), dtype=int)
    for t_idx, (i, j, k) in enumerate(triangles):
        e_jk = edge_index[(j, k)]
        e_ik = edge_index[(i, k)]
        e_ij = edge_index[(i, j)]
        d1[t_idx, e_jk] = 1
        d1[t_idx, e_ik] = -1
        d1[t_idx, e_ij] = 1
        ip = np.vdot(rays[i], rays[j]) * np.vdot(rays[j], rays[k]) * np.conjugate(np.vdot(rays[i], rays[k]))
        t[t_idx] = phase_to_k(np.angle(ip)) % 3

    # solve d1 x = t over GF(3)
    A = d1.copy() % 3
    b = t.copy() % 3
    m, n = A.shape
    row = 0
    piv = [-1] * n
    for col in range(n):
        pivot = None
        for r in range(row, m):
            if A[r, col] % 3 != 0:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
            b[[row, pivot]] = b[[pivot, row]]
        inv = 1 if A[row, col] == 1 else 2
        A[row] = (A[row] * inv) % 3
        b[row] = (b[row] * inv) % 3
        for r in range(m):
            if r == row:
                continue
            if A[r, col] % 3 != 0:
                factor = A[r, col] % 3
                A[r] = (A[r] - factor * A[row]) % 3
                b[r] = (b[r] - factor * b[row]) % 3
        piv[col] = row
        row += 1
        if row == m:
            break
    x = np.zeros(n, dtype=int)
    for col, r in enumerate(piv):
        if r != -1:
            x[col] = b[r] % 3
    return edges, x


def ray_family(idx):
    if idx < 4:
        return ("B", None, None)
    t = idx - 4
    pair = t // 4
    fam = t % 4
    mu = pair // 3
    nu = pair % 3
    return (f"F{fam}", mu, nu)


def build_features(edges, labels, mapping=None, f3_points=None):
    rows = []
    ys = []
    for idx, (i, j) in enumerate(edges):
        fi, mui, nui = ray_family(i)
        fj, muj, nuj = ray_family(j)
        bi = 1 if i < 4 else 0
        bj = 1 if j < 4 else 0
        same_fam = 1 if fi == fj else 0
        # support sizes (nonzero coords)
        nz_i = sum(1 for z in construct_witting_40_rays()[i] if abs(z) > 1e-9)
        nz_j = sum(1 for z in construct_witting_40_rays()[j] if abs(z) > 1e-9)
        # symplectic omega if mapping present
        if mapping is not None:
            pi = f3_points[mapping[i]]
            pj = f3_points[mapping[j]]
            w = omega_symp(pi, pj)
        else:
            w = 0
        rows.append({
            "fam_i": fi,
            "fam_j": fj,
            "same_fam": same_fam,
            "basis": (bi, bj),
            "mu_i": 0 if mui is None else mui,
            "nu_i": 0 if nui is None else nui,
            "mu_j": 0 if muj is None else muj,
            "nu_j": 0 if nuj is None else nuj,
            "support": (min(nz_i, nz_j), max(nz_i, nz_j)),
            "omega": w,
        })
        ys.append(int(labels[idx]))
    return rows, ys


def gini(counts):
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return 1.0 - sum((c/total)**2 for c in counts.values())


def best_split(rows, ys, features):
    best = None
    n = len(rows)
    base = gini(Counter(ys))
    for feat in features:
        buckets = defaultdict(list)
        for r, y in zip(rows, ys):
            buckets[r[feat]].append(y)
        # compute weighted gini
        w = 0.0
        for vals in buckets.values():
            w += (len(vals)/n) * gini(Counter(vals))
        gain = base - w
        if best is None or gain > best[0]:
            best = (gain, feat, buckets)
    return best


def build_tree(rows, ys, features, depth=0, max_depth=3):
    counts = Counter(ys)
    if depth >= max_depth or len(counts) == 1:
        return {"leaf": True, "label": counts.most_common(1)[0][0], "counts": dict(counts)}
    gain, feat, buckets = best_split(rows, ys, features)
    if gain <= 1e-6:
        return {"leaf": True, "label": counts.most_common(1)[0][0], "counts": dict(counts)}
    node = {"leaf": False, "feature": feat, "gain": gain, "children": {}}
    for key, vals in buckets.items():
        sub_rows = [r for r, y in zip(rows, ys) if r[feat] == key]
        sub_ys = [y for r, y in zip(rows, ys) if r[feat] == key]
        node["children"][str(key)] = build_tree(sub_rows, sub_ys, features, depth+1, max_depth)
    return node


def predict(tree, row):
    if tree["leaf"]:
        return tree["label"]
    key = str(row[tree["feature"]])
    if key not in tree["children"]:
        # fallback to majority
        counts = Counter()
        for child in tree["children"].values():
            if child["leaf"]:
                counts[child["label"]] += sum(child["counts"].values())
        if counts:
            return counts.most_common(1)[0][0]
        return 0
    return predict(tree["children"][key], row)


def tree_accuracy(tree, rows, ys):
    correct = 0
    for r, y in zip(rows, ys):
        if predict(tree, r) == y:
            correct += 1
    return correct / len(ys)


def main():
    print("Z3 EDGE LABEL DECISION TREE")
    print("=" * 60)
    rays = construct_witting_40_rays()
    edges, labels = solve_edge_potential(rays)

    map_path = ROOT / "artifacts" / "witting_graph_isomorphism.json"
    if map_path.exists():
        mapping = json.loads(map_path.read_text())["mapping"]
        mapping = {int(k): int(v) for k, v in mapping.items()}
        f3_points = construct_f3_points()
    else:
        mapping = None
        f3_points = None

    rows, ys = build_features(edges, labels, mapping, f3_points)
    features = ["fam_i", "fam_j", "same_fam", "basis", "mu_i", "nu_i", "mu_j", "nu_j", "support", "omega"]

    tree = build_tree(rows, ys, features, max_depth=3)
    acc = tree_accuracy(tree, rows, ys)

    out_path = ROOT / "docs" / "witting_z3_edge_potential_tree.md"
    with out_path.open("w", encoding="utf-8") as f:
        f.write("# Z3 Edge Potential: Greedy Decision Tree\n\n")
        f.write(f"Accuracy (depth<=3): {acc:.3f}\n\n")
        f.write("Tree:\n\n")
        f.write("```\n")
        f.write(str(tree))
        f.write("\n```\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
