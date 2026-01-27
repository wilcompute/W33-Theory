"""Generate figures from data/_docs/toe_key_lines.csv and save to data/_docs/figures/"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')
import os
import argparse

repo_root = Path(__file__).resolve().parents[1]
# Allow overriding the repo root for tests: CLI --root then TOE_ROOT env var
vparser = argparse.ArgumentParser(add_help=False)
vparser.add_argument('--root', type=str, default=None)
vargs, _ = vparser.parse_known_args()
if vargs.root:
    repo_root = Path(vargs.root).resolve()
else:
    env_root = os.environ.get('TOE_ROOT')
    if env_root:
        repo_root = Path(env_root).resolve()

key_lines = repo_root / 'data' / '_docs' / 'toe_key_lines.csv'
fig_dir = repo_root / 'data' / '_docs' / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)

if not key_lines.exists():
    print(f"ERROR: {key_lines} does not exist. Run scripts/generate_toe_key_lines.py first.")
    raise SystemExit(1)

print('Loading', key_lines)
df = pd.read_csv(key_lines, encoding='utf-8-sig')
print('Read', len(df), 'rows')

# Boxplot: mean_abs_delta by unique_k_mod6
if 'mean_abs_delta' in df.columns and 'unique_k_mod6' in df.columns:
    plt.figure(figsize=(6,4))
    sns.boxplot(x='unique_k_mod6', y='mean_abs_delta', data=df)
    plt.title('mean_abs_delta by unique_k_mod6')
    out = fig_dir / 'mean_abs_delta_by_kmod6.png'
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    print('Wrote', out)

# Scatter: native_mean_abs_delta vs prior_score
if 'native_mean_abs_delta' in df.columns and 'prior_score' in df.columns:
    plt.figure(figsize=(6,4))
    s = df.get('node_commutator_score')
    sizes = (s.fillna(s.mean())*200).clip(20,300) if s is not None else 40
    sns.scatterplot(x='native_mean_abs_delta', y='prior_score', hue=df.get('in_top_native', False), size=sizes, data=df)
    plt.title('prior_score vs native_mean_abs_delta')
    out = fig_dir / 'prior_vs_native_scatter.png'
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    print('Wrote', out)

# Histogram: k12_entropy
if 'k12_entropy' in df.columns:
    plt.figure(figsize=(6,4))
    sns.histplot(df['k12_entropy'].dropna(), bins=30, kde=True)
    plt.title('k12_entropy distribution')
    out = fig_dir / 'k12_entropy_hist.png'
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    print('Wrote', out)

# Small summary CSV
summary = {}
summary['n_rows'] = len(df)
summary['mean_abs_delta_mean'] = float(df['mean_abs_delta'].mean()) if 'mean_abs_delta' in df.columns else None
summary['k12_entropy_mean'] = float(df['k12_entropy'].mean()) if 'k12_entropy' in df.columns else None
pd.DataFrame([summary]).to_csv(repo_root / 'data' / '_docs' / 'toe_key_lines_summary.csv', index=False)
print('Wrote summary CSV')
