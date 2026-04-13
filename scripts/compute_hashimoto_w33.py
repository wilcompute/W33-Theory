#!/usr/bin/env python3
"""Compute the Hashimoto (non-backtracking) operator for W33 and its spectrum.

Requires the repo's W33 builder: `from scripts.e8_embedding_group_theoretic import build_w33`.
Writes eigenvalue JSON and a small plot to `checks/`.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

try:
    # Prefer package-relative import when used as a module; fall back to
    # absolute import for direct script execution.
    from .e8_embedding_group_theoretic import build_w33
except Exception:  # pragma: no cover - fallback for direct script execution
    from scripts.e8_embedding_group_theoretic import build_w33


def build_hashimoto(adj, edges):
    # directed edges list: (u->v) for each undirected edge
    directed = []
    for u, v in edges:
        directed.append((u, v))
        directed.append((v, u))
    m = len(directed)
    index = {e: i for i, e in enumerate(directed)}

    B = np.zeros((m, m), dtype=int)
    for i, (u, v) in enumerate(directed):
        for j, (x, y) in enumerate(directed):
            # non-backtracking condition: v == x and y != u
            if v == x and y != u:
                B[i, j] = 1
    return B, directed


def main():
    out_dir = Path("checks")
    out_dir.mkdir(exist_ok=True)

    n, vertices, adj, edges = build_w33()
    B, directed = build_hashimoto(adj, edges)
    # eigenvalues
    w = np.linalg.eigvals(B.astype(float))
    spectral_radius = float(np.max(np.abs(w)))
    out = {
        "n": n,
        "directed_edges": len(directed),
        "spectral_radius": spectral_radius,
        "spectral_radius_squared": spectral_radius ** 2,
    }
    with open(out_dir / "w33_hashimoto_spectrum.json", "w") as f:
        json.dump(out, f, indent=2)
    np.savez(out_dir / "w33_hashimoto_eigs.npz", w=w)
    print(f"Wrote Hashimoto spectrum artifact to {out_dir}")


if __name__ == "__main__":
    main()
