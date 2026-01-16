#!/usr/bin/env python3
"""Extend topology alignment to modes 4–5 (pairwise kernels vs H1 pairings)."""

from __future__ import annotations

import ast
import json
import math
import random
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "04_measurement"

GRID_CSV = DATA / "_toe" / "native_fullgrid_20260110" / "nativeC24_fullgrid_line_stabilities_flux_noflux.csv"
LINES_CSV = DATA / "_toe" / "coupling_20260110" / "W33_lines_to_projective_quartets.csv"
MASKS_NPZ = DATA / "_toe" / "projector_recon_20260110" / "TOE_W33_clock_projector_masks_20260109T210928Z.npz"
H1_JSON = DATA / "_n12" / "n12_58_orbit_cup_analysis.json"


def load_delta_matrix():
    df = pd.read_csv(GRID_CSV)
    line_ids = sorted(df["line_id"].unique())
    grid = df[["lambda", "mu"]].drop_duplicates().sort_values(["lambda", "mu"])
    vectors = []
    for _, row in grid.iterrows():
        sub = df[(df["lambda"] == row["lambda"]) & (df["mu"] == row["mu"])]
        sub = sub.set_index("line_id").loc[line_ids]
        vectors.append(sub["delta_stability"].to_numpy())
    D = np.vstack(vectors)
    return D, grid.reset_index(drop=True), line_ids


def load_projective_classes():
    npz = np.load(MASKS_NPZ, allow_pickle=True)
    classes = [str(x) for x in npz["projective_classes"]]
    return classes


def load_line_quartets(classes):
    df = pd.read_csv(LINES_CSV)
    class_index = {c: i for i, c in enumerate(classes)}
    line_to_classes = {}
    for _, row in df.iterrows():
        line_id = int(row["line_id"])
        proj_list = ast.literal_eval(row["proj_list"])
        line_to_classes[line_id] = [class_index[c] for c in proj_list]
    return line_to_classes


def build_design(line_ids, line_to_classes, n_classes):
    pairs = [(i, j) for i in range(n_classes) for j in range(i + 1, n_classes)]
    X = np.zeros((len(line_ids), 1 + len(pairs)), dtype=float)
    X[:, 0] = 1.0
    for r, line_id in enumerate(line_ids):
        idxs = sorted(line_to_classes[line_id])
        for i, j in pairs:
            if i in idxs and j in idxs:
                X[r, 1 + pairs.index((i, j))] = 1.0
    return X, pairs


def fit_pairwise_kernel(v, X, pairs, n_classes):
    beta, _, _, _ = np.linalg.lstsq(X, v, rcond=None)
    alpha = float(beta[0])
    K = np.zeros((n_classes, n_classes), dtype=float)
    for (i, j), w in zip(pairs, beta[1:]):
        K[i, j] = w
        K[j, i] = w
    v_hat = X @ beta
    ss_res = float(np.sum((v - v_hat) ** 2))
    ss_tot = float(np.sum((v - v.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot else 0.0
    return alpha, K, r2


def corr_upper(a, b):
    iu = np.triu_indices_from(a, k=1)
    x = a[iu]
    y = b[iu]
    if np.allclose(x, x[0]) or np.allclose(y, y[0]):
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def best_alignment(K, B, n_perm=8000, seed=7):
    rng = random.Random(seed)
    n = K.shape[0]
    best = None
    best_p = None
    for _ in range(n_perm):
        perm = list(range(n))
        rng.shuffle(perm)
        P = B[np.ix_(perm, perm)]
        c = corr_upper(K, P)
        if best is None or abs(c) > abs(best):
            best = c
            best_p = perm
    # Local swap refinement.
    improved = True
    while improved:
        improved = False
        for i in range(n):
            for j in range(i + 1, n):
                perm = best_p[:]
                perm[i], perm[j] = perm[j], perm[i]
                P = B[np.ix_(perm, perm)]
                c = corr_upper(K, P)
                if abs(c) > abs(best) + 1e-9:
                    best = c
                    best_p = perm
                    improved = True
    return best, best_p


def baseline_max(K, B, n_perm=2000, seed=11):
    rng = random.Random(seed)
    n = K.shape[0]
    best = None
    for _ in range(n_perm):
        perm = list(range(n))
        rng.shuffle(perm)
        P = B[np.ix_(perm, perm)]
        c = corr_upper(K, P)
        if best is None or abs(c) > abs(best):
            best = c
    return best


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    D, grid, line_ids = load_delta_matrix()
    U, s, Vt = np.linalg.svd(D, full_matrices=False)

    classes = load_projective_classes()
    line_to_classes = load_line_quartets(classes)
    X, pairs = build_design(line_ids, line_to_classes, len(classes))

    with open(H1_JSON, "r", encoding="utf-8") as f:
        h1 = json.load(f)
    J = np.array(h1["intersection_form_J_on_H1"], dtype=float)
    Umat = np.array(h1["cohomology"]["cup_product_matrix_U"], dtype=float)

    rows = []
    baseline_rows = []
    for mode_k in (4, 5):
        v = Vt[mode_k - 1]
        alpha, K, r2 = fit_pairwise_kernel(v, X, pairs, len(classes))

        best_J, perm_J = best_alignment(K, J)
        best_U, perm_U = best_alignment(K, Umat)
        base_J = baseline_max(K, J)
        base_U = baseline_max(K, Umat)

        rows.append(
            {
                "mode_k": mode_k,
                "pairwise_r2": r2,
                "best_corr_J": best_J,
                "best_corr_U": best_U,
                "perm_J": " ".join(map(str, perm_J)),
                "perm_U": " ".join(map(str, perm_U)),
            }
        )
        baseline_rows.append(
            {
                "mode_k": mode_k,
                "baseline_max_abs_corr_J": base_J,
                "baseline_max_abs_corr_U": base_U,
            }
        )

        # Save kernel weights.
        out_csv = OUT_DIR / f"nativeC24_mode{mode_k}_pairwise_kernel.csv"
        with out_csv.open("w", encoding="utf-8") as f:
            f.write("class_a,class_b,weight\n")
            for (i, j) in pairs:
                f.write(f"{classes[i]},{classes[j]},{K[i, j]}\n")

        # Save mapping for best J and U alignments.
        map_J = OUT_DIR / f"mode{mode_k}_best_alignment_to_J.csv"
        map_U = OUT_DIR / f"mode{mode_k}_best_alignment_to_U.csv"
        with map_J.open("w", encoding="utf-8") as f:
            f.write("class_label,h1_index\n")
            for i, p in enumerate(perm_J):
                f.write(f"{classes[i]},{p}\n")
        with map_U.open("w", encoding="utf-8") as f:
            f.write("class_label,h1_index\n")
            for i, p in enumerate(perm_U):
                f.write(f"{classes[i]},{p}\n")

    summary_csv = OUT_DIR / "topology_alignment_modes45_summary.csv"
    pd.DataFrame(rows).to_csv(summary_csv, index=False)

    baseline_csv = OUT_DIR / "topology_alignment_modes45_baselines.csv"
    pd.DataFrame(baseline_rows).to_csv(baseline_csv, index=False)

    md_path = OUT_DIR / "topology_alignment_modes45_summary.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Topology alignment (modes 4–5)\n\n")
        f.write(f"Inputs:\n- {GRID_CSV}\n- {LINES_CSV}\n- {H1_JSON}\n\n")
        f.write(pd.DataFrame(rows).to_markdown(index=False))
        f.write("\n\nBaselines:\n\n")
        f.write(pd.DataFrame(baseline_rows).to_markdown(index=False))


if __name__ == "__main__":
    main()
