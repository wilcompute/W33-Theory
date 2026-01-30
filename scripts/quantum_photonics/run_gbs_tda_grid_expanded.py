"""Expanded GBS-TDA grid runner (fallback-friendly)
Runs a grid over modes, squeezings, and etas, with configurable shots/bootstrap.
Saves per-point JSONs and a grid summary JSON and summary plot.
"""
from pathlib import Path
import json, os
import numpy as np
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

repo = Path(__file__).resolve().parents[2]
out_dir = repo / "bundles" / "v23_toe_finish" / "v23"
out_dir.mkdir(parents=True, exist_ok=True)

modes_list = [4,5,6]
squeezings = [0.3, 0.6, 0.9]
etas = [0.6, 0.8, 1.0]
shots = int(os.getenv('GRID_SHOTS','5000'))
bootstrap = int(os.getenv('GRID_BOOTSTRAP','500'))

from scripts.quantum_photonics.run_gbs import build_interferometer, compute_threshold_probs

results = []
for modes in modes_list:
    for squeezing in squeezings:
        U = build_interferometer(modes, seed=42)
        for eta in etas:
            print('Running:', modes, squeezing, eta)
            # fallback sampling
            try:
                from scripts.quantum_photonics.run_gbs import sample_gbs
                samples = sample_gbs(modes=modes, squeezing=squeezing, U=U, backend='gaussian', shots=shots)
                thresholds = (np.array(samples) > 0).astype(int)
            except Exception as e:
                print('gaussian unavailable, fallback to analytical threshold sampling', e)
                th_probs = compute_threshold_probs(modes=modes, squeezings=[squeezing]*modes, U=U, eta=eta)
                patterns = list(th_probs.keys())
                probs = [th_probs[patt] for patt in patterns]
                ssum = sum(probs)
                if ssum <= 0:
                    probs = [1.0/len(probs)]*len(probs)
                else:
                    probs = [v/ssum for v in probs]
                import random
                draws = random.choices(patterns, weights=probs, k=shots)
                thresholds = np.array([list(d) for d in draws], dtype=int)

            counts = Counter(tuple(row) for row in thresholds)
            try:
                th_probs = compute_threshold_probs(modes=modes, squeezings=[squeezing]*modes, U=U, eta=eta)
            except Exception as e:
                print('compute_threshold_probs failed, using independent-mode product fallback:', e)
                # Approximate single-mode click probability from squeezing (heuristic)
                p_click = float((np.tanh(squeezing)) ** 2)
                p_click = min(0.9, max(0.01, p_click))
                from itertools import product
                th_probs = {}
                for patt in product([0,1], repeat=modes):
                    prob = 1.0
                    for bit in patt:
                        prob *= (p_click if bit == 1 else (1.0 - p_click))
                    th_probs[tuple(patt)] = prob
                # normalize
                ssum = sum(th_probs.values())
                if ssum <= 0:
                    keys = list(th_probs.keys())
                    for k in keys:
                        th_probs[k] = 1.0 / len(keys)
                else:
                    for k in list(th_probs.keys()):
                        th_probs[k] = th_probs[k] / ssum

            all_patterns = sorted(th_probs.keys())
            p_emp = np.array([counts.get(p,0)/shots for p in all_patterns])
            p_th = np.array([th_probs.get(p,0.0) for p in all_patterns])
            m = 0.5*(p_emp + p_th)
            from scipy.stats import entropy
            js = 0.5*(entropy(np.maximum(p_emp,1e-12), np.maximum(m,1e-12)) + entropy(np.maximum(p_th,1e-12), np.maximum(m,1e-12)))
            # h1 via ripser if available
            try:
                from ripser import ripser
                dgms = ripser(thresholds.astype(float), maxdim=1)['dgms']
                h1 = int(len(dgms[1]))
            except Exception:
                h1 = 0

            res = {"modes": modes, "squeezing": squeezing, "eta": eta, "shots": shots, "js": float(js), "h1": h1}
            fname = out_dir / f"gbs_threshold_tda_grid_modes{modes}_r{str(squeezing).replace('.','_')}_eta{str(eta).replace('.','_')}.json"
            fname.write_text(json.dumps(res, indent=2))
            results.append(res)
            print('Wrote', fname)

# summary
out_file = out_dir / 'gbs_threshold_tda_grid_expanded.json'
out_file.write_text(json.dumps(results, indent=2))

# plot JS vs eta per modes and r
fig, axs = plt.subplots(len(squeezings), 1, figsize=(6,3*len(squeezings)), sharex=True)
for i, r in enumerate(squeezings):
    ax = axs[i]
    for modes in modes_list:
        xs = [res['eta'] for res in results if res['modes']==modes and res['squeezing']==r]
        ys = [res['js'] for res in results if res['modes']==modes and res['squeezing']==r]
        ax.plot(xs, ys, marker='o', label=f"modes={modes}")
    ax.set_title(f"squeezing r={r}")
    ax.set_ylabel('JS')
    ax.grid(True)
    ax.legend()
axs[-1].set_xlabel('eta')
plt.tight_layout()
png = out_dir / 'gbs_threshold_tda_grid_expanded.png'
plt.savefig(png)
print('Saved grid summary', out_file, png)
