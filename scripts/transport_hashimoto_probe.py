"""Probe Hashimoto (non-backtracking) spectrum under a candidate selector.

This utility constructs the directed-edge Hashimoto (non-backtracking) operator
for the W33 transport carrier and applies a phase-twist determined by a
candidate assignment (labels 0..2 interpreted as cubic phases) on each
quadrangle index.  It computes spectral diagnostics (trace, top eigenvalues,
Ihara polynomial seeds) that can be compared across candidate assignments to
detect the signature of an activated holonomy.

Usage (run locally in venv):
  python scripts/transport_hashimoto_probe.py --assignment data/transport_csp_or_tools_seed0.json --out data/transport_hashimoto_probe_seed0.json

Note: this is a diagnostic tool to compare candidate selectors without running
the full holonomy bridge.  The computed spectra are useful for clustering
candidate solutions and for detecting the expected branch-averaged corrections
in the Hashimoto spectrum.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
if str(Path(__file__).resolve().parents[1]) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np


def build_directed_edge_list():
    # reuse the W33 geometry builder for edges ordering
    from scripts.w33_h4_orbital_no_go import _simple_line_graph_cycles, _line_intersection_graph

    # build quadrangle cycles as canonical 4-cycles
    cycles = _simple_line_graph_cycles(4)
    # flatten to directed edge list (ordered pairs) for Hashimoto operator indexing
    directed = []
    for cycle in cycles:
        for i in range(4):
            a = cycle[i]
            b = cycle[(i + 1) % 4]
            directed.append((a, b))
    return cycles, directed


def build_hashimoto_matrix(directed_edges):
    m = len(directed_edges)
    idx_map = {e: i for i, e in enumerate(directed_edges)}
    B = np.zeros((m, m), dtype=complex)
    for i, (u, v) in enumerate(directed_edges):
        for j, (x, y) in enumerate(directed_edges):
            # non-backtracking: v == x and y != u
            if v == x and y != u:
                B[i, j] = 1.0
    return B, idx_map


def apply_selector_phases(B, idx_map, assignment_map):
    # assignment_map: mapping from quadrangle index -> label 0/1/2
    # interpret label b as phase exp(2π i b / 3)
    phases = {int(k): np.exp(2j * np.pi * (int(v) % 3) / 3.0) for k, v in assignment_map.items()}
    # For simplicity, multiply rows corresponding to directed edges whose base quadrangle index is in phases
    B2 = B.copy()
    for (a, b), idx in idx_map.items():
        # use base quadrangle index `a` as proxy (heuristic); if label present, apply as multiplier
        if str(a) in assignment_map or a in phases:
            ph = phases.get(a, phases.get(str(a), 1.0))
            B2[idx, :] *= ph
    return B2


def spectral_diagnostics(B, k=8):
    vals, vecs = np.linalg.eig(B)
    # sort by magnitude
    mags = np.abs(vals)
    order = np.argsort(-mags)
    top_vals = vals[order][:k]
    return {
        "trace": float(np.trace(B)),
        "spectral_radius": float(np.max(mags)),
        "top_eigenvalues": [complex(v) for v in top_vals],
        "eigenvalue_count": int(len(vals)),
    }


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--assignment", default="data/transport_csp_or_tools_seed0.json")
    parser.add_argument("--out", default="data/transport_hashimoto_probe.json")
    args = parser.parse_args()

    path = Path(args.assignment)
    if not path.exists():
        print(json.dumps({"status": "missing_assignment", "path": str(path)}))
        return

    data = json.loads(path.read_text(encoding="utf-8"))
    assignment = data.get("assignment") or data.get("assignments") or {}

    cycles, directed = build_directed_edge_list()
    B, idx_map = build_hashimoto_matrix(directed)
    B_twisted = apply_selector_phases(B, idx_map, assignment)
    diag = spectral_diagnostics(B_twisted)

    out = {"status": "ok", "input_assignment": str(path), "diagnostics": diag}
    out_path = Path(args.out)
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, default=str))
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
