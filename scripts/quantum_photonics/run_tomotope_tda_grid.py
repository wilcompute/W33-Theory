"""Run a TDA grid on induced subgraphs of W33 (tomotope-related structures).
- For modes in 4..8, build a structured subset (from non-neighbors of a vertex) and a random subset
- Sample with The Walrus (hafnian_sample_graph) and Strawberry Fields Gaussian backend
- Compute JS between walrus and SF distributions, mean H1 (from ripser), and save results
"""

import json
import runpy
from collections import Counter
from pathlib import Path

import numpy as np
from ripser import ripser
from scipy.stats import entropy
from thewalrus import samples
from thewalrus.random import random_interferometer

repo = Path(__file__).resolve().parents[2]
out = repo / "bundles" / "v23_toe_finish" / "v23" / "tomotope_tda_grid.json"

# Build W33 adjacency (reuse existing builder)
mod = runpy.run_path(str(repo / "THEORY_PART_CXXV_D5_VERIFICATION.py"))
build_W33_symplectic = mod["build_W33_symplectic"]
import io
import os
# suppress unicode printing from the module on Windows consoles
import sys

old_stdout = sys.stdout
try:
    sys.stdout = io.TextIOWrapper(open(os.devnull, "wb"), encoding="utf-8")
    verts, adj = build_W33_symplectic()
finally:
    try:
        sys.stdout.detach()
    except Exception:
        pass
    sys.stdout = old_stdout
if verts is None:
    raise SystemExit("failed to build W33")

N = len(adj)
np.random.seed(42)
results = []
for modes in range(4, 9):
    # structured subset: take first vertex's non-neighbors and pick first 'modes' nodes from it
    non_neighbors = [j for j in range(N) if adj[0][j] == 0 and j != 0]
    structured = non_neighbors[:modes]
    random_subset = list(np.random.choice(range(N), size=modes, replace=False))

    for kind, subset in [("structured", structured), ("random", random_subset)]:
        A = np.array([[adj[i][j] for j in subset] for i in subset], dtype=float)
        # scale adjacency to [0,1]
        if A.max() > 0:
            A = A / A.max()
        else:
            A = A
        shots = 1000
        # walrus sampling (graph-based hafnian sampler)
        try:
            walrus_samples = samples.hafnian_sample_graph(A, n_mean=1.0, samples=shots)
            walrus_thresholds = (np.array(walrus_samples) > 0).astype(int)
            walrus_patterns = [tuple(row.tolist()) for row in walrus_thresholds]
            walrus_counts = Counter(walrus_patterns)
        except Exception as e:
            walrus_counts = Counter()
        # strawberryfields gaussian sampling (rough comparison via random interferometer)
        try:
            U = random_interferometer(modes)
            from scripts.quantum_photonics.run_gbs import sample_gbs

            sf_samples = sample_gbs(
                modes=modes, squeezing=0.6, U=U, backend="gaussian", shots=shots
            )
            sf_thresholds = (np.array(sf_samples) > 0).astype(int)
            sf_patterns = [tuple(row.tolist()) for row in sf_thresholds]
            sf_counts = Counter(sf_patterns)
        except Exception as e:
            sf_counts = Counter()
        all_patterns = sorted(set(walrus_counts.keys()) | set(sf_counts.keys()))

        def dist_from_counts(counts):
            total = sum(counts.values())
            if total == 0:
                return np.array([1.0 / len(all_patterns)] * len(all_patterns))
            return np.array([counts.get(p, 0) / total for p in all_patterns])

        p_w = dist_from_counts(walrus_counts)
        p_s = dist_from_counts(sf_counts)
        m = 0.5 * (p_w + p_s)
        js = 0.5 * (
            entropy(np.maximum(p_w, 1e-12), np.maximum(m, 1e-12))
            + entropy(np.maximum(p_s, 1e-12), np.maximum(m, 1e-12))
        )

        # mean H1 features (approx): compute persistence on unique observed patterns
        def mean_h1_counts(patterns):
            if len(patterns) == 0:
                return 0.0
            h1s = []
            for pat in patterns[: min(200, len(patterns))]:
                X = np.array(pat).reshape(1, -1)
                dgms = ripser(X, maxdim=1)["dgms"]
                h1s.append(len(dgms[1]))
            return float(np.mean(h1s))

        mw = mean_h1_counts(list(walrus_counts.keys()))
        ms = mean_h1_counts(list(sf_counts.keys()))
        results.append(
            {
                "modes": modes,
                "kind": kind,
                "shots": shots,
                "js_w_sf": float(js),
                "mean_h1_walrus": mw,
                "mean_h1_sf": ms,
                "walrus_samples": sum(walrus_counts.values()),
                "sf_samples": sum(sf_counts.values()),
            }
        )

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(results, indent=2))
print("Wrote", out)
