#!/usr/bin/env sage
"""Run a subgraph isomorphism search inside Sage's Docker using stronger tools/time.

This script is intended to be executed via the Sage Docker image in CI, where it
can be given more time and memory than local quick runs. It builds the W33
line-disjointness graph and the Schlaefli 27 graph and tries to find an induced
subgraph isomorphic to Schlaefli using VF2 (NetworkX) with logging.

If found, writes artifacts/sage_schlafli_embedding.json with mapping and stabilizer info.
"""
import json
import sys
from collections import Counter
from pathlib import Path

try:
    import networkx as nx
except Exception as e:
    print("NetworkX not available in Sage container:", e)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

# reuse helpers from earlier module (we import by package path)
sys.path.append(str(ROOT))
from find_schlafli_embedding_in_w33 import (build_schlafli_adj,
                                            compute_w33_lines,
                                            compute_we6_orbits,
                                            construct_e8_roots,
                                            construct_w33_points)


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
    G_lines = nx.Graph()
    G_lines.add_nodes_from(range(len(wlines)))
    for i in range(len(wlines)):
        for j in range(i + 1, len(wlines)):
            if set(wlines[i]).isdisjoint(set(wlines[j])):
                G_lines.add_edge(i, j)

    print("W33 lines:", len(wlines))
    print("Schlaefli degrees check:", Counter(d for _, d in G_sch.degree()))

    # Try VF2 but allow long running scan; collect first match if any
    GM = nx.algorithms.isomorphism.GraphMatcher(G_lines, G_sch)
    mapping = None
    count = 0
    for iso in GM.subgraph_isomorphisms_iter():
        mapping = iso
        count += 1
        print("Found embedding #", count)
        break

    if mapping is None:
        print("No embedding found (VF2 search completed without hits).")
        return

    sch_to_w = {int(sch_i): int(w_i) for w_i, sch_i in mapping.items()}

    out = {
        "sch_to_w_mapping": sch_to_w,
    }
    (ART / "sage_schlafli_embedding.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/sage_schlafli_embedding.json")


if __name__ == "__main__":
    main()
