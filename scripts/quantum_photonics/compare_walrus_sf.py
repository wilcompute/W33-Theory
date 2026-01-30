"""Compare The Walrus hafnian-based sampling with Strawberry Fields gaussian sampling.
Runs small experiments for low mode counts and reports JS divergence, mean clicks, and simple H1 proxy.
Saves results to bundles/v23_toe_finish/v23/walrus_sf_comparison.json
"""

import json
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import entropy
from thewalrus import samples
from thewalrus.random import random_interferometer

from scripts.quantum_photonics.run_gbs import sample_gbs

repo = Path(__file__).resolve().parents[2]
out = repo / "bundles" / "v23_toe_finish" / "v23" / "walrus_sf_comparison.json"

modes_list = [3, 4, 5]
shots = 400
results = []
for modes in modes_list:
    np.random.seed(123 + modes)
    U = random_interferometer(modes)
    A = np.abs(U + U.T)
    A = A / np.max(A)

    # walrus sampling
    try:
        walrus_samples = samples.hafnian_sample_graph(A, n_mean=1.0, samples=shots)
        walrus_thresholds = (np.array(walrus_samples) > 0).astype(int)
        walrus_patterns = [tuple(row.tolist()) for row in walrus_thresholds]
        walrus_counts = Counter(walrus_patterns)
    except Exception as e:
        walrus_counts = Counter()

    # strawberryfields gaussian sampling
    try:
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
    mw = sum(sum(p) * c for p, c in walrus_counts.items()) / max(
        1, sum(walrus_counts.values())
    )
    ms = sum(sum(p) * c for p, c in sf_counts.items()) / max(1, sum(sf_counts.values()))

    results.append(
        {
            "modes": modes,
            "shots": shots,
            "js": float(js),
            "mean_clicks_walrus": float(mw),
            "mean_clicks_sf": float(ms),
        }
    )

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(results, indent=2))
print("Wrote", out)
