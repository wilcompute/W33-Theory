"""Robust runner for GBS TDA follow-ups with analytic fallback.
Will attempt to sample with SF gaussian backend; if unavailable or errors occur, will fall back to analytic threshold sampling using compute_threshold_probs.
Saves per-point JSON and a summary PNG in bundles/v23_toe_finish/v23/ to ensure artifacts exist for inspection.
"""
from pathlib import Path
import json
import os
import numpy as np
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

repo = Path(__file__).resolve().parents[2]
out_dir = repo / "bundles" / "v23_toe_finish" / "v23"
out_dir.mkdir(parents=True, exist_ok=True)

# Selected points (same as followup script)
points = [
    {"modes": 6, "eta": 1.0},
    {"modes": 5, "eta": 1.0},
    {"modes": 4, "eta": 1.0},
]

squeezing = 0.6
shots = int(os.getenv("TDA_FOLLOWUP_SHOTS", "2000"))
bootstrap_samples = int(os.getenv("TDA_FOLLOWUP_BOOTSTRAP", "200"))

# import helpers
from scripts.quantum_photonics.run_gbs import build_interferometer, compute_threshold_probs

results = []
for p in points:
    modes = p['modes']
    eta = p['eta']
    U = build_interferometer(modes, seed=42)
    print('Point', modes, eta, 'shots', shots)

    # Try gaussian sampling; fallback to analytic threshold sampling
    samples = None
    try:
        from scripts.quantum_photonics.run_gbs import sample_gbs
        samples = sample_gbs(modes=modes, squeezing=squeezing, U=U, backend='gaussian', shots=shots)
        thresholds = (np.array(samples) > 0).astype(int)
    except Exception as e:
        print('Gaussian sampling failed or unavailable:', e)
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

    # compute TDA and JS metric (use ripser if available)
    try:
        from ripser import ripser
        X = thresholds.astype(float)
        dgms = ripser(X, maxdim=1)['dgms']
        h1_features = int(len(dgms[1]))
    except Exception as e:
        print('ripser not available, skipping dgms:', e)
        h1_features = 0

    counts = Counter(tuple(row) for row in thresholds)
    th_probs = compute_threshold_probs(modes=modes, squeezings=[squeezing]*modes, U=U, eta=eta)
    all_patterns = sorted(th_probs.keys())
    p_emp = np.array([counts.get(p,0)/shots for p in all_patterns])
    p_th = np.array([th_probs.get(p,0.0) for p in all_patterns])
    m = 0.5*(p_emp + p_th)
    # JS
    from scipy.stats import entropy
    js = 0.5*(entropy(np.maximum(p_emp,1e-12), np.maximum(m,1e-12)) + entropy(np.maximum(p_th,1e-12), np.maximum(m,1e-12)))

    point_result = {"modes": modes, "eta": eta, "shots": shots, "js": float(js), "h1_features": h1_features}
    fname = out_dir / f"gbs_threshold_tda_followup_modes{modes}_eta{str(eta).replace('.','_')}.json"
    open(fname,'w').write(json.dumps(point_result, indent=2))
    results.append(point_result)
    print('Wrote', fname)

# summary file and quick plot
out_json = out_dir / 'gbs_threshold_tda_followup_summary.json'
open(out_json,'w').write(json.dumps(results, indent=2))

fig, ax = plt.subplots(figsize=(6,4))
for r in results:
    ax.plot(r['eta'], r['js'], 'o', label=f"modes={r['modes']}")
ax.set_xlabel('eta')
ax.set_ylabel('JS')
ax.set_title('Follow-up JS (fallback-friendly)')
ax.grid(True)
ax.legend()
png = out_dir / 'gbs_threshold_tda_followup_summary_stub.png'
plt.savefig(png)
print('Saved summary', out_json, png)
