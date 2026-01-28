"""Evaluate predictor signals against native sensitivity with permutation tests.

Produces:
 - data/_docs/predictor_evaluation.csv
 - data/_docs/predictor_evaluation.md

Usage: python scripts/eval_predictors.py [--root <repo-root>] [--permutations N] [--seed S]
"""

import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr


def permutation_pvalue(obs, nulls, two_sided=True):
    # obs: observed statistic (float)
    # nulls: array of null statistics
    if two_sided:
        return float((np.sum(np.abs(nulls) >= abs(obs)) + 1) / (len(nulls) + 1))
    else:
        return float((np.sum(nulls >= obs) + 1) / (len(nulls) + 1))


def bootstrap_ci(stat_func, x, y, n_boot=1000, alpha=0.05, seed=None):
    rng = np.random.default_rng(seed)
    stats = []
    n = len(x)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        try:
            stats.append(stat_func(x[idx], y[idx]))
        except Exception:
            stats.append(np.nan)
    stats = np.array(stats)
    lo = np.nanpercentile(stats, 100 * (alpha / 2.0))
    hi = np.nanpercentile(stats, 100 * (1 - alpha / 2.0))
    return float(lo), float(hi)


def compute_stats(df, predictor, target, perms=1000, seed=None):
    rng = np.random.default_rng(seed)
    x = df[predictor].to_numpy(dtype=float)
    y = df[target].to_numpy(dtype=float)
    # handle NaNs
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 3:
        return None
    x = x[mask]
    y = y[mask]
    pear_obs = pearsonr(x, y)[0]
    spear_obs = spearmanr(x, y).correlation
    # permutation nulls (shuffle x)
    nulls_pear = np.zeros(perms)
    nulls_spear = np.zeros(perms)
    for i in range(perms):
        xp = rng.permutation(x)
        nulls_pear[i] = pearsonr(xp, y)[0]
        nulls_spear[i] = spearmanr(xp, y).correlation
    p_pear = permutation_pvalue(pear_obs, nulls_pear)
    p_spear = permutation_pvalue(spear_obs, nulls_spear)
    pear_ci = bootstrap_ci(
        lambda a, b: pearsonr(a, b)[0], x, y, n_boot=200, alpha=0.05, seed=seed
    )
    spear_ci = bootstrap_ci(
        lambda a, b: spearmanr(a, b).correlation,
        x,
        y,
        n_boot=200,
        alpha=0.05,
        seed=seed,
    )
    return {
        "predictor": predictor,
        "n": int(mask.sum()),
        "pearson": float(pear_obs),
        "pearson_p": float(p_pear),
        "pearson_ci_lo": pear_ci[0],
        "pearson_ci_hi": pear_ci[1],
        "spearman": float(spear_obs),
        "spearman_p": float(p_spear),
        "spearman_ci_lo": spear_ci[0],
        "spearman_ci_hi": spear_ci[1],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, default=None)
    parser.add_argument("--permutations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    repo_root = (
        Path(args.root)
        if args.root
        else (
            Path(os.environ.get("TOE_ROOT"))
            if os.environ.get("TOE_ROOT")
            else Path(__file__).resolve().parents[1]
        )
    )
    docs = repo_root / "data" / "_docs"
    key_lines = docs / "toe_key_lines.csv"
    out_csv = docs / "predictor_evaluation.csv"
    out_md = docs / "predictor_evaluation.md"
    if not key_lines.exists():
        raise SystemExit(
            f"Missing {key_lines}; run scripts/generate_toe_key_lines.py first"
        )
    df = pd.read_csv(key_lines, encoding="utf-8-sig")
    target = "native_mean_abs_delta"
    possible_predictors = [
        "node_commutator_score",
        "mixed_score",
        "e_star_oddness",
        "prior_score",
        "fit_score",
    ]
    results = []
    for p in possible_predictors:
        if p in df.columns:
            stats = compute_stats(
                df, p, target, perms=args.permutations, seed=args.seed
            )
            if stats:
                results.append(stats)
    if not results:
        raise SystemExit("No predictors found in toe_key_lines.csv")
    out_df = pd.DataFrame(results)
    out_df.to_csv(out_csv, index=False)
    # Write short markdown
    with out_md.open("w", encoding="utf-8") as f:
        f.write("# Predictor evaluation (permutation tests)\n\n")
        f.write(f"Inputs: {key_lines}\n\n")
        for _, row in out_df.iterrows():
            f.write(
                f"- **{row['predictor']}** (n={int(row['n'])}): pearson={row['pearson']:.4f} (p={row['pearson_p']:.4f}, CI={row['pearson_ci_lo']:.3f}..{row['pearson_ci_hi']:.3f}), spearman={row['spearman']:.4f} (p={row['spearman_p']:.4f}, CI={row['spearman_ci_lo']:.3f}..{row['spearman_ci_hi']:.3f})\n"
            )
    print("Wrote", out_csv)
    print("Wrote", out_md)


if __name__ == "__main__":
    main()
