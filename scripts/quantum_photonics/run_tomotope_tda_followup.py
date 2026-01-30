"""High-precision follow-up for a selected tomotope-induced point set.
Saves per-point JSON to bundles and summary.
"""

import json
import os
import runpy
from collections import Counter
from pathlib import Path

import numpy as np
from ripser import ripser
from scipy.stats import entropy
from thewalrus import samples
from thewalrus.random import random_interferometer

repo = Path(__file__).resolve().parents[2]
out_dir = repo / "bundles" / "v23_toe_finish" / "v23"

shots = int(os.getenv("TOMOTOPE_FOLLOWUP_SHOTS", "2000"))
bootstrap = int(os.getenv("TOMOTOPE_FOLLOWUP_BOOTSTRAP", "200"))
mode = int(os.getenv("TOMOTOPE_FOLLOWUP_MODES", "8"))
kind = os.getenv("TOMOTOPE_FOLLOWUP_KIND", "structured")

# build W33
mod = runpy.run_path(str(repo / "THEORY_PART_CXXV_D5_VERIFICATION.py"))
build_W33_symplectic = mod["build_W33_symplectic"]
verts, adj = build_W33_symplectic()

N = len(adj)
if kind == "structured":
    non_neighbors = [j for j in range(N) if adj[0][j] == 0 and j != 0]
    subset = non_neighbors[:mode]
else:
    subset = list(np.random.choice(range(N), size=mode, replace=False))

A = np.array([[adj[i][j] for j in subset] for i in subset], dtype=float)
if A.max() > 0:
    A = A / A.max()

# sample
walrus_counts = Counter()
try:
    walrus_samples = samples.hafnian_sample_graph(A, n_mean=1.0, samples=shots)
    walrus_thresholds = (np.array(walrus_samples) > 0).astype(int)
    walrus_patterns = [tuple(row.tolist()) for row in walrus_thresholds]
    walrus_counts = Counter(walrus_patterns)
except Exception as e:
    walrus_counts = Counter()

# SF sampling
sf_counts = Counter()
try:
    U = random_interferometer(mode)
    from scripts.quantum_photonics.run_gbs import sample_gbs

    sf_samples = sample_gbs(
        modes=mode, squeezing=0.6, U=U, backend="gaussian", shots=shots
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

# bootstrap on walrus counts to get CI for mean H1 or js? We'll bootstrap js by resampling counts
boot_js = []
emp_counts = np.array([walrus_counts.get(p, 0) for p in all_patterns])
emp_probs = emp_counts / max(1, emp_counts.sum())
for b in range(min(bootstrap, 500)):
    draw = np.random.multinomial(shots, emp_probs)
    p_w_b = draw / shots
    m_b = 0.5 * (p_w_b + p_s)
    js_b = 0.5 * (
        entropy(np.maximum(p_w_b, 1e-12), np.maximum(m_b, 1e-12))
        + entropy(np.maximum(p_s, 1e-12), np.maximum(m_b, 1e-12))
    )
    boot_js.append(js_b)
lo = float(np.percentile(boot_js, 2.5)) if boot_js else None
hi = float(np.percentile(boot_js, 97.5)) if boot_js else None

# compute persistence on observed patterns (embed binary patterns in R^mode)
unique_patterns = [np.array(p) for p in all_patterns]
if unique_patterns:
    X = np.vstack(unique_patterns)
    try:
        R = ripser(X, maxdim=1)
        dgms = R["dgms"]
        h1_count = len([d for d in dgms[1] if np.isfinite(d[1])])
    except Exception as e:
        dgms = None
        h1_count = None
else:
    dgms = None
    h1_count = None

# save counts as serializable dicts
walrus_counts_ser = {"".join(map(str, p)): c for p, c in walrus_counts.items()}
sf_counts_ser = {"".join(map(str, p)): c for p, c in sf_counts.items()}

point_result = {
    "modes": mode,
    "kind": kind,
    "shots": shots,
    "js": float(js),
    "js_ci": [lo, hi],
    "walrus_samples": sum(walrus_counts.values()),
    "sf_samples": sum(sf_counts.values()),
    "walrus_counts": walrus_counts_ser,
    "sf_counts": sf_counts_ser,
    "h1_count": h1_count,
}

# optionally save persistence diagrams
if dgms is not None:
    # convert to lists
    point_result["persistence"] = {"H0": dgms[0].tolist(), "H1": dgms[1].tolist()}

fname = out_dir / f"tomotope_tda_followup_modes{mode}_{kind}.json"
fname.write_text(json.dumps(point_result, indent=2))
# summary
summary = [point_result]
out_dir.joinpath("tomotope_tda_followup_summary.json").write_text(
    json.dumps(summary, indent=2)
)
print("Wrote", fname, out_dir.joinpath("tomotope_tda_followup_summary.json"))
