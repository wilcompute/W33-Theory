#!/usr/bin/env python3
"""Predict flux-sensitive lines from commutator-hot nodes + projective images."""

from __future__ import annotations

import ast
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "04_measurement"

NODE_WEIGHTS = (
    DATA
    / "_workbench"
    / "05_symmetry"
    / "transport_commutator_node_localization_summary.csv"
)
EDGE_IMAGES = (
    DATA / "_toe" / "coupling_20260110" / "orbit0_edges_with_projective_images.csv"
)
LINES = DATA / "_toe" / "coupling_20260110" / "W33_lines_to_projective_quartets.csv"
FLUX_SUMMARY = (
    DATA / "_toe" / "flux_response_rankings_20260110" / "line_flux_response_summary.csv"
)
GRID = (
    DATA
    / "_toe"
    / "native_fullgrid_20260110"
    / "nativeC24_fullgrid_line_stabilities_flux_noflux.csv"
)


def node_class_counts(edges: pd.DataFrame, class_cols: list[str]) -> pd.DataFrame:
    nodes = pd.Index(sorted(set(edges["u"]).union(edges["v"])))
    classes = sorted(
        {cls for col in class_cols for cls in edges[col].dropna().unique()}
    )
    counts = pd.DataFrame(0, index=nodes, columns=classes, dtype=float)

    for _, row in edges.iterrows():
        u = int(row["u"])
        v = int(row["v"])
        for col in class_cols:
            cls = row[col]
            if pd.isna(cls):
                continue
            counts.at[u, cls] += 1.0
            counts.at[v, cls] += 1.0

    counts = counts.reset_index().rename(columns={"index": "node"})
    return counts


def class_weights_from_nodes(
    node_counts: pd.DataFrame, node_weights: pd.DataFrame
) -> pd.Series:
    df = node_counts.merge(node_weights[["node", "mean"]], on="node", how="left")
    df["mean"] = df["mean"].fillna(0.0)
    class_cols = [c for c in df.columns if c not in {"node", "mean"}]
    weights = {}
    for cls in class_cols:
        denom = df[cls].sum()
        if denom == 0:
            weights[cls] = 0.0
        else:
            weights[cls] = (df[cls] * df["mean"]).sum() / denom
    return pd.Series(weights, name="class_weight")


def load_lines() -> pd.DataFrame:
    lines = pd.read_csv(LINES)
    lines["proj_list"] = lines["proj_list"].apply(ast.literal_eval)
    return lines


def line_scores(lines: pd.DataFrame, class_weights: pd.Series) -> pd.DataFrame:
    rows = []
    for _, row in lines.iterrows():
        line_id = int(row["line_id"])
        classes = row["proj_list"]
        score = sum(class_weights.get(cls, 0.0) for cls in classes)
        score = score / len(classes) if classes else 0.0
        rows.append({"line_id": line_id, "score": score})
    return pd.DataFrame(rows).sort_values("line_id")


def winner_grid(scores: pd.DataFrame) -> pd.DataFrame:
    grid = pd.read_csv(GRID)
    winners = []
    for (lam, mu), sub in grid.groupby(["lambda", "mu"]):
        flux_winner = int(sub.loc[sub["stability_flux"].idxmax(), "line_id"])
        noflux_winner = int(sub.loc[sub["stability_noflux"].idxmax(), "line_id"])
        winners.append(
            {
                "lambda": lam,
                "mu": mu,
                "flux_winner": flux_winner,
                "noflux_winner": noflux_winner,
                "winner_changed": int(flux_winner != noflux_winner),
            }
        )
    win_df = pd.DataFrame(winners)
    win_df = win_df.merge(scores, left_on="flux_winner", right_on="line_id", how="left")
    win_df = win_df.rename(columns={"score": "flux_score"}).drop(columns=["line_id"])
    win_df = win_df.merge(
        scores, left_on="noflux_winner", right_on="line_id", how="left"
    )
    win_df = win_df.rename(columns={"score": "noflux_score"}).drop(columns=["line_id"])
    win_df["flux_beats_noflux"] = (
        win_df["flux_score"] > win_df["noflux_score"]
    ).astype(int)
    return win_df


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    edges = pd.read_csv(EDGE_IMAGES)
    class_cols = [c for c in edges.columns if c.startswith("img_sec")]
    node_counts = node_class_counts(edges, class_cols)
    node_weights = pd.read_csv(NODE_WEIGHTS)
    class_weights = class_weights_from_nodes(node_counts, node_weights)

    lines = load_lines()
    scores = line_scores(lines, class_weights)
    scores.to_csv(OUT_DIR / "node_commutator_line_scores.csv", index=False)
    class_weights.rename("weight").to_csv(
        OUT_DIR / "node_commutator_projective_class_weights.csv", header=True
    )

    flux = pd.read_csv(FLUX_SUMMARY)
    joined = flux.merge(scores, on="line_id", how="left")
    pearson = joined["score"].corr(joined["mean_abs_delta"])
    spearman = joined["score"].corr(joined["mean_abs_delta"], method="spearman")

    win_df = winner_grid(scores)
    win_df.to_csv(OUT_DIR / "node_commutator_winner_grid.csv", index=False)

    top5 = scores.sort_values("score", ascending=False).head(5)["line_id"].tolist()
    win_df["flux_in_top5"] = win_df["flux_winner"].isin(top5).astype(int)
    win_df["noflux_in_top5"] = win_df["noflux_winner"].isin(top5).astype(int)

    summary_path = OUT_DIR / "node_commutator_predictor_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Node-commutator projective predictor\n\n")
        f.write("Inputs:\n")
        f.write(f"- {NODE_WEIGHTS}\n")
        f.write(f"- {EDGE_IMAGES}\n")
        f.write(f"- {LINES}\n")
        f.write(f"- {FLUX_SUMMARY}\n")
        f.write(f"- {GRID}\n\n")
        f.write(f"- corr(score, mean_abs_delta) pearson: {pearson:.6f}\n")
        f.write(f"- corr(score, mean_abs_delta) spearman: {spearman:.6f}\n")
        f.write(f"- top5 lines by score: {top5}\n")
        f.write(f"- flux winners in top5: {win_df['flux_in_top5'].mean():.6f}\n")
        f.write(f"- noflux winners in top5: {win_df['noflux_in_top5'].mean():.6f}\n")
        f.write(
            f"- flux winner beats noflux score: {win_df['flux_beats_noflux'].mean():.6f}\n"
        )
        changed = win_df[win_df["winner_changed"] == 1]
        changed_rate = changed["flux_beats_noflux"].mean() if not changed.empty else 0.0
        f.write(f"- flux beats noflux when winner changes: {changed_rate:.6f}\n")


if __name__ == "__main__":
    main()
