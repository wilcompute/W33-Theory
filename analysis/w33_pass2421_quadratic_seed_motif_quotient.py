#!/usr/bin/env python3
"""Pass 2421: quotient the 24 quadratic orbit programs by W33 edge geometry.

Pass 2310 proved that fifty complete quadratic Hom maps reuse twenty-four
signed-orbit programs.  Here target labels are forgotten and the two source
slots are canonicalized under interchange.  The resulting literal W33
three-edge supports fall into six geometric motifs.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, deque
from pathlib import Path

from w33_pass1060_1064_core import build_w33

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "w33_pass2310_quadratic_hom_orbit_seed_compression.json"
OUT = ROOT / "data" / "w33_pass2421_quadratic_seed_motif_quotient.json"
EXPECTED = "TO_BE_FROZEN"


def digest(d):
    x = dict(d)
    x.pop("sha256_without_hash_field", None)
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build_line_graph_distances(edges):
    incident = [[] for _ in range(40)]
    for i, (a, b) in enumerate(edges):
        incident[a].append(i)
        incident[b].append(i)
    adj = [set() for _ in edges]
    for block in incident:
        for i in block:
            adj[i].update(block)
            adj[i].discard(i)
    distances = []
    for source in range(len(edges)):
        row = [-1] * len(edges)
        row[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if row[v] < 0:
                    row[v] = row[u] + 1
                    queue.append(v)
        distances.append(row)
    return distances


def same_isotropic_line(e, f, point_adj):
    shared = set(e) & set(f)
    if len(shared) != 1:
        return False
    x = next(iter(shared))
    y = e[1] if e[0] == x else e[0]
    z = f[1] if f[0] == x else f[0]
    return bool(point_adj[y, z])


def descriptor(rep, edges, point_adj, distances):
    target, left, right = map(int, rep)
    es = [edges[target], edges[left], edges[right]]
    degrees = Counter(v for e in es for v in e)
    d_tl, d_tr, d_lr = distances[target][left], distances[target][right], distances[left][right]
    s_tl, s_tr, s_lr = len(set(es[0]) & set(es[1])), len(set(es[0]) & set(es[2])), len(set(es[1]) & set(es[2]))
    l_tl = same_isotropic_line(es[0], es[1], point_adj)
    l_tr = same_isotropic_line(es[0], es[2], point_adj)
    l_lr = same_isotropic_line(es[1], es[2], point_adj)
    target_source = sorted([(d_tl, s_tl, l_tl), (d_tr, s_tr, l_tr)])
    return {
        "distinct_edge_count": len({target, left, right}),
        "union_vertex_count": len(set().union(*map(set, es))),
        "union_degree_multiset": sorted(degrees.values(), reverse=True),
        "target_source_features": [list(x) for x in target_source],
        "source_source_feature": [d_lr, s_lr, l_lr],
        "target_radius": max(d_tl, d_tr),
    }, [list(e) for e in es]


def build():
    src = json.loads(SRC.read_text())
    assert src["sha256_without_hash_field"] == "2bb3b09a06e4d030a5737553518e6c019519e42ba0024494313e6214f0405686"
    w = build_w33()
    edges = [(a, b) for a in range(40) for b in range(a + 1, 40) if w.adj[a, b]]
    assert len(edges) == 240
    distances = build_line_graph_distances(edges)

    seeds = []
    motifs = {}
    for row in src["seed_table"]:
        desc, literal_edges = descriptor(row["representative"], edges, w.adj, distances)
        key = hashlib.sha256(json.dumps(desc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        seed = {
            "symmetry": row["symmetry"],
            "representative": row["representative"],
            "literal_edges": literal_edges,
            "reuse_count": row["reuse_count"],
            "targets": row["targets"],
            "orbit_size": row["orbit_size"],
            "stabilizer_order": row["stabilizer_order"],
            "motif_sha256": key,
        }
        seeds.append(seed)
        m = motifs.setdefault(key, {"descriptor": desc, "unique_seeds": 0, "basis_maps": 0, "symmetric_seeds": 0, "alternating_seeds": 0, "nonfree_seeds": 0, "target_histogram": Counter()})
        m["unique_seeds"] += 1
        m["basis_maps"] += row["reuse_count"]
        m["symmetric_seeds"] += row["symmetry"] == "Sym"
        m["alternating_seeds"] += row["symmetry"] == "Lambda"
        m["nonfree_seeds"] += row["stabilizer_order"] > 1
        m["target_histogram"].update(row["targets"])

    ordered = []
    for i, (key, m) in enumerate(sorted(motifs.items(), key=lambda kv: (kv[1]["descriptor"]["target_radius"], kv[1]["descriptor"]["union_vertex_count"], kv[1]["descriptor"]["target_source_features"], kv[1]["descriptor"]["source_source_feature"]))):
        z = dict(m)
        z["target_histogram"] = {str(k): v for k, v in sorted(z["target_histogram"].items())}
        z["motif_id"] = f"M{i+1}"
        z["motif_sha256"] = key
        ordered.append(z)
    motif_id = {z["motif_sha256"]: z["motif_id"] for z in ordered}
    for seed in seeds:
        seed["motif_id"] = motif_id[seed["motif_sha256"]]

    d = {
        "schema": "w33.pass2421.quadratic_seed_motif_quotient.v1",
        "status": "PASS_SIX_GEOMETRIC_MOTIFS_BELOW_TWENTY_FOUR_ORBIT_PROGRAMS",
        "source": {"certificate": str(SRC.relative_to(ROOT)), "sha256_without_hash_field": src["sha256_without_hash_field"]},
        "counts": {
            "basis_maps": sum(z["reuse_count"] for z in seeds),
            "unique_orbit_programs": len(seeds),
            "geometric_motifs": len(ordered),
            "motif_unique_seed_multiset": sorted((z["unique_seeds"] for z in ordered), reverse=True),
            "motif_basis_map_multiset": sorted((z["basis_maps"] for z in ordered), reverse=True),
            "nonfree_orbit_programs": sum(z["stabilizer_order"] > 1 for z in seeds),
        },
        "motifs": ordered,
        "seed_table": sorted(seeds, key=lambda z: (z["motif_id"], z["symmetry"], z["representative"])),
        "checks": {
            "literal_edge_index_size_240": len(edges) == 240,
            "source_seed_count_24": len(seeds) == 24,
            "lifted_map_count_50": sum(z["reuse_count"] for z in seeds) == 50,
            "exactly_six_motifs": len(ordered) == 6,
            "seed_multiplicities_9_6_4_3_1_1": sorted((z["unique_seeds"] for z in ordered), reverse=True) == [9, 6, 4, 3, 1, 1],
            "map_multiplicities_17_12_10_6_4_1": sorted((z["basis_maps"] for z in ordered), reverse=True) == [17, 12, 10, 6, 4, 1],
            "four_nonfree_programs": sum(z["stabilizer_order"] > 1 for z in seeds) == 4,
            "all_nonfree_in_largest_motif": sum(z["nonfree_seeds"] for z in ordered if z["unique_seeds"] == 9) == 4,
            "no_diagonal_source_pairs": all(z["representative"][1] != z["representative"][2] for z in seeds),
        },
        "theorem": "The twenty-four cached signed-orbit programs underlying all fifty complete quadratic Hom maps collapse to exactly six source-swap-invariant W33 three-edge motifs. Thus representation storage sparsity has a second geometric quotient: 50 maps -> 24 orbit programs -> 6 edge motifs.",
        "compiler_consequence": "A hardware or symbolic compiler needs six geometric address templates plus orbit/program and target labels; it need not treat all twenty-four programs as unrelated routing geometries.",
        "boundary": "The six-motif quotient is literal edge-support geometry. It does not prove minimal CP tensor rank, short physical interaction range, or select coupling coefficients.",
    }
    assert all(d["checks"].values())
    d["sha256_without_hash_field"] = digest(d)
    return d


def main():
    d = build()
    if EXPECTED != "TO_BE_FROZEN":
        assert d["sha256_without_hash_field"] == EXPECTED
        assert d == json.loads(OUT.read_text())
    print(json.dumps({"status": d["status"], "certificate": d["sha256_without_hash_field"], "maps": 50, "programs": 24, "motifs": 6}, sort_keys=True))


if __name__ == "__main__":
    main()
