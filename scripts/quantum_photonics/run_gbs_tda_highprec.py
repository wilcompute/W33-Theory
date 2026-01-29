"""High-precision TDA sweep for GBS threshold samples.
Runs small grid of (modes,eta) with larger shot counts, computes persistence
(diagrams), JS divergence, H1 Wasserstein between neighboring etas, and
bootstrap confidence intervals for JS.

Writes results to bundles/v23_toe_finish/v23/gbs_threshold_tda_highprec.json
and produces some diagnostic PNGs.
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
out_json = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'gbs_threshold_tda_highprec.json'
out_png = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'gbs_threshold_tda_highprec.png'

modes_list = [3,4,5]
shots = 2000
squeezing = 0.6
etas = [0.6, 0.8]
bootstrap_samples = 100

results = []
for modes in modes_list:
    U = build_interferometer(modes, seed=42)
    dgms_by_eta = {}
    js_by_eta = {}
    boot_js_ci = {}
    for eta in etas:
        print('Running modes', modes, 'eta', eta)
        samples = sample_gbs(modes=modes, squeezing=squeezing, U=U, backend='gaussian', shots=shots)
        thresholds = (np.array(samples) > 0).astype(int)
        X = thresholds.astype(float)
        dgms = ripser(X, maxdim=1)['dgms']
        dgms_by_eta[eta] = dgms
        counts = Counter(tuple(row) for row in thresholds)
        th_probs = compute_threshold_probs(modes=modes, squeezings=[squeezing]*modes, U=U, eta=eta)
        all_patterns = sorted(th_probs.keys())
        p_emp = np.array([counts.get(p,0)/shots for p in all_patterns])
        p_th = np.array([th_probs.get(p,0.0) for p in all_patterns])
        m = 0.5*(p_emp + p_th)
        js = 0.5*(entropy(np.maximum(p_emp,1e-12), np.maximum(m,1e-12)) + entropy(np.maximum(p_th,1e-12), np.maximum(m,1e-12)))
        js_by_eta[eta] = float(js)
        # bootstrap JS by resampling empirical counts
        boot_js = []
        patterns = np.array(all_patterns)
        emp_counts = np.array([counts.get(tuple(p),0) for p in all_patterns])
        for b in range(bootstrap_samples):
            draw = np.random.multinomial(shots, emp_counts/np.maximum(emp_counts.sum(),1))
            p_emp_b = draw / shots
            m_b = 0.5*(p_emp_b + p_th)
            js_b = 0.5*(entropy(np.maximum(p_emp_b,1e-12), np.maximum(m_b,1e-12)) + entropy(np.maximum(p_th,1e-12), np.maximum(m_b,1e-12)))
            boot_js.append(js_b)
        lo = float(np.percentile(boot_js, 2.5))
        hi = float(np.percentile(boot_js, 97.5))
        boot_js_ci[eta] = (lo, hi)
        results.append({'modes': modes, 'eta': eta, 'js': float(js), 'js_ci': [lo, hi], 'h1_features': int(len(dgms[1]))})

    # compute Wasserstein between the two etas for H1
    if len(etas) >= 2:
        a, b = etas[0], etas[1]
        try:
            w = wasserstein(dgms_by_eta[a][1], dgms_by_eta[b][1], matching=False)
        except Exception:
            w = None
        results.append({'modes': modes, 'wasserstein_h1_between_etas': w})

# save outputs
out_json.parent.mkdir(parents=True, exist_ok=True)
open(out_json, 'w').write(json.dumps(results, indent=2))

# simple summary plot: JS with CI vs eta for each mode
fig, ax = plt.subplots(figsize=(6,4))
for modes in modes_list:
    sub = [r for r in results if r.get('modes')==modes and 'eta' in r]
    xs = [r['eta'] for r in sub]
    ys = [r['js'] for r in sub]
    yslo = [r['js_ci'][0] for r in sub]
    yshi = [r['js_ci'][1] for r in sub]
    ax.errorbar(xs, ys, yerr=[np.array(ys)-np.array(yslo), np.array(yshi)-np.array(ys)], marker='o', label=f'modes={modes}')
ax.set_xlabel('eta')
ax.set_ylabel('JS divergence')
ax.set_title('High-precision TDA sweep: JS with bootstrap CIs')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig(out_png)
print('Saved', out_json, out_png)
print('Done')
