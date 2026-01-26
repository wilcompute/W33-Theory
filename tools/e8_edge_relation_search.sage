#!/usr/bin/env sage
"""
Search for alternative E8 mappings by comparing graphs on W33 edges to
E8 root adjacency graphs under different relations.

We classify pairs of W33 edges by:
  - s = number of shared endpoints (0 or 1)
  - x = number of cross-adjacencies between endpoints

We then build graphs on the 240 edges using each class and unions of classes,
and compare regular candidates to E8 root graphs (inner products 1, 0, -1).

Outputs:
- artifacts/e8_edge_relation_search.json
- artifacts/e8_edge_relation_search.md
"""
from sage.all import *
import json
from datetime import datetime
from itertools import combinations

out_json = "artifacts/e8_edge_relation_search.json"
out_md = "artifacts/e8_edge_relation_search.md"

W33 = graphs.SymplecticPolarGraph(4, 3)
adj = W33.adjacency_matrix()

# List W33 edges (u < v)
edge_list = []
for u, v in W33.edges(labels=False):
    if u == v:
        continue
    edge_list.append((min(u, v), max(u, v)))
edge_list = sorted(set(edge_list))
num_edges = len(edge_list)

def is_adj(u, v):
    return bool(adj[u, v])

# Classify edge pairs by (s, x)
from collections import defaultdict

class_pairs = defaultdict(list)
class_degs = defaultdict(lambda: [0] * num_edges)

for i in range(num_edges):
    a, b = edge_list[i]
    for j in range(i + 1, num_edges):
        c, d = edge_list[j]
        s = len({a, b} & {c, d})
        if s == 2:
            continue
        if s == 1:
            shared = a if a in (c, d) else b
            other1 = b if shared == a else a
            other2 = d if shared == c else c
            x = 1 if is_adj(other1, other2) else 0
        else:
            x = 0
            if is_adj(a, c):
                x += 1
            if is_adj(a, d):
                x += 1
            if is_adj(b, c):
                x += 1
            if is_adj(b, d):
                x += 1
        key = (s, x)
        class_pairs[key].append((i, j))
        class_degs[key][i] += 1
        class_degs[key][j] += 1

class_keys = sorted(class_pairs.keys())

def graph_summary(G):
    degs = G.degree_sequence()
    deg_set = sorted(set(degs))
    try:
        eigs = G.adjacency_matrix().eigenvalues()
        from collections import Counter
        counts = Counter(eigs)
        spectrum = sorted([(int(e), int(m)) for e, m in counts.items()], key=lambda x: -x[0])
    except Exception:
        spectrum = None
    return {
        "order": G.order(),
        "size": G.size(),
        "degree_set": deg_set,
        "degree": degs[0] if len(deg_set) == 1 else None,
        "spectrum": spectrum,
    }

# E8 roots and root graphs
E8 = RootSystem(['E', 8])
L_root = E8.root_lattice()
roots = list(L_root.roots())
C = E8.cartan_type().cartan_matrix()
n = len(roots)

def root_inner_product(r, s):
    v = vector(ZZ, r.to_vector())
    w = vector(ZZ, s.to_vector())
    return (v * C * w)

def root_graph(inner_product_value):
    edges = []
    for i in range(n):
        ri = roots[i]
        for j in range(i + 1, n):
            if root_inner_product(ri, roots[j]) == inner_product_value:
                edges.append((i, j))
    G = Graph(edges)
    G.add_vertices(range(n))
    return G

e8_graphs = {}
for ip in [1, 0, -1]:
    G = root_graph(ip)
    e8_graphs[str(ip)] = graph_summary(G)

results = {
    "timestamp": datetime.now().isoformat(),
    "edge_count": num_edges,
    "classes": {},
    "regular_subsets": [],
    "e8_root_graphs": e8_graphs,
}

# Summarize each class
for key in class_keys:
    degs = class_degs[key]
    deg_set = sorted(set(degs))
    results["classes"][f"{key[0]}_{key[1]}"] = {
        "shared_endpoints": key[0],
        "cross_adjacent": key[1],
        "pair_count": len(class_pairs[key]),
        "degree_set": deg_set,
        "degree": degs[0] if len(deg_set) == 1 else None,
    }

# Precompute degree arrays for subset search
deg_arrays = {key: class_degs[key] for key in class_keys}

def subset_degree(keys):
    deg = [0] * num_edges
    for key in keys:
        arr = deg_arrays[key]
        for i in range(num_edges):
            deg[i] += arr[i]
    return deg

def build_graph(keys):
    edges = []
    for key in keys:
        edges.extend(class_pairs[key])
    G = Graph(edges)
    G.add_vertices(range(num_edges))
    return G

# Search all subsets for regular graphs (including degree 56 candidates)
keys_list = list(class_keys)
for mask in range(1, 1 << len(keys_list)):
    subset = [keys_list[i] for i in range(len(keys_list)) if (mask >> i) & 1]
    deg = subset_degree(subset)
    if len(set(deg)) != 1:
        continue
    d = deg[0]
    G = build_graph(subset)
    summary = graph_summary(G)
    item = {
        "keys": [f"{k[0]}_{k[1]}" for k in subset],
        "degree": d,
        "size": summary["size"],
        "spectrum": summary["spectrum"],
        "matches_e8": {},
    }
    for ip, e8s in e8_graphs.items():
        item["matches_e8"][ip] = (
            summary["order"] == e8s["order"]
            and summary["degree"] == e8s["degree"]
            and summary["spectrum"] == e8s["spectrum"]
        )
    results["regular_subsets"].append(item)

# Write JSON
import os
os.makedirs("artifacts", exist_ok=True)
with open(out_json, "w") as f:
    json.dump(results, f, indent=2)

# Write markdown
lines = []
lines.append("# E8 Alternative Mapping Search (Edge-Relation Classes)")
lines.append("")
lines.append(f"Generated: {results['timestamp']}")
lines.append("")
lines.append(f"W33 edges: {results['edge_count']}")
lines.append("")
lines.append("## Class Summary (by shared endpoints / cross adjacency)")
lines.append("")
lines.append("| class | shared endpoints | cross adjacency | pair_count | degree_set | degree |")
lines.append("|---|---:|---:|---:|---|---:|")
for key in class_keys:
    kstr = f"{key[0]}_{key[1]}"
    c = results["classes"][kstr]
    lines.append(
        f"| {kstr} | {c['shared_endpoints']} | {c['cross_adjacent']} | {c['pair_count']} | {c['degree_set']} | {c['degree']} |"
    )

lines.append("")
lines.append("## Regular Subsets")
lines.append("")
lines.append("| keys | degree | size | spectrum | matches E8 ip=1 | ip=0 | ip=-1 |")
lines.append("|---|---:|---:|---|:---:|:---:|:---:|")
for item in results["regular_subsets"]:
    keys = ",".join(item["keys"])
    lines.append(
        f"| {keys} | {item['degree']} | {item['size']} | {item['spectrum']} | {item['matches_e8']['1']} | {item['matches_e8']['0']} | {item['matches_e8']['-1']} |"
    )

lines.append("")
lines.append("## E8 Root Graph Summaries")
lines.append("")
for ip, e8s in results["e8_root_graphs"].items():
    lines.append(f"- inner product {ip}: degree={e8s['degree']}, spectrum={e8s['spectrum']}")

with open(out_md, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {out_json}")
print(f"Wrote {out_md}")
