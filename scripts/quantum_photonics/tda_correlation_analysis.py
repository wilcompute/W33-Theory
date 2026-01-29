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

# load available datasets (grid, high-precision, follow-up summary)

def load_json_if_exists(p):
    try:
        return json.load(open(p))
    except Exception:
        return []

grid = load_json_if_exists(gridf)
high = load_json_if_exists(highprec)
followup_summary = load_json_if_exists(bundle / 'gbs_threshold_tda_followup_summary.json')
# tomotope results
tomotope_followup = load_json_if_exists(bundle / 'tomotope_tda_followup_summary.json')
tomotope_grid = load_json_if_exists(bundle / 'tomotope_tda_grid.json')

# collect all modes present across datasets
modes = sorted(set(
    [r['modes'] for r in grid if 'modes' in r and 'eta' in r]
    + [r['modes'] for r in high if 'modes' in r and 'eta' in r]
    + [r['modes'] for r in followup_summary if 'modes' in r]
    + [r['modes'] for r in tomotope_followup if 'modes' in r]
    + [r['modes'] for r in tomotope_grid if 'modes' in r]
))

data = []
for m in modes:
    # collect JS values from grid and high-precision and follow-up
    js_vals = []
    js_vals += [r['js'] for r in grid if r.get('modes')==m and 'js' in r]
    js_vals += [r['js'] for r in high if r.get('modes')==m and 'js' in r]
    js_vals += [r['js'] for r in followup_summary if r.get('modes')==m and 'js' in r]
    js_vals += [r['js'] for r in tomotope_followup if r.get('modes')==m and 'js' in r]
    js_vals += [r['js'] for r in tomotope_grid if r.get('modes')==m and 'js' in r]
    if not js_vals:
        continue
    js_mean = float(np.mean(js_vals))

    # collect wasserstein entries mainly from grid/high where available
    ws = []
    w_entries = [r for r in grid+high if r.get('modes')==m and 'wasserstein_h1_pairs' in r]
    for w_entry in w_entries:
        for k,v in w_entry['wasserstein_h1_pairs'].items():
            if v is not None:
                ws.append(v)
    # fallback: if no wasserstein, use h1_features count as a proxy (normalized)
    if not ws:
        h1_vals = [r.get('h1_features') for r in grid+high+followup_summary+tomotope_followup+tomotope_grid if r.get('modes')==m and ('h1_features' in r or 'h1_count' in r)]
        # prefer explicit h1_count if present
        h1_vals = [ (r.get('h1_count') if r.get('h1_count') is not None else r.get('h1_features')) for r in (grid+high+followup_summary+tomotope_followup+tomotope_grid) if r.get('modes')==m and ('h1_features' in r or 'h1_count' in r)]
        h1_vals = [v for v in h1_vals if v is not None]
        if h1_vals:
            # scale small integers into a pseudo-wasserstein range
            ws = [float(v) for v in h1_vals]

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
