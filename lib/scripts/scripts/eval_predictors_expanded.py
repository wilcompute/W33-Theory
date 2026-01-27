"""Expanded predictor evaluation with permutations, BH-FDR, CV metrics and diagnostic plots.

Produces:
 - data/_docs/predictor_evaluation_expanded.csv
 - data/_docs/predictor_evaluation_expanded.md
 - data/_docs/figures/predictor_pvalue_hist.png
 - data/_docs/figures/nulldist_<predictor>_pearson.png (one per predictor)

Usage: python scripts/eval_predictors_expanded.py [--root <repo-root>] [--permutations N] [--seed S]
"""
from pathlib import Path
import argparse
import os
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')


def permutation_pvalue(obs, nulls, two_sided=True):
    if two_sided:
        return float((np.sum(np.abs(nulls) >= abs(obs)) + 1) / (len(nulls) + 1))
    else:
        return float((np.sum(nulls >= obs) + 1) / (len(nulls) + 1))


def bh_fdr(pvals):
    # Benjamini-Hochberg FDR adjustment (returns adjusted p-values)
    p = np.asarray(pvals)
    n = len(p)
    order = np.argsort(p)
    ranks = np.empty(n, int)
    ranks[order] = np.arange(1, n+1)
    q = p * n / ranks
    # enforce monotonicity
    q_adj = np.minimum.accumulate(q[::-1])[::-1]
    q_adj = np.clip(q_adj, 0, 1.0)
    return q_adj


def bootstrap_ci(stat_func, x, y, n_boot=500, alpha=0.05, seed=None):
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


def cv_r2(predictor, target, n_splits=5, seed=None):
    # Make sklearn optional: if unavailable, return NaN values for CV metrics
    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.model_selection import KFold
    except Exception:
        print('Warning: sklearn not available; returning NaN for CV R^2 metrics')
        return float('nan'), float('nan')
    X = predictor.reshape(-1, 1)
    y = target
    kf = KFold(n_splits=min(n_splits, len(y)), shuffle=True, random_state=seed)
    scores = []
    for tr, te in kf.split(X):
        try:
            model = LinearRegression()
            model.fit(X[tr], y[tr])
            r2 = model.score(X[te], y[te])
            scores.append(r2)
        except Exception:
            scores.append(np.nan)
    return float(np.nanmean(scores)), float(np.nanstd(scores))


def compute_stats(df, predictor, target, perms=1000, seed=None):
    rng = np.random.default_rng(seed)
    x = df[predictor].to_numpy(dtype=float)
    y = df[target].to_numpy(dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 3:
        return None
    x = x[mask]
    y = y[mask]
    # observed
    try:
        pear_obs = pearsonr(x, y)[0]
    except Exception:
        pear_obs = np.nan
    try:
        spear_obs = spearmanr(x, y).correlation
    except Exception:
        spear_obs = np.nan
    # permutation nulls
    nulls_pear = np.zeros(perms)
    nulls_spear = np.zeros(perms)
    for i in range(perms):
        xp = rng.permutation(x)
        try:
            nulls_pear[i] = pearsonr(xp, y)[0]
        except Exception:
            nulls_pear[i] = np.nan
        try:
            nulls_spear[i] = spearmanr(xp, y).correlation
        except Exception:
            nulls_spear[i] = np.nan
    p_pear = permutation_pvalue(pear_obs, nulls_pear)
    p_spear = permutation_pvalue(spear_obs, nulls_spear)
    pear_ci = bootstrap_ci(lambda a, b: pearsonr(a, b)[0], x, y, n_boot=200, alpha=0.05, seed=seed)
    spear_ci = bootstrap_ci(lambda a, b: spearmanr(a, b).correlation, x, y, n_boot=200, alpha=0.05, seed=seed)
    cv_mean, cv_std = cv_r2(x, y, n_splits=5, seed=seed)
    return {
        'predictor': predictor,
        'n': int(mask.sum()),
        'pearson': float(pear_obs),
        'pearson_p': float(p_pear),
        'pearson_ci_lo': pear_ci[0],
        'pearson_ci_hi': pear_ci[1],
        'spearman': float(spear_obs),
        'spearman_p': float(p_spear),
        'spearman_ci_lo': spear_ci[0],
        'spearman_ci_hi': spear_ci[1],
        'cv_r2_mean': cv_mean,
        'cv_r2_std': cv_std,
        'nulls_pear': nulls_pear,
        'nulls_spear': nulls_spear,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str, default=None)
    parser.add_argument('--permutations', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    repo_root = Path(args.root) if args.root else (Path(os.environ.get('TOE_ROOT')) if os.environ.get('TOE_ROOT') else Path(__file__).resolve().parents[1])
    docs = repo_root / 'data' / '_docs'
    figs = docs / 'figures'
    figs.mkdir(parents=True, exist_ok=True)
    key_lines = docs / 'toe_key_lines.csv'
    out_csv = docs / 'predictor_evaluation_expanded.csv'
    out_md = docs / 'predictor_evaluation_expanded.md'

    if not key_lines.exists():
        raise SystemExit(f"Missing {key_lines}; run scripts/generate_toe_key_lines.py first")
    df = pd.read_csv(key_lines, encoding='utf-8-sig')
    target = 'native_mean_abs_delta'
    possible_predictors = ['node_commutator_score', 'mixed_score', 'e_star_oddness', 'prior_score', 'fit_score']

    results = []
    nulls_store = {}
    for p in possible_predictors:
        if p in df.columns:
            stats = compute_stats(df, p, target, perms=args.permutations, seed=args.seed)
            if stats:
                nulls_store[p] = stats['nulls_pear']
                # remove the heavy arrays from the result we plan to write to CSV
                stats_simple = {k: v for k, v in stats.items() if not k.startswith('nulls_')}
                results.append(stats_simple)

    if not results:
        raise SystemExit('No predictors found in toe_key_lines.csv')

    out_df = pd.DataFrame(results)
    # adjust p-values with BH-FDR
    out_df['pearson_p_adj'] = bh_fdr(out_df['pearson_p'].fillna(1.0).to_numpy())
    out_df['spearman_p_adj'] = bh_fdr(out_df['spearman_p'].fillna(1.0).to_numpy())

    out_df.to_csv(out_csv, index=False)

    # plots: p-value histogram
    plt.figure(figsize=(6,4))
    plt.hist(out_df['pearson_p'].dropna(), bins=20, alpha=0.8)
    plt.title('Pearson p-value histogram')
    plt.xlabel('p-value')
    plt.ylabel('count')
    ph = figs / 'predictor_pvalue_hist.png'
    plt.savefig(ph, bbox_inches='tight')
    plt.close()

    # null distributions for pearson per predictor
    for p, nulls in nulls_store.items():
        plt.figure(figsize=(6,4))
        valid = nulls[~np.isnan(nulls)]
        if valid.size > 0:
            sns.histplot(valid, bins=30, kde=True)
        plt.title(f'Null distribution (pearson) for {p}')
        plt.xlabel('pearson')
        out = figs / f'null_{p}_pearson.png'
        plt.savefig(out, bbox_inches='tight')
        plt.close()

    # write markdown summary
    with out_md.open('w', encoding='utf-8') as f:
        f.write('# Expanded predictor evaluation (permutation tests + BH-FDR + CV)\n\n')
        f.write(f'Inputs: {key_lines}\n\n')
        for _, row in out_df.iterrows():
            f.write(f"- **{row['predictor']}** (n={int(row['n'])}): pearson={row['pearson']:.4f} (p={row['pearson_p']:.4f}, adj={row['pearson_p_adj']:.4f}, CI={row['pearson_ci_lo']:.3f}..{row['pearson_ci_hi']:.3f}), spearman={row['spearman']:.4f} (p={row['spearman_p']:.4f}, adj={row['spearman_p_adj']:.4f}) CV R^2={row['cv_r2_mean']:.3f} (sd={row['cv_r2_std']:.3f})\n")

    print('Wrote', out_csv)
    print('Wrote', out_md)
    print('Wrote', ph)


if __name__ == '__main__':
    main()
