#!/usr/bin/env python3
"""Mixed predictor: e* oddness + defect-mass coefficient vs flux winner changes."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "04_measurement"

ODDNESS = OUT_DIR / "e_star_oddness_per_line.csv"
RESPONSE = DATA / "_toe" / "flux_response_law_20260110" / "response_law_regression_coeffs_all40.csv"
GRID = DATA / "_toe" / "native_fullgrid_20260110" / "nativeC24_fullgrid_line_stabilities_flux_noflux.csv"


def zscore(x):
    mu = x.mean()
    sigma = x.std(ddof=0)
    if sigma == 0:
        return x * 0.0
    return (x - mu) / sigma


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    odd = pd.read_csv(ODDNESS)
    resp = pd.read_csv(RESPONSE)
    df = odd.merge(resp[["line_id", "coef_flux_def_mass"]], on="line_id", how="left")
    df["odd_z"] = zscore(df["odd_fraction"])
    df["def_mass_z"] = zscore(df["coef_flux_def_mass"])
    df["score"] = df["odd_z"] + df["def_mass_z"]

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
    win_df = win_df.merge(df[["line_id", "score"]], left_on="flux_winner", right_on="line_id", how="left")
    win_df = win_df.rename(columns={"score": "flux_score"}).drop(columns=["line_id"])
    win_df = win_df.merge(df[["line_id", "score"]], left_on="noflux_winner", right_on="line_id", how="left")
    win_df = win_df.rename(columns={"score": "noflux_score"}).drop(columns=["line_id"])
    win_df["flux_beats_noflux"] = (win_df["flux_score"] > win_df["noflux_score"]).astype(int)

    top5 = df.sort_values("score", ascending=False).head(5)["line_id"].tolist()
    win_df["flux_in_top5"] = win_df["flux_winner"].isin(top5).astype(int)
    win_df["noflux_in_top5"] = win_df["noflux_winner"].isin(top5).astype(int)

    overall_flux_beats = win_df["flux_beats_noflux"].mean()
    changed = win_df[win_df["winner_changed"] == 1]
    changed_flux_beats = changed["flux_beats_noflux"].mean() if not changed.empty else 0.0

    summary_path = OUT_DIR / "mixed_predictor_oddness_defect_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Mixed predictor: oddness + defect mass\n\n")
        f.write(f"Inputs:\n- {ODDNESS}\n- {RESPONSE}\n- {GRID}\n\n")
        f.write(f"- top5 lines by score: {top5}\n")
        f.write(f"- flux winner beats noflux score: {overall_flux_beats:.6f}\n")
        f.write(f"- flux winner beats noflux when winner changes: {changed_flux_beats:.6f}\n")
        f.write(f"- flux winners in top5: {win_df['flux_in_top5'].mean():.6f}\n")
        f.write(f"- noflux winners in top5: {win_df['noflux_in_top5'].mean():.6f}\n")

    df.to_csv(OUT_DIR / "mixed_predictor_oddness_defect_scores.csv", index=False)
    win_df.to_csv(OUT_DIR / "mixed_predictor_oddness_defect_grid.csv", index=False)


if __name__ == "__main__":
    main()
