"""Expanded TDA grid sweep for GBS threshold samples.
Grid: modes 2-6, etas [0.4,0.6,0.8,0.9,1.0], fixed squeezing 0.6 by default.
Adaptive shots: try baseline shots, reduce on keyboard interrupt / timeouts to keep runs tractable.
Computes persistence diagrams (ripser), JS divergence, H1 Wasserstein between neighboring etas, and saves results and plots.
"""
import json
from pathlib import Path
import numpy as np
from collections import Counter
from ripser import ripser
from persim import wasserstein
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import entropy
from scripts.quantum_photonics.run_gbs import build_interferometer, sample_gbs, compute_threshold_probs

repo = Path(__file__).resolve().parents[2]
out_json = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'gbs_threshold_tda_grid.json'
out_png1 = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'gbs_threshold_tda_grid_js_vs_eta.png'
out_png2 = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'gbs_threshold_tda_grid_w_vs_js.png'

import os

modes_list = [2,3,4,5,6]
squeezing = 0.6
# Allow overriding base shots via environment for quick exploratory runs
base_shots = int(os.getenv('TDA_BASE_SHOTS', '1000'))
etas = [0.4, 0.6, 0.8, 0.9, 1.0]

results = []
# helper to compute JS

def js_divergence(p_emp, p_th):
    m = 0.5 * (p_emp + p_th)
    return float(0.5 * (entropy(np.maximum(p_emp, 1e-12), np.maximum(m, 1e-12)) + entropy(np.maximum(p_th, 1e-12), np.maximum(m, 1e-12))))

for modes in modes_list:
    print('mode', modes)
    U = build_interferometer(modes, seed=42)
    dgms_by_eta = {}
    js_by_eta = {}
    h1_counts = {}
    for eta in etas:
        shots = base_shots
        while True:
            try:
                print(f'  sampling modes={modes} eta={eta} shots={shots}')
                samples = sample_gbs(modes=modes, squeezing=squeezing, U=U, backend='gaussian', shots=shots)
                thresholds = (np.array(samples) > 0).astype(int)
                X = thresholds.astype(float)
                dgms = ripser(X, maxdim=1)['dgms']
                counts = Counter(tuple(row) for row in thresholds)
                th_probs = compute_threshold_probs(modes=modes, squeezings=[squeezing] * modes, U=U, eta=eta)
                all_patterns = sorted(th_probs.keys())
                p_emp = np.array([counts.get(p, 0) / shots for p in all_patterns])
                p_th = np.array([th_probs.get(p, 0.0) for p in all_patterns])
                js = js_divergence(p_emp, p_th)
                dgms_by_eta[eta] = dgms
                js_by_eta[eta] = js
                h1_counts[eta] = int(len(dgms[1]))
                results.append({'modes': modes, 'eta': eta, 'shots': shots, 'js': js, 'h1_features': int(len(dgms[1]))})
                break
            except KeyboardInterrupt:
                # if user interrupts, reduce shots and continue
                shots = max(100, shots // 2)
                print('    interrupted: reducing shots to', shots)
            except Exception as e:
                # on other errors, reduce shots and try once
                print('    error sampling ({}), reducing shots and retrying'.format(e))
                shots = max(100, shots // 2)
                if shots <= 100:
                    print('    too small shots; recording failure and continuing')
                    results.append({'modes': modes, 'eta': eta, 'shots': shots, 'error': str(e)})
                    break

    # compute pairwise Wasserstein between neighboring etas for H1
    ws = {}
    for i in range(len(etas)-1):
        a, b = etas[i], etas[i+1]
        try:
            w = wasserstein(dgms_by_eta[a][1], dgms_by_eta[b][1], matching=False)
        except Exception:
            w = None
        ws[f'{a}-{b}'] = w
    results.append({'modes': modes, 'wasserstein_h1_pairs': ws})

# save
out_json.parent.mkdir(parents=True, exist_ok=True)
open(out_json, 'w').write(json.dumps(results, indent=2))

# Plot JS vs eta per mode
fig, ax = plt.subplots(figsize=(8,6))
for modes in modes_list:
    sub = [r for r in results if r.get('modes')==modes and 'eta' in r]
    xs = [r['eta'] for r in sub]
    ys = [r['js'] for r in sub]
    ax.plot(xs, ys, marker='o', label=f'modes={modes}')
ax.set_xlabel('eta')
ax.set_ylabel('JS divergence')
ax.set_title('TDA grid: JS vs eta (modes)')
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.savefig(out_png1)

# scatter Wasserstein (avg neighboring) vs JS (avg) per mode
w_vals = []
js_vals = []
for modes in modes_list:
    sub = [r for r in results if r.get('modes')==modes and 'eta' in r]
    if not sub:
        continue
    rs_sorted = sorted(sub, key=lambda r: r['eta'])
    ds = []
    for i in range(len(rs_sorted)-1):
        pair_key = f"{rs_sorted[i]['eta']}-{rs_sorted[i+1]['eta']}"
        # find wasserstein entry
        w_entry = next((s for s in results if s.get('modes')==modes and 'wasserstein_h1_pairs' in s), None)
        if w_entry:
            ds.extend([v for k,v in w_entry['wasserstein_h1_pairs'].items() if v is not None])
    w_mean = float(np.mean(ds)) if ds else 0.0
    j_mean = float(np.mean([r['js'] for r in sub]))
    w_vals.append(w_mean); js_vals.append(j_mean)

fig, ax = plt.subplots(figsize=(6,5))
ax.scatter(w_vals, js_vals)
for i,m in enumerate(modes_list):
    ax.annotate(f'modes={m}', (w_vals[i], js_vals[i]))
ax.set_xlabel('avg Wasserstein (H1)')
ax.set_ylabel('avg JS')
ax.set_title('Wasserstein vs JS per mode')
ax.grid(True)
plt.tight_layout()
plt.savefig(out_png2)
print('Saved outputs:', out_json, out_png1, out_png2)
