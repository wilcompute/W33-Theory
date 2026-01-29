"""Compute enrichment of various repetend properties across residue classes and other partitions.
Saves summary CSV/JSON and a heatmap PNG for PR-ready figures.
"""
from pathlib import Path
import csv
import json
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import fisher_exact

repo = Path(__file__).resolve().parents[2]
repetend_csv = repo / 'data' / 'repetend_scan' / 'repetend_scan_10000.csv'
out_dir = repo / 'data' / 'repetend_scan'
out_dir.mkdir(parents=True, exist_ok=True)

# properties to check
PROPERTY_FUNCS = {
    'full_repetend': lambda r: bool(int(r['full_repetend'])),
    'eq6': lambda r: int(r['repetend']) == 6,
    'div6': lambda r: (int(r['repetend'])>0 and int(r['repetend']) % 6 == 0),
    'div12': lambda r: (int(r['repetend'])>0 and int(r['repetend']) % 12 == 0),
    'div24': lambda r: (int(r['repetend'])>0 and int(r['repetend']) % 24 == 0),
    'div192': lambda r: (int(r['repetend'])>0 and int(r['repetend']) % 192 == 0),
}

# partitions to test: residue classes mod 12 and mod 24
PARTITIONS = {
    'mod12': list(range(12)),
    'mod24': list(range(24)),
}

# load rows
rows = []
with repetend_csv.open('r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        rows.append(row)

# helper to compute contingency and fisher p/odds

def fisher_for_partition(prop_fn, partition_key, partition_value, rows):
    # a = count where in partition and prop true
    # b = in partition and prop false
    # c = not in partition and prop true
    # d = not in partition and prop false
    a = b = c = d = 0
    for r in rows:
        in_part = int(r[partition_key]) == partition_value
        prop = bool(prop_fn(r))
        if in_part and prop:
            a += 1
        elif in_part and not prop:
            b += 1
        elif not in_part and prop:
            c += 1
        else:
            d += 1
    # avoid degenerate cases
    if (a + b) == 0 or (c + d) == 0:
        return {'a':a,'b':b,'c':c,'d':d,'odds':None,'p':None}
    try:
        odds, p = fisher_exact([[a,b],[c,d]])
    except Exception:
        odds, p = None, None
    return {'a':a,'b':b,'c':c,'d':d,'odds':odds,'p':p}

# run sweep and collect matrix of p-values and odds
results = {}
for part, values in PARTITIONS.items():
    results[part] = {}
    for val in values:
        results[part][val] = {}
        for pname, pfun in PROPERTY_FUNCS.items():
            res = fisher_for_partition(pfun, part, val, rows)
            results[part][val][pname] = res

# write JSON summary
out_json = out_dir / 'repetend_enrichment_sweep_10000.json'
out_json.write_text(json.dumps(results, indent=2, default=lambda x: (x if isinstance(x,(int,float)) else str(x))))

# build heatmaps: for each partition, matrix props x residues of -log10(p) (cap) and odds
for part, valmap in results.items():
    propnames = list(PROPERTY_FUNCS.keys())
    vals = sorted(valmap.keys())
    pmat = np.zeros((len(propnames), len(vals)))
    omat = np.zeros((len(propnames), len(vals)))
    for i,p in enumerate(propnames):
        for j,v in enumerate(vals):
            r = valmap[v][p]
            pval = r['p']
            odds = r['odds']
            if pval is None:
                pmat[i,j] = 0.0
            else:
                # -log10 p, cap at 50
                try:
                    pmat[i,j] = min(-np.log10(pval) if pval>0 else 50.0, 50.0)
                except Exception:
                    pmat[i,j] = 0.0
            omat[i,j] = odds if odds is not None else 0.0
    # save CSVs
    import csv
    csvp = out_dir / f'enrichment_pvals_{part}_10000.csv'
    with csvp.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['property'] + vals)
        for i,p in enumerate(propnames):
            w.writerow([p] + list(pmat[i,:].tolist()))
    csvp2 = out_dir / f'enrichment_odds_{part}_10000.csv'
    with csvp2.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['property'] + vals)
        for i,p in enumerate(propnames):
            w.writerow([p] + list(omat[i,:].tolist()))

    # plot heatmap of p-values
    plt.figure(figsize=(max(6, len(vals)*0.3), max(2, len(propnames)*0.6)))
    im = plt.imshow(pmat, aspect='auto', cmap='viridis')
    plt.colorbar(im, label='-log10(p) (capped 50)')
    plt.yticks(range(len(propnames)), propnames)
    plt.xticks(range(len(vals)), vals, rotation=90)
    plt.title(f'Enrichment -log10(p) {part} (d up to 10000)')
    plt.tight_layout()
    pngp = out_dir / f'enrichment_pval_heatmap_{part}_10000.png'
    plt.savefig(pngp)
    plt.close()

print('Wrote enrichment JSON and heatmaps to', out_dir)