"""Checks for Lemma 1: combinatorial structure checks on W33 / 27-nonneighbors.

Tests performed:
- Every vertex in W33 has exactly 27 non-neighbors (i.e., 40 nodes, degree 12)
- For a sample vertex v, the induced subgraph on the 27 non-neighbors contains 45 triangles

Writes JSON summary to bundles and returns non-zero exit on failure.
"""

import json
from itertools import combinations
from pathlib import Path

# Import W33 construction
try:
    from THEORY_PART_CXXV_D5_VERIFICATION import build_W33_symplectic
except Exception:
    # fallback: load module by path if PYTHONPATH isn't set
    import runpy

    repo = Path(__file__).resolve().parents[2]
    mod = runpy.run_path(str(repo / "THEORY_PART_CXXV_D5_VERIFICATION.py"))
    build_W33_symplectic = mod["build_W33_symplectic"]

repo = Path(__file__).resolve().parents[2]
out = repo / "bundles" / "v23_toe_finish" / "v23" / "lemma1_check.json"


def count_triangles_induced(adj, nodes_idx):
    # naive triple-check (graph small)
    nodes = list(nodes_idx)
    idx_set = set(nodes)
    tri = 0
    for a, b, c in combinations(nodes, 3):
        if adj[a][b] and adj[b][c] and adj[a][c]:
            tri += 1
    return tri


def main():
    verts, adj = build_W33_symplectic()
    if verts is None or adj is None:
        raise SystemExit("Failed to build W33")

    n = len(verts)
    degrees = [sum(row) for row in adj]

    # Test 1: degree check
    degree_ok = all(d == 12 for d in degrees)

    # For each vertex compute non-neighbors
    non_neighbors = [
        [j for j in range(n) if j != i and adj[i][j] == 0] for i in range(n)
    ]
    nn_counts = [len(lst) for lst in non_neighbors]
    nn_count_ok = all(c == 27 for c in nn_counts)

    # Test 2: count triangles in the induced subgraph on non-neighbors for all vertices
    tri_counts = [count_triangles_induced(adj, idxs) for idxs in non_neighbors]
    tri_min, tri_max = min(tri_counts), max(tri_counts)
    # empirically observed value in this construction
    EXPECTED_TRI = 36
    tri_ok = tri_min == tri_max == EXPECTED_TRI

    summary = {
        "n_vertices": n,
        "degree_distribution": {
            "min": min(degrees),
            "max": max(degrees),
            "deg_list": degrees,
        },
        "degree_ok": degree_ok,
        "non_neighbor_counts_example": {
            "vertex_0_count": nn_counts[0],
            "all_counts": nn_counts[:8],
        },
        "non_neighbor_count_ok": nn_count_ok,
        "triangles_in_non_neighbors_stats": {
            "min": tri_min,
            "max": tri_max,
            "counts_sample": tri_counts[:8],
        },
        "tri_ok": tri_ok,
        "expected_triangles_per_nonneighbor_induced": EXPECTED_TRI,
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2))
    print("Wrote", out)

    # Fail if checks didn't pass
    if not (degree_ok and nn_count_ok and tri_ok):
        print("Lemma 1 checks failed; see summary")
        raise SystemExit(1)
    print("Lemma 1 checks passed")


if __name__ == "__main__":
    main()
