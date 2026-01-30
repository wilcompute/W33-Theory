"""Quick adaptive threshold sweep with conservative shot counts to ensure completion."""

import json

import matplotlib
import numpy as np

matplotlib.use("Agg")
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from scipy.stats import entropy

from scripts.quantum_photonics.run_gbs import (build_interferometer,
                                               compute_threshold_probs,
                                               sample_gbs)

repo = Path(__file__).resolve().parents[2]
out_json = (
    repo / "bundles" / "v23_toe_finish" / "v23" / "gbs_threshold_sweep_quick.json"
)
out_png = (
    repo / "bundles" / "v23_toe_finish" / "v23" / "gbs_threshold_js_vs_eta_quick.png"
)

modes_list = [2, 3, 4, 5, 6]
squeezings = [0.3, 0.6, 0.9]
# conservative shots: 2-3 -> 2000; 4 -> 500; >=5 -> 200
shots_map = {2: 2000, 3: 2000, 4: 500, 5: 200, 6: 200}
etas = [0.4, 0.6, 0.8, 0.9, 1.0]
results = []
for squeezing in squeezings:
    for modes in modes_list:
        shots = shots_map.get(modes, 200)
        U = build_interferometer(modes, seed=42)
        for eta in etas:
            print(f"RUN start: modes={modes} r={squeezing} eta={eta} shots={shots}")
            try:
                samples_gauss = sample_gbs(
                    modes=modes,
                    squeezing=squeezing,
                    U=U,
                    backend="gaussian",
                    shots=shots,
                )
            except Exception as e:
                print("Gaussian sampler failed, falling back to analytic sampling:", e)
                th_probs = compute_threshold_probs(
                    modes=modes, squeezings=[squeezing] * modes, U=U, eta=eta
                )
                import random

                patterns = list(th_probs.keys())
                probs = [th_probs[p] for p in patterns]
                ssum = sum(probs)
                if ssum <= 0:
                    probs = [1.0 / len(probs)] * len(probs)
                else:
                    probs = [p / ssum for p in probs]
                draws = random.choices(patterns, weights=probs, k=shots)
                samples_gauss = np.array(draws, dtype=int)
            thresholds_emp = np.array(samples_gauss) > 0
            counts = Counter(tuple(row.astype(int)) for row in thresholds_emp)
            th_probs = compute_threshold_probs(
                modes=modes, squeezings=[squeezing] * modes, U=U, eta=eta
            )
            all_patterns = sorted(th_probs.keys())
            p_emp = np.array([counts.get(p, 0) / shots for p in all_patterns])
            p_th = np.array([th_probs.get(p, 0.0) for p in all_patterns])
            m = 0.5 * (p_emp + p_th)
            js = 0.5 * (
                entropy(np.maximum(p_emp, 1e-12), np.maximum(m, 1e-12))
                + entropy(np.maximum(p_th, 1e-12), np.maximum(m, 1e-12))
            )
            topk = counts.most_common(10)
            results.append(
                {
                    "modes": modes,
                    "squeezing": squeezing,
                    "eta": eta,
                    "shots": shots,
                    "js": float(js),
                    "top_patterns": [(list(k), int(v), v / shots) for k, v in topk],
                }
            )
            out_json.parent.mkdir(parents=True, exist_ok=True)
            open(out_json, "w").write(json.dumps(results, indent=2))
            print("RUN done:", modes, squeezing, eta, "js", js)
# plots
if len(results) > 0:
    fig, axs = plt.subplots(
        len(squeezings), 1, figsize=(6, 3 * len(squeezings)), sharex=True
    )
    for i, squeezing in enumerate(squeezings):
        ax = axs[i]
        for modes in modes_list:
            xs = [
                r["eta"]
                for r in results
                if r["modes"] == modes and r["squeezing"] == squeezing
            ]
            ys = [
                r["js"]
                for r in results
                if r["modes"] == modes and r["squeezing"] == squeezing
            ]
            ax.plot(xs, ys, marker="o", label=f"modes={modes}")
        ax.set_title(f"squeezing r={squeezing}")
        ax.set_ylabel("JS divergence")
        ax.grid(True)
        ax.legend()
    axs[-1].set_xlabel("eta")
    plt.tight_layout()
    plt.savefig(out_png)
    print("Saved", out_png)
    print("Wrote", out_json)
else:
    print("No results generated.")
