#!/usr/bin/env sage
"""
Enumerate SRG(40,12,2,4) graphs from Sage's database and compare invariants
against the symplectic polar graph W33.

Outputs:
- artifacts/srg40_uniqueness.json
- artifacts/srg40_uniqueness.md
"""
from sage.all import *
import json
from datetime import datetime

out_json = "artifacts/srg40_uniqueness.json"
out_md = "artifacts/srg40_uniqueness.md"

results = {
    "timestamp": datetime.now().isoformat(),
    "graphs": [],
    "count": 0,
    "errors": [],
    "source": None,
}

W33 = graphs.SymplecticPolarGraph(4, 3)

graphs_iter = []
try:
    from sage.graphs.strongly_regular_db import strongly_regular_graphs
    graphs_iter = strongly_regular_graphs(40, 12, 2, 4)
except Exception as e:
    results["errors"].append(f"Failed to import strongly_regular_graphs: {e}")

# Optional: load graph6 list from path or URL if provided
import os as _os
from urllib.request import urlopen

g6_path = _os.environ.get("SRG40_G6_PATH", "").strip()
g6_url = _os.environ.get("SRG40_G6_URL", "").strip()
text_path = _os.environ.get("SRG40_TEXT_PATH", "").strip()
text_url = _os.environ.get("SRG40_TEXT_URL", "").strip()
default_text_path = "data/srg_40_12_2_4.txt"

if not graphs_iter:
    g6_data = None
    try:
        if g6_path:
            with open(g6_path, "r") as f:
                g6_data = f.read().strip().splitlines()
        elif g6_url:
            with urlopen(g6_url) as resp:
                g6_data = resp.read().decode("utf-8").strip().splitlines()
    except Exception as e:
        results["errors"].append(f"Failed to load graph6 list: {e}")

    if g6_data:
        graphs_iter = [Graph(g6) for g6 in g6_data if g6 and not g6.startswith("#")]
        results["source"] = f"graph6:{g6_path or g6_url}"

def _load_text_graphs(raw_text):
    rows = []
    for line in raw_text.splitlines():
        s = line.strip().replace(" ", "")
        if not s:
            continue
        if s.startswith("dim=") or s.startswith("TOTAL"):
            continue
        if set(s) <= {"0", "1"}:
            rows.append(s)
    if len(rows) % 40 != 0:
        raise ValueError(f"Expected rows multiple of 40, got {len(rows)}")
    graphs = []
    for i in range(0, len(rows), 40):
        block = rows[i : i + 40]
        if any(len(r) != 40 for r in block):
            raise ValueError("Row length mismatch in adjacency matrix block")
        mat = matrix(ZZ, [[int(c) for c in r] for r in block])
        graphs.append(Graph(mat))
    return graphs

if not graphs_iter:
    text_data = None
    try:
        if text_path:
            with open(text_path, "r") as f:
                text_data = f.read()
        elif text_url:
            with urlopen(text_url) as resp:
                text_data = resp.read().decode("utf-8")
        elif _os.path.exists(default_text_path):
            with open(default_text_path, "r") as f:
                text_data = f.read()
    except Exception as e:
        results["errors"].append(f"Failed to load adjacency matrices: {e}")

    if text_data:
        try:
            graphs_iter = _load_text_graphs(text_data)
            results["source"] = f"text:{text_path or text_url or default_text_path}"
        except Exception as e:
            results["errors"].append(f"Failed to parse adjacency matrices: {e}")

for idx, G in enumerate(graphs_iter):
    try:
        aut = G.automorphism_group().order()
    except Exception:
        aut = None

    try:
        clique_num = G.clique_number()
        clique_max_count = len(G.cliques_maximum()) if clique_num is not None else None
    except Exception:
        clique_num = None
        clique_max_count = None

    # neighbor-graph triangle-free property
    neighbor_triangle_free = True
    try:
        for v in G.vertices():
            N = G.subgraph(G.neighbors(v))
            if N.triangles_count() != 0:
                neighbor_triangle_free = False
                break
    except Exception:
        neighbor_triangle_free = None

    try:
        is_w33 = G.is_isomorphic(W33)
    except Exception:
        is_w33 = None

    results["graphs"].append({
        "index": idx,
        "aut_order": int(aut) if aut is not None else None,
        "clique_number": int(clique_num) if clique_num is not None else None,
        "max_clique_count": int(clique_max_count) if clique_max_count is not None else None,
        "neighbor_graphs_triangle_free": neighbor_triangle_free,
        "isomorphic_to_w33": is_w33,
    })

results["count"] = len(results["graphs"])

# Write JSON
import os
os.makedirs("artifacts", exist_ok=True)
with open(out_json, "w") as f:
    json.dump(results, f, indent=2)

# Write markdown summary
lines = []
lines.append("# SRG(40,12,2,4) Uniqueness Scan")
lines.append("")
lines.append(f"Generated: {results['timestamp']}")
lines.append("")
lines.append(f"Total graphs enumerated: {results['count']}")
if results["errors"]:
    lines.append("")
    lines.append("## Errors")
    for e in results["errors"]:
        lines.append(f"- {e}")

lines.append("")
lines.append("## Summary Table")
lines.append("")
lines.append("| idx | aut_order | clique_number | max_clique_count | neighbor_graphs_triangle_free | isomorphic_to_w33 |")
lines.append("|---:|---:|---:|---:|:---:|:---:|")
for g in results["graphs"]:
    lines.append(
        f"| {g['index']} | {g['aut_order']} | {g['clique_number']} | {g['max_clique_count']} | {g['neighbor_graphs_triangle_free']} | {g['isomorphic_to_w33']} |"
    )

with open(out_md, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {out_json}")
print(f"Wrote {out_md}")
