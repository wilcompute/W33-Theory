"""Compute decimal repetend statistics for denominators up to N.
Saves JSON and CSV outputs and a couple of PNG visualizations.
Usage: python scripts/number_theory/run_repetend_scan.py --max-den 1000
"""

import argparse
import csv
import json
from math import gcd
from pathlib import Path

import matplotlib
import numpy as np
from sympy import totient

matplotlib.use("Agg")
import matplotlib.pyplot as plt

out_dir = Path("data/repetend_scan")
out_dir.mkdir(parents=True, exist_ok=True)


def repetend_length(d):
    n = d
    while n % 2 == 0:
        n //= 2
    while n % 5 == 0:
        n //= 5
    if n == 1:
        return 0
    # multiplicative order of 10 modulo n
    t = 1
    r = 10 % n
    seen = set()
    while r != 1:
        r = (r * 10) % n
        t += 1
        if t > 10 * n:
            return None
    return t


def analyze(max_den=1000):
    rows = []
    for d in range(1, max_den + 1):
        rl = repetend_length(d)
        n = d
        while n % 2 == 0:
            n //= 2
        while n % 5 == 0:
            n //= 5
        full = False
        if n > 1 and rl is not None:
            full = rl == totient(n)
        rows.append(
            {
                "d": d,
                "repetend": rl if rl is not None else -1,
                "mod12": d % 12,
                "mod24": d % 24,
                "mod192": d % 192,
                "full_repetend": full,
            }
        )
    return rows


def save_rows(rows, max_den):
    jsonp = out_dir / f"repetend_scan_{max_den}.json"
    csvp = out_dir / f"repetend_scan_{max_den}.csv"
    jsonp.write_text(json.dumps(rows, indent=2))
    with csvp.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["d", "repetend", "mod12", "mod24", "mod192", "full_repetend"])
        for r in rows:
            w.writerow(
                [
                    r["d"],
                    r["repetend"],
                    r["mod12"],
                    r["mod24"],
                    r["mod192"],
                    int(r["full_repetend"]),
                ]
            )
    return jsonp, csvp


def make_plots(rows, max_den):
    repetends = [
        r["repetend"] for r in rows if r["repetend"] is not None and r["repetend"] >= 0
    ]
    plt.figure(figsize=(6, 4))
    plt.hist(repetends, bins=40)
    plt.xlabel("Repetend length")
    plt.ylabel("Count")
    plt.title(f"Repetend length histogram up to {max_den}")
    p1 = out_dir / f"repetend_hist_{max_den}.png"
    plt.tight_layout()
    plt.savefig(p1)
    plt.close()

    # distribution of full repetends by mod12
    from collections import Counter

    fulls = [r for r in rows if r["full_repetend"]]
    by12 = Counter([r["mod12"] for r in fulls])
    labels = sorted(by12.keys())
    vals = [by12[k] for k in labels]
    plt.figure(figsize=(6, 3))
    plt.bar(labels, vals)
    plt.xlabel("d mod 12 (full repetend denominators)")
    plt.ylabel("Count")
    plt.title(f"Full repetends by residue mod12 up to {max_den}")
    p2 = out_dir / f"full_repetend_mod12_{max_den}.png"
    plt.tight_layout()
    plt.savefig(p2)
    plt.close()

    return p1, p2


def enrichment_tests(rows):
    from collections import Counter

    import numpy as np

    # e.g., are residues 10,11 overrepresented among full repetends?
    fulls = [r for r in rows if r["full_repetend"]]
    cnt_full = Counter([r["mod12"] for r in fulls])
    cnt_all = Counter([r["mod12"] for r in rows if r["repetend"] > 0])
    res = []
    for residue in sorted(set(cnt_all.keys())):
        a = cnt_full.get(residue, 0)
        b = cnt_all.get(residue, 0) - a
        c = len(fulls) - a
        d = len([r for r in rows if r["repetend"] > 0]) - len(fulls) - b
        # Fisher exact test
        try:
            from scipy.stats import fisher_exact

            odds, p = fisher_exact([[a, b], [c, d]])
        except Exception:
            odds, p = None, None
        res.append(
            {
                "residue": residue,
                "full_count": a,
                "all_count": cnt_all.get(residue, 0),
                "odds_ratio": odds,
                "pvalue": p,
            }
        )
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-den", type=int, default=1000)
    args = parser.parse_args()
    rows = analyze(args.max_den)
    j, csvp = save_rows(rows, args.max_den)
    p1, p2 = make_plots(rows, args.max_den)
    enrich = enrichment_tests(rows)
    out = {
        "json": str(j),
        "csv": str(csvp),
        "hist": str(p1),
        "mod12_plot": str(p2),
        "enrichment": enrich,
    }
    outp = out_dir / f"repetend_summary_{args.max_den}.json"
    outp.write_text(json.dumps(out, indent=2))
    print("Wrote", outp)


if __name__ == "__main__":
    main()
