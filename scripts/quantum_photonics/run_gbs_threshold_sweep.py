"""Sweep detection efficiency and compute JS divergence between empirical threshold samples and TheWalrus analytic threshold probabilities."""

import json
from math import log
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import entropy

from scripts.quantum_photonics.run_gbs import (build_interferometer,
                                               compute_exact_probs_fock,
                                               compute_threshold_probs,
                                               sample_gbs)

repo = Path(__file__).resolve().parents[2]
out_json = repo / "bundles" / "v23_toe_finish" / "v23" / "gbs_threshold_sweep.json"
out_png = repo / "bundles" / "v23_toe_finish" / "v23" / "gbs_threshold_js_vs_eta.png"

modes_list = [2, 3]
squeezing = 0.6
shots = 200
etas = [0.4, 0.6, 0.8, 0.9, 1.0]
results = []
for modes in modes_list:
    U = build_interferometer(modes, seed=42)
    for eta in etas:
        # empirical from gaussian sampling
        samples_gauss = sample_gbs(
            modes=modes, squeezing=squeezing, U=U, backend="gaussian", shots=shots
        )
        # convert to threshold patterns
        thresholds_emp = np.array(samples_gauss) > 0
        # empirical distribution over binary patterns
        from collections import Counter

        counts = Counter(tuple(row.astype(int)) for row in thresholds_emp)
        keys = list(counts.keys())
        # analytic threshold probs
        th_probs = compute_threshold_probs(
            modes=modes, squeezings=[squeezing] * modes, U=U, eta=eta
        )
        # build aligned vector support: all patterns
        all_patterns = sorted(th_probs.keys())
        p_emp = np.array([counts.get(p, 0) / shots for p in all_patterns])
        p_th = np.array([th_probs.get(p, 0.0) for p in all_patterns])
        # compute JS divergence
        m = 0.5 * (p_emp + p_th)
        js = 0.5 * (
            entropy(np.maximum(p_emp, 1e-12), np.maximum(m, 1e-12))
            + entropy(np.maximum(p_th, 1e-12), np.maximum(m, 1e-12))
        )
        results.append({"modes": modes, "eta": eta, "js": float(js)})
        print("modes", modes, "eta", eta, "js", js)

# plot
import matplotlib.pyplot as plt

for modes in modes_list:
    xs = [r["eta"] for r in results if r["modes"] == modes]
    ys = [r["js"] for r in results if r["modes"] == modes]
    plt.plot(xs, ys, marker="o", label=f"modes={modes}")
plt.xlabel("Detector efficiency / transmissivity (eta)")
plt.ylabel("Jensen-Shannon divergence (empirical || analytic threshold)")
plt.legend()
plt.title("GBS threshold JS divergence vs detector efficiency")
plt.grid(True)
plt.savefig(out_png)
print("Saved", out_png)
open(out_json, "w").write(json.dumps(results, indent=2))
print("Wrote", out_json)
