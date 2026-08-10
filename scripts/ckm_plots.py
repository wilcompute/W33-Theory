#!/usr/bin/env python3
"""
Generate CKM diagnostic plots from data produced by the CKM pipeline.

Produces PNGs in `reports/`:
 - `ckm_unitarity_hist.png`
 - `ckm_jarlskog_hist.png`
 - `ckm_unit_vs_j_scatter.png`
 - `ckm_matrices.png` (overlap / scaled / experimental side-by-side)
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def ensure_reports_dir():
    p = Path("reports")
    p.mkdir(exist_ok=True)
    return p


def plot_histograms(sample_stats_path: Path, out_dir: Path):
    data = load_json(sample_stats_path)
    if not data:
        print(f"{sample_stats_path} missing; skipping histograms")
        return []

    results = data.get("results", [])
    unitary = np.array([r.get("unitarity_err", np.nan) for r in results])
    jvals = np.array([r.get("jarlskog", np.nan) for r in results])

    files = []
    if unitary.size:
        plt.figure(figsize=(6, 4))
        plt.hist(unitary, bins=30, color="#1f77b4", alpha=0.8)
        plt.xlabel("Unitary error ||V V^† - I||")
        plt.ylabel("Count")
        plt.title("Distribution of unitarity error (samples)")
        f1 = out_dir / "ckm_unitarity_hist.png"
        plt.tight_layout()
        plt.savefig(f1)
        plt.close()
        files.append(str(f1))

    if jvals.size:
        plt.figure(figsize=(6, 4))
        plt.hist(jvals, bins=30, color="#ff7f0e", alpha=0.8)
        plt.xlabel("Jarlskog invariant J")
        plt.ylabel("Count")
        plt.title("Distribution of Jarlskog (samples)")
        f2 = out_dir / "ckm_jarlskog_hist.png"
        plt.tight_layout()
        plt.savefig(f2)
        plt.close()
        files.append(str(f2))

    if unitary.size and jvals.size:
        plt.figure(figsize=(6, 5))
        plt.scatter(unitary, np.abs(jvals), s=30, c="#2ca02c", alpha=0.8)
        plt.xlabel("Unitary error")
        plt.ylabel("|Jarlskog|")
        plt.title("Unitary error vs |Jarlskog| (samples)")
        f3 = out_dir / "ckm_unit_vs_j_scatter.png"
        plt.tight_layout()
        plt.savefig(f3)
        plt.close()
        files.append(str(f3))

    return files


def plot_matrices(overlap_path: Path, fitted_path: Path, phase_rec_path: Path, out_dir: Path):
    d_ov = load_json(overlap_path) or {}
    M = np.array(d_ov.get("overlap_matrix", []), dtype=float) if d_ov else None
    exp = np.array(d_ov.get("experimental", []), dtype=float) if d_ov else None

    d_fit = load_json(fitted_path) or {}
    scaled = np.array(d_fit.get("scaled_matrix", []), dtype=float) if d_fit else None

    d_pr = load_json(phase_rec_path) or {}
    rec = np.array(d_pr.get("abs2", []), dtype=float) if d_pr else None

    mats = [M, scaled, exp, rec]
    labels = ["overlap", "scaled", "experimental", "reconstructed_abs2"]

    # pick up to 4 panels depending on availability
    panels = [(lab, mat) for lab, mat in zip(labels, mats) if mat is not None and mat.size]
    if not panels:
        print("No matrices found to plot; skipping matrix panel")
        return []

    n = len(panels)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
    if n == 1:
        axes = [axes]

    for ax, (lab, mat) in zip(axes, panels):
        im = ax.imshow(mat, cmap="viridis", vmin=0)
        ax.set_title(lab)
        for (i, j), val in np.ndenumerate(mat):
            ax.text(j, i, f"{val:.3f}", ha="center", va="center", color="white", fontsize=8)
    fig.colorbar(im, ax=axes, fraction=0.02)
    out = out_dir / "ckm_matrices.png"
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return [str(out)]


def main():
    rpt = ensure_reports_dir()
    files = []
    files += plot_histograms(Path("data/ckm_sample_stats.json"), rpt)
    files += plot_matrices(
        Path("data/ckm_from_grams.json"),
        Path("data/ckm_fitted_scalings.json"),
        Path("data/ckm_phase_reconstruction.json"),
        rpt,
    )

    if files:
        print("Saved plots:")
        for f in files:
            print("  ", f)
    else:
        print("No plots generated.")


if __name__ == "__main__":
    main()
