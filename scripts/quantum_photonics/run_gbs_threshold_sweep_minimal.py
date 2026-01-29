"""Minimal quick sweep (modes 2-3 only) to produce fast reliable outputs."""
import json
import numpy as np
from pathlib import Path
from collections import Counter
from scipy.stats import entropy
from scripts.quantum_photonics.run_gbs import build_interferometer, sample_gbs, compute_threshold_probs

repo = Path(__file__).resolve().parents[2]
out_json = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'gbs_threshold_sweep_minimal.json'
out_png = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'gbs_threshold_js_vs_eta_minimal.png'

modes_list = [2,3]
squeezings = [0.6]
shots = 2000
etas = [0.4,0.6,0.8,0.9,1.0]
results = []
for squeezing in squeezings:
    for modes in modes_list:
        U = build_interferometer(modes, seed=42)
        for eta in etas:
            print(f'RUN start: modes={modes} r={squeezing} eta={eta} shots={shots}')
            samples_gauss = sample_gbs(modes=modes, squeezing=squeezing, U=U, backend='gaussian', shots=shots)
            thresholds_emp = np.array(samples_gauss) > 0
            counts = Counter(tuple(row.astype(int)) for row in thresholds_emp)
            th_probs = compute_threshold_probs(modes=modes, squeezings=[squeezing]*modes, U=U, eta=eta)
            all_patterns = sorted(th_probs.keys())
            p_emp = np.array([counts.get(p,0)/shots for p in all_patterns])
            p_th = np.array([th_probs.get(p,0.0) for p in all_patterns])
            m = 0.5*(p_emp + p_th)
            js = 0.5*(entropy(np.maximum(p_emp,1e-12), np.maximum(m,1e-12)) + entropy(np.maximum(p_th,1e-12), np.maximum(m,1e-12)))
            topk = counts.most_common(10)
            results.append({'modes': modes, 'squeezing': squeezing, 'eta': eta, 'shots': shots, 'js': float(js), 'top_patterns': [(list(k), int(v), v/shots) for k,v in topk]})
            print('RUN done:', modes, squeezing, eta, 'js', js)

out_json.parent.mkdir(parents=True, exist_ok=True)
open(out_json,'w').write(json.dumps(results, indent=2))

# plot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1,1,figsize=(6,4))
for modes in modes_list:
    xs = [r['eta'] for r in results if r['modes']==modes]
    ys = [r['js'] for r in results if r['modes']==modes]
    ax.plot(xs, ys, marker='o', label=f'modes={modes}')
ax.set_xlabel('eta')
ax.set_ylabel('JS')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig(out_png)
print('Saved', out_png)
print('Wrote', out_json)
