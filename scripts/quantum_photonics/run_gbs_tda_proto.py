"""Quick TDA prototype for GBS samples.
Computes persistence diagrams for threshold point clouds at small shots
and writes a JSON summary to bundles/v23_toe_finish/v23/gbs_threshold_tda_runtime.json
"""
from ripser import ripser
from persim import wasserstein
import numpy as np
from collections import Counter
from pathlib import Path
from scripts.quantum_photonics.run_gbs import build_interferometer, sample_gbs, compute_threshold_probs
from scipy.stats import entropy
import json

repo = Path(__file__).resolve().parents[2]
out = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'gbs_threshold_tda_runtime.json'

modes = 3
squeezing = 0.6
shots = 300
etas = [0.4, 0.6, 0.8, 1.0]
results = []
for eta in etas:
    U = build_interferometer(modes, seed=42)
    samples = sample_gbs(modes=modes, squeezing=squeezing, U=U, backend='gaussian', shots=shots)
    thresholds = (np.array(samples) > 0).astype(int)
    X = thresholds.astype(float)
    dgms = ripser(X, maxdim=1)['dgms']
    counts = Counter(tuple(row) for row in thresholds)
    th_probs = compute_threshold_probs(modes=modes, squeezings=[squeezing] * modes, U=U, eta=eta)
    all_patterns = sorted(th_probs.keys())
    p_emp = np.array([counts.get(p, 0) / shots for p in all_patterns])
    p_th = np.array([th_probs.get(p, 0.0) for p in all_patterns])
    m = 0.5 * (p_emp + p_th)
    js = 0.5 * (entropy(np.maximum(p_emp, 1e-12), np.maximum(m, 1e-12)) + entropy(np.maximum(p_th, 1e-12), np.maximum(m, 1e-12)))
    results.append({'modes': modes, 'eta': eta, 'js': float(js), 'dgm_h1_len': int(len(dgms[1]))})
    print('modes', modes, 'eta', eta, 'js', js, 'H1 features', len(dgms[1]))

# example wasserstein between first and last
if len(etas) >= 2:
    U = build_interferometer(modes, seed=42)
    dg0 = ripser((np.array(sample_gbs(modes=modes, squeezing=squeezing, U=U, backend='gaussian', shots=shots) > 0).astype(int).astype(float)), maxdim=1)['dgms'][1]
    dg1 = dgms[1]
    try:
        w = wasserstein(dg0, dg1, matching=False)
    except Exception:
        w = None
    print('Example wasserstein (H1):', w)

out.parent.mkdir(parents=True, exist_ok=True)
open(out, 'w').write(json.dumps(results, indent=2))
print('Wrote', out)
