#!/usr/bin/env python3
"""Fit c_k(lambda, mu) surfaces for k=1..5 and evaluate prediction accuracy."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "04_measurement"

GRID_CSV = (
    DATA
    / "_toe"
    / "native_fullgrid_20260110"
    / "nativeC24_fullgrid_line_stabilities_flux_noflux.csv"
)


def load_grid():
    df = pd.read_csv(GRID_CSV)
    line_ids = sorted(df["line_id"].unique())
    grid = df[["lambda", "mu"]].drop_duplicates().sort_values(["lambda", "mu"])
    delta_rows = []
    flux_rows = []
    noflux_rows = []
    for _, row in grid.iterrows():
        sub = df[(df["lambda"] == row["lambda"]) & (df["mu"] == row["mu"])]
        sub = sub.set_index("line_id").loc[line_ids]
        delta_rows.append(sub["delta_stability"].to_numpy())
        flux_rows.append(sub["stability_flux"].to_numpy())
        noflux_rows.append(sub["stability_noflux"].to_numpy())
    return (
        np.vstack(delta_rows),
        np.vstack(flux_rows),
        np.vstack(noflux_rows),
        grid.reset_index(drop=True),
        line_ids,
    )


def design_matrix(lam, mu):
    return np.column_stack([np.ones_like(lam), lam, mu, lam**2, lam * mu, mu**2])


def fit_surfaces(C, lam, mu):
    X = design_matrix(lam, mu)
    coefs = []
    r2s = []
    C_hat = np.zeros_like(C)
    for k in range(C.shape[1]):
        y = C[:, k]
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        y_hat = X @ beta
        ss_res = float(np.sum((y - y_hat) ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot else 0.0
        coefs.append(beta)
        r2s.append(r2)
        C_hat[:, k] = y_hat
    return np.array(coefs), np.array(r2s), C_hat


def winner_accuracy(flux, noflux, delta_hat):
    pred_flux = noflux + delta_hat
    actual = np.argmax(flux, axis=1)
    pred = np.argmax(pred_flux, axis=1)
    return float(np.mean(actual == pred))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    D, flux, noflux, grid, line_ids = load_grid()
    U, s, Vt = np.linalg.svd(D, full_matrices=False)
    kmax = 5
    C = U[:, :kmax] * s[:kmax]

    lam = grid["lambda"].to_numpy()
    mu = grid["mu"].to_numpy()
    coefs, r2s, C_hat = fit_surfaces(C, lam, mu)

    delta_hat = C_hat @ Vt[:kmax]
    overall_rmse = float(np.sqrt(np.mean((D - delta_hat) ** 2)))
    winner_acc = winner_accuracy(flux, noflux, delta_hat)

    params_path = OUT_DIR / "response_surface_k1_5_params.csv"
    params = pd.DataFrame(
        coefs,
        columns=["c0", "c_lam", "c_mu", "c_lam2", "c_lam_mu", "c_mu2"],
    )
    params.insert(0, "mode_k", np.arange(1, kmax + 1))
    params["r2"] = r2s
    params.to_csv(params_path, index=False)

    coeffs_path = OUT_DIR / "response_surface_k1_5_grid_coeffs.csv"
    coeffs = grid.copy()
    for k in range(kmax):
        coeffs[f"c{k+1}"] = C[:, k]
        coeffs[f"c{k+1}_hat"] = C_hat[:, k]
    coeffs.to_csv(coeffs_path, index=False)

    err_path = OUT_DIR / "response_surface_k1_5_error.csv"
    err = grid.copy()
    err["rmse"] = np.sqrt(np.mean((D - delta_hat) ** 2, axis=1))
    err.to_csv(err_path, index=False)

    summary_path = OUT_DIR / "response_surface_k1_5_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Response surface fit (k=1..5)\n\n")
        f.write(f"Inputs:\n- {GRID_CSV}\n\n")
        f.write("Per-mode surface R^2:\n\n")
        f.write(params[["mode_k", "r2"]].to_markdown(index=False))
        f.write("\n\nOverall metrics:\n\n")
        f.write(f"- RMSE (delta): {overall_rmse:.6e}\n")
        f.write(f"- Winner accuracy: {winner_acc:.6f}\n")


if __name__ == "__main__":
    main()
