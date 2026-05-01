#!/usr/bin/env python3
"""Brute-force assign the three Yukawa Gram matrices to physical sectors.

We have three 27x27 Gram matrices coming from the H1 decomposition.  The
physical interpretation could be {up quark, down quark, charged lepton} in
some order.  This script tries all six permutations and scores each assignment
based on how well the CKM matrix from the first two matches experiment and how
close the Koide parameter of the third is to 2/3.

Usage::

    python scripts/yukawa_sector_assignment.py

Results are printed and the best assignment saved to
``data/yukawa_sector_assignment.json``.
"""

from __future__ import annotations

import itertools
import json

# ensure repo root on path
import os
import sys
from pathlib import Path

import numpy as np

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_root)

from scripts.ckm_from_grams import V_CKM_exp, compute_ckm
from scripts.yukawa_analysis import koide_parameter, load_gram_list, masses_GeV

sectors = ["up", "down", "lepton"]


def ckmlike_error(Gup: np.ndarray, Gdown: np.ndarray) -> float:
    CKM = compute_ckm(Gup, Gdown)
    # simple Frobenius norm of difference
    return np.linalg.norm(CKM - V_CKM_exp)


def koide_error(Glep: np.ndarray) -> float:
    eigs = np.linalg.eigvalsh(np.array(Glep, dtype=float))
    eigs.sort()
    sqrt_eigs = np.sqrt(eigs)
    top3 = sqrt_eigs[-3:]
    Q = koide_parameter(top3[0], top3[1], top3[2])
    return abs(Q - 2 / 3)


def mass_ratio_error(pred: np.ndarray, actual: tuple[float, float, float]) -> float:
    """Compare predicted eigenvalue set with three physical masses.

    We compute the two inter-generation ratios m2/m1 and m3/m1 and return the
    sum of squared relative differences.  This gives a simple quantitative
    penalty for how well the hierarchy matches experiment.
    """
    if pred.size < 3:
        return float("inf")
    r_pred = (pred[1] / pred[0], pred[2] / pred[0])
    r_actual = (actual[1] / actual[0], actual[2] / actual[0])
    return sum(((rp - ra) / ra) ** 2 for rp, ra in zip(r_pred, r_actual))


def main():
    grams = load_gram_list()
    if len(grams) < 3:
        print("need three Gram matrices, run cycle_space_decompose.py first")
        sys.exit(1)

    best = None
    results = []
    for perm in itertools.permutations(range(3)):
        Gup = np.array(grams[perm[0]], dtype=float)
        Gdown = np.array(grams[perm[1]], dtype=float)
        Glep = np.array(grams[perm[2]], dtype=float)
        ckm_err = ckmlike_error(Gup, Gdown)
        koide_err = koide_error(Glep)

        # compute predicted light masses if largest eigenlet scaled to heavy mass
        def scaled_masses(G, heavy_mass):
            vals = np.linalg.eigvalsh(G)
            vals.sort()
            sqrt_vals = np.sqrt(vals)
            scale = heavy_mass / sqrt_vals[-1]
            return scale * sqrt_vals

        # heavy masses for each sector
        heavy = {
            "up": masses_GeV["t"],
            "down": masses_GeV["b"],
            "lepton": masses_GeV["τ"],
        }
        pred_up = scaled_masses(Gup, heavy["up"])
        pred_down = scaled_masses(Gdown, heavy["down"])
        pred_lep = scaled_masses(Glep, heavy["lepton"])

        # compare to actual experimental masses
        actual = {
            "up": (masses_GeV["u"], masses_GeV["c"], masses_GeV["t"]),
            "down": (masses_GeV["d"], masses_GeV["s"], masses_GeV["b"]),
            "lepton": (masses_GeV["e"], masses_GeV["μ"], masses_GeV["τ"]),
        }
        mass_err = (
            mass_ratio_error(pred_up, actual["up"])
            + mass_ratio_error(pred_down, actual["down"])
            + mass_ratio_error(pred_lep, actual["lepton"])
        )

        # also compute best-fit scale factor for each sector and resulting heavy-mass prediction
        def fit_scale(
            pred: np.ndarray, target: tuple[float, float, float]
        ) -> tuple[float, float]:
            # least-squares scale through origin
            vec = pred[:3]
            targ = np.array(target, dtype=float)
            scale = (
                float(np.dot(vec, targ) / np.dot(vec, vec))
                if np.dot(vec, vec) > 0
                else 0.0
            )
            pred_heavy = scale * pred[-1]
            return scale, pred_heavy

        fit_up, pred_heavy_up = fit_scale(pred_up, actual["up"])
        fit_down, pred_heavy_down = fit_scale(pred_down, actual["down"])
        fit_lep, pred_heavy_lep = fit_scale(pred_lep, actual["lepton"])

        heavy_err = (
            abs(pred_heavy_up - actual["up"][2]) / actual["up"][2]
            + abs(pred_heavy_down - actual["down"][2]) / actual["down"][2]
            + abs(pred_heavy_lep - actual["lepton"][2]) / actual["lepton"][2]
        )

        score = ckm_err + koide_err + mass_err + heavy_err

        entry = {
            "perm": perm,
            "sectors": [sectors[i] for i in perm],
            "ckm_error": ckm_err,
            "koide_error": koide_err,
            "mass_error": mass_err,
            "heavy_error": heavy_err,
            "score": score,
            "fit_scales": {"up": fit_up, "down": fit_down, "lepton": fit_lep},
            "predicted_heavy_masses": {
                "up": pred_heavy_up,
                "down": pred_heavy_down,
                "lepton": pred_heavy_lep,
            },
            "predicted_masses": {
                "up": pred_up.tolist(),
                "down": pred_down.tolist(),
                "lepton": pred_lep.tolist(),
            },
        }
        results.append(entry)
        if best is None or score < best["score"]:
            best = entry

    print("Assignment results (lower score better):")
    for r in sorted(results, key=lambda x: x["score"]):
        print(r)

    print("\nBest assignment:", best)
    Path("data").mkdir(exist_ok=True)
    json.dump(
        {"results": results, "best": best},
        open("data/yukawa_sector_assignment.json", "w"),
        indent=2,
    )
    print("saved data/yukawa_sector_assignment.json")


if __name__ == "__main__":
    main()
