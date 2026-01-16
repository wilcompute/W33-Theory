#!/usr/bin/env python3
"""Use e* parity on clock masks as a reduced predictor for flux winner changes."""

from __future__ import annotations

import ast
import csv
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "04_measurement"

MAP_PATH = DATA / "_workbench" / "05_symmetry" / "coin_c24_2t_alignment_mapping.csv"
TABLE_PATH = DATA / "_toe" / "projector_recon_20260110" / "binary_tetrahedral_2T_multiplication_table.csv"
MASKS_CSV = DATA / "_toe" / "projector_recon_20260110" / "W33_line_clock_projector_masks_20260109T210928Z.csv"
GRID_CSV = DATA / "_toe" / "native_fullgrid_20260110" / "nativeC24_fullgrid_line_stabilities_flux_noflux.csv"
FLUX_SUMMARY = DATA / "_toe" / "flux_response_rankings_20260110" / "line_flux_response_summary.csv"


def load_table():
    with TABLE_PATH.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        elems = [h.strip() for h in header[1:] if h.strip()]
        table = {}
        for row in reader:
            row_elem = row[0].strip()
            for col_elem, prod in zip(elems, row[1:]):
                table[(row_elem, col_elem)] = prod.strip()
    return elems, table


def load_mapping():
    coin_to_elem = {}
    with MAP_PATH.open("r", encoding="utf-8") as f:
        next(f)
        for line in f:
            idx, label = line.strip().split(",")
            coin_to_elem[int(idx)] = label
    elem_to_coin = {v: k for k, v in coin_to_elem.items()}
    return coin_to_elem, elem_to_coin


def e_star_pairs(table, coin_to_elem, elem_to_coin):
    pairs = []
    seen = set()
    for i in range(24):
        if i in seen:
            continue
        elem = coin_to_elem[i]
        prod = table[("e*", elem)]
        j = elem_to_coin[prod]
        if i == j:
            continue
        seen.add(i)
        seen.add(j)
        a, b = (i, j) if i < j else (j, i)
        pairs.append((a, b))
    pairs.sort()
    return pairs


def load_masks():
    df = pd.read_csv(MASKS_CSV)
    masks = {}
    for _, row in df.iterrows():
        line_id = int(row["w33_line_id"])
        ids = [int(x) for x in str(row["clock_state_ids"]).split()]
        masks[line_id] = set(ids)
    return masks


def odd_fraction(mask, pairs):
    odd = 0
    for a, b in pairs:
        in_a = a in mask
        in_b = b in mask
        if in_a != in_b:
            odd += 1
    return odd / len(pairs)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    elems, table = load_table()
    coin_to_elem, elem_to_coin = load_mapping()
    pairs = e_star_pairs(table, coin_to_elem, elem_to_coin)
    masks = load_masks()

    rows = []
    for line_id, mask in masks.items():
        rows.append({"line_id": line_id, "odd_fraction": odd_fraction(mask, pairs)})
    odd_df = pd.DataFrame(rows).sort_values("line_id")
    odd_df.to_csv(OUT_DIR / "e_star_oddness_per_line.csv", index=False)

    # Correlate with mean_abs_delta.
    flux = pd.read_csv(FLUX_SUMMARY)
    flux = flux.merge(odd_df, on="line_id", how="left")
    corr = flux["odd_fraction"].corr(flux["mean_abs_delta"])

    # Flux/noflux winners by gridpoint.
    grid = pd.read_csv(GRID_CSV)
    winners = []
    for (lam, mu), sub in grid.groupby(["lambda", "mu"]):
        sub = sub.sort_values("line_id")
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

    # Evaluate oddness predictor for winners.
    top_lines = (
        odd_df.sort_values("odd_fraction", ascending=False)
        .head(5)["line_id"]
        .tolist()
    )
    win_df["flux_winner_in_top5_odd"] = win_df["flux_winner"].isin(top_lines).astype(int)
    win_df["noflux_winner_in_top5_odd"] = win_df["noflux_winner"].isin(top_lines).astype(int)

    overall_flux_top5 = win_df["flux_winner_in_top5_odd"].mean()
    overall_noflux_top5 = win_df["noflux_winner_in_top5_odd"].mean()
    changed = win_df[win_df["winner_changed"] == 1]
    changed_flux_top5 = changed["flux_winner_in_top5_odd"].mean() if not changed.empty else 0.0

    win_df.to_csv(OUT_DIR / "e_star_oddness_winner_grid.csv", index=False)

    summary_path = OUT_DIR / "e_star_oddness_flux_winner_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# e* oddness predictor vs flux winners\n\n")
        f.write(f"Inputs:\n- {MASKS_CSV}\n- {GRID_CSV}\n- {FLUX_SUMMARY}\n- {MAP_PATH}\n\n")
        f.write(f"- corr(odd_fraction, mean_abs_delta): {corr:.6f}\n")
        f.write(f"- top5 oddness lines: {top_lines}\n\n")
        f.write("Winner overlap (top5 oddness lines):\n\n")
        f.write(f"- flux winners: {overall_flux_top5:.6f}\n")
        f.write(f"- noflux winners: {overall_noflux_top5:.6f}\n")
        f.write(f"- flux winners when winner changed: {changed_flux_top5:.6f}\n")


if __name__ == "__main__":
    main()
