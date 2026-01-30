"""Produce consolidated GBS-TDA report: read per-point followup JSONs and grid JSON (if present), make plots, and write a short Markdown summary in docs/GBS_TDA_RESULTS.md."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

repo = Path(__file__).resolve().parents[2]
out_dir = repo / 'bundles' / 'v23_toe_finish' / 'v23'
report_dir = repo / 'docs'
report_dir.mkdir(parents=True, exist_ok=True)

# collect followup files
followup_files = sorted(out_dir.glob('gbs_threshold_tda_followup_modes*_eta*.json'))
followups = []
for f in followup_files:
    try:
        j = json.load(open(f))
        followups.append(j)
    except Exception:
        continue

# grid
grid_file = out_dir / 'gbs_threshold_tda_grid_expanded.json'
grid = []
if grid_file.exists():
    try:
        grid = json.load(open(grid_file))
    except Exception:
        grid = []

# Make plots if we have followups
if followups:
    modes = [int(r['modes']) for r in followups]
    js = [float(r['js']) for r in followups]
    h1 = [int(r.get('h1_features', r.get('h1', 0))) for r in followups]

    fig, ax1 = plt.subplots(figsize=(6,4))
    ax1.plot(modes, js, 'o-', label='JS')
    ax1.set_xlabel('modes')
    ax1.set_ylabel('JS divergence')
    ax2 = ax1.twinx()
    ax2.plot(modes, h1, 's--', color='orange', label='H1 features')
    ax2.set_ylabel('H1 features')
    fig.tight_layout()
    png = out_dir / 'gbs_tda_followup_js_h1_summary.png'
    plt.savefig(png)
else:
    png = None

# grid summary plot (if grid loaded)
grid_png = None
if grid:
    # compute mean JS for each (modes, squeezing)
    from collections import defaultdict
    agg = defaultdict(list)
    for r in grid:
        agg[(r['modes'], r['squeezing'])].append(r['js'])
    # plot: for each r, JS vs modes
    squeezings = sorted({k[1] for k in agg.keys()})
    fig, axs = plt.subplots(len(squeezings), 1, figsize=(6, 3*len(squeezings)), sharex=True)
    if len(squeezings)==1:
        axs=[axs]
    for i, r in enumerate(squeezings):
        ax = axs[i]
        for m in sorted({k[0] for k in agg.keys()}):
            xs = [r for (mm, rr) in agg.keys() if rr==r and mm==m]
            ys = agg[(m, r)]
            # plot at a single x=m using mean
            ax.plot(m, np.mean(ys), 'o', label=f'modes={m}')
        ax.set_title(f'squeezing r={r}')
        ax.set_ylabel('mean JS')
        ax.grid(True)
    axs[-1].set_xlabel('modes')
    grid_png = out_dir / 'gbs_tda_grid_js_summary.png'
    plt.tight_layout()
    plt.savefig(grid_png)

# write markdown summary
md = report_dir / 'GBS_TDA_RESULTS.md'
with open(md, 'w') as f:
    f.write('# GBS / TDA Results Summary\n\n')
    if followups:
        f.write('## Follow-up per-point results\n\n')
        f.write('| modes | eta | shots | JS | H1 |\n')
        f.write('|---:|---:|---:|---:|---:|\n')
        for r in sorted(followups, key=lambda x: (x['modes'])):
            f.write(f"| {r['modes']} | {r['eta']} | {r['shots']} | {r['js']:.6f} | {r.get('h1_features', r.get('h1',0))} |\n")
        if png:
            f.write('\n![](../bundles/v23_toe_finish/v23/' + png.name + ')\n')
    if grid:
        f.write('\n## Grid summary (expanded)\n\n')
        f.write(f'Grid points: {len(grid)}\n\n')
        if grid_png:
            f.write('\n![](../bundles/v23_toe_finish/v23/' + grid_png.name + ')\n')

print('Wrote report', md)
