#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def canon(v):
    vv = [x % 3 for x in v]
    first = next(x for x in vv if x)
    if first == 2:
        vv = [(2 * x) % 3 for x in vv]
    return tuple(vv)


def symp(a, b):
    return (a[0]*b[2] + a[1]*b[3] - a[2]*b[0] - a[3]*b[1]) % 3


def w33_adjacency():
    pts = []
    seen = set()
    for v in itertools.product(range(3), repeat=4):
        if v == (0, 0, 0, 0):
            continue
        c = canon(v)
        if c not in seen:
            seen.add(c)
            pts.append(c)
    n = len(pts)
    adj = np.zeros((n, n), dtype=int)
    for i, a in enumerate(pts):
        for j, b in enumerate(pts):
            if i < j and symp(a, b) == 0:
                adj[i, j] = adj[j, i] = 1
    return adj


def hashimoto(adj: np.ndarray):
    n = adj.shape[0]
    directed = [(i, j) for i in range(n) for j in range(n) if adj[i, j]]
    idx = {e: i for i, e in enumerate(directed)}
    b = np.zeros((len(directed), len(directed)), dtype=int)
    for a, (u, v) in enumerate(directed):
        for w in range(n):
            if adj[v, w] and w != u:
                b[a, idx[(v, w)]] = 1
    return b, directed


def phase_summary(vals):
    angles = []
    for z in vals:
        if abs(abs(z) - math.sqrt(11)) < 1e-6:
            ang = math.degrees(math.atan2(float(z.imag), float(z.real))) % 360.0
            if ang > 180:
                ang = 360 - ang
            angles.append(round(ang, 6))
    clusters = {}
    for a in angles:
        key = round(a, 3)
        clusters[str(key)] = clusters.get(str(key), 0) + 1
    return clusters


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1345_hashimoto_matrix_falsifier.json")
    ns = ap.parse_args()
    adj = w33_adjacency()
    b, directed = hashimoto(adj)
    evals_adj = np.linalg.eigvalsh(adj)
    evals_b = np.linalg.eigvals(b)
    phase_clusters = phase_summary(evals_b)
    exact_from_adjacency = {
        "r_2_phase_deg": math.degrees(math.atan2(math.sqrt(10), 1.0)),
        "s_minus4_phase_deg": 180.0 - math.degrees(math.atan2(math.sqrt(7), 2.0)),
    }
    protocol_targets = {"gauge_deg": 63.43494882292201, "chiral_deg": 112.20765429859648}
    checks = {
        "srg_degree_12": bool(np.all(adj.sum(axis=1) == 12)),
        "edge_count_240": int(adj.sum() // 2) == 240,
        "directed_edges_480": len(directed) == 480,
        "adjacency_spectrum_12_2_minus4": sorted(set(round(float(x), 6) for x in evals_adj)) == [-4.0, 2.0, 12.0],
        "hashimoto_phase_clusters_present": "72.452" in phase_clusters and "127.087" in phase_clusters,
    }
    protocol_match = {
        "gauge_target_matches_matrix": abs(protocol_targets["gauge_deg"] - exact_from_adjacency["r_2_phase_deg"]) <= 0.5,
        "chiral_target_matches_matrix": abs(protocol_targets["chiral_deg"] - exact_from_adjacency["s_minus4_phase_deg"]) <= 0.5,
    }
    result = {
        "bt": 1345,
        "title": "Matrix-derived Hashimoto falsifier",
        "verified": all(checks.values()),
        "checks": checks,
        "protocol_targets_match_standard_hashimoto": all(protocol_match.values()),
        "protocol_match_checks": protocol_match,
        "graph": {"v": int(adj.shape[0]), "edges": int(adj.sum() // 2), "directed_edges": len(directed)},
        "adjacency_eigenvalue_set": sorted(set(round(float(x), 6) for x in evals_adj)),
        "hashimoto_phase_clusters_deg": phase_clusters,
        "matrix_derived_phases_deg": exact_from_adjacency,
        "protocol_target_phases_deg": protocol_targets,
        "interpretation": "The standard non-backtracking Hashimoto matrix on W(3,3) gives phase clusters near 72.45 and 127.09 degrees, not the synthetic protocol targets 63.43 and 112.21 degrees. The protocol angles need a corrected operator definition or must be relabeled as nonstandard phase observables."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1345, "verified": result["verified"], "protocol_targets_match_standard_hashimoto": result["protocol_targets_match_standard_hashimoto"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
