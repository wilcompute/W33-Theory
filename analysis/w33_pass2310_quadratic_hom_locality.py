#!/usr/bin/env python3
"""Pass 2310: geometric locality census of the fifty complete quadratic Hom seeds.

Pass 2301 proves completeness and surjectivity of the signed-orbit basis.  This
pass asks a different question: what local W33 edge motifs seed those maps?
The classification is performed on the literal deterministic 240-edge indexing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from pathlib import Path

from w33_pass1060_1064_core import build_w33
from w33_pass2301_complete_quadratic_hom_bases import REPS

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass2301_complete_quadratic_hom_bases.json"


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def line_graph_distances(edges):
    incident = [[] for _ in range(40)]
    for i, (a, b) in enumerate(edges):
        incident[a].append(i)
        incident[b].append(i)
    adj = [set() for _ in edges]
    for block in incident:
        for i in block:
            adj[i].update(block)
            adj[i].discard(i)
    D = []
    for source in range(len(edges)):
        d = [-1] * len(edges)
        d[source] = 0
        q = deque([source])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if d[v] < 0:
                    d[v] = d[u] + 1
                    q.append(v)
        assert min(d) == 0 and max(d) >= 1
        D.append(d)
    return D


def same_gq_line(e, f, adj):
    a, b = e
    c, d = f
    shared = set(e) & set(f)
    if len(shared) != 1:
        return False
    x = next(iter(shared))
    y = b if a == x else a
    z = d if c == x else c
    return bool(adj[y, z])


def motif(rep, kind, target, edges, adj, D):
    o, i, j = rep
    idx = [o, i, j]
    es = [edges[z] for z in idx]
    vertices = sorted(set().union(*map(set, es)))
    degrees = Counter()
    for a, b in es:
        degrees[a] += 1
        degrees[b] += 1
    pair_d = [D[o][i], D[o][j], D[i][j]]
    pair_shared = [len(set(es[0]) & set(es[1])), len(set(es[0]) & set(es[2])), len(set(es[1]) & set(es[2]))]
    pair_same_line = [same_gq_line(es[0], es[1], adj), same_gq_line(es[0], es[2], adj), same_gq_line(es[1], es[2], adj)]
    shape = {
        "source_equal": i == j,
        "distinct_edge_count": len(set(idx)),
        "union_vertex_count": len(vertices),
        "union_degree_multiset": sorted(degrees.values(), reverse=True),
        "line_graph_distances_target_i_target_j_i_j": pair_d,
        "shared_endpoint_counts": pair_shared,
        "same_isotropic_line_flags": pair_same_line,
        "target_radius": max(D[o][i], D[o][j]),
    }
    shape_key = json.dumps(shape, sort_keys=True, separators=(",", ":"))
    return {
        "kind": kind,
        "target": int(target),
        "representative": list(rep),
        "edges": [list(e) for e in es],
        "shape": shape,
        "shape_sha256": hashlib.sha256(shape_key.encode()).hexdigest(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-json", type=Path)
    args = ap.parse_args()

    frozen = json.loads(CERT.read_text())
    w = build_w33()
    edges = [(a, b) for a in range(40) for b in range(a + 1, 40) if w.adj[a, b]]
    assert len(edges) == 240
    D = line_graph_distances(edges)

    rows = []
    for kind in ("Sym", "Lambda"):
        for target, reps in REPS[kind].items():
            meta = frozen["compressed_orbit_bases"][kind][target]
            assert len(meta) == len(reps)
            for rep, orbit_meta in zip(reps, meta):
                row = motif(rep, kind, target, edges, w.adj, D)
                row.update(orbit_meta)
                rows.append(row)
    assert len(rows) == 50

    motif_counts = Counter(r["shape_sha256"] for r in rows)
    radius_counts = Counter(r["shape"]["target_radius"] for r in rows)
    stabilizer_counts = Counter(r["stabilizer_order"] for r in rows)
    special = [r for r in rows if r["stabilizer_order"] > 1]
    source_diagonal = [r for r in rows if r["shape"]["source_equal"]]

    out = {
        "schema": "w33.pass2310.quadratic_hom_locality.v1",
        "status": "PASS_COMPLETE_SEED_MOTIF_CENSUS",
        "basis_maps": 50,
        "symmetric_maps": 26,
        "alternating_maps": 24,
        "unique_seed_motifs": len(motif_counts),
        "motif_multiplicities": dict(sorted(motif_counts.items())),
        "target_radius_histogram": {str(k): v for k, v in sorted(radius_counts.items())},
        "stabilizer_order_histogram": {str(k): v for k, v in sorted(stabilizer_counts.items())},
        "nonfree_seed_orbits": special,
        "source_diagonal_seed_count": len(source_diagonal),
        "source_diagonal_seeds": source_diagonal,
        "rows": rows,
        "checks": {
            "literal_240_edge_indexing": len(edges) == 240,
            "all_50_basis_seeds_classified": len(rows) == 50,
            "dimension_split_26_24": sum(r["kind"] == "Sym" for r in rows) == 26 and sum(r["kind"] == "Lambda" for r in rows) == 24,
            "only_recorded_orbit_stabilizers_used": all(25920 // r["orbit_size"] == r["stabilizer_order"] for r in rows),
        },
        "theorem": "The complete fifty-dimensional quadratic Hom space admits a literal W33 edge-motif census. This classifies seed locality and exceptional stabilizers without changing the representation-theoretic completeness theorem.",
        "boundary": "A short orbit seed is geometrically more symmetric, not automatically more physical or more local in hardware cost. Tensor rank of the fully expanded orbit map is not inferred from one seed triple.",
    }
    out["sha256_without_hash_field"] = digest(out)
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
