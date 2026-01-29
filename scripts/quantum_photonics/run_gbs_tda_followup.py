"""High-precision follow-up on selected parameter points.
Runs specified (modes, eta) pairs with higher shots and bootstrap for JS CI.
Saves per-point JSON and a small summary JSON and PNGs.
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
out_dir = repo / 'bundles' / 'v23_toe_finish' / 'v23'
out_dir.mkdir(parents=True, exist_ok=True)

# Selected parameter points
points = [
    {'modes': 6, 'eta': 1.0},
    {'modes': 5, 'eta': 1.0},
    {'modes': 4, 'eta': 1.0},
]

import os
squeezing = 0.6
shots = int(os.getenv('TDA_FOLLOWUP_SHOTS', '5000'))
bootstrap_samples = int(os.getenv('TDA_FOLLOWUP_BOOTSTRAP', '500'))
results = []

for p in points:
    modes = p['modes']
    eta = p['eta']
    print('Running follow-up: modes', modes, 'eta', eta, 'shots', shots)
    U = build_interferometer(modes, seed=42)
    # adaptive sampling: try with full shots, reduce on error/timeout
    cur_shots = shots
    sampling_error = None
    while cur_shots >= 100:
        try:
            samples = sample_gbs(modes=modes, squeezing=squeezing, U=U, backend='gaussian', shots=cur_shots)
            thresholds = (np.array(samples) > 0).astype(int)
            X = thresholds.astype(float)
            dgms = ripser(X, maxdim=1)['dgms']
            counts = Counter(tuple(row) for row in thresholds)
            th_probs = compute_threshold_probs(modes=modes, squeezings=[squeezing]*modes, U=U, eta=eta)
            all_patterns = sorted(th_probs.keys())
            p_emp = np.array([counts.get(pat,0)/cur_shots for pat in all_patterns])
            p_th = np.array([th_probs.get(pat,0.0) for pat in all_patterns])
            m = 0.5*(p_emp + p_th)
            js = 0.5*(entropy(np.maximum(p_emp,1e-12), np.maximum(m,1e-12)) + entropy(np.maximum(p_th,1e-12), np.maximum(m,1e-12)))
            break
        except KeyboardInterrupt:
            print('    interrupted during sampling; reducing shots', cur_shots, '->', max(100, cur_shots//2))
            cur_shots = max(100, cur_shots // 2)
        except Exception as e:
            sampling_error = str(e)
            print('    sampling error:', e, '- reducing shots and retrying')
            cur_shots = max(100, cur_shots // 2)
    else:
        # failed to sample
        point_result = {'modes': modes, 'eta': eta, 'shots': cur_shots, 'error': sampling_error}
        fname = out_dir / f"gbs_threshold_tda_followup_modes{modes}_eta{str(eta).replace('.', '_')}.json"
        open(fname, 'w').write(json.dumps(point_result, indent=2))
        results.append(point_result)
        print('Sampling ultimately failed; wrote', fname)
        continue

    # bootstrap JS (reduced to keep time reasonable)
    boot_js = []
    emp_counts = np.array([counts.get(tuple(pat),0) for pat in all_patterns])
    emp_probs = emp_counts / np.maximum(emp_counts.sum(), 1)
    for b in range(min(200, bootstrap_samples)):
        draw = np.random.multinomial(cur_shots, emp_probs)
        p_emp_b = draw / cur_shots
        m_b = 0.5*(p_emp_b + p_th)
        js_b = 0.5*(entropy(np.maximum(p_emp_b,1e-12), np.maximum(m_b,1e-12)) + entropy(np.maximum(p_th,1e-12), np.maximum(m_b,1e-12)))
        boot_js.append(js_b)
    lo = float(np.percentile(boot_js, 2.5))
    hi = float(np.percentile(boot_js, 97.5))

    # save point-level JSON
    point_result = {'modes': modes, 'eta': eta, 'shots': shots, 'js': float(js), 'js_ci': [lo, hi], 'h1_features': int(len(dgms[1]))}
    fname = out_dir / f"gbs_threshold_tda_followup_modes{modes}_eta{str(eta).replace('.', '_')}.json"
    open(fname, 'w').write(json.dumps(point_result, indent=2))
    results.append(point_result)
    print('Wrote', fname)

# summary
out_json = out_dir / 'gbs_threshold_tda_followup_summary.json'
open(out_json, 'w').write(json.dumps(results, indent=2))

# plot
fig, ax = plt.subplots(figsize=(6,4))
for r in results:
    ax.errorbar(r['eta'], r['js'], yerr=[[r['js']-r['js_ci'][0]],[r['js_ci'][1]-r['js']]], fmt='o', label=f"modes={r['modes']}")
ax.set_xlabel('eta')
ax.set_ylabel('JS')
ax.set_title('Follow-up JS with bootstrap CI')
ax.grid(True)
ax.legend()
plt.tight_layout()
png = out_dir / 'gbs_threshold_tda_followup_summary.png'
plt.savefig(png)
print('Saved summary', out_json, png)
