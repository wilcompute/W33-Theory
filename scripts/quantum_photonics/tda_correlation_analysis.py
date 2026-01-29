"""Compute correlations between JS and Wasserstein from TDA outputs.
Uses grid results and high-precision results if available. Saves JSON summary and PNG scatter with regression.
"""
import json
from pathlib import Path
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

repo = Path(__file__).resolve().parents[2]
bundle = repo / 'bundles' / 'v23_toe_finish' / 'v23'
gridf = bundle / 'gbs_threshold_tda_grid.json'
highprec = bundle / 'gbs_threshold_tda_highprec.json'
out_json = bundle / 'gbs_tda_correlation_summary.json'
out_png = bundle / 'gbs_tda_w_vs_js_correlation.png'

# load grid
grid = json.load(open(gridf))
# aggregate per-mode
modes = sorted(set([r['modes'] for r in grid if 'modes' in r and 'eta' in r]))
data = []
for m in modes:
    sub = [r for r in grid if r.get('modes')==m and 'eta' in r]
    if not sub:
        continue
    js_vals = [r['js'] for r in sub]
    js_mean = float(np.mean(js_vals))
    # wasserstein entries
    w_entry = next((r for r in grid if r.get('modes')==m and 'wasserstein_h1_pairs' in r), None)
    ws = []
    if w_entry:
        for k,v in w_entry['wasserstein_h1_pairs'].items():
            if v is not None:
                ws.append(v)
    w_mean = float(np.mean(ws)) if ws else 0.0
    data.append({'modes': m, 'js_mean': js_mean, 'w_mean': w_mean, 'js_vals': js_vals, 'w_vals': ws})

# correlation
js_arr = np.array([d['js_mean'] for d in data])
w_arr = np.array([d['w_mean'] for d in data])
pearson = pearsonr(w_arr, js_arr) if len(data)>1 else (None,None)
spearman = spearmanr(w_arr, js_arr) if len(data)>1 else (None,None)

summary = {'n_modes': len(data), 'pearson': {'r': float(pearson[0]) if pearson[0] is not None else None, 'p': float(pearson[1]) if pearson[1] is not None else None}, 'spearman': {'rho': float(spearman[0]) if spearman[0] is not None else None, 'p': float(spearman[1]) if spearman[1] is not None else None}, 'data': data}
open(out_json,'w').write(json.dumps(summary, indent=2))

# plot
plt.figure(figsize=(6,5))
plt.scatter(w_arr, js_arr)
for i,d in enumerate(data):
    plt.annotate(f"m={d['modes']}", (w_arr[i], js_arr[i]))
plt.xlabel('avg Wasserstein (H1)')
plt.ylabel('avg JS')
plt.title('Average Wasserstein vs average JS across modes')
plt.grid(True)
plt.tight_layout()
plt.savefig(out_png)
print('Wrote', out_json, out_png)
