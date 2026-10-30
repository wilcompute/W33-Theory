"""Find a global linear transform mapping W33 edge lifts to E8 roots and compute a one-to-one mapping.

Algorithm:
 1. Use anchor matches from HYBRID_BIJECTION_CONSTRUCTION strategies (diff_pad, diff_double, concat)
 2. Compute Procrustes/Kabsch rotation + uniform scale aligning anchor lifts to E8 roots
 3. Apply transform to lifts for all edges (try multiple lift strategies/variants) and compute nearest E8 root
 4. Solve greedy minimal-distance bipartite matching (edge -> root) and report coverage
 5. Save mapping and diagnostics to artifacts/edge_root_mapping.json

This is heuristic but deterministic given the anchor set.
"""

import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

from utils.json_safe import dump_json

# Ensure repo root is in sys.path so top-level modules are importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Import construction helpers from existing module
from HYBRID_BIJECTION_CONSTRUCTION import (
    build_E8_roots,
    build_W33,
    is_E8_root,
    lift_concat,
    lift_diff_double,
    lift_diff_pad,
    lift_diff_pad_right,
    lift_half_int,
    lift_sum_double,
    lift_sum_pad,
)

ARTIFACTS = Path("artifacts")
ARTIFACTS.mkdir(parents=True, exist_ok=True)


def anchors_from_strategies():
    """Return list of anchor pairs (edge_idx, lift_vec (8,), root (8,))"""
    vertices, edges = build_W33()
    e8_roots = build_E8_roots()
    E8_set = set(e8_roots)

    anchors = []
    # expanded set of strategies (including half-int and variant families) to increase anchor coverage
    strategies = [
        lift_diff_pad,
        lift_diff_double,
        lift_concat,
        lift_diff_pad_right,
        lift_sum_pad,
        lift_sum_double,
        lift_half_int,
    ]
    # also try scaled/variant families
    from HYBRID_BIJECTION_CONSTRUCTION import (
        lift_concat_variants,
        lift_diff_scaled_variants,
        lift_half_int_variants,
    )

    for lift_fn in strategies:
        for i in range(len(edges)):
            vec = lift_fn(i)
            is_root, root = is_E8_root(vec)
            if is_root:
                anchors.append(
                    (i, np.array(vec, dtype=float), np.array(root, dtype=float))
                )

    # try family variants (may return multiple vectors per edge)
    for i in range(len(edges)):
        try:
            for vec in lift_diff_scaled_variants(i):
                is_root, root = is_E8_root(vec)
                if is_root:
                    anchors.append(
                        (i, np.array(vec, dtype=float), np.array(root, dtype=float))
                    )
        except Exception:
            pass
        try:
            for vec in lift_concat_variants(i):
                is_root, root = is_E8_root(vec)
                if is_root:
                    anchors.append(
                        (i, np.array(vec, dtype=float), np.array(root, dtype=float))
                    )
        except Exception:
            pass
        try:
            for vec in lift_half_int_variants(i):
                is_root, root = is_E8_root(vec)
                if is_root:
                    anchors.append(
                        (i, np.array(vec, dtype=float), np.array(root, dtype=float))
                    )
        except Exception:
            pass

    # unique anchors by edge (prefer half-integer matches if available)
    anchors_by_edge = {}
    for eidx, vec, root in anchors:
        if eidx not in anchors_by_edge or (
            not all(c == int(c) for c in anchors_by_edge[eidx][1])
            and all(c != int(c) for c in root)
        ):
            # prefer half-int root match for the same edge
            anchors_by_edge[eidx] = (vec, root)
    return [(e, v, r) for e, (v, r) in anchors_by_edge.items()]


def compute_procrustes(A, B, allow_scale=True):
    """Compute linear transform (s,R,t) minimizing ||s*A*R + t - B||_F.

    Returns scale s (float), rotation R (8x8 ndarray), translation t (1x8 ndarray)
    """
    assert A.shape == B.shape
    n, d = A.shape
    # centroids
    muA = A.mean(axis=0)
    muB = B.mean(axis=0)
    A0 = A - muA
    B0 = B - muB

    # covariance matrix
    H = A0.T.dot(B0)
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T.dot(U.T)
    # Handle reflection
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T.dot(U.T)
    if allow_scale:
        scale = np.trace(np.diag(S)) / np.sum(A0**2)
    else:
        scale = 1.0

    t = muB - scale * (muA.dot(R))
    return scale, R, t


def all_lift_variants(edge_idx):
    """Return a list of candidate lift vectors for the given edge index."""
    from HYBRID_BIJECTION_CONSTRUCTION import (
        lift_concat,
        lift_concat_variants,
        lift_diff_double,
        lift_diff_pad,
        lift_diff_pad_right,
        lift_diff_scaled_variants,
        lift_half_int,
        lift_half_int_variants,
        lift_sum_double,
        lift_sum_pad,
    )

    vecs = []
    for fn in [
        lift_diff_pad,
        lift_diff_double,
        lift_concat,
        lift_diff_pad_right,
        lift_sum_pad,
        lift_sum_double,
        lift_half_int,
    ]:
        try:
            v = fn(edge_idx)
            vecs.append(np.array(v, dtype=float))
        except Exception:
            pass

    # add variants
    try:
        for vv in lift_diff_scaled_variants(edge_idx):
            vecs.append(np.array(vv, dtype=float))
    except Exception:
        pass
    try:
        for vv in lift_concat_variants(edge_idx):
            vecs.append(np.array(vv, dtype=float))
    except Exception:
        pass
    try:
        for vv in lift_half_int_variants(edge_idx):
            vecs.append(np.array(vv, dtype=float))
    except Exception:
        pass

    # Deduplicate
    uniq = []
    seen = set()
    for v in vecs:
        key = tuple(np.round(v, 8))
        if key not in seen:
            seen.add(key)
            uniq.append(v)
    return uniq


def nearest_root(vec, roots):
    """Return (root, dist) nearest to vec from roots (ndarray list)."""
    arr = np.vstack(roots)
    dists = np.linalg.norm(arr - vec.reshape(1, -1), axis=1)
    idx = int(np.argmin(dists))
    return tuple(arr[idx]), float(dists[idx])


def greedy_bipartite_match(candidate_triples, n_edges, n_roots):
    """Greedy assignment from sorted candidate triples (edge, root, dist).
    candidate_triples should be sorted by dist ascending.
    Returns dict edge->root and stats.
    """
    assigned_edges = set()
    assigned_roots = set()
    mapping = {}
    for eidx, rtuple, dist in candidate_triples:
        if eidx in assigned_edges or rtuple in assigned_roots:
            continue
        mapping[eidx] = rtuple
        assigned_edges.add(eidx)
        assigned_roots.add(rtuple)
        if len(assigned_edges) == n_edges or len(assigned_roots) == n_roots:
            break
    return mapping


def compute_line_graph_embedding(k=16):
    """Compute spectral embedding of the line graph of W33 edges."""
    # Build line graph adjacency directly (avoid external dependency on networkx)
    vertices, edges = build_W33()
    n = len(edges)
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        u, v = edges[i]
        for j in range(i + 1, n):
            a, b = edges[j]
            # line graph adjacency: edges share a vertex
            if u == a or u == b or v == a or v == b:
                A[i, j] = A[j, i] = 1.0

    # spectral embedding via eigenvectors of adjacency
    vals, vecs = np.linalg.eigh(A)
    idx = np.argsort(vals)[::-1]
    vecs = vecs[:, idx]
    k = min(k, vecs.shape[1])
    emb = vecs[:, :k]
    # normalize rows
    norms = np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12
    emb = emb / norms
    return emb


def compute_root_graph_embedding(k=16, relation="abs1"):
    """Compute spectral embedding for E8 root graph using a relation on inner products.
    relation: 'abs1' -> |dot| == 1, '1' -> dot == 1, '-1' -> dot == -1
    """
    roots = [np.array(r, dtype=float) for r in build_E8_roots()]
    n = len(roots)
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            ip = int(np.dot(roots[i], roots[j]))
            ok = False
            if relation == "abs1":
                ok = abs(ip) == 1
            elif relation == "1":
                ok = ip == 1
            elif relation == "-1":
                ok = ip == -1
            if ok:
                A[i, j] = A[j, i] = 1.0

    vals, vecs = np.linalg.eigh(A)
    idx = np.argsort(vals)[::-1]
    vecs = vecs[:, idx]
    k = min(k, vecs.shape[1])
    emb = vecs[:, :k]
    norms = np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12
    emb = emb / norms
    return emb


def run_graph_embedding_mapping(k=16):
    """Compute embeddings of edge-line graph and root graph, align via anchors and assign.
    Returns mapping, candidate distances and transform used.
    """
    print("Computing line-graph embedding for edges...")
    edge_emb = compute_line_graph_embedding(k=k)
    print("Computing root-graph embedding (abs1 relation) ...")
    root_emb = compute_root_graph_embedding(k=k, relation="abs1")

    # Use anchor correspondences to compute Procrustes on embeddings
    anchors = anchors_from_strategies()
    if len(anchors) < 10:
        print("Not enough anchors for embedding alignment; returning empty")
        return {}, [], None

    # anchor indices
    edge_idx_to_root = {e: tuple(r) for (e, _, r) in anchors}
    anchor_edges = []
    anchor_roots = []
    roots = [tuple(r) for r in build_E8_roots()]
    root_index = {tuple(r): i for i, r in enumerate(roots)}
    for eidx, _, r in anchors:
        anchor_edges.append(eidx)
        anchor_roots.append(root_index[tuple(r)])

    A = edge_emb[np.array(anchor_edges)]
    B = root_emb[np.array(anchor_roots)]

    s_emb, R_emb, t_emb = compute_procrustes(A, B, allow_scale=True)
    print(f"Embedding transform: scale={s_emb:.6f}, det(R)={np.linalg.det(R_emb):.6f}")

    # transform edge embeddings
    edge_emb_t = (edge_emb.dot(R_emb)) * s_emb + t_emb

    # Compute cost matrix in embedding space
    n_edges = edge_emb_t.shape[0]
    n_roots = root_emb.shape[0]
    cost = np.linalg.norm(edge_emb_t[:, None, :] - root_emb[None, :, :], axis=2)

    # Hungarian assignment
    mapping = {}
    try:
        from scipy.optimize import linear_sum_assignment

        row_ind, col_ind = linear_sum_assignment(cost)
        for r, c in zip(row_ind, col_ind):
            mapping[r] = tuple(np.array(build_E8_roots())[c])
        method_used = "hungarian_emb"
    except Exception:
        # greedy fallback on embedding nearest
        candidate_triples = []
        for i in range(n_edges):
            j = int(np.argmin(cost[i]))
            candidate_triples.append(
                (i, tuple(np.array(build_E8_roots())[j]), float(cost[i, j]))
            )
        mapping = greedy_bipartite_match(
            sorted(candidate_triples, key=lambda x: x[2]), n_edges, n_roots
        )
        method_used = "greedy_emb"

    # Stats
    matched = len(mapping)
    out = ARTIFACTS / "edge_root_mapping_embedding.json"
    with out.open("w", encoding="utf-8") as f:
        dump_json({"method": method_used, "matched": matched}, f, indent=2)

    print("Embedding mapping matched:", matched)
    return mapping, cost, (s_emb, R_emb, t_emb)


def run_geometry_mapping(tol=1e-8):
    """Geometric anchor-based Procrustes mapping (original method).
    Returns (mapping, candidate_triples, (s,R,t))
    """
    vertices, edges = build_W33()
    E8_roots = [np.array(r, dtype=float) for r in build_E8_roots()]

    anchors = anchors_from_strategies()
    print(f"Anchors available: {len(anchors)}")
    assert len(anchors) >= 4, "Not enough anchors to compute stable transform"

    A = np.vstack([v for (_, v, _) in anchors])
    B = np.vstack([r for (_, _, r) in anchors])

    s, R, t = compute_procrustes(A, B, allow_scale=True)
    print(f"Computed transform: scale={s:.6f}, det(R)={np.linalg.det(R):.6f}")

    # Generate candidate assignments (and full cost matrix for global assignment)
    candidate_triples = []  # (edge_idx, root_tuple, dist)
    n_edges = len(edges)
    n_roots = len(E8_roots)
    cost = np.full((n_edges, n_roots), fill_value=np.inf)

    for eidx in range(n_edges):
        vec_candidates = all_lift_variants(eidx)
        best = None
        for v in vec_candidates:
            v_trans = s * (v.dot(R)) + t
            arr = np.vstack(E8_roots)
            dists = np.linalg.norm(arr - v_trans.reshape(1, -1), axis=1)
            cost[eidx] = np.minimum(cost[eidx], dists)
            j = int(np.argmin(dists))
            dist = float(dists[j])
            root = tuple(arr[j])
            if best is None or dist < best[0]:
                best = (dist, root, v, v_trans)
        if best is not None:
            candidate_triples.append((eidx, best[1], best[0]))

    candidate_triples.sort(key=lambda x: x[2])

    # Try Hungarian assignment
    mapping = {}
    try:
        from scipy.optimize import linear_sum_assignment

        row_ind, col_ind = linear_sum_assignment(cost)
        for r, c in zip(row_ind, col_ind):
            rr = int(r)
            cc = int(c)
            mapping[rr] = tuple(float(x) for x in E8_roots[cc])
        method_used = "hungarian"
    except Exception:
        mapping = greedy_bipartite_match(candidate_triples, n_edges, n_roots)
        method_used = "greedy"

    # Stats
    matched = len(mapping)
    close_matches = sum(1 for (_, _, d) in candidate_triples if d < tol)

    result = {
        "n_edges": n_edges,
        "n_roots": n_roots,
        "anchors": len(anchors),
        "matched": matched,
        "close_matches": close_matches,
        "assignment_method": method_used,
    }

    outp = ARTIFACTS / "edge_root_mapping_geom.json"
    sample = [[int(k), [float(x) for x in v]] for k, v in list(mapping.items())[:20]]
    with outp.open("w", encoding="utf-8") as f:
        dump_json({"result": result, "sample": sample}, f, indent=2)

    print("Geometric mapping summary:", result)
    return mapping, candidate_triples, (s, R, t)


def run_iterative_refinement(max_iter=10, add_tol=1e-8, tol=1e-6):
    """Iterative EM-style refinement: grow anchors from high-confidence matches and recompute transforms."""
    vertices, edges = build_W33()
    E8_roots = [np.array(r, dtype=float) for r in build_E8_roots()]

    anchors = {e: (v, r) for (e, v, r) in anchors_from_strategies()}
    print(f"Starting anchors: {len(anchors)}")

    prev_best = None
    best_mapping = {}
    best_metrics = None

    for it in range(max_iter):
        # partition anchors
        anchors_list = [(e, v, r) for e, (v, r) in anchors.items()]
        anchors_int = [
            (e, v, r) for (e, v, r) in anchors_list if all(c == int(c) for c in r)
        ]
        anchors_half = [
            (e, v, r) for (e, v, r) in anchors_list if not all(c == int(c) for c in r)
        ]

        transforms = []
        if len(anchors_int) >= 3:
            A = np.vstack([v for (_, v, _) in anchors_int])
            B = np.vstack([r for (_, _, r) in anchors_int])
            s, R, t = compute_procrustes(A, B, allow_scale=True)
            transforms.append(("int", s, R, t))
        if len(anchors_half) >= 3:
            A = np.vstack([v for (_, v, _) in anchors_half])
            B = np.vstack([r for (_, _, r) in anchors_half])
            s, R, t = compute_procrustes(A, B, allow_scale=True)
            transforms.append(("half", s, R, t))
        if not transforms and len(anchors_list) >= 3:
            A = np.vstack([v for (_, v, _) in anchors_list])
            B = np.vstack([r for (_, _, r) in anchors_list])
            s, R, t = compute_procrustes(A, B, allow_scale=True)
            transforms.append(("all", s, R, t))

        # candidate best distances per edge across transforms
        n_edges = len(edges)
        n_roots = len(E8_roots)
        cost = np.full((n_edges, n_roots), fill_value=np.inf)
        best_info = {}
        for eidx in range(n_edges):
            vec_candidates = all_lift_variants(eidx)
            for v in vec_candidates:
                for name, s, R, t in transforms:
                    v_trans = s * (v.dot(R)) + t
                    arr = np.vstack(E8_roots)
                    dists = np.linalg.norm(arr - v_trans.reshape(1, -1), axis=1)
                    cost[eidx] = np.minimum(cost[eidx], dists)
                    j = int(np.argmin(dists))
                    dist = float(dists[j])
                    if (eidx not in best_info) or (dist < best_info[eidx][0]):
                        # store the best candidate distance, root, transform name, and the raw lift vector
                        best_info[eidx] = (
                            dist,
                            tuple(arr[j]),
                            name,
                            np.array(v, dtype=float),
                        )

        # Solve assignment
        try:
            from scipy.optimize import linear_sum_assignment

            row_ind, col_ind = linear_sum_assignment(cost)
            mapping = {
                int(r): tuple(E8_roots[int(c)]) for r, c in zip(row_ind, col_ind)
            }
            method_used = "hungarian"
        except Exception:
            candidate_triples = [
                (e, best_info[e][1], best_info[e][0])
                for e in range(n_edges)
                if e in best_info
            ]
            candidate_triples.sort(key=lambda x: x[2])
            mapping = greedy_bipartite_match(candidate_triples, n_edges, n_roots)
            method_used = "greedy"

        # compute high-confidence matches (dist < add_tol)
        added = 0
        # diagnostic: distance distribution among best_info
        if best_info:
            dists = [v[0] for v in best_info.values()]
            n_below_add = sum(1 for d in dists if d < add_tol)
            n_below_1e3 = sum(1 for d in dists if d < 1e-3)
            n_unanchored_below_add = sum(
                1 for e, v in best_info.items() if (v[0] < add_tol and e not in anchors)
            )
            print(
                f"Iteration {it}: mapped={len(mapping)} best_dist_min={min(dists):.6g} med={np.median(dists):.6g} #<add_tol={n_below_add} #unanchored<add_tol={n_unanchored_below_add} #<1e-3={n_below_1e3}"
            )
        # consider best_info entries (not just current mapping) to find high-confidence matches
        anchored_roots = set(tuple(rr) for (_, rr) in anchors.values())
        unanchored = [
            (e, info[0], info[1], info[3] if len(info) > 3 else None)
            for e, info in best_info.items()
            if e not in anchors
        ]
        # try strict threshold first
        for e, dist, root, lift_vec in sorted(unanchored, key=lambda x: x[1]):
            if dist < add_tol and tuple(root) not in anchored_roots:
                if lift_vec is not None:
                    anchors[e] = (lift_vec, np.array(root, dtype=float))
                    anchored_roots.add(tuple(root))
                    added += 1
        # if nothing added, try a lenient quantile-based addition (top-K if within max_add_dist)
        if added == 0 and unanchored:
            # parameters: add_k=5, max_add_dist=0.1
            add_k = 5
            max_add_dist = 0.1
            for e, dist, root, lift_vec in sorted(unanchored, key=lambda x: x[1])[
                :add_k
            ]:
                if dist < max_add_dist and tuple(root) not in anchored_roots:
                    if lift_vec is not None:
                        anchors[e] = (lift_vec, np.array(root, dtype=float))
                        anchored_roots.add(tuple(root))
                        added += 1
                    else:
                        pass

        print(
            f"Iteration {it}: method={method_used} mapped={len(mapping)} added_anchors={added}"
        )

        # keep best mapping
        if best_metrics is None or len(mapping) > best_metrics:
            best_mapping = mapping
            best_metrics = len(mapping)

        # stop if nothing new added
        if added == 0:
            # fallback: try more lenient add_tol and break
            if add_tol < 1e-1:
                add_tol *= 10
                print(f"No anchors added — increasing add_tol to {add_tol}")
                continue
            print("No anchors could be added; stopping iterative refinement")
            break

    out = ARTIFACTS / "edge_root_mapping_iterative.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(
            {"best_matched": best_metrics, "final_anchors": len(anchors)}, f, indent=2
        )

    print("Iterative best matched:", best_metrics, "final anchors:", len(anchors))
    return best_mapping, anchors, transforms


def local_search_refine_mapping(
    initial_mapping, relation="abs1", iterations=20000, temp=0.01
):
    """Local swap-based refinement to maximize adjacency-preservation score.

    initial_mapping: dict edge_idx -> root_tuple
    relation: root adjacency rule (abs1, 1, -1)
    """
    # Build line-graph adjacency for edges
    vertices, edges = build_W33()
    n_edges = len(edges)
    L_adj = [set() for _ in range(n_edges)]
    for i in range(n_edges):
        u, v = edges[i]
        for j in range(i + 1, n_edges):
            a, b = edges[j]
            if u == a or u == b or v == a or v == b:
                L_adj[i].add(j)
                L_adj[j].add(i)

    # Build root index map and root adjacency
    roots = [tuple(r) for r in build_E8_roots()]
    root_index = {r: i for i, r in enumerate(roots)}
    n_roots = len(roots)
    R_adj = [set() for _ in range(n_roots)]
    for i in range(n_roots):
        ri = np.array(roots[i], dtype=float)
        for j in range(i + 1, n_roots):
            rj = np.array(roots[j], dtype=float)
            ip = int(np.dot(ri, rj))
            ok = False
            if relation == "abs1":
                ok = abs(ip) == 1
            elif relation == "1":
                ok = ip == 1
            elif relation == "-1":
                ok = ip == -1
            if ok:
                R_adj[i].add(j)
                R_adj[j].add(i)

    # Convert initial mapping to arrays of indices
    edge_to_root = {}
    for e, rtuple in initial_mapping.items():
        edge_to_root[e] = root_index[tuple(rtuple)]

    # fill unassigned edges randomly with unused roots
    unused_roots = set(range(n_roots)) - set(edge_to_root.values())
    for e in range(n_edges):
        if e not in edge_to_root:
            if unused_roots:
                edge_to_root[e] = unused_roots.pop()
            else:
                edge_to_root[e] = e % n_roots

    # compute initial score
    def compute_score(mapping):
        score = 0
        for i in range(n_edges):
            ri = mapping[i]
            for j in L_adj[i]:
                if j <= i:
                    continue
                rj = mapping[j]
                if rj in R_adj[ri]:
                    score += 1
        return score

    current_score = compute_score(edge_to_root)
    best_score = current_score
    best_map = edge_to_root.copy()

    import random

    for it in range(iterations):
        # pick two random edges to swap roots
        e1, e2 = random.sample(range(n_edges), 2)
        r1 = edge_to_root[e1]
        r2 = edge_to_root[e2]

        # compute delta score efficiently by looking at neighbors
        def local_contrib(e, mapping):
            ri = mapping[e]
            s = 0
            for j in L_adj[e]:
                if j == e:
                    continue
                rj = mapping[j]
                if rj in R_adj[ri]:
                    s += 1
            return s

        before = local_contrib(e1, edge_to_root) + local_contrib(e2, edge_to_root)
        # perform swap
        edge_to_root[e1], edge_to_root[e2] = r2, r1
        after = local_contrib(e1, edge_to_root) + local_contrib(e2, edge_to_root)
        delta = after - before
        accept = False
        if delta >= 0:
            accept = True
        else:
            # Metropolis criterion
            if random.random() < math.exp(delta / (temp + 1e-12)):
                accept = True
        if not accept:
            # revert
            edge_to_root[e1], edge_to_root[e2] = r1, r2
        else:
            current_score += delta
            if current_score > best_score:
                best_score = current_score
                best_map = edge_to_root.copy()

    print(
        f"Local search best score: {best_score} (initial {compute_score(edge_to_root)})"
    )
    # Convert best_map back to edge->root tuples
    final_mapping = {e: tuple(roots[idx]) for e, idx in best_map.items()}
    return final_mapping, best_score


# ---- New: feature-driven mapping helpers & CP-SAT local-hotspot optimizer ----


def compute_adjacency_score(mapping, relation="abs1"):
    """Compute adjacency-preservation score (number of preserved adjacent pairs)."""
    vertices, edges = build_W33()
    n_edges = len(edges)
    # Build line-graph adjacency
    L_adj = [set() for _ in range(n_edges)]
    for i in range(n_edges):
        u, v = edges[i]
        for j in range(i + 1, n_edges):
            a, b = edges[j]
            if u == a or u == b or v == a or v == b:
                L_adj[i].add(j)
                L_adj[j].add(i)

    roots = [tuple(r) for r in build_E8_roots()]
    root_index = {r: i for i, r in enumerate(roots)}
    n_roots = len(roots)
    R_adj = [set() for _ in range(n_roots)]
    for i in range(n_roots):
        ri = np.array(roots[i], dtype=float)
        for j in range(i + 1, n_roots):
            rj = np.array(roots[j], dtype=float)
            ip = int(np.dot(ri, rj))
            ok = False
            if relation == "abs1":
                ok = abs(ip) == 1
            elif relation == "1":
                ok = ip == 1
            elif relation == "-1":
                ok = ip == -1
            if ok:
                R_adj[i].add(j)
                R_adj[j].add(i)

    # convert mapping to root indices, filling missing edges with unused roots
    map_idx = {}
    assigned = set()
    for e, r in mapping.items():
        try:
            map_idx[int(e)] = root_index[tuple(r)]
            assigned.add(map_idx[int(e)])
        except Exception:
            # skip malformed entries
            pass

    unused_roots = set(range(n_roots)) - assigned
    for e in range(n_edges):
        if e not in map_idx:
            if unused_roots:
                map_idx[e] = unused_roots.pop()
            else:
                map_idx[e] = e % n_roots

    score = 0
    for i in range(n_edges):
        ri = map_idx[i]
        for j in L_adj[i]:
            if j <= i:
                continue
            rj = map_idx[j]
            if rj in R_adj[ri]:
                score += 1
    return score


def compute_edge_orbit_ids(cache_path=None, force=False):
    """Compute (and cache) edge orbit ids under Aut(W33).

    Returns (edge_to_orbit list, orbit_size dict)
    """
    if cache_path is None:
        cache_path = ARTIFACTS / "w33_edge_orbits.json"
    if cache_path.exists() and not force:
        try:
            j = json.loads(cache_path.read_text(encoding="utf-8"))
            edge_to_orbit = [
                int(j["edge_to_orbit"][str(i)]) for i in range(len(j["edge_to_orbit"]))
            ]
            orbit_sizes = {int(k): int(v) for k, v in j.get("orbit_sizes", {}).items()}
            return edge_to_orbit, orbit_sizes
        except Exception:
            pass

    # enumerate group and compute orbits (may be slow; results cached)
    import tools.analyze_balanced_orbit_stabilizer as bal

    pts, adj, edges = bal.build_w33()
    gens = bal.get_generators(pts)
    G = bal.enumerate_group(gens)

    edge_index = {edges[i]: i for i in range(len(edges))}
    # allow reversed tuple mapping
    for i, (u, v) in enumerate(edges):
        if (v, u) not in edge_index:
            edge_index[(v, u)] = i

    n_edges = len(edges)
    edge_orbit_id = [-1] * n_edges
    next_orbit = 0
    for e in range(n_edges):
        if edge_orbit_id[e] != -1:
            continue
        orb = set()
        u, v = edges[e]
        for p in G:
            u2 = p[u]
            v2 = p[v]
            idx = edge_index.get((u2, v2))
            if idx is None:
                idx = edge_index.get((v2, u2))
            if idx is None:
                continue
            orb.add(idx)
        for idx in orb:
            edge_orbit_id[idx] = next_orbit
        next_orbit += 1

    # compute sizes
    from collections import Counter

    counts = Counter(edge_orbit_id)
    orbit_sizes = {int(k): int(v) for k, v in counts.items()}

    # cache
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        json.dump(
            {
                "edge_to_orbit": {
                    str(i): int(edge_orbit_id[i]) for i in range(len(edge_orbit_id))
                },
                "orbit_sizes": {str(k): int(v) for k, v in orbit_sizes.items()},
            },
            cache_path.open("w", encoding="utf-8"),
            indent=2,
        )
    except Exception:
        pass

    return edge_orbit_id, orbit_sizes


def compute_feature_vectors(k=16, use_orbit_features=False):
    """Compute feature vectors for edges and roots.

    Returns (edge_feats, root_feats, meta) where meta includes L_adj and other helpers.
    """
    vertices, edges = build_W33()
    n_edges = len(edges)
    roots = [np.array(r, dtype=float) for r in build_E8_roots()]
    n_roots = len(roots)

    # line/root embeddings
    edge_emb = compute_line_graph_embedding(k=k)
    root_emb = compute_root_graph_embedding(k=k, relation="abs1")

    # adjacency structures
    L_adj = [set() for _ in range(n_edges)]
    for i in range(n_edges):
        u, v = edges[i]
        for j in range(i + 1, n_edges):
            a, b = edges[j]
            if u == a or u == b or v == a or v == b:
                L_adj[i].add(j)
                L_adj[j].add(i)

    R_adj = [set() for _ in range(n_roots)]
    for i in range(n_roots):
        ri = roots[i]
        for j in range(i + 1, n_roots):
            rj = roots[j]
            ip = int(np.dot(ri, rj))
            if abs(ip) == 1:
                R_adj[i].add(j)
                R_adj[j].add(i)

    # compute anchor-based geometric transform
    anchors = anchors_from_strategies()
    if len(anchors) >= 3:
        A = np.vstack([v for (_, v, _) in anchors])
        B = np.vstack([r for (_, _, r) in anchors])
        s, R, t = compute_procrustes(A, B, allow_scale=True)
    else:
        s = 1.0
        R = np.eye(8)
        t = np.zeros(8)

    # per-edge best geometric distance to any E8 root (under transform)
    arr_roots = np.vstack(roots)
    best_geo_dist = np.full(n_edges, np.inf, dtype=float)
    lift_norm = np.zeros(n_edges, dtype=float)
    for eidx in range(n_edges):
        vec_candidates = all_lift_variants(eidx)
        best = np.inf
        best_norm = 0.0
        for v in vec_candidates:
            try:
                v = np.array(v, dtype=float)
                v_trans = s * (v.dot(R)) + t
                dists = np.linalg.norm(arr_roots - v_trans.reshape(1, -1), axis=1)
                md = float(np.min(dists))
                if md < best:
                    best = md
                    best_norm = float(np.linalg.norm(v))
            except Exception:
                pass
        if np.isfinite(best):
            best_geo_dist[eidx] = best
            lift_norm[eidx] = best_norm
        else:
            best_geo_dist[eidx] = 1e6
            lift_norm[eidx] = 0.0

    # compute triangle counts per edge (number of triangles in line graph involving edge)
    tri_count = np.zeros(n_edges, dtype=int)
    for i in range(n_edges):
        cnt = 0
        neigh = list(L_adj[i])
        sset = set(neigh)
        for a_i in range(len(neigh)):
            for b_i in range(a_i + 1, len(neigh)):
                if neigh[b_i] in L_adj[neigh[a_i]]:
                    cnt += 1
        tri_count[i] = cnt

    # build feature arrays
    base_edge_feats = [
        edge_emb,
        tri_count.reshape(-1, 1).astype(float),
        best_geo_dist.reshape(-1, 1),
        lift_norm.reshape(-1, 1),
        np.array([len(L_adj[i]) for i in range(n_edges)], dtype=float).reshape(-1, 1),
    ]
    # optional orbit-based feature (cached)
    # use_orbit_features must be passed into this function to enable
    try:
        use_orbit = bool(use_orbit_features)
    except NameError:
        use_orbit = False
    if use_orbit:
        edge_orbit_id, orbit_sizes = compute_edge_orbit_ids()
        orbit_size_arr = np.array(
            [orbit_sizes.get(int(edge_orbit_id[i]), 1) for i in range(n_edges)],
            dtype=float,
        ).reshape(-1, 1)
        base_edge_feats.append(orbit_size_arr)

    edge_feats = np.hstack(base_edge_feats)

    is_integer_root = np.array(
        [all(c == int(c) for c in r) for r in arr_roots], dtype=float
    )
    # D4 membership (first 4 coords or last 4 coords nonzero only)
    in_d4_first = np.array(
        [all(r[4 + i] == 0 for i in range(4)) for r in arr_roots], dtype=float
    )
    in_d4_last = np.array(
        [all(r[i] == 0 for i in range(4)) for r in arr_roots], dtype=float
    )
    root_feats = np.hstack(
        [
            root_emb,
            np.array([len(R_adj[i]) for i in range(n_roots)], dtype=float).reshape(
                -1, 1
            ),
            is_integer_root.reshape(-1, 1),
            in_d4_first.reshape(-1, 1),
            in_d4_last.reshape(-1, 1),
        ]
    )

    meta = {
        "L_adj": L_adj,
        "R_adj": R_adj,
        "best_geo_dist": best_geo_dist,
        "lift_norm": lift_norm,
        "edge_emb": edge_emb,
        "root_emb": root_emb,
        "anchors": anchors,
    }
    return edge_feats, root_feats, meta


def build_score_matrix(edge_feats, root_feats, meta, weights=None):
    """Build a composite score matrix (higher = better match) from features."""
    if weights is None:
        weights = {"emb": 0.6, "geom": 0.3, "meta": 0.1}

    edge_emb = meta["edge_emb"]
    root_emb = meta["root_emb"]
    # normalize embeddings already unit-norm in embedding functions; use dot product -> [-1,1]
    emb_sim = (edge_emb.dot(root_emb.T) + 1.0) / 2.0  # map to [0,1]

    # geometry score from distances
    best_geo = meta["best_geo_dist"].reshape(-1, 1)
    geom_score = 1.0 / (1.0 + best_geo)  # in (0,1]

    # broadcast root constants for deg matches
    n_edges = edge_feats.shape[0]
    n_roots = root_feats.shape[0]

    edge_deg = edge_feats[:, -1].reshape(-1, 1)
    root_deg = root_feats[:, -4].reshape(1, -1)  # degree stored at column -4
    max_deg = max(edge_deg.max(), root_deg.max(), 1.0)
    deg_sim = 1.0 - (np.abs(edge_deg - root_deg) / float(max_deg))

    # integer/half-int match
    root_is_int = root_feats[:, -3].reshape(1, -1)
    # for edges, approximate integer-likeness by nearest integer check on lift_norm (small integer norms less likely?)
    # but better to set to 0.5 neutral; keep it simple: no edge integer flag -> ignore
    int_sim = np.where(root_is_int == 1.0, 1.0, 0.0)

    meta_sim = deg_sim * 0.7 + int_sim * 0.3

    # final composite score
    score = (
        weights["emb"] * emb_sim
        + weights["geom"] * geom_score
        + weights["meta"] * meta_sim
    )
    # clip and normalize to [0,1]
    score = np.clip(score, 0.0, 1.0)
    return score


def run_feature_hungarian_mapping(
    weights=None, write_artifact=True, use_orbit_features=False
):
    """Compute feature-driven score matrix and run Hungarian assignment.

    Returns mapping dict edge->root_tuple and stats.
    """
    edge_feats, root_feats, meta = compute_feature_vectors(
        k=16, use_orbit_features=use_orbit_features
    )
    score = build_score_matrix(edge_feats, root_feats, meta, weights=weights)

    try:
        from scipy.optimize import linear_sum_assignment

        # convert to cost (minimize)
        max_s = float(np.max(score))
        cost = max_s - score
        row_ind, col_ind = linear_sum_assignment(cost)
        mapping = {
            int(r): tuple(np.array(build_E8_roots())[int(c)])
            for r, c in zip(row_ind, col_ind)
        }
        method_used = "hungarian_feature"
    except Exception:
        # greedy fallback: include top-k candidate roots per edge so we can cover all edges
        candidate_triples = []
        n_edges = score.shape[0]
        n_roots = score.shape[1]
        top_k = min(50, n_roots)
        roots_arr = np.array(build_E8_roots())
        for i in range(n_edges):
            idxs = np.argsort(-score[i])[:top_k]
            for j in idxs:
                candidate_triples.append(
                    (i, tuple(roots_arr[int(j)]), float(-score[i, int(j)]))
                )
        candidate_triples.sort(key=lambda x: x[2])
        mapping = greedy_bipartite_match(candidate_triples, n_edges, n_roots)
        # fill any unassigned edges with unused roots to produce a complete bijection
        if len(mapping) < n_edges:
            all_roots = [tuple(r) for r in build_E8_roots()]
            used = set(mapping.values())
            unused = [r for r in all_roots if r not in used]
            unassigned_edges = [e for e in range(n_edges) if e not in mapping]
            for e, r in zip(unassigned_edges, unused):
                mapping[e] = r
        method_used = "greedy_feature"
    n_edges = score.shape[0]
    # final safety: ensure mapping complete by filling any leftover edges with unused roots
    if len(mapping) < n_edges:
        all_roots = [tuple(r) for r in build_E8_roots()]
        used = set(mapping.values())
        unused = [r for r in all_roots if r not in used]
        unassigned_edges = [e for e in range(n_edges) if e not in mapping]
        for e, r in zip(unassigned_edges, unused):
            mapping[e] = r

    # compute adjacency score
    adj_score = compute_adjacency_score(mapping, relation="abs1")

    result = {
        "method": method_used,
        "adj_score": int(adj_score),
    }

    if write_artifact:
        out = ARTIFACTS / "edge_root_mapping_feature.json"
        with out.open("w", encoding="utf-8") as f:
            dump_json(
                {"result": result, "sample": list(mapping.items())[:50]}, f, indent=2
            )

    print("Feature mapping adj_score:", adj_score, "method:", method_used)
    return mapping, result, score, meta


def detect_hotspots(mapping, meta, top_k=20, max_cluster=16):
    """Detect clusters of edges that are hotspots for local refinement.

    Heuristic: pick edges with lowest local adjacency-preservation and return the
    connected component up to max_cluster in the line graph.
    """
    L_adj = meta["L_adj"]
    # compute per-edge preserved adjacency count
    roots = [tuple(r) for r in build_E8_roots()]
    root_index = {r: i for i, r in enumerate(roots)}
    R_adj = meta["R_adj"]

    # convert mapping to root idx
    map_idx = {e: root_index[tuple(r)] for e, r in mapping.items()}

    preserved = np.zeros(len(L_adj), dtype=int)
    for i in range(len(L_adj)):
        ri = map_idx[i]
        for j in L_adj[i]:
            if j <= i:
                continue
            rj = map_idx[j]
            if rj in R_adj[ri]:
                preserved[i] += 1
                preserved[j] += 1

    # lower preserved -> candidate
    worst = np.argsort(preserved)[: top_k * 2]
    # build induced subgraph on worst and pick largest connected component under L_adj
    worst_set = set(int(x) for x in worst)
    comps = []
    seen = set()
    for v in worst:
        if v in seen:
            continue
        stack = [int(v)]
        comp = []
        while stack and len(comp) < max_cluster:
            u = stack.pop()
            if u in seen or u not in worst_set:
                continue
            seen.add(u)
            comp.append(u)
            for w in L_adj[u]:
                if w not in seen and w in worst_set:
                    stack.append(w)
        if comp:
            comps.append(comp)
    if not comps:
        return []
    # return largest comp limited to max_cluster
    largest = max(comps, key=len)
    return largest[:max_cluster]


def cp_sat_local_refine(mapping_init, cluster_edges, top_k=8, time_limit=10):
    """Refine mapping on a small cluster with OR-Tools CP-SAT maximizing local adjacency.

    Returns updated mapping for cluster and local adj score.
    """
    try:
        from ortools.sat.python import cp_model
    except Exception:
        print("OR-Tools not available; skipping CP-SAT local refine")
        return mapping_init, 0

    if not cluster_edges:
        return mapping_init, 0

    roots = [tuple(r) for r in build_E8_roots()]
    root_index = {r: i for i, r in enumerate(roots)}
    n_roots = len(roots)

    # candidate roots per edge: top_k nearest by feature score
    # reuse feature score by running run_feature_hungarian_mapping to get score & meta
    _, _, score_matrix, meta = run_feature_hungarian_mapping(write_artifact=False)

    # for each edge in cluster, pick top_k roots
    candid_roots = []
    for e in cluster_edges:
        top_idxs = np.argsort(-score_matrix[e])[:top_k]
        candid_roots.append(list(map(int, top_idxs)))

    # build map from root index to local index
    pool = sorted({r for sub in candid_roots for r in sub})
    pool_index = {r: i for i, r in enumerate(pool)}

    model = cp_model.CpModel()
    x = {}
    for i_e, e in enumerate(cluster_edges):
        for r in candid_roots[i_e]:
            x[(i_e, r)] = model.NewBoolVar(f"x_e{e}_r{r}")
        # assign exactly one root per edge
        model.Add(sum(x[(i_e, r)] for r in candid_roots[i_e]) == 1)

    # each root used at most once across cluster
    for r in pool:
        model.Add(
            sum(x[(i_e, r)] for i_e in range(len(cluster_edges)) if (i_e, r) in x) <= 1
        )

    # adjacency objective: for every adjacent pair in cluster, reward if assigned roots are adjacent in root graph
    L_adj = meta["L_adj"]
    R_adj = meta["R_adj"]
    pairs = []
    for i in range(len(cluster_edges)):
        for j in L_adj[cluster_edges[i]]:
            if j <= cluster_edges[i]:
                continue
            if j in cluster_edges:
                j_idx = cluster_edges.index(j)
                if j_idx <= i:
                    continue
                pairs.append((i, j_idx, cluster_edges[i], j))

    # linearize pair products with auxiliary y vars
    y_vars = []
    for i, j_idx, ei, ej in pairs:
        for ri in candid_roots[i]:
            for rj in candid_roots[j_idx]:
                v = model.NewBoolVar(f"y_e{ei}_r{ri}_e{ej}_r{rj}")
                model.AddBoolAnd([x[(i, ri)], x[(j_idx, rj)]]).OnlyEnforceIf(v)
                # enforce v -> both x true
                model.Add(x[(i, ri)] + x[(j_idx, rj)] - 1 >= v)
                y_vars.append((v, ri, rj))

    # objective: maximize sum of y * adj_root_indicator
    terms = []
    for v, ri, rj in y_vars:
        adj_val = 1 if (int(rj) in R_adj[int(ri)]) else 0
        if adj_val:
            terms.append(v)
    if not terms:
        # nothing to do
        return mapping_init, compute_adjacency_score(mapping_init)

    model.Maximize(sum(terms))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(time_limit)
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("CP-SAT found no feasible improvement")
        return mapping_init, compute_adjacency_score(mapping_init)

    # build updated mapping
    updated = dict(mapping_init)
    for i_e, e in enumerate(cluster_edges):
        for r in candid_roots[i_e]:
            if solver.Value(x[(i_e, r)]) == 1:
                updated[e] = tuple(np.array(build_E8_roots())[int(r)])
                break

    local_score = compute_adjacency_score({e: updated[e] for e in cluster_edges})
    return updated, local_score


# Simple plotting helpers


def plot_feature_embeddings(mapping, score_matrix, meta, out_dir=ARTIFACTS / "figures"):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib not available; skipping plotting")
        return None

    out_dir.mkdir(parents=True, exist_ok=True)
    edge_emb = meta["edge_emb"]
    root_emb = meta["root_emb"]
    # project embeddings to 2D via SVD
    X = np.vstack([edge_emb, root_emb])
    U, S, Vt = np.linalg.svd(X - X.mean(axis=0), full_matrices=False)
    coords = (X - X.mean(axis=0)).dot(Vt.T)[:, :2]
    e_coords = coords[: edge_emb.shape[0]]
    r_coords = coords[edge_emb.shape[0] :]

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(e_coords[:, 0], e_coords[:, 1], c="C0", s=10, label="edges", alpha=0.6)
    ax.scatter(r_coords[:, 0], r_coords[:, 1], c="C1", s=5, label="roots", alpha=0.6)
    ax.set_title("Edge vs Root Embeddings (2D PCA)")
    ax.legend()
    out = out_dir / "feature_embeddings.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_adj_preservation(mapping, meta, out_dir=ARTIFACTS / "figures"):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib not available; skipping plotting")
        return None

    out_dir.mkdir(parents=True, exist_ok=True)
    L_adj = meta["L_adj"]
    roots = [tuple(r) for r in build_E8_roots()]
    root_index = {r: i for i, r in enumerate(roots)}
    R_adj = meta["R_adj"]

    # ensure mapping covers all edges
    n = len(L_adj)
    map_idx = {}
    assigned = set()
    for e, r in mapping.items():
        try:
            map_idx[int(e)] = root_index[tuple(r)]
            assigned.add(map_idx[int(e)])
        except Exception:
            pass
    unused = [i for i in range(len(roots)) if i not in assigned]
    for e in range(n):
        if e not in map_idx:
            map_idx[e] = unused.pop() if unused else e % len(roots)

    M = np.zeros((n, n), dtype=int)
    for i in range(n):
        ri = map_idx[i]
        for j in L_adj[i]:
            rj = map_idx[j]
            if rj in R_adj[ri]:
                M[i, j] = 1

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(M, cmap="Greens", interpolation="nearest")
    ax.set_title("Adjacency-preservation heatmap (edges x edges)")
    out = out_dir / "adj_preservation_heatmap.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


# ---- end new helpers ----


def run_mapping(tol=1e-8):
    """Run the three mapping strategies and summarize results."""
    mapping_geom, candidate_triples, geom_transform = run_geometry_mapping(tol=tol)
    mapping_emb, cost_emb, emb_transform = run_graph_embedding_mapping(k=16)
    mapping_iter, final_anchors, transforms_iter = run_iterative_refinement()

    # Write a summary
    out = ARTIFACTS / "edge_root_mapping_summary.json"
    summary = {
        "geom_matched": len(mapping_geom) if mapping_geom else 0,
        "embedding_matched": len(mapping_emb) if mapping_emb else 0,
        "iterated_matched": len(mapping_iter) if mapping_iter else 0,
    }
    with out.open("w", encoding="utf-8") as f:
        dump_json(summary, f, indent=2)

    print("Final summary:", summary)
    return (
        mapping_geom,
        mapping_emb,
        mapping_iter,
        (geom_transform, emb_transform, transforms_iter),
    )


if __name__ == "__main__":
    run_mapping()
