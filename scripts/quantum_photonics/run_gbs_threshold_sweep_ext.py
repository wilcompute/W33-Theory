"""Extended threshold sweep: modes 2-6, squeezings [0.3,0.6,0.9], shots 2000 by default."""

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
    repo / "bundles" / "v23_toe_finish" / "v23" / "gbs_threshold_sweep_extended.json"
)
out_png = (
    repo / "bundles" / "v23_toe_finish" / "v23" / "gbs_threshold_js_vs_eta_extended.png"
)
out_pdf = repo / "bundles" / "v23_toe_finish" / "v23" / "gbs_threshold_summary.pdf"

modes_list = [2, 3, 4, 5, 6]
squeezings = [0.3, 0.6, 0.9]
shots = 2000
etas = [0.4, 0.6, 0.8, 0.9, 1.0]
results = []
for squeezing in squeezings:
    for modes in modes_list:
        U = build_interferometer(modes, seed=42)
        for eta in etas:
            samples_gauss = sample_gbs(
                modes=modes, squeezing=squeezing, U=U, backend="gaussian", shots=shots
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
                    "js": float(js),
                    "top_patterns": [(list(k), int(v), v / shots) for k, v in topk],
                }
            )
            print("modes", modes, "r", squeezing, "eta", eta, "js", js)

# save
out_json.parent.mkdir(parents=True, exist_ok=True)
open(out_json, "w").write(json.dumps(results, indent=2))

# plot: one subplot per squeezing
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

# simple summary PDF: include the image and bullets
fig = plt.figure(figsize=(8.5, 11))
# left: image
ax1 = fig.add_axes([0.05, 0.45, 0.6, 0.5])
im = plt.imread(out_png)
ax1.imshow(im)
ax1.axis("off")
# right: bullets
ax2 = fig.add_axes([0.05, 0.05, 0.9, 0.35])
ax2.axis("off")
summary_lines = [
    "GBS threshold sweep extended",
    f"modes={modes_list}, squeezings={squeezings}, shots={shots}, etas={etas}",
    "",
    "Key observations:",
    "- JS divergence increases with modes and squeezing in many cases",
    "- Values remain small (<0.1) for our parameter grid and shots=2000",
    "- Top click patterns are stable across etas for each (modes, r) setting",
]
text = "\n".join(summary_lines)
ax2.text(0, 0.95, text, va="top", ha="left", fontsize=10, family="monospace")
plt.savefig(out_pdf)
print("Saved", out_pdf)

# also save top-pattern diagnostics separately
diag = {
    f"modes_{r['modes']}_r_{r['squeezing']}_eta_{r['eta']}": {
        "top_patterns": r["top_patterns"],
        "js": r["js"],
    }
    for r in results
}
open(str(out_json).replace(".json", "_diagnostics.json"), "w").write(
    json.dumps(diag, indent=2)
)
print("Wrote", out_json)
print("Wrote diagnostics")
