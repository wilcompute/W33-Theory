"""Link repetend statistics to tomotope invariants and residue classes.
Saves JSON summary and a heatmap PNG for quick inspection.
"""

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import fisher_exact

repo = Path(__file__).resolve().parents[2]
repetend_csv = repo / "data" / "repetend_scan" / "repetend_scan_10000.csv"
tomotope_summary = (
    repo / "data" / "maniplex_tables" / "tomotope_permutation_summary.json"
)
out_dir = repo / "data" / "repetend_scan"
out_dir.mkdir(parents=True, exist_ok=True)

# load repetend table
rows = []
with repetend_csv.open("r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for row in r:
        d = int(row["d"])
        repetend = int(row["repetend"])
        rows.append(
            {
                "d": d,
                "repetend": repetend,
                "mod12": int(row["mod12"]),
                "mod24": int(row["mod24"]),
                "mod192": int(row["mod192"]),
                "full_repetend": bool(int(row["full_repetend"])),
            }
        )

# load tomotope info
try:
    tom = json.loads(tomotope_summary.read_text(encoding="utf-8"))
    tom_group_size = tom.get("group_size")
    tom_orbit_sizes = (
        {int(k): len(v) for k, v in tom.get("orbits", {}).items()}
        if "orbits" in tom
        else {}
    )
except Exception:
    tom = {}
    tom_group_size = None
    tom_orbit_sizes = {}

# properties to test
for r in rows:
    r["repetend_div12"] = r["repetend"] > 0 and r["repetend"] % 12 == 0
    r["repetend_eq6"] = r["repetend"] == 6

# aggregate by residue mod12
residues = sorted(set(r["mod12"] for r in rows))
summary = {"by_residue": {}}
for res in residues:
    subset = [r for r in rows if r["mod12"] == res and r["repetend"] > 0]
    n = len(subset)
    if n == 0:
        continue
    div12 = sum(1 for r in subset if r["repetend_div12"])
    eq6 = sum(1 for r in subset if r["repetend_eq6"])
    fulls = sum(1 for r in subset if r["full_repetend"])
    summary["by_residue"][res] = {
        "n": n,
        "div12": int(div12),
        "eq6": int(eq6),
        "fulls": int(fulls),
        "fraction_div12": div12 / n,
        "fraction_eq6": eq6 / n,
        "fraction_full": fulls / n,
    }

# Fisher tests: for each residue, test enrichment of div12 vs other residues
all_div12 = sum(1 for r in rows if r["repetend"] > 0 and r["repetend_div12"])
all_pos = sum(1 for r in rows if r["repetend"] > 0)
fisher_results = {}
for res in residues:
    a = summary["by_residue"].get(res, {}).get("div12", 0)
    b = summary["by_residue"].get(res, {}).get("n", 0) - a
    c = all_div12 - a
    d = all_pos - all_div12 - b
    if (a + b) == 0 or (c + d) == 0:
        fisher_results[res] = {"odds": None, "p": None}
    else:
        odds, p = fisher_exact([[a, b], [c, d]])
        fisher_results[res] = {"odds": odds, "p": p}

# Save summary
out = {
    "tomotope_group_size": tom_group_size,
    "by_residue": summary["by_residue"],
    "fisher_div12": fisher_results,
}
outp = out_dir / "repetend_tomotope_correlation_10000.json"
outp.write_text(json.dumps(out, indent=2))

# heatmap: fraction_div12 by residue
labels = sorted(summary["by_residue"].keys())
vals = [summary["by_residue"][r]["fraction_div12"] for r in labels]
plt.figure(figsize=(6, 3))
plt.bar(labels, vals)
plt.xlabel("residue mod 12")
plt.ylabel("fraction with repetend divisible by 12")
plt.title("Fraction div-by-12 by residue (d up to 10000)")
plt.tight_layout()
pngp = out_dir / "div12_fraction_by_residue_10000.png"
plt.savefig(pngp)

print("Wrote", outp, pngp)
