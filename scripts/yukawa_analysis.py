#!/usr/bin/env python3
"""Simple command-line tool to examine Yukawa eigenvalue predictions.

Reads the three 27x27 Gram matrices computed by
`tools/cycle_space_decompose.py` and prints a table of eigenvalue
hierarchies, Koide parameters, and the closest match to known fermion
mass ratios.

Usage::

    python scripts/yukawa_analysis.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

masses_GeV = {
    "u": 0.00216,
    "c": 1.27,
    "t": 172.4,
    "d": 0.00467,
    "s": 0.093,
    "b": 4.18,
    "e": 0.000511,
    "μ": 0.1057,
    "τ": 1.777,
}


def koide_parameter(m1: float, m2: float, m3: float) -> float:
    """Compute Q = (m1+m2+m3)/(sqrt(m1)+sqrt(m2)+sqrt(m3))^2."""
    sum_m = m1 + m2 + m3
    sum_sqrt = np.sqrt(m1) + np.sqrt(m2) + np.sqrt(m3)
    return float(sum_m / sum_sqrt**2)


def load_gram_list(path: Path | str = "data/h1_subspaces.json") -> list[np.ndarray]:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(
            f"{path} not found; run tools/cycle_space_decompose.py first"
        )
    data = json.load(open(path))
    return [np.array(G, dtype=float) for G in data.get("gram_matrices", [])]


def main():
    path = Path("data/h1_subspaces.json")
    if not path.is_file():
        print(
            "ERROR: data/h1_subspaces.json not found. Run tools/cycle_space_decompose.py first."
        )
        sys.exit(1)

    data = json.load(open(path))
    gram_list = data.get("gram_matrices", [])

    # attempt to fetch updated fermion masses
    try:
        from scripts.experimental_data import fetch_fermion_masses_from_wikipedia

        fm = fetch_fermion_masses_from_wikipedia()
        if fm:
            print("Using fetched fermion masses from Wikipedia:", fm)
            masses = fm
        else:
            masses = masses_GeV
    except Exception:
        masses = masses_GeV
    exp_ratios = {
        "tau/mu": masses["τ"] / masses["μ"],
        "mu/e": masses["μ"] / masses["e"],
        "tau/e": masses["τ"] / masses["e"],
        "b/s": masses["b"] / masses["s"],
        "s/d": masses["s"] / masses["d"],
        "b/d": masses["b"] / masses["d"],
        "t/c": masses["t"] / masses["c"],
        "c/u": masses["c"] / masses["u"],
        "t/u": masses["t"] / masses["u"],
    }

    print("Yukawa eigenvalue analysis from W33 H1 subspaces")
    print("data file:", path)
    print("number of subspaces:", len(gram_list))

    for idx, G in enumerate(gram_list):
        Gmat = np.array(G, dtype=float)
        eigs = np.linalg.eigvalsh(Gmat)
        eigs.sort()
        sqrt_eigs = np.sqrt(eigs)
        ratio = sqrt_eigs[-1] / sqrt_eigs[0]
        print(f"\nSubspace {idx} (dim {Gmat.shape[0]})")
        print(
            f"  sqrt eigenvalues: min {sqrt_eigs[0]:.4f}, max {sqrt_eigs[-1]:.4f}, ratio {ratio:.3f}"
        )

        best = min(exp_ratios.items(), key=lambda kv: abs(kv[1] - ratio) / kv[1])
        print(
            f"  Best match to experimental ratio: {best[0]} = {best[1]:.3f}, rel diff {abs(best[1]-ratio)/best[1]:.1%}"
        )
        # Koide for top 3
        top3 = sqrt_eigs[-3:]
        Q = koide_parameter(top3[0], top3[1], top3[2])
        print(f"  Koide parameter (largest 3): {Q:.6f}")

        # try scaling the spectrum to physical masses
        def scale_and_predict(target_label, target_mass):
            s = target_mass / sqrt_eigs[-1]
            preds = s * sqrt_eigs
            return s, preds

        print("  mass prediction trials:")
        for label, mass in [
            ("tau", masses_GeV["τ"]),
            ("top", masses_GeV["t"]),
            ("bottom", masses_GeV["b"]),
        ]:
            s, preds = scale_and_predict(label, mass)
            print(
                f"    assume largest eigen scaled to {label} ({mass:.3g} GeV): scale={s:.3e}"
            )
            print(
                f"      predicted second/first ratios: {preds[-2]/preds[0]:.3f}, {preds[-1]/preds[-2]:.3f}"
            )

    print("\nDone.")


if __name__ == "__main__":
    main()
