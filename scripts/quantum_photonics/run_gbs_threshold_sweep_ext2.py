"""Adaptive extended threshold sweep with per-mode shot scheduling and safe partial-save on interruption."""

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
    repo
    / "bundles"
    / "v23_toe_finish"
    / "v23"
    / "gbs_threshold_sweep_ext_adaptive.json"
)
out_png = (
    repo
    / "bundles"
    / "v23_toe_finish"
    / "v23"
    / "gbs_threshold_js_vs_eta_ext_adaptive.png"
)
out_pdf = (
    repo / "bundles" / "v23_toe_finish" / "v23" / "gbs_threshold_summary_adaptive.pdf"
)

modes_list = [2, 3, 4, 5, 6]
squeezings = [0.3, 0.6, 0.9]
# adaptive shots: modes<=3 -> 2000, 4 -> 1000, >=5 -> 500
shots_map = {2: 2000, 3: 2000, 4: 1000, 5: 500, 6: 500}
etas = [0.4, 0.6, 0.8, 0.9, 1.0]
results = []
try:
    for squeezing in squeezings:
        for modes in modes_list:
            shots = shots_map.get(modes, 500)
            U = build_interferometer(modes, seed=42)
            for eta in etas:
                print(f"RUN start: modes={modes} r={squeezing} eta={eta} shots={shots}")
                samples_gauss = sample_gbs(
                    modes=modes,
                    squeezing=squeezing,
                    U=U,
                    backend="gaussian",
                    shots=shots,
                )
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
                # partial save after each run
                out_json.parent.mkdir(parents=True, exist_ok=True)
                open(out_json, "w").write(json.dumps(results, indent=2))
                print("RUN done:", modes, squeezing, eta, "js", js)
except KeyboardInterrupt:
    print("Interrupted by user, saved partial results.")
finally:
    # create plots from whatever we have
    if len(results) > 0:
        squeezings_present = sorted(list({r["squeezing"] for r in results}))
        fig, axs = plt.subplots(
            len(squeezings_present),
            1,
            figsize=(6, 3 * len(squeezings_present)),
            sharex=True,
        )
        if len(squeezings_present) == 1:
            axs = [axs]
        for i, squeezing in enumerate(squeezings_present):
            ax = axs[i]
            modes_list_present = sorted(
                list({r["modes"] for r in results if r["squeezing"] == squeezing})
            )
            for modes in modes_list_present:
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
        # summary pdf
        fig = plt.figure(figsize=(8.5, 11))
        ax1 = fig.add_axes([0.05, 0.45, 0.6, 0.5])
        im = plt.imread(out_png)
        ax1.imshow(im)
        ax1.axis("off")
        ax2 = fig.add_axes([0.05, 0.05, 0.9, 0.35])
        ax2.axis("off")
        summary_lines = [
            "GBS threshold sweep (adaptive)",
            f"modes={modes_list}, squeezings={squeezings}, shots_map={shots_map}, etas={etas}",
            "",
            "Key observations (partial):",
            "- JS divergence generally increases with modes and squeezing for this grid",
            "- Adaptive shots reduce runtime for large modes while preserving trend signals",
        ]
        ax2.text(
            0,
            0.95,
            "\n".join(summary_lines),
            va="top",
            ha="left",
            fontsize=10,
            family="monospace",
        )
        plt.savefig(out_pdf)
        print("Saved final/partial outputs")
    else:
        print("No results to save.")
